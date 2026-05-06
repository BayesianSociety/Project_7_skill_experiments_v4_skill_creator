#!/usr/bin/env python3
"""Local SQLite storage system for innovation-analysis JSON artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_DB = ROOT / "storage.db"
SCHEMA_FILE = ROOT / "schema.sql"


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value or "unknown"


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))


def pretty_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def as_bool_int(value: Any) -> int | None:
    if value is None:
        return None
    return 1 if bool(value) else 0


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        loaded = json.load(handle)
    if not isinstance(loaded, dict):
        raise ValueError(f"{path} does not contain a JSON object")
    return loaded


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path: Path) -> None:
    if not SCHEMA_FILE.exists():
        raise FileNotFoundError(f"Missing schema file: {SCHEMA_FILE}")
    with connect(db_path) as conn:
        conn.executescript(SCHEMA_FILE.read_text(encoding="utf-8"))


def parse_ticker(ticker: str | None) -> tuple[str | None, str | None]:
    if not ticker:
        return None, None
    if ":" in ticker:
        exchange, value = ticker.split(":", 1)
        return exchange.strip(), value.strip()
    return None, ticker.strip()


def upsert_company(conn: sqlite3.Connection, company_name: str, ticker: str | None, identifiers: dict[str, Any]) -> int:
    slug = slugify(company_name)
    conn.execute(
        """
        INSERT INTO companies (legal_name, display_name, slug, metadata_json)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(slug) DO UPDATE SET
            legal_name = excluded.legal_name,
            display_name = excluded.display_name,
            metadata_json = excluded.metadata_json,
            updated_at = datetime('now')
        """,
        (company_name, company_name, slug, stable_json({"source_identifiers": identifiers})),
    )
    company_id = conn.execute("SELECT id FROM companies WHERE slug = ?", (slug,)).fetchone()["id"]

    exchange, ticker_value = parse_ticker(ticker)
    if ticker_value:
        conn.execute(
            """
            INSERT OR IGNORE INTO company_identifiers
                (company_id, identifier_type, identifier_value, exchange, is_primary)
            VALUES (?, 'ticker', ?, ?, 1)
            """,
        (company_id, ticker_value, exchange or ""),
        )

    cik = identifiers.get("cik")
    if cik:
        conn.execute(
            """
            INSERT OR IGNORE INTO company_identifiers
                (company_id, identifier_type, identifier_value, is_primary)
            VALUES (?, 'cik', ?, 0)
            """,
            (company_id, str(cik)),
        )

    return company_id


def upsert_framework(conn: sqlite3.Connection, payload: dict[str, Any], scored: dict[str, Any] | None) -> int:
    merged = payload if payload else scored or {}
    skill = merged.get("skill_metadata") or {}
    scorer = (scored or {}).get("scorer_metadata") or {}

    name = skill.get("skill_name") or "legacy-innovation-analysis"
    version = skill.get("skill_version") or merged.get("schema_version") or "legacy"
    schema_version = merged.get("schema_version") or "legacy"
    scorer_name = scorer.get("scorer_name") or skill.get("scorer_name") or ""
    scorer_version = scorer.get("scorer_version") or skill.get("scorer_version") or ""
    metric_rules_version = scorer.get("metric_rules_version") or skill.get("metric_rules_version") or ""

    definition = {
        "skill_metadata": skill,
        "scorer_metadata": scorer,
        "schema_version": schema_version,
    }
    conn.execute(
        """
        INSERT INTO analysis_frameworks
            (name, version, schema_version, scorer_name, scorer_version, metric_rules_version, definition_json)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (
            name,
            version,
            schema_version,
            scorer_name,
            scorer_version,
            metric_rules_version
        ) DO UPDATE SET definition_json = excluded.definition_json
        """,
        (name, version, schema_version, scorer_name, scorer_version, metric_rules_version, stable_json(definition)),
    )
    row = conn.execute(
        """
        SELECT id FROM analysis_frameworks
        WHERE name = ?
          AND version = ?
          AND schema_version = ?
          AND scorer_name = ?
          AND scorer_version = ?
          AND metric_rules_version = ?
        """,
        (name, version, schema_version, scorer_name, scorer_version, metric_rules_version),
    ).fetchone()
    return int(row["id"])


def derive_run_uid(stem: str, payload: dict[str, Any], scored: dict[str, Any] | None) -> str:
    run = payload.get("research_run") or (scored or {}).get("research_run") or {}
    if run.get("run_id"):
        return str(run["run_id"])
    return stem


def source_dedupe_key(source: dict[str, Any]) -> str:
    url = (source.get("url") or "").strip()
    if url:
        return "url:" + url.lower()
    parts = [
        source.get("title") or "",
        source.get("publisher") or "",
        source.get("document_date") or "",
        source.get("source_type") or "",
    ]
    return "source:" + "|".join(str(part).strip().lower() for part in parts)


def insert_sources(conn: sqlite3.Connection, run_id: int, payload: dict[str, Any], scored: dict[str, Any] | None) -> dict[str, int]:
    source_map: dict[str, int] = {}
    source_items = payload.get("sources") or (scored or {}).get("sources") or []
    if not isinstance(source_items, list):
        return source_map

    for source in source_items:
        if not isinstance(source, dict):
            continue
        local_source_id = str(source.get("source_id") or f"source_{len(source_map) + 1}")
        url_hash = sha256_text(source_dedupe_key(source))
        conn.execute(
            """
            INSERT INTO sources
                (canonical_url, url_hash, title, publisher, source_type, document_date,
                 reliability, availability, notes, metadata_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(url_hash) DO UPDATE SET
                canonical_url = COALESCE(excluded.canonical_url, sources.canonical_url),
                title = COALESCE(excluded.title, sources.title),
                publisher = COALESCE(excluded.publisher, sources.publisher),
                source_type = COALESCE(excluded.source_type, sources.source_type),
                document_date = COALESCE(excluded.document_date, sources.document_date),
                reliability = COALESCE(excluded.reliability, sources.reliability),
                availability = COALESCE(excluded.availability, sources.availability),
                notes = COALESCE(excluded.notes, sources.notes),
                metadata_json = excluded.metadata_json,
                updated_at = datetime('now')
            """,
            (
                source.get("url"),
                url_hash,
                source.get("title"),
                source.get("publisher"),
                source.get("source_type"),
                source.get("document_date"),
                source.get("reliability"),
                source.get("availability"),
                source.get("notes"),
                stable_json({"dedupe_key": source_dedupe_key(source)}),
            ),
        )
        source_id = conn.execute("SELECT id FROM sources WHERE url_hash = ?", (url_hash,)).fetchone()["id"]
        source_map[local_source_id] = int(source_id)
        conn.execute(
            """
            INSERT INTO run_source_refs
                (analysis_run_id, source_id, local_source_id, accessed_at, raw_source_json)
            VALUES (?, ?, ?, ?, ?)
            """,
            (run_id, source_id, local_source_id, source.get("accessed_at"), stable_json(source)),
        )
    return source_map


def insert_evidence(
    conn: sqlite3.Connection,
    run_id: int,
    payload: dict[str, Any],
    scored: dict[str, Any] | None,
    source_map: dict[str, int],
) -> dict[str, int]:
    evidence_map: dict[str, int] = {}
    evidence_items = payload.get("evidence_items") or (scored or {}).get("evidence_items") or []
    if not isinstance(evidence_items, list):
        return evidence_map

    for evidence in evidence_items:
        if not isinstance(evidence, dict):
            continue
        local_evidence_id = str(evidence.get("evidence_id") or f"ev_{len(evidence_map) + 1:03d}")
        layer_label = evidence.get("layer")
        metric_codes = evidence.get("metric_codes") if isinstance(evidence.get("metric_codes"), list) else []
        source_id = source_map.get(str(evidence.get("source_id")))
        conn.execute(
            """
            INSERT INTO evidence_items
                (analysis_run_id, source_id, local_evidence_id, layer_code, layer_label,
                 fact_type, fact, quote_or_excerpt, raw_value, raw_unit, period_start,
                 period_end, company_attributable, field_proxy, location, verified,
                 limitations, metric_codes_json, raw_evidence_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run_id,
                source_id,
                local_evidence_id,
                slugify(str(layer_label or "")),
                layer_label,
                evidence.get("fact_type"),
                evidence.get("fact"),
                evidence.get("quote_or_excerpt"),
                evidence.get("raw_value") if isinstance(evidence.get("raw_value"), (int, float)) else None,
                evidence.get("raw_unit"),
                evidence.get("period_start"),
                evidence.get("period_end"),
                as_bool_int(evidence.get("company_attributable")),
                as_bool_int(evidence.get("field_proxy")),
                evidence.get("location"),
                as_bool_int(evidence.get("verified")),
                evidence.get("limitations"),
                stable_json(metric_codes),
                stable_json(evidence),
            ),
        )
        evidence_id = conn.execute(
            "SELECT id FROM evidence_items WHERE analysis_run_id = ? AND local_evidence_id = ?",
            (run_id, local_evidence_id),
        ).fetchone()["id"]
        evidence_map[local_evidence_id] = int(evidence_id)
    return evidence_map


