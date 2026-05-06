#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { initDatabase, openDatabase } from "./db.js";
import { exportRunRaw, ingestDirectory, runSummary, writeJsonFile } from "./ingest.js";
import { getStatus, listRuns } from "./queries.js";
import { DEFAULT_DB, prettyJson, resolveDbPath } from "./utils.js";

function parseArgs(argv) {
  const args = { _: [] };
  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];
    if (value.startsWith("--")) {
      const key = value.slice(2).replace(/-([a-z])/gu, (_, char) => char.toUpperCase());
      const next = argv[index + 1];
      if (!next || next.startsWith("--")) {
        args[key] = true;
      } else {
        args[key] = next;
        index += 1;
      }
    } else {
      args._.push(value);
    }
  }
  return args;
}

function usage() {
  return `Usage:
  node src/cli.js init [--db PATH]
  node src/cli.js ingest --source-dir PATH [--db PATH]
  node src/cli.js start [--ingest --source-dir PATH] [--db PATH]
  node src/cli.js end [--db PATH]
  node src/cli.js status [--db PATH]
  node src/cli.js runs [--db PATH]
  node src/cli.js show-run RUN_UID [--db PATH]
  node src/cli.js export-run RUN_UID --out FILE [--db PATH]

Default DB: ${DEFAULT_DB}`;
}

function printRuns(rows) {
  if (!rows.length) {
    console.log("No analysis runs found.");
    return;
  }
  rows.forEach((row) => {
    const gate = row.gate_pass ? "pass" : "fail";
    console.log(`${row.run_uid} | ${row.company} | ${row.ticker || "no ticker"} | ${row.research_date || "no date"} | score=${row.display_total_score || "n/a"} | gate=${gate} | sources=${row.source_count} evidence=${row.evidence_count} metrics=${row.metric_count}`);
    if (row.verdict) console.log(`  verdict: ${row.verdict}`);
  });
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const command = args._[0];
  const dbPath = resolveDbPath(args.db);
  let db;

  try {
    if (!command || command === "help" || command === "--help") {
      console.log(usage());
      return 0;
    }

    if (command === "init") {
      db = initDatabase(dbPath);
      console.log(`Initialized SQLite database: ${dbPath}`);
      return 0;
    }

    if (command === "start") {
      db = initDatabase(dbPath);
      console.log(`Storage system ready: ${dbPath}`);
      if (args.ingest) {
        const sourceDir = path.resolve(args.sourceDir || "..");
        const imported = ingestDirectory(db, sourceDir);
        console.log(`Imported ${imported.length} analysis run(s) into ${dbPath}:`);
        imported.forEach((runUid) => console.log(`  - ${runUid}`));
      } else {
        console.log("No daemon is running for CLI mode. Use `npm run api` to start the frontend-ready HTTP API server.");
      }
      return 0;
    }

    if (command === "ingest") {
      db = initDatabase(dbPath);
      const sourceDir = path.resolve(args.sourceDir || "..");
      const imported = ingestDirectory(db, sourceDir);
      console.log(`Imported ${imported.length} analysis run(s) into ${dbPath}:`);
      imported.forEach((runUid) => console.log(`  - ${runUid}`));
      return 0;
    }

    if (command === "end") {
      console.log("CLI mode has no background process. SQLite connections close when each command exits.");
      console.log("If the API server is running, stop it with Ctrl+C in the terminal where `npm run api` is active.");
      console.log(`Database remains on disk at: ${dbPath}`);
      return 0;
    }

    if (!fs.existsSync(dbPath) && !["status", "runs", "show-run", "export-run"].includes(command)) {
      throw new Error(`Database not found: ${dbPath}`);
    }
    db = initDatabase(dbPath);

    if (command === "status") {
      const counts = getStatus(db);
      Object.entries(counts).forEach(([table, count]) => console.log(`${table}: ${count}`));
      return 0;
    }

    if (command === "runs") {
      printRuns(listRuns(db));
      return 0;
    }

    if (command === "show-run") {
      const runRef = args._[1];
      if (!runRef) throw new Error("Missing RUN_UID.");
      console.log(prettyJson(runSummary(db, runRef)));
      return 0;
    }

    if (command === "export-run") {
      const runRef = args._[1];
      if (!runRef) throw new Error("Missing RUN_UID.");
      const output = exportRunRaw(db, runRef);
      if (args.out) {
        writeJsonFile(path.resolve(args.out), output);
        console.log(`Exported run to ${path.resolve(args.out)}`);
      } else {
        console.log(prettyJson(output));
      }
      return 0;
    }

    throw new Error(`Unknown command: ${command}\n\n${usage()}`);
  } finally {
    if (db) db.close();
  }
}

try {
  process.exitCode = main();
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}

