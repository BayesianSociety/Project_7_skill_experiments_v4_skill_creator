import fs from "node:fs";
import path from "node:path";
import {
  IMPORTER_NAME,
  IMPORTER_VERSION,
  asBoolInt,
  parseTicker,
  prettyJson,
  readJson,
  removePayloadSuffix,
  sha256Text,
  slugify,
  sourceDedupeKey,
  stableJson
} from "./utils.js";

function getExpectedKeys(db, schemaName, schemaVersion) {
  const row = db.prepare(`
    SELECT expected_top_level_keys_json
    FROM schema_registry
    WHERE schema_name = ? AND schema_version = ?
  `).get(schemaName, schemaVersion);
  if (!row) return [];
  return JSON.parse(row.expected_top_level_keys_json);
}

function schemaVersionFor(document) {
  return document?.schema_version ? String(document.schema_version) : "legacy";
}

function observeJsonSchema(db, runId, sourceFile, role, document) {
  if (!document) return;
  const schemaName = role === "payload" ? "analysis_payload" : "analysis_scored";
  const declaredSchemaVersion = schemaVersionFor(document);
  const observed = Object.keys(document).sort();
  const expected = getExpectedKeys(db, schemaName, declaredSchemaVersion).sort();
  const expectedSet = new Set(expected);
  const observedSet = new Set(observed);
  const unmapped = observed.filter((key) => !expectedSet.has(key));
  const missing = expected.filter((key) => !observedSet.has(key));

  db.prepare(`
    INSERT INTO json_ingestion_events
      (analysis_run_id, source_file, document_role, declared_schema_version,
       observed_top_level_keys_json, expected_top_level_keys_json,
       unmapped_top_level_keys_json, missing_expected_keys_json,
       importer_name, importer_version, raw_document_hash)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `).run(
    runId,
    sourceFile,
    role,
    declaredSchemaVersion,
    stableJson(observed),
    stableJson(expected),
    stableJson(unmapped),
    stableJson(missing),
    IMPORTER_NAME,
    IMPORTER_VERSION,
    sha256Text(stableJson(document))
  );
}

function upsertCompany(db, companyName, ticker, identifiers = {}) {
  const slug = slugify(companyName);
  db.prepare(`
    INSERT INTO companies (legal_name, display_name, slug, metadata_json)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(slug) DO UPDATE SET
      legal_name = excluded.legal_name,
      display_name = excluded.display_name,
      metadata_json = excluded.metadata_json,
      updated_at = datetime('now')
  `).run(companyName, companyName, slug, stableJson({ source_identifiers: identifiers }));

  const companyId = db.prepare("SELECT id FROM companies WHERE slug = ?").get(slug).id;
  const parsedTicker = parseTicker(ticker);
  if (parsedTicker.value) {
    db.prepare(`
      INSERT OR IGNORE INTO company_identifiers
        (company_id, identifier_type, identifier_value, exchange, is_primary)
      VALUES (?, 'ticker', ?, ?, 1)
    `).run(companyId, parsedTicker.value, parsedTicker.exchange);
  }

  if (identifiers.cik) {
    db.prepare(`
      INSERT OR IGNORE INTO company_identifiers
        (company_id, identifier_type, identifier_value, is_primary)
      VALUES (?, 'cik', ?, 0)
    `).run(companyId, String(identifiers.cik));
  }

  return companyId;
}

