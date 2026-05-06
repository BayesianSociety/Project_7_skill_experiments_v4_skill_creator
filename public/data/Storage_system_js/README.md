# Storage System JS

This is a JavaScript/Node.js version of the local company-analysis storage system.

It uses SQLite for durable local storage, preserves raw JSON artifacts, normalizes stable analysis concepts, records schema observations during ingestion, exposes a small HTTP API, and includes a simple Next.js frontend connected to the same database.

## What This Directory Contains

```text
Storage_system_js/
  package.json
  package-lock.json
  schema.sql
  storage_js.db
  example_queries.sql
  src/
    cli.js
    db.js
    ingest.js
    queries.js
    server.js
    utils.js
  app/
    page.js
    layout.js
    globals.css
    api/
  lib/
    dashboard-data.js
  docs/
    DESIGN.md
    API.md
    CREATION_LOG.md
    REPLICATION_PROMPT.md
```

## Why A JavaScript Version

The earlier SQLite system was implemented in Python. This version keeps the same database philosophy but moves the operational layer into JavaScript so it can integrate smoothly with a future frontend.

The intended future shape is:

```text
JSON analysis artifacts
        |
        v
Node.js ingestion + SQLite
        |
        v
Express API
        |
        v
React / Next.js frontend
```

The current frontend uses Next.js. Vite is not used.

## Dependencies

This project uses:

- `better-sqlite3` for local SQLite access.
- `express` for the frontend-ready HTTP API.
- `next`, `react`, and `react-dom` for the business frontend.
- `lucide-react` for interface icons.

Install dependencies from inside `Storage_system_js`:

```bash
npm install
```

## Quick Start

From `Storage_system_js`:

```bash
npm run start:ingest
```

This creates or updates:

```text
Storage_system_js/storage_js.db
```

and imports all `*_payload.json` files from the parent directory with their matching `*_scored.json` files.

Check the imported data:

```bash
npm run status
npm run runs
```

Start the Next.js frontend:

```bash
npm run web:dev -- --port 3001
```

Open:

```text
http://127.0.0.1:3001
```

Inspect one run:

```bash
node src/cli.js show-run snowflake-innovation-2026-05-04
```

## Start And End

There are three operating modes.

### CLI Mode

CLI mode is one command at a time. It does not leave a background process running.

Start or initialize:

```bash
npm run start
```

Start and ingest:

```bash
npm run start:ingest
```

End:

```bash
npm run end
```

The `end` command explains that CLI mode has no daemon. SQLite connections close automatically when commands exit.

### API Server Mode

Start the local API server:

```bash
npm run api
```

The default URL is:

```text
http://127.0.0.1:4177
```

Stop it with `Ctrl+C` in the terminal where it is running.

Use a different port:

```bash
node src/server.js --port 4180
```

Use a different database:

```bash
node src/server.js --db ./storage_js.db --port 4180
```

### Next.js Frontend Mode

Start the business console:

```bash
npm run web:dev -- --port 3001
```

The frontend reads directly from `storage_js.db` on the server side through:

```text
lib/dashboard-data.js
```

It also exposes Next.js app routes:

```text
GET /api/status
GET /api/runs
GET /api/runs/:runUid
GET /api/schema-observations
```

Stop the frontend with `Ctrl+C` in the terminal where it is running.

## Main CLI Commands

```bash
node src/cli.js init
```

Creates or migrates the SQLite database.

```bash
node src/cli.js ingest --source-dir ..
```

Imports all `*_payload.json` and paired `*_scored.json` files.

```bash
node src/cli.js status
```

Prints table counts.

```bash
node src/cli.js runs
```

Lists imported analysis runs.

```bash
node src/cli.js show-run RUN_UID
```

Prints a structured JSON summary for one run.

```bash
node src/cli.js export-run RUN_UID --out output.json
```

Exports preserved raw payload/scored JSON for one run.

## Frontend-Ready API

Start:

```bash
npm run api
```

Useful endpoints:

```text
GET  /api/health
GET  /api/status
GET  /api/runs
GET  /api/runs/:runUid
GET  /api/runs/:runUid/evidence
GET  /api/companies
GET  /api/metric-evidence
GET  /api/schema-observations
POST /api/content-artifacts
```

See [docs/API.md](docs/API.md) for details.

## Future Schema Changes

This system is designed to be resilient when future analysis JSON changes.

It does three things:

1. Preserves the full raw payload/scored JSON in `analysis_runs`.
2. Normalizes known stable fields into queryable tables.
3. Records observed, missing, and unmapped top-level fields in `json_ingestion_events`.

That means a new field in a future JSON file will not be lost. If the importer does not yet know how to normalize it, the raw JSON still stores it and the schema-observation table flags it.

The relevant tables are:

```text
schema_registry
json_ingestion_events
```

Use:

```bash
sqlite3 storage_js.db "SELECT * FROM v_schema_observations;"
```

or:

```bash
curl http://127.0.0.1:4177/api/schema-observations
```

## Current Imported Dataset

After running `npm run start:ingest`, the database contains:

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
json_ingestion_events: 10
schema_registry: 4
```

## Running SQL Examples

```bash
sqlite3 storage_js.db < example_queries.sql
```

## Rebuild From Scratch

From `Storage_system_js`:

```bash
rm storage_js.db
npm run start:ingest
```

Only remove `storage_js.db` if you intentionally want to rebuild from source JSON files.
