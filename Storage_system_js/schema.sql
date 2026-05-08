PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;

CREATE TABLE IF NOT EXISTS schema_migrations (
    version INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    applied_at TEXT NOT NULL DEFAULT (datetime('now'))
);

INSERT OR IGNORE INTO schema_migrations (version, name)
VALUES (1, 'initial_storage_system_schema');

CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY,
    legal_name TEXT NOT NULL,
    display_name TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    country TEXT,
    sector TEXT,
    industry TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}'
        CHECK (json_valid(metadata_json)),
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS company_identifiers (
    id INTEGER PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    identifier_type TEXT NOT NULL,
    identifier_value TEXT NOT NULL,
    exchange TEXT NOT NULL DEFAULT '',
    valid_from TEXT,
    valid_to TEXT,
    is_primary INTEGER NOT NULL DEFAULT 0 CHECK (is_primary IN (0, 1)),
    metadata_json TEXT NOT NULL DEFAULT '{}'
        CHECK (json_valid(metadata_json)),
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE (company_id, identifier_type, identifier_value, exchange),
    CHECK (identifier_type <> ''),
    CHECK (identifier_value <> '')
);

CREATE TABLE IF NOT EXISTS analysis_frameworks (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    version TEXT NOT NULL,
    schema_version TEXT NOT NULL DEFAULT '',
    scorer_name TEXT NOT NULL DEFAULT '',
    scorer_version TEXT NOT NULL DEFAULT '',
    metric_rules_version TEXT NOT NULL DEFAULT '',
    definition_json TEXT NOT NULL DEFAULT '{}'
        CHECK (json_valid(definition_json)),
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE (
        name,
        version,
        schema_version,
        scorer_name,
        scorer_version,
        metric_rules_version
    )
);

CREATE TABLE IF NOT EXISTS analysis_runs (
    id INTEGER PRIMARY KEY,
    run_uid TEXT NOT NULL UNIQUE,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    framework_id INTEGER REFERENCES analysis_frameworks(id) ON DELETE SET NULL,
    mode TEXT,
    research_date TEXT,
    analyst TEXT,
    user_request TEXT,
    time_horizon TEXT,
    research_mode TEXT,
    benchmark_ready INTEGER CHECK (benchmark_ready IN (0, 1)),
    source_payload_file TEXT,
    source_scored_file TEXT,
    source_directory TEXT,
    focus_technologies_json TEXT NOT NULL DEFAULT '[]'
        CHECK (json_valid(focus_technologies_json)),
    research_context_json TEXT NOT NULL DEFAULT '{}'
        CHECK (json_valid(research_context_json)),
    normalization_notes_json TEXT NOT NULL DEFAULT '[]'
        CHECK (json_valid(normalization_notes_json)),
    storage_metadata_json TEXT NOT NULL DEFAULT '{}'
        CHECK (json_valid(storage_metadata_json)),
    raw_payload_json TEXT
        CHECK (raw_payload_json IS NULL OR json_valid(raw_payload_json)),
    raw_scored_json TEXT
        CHECK (raw_scored_json IS NULL OR json_valid(raw_scored_json)),
    payload_hash TEXT,
    scored_hash TEXT,
    import_hash TEXT NOT NULL,
    imported_at TEXT NOT NULL DEFAULT (datetime('now')),
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY,
    canonical_url TEXT,
    url_hash TEXT NOT NULL UNIQUE,
    title TEXT,
    publisher TEXT,
    source_type TEXT,
    document_date TEXT,
    reliability TEXT,
    availability TEXT,
    notes TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}'
        CHECK (json_valid(metadata_json)),
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS run_source_refs (
    id INTEGER PRIMARY KEY,
    analysis_run_id INTEGER NOT NULL REFERENCES analysis_runs(id) ON DELETE CASCADE,
    source_id INTEGER NOT NULL REFERENCES sources(id) ON DELETE RESTRICT,
    local_source_id TEXT NOT NULL,
    accessed_at TEXT,
    raw_source_json TEXT NOT NULL
        CHECK (json_valid(raw_source_json)),
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE (analysis_run_id, local_source_id)
);

CREATE TABLE IF NOT EXISTS evidence_items (
    id INTEGER PRIMARY KEY,
    analysis_run_id INTEGER NOT NULL REFERENCES analysis_runs(id) ON DELETE CASCADE,
    source_id INTEGER REFERENCES sources(id) ON DELETE SET NULL,
    local_evidence_id TEXT NOT NULL,
    layer_code TEXT,
    layer_label TEXT,
    fact_type TEXT,
    fact TEXT,
    quote_or_excerpt TEXT,
    raw_value REAL,
    raw_unit TEXT,
    period_start TEXT,
    period_end TEXT,
    company_attributable INTEGER CHECK (company_attributable IN (0, 1)),
    field_proxy INTEGER CHECK (field_proxy IN (0, 1)),
    location TEXT,
    verified INTEGER CHECK (verified IN (0, 1)),
    limitations TEXT,
    metric_codes_json TEXT NOT NULL DEFAULT '[]'
        CHECK (json_valid(metric_codes_json)),
    raw_evidence_json TEXT NOT NULL
        CHECK (json_valid(raw_evidence_json)),
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE (analysis_run_id, local_evidence_id)
);