function upsertFramework(db, payload, scored) {
  const merged = payload || scored || {};
  const skill = merged.skill_metadata || {};
  const scorer = scored?.scorer_metadata || {};
  const name = skill.skill_name || "legacy-innovation-analysis";
  const version = skill.skill_version || merged.schema_version || "legacy";
  const schemaVersion = merged.schema_version || "legacy";
  const scorerName = scorer.scorer_name || skill.scorer_name || "";
  const scorerVersion = scorer.scorer_version || skill.scorer_version || "";
  const metricRulesVersion = scorer.metric_rules_version || skill.metric_rules_version || "";

  db.prepare(`
    INSERT INTO analysis_frameworks
      (name, version, schema_version, scorer_name, scorer_version, metric_rules_version, definition_json)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(name, version, schema_version, scorer_name, scorer_version, metric_rules_version)
    DO UPDATE SET definition_json = excluded.definition_json
  `).run(
    name,
    version,
    schemaVersion,
    scorerName,
    scorerVersion,
    metricRulesVersion,
    stableJson({ skill_metadata: skill, scorer_metadata: scorer, schema_version: schemaVersion })
  );

  return db.prepare(`
    SELECT id
    FROM analysis_frameworks
    WHERE name = ?
      AND version = ?
      AND schema_version = ?
      AND scorer_name = ?
      AND scorer_version = ?
      AND metric_rules_version = ?
  `).get(name, version, schemaVersion, scorerName, scorerVersion, metricRulesVersion).id;
}

function deriveRunUid(stem, payload, scored) {
  const run = payload.research_run || scored?.research_run || {};
  return run.run_id ? String(run.run_id) : String(payload.run_id || scored?.run_id || stem);
}

function insertSources(db, runId, payload, scored) {
  const sourceMap = new Map();
  const sourceItems = Array.isArray(payload.sources) ? payload.sources : Array.isArray(scored?.sources) ? scored.sources : [];
  const upsert = db.prepare(`
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
  `);
  const insertRef = db.prepare(`
    INSERT INTO run_source_refs
      (analysis_run_id, source_id, local_source_id, accessed_at, raw_source_json)
    VALUES (?, ?, ?, ?, ?)
  `);

  sourceItems.forEach((source, index) => {
    if (!source || typeof source !== "object" || Array.isArray(source)) return;
    const localSourceId = String(source.source_id || `source_${index + 1}`);
    const dedupeKey = sourceDedupeKey(source);
    const urlHash = sha256Text(dedupeKey);
    upsert.run(
      source.url || null,
      urlHash,
      source.title || null,
      source.publisher || null,
      source.source_type || null,
      source.document_date || null,
      source.reliability || null,
      source.availability || null,
      source.notes || null,
      stableJson({ dedupe_key: dedupeKey })
    );
    const sourceId = db.prepare("SELECT id FROM sources WHERE url_hash = ?").get(urlHash).id;
    sourceMap.set(localSourceId, sourceId);
    insertRef.run(runId, sourceId, localSourceId, source.accessed_at || null, stableJson(source));
  });

  return sourceMap;
}

function insertEvidence(db, runId, payload, scored, sourceMap) {
  const evidenceMap = new Map();
  const evidenceItems = Array.isArray(payload.evidence_items)
    ? payload.evidence_items
    : Array.isArray(scored?.evidence_items)
      ? scored.evidence_items
      : [];
  const insert = db.prepare(`
    INSERT INTO evidence_items
      (analysis_run_id, source_id, local_evidence_id, layer_code, layer_label,
       fact_type, fact, quote_or_excerpt, raw_value, raw_unit, period_start,
       period_end, company_attributable, field_proxy, location, verified,
       limitations, metric_codes_json, raw_evidence_json)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `);

  evidenceItems.forEach((evidence, index) => {
    if (!evidence || typeof evidence !== "object" || Array.isArray(evidence)) return;
    const localEvidenceId = String(evidence.evidence_id || `ev_${String(index + 1).padStart(3, "0")}`);
    const metricCodes = Array.isArray(evidence.metric_codes) ? evidence.metric_codes : [];
    insert.run(
      runId,
      sourceMap.get(String(evidence.source_id)) || null,
      localEvidenceId,
      slugify(evidence.layer || ""),
      evidence.layer || null,
      evidence.fact_type || null,
      evidence.fact || null,
      evidence.quote_or_excerpt || null,
      typeof evidence.raw_value === "number" ? evidence.raw_value : null,
      evidence.raw_unit || null,
      evidence.period_start || null,
      evidence.period_end || null,
      asBoolInt(evidence.company_attributable),
      asBoolInt(evidence.field_proxy),
      evidence.location || null,
      asBoolInt(evidence.verified),
      evidence.limitations || null,
      stableJson(metricCodes),
      stableJson(evidence)
    );
    const evidenceId = db.prepare(`
      SELECT id FROM evidence_items
      WHERE analysis_run_id = ? AND local_evidence_id = ?
    `).get(runId, localEvidenceId).id;
    evidenceMap.set(localEvidenceId, evidenceId);
  });

  return evidenceMap;
}

