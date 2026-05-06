import fs from "node:fs";
import path from "node:path";
import Database from "better-sqlite3";
import { SCHEMA_FILE, stableJson } from "./utils.js";

export function openDatabase(dbPath) {
  fs.mkdirSync(path.dirname(dbPath), { recursive: true });
  const db = new Database(dbPath);
  db.pragma("foreign_keys = ON");
  return db;
}

export function initDatabase(dbPath) {
  if (!fs.existsSync(SCHEMA_FILE)) {
    throw new Error(`Missing schema file: ${SCHEMA_FILE}`);
  }
  const db = openDatabase(dbPath);
  db.exec(fs.readFileSync(SCHEMA_FILE, "utf8"));
  seedSchemaRegistry(db);
  return db;
}

export function seedSchemaRegistry(db) {
  const insert = db.prepare(`
    INSERT INTO schema_registry
      (schema_name, schema_version, expected_top_level_keys_json, field_mapping_json, notes)
    VALUES (@schema_name, @schema_version, @expected_top_level_keys_json, @field_mapping_json, @notes)
    ON CONFLICT(schema_name, schema_version) DO UPDATE SET
      expected_top_level_keys_json = excluded.expected_top_level_keys_json,
      field_mapping_json = excluded.field_mapping_json,
      notes = excluded.notes,
      updated_at = datetime('now')
  `);

  insert.run({
    schema_name: "analysis_payload",
    schema_version: "legacy",
    expected_top_level_keys_json: stableJson([
      "company",
      "ticker",
      "mode",
      "benchmark_ready",
      "research_date",
      "focus_technologies",
      "layers"
    ]),
    field_mapping_json: stableJson({
      company: "companies",
      ticker: "company_identifiers",
      layers: "analysis_layers + analysis_metrics",
      focus_technologies: "analysis_runs.focus_technologies_json"
    }),
    notes: "Legacy payload schema found in older local JSON artifacts."
  });

  insert.run({
    schema_name: "analysis_payload",
    schema_version: "2.0",
    expected_top_level_keys_json: stableJson([
      "schema_version",
      "company",
      "ticker",
      "mode",
      "benchmark_ready",
      "skill_metadata",
      "research_run",
      "research_context",
      "sources",
      "evidence_items",
      "layers",
      "normalization_notes",
      "storage_metadata"
    ]),
    field_mapping_json: stableJson({
      research_run: "analysis_runs",
      research_context: "analysis_runs.research_context_json",
      sources: "sources + run_source_refs",
      evidence_items: "evidence_items",
      layers: "analysis_layers + analysis_metrics",
      normalization_notes: "analysis_runs.normalization_notes_json",
      storage_metadata: "analysis_runs.storage_metadata_json"
    }),
    notes: "Richer payload schema with source and evidence support."
  });

  insert.run({
    schema_name: "analysis_scored",
    schema_version: "legacy",
    expected_top_level_keys_json: stableJson([
      "company",
      "ticker",
      "mode",
      "layers",
      "total_score",
      "display_total_score",
      "gate_pass",
      "verdict",
      "benchmark_ready"
    ]),
    field_mapping_json: stableJson({
      layers: "analysis_layers + analysis_metrics",
      total_score: "analysis_outputs.total_score",
      verdict: "analysis_outputs.verdict"
    }),
    notes: "Legacy scored schema."
  });

  insert.run({
    schema_name: "analysis_scored",
    schema_version: "2.0",
    expected_top_level_keys_json: stableJson([
      "schema_version",
      "company",
      "ticker",
      "mode",
      "skill_metadata",
      "research_run",
      "research_context",
      "sources",
      "evidence_items",
      "normalization_notes",
      "layers",
      "total_score",
      "display_total_score",
      "gate_pass",
      "verdict",
      "benchmark_ready",
      "storage_metadata",
      "scorer_metadata"
    ]),
    field_mapping_json: stableJson({
      layers: "analysis_layers + analysis_metrics",
      total_score: "analysis_outputs.total_score",
      scorer_metadata: "analysis_outputs.scorer_metadata_json"
    }),
    notes: "Richer scored schema with scorer metadata."
  });
}

export function tableCounts(db) {
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

