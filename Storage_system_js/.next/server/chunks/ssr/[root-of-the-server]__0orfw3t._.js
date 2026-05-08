module.exports=[93695,(a,b,c)=>{b.exports=a.x("next/dist/shared/lib/no-fallback-error.external.js",()=>require("next/dist/shared/lib/no-fallback-error.external.js"))},50227,(a,b,c)=>{b.exports=a.x("node:path",()=>require("node:path"))},85148,(a,b,c)=>{b.exports=a.x("better-sqlite3-90e2652d1716b047",()=>require("better-sqlite3-90e2652d1716b047"))},71306,(a,b,c)=>{b.exports=a.r(18622)},79847,a=>{a.n(a.i(3343))},9185,a=>{a.n(a.i(29432))},72842,a=>{a.n(a.i(75164))},54897,a=>{a.n(a.i(30106))},56157,a=>{a.n(a.i(18970))},94331,a=>{a.n(a.i(60644))},15988,a=>{a.n(a.i(56952))},25766,a=>{a.n(a.i(77341))},29725,a=>{a.n(a.i(94290))},5785,a=>{a.n(a.i(90588))},74793,a=>{a.n(a.i(33169))},85826,a=>{a.n(a.i(37111))},21565,a=>{a.n(a.i(41763))},65911,a=>{a.n(a.i(8950))},25128,a=>{a.n(a.i(91562))},40781,a=>{a.n(a.i(49670))},69411,a=>{a.n(a.i(75700))},63081,a=>{a.n(a.i(276))},62837,a=>{a.n(a.i(40795))},34607,a=>{a.n(a.i(11614))},96338,a=>{a.n(a.i(21751))},50642,a=>{a.n(a.i(12213))},32242,a=>{a.n(a.i(22693))},88530,a=>{a.n(a.i(10531))},8583,a=>{a.n(a.i(1082))},38534,a=>{a.n(a.i(98175))},70408,a=>{a.n(a.i(9095))},22922,a=>{a.n(a.i(96772))},78294,a=>{a.n(a.i(71717))},16625,a=>{a.n(a.i(85034))},88648,a=>{a.n(a.i(68113))},51914,a=>{a.n(a.i(66482))},25466,a=>{a.n(a.i(91505))},96544,a=>{"use strict";a.s(["default",()=>b]);let b=(0,a.i(11857).registerClientReference)(function(){throw Error("Attempted to call the default export of [project]/app/components/DashboardClient.jsx <module evaluation> from the server, but it's on the client. It's not possible to invoke a client function from the server, it can only be rendered as a Component or passed to props of a Client Component.")},"[project]/app/components/DashboardClient.jsx <module evaluation>","default")},10558,a=>{"use strict";a.s(["default",()=>b]);let b=(0,a.i(11857).registerClientReference)(function(){throw Error("Attempted to call the default export of [project]/app/components/DashboardClient.jsx from the server, but it's on the client. It's not possible to invoke a client function from the server, it can only be rendered as a Component or passed to props of a Client Component.")},"[project]/app/components/DashboardClient.jsx","default")},70274,a=>{"use strict";a.i(96544);var b=a.i(10558);a.n(b)},65127,a=>{"use strict";var b=a.i(7997),c=a.i(70274),d=a.i(50227),e=a.i(85148);let f=d.default.join(process.cwd(),"storage_js.db");function g(a){return{...a,gate_pass:!!a.gate_pass}}a.s(["default",0,function(){let a=function(){let a=new e.default(f,{readonly:!0,fileMustExist:!0});try{let b=Object.fromEntries(["companies","company_identifiers","analysis_frameworks","analysis_runs","analysis_layers","analysis_metrics","sources","run_source_refs","evidence_items","metric_evidence_links","analysis_outputs","content_artifacts","raw_documents","json_ingestion_events","schema_registry"].map(b=>[b,a.prepare(`SELECT COUNT(*) AS n FROM ${b}`).get().n])),c=a.prepare(`
    SELECT run_uid, company, ticker, research_date, display_total_score,
           gate_pass, verdict, source_count, evidence_count, metric_count
    FROM v_run_summary
    ORDER BY COALESCE(research_date, ''), company
  `).all().map(g),d=a.prepare(`
    SELECT *
    FROM v_schema_observations
    ORDER BY created_at DESC, id DESC
  `).all().map(a=>({...a,unmapped:JSON.parse(a.unmapped_top_level_keys_json||"[]"),missing:JSON.parse(a.missing_expected_keys_json||"[]")})),e=Object.fromEntries(c.map(b=>{var c,d;let e;return[b.run_uid,{...function(a,b){let c=a.prepare("SELECT * FROM v_run_summary WHERE run_uid = ?").get(b);if(!c)return null;let d=a.prepare("SELECT * FROM analysis_runs WHERE id = ?").get(c.analysis_run_id),e=a.prepare(`
    SELECT * FROM analysis_layers
    WHERE analysis_run_id = ?
    ORDER BY sort_order
  `).all(c.analysis_run_id),f=a.prepare(`
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
  `).all(c.analysis_run_id),g={};try{g=JSON.parse(d.raw_scored_json||"{}")}catch{g={}}return{summary:{...c,gate_pass:!!c.gate_pass,benchmark_ready:!!c.benchmark_ready},focus_technologies:JSON.parse(d.focus_technologies_json||"[]"),research_context:JSON.parse(d.research_context_json||"{}"),narrative:{dashboard_content:g.dashboard_content||null,claims:Array.isArray(g.claims)?g.claims:[]},layers:e,metrics:f}}(a,b.run_uid),evidence:(c=b.run_uid,(e=a.prepare("SELECT analysis_run_id FROM v_run_summary WHERE run_uid = ?").get(c))?a.prepare(`
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
  `).all(e.analysis_run_id).map(a=>({...a,verified:!!a.verified})):[]),metricEvidence:(d=b.run_uid,a.prepare(`
    SELECT *
    FROM v_metric_evidence
    WHERE run_uid = ?
    ORDER BY company, layer, metric_code, local_evidence_id
  `).all(d))}]}));return{status:b,runs:c,schemaObservations:d,runDetails:e,generatedAt:new Date().toISOString()}}finally{a.close()}}();return(0,b.jsx)(c.default,{data:a})},"dynamic",0,"force-dynamic"],65127)},82894,a=>{a.n(a.i(65127))}];

//# sourceMappingURL=%5Broot-of-the-server%5D__0orfw3t._.js.map