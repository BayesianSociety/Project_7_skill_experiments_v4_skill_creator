from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from metric_rules import (
    METRIC_RULES_VERSION,
    absolute_verdict,
    clamp,
    confidence_label,
    confidence_penalty,
    format_score,
    validate_payload_shape,
    weighted_average,
)

SCORER_VERSION = "1.2.0"


def score_payload(payload: dict[str, Any]) -> dict[str, Any]:
    validate_payload_shape(payload)
    layers_out: list[dict[str, Any]] = []
    total_score = 0.0

    for layer in payload["layers"]:
        metrics = layer["metrics"]
        normalized_score = weighted_average((metric["value"], metric["weight"]) for metric in metrics)
        normalized_score = clamp(normalized_score, 0.0, 1.0)

        coverage_ratio = clamp(layer.get("coverage_ratio", 1.0), 0.0, 1.0)
        penalty = layer.get("confidence_penalty")
        if penalty is None:
            penalty = confidence_penalty(coverage_ratio)
        penalty = clamp(penalty, 0.0, 1.0)

        raw_score = 5.0 * normalized_score
        final_score = raw_score * penalty

        cap_reasons: list[str] = []
        for cap in layer.get("caps", []):
            if cap.get("active"):
                final_score = min(final_score, float(cap["max_score"]))
                cap_reasons.append(cap["reason"])

        final_score = round(clamp(final_score, 0.0, 5.0), 1)
        total_score += final_score

        layers_out.append(
            {
                "label": layer["label"],
                "score": final_score,
                "display_score": format_score(final_score),
                "raw_score": round(raw_score, 3),
                "normalized_score": round(normalized_score, 4),
                "coverage_ratio": round(coverage_ratio, 4),
                "confidence_penalty": round(penalty, 4),
                "confidence": layer.get("confidence") or confidence_label(coverage_ratio),
                "summary": layer["summary"],
                "strong": layer["strong"],
                "missing": layer["missing"],
                "metrics": metrics,
                "cap_reasons": cap_reasons,
            }
        )

    total_score = round(total_score, 1)
    layer_lookup = {layer["label"]: layer for layer in layers_out}
    industrial = layer_lookup.get("Industrialization", {})
    adoption = layer_lookup.get("Adoption", {})
    gate_pass = (
        industrial.get("score", 0.0) >= 3.0
        and adoption.get("score", 0.0) >= 3.0
        and industrial.get("confidence_penalty", 0.0) >= 0.8
        and adoption.get("confidence_penalty", 0.0) >= 0.8
    )

    verdict = payload.get("verdict_override") or absolute_verdict(total_score)

    scored: dict[str, Any] = {
        "schema_version": payload.get("schema_version", "1.0"),
        "company": payload.get("company"),
        "ticker": payload.get("ticker"),
        "mode": payload.get("mode", "absolute"),
        "skill_metadata": payload.get("skill_metadata"),
        "research_run": payload.get("research_run"),
        "research_context": payload.get("research_context"),
        "sources": payload.get("sources", []),
        "evidence_items": payload.get("evidence_items", []),
        "normalization_notes": payload.get("normalization_notes", []),
        "dashboard_content": payload.get("dashboard_content"),
        "claims": payload.get("claims"),
        "layers": layers_out,
        "total_score": total_score,
        "display_total_score": format_score(total_score),
        "gate_pass": gate_pass,
        "verdict": verdict,
        "benchmark_ready": payload.get("benchmark_ready", True),
        "storage_metadata": payload.get("storage_metadata"),
        "scorer_metadata": {
            "scorer_name": "score_innovation_benchmark.py",
            "scorer_version": SCORER_VERSION,
            "metric_rules_version": METRIC_RULES_VERSION,
            "formula": "layer_score = 5 * confidence_penalty * sum(weight_i * metric_i_value)",
        },
    }
    return {key: value for key, value in scored.items() if value is not None}


def _main() -> int:
    parser = argparse.ArgumentParser(description="Score a structured technology innovation benchmark payload.")
    parser.add_argument("input", help="Path to input JSON payload.")
    parser.add_argument("-o", "--output", help="Optional path to write scored JSON output.")
    args = parser.parse_args()

    input_path = Path(args.input)
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    scored = score_payload(payload)
    output_text = json.dumps(scored, indent=2, ensure_ascii=True) + "\n"

    if args.output:
        Path(args.output).write_text(output_text, encoding="utf-8")
    else:
        print(output_text, end="")

    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
