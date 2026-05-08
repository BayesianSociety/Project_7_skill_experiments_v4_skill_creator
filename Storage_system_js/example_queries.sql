.headers on
.mode column

SELECT 'Run summary' AS section;

SELECT
  run_uid,
  company,
  ticker,
  research_date,
  display_total_score,
  gate_pass,
  source_count,
  evidence_count
FROM v_run_summary
ORDER BY research_date, company;

SELECT 'Schema observations' AS section;

SELECT
  run_uid,
  document_role,
  declared_schema_version,
  unmapped_top_level_keys_json,
  missing_expected_keys_json
FROM v_schema_observations
ORDER BY run_uid, document_role;

SELECT 'Layer scores' AS section;

SELECT
  ar.run_uid,
  c.display_name AS company,
  al.sort_order,
  al.label,
  al.display_score,
  al.confidence,
  al.coverage_ratio
FROM analysis_layers al
JOIN analysis_runs ar ON ar.id = al.analysis_run_id
JOIN companies c ON c.id = ar.company_id
ORDER BY ar.research_date, c.display_name, al.sort_order;

SELECT 'Metrics with evidence count' AS section;

SELECT
  ar.run_uid,
  al.label AS layer,
  am.metric_code,
  am.value,
  am.weight,
  COUNT(mel.evidence_item_id) AS linked_evidence_count
FROM analysis_metrics am
JOIN analysis_layers al ON al.id = am.layer_id
JOIN analysis_runs ar ON ar.id = am.analysis_run_id
LEFT JOIN metric_evidence_links mel ON mel.metric_id = am.id
GROUP BY am.id
ORDER BY ar.run_uid, al.sort_order, am.metric_code;

SELECT 'Content artifacts' AS section;

SELECT
  ca.id,
  vrs.company,
  vrs.run_uid,
  ca.artifact_type,
  ca.title,
  ca.status,
  ca.theme,
  ca.created_at
FROM content_artifacts ca
LEFT JOIN v_run_summary vrs ON vrs.analysis_run_id = ca.analysis_run_id
ORDER BY ca.created_at DESC;