function chooseLayers(payload, scored) {
  if (Array.isArray(scored?.layers)) return scored.layers.filter((layer) => layer && typeof layer === "object");
  if (Array.isArray(payload.layers)) return payload.layers.filter((layer) => layer && typeof layer === "object");
  return [];
}

function insertLayersAndMetrics(db, runId, payload, scored, evidenceMap) {
  const insertLayer = db.prepare(`
    INSERT INTO analysis_layers
      (analysis_run_id, layer_code, label, sort_order, summary, strong, missing,
       coverage_ratio, score, raw_score, normalized_score, confidence,
       confidence_penalty, display_score, caps_json, cap_reasons_json, raw_layer_json)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `);
  const insertMetric = db.prepare(`
    INSERT INTO analysis_metrics
      (analysis_run_id, layer_id, metric_code, label, value, weight, unit,
       source_type, verified, normalization_method, normalization_json, raw_metric_json)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `);
  const link = db.prepare(`
    INSERT OR IGNORE INTO metric_evidence_links
      (metric_id, evidence_item_id, relationship_type)
    VALUES (?, ?, 'supports')
  `);

  chooseLayers(payload, scored).forEach((layer, index) => {
    const label = String(layer.label || `Layer ${index + 1}`);
    const layerCode = slugify(label);
    insertLayer.run(
      runId,
      layerCode,
      label,
      index,
      layer.summary || null,
      layer.strong || null,
      layer.missing || null,
      layer.coverage_ratio ?? null,
      layer.score ?? null,
      layer.raw_score ?? null,
      layer.normalized_score ?? null,
      layer.confidence || null,
      layer.confidence_penalty ?? null,
      layer.display_score || null,
      stableJson(Array.isArray(layer.caps) ? layer.caps : []),
      stableJson(Array.isArray(layer.cap_reasons) ? layer.cap_reasons : []),
      stableJson(layer)
    );
    const layerId = db.prepare(`
      SELECT id FROM analysis_layers
      WHERE analysis_run_id = ? AND layer_code = ?
    `).get(runId, layerCode).id;

    const metrics = Array.isArray(layer.metrics) ? layer.metrics : [];
    metrics.forEach((metric, metricIndex) => {
      if (!metric || typeof metric !== "object" || Array.isArray(metric)) return;
      const metricCode = String(metric.code || `metric_${metricIndex + 1}`);
      const normalization = metric.normalization && typeof metric.normalization === "object" && !Array.isArray(metric.normalization)
        ? metric.normalization
        : {};
      insertMetric.run(
        runId,
        layerId,
        metricCode,
        metric.label || null,
        metric.value ?? null,
        metric.weight ?? null,
        metric.unit || null,
        metric.source_type || null,
        asBoolInt(metric.verified),
        normalization.method || null,
        stableJson(normalization),
        stableJson(metric)
      );
      const metricId = db.prepare(`
        SELECT id FROM analysis_metrics
        WHERE analysis_run_id = ? AND layer_id = ? AND metric_code = ?
      `).get(runId, layerId, metricCode).id;

      const evidenceIds = Array.isArray(metric.evidence_ids) ? metric.evidence_ids : [];
      evidenceIds.forEach((localEvidenceId) => {
        const evidenceId = evidenceMap.get(String(localEvidenceId));
        if (evidenceId) link.run(metricId, evidenceId);
      });
    });
  });

  const evidenceRows = db.prepare(`
    SELECT id, metric_codes_json
    FROM evidence_items
    WHERE analysis_run_id = ?
  `).all(runId);
  const metricLookup = db.prepare(`
    SELECT id FROM analysis_metrics
    WHERE analysis_run_id = ? AND metric_code = ?
  `);
  evidenceRows.forEach((evidence) => {
    JSON.parse(evidence.metric_codes_json).forEach((metricCode) => {
      metricLookup.all(runId, String(metricCode)).forEach((metric) => {
        link.run(metric.id, evidence.id);
      });
    });
  });
}

