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

SELECT 'Top evidence-backed metrics' AS section;

SELECT
  run_uid,
  company,
  layer,
  metric_code,
  metric_label,
  value,
  local_evidence_id,
  fact_type,
  substr(fact, 1, 100) AS fact_preview,
  publisher
FROM v_metric_evidence
WHERE local_evidence_id IS NOT NULL
ORDER BY company, layer, metric_code, local_evidence_id
LIMIT 25;

SELECT 'Raw JSON availability' AS section;

SELECT
  run_uid,
  raw_payload_json IS NOT NULL AS has_payload_json,
  raw_scored_json IS NOT NULL AS has_scored_json,
  length(raw_payload_json) AS payload_bytes,
  length(raw_scored_json) AS scored_bytes
FROM analysis_runs
ORDER BY run_uid;
