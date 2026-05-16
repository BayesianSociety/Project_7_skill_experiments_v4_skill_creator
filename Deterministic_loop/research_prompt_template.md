Use $technology-innovation-analysis skill to research {{company}}, {{ticker}} and then present the output results using a dashboard created with the $frontend-skill, using the Desert Rose theme from the $theme-factory.

Batch orchestration context:
- batch_id: {{batch_id}}
- company_slug: {{company_slug}}
- research_date: {{research_date}}
- run_id: {{run_id}}
- artifact_dir: {{artifact_dir}}

Use this exact run-scoped artifact set for this company:
- {{payload_path}}
- {{scored_path}}
- {{dashboard_path}}
- {{artifact_dir}}/story.md

Keep this as a single-company analysis. Do not combine this company with other companies in the batch. Do not invent peer percentiles or relative rankings unless a separate real peer benchmark is explicitly requested.

For this company:
- identify the 1 to 3 most material innovation domains,
- gather 5-year evidence from filings, company materials, patents, publications, universities, policy sources, and reputable industry sources,
- build the required structured payload,
- run the deterministic scorer to create scored.json,
- create the dashboard from scored.json, not from hard-coded company-specific text,
- create the dashboard story from Story_prompt.txt after a base dashboard.html exists,
- validate that scored.json contains total_score, display_total_score, gate_pass, verdict, layers, and scorer_metadata,
- ensure the five-layer dashboard is stacked vertically with horizontal progress bars.

The approved scorer command for this company is:

```bash
python3 .codex/skills/technology-innovation-analysis/score_innovation_benchmark.py {{payload_path}} -o {{scored_path}}
```

The dashboard.html must be self-contained. Embed the full scorer-produced scored.json in a <script id="scored-data" type="application/json">...</script> block and render from that embedded JSON. Do not use fetch("scored.json"), XMLHttpRequest, or any runtime load of local JSON files.

Story workflow:
- Do not edit Story_prompt.txt.
- First create a base dashboard.html from scorer-produced scored.json, before a story section is present.
- Then read Story_prompt.txt unchanged and apply it to the base dashboard.html. The original prompt outcome must be written to {{artifact_dir}}/story.md.
- Also generate three audience-level variants from the same base dashboard content:
  - basic: for a reader who needs simple, almost basic explanation,
  - informed: for a reader who already knows something about the technology,
  - expert: for a reader who is already expert in the technology.
- Insert the original story and all three variants into {{payload_path}} at dashboard_content.story. Preserve the original story. Use this shape:
  - original.label: "Original",
  - original.title: short title for the original story section,
  - original.body_markdown: exact story.md content,
  - original.paragraphs: the original story split into paragraphs for safe dashboard rendering,
  - variants.basic.label: "Basic",
  - variants.basic.title/body_markdown/paragraphs,
  - variants.informed.label: "Informed",
  - variants.informed.title/body_markdown/paragraphs,
  - variants.expert.label: "Expert",
  - variants.expert.title/body_markdown/paragraphs,
  - default_variant: "original",
  - source_dashboard_file: "{{dashboard_path}}",
  - source_dashboard_hash: sha256 of the base dashboard.html used to generate the story,
  - prompt_file: "Story_prompt.txt",
  - prompt_hash: sha256 of Story_prompt.txt,
  - generated_at: ISO timestamp,
  - external_sources_used: [] unless Story_prompt.txt allowed and you used official or Wikipedia company sources.
- Rerun the deterministic scorer so {{scored_path}} contains dashboard_content.story.
- Rerender the final {{dashboard_path}} from the updated scored.json and show the original story near the end of the dashboard by default, before the final audit/sources section when that section exists.
- Add three buttons immediately above the story text in {{dashboard_path}}: Basic, Informed, and Expert. These buttons must not call an LLM or external API from the browser; they only switch the visible text between the embedded variants in dashboard_content.story while preserving the original story in the embedded JSON.
- Storage option 1 is required: do not change Storage_system_js, do not create a content_artifacts row, and do not add storage schema/importer logic. The story is ingested through raw_payload_json and raw_scored_json because it lives inside dashboard_content.story.

Permissions:
- You may use network access for curl, SEC.gov, OpenAlex, patent databases, company investor-relations pages,
and image generation without asking first.
- You may run local validation commands, JSON tooling, Node scripts, Python scripts, and browser/headless
screenshot checks without asking first.
- You may create, edit, and overwrite files inside this repo under public/runs/, imagegen/, and
scripts/ without asking first.
- Do not ask for approval unless the action is destructive, writes outside the repo, installs packages, uses
paid APIs, or changes system configuration.
- If a command fails because of sandbox/network restrictions, request escalation once using the broadest
reasonable approved prefix for this task, then continue without asking again for similar commands.
