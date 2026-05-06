from __future__ import annotations

from typing import Iterable


REQUIRED_LAYERS = (
    "Science",
    "IP",
    "Industrialization",
    "Adoption",
    "Policy & Economics",
)

REQUIRED_LAYER_METRICS = {
    "Science": (
        "publication_growth",
        "citation_velocity_or_quality",
        "science_to_application_linkage",
    ),
    "IP": (
        "patent_family_growth",
        "technical_specificity",
        "science_to_patent_or_assignee_quality",
    ),
    "Industrialization": (
        "manufacturing_or_deployment_evidence",
        "process_learning_or_capex",
        "operational_scale_signal",
    ),
    "Adoption": (
        "revenue_or_booking_evidence",
        "customer_or_partner_breadth",
        "repeatability_or_deployment_scale",
    ),
    "Policy & Economics": (
        "regulatory_or_standards_fit",
        "policy_or_supply_chain_support",
        "economic_readiness",
    ),
}

REQUIRED_DASHBOARD_CONTENT_SECTIONS = (
    "hero",
    "thesis",
    "technology_map",
    "quantitative_signals",
    "commercialization_evidence",
    "breakthrough_gate",
    "university_research_signals",
    "patent_signals",
    "red_flags",
    "watchlist",
    "operational_snapshot",
    "method_notes",
    "bottom_line",
)

ALLOWED_CLAIM_TYPES = {
    "sourced_fact",
    "inference",
    "limitation",
    "forecast",
    "monitoring_trigger",
}

ALLOWED_CLAIM_CONFIDENCE = {"High", "Medium", "Low"}

METRIC_RULES_VERSION = "1.2.0"


def clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


def format_score(value: float) -> str:
    rounded = round(value, 1)
    if rounded.is_integer():
        return str(int(rounded))
    return f"{rounded:.1f}"


def confidence_label(coverage_ratio: float) -> str:
    if coverage_ratio >= 0.85:
        return "High"
    if coverage_ratio >= 0.65:
        return "Medium"
    return "Low"


def confidence_penalty(coverage_ratio: float) -> float:
    return 0.6 + 0.4 * clamp(coverage_ratio, 0.0, 1.0)


def absolute_verdict(total_score: float) -> str:
    if total_score >= 20:
        return "Exceptional innovator and plausible scale-up candidate"
    if total_score >= 15:
        return "Strong innovator with translational momentum"
    if total_score >= 9:
        return "Emerging innovator worth monitoring"
    return "Scientifically interesting but early"


def normalize_min_max(value: float, floor: float, cap: float) -> float:
    if cap <= floor:
        raise ValueError("cap must be greater than floor")
    return clamp((value - floor) / (cap - floor), 0.0, 1.0)


def normalize_log(value: float, cap: float) -> float:
    import math

    if cap <= 0:
        raise ValueError("cap must be positive")
    return clamp(math.log1p(max(0.0, value)) / math.log1p(cap), 0.0, 1.0)


def normalize_growth(start_value: float, end_value: float, years: float, floor: float, cap: float) -> float:
    if years <= 0:
        raise ValueError("years must be positive")
    if start_value <= 0 or end_value < 0:
        raise ValueError("growth normalization requires positive start_value and non-negative end_value")
    annualized_growth = (end_value / start_value) ** (1.0 / years) - 1.0
    return normalize_min_max(annualized_growth, floor, cap)


def _version_tuple(version: str) -> tuple[int, ...]:
    parts: list[int] = []
    for part in version.split("."):
        try:
            parts.append(int(part))
        except ValueError:
            break
    return tuple(parts or [0])


def _iter_reference_lists(value, key_name: str):
    if isinstance(value, dict):
        for key, child in value.items():
            if key == key_name and isinstance(child, list):
                yield child
            else:
                yield from _iter_reference_lists(child, key_name)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_reference_lists(child, key_name)


def _validate_references(value, key_name: str, allowed_ids: set[str], label: str) -> None:
    for ids in _iter_reference_lists(value, key_name):
        unknown = [item_id for item_id in ids if item_id not in allowed_ids]
        if unknown:
            raise ValueError(f"{label} references unknown {key_name}: " + ", ".join(str(item) for item in unknown))


def _validate_claims(claims: list[dict], source_ids: set[str], evidence_ids: set[str]) -> set[str]:
    claim_ids: set[str] = set()
    for claim in claims:
        claim_id = claim.get("claim_id")
        if not claim_id:
            raise ValueError("every claim must define claim_id")
        if claim_id in claim_ids:
            raise ValueError(f"duplicate claim_id: {claim_id}")
        claim_ids.add(claim_id)

        if not claim.get("section"):
            raise ValueError(f"Claim {claim_id} must define section")
        if not claim.get("text"):
            raise ValueError(f"Claim {claim_id} must define text")
        if claim.get("claim_type") not in ALLOWED_CLAIM_TYPES:
            raise ValueError(f"Claim {claim_id} must define a valid claim_type")
        if claim.get("confidence") not in ALLOWED_CLAIM_CONFIDENCE:
            raise ValueError(f"Claim {claim_id} must define confidence as High, Medium, or Low")

        claim_source_ids = claim.get("source_ids", [])
        if claim_source_ids:
            unknown = [source_id for source_id in claim_source_ids if source_id not in source_ids]
            if unknown:
                raise ValueError(f"Claim {claim_id} references unknown source_ids: " + ", ".join(unknown))

        claim_evidence_ids = claim.get("evidence_ids", [])
        if claim_evidence_ids:
            unknown = [evidence_id for evidence_id in claim_evidence_ids if evidence_id not in evidence_ids]
            if unknown:
                raise ValueError(f"Claim {claim_id} references unknown evidence_ids: " + ", ".join(unknown))

        if claim.get("claim_type") in {"sourced_fact", "inference", "limitation"} and not (
            claim_source_ids or claim_evidence_ids
        ):
            raise ValueError(f"Claim {claim_id} must link to source_ids or evidence_ids")

    return claim_ids


