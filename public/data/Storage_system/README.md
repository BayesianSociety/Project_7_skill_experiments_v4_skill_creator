# Storage System

This directory contains a self-contained local SQLite storage system for company-analysis artifacts.

It was created to migrate the current JSON files in `public/data` from loose file pairs into a durable, queryable, future-proof local database. The system preserves every original payload and scored JSON document while also normalizing the useful parts into relational tables.

## Contents

```text
Storage_system/
  README.md
  schema.sql
  storage_system.py
  storage.db
  example_queries.sql
  docs/
    DESIGN.md
    CREATION_LOG.md
    REPLICATION_PROMPT.md
```

## What This Stores

The current source files follow two generations of schema:

- Legacy JSON files with company, ticker, focus technologies, layers, and scores.
- Richer v2 JSON files with research runs, framework metadata, sources, evidence items, normalization notes, layers, metrics, and scorer metadata.

This storage system handles both.

The database stores:

- Companies and identifiers.
- Analysis frameworks and scorer versions.
- Immutable analysis runs.
- Raw payload JSON and raw scored JSON.
- Layers and metrics.
- Sources and evidence.
- Links between metrics and evidence.
- Final scoring outputs.
- Future content artifacts such as dashboards, reports, decks, carousel assets, generated HTML, or PDFs.
- Future raw documents such as filings, annual reports, transcripts, patent exports, PDFs, or scraped pages.

## Quick Start

From the parent `public/data` directory:

```bash
python3 Storage_system/storage_system.py start --ingest --source-dir .
```

This initializes `Storage_system/storage.db` and imports every `*_payload.json` file with its paired `*_scored.json` file.

To check the database:

```bash
python3 Storage_system/storage_system.py status
python3 Storage_system/storage_system.py runs
```

To inspect one run:

```bash
python3 Storage_system/storage_system.py show-run snowflake-innovation-2026-05-04
```

To export the preserved raw JSON for one run:

```bash
python3 Storage_system/storage_system.py export-run snowflake-innovation-2026-05-04 --out /tmp/snowflake_run_export.json
```

## Starting And Ending The Program

This is a local SQLite command-line program. There is no server and no background daemon.

Start or initialize it with:

```bash
python3 Storage_system/storage_system.py start
```

Start and ingest source JSON files with:

```bash
python3 Storage_system/storage_system.py start --ingest --source-dir .
```

End it with:

```bash
python3 Storage_system/storage_system.py end
```

The `end` command does not kill a process because no process remains running. Each command opens a SQLite connection, performs its work, commits, closes the connection, and exits. The database remains on disk at:

```text
Storage_system/storage.db
```

## Main Commands

```bash
python3 Storage_system/storage_system.py init
```

Creates or migrates the SQLite database from `schema.sql`.

```bash
python3 Storage_system/storage_system.py ingest --source-dir .
```

Imports all `*_payload.json` files from the given directory and pairs each with the matching `*_scored.json`.

```bash
python3 Storage_system/storage_system.py status
```

Prints row counts for the main tables.

```bash
python3 Storage_system/storage_system.py runs
```

Lists imported analysis runs with company, ticker, date, score, gate result, and evidence counts.

```bash
python3 Storage_system/storage_system.py show-run RUN_UID
```

Prints a JSON summary for one analysis run.

```bash
python3 Storage_system/storage_system.py export-run RUN_UID --out output.json
```

Exports the preserved raw payload and scored JSON for one analysis run.

## Current Imported Dataset

The generated `storage.db` currently contains:

```text
companies: 5
analysis_runs: 5
analysis_layers: 25
analysis_metrics: 75
sources: 47
evidence_items: 51
analysis_outputs: 5
```

The imported analysis runs are:

```text
demant-as-2026-04-30
gilead_sciences_inc
postnl_nv
snowflake-innovation-2026-05-04
uber-innovation-2026-05-04
```

## Design Summary

The central object is `analysis_runs`, not companies and not files.

Companies are durable entities. Analysis runs are time-stamped, versioned observations about companies. This allows the system to store many future analyses for the same company without overwriting history.

Every run stores:

- A normalized relational representation for querying.
- The original raw JSON for compatibility and auditability.
- Content hashes for repeatable imports and change detection.

This hybrid model avoids two bad extremes:

- Pure JSON storage, which is flexible but hard to query.
- Pure relational storage, which is queryable but brittle when schemas evolve.

See [docs/DESIGN.md](docs/DESIGN.md) for the full design documentation.

## Running SQL Queries

Use the SQLite shell:

```bash
sqlite3 Storage_system/storage.db
```

Then run:

```sql
.tables
SELECT * FROM v_run_summary;
```

Or execute the included query examples:

```bash
sqlite3 Storage_system/storage.db < Storage_system/example_queries.sql
```

## Rebuilding From Scratch

To rebuild the local database:

```bash
rm Storage_system/storage.db
python3 Storage_system/storage_system.py start --ingest --source-dir .
```

Only remove `storage.db` if you intentionally want to rebuild the database from the JSON source files. The importer is idempotent by `run_uid`: importing the same run again replaces that run's normalized records and preserved raw JSON.

## Future Use

For future companies or content types:

1. Create a new `*_payload.json` file.
2. Optionally create a matching `*_scored.json` file.
3. Include rich v2 fields where possible: `schema_version`, `skill_metadata`, `research_run`, `research_context`, `sources`, `evidence_items`, `layers`, `normalization_notes`, and `storage_metadata`.
4. Run:

```bash
python3 Storage_system/storage_system.py ingest --source-dir .
```

The database can also store non-score artifacts in `content_artifacts`, such as generated dashboards, reports, carousel slides, deck metadata, rendered HTML, or PDF paths.