CREATE TABLE IF NOT EXISTS analysis_layers (
    id INTEGER PRIMARY KEY,
    analysis_run_id INTEGER NOT NULL REFERENCES analysis_runs(id) ON DELETE CASCADE,
    layer_code TEXT NOT NULL,
    label TEXT NOT NULL,
    sort_order INTEGER NOT NULL,
    summary TEXT,
    strong TEXT,
    missing TEXT,
    coverage_ratio REAL,
    score REAL,
    raw_score REAL,
    normalized_score REAL,
    confidence TEXT,
    confidence_penalty REAL,
    display_score TEXT,
    caps_json TEXT NOT NULL DEFAULT '[]'
        CHECK (json_valid(caps_json)),
    cap_reasons_json TEXT NOT NULL DEFAULT '[]'
        CHECK (json_valid(cap_reasons_json)),
    raw_layer_json TEXT NOT NULL
        CHECK (json_valid(raw_layer_json)),
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE (analysis_run_id, layer_code)
);

CREATE TABLE IF NOT EXISTS analysis_metrics (
    id INTEGER PRIMARY KEY,
    analysis_run_id INTEGER NOT NULL REFERENCES analysis_runs(id) ON DELETE CASCADE,
    layer_id INTEGER NOT NULL REFERENCES analysis_layers(id) ON DELETE CASCADE,
    metric_code TEXT NOT NULL,
    label TEXT,
    value REAL,
    weight REAL,
    unit TEXT,
    source_type TEXT,
    verified INTEGER CHECK (verified IN (0, 1)),
    normalization_method TEXT,
    normalization_json TEXT NOT NULL DEFAULT '{}'
        CHECK (json_valid(normalization_json)),
    raw_metric_json TEXT NOT NULL
        CHECK (json_valid(raw_metric_json)),
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE (analysis_run_id, layer_id, metric_code)
);

CREATE TABLE IF NOT EXISTS metric_evidence_links (
    metric_id INTEGER NOT NULL REFERENCES analysis_metrics(id) ON DELETE CASCADE,
    evidence_item_id INTEGER NOT NULL REFERENCES evidence_items(id) ON DELETE CASCADE,
    relationship_type TEXT NOT NULL DEFAULT 'supports',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (metric_id, evidence_item_id, relationship_type)
);

