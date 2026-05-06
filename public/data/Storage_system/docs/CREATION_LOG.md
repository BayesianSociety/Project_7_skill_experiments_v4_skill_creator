# Creation Log

## What Was Inspected

The current directory contained ten JSON files:

```text
demant_as_payload.json
demant_as_scored.json
gilead_sciences_inc_payload.json
gilead_sciences_inc_scored.json
postnl_nv_payload.json
postnl_nv_scored.json
snowflake_inc_payload.json
snowflake_inc_scored.json
uber_technologies_inc_payload.json
uber_technologies_inc_scored.json
```

Each company has a payload file and a scored file.

## Schemas Found

Two generations of JSON schema were found.

Legacy files:

```text
postnl_nv_payload.json
postnl_nv_scored.json
gilead_sciences_inc_payload.json
gilead_sciences_inc_scored.json
```

These contain:

```text
company
ticker
mode
benchmark_ready
research_date
focus_technologies
layers
```

Scored files also contain:

```text
total_score
display_total_score
gate_pass
verdict
```

Richer v2 files:

```text
snowflake_inc_payload.json
snowflake_inc_scored.json
uber_technologies_inc_payload.json
uber_technologies_inc_scored.json
demant_as_payload.json
demant_as_scored.json
```

These contain:

```text
schema_version
company
ticker
mode
benchmark_ready
skill_metadata
research_run
research_context
sources
evidence_items
layers
normalization_notes
storage_metadata
scorer_metadata
```

## Design Decision

The database was designed around immutable analysis runs rather than company files.

This allows:

- multiple analyses per company
- repeated analyses over time
- multiple frameworks
- multiple scorer versions
- different future content artifacts
- different source and evidence structures

## Files Created

```text
schema.sql
```

Defines the SQLite schema, indexes, and views.

```text
storage_system.py
```

Provides the CLI for initializing, importing, listing, inspecting, and exporting analysis runs.

```text
storage.db
```

Generated SQLite database containing the imported current JSON files.

```text
example_queries.sql
```

Practical SQL examples for inspecting the database.

```text
README.md
docs/DESIGN.md
docs/REPLICATION_PROMPT.md
```

Documentation and future replication instructions.

## Commands Used To Build

From the parent `public/data` directory:

```bash
python3 Storage_system/storage_system.py start --ingest --source-dir .
python3 Storage_system/storage_system.py status
python3 Storage_system/storage_system.py runs
python3 Storage_system/storage_system.py show-run snowflake-innovation-2026-05-04
```

## Result

The generated database contains:

```text
companies: 5
company_identifiers: 7
analysis_frameworks: 2
analysis_runs: 5
analysis_layers: 25
analysis_metrics: 75
sources: 47
run_source_refs: 47
evidence_items: 51
metric_evidence_links: 101
analysis_outputs: 5
content_artifacts: 0
raw_documents: 0
```

The system is dependency-free and uses only:

- Python 3 standard library
- SQLite

