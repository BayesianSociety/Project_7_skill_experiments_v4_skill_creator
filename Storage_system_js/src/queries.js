import { tableCounts } from "./db.js";

export function getStatus(db) {
  return tableCounts(db);
}

export function listRuns(db) {
  return db.prepare(`
    SELECT run_uid, company, ticker, research_date, display_total_score,
           gate_pass, verdict, source_count, evidence_count, metric_count
    FROM v_run_summary
    ORDER BY COALESCE(research_date, ''), company
  `).all();
}

export function getCompanies(db) {
  return db.prepare(`
    SELECT
      c.id,
      c.display_name,
      c.legal_name,
      c.slug,
      COUNT(DISTINCT ar.id) AS analysis_run_count,
      MAX(ar.research_date) AS latest_research_date
    FROM companies c
    LEFT JOIN analysis_runs ar ON ar.company_id = c.id
    GROUP BY c.id
    ORDER BY c.display_name
  `).all();
}

export function getRunByUid(db, runUid) {
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
  return {
    summary,
    focus_technologies: JSON.parse(run.focus_technologies_json),
    research_context: JSON.parse(run.research_context_json),
    layers,
    metrics
  };
}

export function getEvidenceForRun(db, runUid) {
  const summary = db.prepare("SELECT analysis_run_id FROM v_run_summary WHERE run_uid = ?").get(runUid);
  if (!summary) return null;
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
  `).all(summary.analysis_run_id);
}

export function getMetricEvidence(db, runUid) {
  const params = [];
  let where = "";
  if (runUid) {
    where = "WHERE run_uid = ?";
    params.push(runUid);
  }
  return db.prepare(`
    SELECT *
    FROM v_metric_evidence
    ${where}
    ORDER BY company, layer, metric_code, local_evidence_id
  `).all(...params);
}

export function getSchemaObservations(db) {
  return db.prepare(`
    SELECT *
    FROM v_schema_observations
    ORDER BY created_at DESC, id DESC
  `).all();
}

export function createContentArtifact(db, input) {
  const run = input.run_uid
    ? db.prepare("SELECT id, company_id FROM analysis_runs WHERE run_uid = ?").get(input.run_uid)
    : null;
  const info = db.prepare(`
    INSERT INTO content_artifacts
      (analysis_run_id, company_id, artifact_type, title, status, content_json,
       file_path, rendered_html, theme, metadata_json)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `).run(
    run?.id || null,
    input.company_id || run?.company_id || null,
    input.artifact_type,
    input.title || null,
    input.status || "draft",
    JSON.stringify(input.content || {}),
    input.file_path || null,
    input.rendered_html || null,
    input.theme || null,
    JSON.stringify(input.metadata || {})
  );
  return db.prepare("SELECT * FROM content_artifacts WHERE id = ?").get(Number(info.lastInsertRowid));
}