CREATE TABLE IF NOT EXISTS analysis_outputs (
    id INTEGER PRIMARY KEY,
    analysis_run_id INTEGER NOT NULL UNIQUE REFERENCES analysis_runs(id) ON DELETE CASCADE,
    total_score REAL,
    display_total_score TEXT,
    gate_pass INTEGER CHECK (gate_pass IN (0, 1)),
    verdict TEXT,
    scorer_metadata_json TEXT NOT NULL DEFAULT '{}'
        CHECK (json_valid(scorer_metadata_json)),
    formula TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS content_artifacts (
    id INTEGER PRIMARY KEY,
    analysis_run_id INTEGER REFERENCES analysis_runs(id) ON DELETE SET NULL,
    company_id INTEGER REFERENCES companies(id) ON DELETE SET NULL,
    artifact_type TEXT NOT NULL,
    title TEXT,
    status TEXT NOT NULL DEFAULT 'draft',
    content_json TEXT NOT NULL DEFAULT '{}'
        CHECK (json_valid(content_json)),
    file_path TEXT,
    rendered_html TEXT,
    theme TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}'
        CHECK (json_valid(metadata_json)),
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS raw_documents (
    id INTEGER PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id) ON DELETE SET NULL,
    source_id INTEGER REFERENCES sources(id) ON DELETE SET NULL,
    document_type TEXT,
    title TEXT,
    url TEXT,
    file_path TEXT,
    content_hash TEXT UNIQUE,
    extracted_text TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}'
        CHECK (json_valid(metadata_json)),
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS audit_events (
    id INTEGER PRIMARY KEY,
    event_type TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id INTEGER,
    details_json TEXT NOT NULL DEFAULT '{}'
        CHECK (json_valid(details_json)),
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS schema_registry (
    id INTEGER PRIMARY KEY,
    schema_name TEXT NOT NULL,
    schema_version TEXT NOT NULL,
    expected_top_level_keys_json TEXT NOT NULL DEFAULT '[]'
        CHECK (json_valid(expected_top_level_keys_json)),
    field_mapping_json TEXT NOT NULL DEFAULT '{}'
        CHECK (json_valid(field_mapping_json)),
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE (schema_name, schema_version)
);

CREATE TABLE IF NOT EXISTS json_ingestion_events (
    id INTEGER PRIMARY KEY,
    analysis_run_id INTEGER REFERENCES analysis_runs(id) ON DELETE CASCADE,
    source_file TEXT NOT NULL,
    document_role TEXT NOT NULL,
    declared_schema_version TEXT,
    observed_top_level_keys_json TEXT NOT NULL DEFAULT '[]'
        CHECK (json_valid(observed_top_level_keys_json)),
    expected_top_level_keys_json TEXT NOT NULL DEFAULT '[]'
        CHECK (json_valid(expected_top_level_keys_json)),
    unmapped_top_level_keys_json TEXT NOT NULL DEFAULT '[]'
        CHECK (json_valid(unmapped_top_level_keys_json)),
    missing_expected_keys_json TEXT NOT NULL DEFAULT '[]'
        CHECK (json_valid(missing_expected_keys_json)),
    importer_name TEXT NOT NULL,
    importer_version TEXT NOT NULL,
    raw_document_hash TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_company_identifiers_lookup
ON company_identifiers (identifier_type, identifier_value, exchange);

CREATE INDEX IF NOT EXISTS idx_analysis_runs_company_date
ON analysis_runs (company_id, research_date);

CREATE INDEX IF NOT EXISTS idx_analysis_runs_uid
ON analysis_runs (run_uid);

CREATE INDEX IF NOT EXISTS idx_sources_type_date
ON sources (source_type, document_date);

CREATE INDEX IF NOT EXISTS idx_evidence_run_layer
ON evidence_items (analysis_run_id, layer_code);

CREATE INDEX IF NOT EXISTS idx_evidence_source
ON evidence_items (source_id);

CREATE INDEX IF NOT EXISTS idx_layers_run_order
ON analysis_layers (analysis_run_id, sort_order);

CREATE INDEX IF NOT EXISTS idx_metrics_run_code
ON analysis_metrics (analysis_run_id, metric_code);

CREATE INDEX IF NOT EXISTS idx_artifacts_run_type
ON content_artifacts (analysis_run_id, artifact_type);

CREATE INDEX IF NOT EXISTS idx_json_ingestion_events_run
ON json_ingestion_events (analysis_run_id, document_role);

CREATE INDEX IF NOT EXISTS idx_json_ingestion_events_schema
ON json_ingestion_events (declared_schema_version, importer_version);

CREATE VIEW IF NOT EXISTS v_run_summary AS
SELECT
    ar.id AS analysis_run_id,
    ar.run_uid,
    c.display_name AS company,
    (
        SELECT ci.exchange || ': ' || ci.identifier_value
        FROM company_identifiers ci
        WHERE ci.company_id = c.id
          AND ci.identifier_type = 'ticker'
        ORDER BY ci.is_primary DESC, ci.id
        LIMIT 1
    ) AS ticker,
    ar.mode,
    ar.research_date,
    af.name AS framework_name,
    af.version AS framework_version,
    ao.total_score,
    ao.display_total_score,
    ao.gate_pass,
    ao.verdict,
    ar.benchmark_ready,
    COUNT(DISTINCT al.id) AS layer_count,
    COUNT(DISTINCT am.id) AS metric_count,
    COUNT(DISTINCT ei.id) AS evidence_count,
    COUNT(DISTINCT rsr.id) AS source_count
FROM analysis_runs ar
JOIN companies c ON c.id = ar.company_id
LEFT JOIN analysis_frameworks af ON af.id = ar.framework_id
LEFT JOIN analysis_outputs ao ON ao.analysis_run_id = ar.id
LEFT JOIN analysis_layers al ON al.analysis_run_id = ar.id
LEFT JOIN analysis_metrics am ON am.analysis_run_id = ar.id
LEFT JOIN evidence_items ei ON ei.analysis_run_id = ar.id
LEFT JOIN run_source_refs rsr ON rsr.analysis_run_id = ar.id
GROUP BY ar.id;

CREATE VIEW IF NOT EXISTS v_metric_evidence AS
SELECT
    ar.run_uid,
    c.display_name AS company,
    al.label AS layer,
    am.metric_code,
    am.label AS metric_label,
    am.value,
    am.weight,
    ei.local_evidence_id,
    ei.fact_type,
    ei.fact,
    s.title AS source_title,
    s.publisher,
    s.canonical_url
FROM analysis_metrics am
JOIN analysis_layers al ON al.id = am.layer_id
JOIN analysis_runs ar ON ar.id = am.analysis_run_id
JOIN companies c ON c.id = ar.company_id
LEFT JOIN metric_evidence_links mel ON mel.metric_id = am.id
LEFT JOIN evidence_items ei ON ei.id = mel.evidence_item_id
LEFT JOIN sources s ON s.id = ei.source_id;

CREATE VIEW IF NOT EXISTS v_schema_observations AS
SELECT
    jie.id,
    ar.run_uid,
    jie.source_file,
    jie.document_role,
    jie.declared_schema_version,
    jie.unmapped_top_level_keys_json,
    jie.missing_expected_keys_json,
    jie.importer_name,
    jie.importer_version,
    jie.created_at
FROM json_ingestion_events jie
LEFT JOIN analysis_runs ar ON ar.id = jie.analysis_run_id;
