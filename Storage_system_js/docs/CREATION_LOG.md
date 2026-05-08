# Creation Log

## Source Files

The JavaScript system was built from the current JSON files in the parent data directory:

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

## Existing Shapes

Two JSON generations were found.

Legacy files contain:

```text
company
ticker
mode
benchmark_ready
research_date
focus_technologies
layers
```

Scored legacy files also contain:

```text
total_score
display_total_score
gate_pass
verdict
```

Richer v2 files contain:

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

## What Was Created

The JavaScript implementation created:

```text
schema.sql
```

SQLite schema with relational tables, JSON columns, indexes, views, schema registry, and ingestion observation tables.

```text
src/cli.js
```

Command-line entry point.

```text
src/db.js
```

Database initialization and schema-registry seeding.

```text
src/ingest.js
```

Payload/scored JSON importer.

```text
src/queries.js
```

Shared query helpers for both CLI and API.

```text
src/server.js
```

Express API for future frontend integration.

```text
app/
```

Next.js business console connected to `storage_js.db`.

```text
lib/dashboard-data.js
```

Server-side SQLite data access for the Next.js frontend.

```text
src/utils.js
```

Shared helpers for stable JSON, hashing, slugs, tickers, and paths.

```text
storage_js.db
```

Generated SQLite database.

## Commands Used

From `Storage_system_js`:

```bash
npm install
npm run start:ingest
npm run status
npm run runs
sqlite3 storage_js.db "PRAGMA integrity_check;"
npm run build
npm run web:dev -- --port 3001
```

API validation used:

```bash
npm run api
curl -sS http://127.0.0.1:4177/api/health
curl -sS http://127.0.0.1:4177/api/runs
```

Next.js validation used:

```bash
curl -sS http://127.0.0.1:3001/api/status
curl -sS http://127.0.0.1:3001/api/runs
curl -sS http://127.0.0.1:3001/
```

## Import Result

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
json_ingestion_events: 10
schema_registry: 4
```

## Integrity

SQLite integrity check returned:

```text
ok
```

The JS import counts match the earlier Python system and add schema-observation records for future schema-change monitoring.