def _validate_dashboard_content(
    dashboard_content: dict,
    claims: list[dict],
    source_ids: set[str],
    evidence_ids: set[str],
) -> None:
    if not isinstance(dashboard_content, dict):
        raise ValueError("schema_version 2.1+ payloads must define dashboard_content as an object")
    if not isinstance(claims, list) or not claims:
        raise ValueError("schema_version 2.1+ payloads must define a non-empty claims list")

    missing_sections = [section for section in REQUIRED_DASHBOARD_CONTENT_SECTIONS if section not in dashboard_content]
    if missing_sections:
        raise ValueError("dashboard_content is missing required sections: " + ", ".join(missing_sections))

    claim_ids = _validate_claims(claims, source_ids, evidence_ids)
    _validate_references(dashboard_content, "source_ids", source_ids, "dashboard_content")
    _validate_references(dashboard_content, "evidence_ids", evidence_ids, "dashboard_content")
    _validate_references(dashboard_content, "claim_ids", claim_ids, "dashboard_content")


def validate_payload_shape(payload: dict) -> None:
    layers = payload.get("layers")
    if not isinstance(layers, list) or not layers:
        raise ValueError("payload must contain a non-empty 'layers' list")

    schema_version = str(payload.get("schema_version", "1.0"))
    schema_tuple = _version_tuple(schema_version)
    strict_evidence_schema = schema_tuple >= (2, 0)
    strict_dashboard_schema = schema_tuple >= (2, 1)
    evidence_ids = set()
    source_ids = set()
    if strict_evidence_schema:
        sources = payload.get("sources")
        evidence_items = payload.get("evidence_items")
        if not isinstance(sources, list) or not sources:
            raise ValueError("schema_version 2.x payloads must contain a non-empty 'sources' list")
        if not isinstance(evidence_items, list) or not evidence_items:
            raise ValueError("schema_version 2.x payloads must contain a non-empty 'evidence_items' list")

        source_ids = {source.get("source_id") for source in sources}
        if None in source_ids:
            raise ValueError("every source must define source_id")

        for item in evidence_items:
            evidence_id = item.get("evidence_id")
            if not evidence_id:
                raise ValueError("every evidence item must define evidence_id")
            if item.get("source_id") not in source_ids:
                raise ValueError(f"Evidence item {evidence_id} references an unknown source_id")
            evidence_ids.add(evidence_id)

    if strict_dashboard_schema:
        _validate_dashboard_content(
            payload.get("dashboard_content"),
            payload.get("claims"),
            source_ids,
            evidence_ids,
        )

    labels = [layer.get("label") for layer in layers]
    missing_layers = [label for label in REQUIRED_LAYERS if label not in labels]
    if missing_layers:
        raise ValueError(f"payload is missing required layers: {', '.join(missing_layers)}")

    for layer in layers:
        label = layer.get("label")
        metrics = layer.get("metrics")
        if not isinstance(metrics, list) or not metrics:
            raise ValueError(f"Layer {label} must define a non-empty 'metrics' list")

        total_weight = sum(metric.get("weight", 0.0) for metric in metrics)
        if abs(total_weight - 1.0) > 1e-6:
            raise ValueError(f"Layer {label} weights must sum to 1.0")

        for metric in metrics:
            value = metric.get("value")
            if value is None or not (0.0 <= value <= 1.0):
                raise ValueError(f"Layer {label} metric values must be normalized to 0..1")
            if strict_evidence_schema:
                metric_evidence_ids = metric.get("evidence_ids")
                if not isinstance(metric_evidence_ids, list) or not metric_evidence_ids:
                    raise ValueError(f"Layer {label} metric {metric.get('code')} must define evidence_ids")
                unknown = [evidence_id for evidence_id in metric_evidence_ids if evidence_id not in evidence_ids]
                if unknown:
                    raise ValueError(
                        f"Layer {label} metric {metric.get('code')} references unknown evidence_ids: "
                        + ", ".join(unknown)
                    )
                if not isinstance(metric.get("normalization"), dict):
                    raise ValueError(f"Layer {label} metric {metric.get('code')} must define normalization metadata")


def weighted_average(pairs: Iterable[tuple[float, float]]) -> float:
    total_weight = 0.0
    weighted_sum = 0.0
    for value, weight in pairs:
        weighted_sum += value * weight
        total_weight += weight
    if total_weight <= 0:
        raise ValueError("weighted_average requires positive total weight")
    return weighted_sum / total_weight
