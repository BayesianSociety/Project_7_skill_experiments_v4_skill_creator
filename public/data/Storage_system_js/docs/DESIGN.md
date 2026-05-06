# Design

## Goal

The JavaScript storage system provides a local, SQLite-backed persistence layer for company-analysis artifacts and future generated content.

It is designed for:

- changing JSON schemas
- many companies
- many analysis dates
- many scoring frameworks
- future generated website content
- future frontend API integration

## Architecture

```text
source JSON files
    |
    v
src/ingest.js
    |
    v
SQLite database
    |
    +--> src/cli.js
    |
    +--> src/server.js
    |
    +--> Next.js app routes + server-rendered frontend
             |
             v
       browser UI
```

The system has three interfaces:

- A CLI for ingestion, status checks, exports, and operational use.
- An Express API for frontend integration.
- A Next.js business console for browsing runs, evidence, and schema health.

## Core Design Principle

The central table is `analysis_runs`.

A company is a durable entity. An analysis run is a dated, versioned observation about that company. A company can have many future runs using different research dates, different scorer versions, different source sets, or different analysis frameworks.

This avoids overwriting historical research.

## Storage Model

The schema uses a hybrid relational plus JSON model.

Relational tables store stable concepts:

- companies
- company identifiers
- frameworks
- runs
- layers
- metrics
- sources
- evidence
- final outputs
- content artifacts

JSON columns store flexible details:

- full raw payload JSON
- full raw scored JSON
- research context
- normalization metadata
- storage metadata
- raw source JSON
- raw evidence JSON
- raw metric JSON
- generated content JSON

SQLite stores JSON as `TEXT`, with `CHECK(json_valid(...))` constraints where possible.

## Schema-Change Strategy

Future JSON schemas may add, remove, or rename fields.

The system handles that with three layers.

### 1. Preserve Raw Documents

Every analysis run stores:

```text
raw_payload_json
raw_scored_json
payload_hash
scored_hash
import_hash
```

Even if the importer does not know a future field, the original JSON remains available.

### 2. Normalize Known Fields

The importer extracts known stable structures:

```text
company
ticker
research_run
research_context
sources
evidence_items
layers
metrics
scores
scorer metadata
```

If a future schema keeps those concepts under the same names, no code change is required.

### 3. Observe Unknown Fields

The JavaScript version adds:

```text
schema_registry
json_ingestion_events
v_schema_observations
```

`schema_registry` stores expected top-level keys for known payload and scored schema versions.

`json_ingestion_events` records:

- observed top-level keys
- expected top-level keys
- unmapped top-level keys
- missing expected keys
- importer version
- raw document hash

This means a future schema change is visible immediately after import.

## Main Tables

### `companies`

Stores stable company identity.

Tickers do not live directly as the primary identity because companies can change tickers, trade on multiple exchanges, delist, or be private.

### `company_identifiers`

Stores tickers, CIKs, and future identifiers.

Examples:

```text
ticker: NYSE / SNOW
cik: 1640147
```

Future additions can include ISIN, LEI, FIGI, PermID, internal IDs, or subsidiary IDs.

### `analysis_frameworks`

Stores the method used for scoring.

Important fields:

```text
name
version
schema_version
scorer_name
scorer_version
metric_rules_version
definition_json
```

This allows old and new scoring systems to coexist.

### `analysis_runs`

Stores one imported analysis event.

This is the main table. It links to the company and framework and preserves full raw JSON.

### `sources`

Stores deduplicated source documents.

Current JSON files have local source IDs such as `src_001`. Those IDs are meaningful only inside one analysis run, so the global `sources` table deduplicates by URL when possible and otherwise by source metadata.

### `run_source_refs`

Maps local source IDs from one run to global source rows.

### `evidence_items`

Stores auditable facts used to support metrics.

Evidence includes:

- fact text
- source reference
- raw value
- unit
- period
- verification status
- limitations
- raw evidence JSON

### `analysis_layers`

Stores layer-level summaries and scores.

The current innovation framework has five layers, but the schema does not hardcode them. Future frameworks can use different layers.

### `analysis_metrics`

Stores metric-level values, weights, units, source type, and normalization metadata.

### `metric_evidence_links`

Links metrics and evidence as a many-to-many relationship.

This is important because one evidence item can support multiple metrics, and one metric can rely on multiple evidence items.

### `analysis_outputs`

Stores final score, gate result, and verdict.

### `content_artifacts`

Stores future generated frontend or reporting artifacts.

Examples:

- dashboard state
- rendered HTML
- reports
- slide deck metadata
- Instagram carousel JSON
- PDF paths
- frontend theme selections

The API already includes `POST /api/content-artifacts` so a future website can save generated artifacts.

### `raw_documents`

Reserved for future document ingestion.

Examples:

- annual reports
- filings
- transcripts
- scraped web pages
- patents
- PDFs

## Next.js Frontend

The frontend lives in:

```text
app/
lib/dashboard-data.js
```

It uses the Next.js app router and reads from `storage_js.db` on the server side. The browser receives a ready-to-render business workspace with:

- database status counts
- analysis run selector
- selected company score detail
- layer score bars
- highest metrics
- evidence search
- schema observation health

The design follows a restrained operational UI pattern: table-first scanning, minimal chrome, clear spacing, and a single green accent.

## Frontend Integration

The Express API in `src/server.js` remains intentionally simple and JSON-first.

A future frontend can call:

```text
GET /api/runs
GET /api/runs/:runUid
GET /api/runs/:runUid/evidence
GET /api/companies
GET /api/metric-evidence
GET /api/schema-observations
POST /api/content-artifacts
```

This can be used from:

- React
- Next.js
- Vite
- Svelte
- any dashboard framework

For production or multi-user use, the same model can later migrate to Postgres. The current SQLite schema is intentionally relational enough to make that path realistic.

## Limitations

This system is future-proof for preserving changing schemas and detecting new fields.

It is not magical automatic normalization for arbitrary renamed structures. If a future schema renames:

```text
layers -> dimensions
evidence_items -> claims
sources -> references
```

then the raw JSON will still be preserved and the schema observation table will flag changes, but the importer will need a new adapter to normalize those renamed concepts.

The recommended future extension is an adapter registry keyed by schema version.
