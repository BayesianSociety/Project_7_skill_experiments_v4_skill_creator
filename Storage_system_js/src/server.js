#!/usr/bin/env node
import express from "express";
import { initDatabase } from "./db.js";
import {
  createContentArtifact,
  getCompanies,
  getEvidenceForRun,
  getMetricEvidence,
  getRunByUid,
  getSchemaObservations,
  getStatus,
  listRuns
} from "./queries.js";
import { DEFAULT_DB, resolveDbPath } from "./utils.js";

const dbPathArgIndex = process.argv.indexOf("--db");
const portArgIndex = process.argv.indexOf("--port");
const dbPath = resolveDbPath(dbPathArgIndex >= 0 ? process.argv[dbPathArgIndex + 1] : DEFAULT_DB);
const port = Number(portArgIndex >= 0 ? process.argv[portArgIndex + 1] : process.env.PORT || 4177);
const db = initDatabase(dbPath);
const app = express();

app.use(express.json({ limit: "5mb" }));
app.use((req, res, next) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET,POST,OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") {
    res.status(204).end();
    return;
  }
  next();
});

function route(handler) {
  return (req, res) => {
    try {
      const result = handler(req, res);
      if (!res.headersSent) res.json(result);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  };
}

app.get("/api/health", route(() => ({ ok: true, db_path: dbPath })));
app.get("/api/status", route(() => getStatus(db)));
app.get("/api/runs", route(() => listRuns(db)));
app.get("/api/companies", route(() => getCompanies(db)));
app.get("/api/schema-observations", route(() => getSchemaObservations(db)));
app.get("/api/metric-evidence", route((req) => getMetricEvidence(db, req.query.run_uid)));

app.get("/api/runs/:runUid", route((req, res) => {
  const run = getRunByUid(db, req.params.runUid);
  if (!run) {
    res.status(404).json({ error: "Run not found" });
    return null;
  }
  return run;
}));

app.get("/api/runs/:runUid/evidence", route((req, res) => {
  const evidence = getEvidenceForRun(db, req.params.runUid);
  if (!evidence) {
    res.status(404).json({ error: "Run not found" });
    return null;
  }
  return evidence;
}));

app.post("/api/content-artifacts", route((req, res) => {
  if (!req.body?.artifact_type) {
    res.status(400).json({ error: "artifact_type is required" });
    return null;
  }
  res.status(201);
  return createContentArtifact(db, req.body);
}));

const server = app.listen(port, "127.0.0.1", () => {
  console.log(`Storage System JS API listening on http://127.0.0.1:${port}`);
  console.log(`Database: ${dbPath}`);
});

function shutdown() {
  server.close(() => {
    db.close();
    console.log("Storage System JS API stopped.");
    process.exit(0);
  });
}

process.on("SIGINT", shutdown);
process.on("SIGTERM", shutdown);

