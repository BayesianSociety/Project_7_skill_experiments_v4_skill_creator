import path from "node:path";
import Database from "better-sqlite3";

const DB_PATH = path.join(process.cwd(), "storage_js.db");

function tableCounts(db) {
  const tables = [
    "companies",
    "company_identifiers",
    "analysis_frameworks",
    "analysis_runs",
    "analysis_layers",
    "analysis_metrics",
    "sources",
    "run_source_refs",
    "evidence_items",
    "metric_evidence_links",
    "analysis_outputs",
    "content_artifacts",
    "raw_documents",
    "json_ingestion_events",
    "schema_registry"
  ];

  return Object.fromEntries(
    tables.map((table) => [table, db.prepare(`SELECT COUNT(*) AS n FROM ${table}`).get().n])
  );
}

function normalizeRun(run) {
  return {
    ...run,
    gate_pass: Boolean(run.gate_pass)
  };
}

function listRuns(db) {
  return db.prepare(`
    SELECT run_uid, company, ticker, research_date, display_total_score,
           gate_pass, verdict, source_count, evidence_count, metric_count
    FROM v_run_summary
    ORDER BY COALESCE(research_date, ''), company
  `).all().map(normalizeRun);
}

function getRunByUid(db, runUid) {
  const summary = db.prepare("SELECT * FROM v_run_summary WHERE run_uid = ?").get(runUid);
  if (!summary) return null;

  const run = db.prepare("SELECT * FROM analysis_runs WHERE id = ?").get(summary.analysis_run_id);
  const layers = db.prepare(`
    SELECT * FROM analysis_layers
    WHERE analysis_run_id = ?
    ORDER BY sort_order
  `).all(summary.analysis_run_id);
  const metrics = db.prepare(`
    SELECT
      am.id,
      al.label AS layer,
      am.metric_code,
      am.label,
      am.value,
      am.weight,
      am.unit,
      am.source_type,
      am.verified,
      am.normalization_method
    FROM analysis_metrics am
    JOIN analysis_layers al ON al.id = am.layer_id
    WHERE am.analysis_run_id = ?
    ORDER BY al.sort_order, am.metric_code
  `).all(summary.analysis_run_id);

  let rawScored = {};
  try {
    rawScored = JSON.parse(run.raw_scored_json || "{}");
  } catch {
    rawScored = {};
  }

  return {
    summary: {
      ...summary,
      gate_pass: Boolean(summary.gate_pass),
      benchmark_ready: Boolean(summary.benchmark_ready)
    },
    focus_technologies: JSON.parse(run.focus_technologies_json || "[]"),
    research_context: JSON.parse(run.research_context_json || "{}"),
    narrative: {
      dashboard_content: rawScored.dashboard_content || null,
      claims: Array.isArray(rawScored.claims) ? rawScored.claims : []
    },
    layers,
    metrics
  };
}

function getEvidenceForRun(db, runUid) {
  const summary = db.prepare("SELECT analysis_run_id FROM v_run_summary WHERE run_uid = ?").get(runUid);
  if (!summary) return [];

  return db.prepare(`
    SELECT
      ei.local_evidence_id,
      ei.layer_label,
      ei.fact_type,
      ei.fact,
      ei.raw_value,
      ei.raw_unit,
      ei.period_start,
      ei.period_end,
      ei.verified,
      s.title AS source_title,
      s.publisher,
      s.canonical_url
    FROM evidence_items ei
    LEFT JOIN sources s ON s.id = ei.source_id
    WHERE ei.analysis_run_id = ?
    ORDER BY ei.local_evidence_id
  `).all(summary.analysis_run_id).map((row) => ({
    ...row,
    verified: Boolean(row.verified)
  }));
}

function getSourcesForRun(db, runUid) {
  const summary = db.prepare("SELECT analysis_run_id FROM v_run_summary WHERE run_uid = ?").get(runUid);
  if (!summary) return [];

  return db.prepare(`
    SELECT
      rsr.local_source_id,
      s.title,
      s.publisher,
      s.canonical_url,
      s.source_type,
      s.document_date
    FROM run_source_refs rsr
    JOIN sources s ON s.id = rsr.source_id
    WHERE rsr.analysis_run_id = ?
    ORDER BY rsr.local_source_id
  `).all(summary.analysis_run_id);
}

function getMetricEvidence(db, runUid) {
  return db.prepare(`
    SELECT *
    FROM v_metric_evidence
    WHERE run_uid = ?
    ORDER BY company, layer, metric_code, local_evidence_id
  `).all(runUid);
}

function getSchemaObservations(db) {
  return db.prepare(`
    SELECT *
    FROM v_schema_observations
    ORDER BY created_at DESC, id DESC
  `).all().map((row) => ({
    ...row,
    unmapped: JSON.parse(row.unmapped_top_level_keys_json || "[]"),
    missing: JSON.parse(row.missing_expected_keys_json || "[]")
  }));
}

function indexBy(rows, key) {
  return Object.fromEntries(
    rows
      .filter((row) => row?.[key])
      .map((row) => [String(row[key]), row])
  );
}

function buildReferenceIndex(run, evidence, sources) {
  const claims = run?.narrative?.claims || [];
  return {
    claimsById: indexBy(claims, "claim_id"),
    evidenceById: indexBy(evidence, "local_evidence_id"),
    sourcesById: indexBy(sources, "local_source_id")
  };
}

export function getDashboardData() {
  const db = new Database(DB_PATH, { readonly: true, fileMustExist: true });
  try {
    const status = tableCounts(db);
    const runs = listRuns(db);
    const schemaObservations = getSchemaObservations(db);
    const runDetails = Object.fromEntries(
      runs.map((run) => {
        const detail = getRunByUid(db, run.run_uid);
        const evidence = getEvidenceForRun(db, run.run_uid);
        const sources = getSourcesForRun(db, run.run_uid);
        return [
          run.run_uid,
          {
            ...detail,
            evidence,
            sources,
            metricEvidence: getMetricEvidence(db, run.run_uid),
            referenceIndex: buildReferenceIndex(detail, evidence, sources)
          }
        ];
      })
    );

    return {
      status,
      runs,
      schemaObservations,
      runDetails,
      generatedAt: new Date().toISOString()
    };
  } finally {
    db.close();
  }
}
