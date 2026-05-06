# Replication Prompt

Use this prompt to recreate the JavaScript storage system in another project.

```text
Create a self-contained JavaScript/Node.js local storage system in a directory named Storage_system_js.

The system must use SQLite for local storage and be ready for future frontend website integration.

Use Node.js with:

- better-sqlite3 for SQLite access
- express for a local JSON API
- Next.js, React, and React DOM for the frontend
- lucide-react for interface icons

The source data consists of company-analysis JSON artifacts. Each analysis may have a *_payload.json file and a matching *_scored.json file.

Design for changing schemas. The system must:

- preserve full raw payload JSON and raw scored JSON
- normalize known stable concepts into relational tables
- use JSON columns for flexible metadata
- record schema observations during ingestion
- detect unmapped top-level keys
- detect missing expected top-level keys
- version importer, schema, framework, scorer, and metric rules

The central table must be analysis_runs, not companies and not files. Companies are durable entities; analysis runs are dated, versioned observations about companies.

Create:

- Storage_system_js/package.json
- Storage_system_js/schema.sql
- Storage_system_js/src/cli.js
- Storage_system_js/src/db.js
- Storage_system_js/src/ingest.js
- Storage_system_js/src/queries.js
- Storage_system_js/src/server.js
- Storage_system_js/src/utils.js
- Storage_system_js/app/layout.js
- Storage_system_js/app/page.js
- Storage_system_js/app/globals.css
- Storage_system_js/app/api/status/route.js
- Storage_system_js/app/api/runs/route.js
- Storage_system_js/app/api/runs/[runUid]/route.js
- Storage_system_js/app/api/schema-observations/route.js
- Storage_system_js/lib/dashboard-data.js
- Storage_system_js/README.md
- Storage_system_js/docs/DESIGN.md
- Storage_system_js/docs/API.md
- Storage_system_js/docs/CREATION_LOG.md
- Storage_system_js/docs/REPLICATION_PROMPT.md
- Storage_system_js/example_queries.sql

The schema should include:

- companies
- company_identifiers
- analysis_frameworks
- analysis_runs
- sources
- run_source_refs
- evidence_items
- analysis_layers
- analysis_metrics
- metric_evidence_links
- analysis_outputs
- content_artifacts
- raw_documents
- audit_events
- schema_registry
- json_ingestion_events

The CLI should support:

- init
- ingest --source-dir PATH
- start
- start --ingest --source-dir PATH
- end
- status
- runs
- show-run RUN_UID
- export-run RUN_UID --out FILE

The API should support:

- GET /api/health
- GET /api/status
- GET /api/runs
- GET /api/runs/:runUid
- GET /api/runs/:runUid/evidence
- GET /api/companies
- GET /api/metric-evidence
- GET /api/schema-observations
- POST /api/content-artifacts

The Next.js frontend should:

- use the app router
- use plain CSS or a minimal styling setup
- avoid Vite
- read SQLite server-side through a small data-access module
- show status counts, run list, selected run details, layer scores, evidence search, and schema observations
- use restrained business UI with clear typography, table-first scanning, and no decorative dashboard-card clutter

The importer should:

- pair *_payload.json with *_scored.json
- use research_run.run_id as run_uid when available
- fall back to filename stem for legacy files
- be idempotent by run_uid
- store raw JSON and content hashes
- extract company names, tickers, and CIKs when available
- store rich v2 sources and evidence when available
- gracefully store legacy files with no sources or evidence
- link metrics to evidence by metric.evidence_ids and by evidence.metric_codes
- create json_ingestion_events for every imported payload and scored document

After implementation, run:

npm install
npm run start:ingest
npm run status
npm run runs
sqlite3 storage_js.db "PRAGMA integrity_check;"
npm run build
npm run web:dev -- --port 3001
npm run api

Document how the system works, how it was created, how to use it, how to start/end it, and how a future frontend should integrate with it.
```
