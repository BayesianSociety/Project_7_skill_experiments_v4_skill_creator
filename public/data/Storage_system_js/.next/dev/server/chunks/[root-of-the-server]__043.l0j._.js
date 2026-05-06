module.exports = [
"[externals]/next/dist/compiled/next-server/app-route-turbo.runtime.dev.js [external] (next/dist/compiled/next-server/app-route-turbo.runtime.dev.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/compiled/next-server/app-route-turbo.runtime.dev.js", () => require("next/dist/compiled/next-server/app-route-turbo.runtime.dev.js"));

module.exports = mod;
}),
"[externals]/next/dist/compiled/@opentelemetry/api [external] (next/dist/compiled/@opentelemetry/api, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/compiled/@opentelemetry/api", () => require("next/dist/compiled/@opentelemetry/api"));

module.exports = mod;
}),
"[externals]/next/dist/compiled/next-server/app-page-turbo.runtime.dev.js [external] (next/dist/compiled/next-server/app-page-turbo.runtime.dev.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/compiled/next-server/app-page-turbo.runtime.dev.js", () => require("next/dist/compiled/next-server/app-page-turbo.runtime.dev.js"));

module.exports = mod;
}),
"[externals]/next/dist/server/app-render/work-unit-async-storage.external.js [external] (next/dist/server/app-render/work-unit-async-storage.external.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/server/app-render/work-unit-async-storage.external.js", () => require("next/dist/server/app-render/work-unit-async-storage.external.js"));

module.exports = mod;
}),
"[externals]/next/dist/server/app-render/work-async-storage.external.js [external] (next/dist/server/app-render/work-async-storage.external.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/server/app-render/work-async-storage.external.js", () => require("next/dist/server/app-render/work-async-storage.external.js"));

module.exports = mod;
}),
"[externals]/next/dist/shared/lib/no-fallback-error.external.js [external] (next/dist/shared/lib/no-fallback-error.external.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/shared/lib/no-fallback-error.external.js", () => require("next/dist/shared/lib/no-fallback-error.external.js"));

module.exports = mod;
}),
"[externals]/node:path [external] (node:path, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("node:path", () => require("node:path"));

module.exports = mod;
}),
"[project]/lib/dashboard-data.js [app-route] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "getDashboardData",
    ()=>getDashboardData
]);
var __TURBOPACK__imported__module__$5b$externals$5d2f$node$3a$path__$5b$external$5d$__$28$node$3a$path$2c$__cjs$29$__ = __turbopack_context__.i("[externals]/node:path [external] (node:path, cjs)");
var __TURBOPACK__imported__module__$5b$externals$5d2f$better$2d$sqlite3__$5b$external$5d$__$28$better$2d$sqlite3$2c$__cjs$2c$__$5b$project$5d2f$node_modules$2f$better$2d$sqlite3$29$__ = __turbopack_context__.i("[externals]/better-sqlite3 [external] (better-sqlite3, cjs, [project]/node_modules/better-sqlite3)");
;
;
const DB_PATH = __TURBOPACK__imported__module__$5b$externals$5d2f$node$3a$path__$5b$external$5d$__$28$node$3a$path$2c$__cjs$29$__["default"].join(process.cwd(), "storage_js.db");
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
    return Object.fromEntries(tables.map((table)=>[
            table,
            db.prepare(`SELECT COUNT(*) AS n FROM ${table}`).get().n
        ]));
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
    } catch  {
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
  `).all(summary.analysis_run_id).map((row)=>({
            ...row,
            verified: Boolean(row.verified)
        }));
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
  `).all().map((row)=>({
            ...row,
            unmapped: JSON.parse(row.unmapped_top_level_keys_json || "[]"),
            missing: JSON.parse(row.missing_expected_keys_json || "[]")
        }));
}
function getDashboardData() {
    const db = new __TURBOPACK__imported__module__$5b$externals$5d2f$better$2d$sqlite3__$5b$external$5d$__$28$better$2d$sqlite3$2c$__cjs$2c$__$5b$project$5d2f$node_modules$2f$better$2d$sqlite3$29$__["default"](DB_PATH, {
        readonly: true,
        fileMustExist: true
    });
    try {
        const status = tableCounts(db);
        const runs = listRuns(db);
        const schemaObservations = getSchemaObservations(db);
        const runDetails = Object.fromEntries(runs.map((run)=>[
                run.run_uid,
                {
                    ...getRunByUid(db, run.run_uid),
                    evidence: getEvidenceForRun(db, run.run_uid),
                    metricEvidence: getMetricEvidence(db, run.run_uid)
                }
            ]));
        return {
            status,
            runs,
            schemaObservations,
            runDetails,
            generatedAt: new Date().toISOString()
        };
    } finally{
        db.close();
    }
}
}),
"[project]/app/api/status/route.js [app-route] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "GET",
    ()=>GET,
    "dynamic",
    ()=>dynamic
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$lib$2f$dashboard$2d$data$2e$js__$5b$app$2d$route$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/lib/dashboard-data.js [app-route] (ecmascript)");
;
const dynamic = "force-dynamic";
function GET() {
    const data = (0, __TURBOPACK__imported__module__$5b$project$5d2f$lib$2f$dashboard$2d$data$2e$js__$5b$app$2d$route$5d$__$28$ecmascript$29$__["getDashboardData"])();
    return Response.json(data.status);
}
}),
];

//# sourceMappingURL=%5Broot-of-the-server%5D__043.l0j._.js.map