function insertOutput(db, runId, scored) {
  if (!scored) return;
  const scorerMetadata = scored.scorer_metadata && typeof scored.scorer_metadata === "object" ? scored.scorer_metadata : {};
  db.prepare(`
    INSERT INTO analysis_outputs
      (analysis_run_id, total_score, display_total_score, gate_pass, verdict,
       scorer_metadata_json, formula)
    VALUES (?, ?, ?, ?, ?, ?, ?)
  `).run(
    runId,
    scored.total_score ?? null,
    scored.display_total_score || null,
    asBoolInt(scored.gate_pass),
    scored.verdict || null,
    stableJson(scorerMetadata),
    scorerMetadata.formula || null
  );
}

const SKIPPED_SOURCE_DIRS = new Set([
  ".git",
  ".next",
  "node_modules"
]);

function shouldSkipSourceDir(name) {
  return SKIPPED_SOURCE_DIRS.has(name);
}

export function findPairs(sourceDir) {
  const resolved = path.resolve(sourceDir);
  const pairs = [];
  const seenPayloads = new Set();

  function addPair(payloadPath, scoredPath) {
    const resolvedPayload = path.resolve(payloadPath);
    if (seenPayloads.has(resolvedPayload)) return;
    seenPayloads.add(resolvedPayload);
    pairs.push({
      payloadPath: resolvedPayload,
      scoredPath: fs.existsSync(scoredPath) ? path.resolve(scoredPath) : null,
      sourceDir: path.dirname(resolvedPayload)
    });
  }

  function walk(dir) {
    fs.readdirSync(dir, { withFileTypes: true }).forEach((entry) => {
      const entryPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        if (!shouldSkipSourceDir(entry.name)) walk(entryPath);
        return;
      }
      if (!entry.isFile()) return;

      if (entry.name.endsWith("_payload.json")) {
        addPair(entryPath, path.join(dir, entry.name.replace("_payload.json", "_scored.json")));
      } else if (entry.name === "payload.json") {
        addPair(entryPath, path.join(dir, "scored.json"));
      }
    });
  }

  walk(resolved);
  return pairs.sort((a, b) => a.payloadPath.localeCompare(b.payloadPath));
}