def choose_layers(payload: dict[str, Any], scored: dict[str, Any] | None) -> list[dict[str, Any]]:
    scored_layers = (scored or {}).get("layers")
    if isinstance(scored_layers, list):
        return [layer for layer in scored_layers if isinstance(layer, dict)]
    payload_layers = payload.get("layers")
    if isinstance(payload_layers, list):
        return [layer for layer in payload_layers if isinstance(layer, dict)]
    return []


def insert_layers_and_metrics(
    conn: sqlite3.Connection,
    run_id: int,
    payload: dict[str, Any],
    scored: dict[str, Any] | None,
    evidence_map: dict[str, int],
) -> None:
    for index, layer in enumerate(choose_layers(payload, scored)):
        label = str(layer.get("label") or f"Layer {index + 1}")
        layer_code = slugify(label)
        conn.execute(
            """
            INSERT INTO analysis_layers
                (analysis_run_id, layer_code, label, sort_order, summary, strong, missing,
                 coverage_ratio, score, raw_score, normalized_score, confidence,
                 confidence_penalty, display_score, caps_json, cap_reasons_json, raw_layer_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run_id,
                layer_code,
                label,
                index,
                layer.get("summary"),
                layer.get("strong"),
                layer.get("missing"),
                layer.get("coverage_ratio"),
                layer.get("score"),
                layer.get("raw_score"),
                layer.get("normalized_score"),
                layer.get("confidence"),
                layer.get("confidence_penalty"),
                layer.get("display_score"),
                stable_json(layer.get("caps") if isinstance(layer.get("caps"), list) else []),
                stable_json(layer.get("cap_reasons") if isinstance(layer.get("cap_reasons"), list) else []),
                stable_json(layer),
            ),
        )
        layer_id = conn.execute(
            "SELECT id FROM analysis_layers WHERE analysis_run_id = ? AND layer_code = ?",
            (run_id, layer_code),
        ).fetchone()["id"]

        metrics = layer.get("metrics") if isinstance(layer.get("metrics"), list) else []
        for metric in metrics:
            if not isinstance(metric, dict):
                continue
            metric_code = str(metric.get("code") or f"metric_{len(metrics)}")
            normalization = metric.get("normalization") if isinstance(metric.get("normalization"), dict) else {}
            conn.execute(
                """
                INSERT INTO analysis_metrics
                    (analysis_run_id, layer_id, metric_code, label, value, weight, unit,
                     source_type, verified, normalization_method, normalization_json, raw_metric_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run_id,
                    layer_id,
                    metric_code,
                    metric.get("label"),
                    metric.get("value"),
                    metric.get("weight"),
                    metric.get("unit"),
                    metric.get("source_type"),
                    as_bool_int(metric.get("verified")),
                    normalization.get("method"),
                    stable_json(normalization),
                    stable_json(metric),
                ),
            )
            metric_id = conn.execute(
                """
                SELECT id FROM analysis_metrics
                WHERE analysis_run_id = ? AND layer_id = ? AND metric_code = ?
                """,
                (run_id, layer_id, metric_code),
            ).fetchone()["id"]

            evidence_ids = metric.get("evidence_ids") if isinstance(metric.get("evidence_ids"), list) else []
            for local_evidence_id in evidence_ids:
                linked_id = evidence_map.get(str(local_evidence_id))
                if linked_id:
                    conn.execute(
                        """
                        INSERT OR IGNORE INTO metric_evidence_links
                            (metric_id, evidence_item_id, relationship_type)
                        VALUES (?, ?, 'supports')
                        """,
                        (metric_id, linked_id),
                    )

    # Legacy or incomplete records may only link evidence to metric codes from
    # the evidence object. Add those links after all metrics exist.
    for evidence_row in conn.execute(
        "SELECT id, metric_codes_json FROM evidence_items WHERE analysis_run_id = ?",
        (run_id,),
    ).fetchall():
        metric_codes = json.loads(evidence_row["metric_codes_json"])
        for metric_code in metric_codes:
            metric_rows = conn.execute(
                "SELECT id FROM analysis_metrics WHERE analysis_run_id = ? AND metric_code = ?",
                (run_id, str(metric_code)),
            ).fetchall()
            for metric_row in metric_rows:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO metric_evidence_links
                        (metric_id, evidence_item_id, relationship_type)
                    VALUES (?, ?, 'supports')
                    """,
                    (metric_row["id"], evidence_row["id"]),
                )


def insert_output(conn: sqlite3.Connection, run_id: int, scored: dict[str, Any] | None) -> None:
    if not scored:
        return
    scorer_metadata = scored.get("scorer_metadata") if isinstance(scored.get("scorer_metadata"), dict) else {}
    conn.execute(
        """
        INSERT INTO analysis_outputs
            (analysis_run_id, total_score, display_total_score, gate_pass, verdict,
             scorer_metadata_json, formula)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            run_id,
            scored.get("total_score"),
            scored.get("display_total_score"),
            as_bool_int(scored.get("gate_pass")),
            scored.get("verdict"),
            stable_json(scorer_metadata),
            scorer_metadata.get("formula"),
        ),
    )


