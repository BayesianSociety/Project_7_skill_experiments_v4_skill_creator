# Deterministic Loop Instructions

This folder provides a one-command batch runner for company innovation analyses. The runner handles orchestration only: it creates one run folder per company, launches the existing single-company research workflow through `codex exec`, runs the deterministic scorer, validates the outputs, and writes a batch summary.

The research analysis itself is unchanged. Each company is still analyzed as a normal `technology-innovation-analysis` task and rendered with `frontend-skill` using the Desert Rose theme from `theme-factory`.

## One Command

From the repo root:

```bash
python3 Deterministic_loop/orchestrate_batch.py run
```

By default, this uses `Deterministic_loop/companies.json` if it exists. If it does not exist, it falls back to `Deterministic_loop/companies.example.json`.

For a fixed date and batch id:

```bash
python3 Deterministic_loop/orchestrate_batch.py run --research-date 2026-05-12 --batch-id commerce-platforms-20260512
```

For limited parallelism:

```bash
python3 Deterministic_loop/orchestrate_batch.py run --research-date 2026-05-12 --batch-id commerce-platforms-20260512 --parallel 2
```

## Company List

Edit or create `Deterministic_loop/companies.json`:

```json
{
  "batch_name": "commerce-platform-innovation",
  "theme": "Desert Rose",
  "companies": [
    {
      "company": "Shopify Inc",
      "ticker": "NASDAQ: SHOP",
      "slug": "shopify-inc"
    }
  ]
}
```

Each company needs at least `company`, `ticker`, and `slug`.

## What The Command Does

The `run` command performs the full sequence:

1. Creates `Deterministic_loop/batches/{batch_id}/batch_plan.json`.
2. Creates one artifact folder per company under `public/runs/`.
3. Renders each company prompt in memory.
4. Runs `codex exec` for each company.
5. Saves Codex logs under `Deterministic_loop/batches/{batch_id}/logs/`.
6. Runs the deterministic scorer for completed payloads.
7. Validates `scored.json` and `dashboard.html`.
8. Writes `batch_summary.md` and `batch_summary.json`.

It does not create separate `research_prompts/` files when using `run`.

## Outputs

Per company:

```text
public/runs/{company_slug}/{research_date}/{run_id}/payload.json
public/runs/{company_slug}/{research_date}/{run_id}/scored.json
public/runs/{company_slug}/{research_date}/{run_id}/dashboard.html
```

Batch summary:

```text
Deterministic_loop/batches/{batch_id}/batch_summary.md
Deterministic_loop/batches/{batch_id}/batch_summary.json
```

Execution logs:

```text
Deterministic_loop/batches/{batch_id}/logs/
```

## Useful Checks

Preview without running research:

```bash
python3 Deterministic_loop/orchestrate_batch.py run --dry-run
```

Check a completed or running batch:

```bash
python3 Deterministic_loop/orchestrate_batch.py status --batch-dir Deterministic_loop/batches/{batch_id}
```

Regenerate a summary:

```bash
python3 Deterministic_loop/orchestrate_batch.py summary --batch-dir Deterministic_loop/batches/{batch_id}
```

## Notes

- Keep one company per `payload.json`.
- Do not hand-edit `scored.json`; rerun the scorer after fixing `payload.json`.
- Use `--parallel 1` for the most predictable run. Increase `--parallel` only when you are comfortable with multiple Codex jobs writing separate run folders at the same time.
- `--unsafe-bypass` passes Codex's `--dangerously-bypass-approvals-and-sandbox` flag. Use it only when you intentionally want a fully unattended run with no sandbox prompts.
