import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
export const DEFAULT_DB = path.join(ROOT, "storage_js.db");
export const SCHEMA_FILE = path.join(ROOT, "schema.sql");
export const IMPORTER_NAME = "storage-system-js";
export const IMPORTER_VERSION = "1.0.0";

export function slugify(value) {
  return String(value || "unknown")
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "_")
    .replace(/_+/g, "_")
    .replace(/^_+|_+$/g, "") || "unknown";
}

function sortDeep(value) {
  if (Array.isArray(value)) return value.map(sortDeep);
  if (value && typeof value === "object") {
    return Object.keys(value)
      .sort()
      .reduce((acc, key) => {
        acc[key] = sortDeep(value[key]);
        return acc;
      }, {});
  }
  return value;
}

export function stableJson(value) {
  return JSON.stringify(sortDeep(value));
}

export function prettyJson(value) {
  return JSON.stringify(sortDeep(value), null, 2);
}

export function sha256Text(value) {
  return crypto.createHash("sha256").update(String(value), "utf8").digest("hex");
}

export function asBoolInt(value) {
  if (value === undefined || value === null) return null;
  return value ? 1 : 0;
}

export function readJson(filePath) {
  const raw = fs.readFileSync(filePath, "utf8");
  const parsed = JSON.parse(raw);
  if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
    throw new Error(`${filePath} does not contain a JSON object`);
  }
  return parsed;
}

export function parseTicker(ticker) {
  if (!ticker) return { exchange: "", value: "" };
  const text = String(ticker);
  if (text.includes(":")) {
    const [exchange, ...rest] = text.split(":");
    return { exchange: exchange.trim(), value: rest.join(":").trim() };
  }
  return { exchange: "", value: text.trim() };
}

export function resolveDbPath(value) {
  return path.resolve(value || DEFAULT_DB);
}

export function sourceDedupeKey(source) {
  const url = String(source?.url || "").trim();
  if (url) return `url:${url.toLowerCase()}`;
  return [
    "source",
    source?.title || "",
    source?.publisher || "",
    source?.document_date || "",
    source?.source_type || ""
  ].map((part) => String(part).trim().toLowerCase()).join("|");
}

export function removePayloadSuffix(filename) {
  return filename.replace(/_payload\.json$/u, "");
}