def import_pair(conn: sqlite3.Connection, payload_path: Path, scored_path: Path | None, source_dir: Path) -> str:
    payload = read_json(payload_path)
    scored = read_json(scored_path) if scored_path and scored_path.exists() else None

    stem = payload_path.name.removesuffix("_payload.json")
    merged = payload if payload else scored or {}
    company_name = str(merged.get("company") or (scored or {}).get("company") or stem)
    ticker = merged.get("ticker") or (scored or {}).get("ticker")
    research_run = merged.get("research_run") or (scored or {}).get("research_run") or {}
    research_context = merged.get("research_context") or {}
    identifiers = research_context.get("company_identifiers") if isinstance(research_context.get("company_identifiers"), dict) else {}

    company_id = upsert_company(conn, company_name, ticker, identifiers)
    framework_id = upsert_framework(conn, payload, scored)
    run_uid = derive_run_uid(stem, payload, scored)

    payload_raw = stable_json(payload)
    scored_raw = stable_json(scored) if scored else None
    import_hash = sha256_text(payload_raw + "\n" + (scored_raw or ""))

    conn.execute("DELETE FROM analysis_runs WHERE run_uid = ?", (run_uid,))
    focus_technologies = (
        research_context.get("focus_technologies")
        if isinstance(research_context.get("focus_technologies"), list)
        else merged.get("focus_technologies") if isinstance(merged.get("focus_technologies"), list) else []
    )

    conn.execute(
        """
        INSERT INTO analysis_runs
            (run_uid, company_id, framework_id, mode, research_date, analyst,
             user_request, time_horizon, research_mode, benchmark_ready,
             source_payload_file, source_scored_file, source_directory,
             focus_technologies_json, research_context_json, normalization_notes_json,
             storage_metadata_json, raw_payload_json, raw_scored_json, payload_hash,
             scored_hash, import_hash)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            run_uid,
            company_id,
            framework_id,
            merged.get("mode") or (scored or {}).get("mode"),
            research_run.get("research_date") or merged.get("research_date"),
            research_run.get("analyst"),
            research_run.get("user_request"),
            research_run.get("time_horizon"),
            research_run.get("research_mode"),
            as_bool_int(merged.get("benchmark_ready") if merged.get("benchmark_ready") is not None else (scored or {}).get("benchmark_ready")),
            str(payload_path),
            str(scored_path) if scored_path else None,
            str(source_dir),
            stable_json(focus_technologies),
            stable_json(research_context),
            stable_json(merged.get("normalization_notes") if isinstance(merged.get("normalization_notes"), list) else []),
            stable_json(merged.get("storage_metadata") if isinstance(merged.get("storage_metadata"), dict) else {}),
            payload_raw,
            scored_raw,
            sha256_text(payload_raw),
            sha256_text(scored_raw) if scored_raw else None,
            import_hash,
        ),
    )
    run_id = conn.execute("SELECT id FROM analysis_runs WHERE run_uid = ?", (run_uid,)).fetchone()["id"]

    source_map = insert_sources(conn, run_id, payload, scored)
    evidence_map = insert_evidence(conn, run_id, payload, scored, source_map)
    insert_layers_and_metrics(conn, run_id, payload, scored, evidence_map)
    insert_output(conn, run_id, scored)
    conn.execute(
        """
        INSERT INTO audit_events (event_type, entity_type, entity_id, details_json)
        VALUES ('imported', 'analysis_run', ?, ?)
        """,
        (run_id, stable_json({"run_uid": run_uid, "payload": str(payload_path), "scored": str(scored_path) if scored_path else None})),
    )
    return run_uid


def find_pairs(source_dir: Path) -> list[tuple[Path, Path | None]]:
    payloads = sorted(source_dir.glob("*_payload.json"))
    return [(payload, payload.with_name(payload.name.replace("_payload.json", "_scored.json"))) for payload in payloads]


def command_init(args: argparse.Namespace) -> int:
    init_db(args.db)
    print(f"Initialized SQLite database: {args.db}")
    return 0


def command_ingest(args: argparse.Namespace) -> int:
    init_db(args.db)
    source_dir = args.source_dir.resolve()
    pairs = find_pairs(source_dir)
    if not pairs:
        print(f"No *_payload.json files found in {source_dir}", file=sys.stderr)
        return 1

    imported: list[str] = []
    with connect(args.db) as conn:
        for payload_path, scored_path in pairs:
            imported.append(import_pair(conn, payload_path, scored_path if scored_path.exists() else None, source_dir))
    print(f"Imported {len(imported)} analysis run(s) into {args.db}:")
    for run_uid in imported:
        print(f"  - {run_uid}")
    return 0


def command_start(args: argparse.Namespace) -> int:
    init_db(args.db)
    print(f"Storage system ready: {args.db}")
    if args.ingest:
        ingest_args = argparse.Namespace(db=args.db, source_dir=args.source_dir)
        return command_ingest(ingest_args)
    print("No daemon is running; this is a local SQLite CLI. Use `status`, `runs`, or `show-run` next.")
    return 0


def command_end(args: argparse.Namespace) -> int:
    print("No background process is running. SQLite connections close automatically when each command exits.")
    print(f"Database remains on disk at: {args.db}")
    return 0


def command_status(args: argparse.Namespace) -> int:
    init_db(args.db)
    with connect(args.db) as conn:
        tables = [
            "companies",
            "company_identifiers",
            "analysis_frameworks",
            "analysis_runs",
            "analysis_layers",
            "analysis_metrics",
            "sources",
            "run_source_refs",
            "evidence_items",
            "metric_evidence_links",
            "analysis_outputs",
            "content_artifacts",
            "raw_documents",
        ]
        for table in tables:
            count = conn.execute(f"SELECT COUNT(*) AS n FROM {table}").fetchone()["n"]
            print(f"{table}: {count}")
    return 0


def command_runs(args: argparse.Namespace) -> int:
    init_db(args.db)
    with connect(args.db) as conn:
        rows = conn.execute(
            """
            SELECT run_uid, company, ticker, research_date, display_total_score,
                   gate_pass, verdict, source_count, evidence_count, metric_count
            FROM v_run_summary
            ORDER BY COALESCE(research_date, ''), company
            """
        ).fetchall()
    if not rows:
        print("No analysis runs found.")
        return 0
    for row in rows:
        gate = "pass" if row["gate_pass"] else "fail"
        print(
            f"{row['run_uid']} | {row['company']} | {row['ticker'] or 'no ticker'} | "
            f"{row['research_date'] or 'no date'} | score={row['display_total_score'] or 'n/a'} | "
            f"gate={gate} | sources={row['source_count']} evidence={row['evidence_count']} metrics={row['metric_count']}"
        )
        if row["verdict"]:
            print(f"  verdict: {row['verdict']}")
    return 0


def resolve_run(conn: sqlite3.Connection, run_ref: str) -> sqlite3.Row:
    if run_ref.isdigit():
        row = conn.execute("SELECT * FROM analysis_runs WHERE id = ?", (int(run_ref),)).fetchone()
    else:
        row = conn.execute("SELECT * FROM analysis_runs WHERE run_uid = ?", (run_ref,)).fetchone()
    if row is None:
        raise SystemExit(f"Run not found: {run_ref}")
    return row


def command_show_run(args: argparse.Namespace) -> int:
    init_db(args.db)
    with connect(args.db) as conn:
        run = resolve_run(conn, args.run)
        summary = conn.execute("SELECT * FROM v_run_summary WHERE analysis_run_id = ?", (run["id"],)).fetchone()
        layers = conn.execute(
            """
            SELECT label, score, display_score, coverage_ratio, confidence
            FROM analysis_layers
            WHERE analysis_run_id = ?
            ORDER BY sort_order
            """,
            (run["id"],),
        ).fetchall()
        output = {
            "summary": dict(summary) if summary else {},
            "layers": [dict(layer) for layer in layers],
            "focus_technologies": json.loads(run["focus_technologies_json"]),
        }
    print(pretty_json(output))
    return 0


def command_export_run(args: argparse.Namespace) -> int:
    init_db(args.db)
    with connect(args.db) as conn:
        run = resolve_run(conn, args.run)
        output = {
            "run_uid": run["run_uid"],
            "payload": json.loads(run["raw_payload_json"]) if run["raw_payload_json"] else None,
            "scored": json.loads(run["raw_scored_json"]) if run["raw_scored_json"] else None,
        }
    if args.out:
        args.out.write_text(pretty_json(output) + "\n", encoding="utf-8")
        print(f"Exported run to {args.out}")
    else:
        print(pretty_json(output))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SQLite storage system for company analysis artifacts.")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB, help=f"SQLite database path. Default: {DEFAULT_DB}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create or migrate the SQLite database.")
    init_parser.set_defaults(func=command_init)

    ingest_parser = subparsers.add_parser("ingest", help="Import *_payload.json and paired *_scored.json files.")
    ingest_parser.add_argument("--source-dir", type=Path, default=ROOT.parent, help="Directory containing JSON files.")
    ingest_parser.set_defaults(func=command_ingest)

    start_parser = subparsers.add_parser("start", help="Initialize the database and optionally ingest source JSON files.")
    start_parser.add_argument("--source-dir", type=Path, default=ROOT.parent, help="Directory containing JSON files.")
    start_parser.add_argument("--ingest", action="store_true", help="Import source JSON files after initialization.")
    start_parser.set_defaults(func=command_start)

    end_parser = subparsers.add_parser("end", help="Explain shutdown/close behavior for the local CLI.")
    end_parser.set_defaults(func=command_end)

    status_parser = subparsers.add_parser("status", help="Print table counts.")
    status_parser.set_defaults(func=command_status)

    runs_parser = subparsers.add_parser("runs", help="List imported analysis runs.")
    runs_parser.set_defaults(func=command_runs)

    show_parser = subparsers.add_parser("show-run", help="Show one run summary as JSON.")
    show_parser.add_argument("run", help="Run UID or numeric database ID.")
    show_parser.set_defaults(func=command_show_run)

    export_parser = subparsers.add_parser("export-run", help="Export raw payload/scored JSON for one run.")
    export_parser.add_argument("run", help="Run UID or numeric database ID.")
    export_parser.add_argument("--out", type=Path, help="Optional output JSON file.")
    export_parser.set_defaults(func=command_export_run)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
