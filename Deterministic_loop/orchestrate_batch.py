#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
LOOP_ROOT = Path(__file__).resolve().parent
DEFAULT_COMPANIES_PATH = LOOP_ROOT / "companies.example.json"
DEFAULT_USER_COMPANIES_PATH = LOOP_ROOT / "companies.json"
DEFAULT_TEMPLATE_PATH = LOOP_ROOT / "research_prompt_template.md"
DEFAULT_BATCH_ROOT = LOOP_ROOT / "batches"
SCORER_PATH = Path(".codex/skills/technology-innovation-analysis/score_innovation_benchmark.py")
REQUIRED_SCORED_FIELDS = {
    "total_score",
    "display_total_score",
    "gate_pass",
    "verdict",
    "layers",
    "scorer_metadata",
}
REQUIRED_LAYER_LABELS = {
    "Science",
    "IP",
    "Industrialization",
    "Adoption",
    "Policy & Economics",
}


def repo_relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "company"


def clean_id(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9._-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "run"


def load_company_manifest(path: Path) -> dict[str, Any]:
    manifest = read_json(path)
    if isinstance(manifest, list):
        manifest = {"companies": manifest}
    if not isinstance(manifest, dict):
        raise ValueError("Company manifest must be a JSON object or a JSON list.")
    companies = manifest.get("companies")
    if not isinstance(companies, list) or not companies:
        raise ValueError("Company manifest must contain a non-empty 'companies' list.")
    return manifest


def normalize_company(item: dict[str, Any], index: int) -> dict[str, str]:
    if not isinstance(item, dict):
        raise ValueError(f"Company entry {index} must be an object.")
    company = str(item.get("company", "")).strip()
    ticker = str(item.get("ticker", "")).strip()
    if not company or not ticker:
        raise ValueError(f"Company entry {index} must define company and ticker.")
    slug = clean_id(str(item.get("slug") or slugify(company)))
    return {
        "company": company,
        "ticker": ticker,
        "slug": slug,
        "cik": str(item.get("cik", "")).strip(),
        "isin": str(item.get("isin", "")).strip(),
    }


def render_template(template: str, values: dict[str, str]) -> str:
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace("{{" + key + "}}", value)
    return rendered


def default_batch_id() -> str:
    return "batch-" + datetime.now().strftime("%Y%m%d-%H%M%S")


def scorer_command(payload_path: str, scored_path: str) -> list[str]:
    return ["python3", str(SCORER_PATH), payload_path, "-o", scored_path]


def default_companies_path() -> Path:
    if DEFAULT_USER_COMPANIES_PATH.exists():
        return DEFAULT_USER_COMPANIES_PATH
    return DEFAULT_COMPANIES_PATH


def prepare_batch(
    companies_path: Path,
    template_path: Path,
    batch_root: Path,
    batch_id_arg: str | None,
    research_date_arg: str | None,
    force: bool,
    dry_run: bool,
    write_research_prompts: bool,
) -> tuple[dict[str, Any], Path, dict[str, str]]:
    manifest = load_company_manifest(companies_path)
    template = template_path.read_text(encoding="utf-8")

    research_date = research_date_arg or date.today().isoformat()
    batch_id = clean_id(batch_id_arg or default_batch_id())
    batch_dir = batch_root / batch_id

    if batch_dir.exists() and not force and not dry_run:
        raise FileExistsError(f"{batch_dir} already exists. Use --force to add or refresh batch files.")

    raw_companies = manifest["companies"]
    companies: list[dict[str, Any]] = []
    prompts: dict[str, str] = {}
    seen_run_dirs: set[str] = set()

    for index, raw_item in enumerate(raw_companies, start=1):
        company = normalize_company(raw_item, index)
        run_id = clean_id(raw_item.get("run_id") or f"run-{batch_id}-{index:02d}")
        run_dir = REPO_ROOT / "public" / "runs" / company["slug"] / research_date / run_id
        run_dir_key = repo_relative(run_dir)
        if run_dir_key in seen_run_dirs:
            raise ValueError(f"Duplicate run directory in manifest: {run_dir_key}")
        seen_run_dirs.add(run_dir_key)
        if run_dir.exists() and any(run_dir.iterdir()) and not force and not dry_run:
            raise FileExistsError(f"{run_dir_key} already exists and is not empty. Use --force to reuse it.")

        payload_path = run_dir / "payload.json"
        scored_path = run_dir / "scored.json"
        dashboard_path = run_dir / "dashboard.html"
        prompt_path = batch_dir / "research_prompts" / f"{index:02d}-{company['slug']}.md"
        if not dry_run:
            run_dir.mkdir(parents=True, exist_ok=True)

        paths = {
            "artifact_dir": repo_relative(run_dir),
            "payload_path": repo_relative(payload_path),
            "scored_path": repo_relative(scored_path),
            "dashboard_path": repo_relative(dashboard_path),
        }
        values = {
            "batch_id": batch_id,
            "company": company["company"],
            "ticker": company["ticker"],
            "company_slug": company["slug"],
            "research_date": research_date,
            "run_id": run_id,
            **paths,
        }
        rendered_prompt = render_template(template, values)
        prompts[company["slug"]] = rendered_prompt
        if write_research_prompts and not dry_run:
            write_text(prompt_path, rendered_prompt)

        entry = {
            "sequence": index,
            "company": company["company"],
            "ticker": company["ticker"],
            "slug": company["slug"],
            "cik": company["cik"],
            "isin": company["isin"],
            "research_date": research_date,
            "run_id": run_id,
            "artifact_dir": paths["artifact_dir"],
            "payload_path": paths["payload_path"],
            "scored_path": paths["scored_path"],
            "dashboard_path": paths["dashboard_path"],
            "scorer_command": " ".join(scorer_command(paths["payload_path"], paths["scored_path"])),
        }
        if write_research_prompts:
            entry["prompt_path"] = repo_relative(prompt_path)
        companies.append(entry)

    plan = {
        "schema_version": "1.0",
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "batch_id": batch_id,
        "batch_name": manifest.get("batch_name", batch_id),
        "research_date": research_date,
        "theme": manifest.get("theme", "Desert Rose"),
        "research_analysis_policy": (
            "The deterministic loop only handles batch orchestration. "
            "Company research, evidence extraction, payload creation, and dashboard design "
            "remain the existing single-company analysis workflow."
        ),
        "companies": companies,
    }
    return plan, batch_dir, prompts


def init_batch(args: argparse.Namespace) -> int:
    plan, batch_dir, _prompts = prepare_batch(
        companies_path=Path(args.companies),
        template_path=Path(args.template),
        batch_root=Path(args.batch_root),
        batch_id_arg=args.batch_id,
        research_date_arg=args.research_date,
        force=args.force,
        dry_run=args.dry_run,
        write_research_prompts=True,
    )
    if args.dry_run:
        print(json.dumps(plan, indent=2, ensure_ascii=True))
        return 0

    write_json(batch_dir / "batch_plan.json", plan)
    print(f"Created batch: {repo_relative(batch_dir)}")
    print(f"Companies: {len(companies)}")
    print("Next: run the generated prompts, then use the score, validate, and summary commands.")
    return 0


def load_plan(batch_dir: Path) -> dict[str, Any]:
    plan_path = batch_dir / "batch_plan.json"
    if not plan_path.exists():
        raise FileNotFoundError(f"Missing batch plan: {plan_path}")
    return read_json(plan_path)


def filter_entries(plan: dict[str, Any], slug: str | None) -> list[dict[str, Any]]:
    entries = plan.get("companies", [])
    if slug:
        entries = [entry for entry in entries if entry.get("slug") == slug]
        if not entries:
            raise ValueError(f"No company with slug '{slug}' in batch plan.")
    return entries


def validate_scored(path: Path) -> tuple[list[str], list[str], dict[str, Any] | None]:
    if not path.exists():
        return ["missing scored.json"], [], None
    try:
        scored = read_json(path)
    except Exception as exc:
        return [f"cannot parse scored.json: {exc}"], [], None

    errors: list[str] = []
    warnings: list[str] = []
    missing = sorted(REQUIRED_SCORED_FIELDS - set(scored))
    if missing:
        errors.append("missing scored fields: " + ", ".join(missing))
    if "absolute_score" in scored:
        errors.append("scored.json must not contain nested absolute_score")

    layers = scored.get("layers")
    if not isinstance(layers, list):
        errors.append("layers must be a list")
    else:
        labels = {layer.get("label") for layer in layers if isinstance(layer, dict)}
        missing_layers = sorted(REQUIRED_LAYER_LABELS - labels)
        if missing_layers:
            errors.append("missing layers: " + ", ".join(missing_layers))

    if scored.get("mode") not in (None, "absolute"):
        warnings.append("mode is not 'absolute'; confirm this was intentional")
    return errors, warnings, scored


def dashboard_warnings(path: Path) -> list[str]:
    if not path.exists():
        return ["missing dashboard.html"]
    text = path.read_text(encoding="utf-8", errors="replace")
    warnings: list[str] = []
    if 'id="scored-data"' not in text and "scored.json" not in text:
        warnings.append("dashboard does not visibly embed or reference scorer-produced data")
    if "large rounded corners on Vertical bars" in text:
        warnings.append("dashboard appears to include prompt text instead of UI content")
    return warnings


def status_rows(plan: dict[str, Any], slug: str | None = None) -> list[dict[str, Any]]:
    rows = []
    for entry in filter_entries(plan, slug):
        payload_path = REPO_ROOT / entry["payload_path"]
        scored_path = REPO_ROOT / entry["scored_path"]
        dashboard_path = REPO_ROOT / entry["dashboard_path"]
        scored_errors, scored_warnings, scored = validate_scored(scored_path)
        rows.append(
            {
                "company": entry["company"],
                "slug": entry["slug"],
                "payload": payload_path.exists(),
                "scored": scored_path.exists() and not scored_errors,
                "dashboard": dashboard_path.exists(),
                "score": None if not scored else scored.get("display_total_score"),
                "verdict": None if not scored else scored.get("verdict"),
                "gate_pass": None if not scored else scored.get("gate_pass"),
                "errors": scored_errors,
                "warnings": scored_warnings + ([] if not dashboard_path.exists() else dashboard_warnings(dashboard_path)),
            }
        )
    return rows


def cmd_status(args: argparse.Namespace) -> int:
    plan = load_plan(Path(args.batch_dir))
    rows = status_rows(plan, args.company_slug)
    for row in rows:
        print(
            f"{row['slug']}: payload={row['payload']} scored={row['scored']} "
            f"dashboard={row['dashboard']} score={row['score']} gate={row['gate_pass']}"
        )
        for error in row["errors"]:
            print(f"  ERROR: {error}")
        for warning in row["warnings"]:
            print(f"  WARN: {warning}")
    return 0


def cmd_score(args: argparse.Namespace) -> int:
    plan = load_plan(Path(args.batch_dir))
    failures = 0
    for entry in filter_entries(plan, args.company_slug):
        payload_path = REPO_ROOT / entry["payload_path"]
        scored_path = REPO_ROOT / entry["scored_path"]
        if not payload_path.exists():
            message = f"{entry['slug']}: missing payload.json"
            if args.skip_missing:
                print(f"SKIP: {message}")
                continue
            print(f"ERROR: {message}")
            failures += 1
            continue
        scored_path.parent.mkdir(parents=True, exist_ok=True)
        command = scorer_command(entry["payload_path"], entry["scored_path"])
        print("RUN: " + " ".join(command))
        result = subprocess.run(command, cwd=REPO_ROOT)
        if result.returncode != 0:
            failures += 1
    return 1 if failures else 0


def cmd_validate(args: argparse.Namespace) -> int:
    plan = load_plan(Path(args.batch_dir))
    failures = 0
    for entry in filter_entries(plan, args.company_slug):
        scored_path = REPO_ROOT / entry["scored_path"]
        dashboard_path = REPO_ROOT / entry["dashboard_path"]
        errors, warnings, _scored = validate_scored(scored_path)
        if args.require_dashboard and not dashboard_path.exists():
            errors.append("missing dashboard.html")
        if dashboard_path.exists():
            warnings.extend(dashboard_warnings(dashboard_path))
        if errors:
            failures += 1
            print(f"FAIL: {entry['slug']}")
            for error in errors:
                print(f"  ERROR: {error}")
        else:
            print(f"OK: {entry['slug']}")
        for warning in warnings:
            print(f"  WARN: {warning}")
    return 1 if failures else 0


def first_focus_technology(scored: dict[str, Any]) -> str:
    context = scored.get("research_context") or {}
    technologies = context.get("focus_technologies")
    if isinstance(technologies, list) and technologies:
        return str(technologies[0])
    content = scored.get("dashboard_content") or {}
    tech_map = content.get("technology_map") or {}
    items = tech_map.get("items")
    if isinstance(items, list) and items:
        return str(items[0].get("name") or "Unavailable")
    return "Unavailable"


def main_red_flag(scored: dict[str, Any]) -> str:
    content = scored.get("dashboard_content") or {}
    flags = content.get("red_flags")
    if isinstance(flags, list) and flags:
        first = flags[0]
        title = str(first.get("title") or "").strip()
        text = str(first.get("text") or "").strip()
        if title and text:
            return f"{title}: {text}"
        return title or text or "Unavailable"
    return "Unavailable"


def cmd_summary(args: argparse.Namespace) -> int:
    batch_dir = Path(args.batch_dir)
    plan = load_plan(batch_dir)
    records: list[dict[str, Any]] = []
    lines = [
        f"# Batch Summary: {plan.get('batch_name', plan.get('batch_id'))}",
        "",
        f"- batch_id: {plan.get('batch_id')}",
        f"- research_date: {plan.get('research_date')}",
        f"- theme: {plan.get('theme')}",
        "",
        "| Company | Score | Gate | Verdict | Top innovation domain | Dashboard | Main red flag |",
        "| --- | ---: | --- | --- | --- | --- | --- |",
    ]

    for entry in filter_entries(plan, args.company_slug):
        scored_path = REPO_ROOT / entry["scored_path"]
        dashboard_path = entry["dashboard_path"]
        errors, _warnings, scored = validate_scored(scored_path)
        if errors or scored is None:
            score = "Missing"
            gate = "Missing"
            verdict = "; ".join(errors)
            focus = "Unavailable"
            red_flag = "Unavailable"
        else:
            score = str(scored.get("display_total_score", "Unavailable"))
            gate = "Pass" if scored.get("gate_pass") else "Fail"
            verdict = str(scored.get("verdict", "Unavailable"))
            focus = first_focus_technology(scored)
            red_flag = main_red_flag(scored)
        dashboard_link = dashboard_path if (REPO_ROOT / dashboard_path).exists() else "Missing"
        lines.append(
            f"| {entry['company']} | {score} | {gate} | {verdict} | "
            f"{focus} | {dashboard_link} | {red_flag} |"
        )
        records.append(
            {
                "company": entry["company"],
                "slug": entry["slug"],
                "score": score,
                "gate": gate,
                "verdict": verdict,
                "top_innovation_domain": focus,
                "dashboard_path": dashboard_link,
                "main_red_flag": red_flag,
            }
        )

    summary_md = batch_dir / "batch_summary.md"
    summary_json = batch_dir / "batch_summary.json"
    write_text(summary_md, "\n".join(lines) + "\n")
    write_json(summary_json, {"batch_id": plan.get("batch_id"), "companies": records})
    print(f"Wrote {repo_relative(summary_md)}")
    print(f"Wrote {repo_relative(summary_json)}")
    return 0


def build_codex_exec_command(args: argparse.Namespace) -> list[str]:
    codex_bin = args.codex_bin
    if shutil.which(codex_bin) is None:
        raise FileNotFoundError(f"Cannot find Codex CLI binary: {codex_bin}")

    command = [codex_bin]
    if args.search:
        command.append("--search")
    if args.model:
        command.extend(["-m", args.model])
    if args.unsafe_bypass:
        command.append("--dangerously-bypass-approvals-and-sandbox")
    else:
        command.extend(["-s", args.sandbox, "-a", "never"])
    command.extend(["-C", str(REPO_ROOT), "exec"])
    command.append("-")
    return command


def run_codex_research(
    entry: dict[str, Any],
    prompt: str,
    command: list[str],
    batch_dir: Path,
) -> dict[str, Any]:
    logs_dir = batch_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = logs_dir / f"{entry['sequence']:02d}-{entry['slug']}.log"
    started_at = datetime.now().astimezone().isoformat(timespec="seconds")
    result = subprocess.run(
        command,
        input=prompt,
        text=True,
        capture_output=True,
        cwd=REPO_ROOT,
    )
    ended_at = datetime.now().astimezone().isoformat(timespec="seconds")
    log_text = "\n".join(
        [
            f"company: {entry['company']}",
            f"ticker: {entry['ticker']}",
            f"started_at: {started_at}",
            f"ended_at: {ended_at}",
            f"returncode: {result.returncode}",
            "",
            "command:",
            " ".join(command),
            "",
            "stdout:",
            result.stdout,
            "",
            "stderr:",
            result.stderr,
        ]
    )
    write_text(log_path, log_text)
    return {
        "company": entry["company"],
        "slug": entry["slug"],
        "returncode": result.returncode,
        "log_path": repo_relative(log_path),
    }


def write_research_results(batch_dir: Path, results: list[dict[str, Any]]) -> None:
    write_json(
        batch_dir / "research_results.json",
        {
            "written_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "results": results,
        },
    )


def cmd_run(args: argparse.Namespace) -> int:
    companies_path = Path(args.companies) if args.companies else default_companies_path()
    plan, batch_dir, prompts = prepare_batch(
        companies_path=companies_path,
        template_path=Path(args.template),
        batch_root=Path(args.batch_root),
        batch_id_arg=args.batch_id,
        research_date_arg=args.research_date,
        force=args.force,
        dry_run=args.dry_run,
        write_research_prompts=False,
    )
    if args.dry_run:
        print(json.dumps(plan, indent=2, ensure_ascii=True))
        return 0

    write_json(batch_dir / "batch_plan.json", plan)
    codex_command = build_codex_exec_command(args)
    entries = plan["companies"]
    max_workers = max(1, min(args.parallel, len(entries)))
    print(f"Created batch: {repo_relative(batch_dir)}")
    print(f"Running research for {len(entries)} companies with parallel={max_workers}")

    results: list[dict[str, Any]] = []
    if max_workers == 1:
        for entry in entries:
            print(f"RESEARCH: {entry['slug']}")
            result = run_codex_research(entry, prompts[entry["slug"]], codex_command, batch_dir)
            print(f"  returncode={result['returncode']} log={result['log_path']}")
            results.append(result)
    else:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(run_codex_research, entry, prompts[entry["slug"]], codex_command, batch_dir): entry
                for entry in entries
            }
            for future in as_completed(futures):
                result = future.result()
                print(f"RESEARCH: {result['slug']} returncode={result['returncode']} log={result['log_path']}")
                results.append(result)

    results.sort(key=lambda item: next(entry["sequence"] for entry in entries if entry["slug"] == item["slug"]))
    write_research_results(batch_dir, results)
    research_failed = any(result["returncode"] != 0 for result in results)

    print("Scoring completed payloads")
    score_status = cmd_score(
        argparse.Namespace(batch_dir=str(batch_dir), company_slug=None, skip_missing=True)
    )
    print("Validating completed dashboards")
    validate_status = cmd_validate(
        argparse.Namespace(batch_dir=str(batch_dir), company_slug=None, require_dashboard=True)
    )
    print("Writing batch summary")
    summary_status = cmd_summary(argparse.Namespace(batch_dir=str(batch_dir), company_slug=None))

    print(f"Batch summary: {repo_relative(batch_dir / 'batch_summary.md')}")
    return 1 if research_failed or score_status or validate_status or summary_status else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Deterministic orchestration loop for company analysis batches.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="Create run folders and per-company research prompts.")
    init.add_argument("--companies", default=str(DEFAULT_COMPANIES_PATH), help="Path to company manifest JSON.")
    init.add_argument("--template", default=str(DEFAULT_TEMPLATE_PATH), help="Path to prompt template.")
    init.add_argument("--batch-root", default=str(DEFAULT_BATCH_ROOT), help="Folder for batch plans and prompts.")
    init.add_argument("--batch-id", help="Filesystem-safe batch id. Defaults to a timestamp.")
    init.add_argument("--research-date", help="ISO research date YYYY-MM-DD. Defaults to today's local date.")
    init.add_argument("--force", action="store_true", help="Allow refreshing existing batch files and empty run dirs.")
    init.add_argument("--dry-run", action="store_true", help="Print the batch plan without creating files.")
    init.set_defaults(func=init_batch)

    status = subparsers.add_parser("status", help="Show payload/scored/dashboard status for a batch.")
    status.add_argument("--batch-dir", required=True, help="Path to Deterministic_loop/batches/<batch_id>.")
    status.add_argument("--company-slug", help="Limit to one company slug.")
    status.set_defaults(func=cmd_status)

    score = subparsers.add_parser("score", help="Run the deterministic scorer for completed payloads.")
    score.add_argument("--batch-dir", required=True, help="Path to Deterministic_loop/batches/<batch_id>.")
    score.add_argument("--company-slug", help="Limit to one company slug.")
    score.add_argument("--skip-missing", action="store_true", help="Skip companies without payload.json.")
    score.set_defaults(func=cmd_score)

    validate = subparsers.add_parser("validate", help="Validate scorer output and optional dashboards.")
    validate.add_argument("--batch-dir", required=True, help="Path to Deterministic_loop/batches/<batch_id>.")
    validate.add_argument("--company-slug", help="Limit to one company slug.")
    validate.add_argument("--require-dashboard", action="store_true", help="Fail when dashboard.html is absent.")
    validate.set_defaults(func=cmd_validate)

    summary = subparsers.add_parser("summary", help="Create batch_summary.md and batch_summary.json.")
    summary.add_argument("--batch-dir", required=True, help="Path to Deterministic_loop/batches/<batch_id>.")
    summary.add_argument("--company-slug", help="Limit to one company slug.")
    summary.set_defaults(func=cmd_summary)

    run = subparsers.add_parser("run", help="Run the complete batch with Codex exec, scoring, validation, and summary.")
    run.add_argument("--companies", help="Path to company manifest JSON. Defaults to companies.json, then example.")
    run.add_argument("--template", default=str(DEFAULT_TEMPLATE_PATH), help="Path to prompt template.")
    run.add_argument("--batch-root", default=str(DEFAULT_BATCH_ROOT), help="Folder for batch plans and logs.")
    run.add_argument("--batch-id", help="Filesystem-safe batch id. Defaults to a timestamp.")
    run.add_argument("--research-date", help="ISO research date YYYY-MM-DD. Defaults to today's local date.")
    run.add_argument("--force", action="store_true", help="Allow reusing existing batch files and run dirs.")
    run.add_argument("--dry-run", action="store_true", help="Print the batch plan without running research.")
    run.add_argument("--parallel", type=int, default=1, help="Number of Codex research jobs to run at once.")
    run.add_argument("--codex-bin", default="codex", help="Codex CLI executable.")
    run.add_argument("--model", help="Optional Codex model override.")
    run.add_argument("--sandbox", default="workspace-write", choices=["read-only", "workspace-write", "danger-full-access"])
    run.add_argument("--search", action=argparse.BooleanOptionalAction, default=True, help="Enable Codex web search.")
    run.add_argument(
        "--unsafe-bypass",
        action="store_true",
        help="Use Codex --dangerously-bypass-approvals-and-sandbox for fully unattended local execution.",
    )
    run.set_defaults(func=cmd_run)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