export function importPair(db, payloadPath, scoredPath, sourceDir) {
  const payload = readJson(payloadPath);
  const scored = scoredPath ? readJson(scoredPath) : null;
  const payloadName = path.basename(payloadPath);
  const stem = payloadName === "payload.json" ? path.basename(path.dirname(payloadPath)) : removePayloadSuffix(payloadName);
  const merged = payload || scored || {};
  const companyName = String(merged.company || scored?.company || stem);
  const ticker = merged.ticker || scored?.ticker || null;
  const researchContext = merged.research_context || {};
  const identifiers = researchContext.company_identifiers && typeof researchContext.company_identifiers === "object"
    ? researchContext.company_identifiers
    : {};
  const companyId = upsertCompany(db, companyName, ticker, identifiers);
  const frameworkId = upsertFramework(db, payload, scored);
  const runUid = deriveRunUid(stem, payload, scored);
  const researchRun = merged.research_run || scored?.research_run || {};
  const payloadRaw = stableJson(payload);
  const scoredRaw = scored ? stableJson(scored) : null;
  const importHash = sha256Text(`${payloadRaw}\n${scoredRaw || ""}`);
  const focusTechnologies = Array.isArray(researchContext.focus_technologies)
    ? researchContext.focus_technologies
    : Array.isArray(merged.focus_technologies)
      ? merged.focus_technologies
      : [];

  db.prepare("DELETE FROM analysis_runs WHERE run_uid = ?").run(runUid);
  const info = db.prepare(`
    INSERT INTO analysis_runs
      (run_uid, company_id, framework_id, mode, research_date, analyst,
       user_request, time_horizon, research_mode, benchmark_ready,
       source_payload_file, source_scored_file, source_directory,
       focus_technologies_json, research_context_json, normalization_notes_json,
       storage_metadata_json, raw_payload_json, raw_scored_json, payload_hash,
       scored_hash, import_hash)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `).run(
    runUid,
    companyId,
    frameworkId,
    merged.mode || scored?.mode || null,
    researchRun.research_date || merged.research_date || null,
    researchRun.analyst || null,
    researchRun.user_request || null,
    researchRun.time_horizon || null,
    researchRun.research_mode || null,
    asBoolInt(merged.benchmark_ready ?? scored?.benchmark_ready),
    payloadPath,
    scoredPath,
    sourceDir,
    stableJson(focusTechnologies),
    stableJson(researchContext),
    stableJson(Array.isArray(merged.normalization_notes) ? merged.normalization_notes : []),
    stableJson(merged.storage_metadata && typeof merged.storage_metadata === "object" ? merged.storage_metadata : {}),
    payloadRaw,
    scoredRaw,
    sha256Text(payloadRaw),
    scoredRaw ? sha256Text(scoredRaw) : null,
    importHash
  );
  const runId = Number(info.lastInsertRowid);

  const sourceMap = insertSources(db, runId, payload, scored);
  const evidenceMap = insertEvidence(db, runId, payload, scored, sourceMap);
  insertLayersAndMetrics(db, runId, payload, scored, evidenceMap);
  insertOutput(db, runId, scored);
  observeJsonSchema(db, runId, payloadPath, "payload", payload);
  if (scored) observeJsonSchema(db, runId, scoredPath, "scored", scored);

  db.prepare(`
    INSERT INTO audit_events (event_type, entity_type, entity_id, details_json)
    VALUES ('imported', 'analysis_run', ?, ?)
  `).run(runId, stableJson({ run_uid: runUid, payload: payloadPath, scored: scoredPath }));

  return runUid;
}

export function ingestDirectory(db, sourceDir) {
  const resolved = path.resolve(sourceDir);
  const pairs = findPairs(resolved);
  if (!pairs.length) {
    throw new Error(`No payload JSON files found in ${resolved}. Expected either *_payload.json files or nested payload.json files.`);
  }
  const transaction = db.transaction(() => pairs.map(({ payloadPath, scoredPath, sourceDir: pairSourceDir }) => importPair(db, payloadPath, scoredPath, pairSourceDir || resolved)));
  return transaction();
}

export function exportRunRaw(db, runRef) {
  const run = resolveRun(db, runRef);
  return {
    run_uid: run.run_uid,
    payload: run.raw_payload_json ? JSON.parse(run.raw_payload_json) : null,
    scored: run.raw_scored_json ? JSON.parse(run.raw_scored_json) : null
  };
}

export function resolveRun(db, runRef) {
  const row = /^\d+$/u.test(String(runRef))
    ? db.prepare("SELECT * FROM analysis_runs WHERE id = ?").get(Number(runRef))
    : db.prepare("SELECT * FROM analysis_runs WHERE run_uid = ?").get(String(runRef));
  if (!row) throw new Error(`Run not found: ${runRef}`);
  return row;
}

export function runSummary(db, runRef) {
  const run = resolveRun(db, runRef);
  const summary = db.prepare("SELECT * FROM v_run_summary WHERE analysis_run_id = ?").get(run.id);
  const layers = db.prepare(`
    SELECT label, score, display_score, coverage_ratio, confidence
    FROM analysis_layers
    WHERE analysis_run_id = ?
    ORDER BY sort_order
  `).all(run.id);
  return {
    summary,
    layers,
    focus_technologies: JSON.parse(run.focus_technologies_json)
  };
}

export function writeJsonFile(filePath, value) {
  fs.writeFileSync(filePath, `${prettyJson(value)}\n`, "utf8");
}
