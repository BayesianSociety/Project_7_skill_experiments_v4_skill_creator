# API

This project has two API surfaces:

- `src/server.js`, the standalone Express API.
- Next.js app routes under `app/api`, used by the frontend and available to browser clients.

## Next.js App Routes

Start the frontend:

```bash
npm run web:dev -- --port 3001
```

Base URL:

```text
http://127.0.0.1:3001
```

Available routes:

```text
GET /api/status
GET /api/runs
GET /api/runs/:runUid
GET /api/schema-observations
```

These routes read from the same SQLite database as the frontend.

## Express API

Start the API server from `Storage_system_js`:

```bash
npm run api
```

Default base URL:

```text
http://127.0.0.1:4177
```

## Health

```text
GET /api/health
```

Returns:

```json
{
  "ok": true,
  "db_path": "/absolute/path/to/storage_js.db"
}
```

## Status

```text
GET /api/status
```

Returns row counts for core tables.

## Runs

```text
GET /api/runs
```

Returns analysis run summaries.

```text
GET /api/runs/:runUid
```

Returns one run with:

- summary
- focus technologies
- research context
- layers
- metrics

Example:

```bash
curl http://127.0.0.1:4177/api/runs/snowflake-innovation-2026-05-04
```

## Evidence

```text
GET /api/runs/:runUid/evidence
```

Returns evidence items for one run.

## Metric Evidence

```text
GET /api/metric-evidence
```

Returns metric-to-evidence joins across all runs.

Filter by run:

```text
GET /api/metric-evidence?run_uid=snowflake-innovation-2026-05-04
```

## Companies

```text
GET /api/companies
```

Returns companies with run counts and latest research dates.

## Schema Observations

```text
GET /api/schema-observations
```

Returns records created during ingestion showing observed, missing, and unmapped top-level JSON keys.

This endpoint is useful for detecting future schema changes before they silently affect dashboards.

## Content Artifacts

```text
POST /api/content-artifacts
```

Creates a generated-content artifact for future frontend use.

Example:

```bash
curl -X POST http://127.0.0.1:4177/api/content-artifacts \
  -H 'Content-Type: application/json' \
  -d '{
    "run_uid": "snowflake-innovation-2026-05-04",
    "artifact_type": "dashboard",
    "title": "Snowflake Innovation Dashboard",
    "status": "draft",
    "theme": "default",
    "content": {
      "layout": "summary"
    }
  }'
```

## CORS

The API currently sends permissive local-development CORS headers:

```text
Access-Control-Allow-Origin: *
```

For production, restrict this to the actual frontend origin.
