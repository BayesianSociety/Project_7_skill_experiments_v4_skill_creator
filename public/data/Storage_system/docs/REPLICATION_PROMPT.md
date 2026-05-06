# Replication Prompt

Use this prompt to recreate this storage system in a future project.

```text
Create a self-contained local database storage system in a directory named Storage_system.

The system must use SQLite for local storage and Python standard library only. It must ingest company-analysis JSON artifacts from a source directory. Each company analysis may have a *_payload.json file and a matching *_scored.json file.

Design the storage system to be future-proof for many companies, many analysis dates, many scoring frameworks, many source types, and many generated content artifacts.

Use a hybrid relational plus JSON-column model:

- Preserve the full raw payload JSON and raw scored JSON.
- Normalize companies, company identifiers, frameworks, analysis runs, layers, metrics, sources, evidence items, metric-evidence links, outputs, content artifacts, raw documents, and audit events.
- Use SQLite TEXT columns with CHECK(json_valid(...)) constraints for JSON fields.
- Include useful indexes and views for run summaries and metric-to-evidence inspection.

The central table must be analysis_runs, not companies and not files. Companies are durable entities; analysis runs are versioned observations about companies.

Create these artifacts:

- Storage_system/schema.sql
- Storage_system/storage_system.py
- Storage_system/README.md
- Storage_system/docs/DESIGN.md
- Storage_system/docs/CREATION_LOG.md
- Storage_system/docs/REPLICATION_PROMPT.md
- Storage_system/example_queries.sql

The CLI should support:

- init: create or migrate the SQLite database
- ingest --source-dir PATH: import all *_payload.json files and paired *_scored.json files
- start: initialize the database
- start --ingest --source-dir PATH: initialize and ingest
- end: explain that no daemon is running and connections close after each command
- status: print table counts
- runs: list imported analysis runs
- show-run RUN_UID: show one run summary as JSON
- export-run RUN_UID --out FILE: export preserved raw payload/scored JSON

The importer should:

- Pair *_payload.json with *_scored.json.
- Use research_run.run_id as run_uid when available.
- Fall back to the payload filename stem for legacy files.
- Be idempotent by run_uid.
- Store raw JSON and hashes.
- Extract company names, tickers, CIKs when available.
- Store rich v2 sources and evidence when available.
- Store legacy files gracefully even when sources and evidence are absent.
- Link metrics to evidence by metric.evidence_ids and by evidence.metric_codes.

After implementation, run:

python3 Storage_system/storage_system.py start --ingest --source-dir .
python3 Storage_system/storage_system.py status
python3 Storage_system/storage_system.py runs

Then document exactly how the system works, how it was created, how to use it, and how to start/end it.
```

