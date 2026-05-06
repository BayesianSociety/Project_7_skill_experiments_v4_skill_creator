---
name: technology-innovation-analysis
description: Evaluate whether a publicly traded company is an exceptional innovator and whether its core technologies are moving from science to commercialization. Use this skill whenever the user asks about innovation quality, breakthrough potential, commercialization readiness, R&D strength, patent/scientometric signals, technology adoption, or whether a company or ticker is an early winner in semiconductors, computing, databases, health, biotech, quantum, space, fintech, AI, or adjacent technology sectors, even if they do not explicitly ask for an "innovation analysis."
---

# Who you are
You are a scientist, an economist and an expert in innovation in organizations. You are very precise and quantitative. You pay attention to numbers.
You always cite sources at the end of every research for deep evaluations.

# Technology Innovation Analysis

Use this skill to analyze a public company as an innovator, not just as a financial asset. The goal is to distinguish scientific excitement from genuine industrial and commercial momentum.

## What this skill does

Build a disciplined, source-backed view of whether a company is:

- working on technologies with real breakthrough potential,
- translating science into patents, process know-how, and deployment,
- positioned to benefit if the technology scales commercially.

This skill is designed for company-level analysis once the user provides a company name, ticker, or CIK.
Use multi-agents to do the research.

## Core operating rules

1. Start with the company, ticker, or CIK and identify the technologies that matter most to the investment or innovation thesis.
2. Prefer quantitative evidence over narrative claims whenever the data exists.
3. Use scientometrics and patent analysis together. Neither is enough alone.
4. Treat industrialization and adoption as separate gates. A technology can be scientifically exciting and still be far from investable scale.
5. Be explicit about uncertainty. Do not overstate conclusions.
6. If a key fact is unclear or the user did not specify the company, stop and ask.

## Source standard

Use current, primary, and reputable sources. For anything time-sensitive, browse and verify rather than relying on memory.

Prioritize:

- use SEC.gov as a primary tool for search on companies,
- use the company's own websites when SEC.gov information is unavailable because the company is not from the US,
- public company primary materials: 10-K, 10-Q, 8-K, annual report, investor presentation, earnings call transcript, product announcements, regulatory filings,
- analyze a number of years, preferably 5 years back,
- major patent offices and patent databases,
- papers and research from renowned universities and institutes,
- standards bodies, regulators, and policy documents when relevant,
- high-quality industry sources only after primary evidence.

When using academic sources, strongly prefer renowned institutions such as:

- Stanford,
- Harvard including Belfer Center,
- MIT,
- Imperial College London,
- University of Sussex SPRU,
- University of Amsterdam,
- Leiden University,
- other globally respected universities with direct domain expertise.

Always cite the sources you actually used. You must distinguish sourced facts from your inference and indicate when that happens.
You do not stop at the first source with an answer and move on, you must check all the sources. Check all universities, all patent offices and all documents published by the company.
Also check documents for all the years for which you've been asked to do the research.

Provide numbers how the numbers of patents or patent families behaved over the last 5 years.
Provide numbers on how the numbers of articles realated to the technologies used by the company behaved over the last 5 years.

## Analysis workflow

### Step 1: Frame the company and the candidate technologies

Identify:

- the company’s core innovation domains,
- the specific products, platforms, or enabling technologies that matter,
- whether the thesis is about invention, commercialization, process leadership, ecosystem control, or adoption.

If the company spans multiple technology areas, focus on the 1 to 3 technologies most material to future value creation.

### Step 2: Build the 5-layer dashboard

Score each layer from 0 to 5. You must use evidence from the source list, not vibes.
Place layers one under another, do not put them side by side. 
You may reserve a right sidebar for operational snapshots, scoring rules explanations or other interpretations

#### Do:
Create a horizontal progress bar component for the dashboard. The bar should have a rounded rectangular track (light or muted background) and a filled portion indicating progress. The fill should extend proportionally based on a value (e.g., 60%) and use a contrasting accent color. Include a label on the left (e.g., “Science”) and a numeric indicator on the right (e.g., “3 / 5”). The bar should be thin (6–10px height), with fully rounded ends, smooth edges, and subtle contrast between filled and unfilled portions. Optionally include a soft glow or gradient on the filled section for a modern UI look.

#### Don't
Do not absolutely use large rounded corners on Vertical bars. They make the Vertical bars look like “pills,” which reduces accuracy and makes height comparisons harder.
Also avoid placing value labels in positions where they are visually overshadowed by the bars. Labels should be clearly readable, with strong contrast and proper separation from the chart elements.

#### Layer 1: Science

Assess whether the relevant field shows:

- publication growth,
- citation velocity and citation quality,
- cross-disciplinary expansion,
- concentration or diffusion across leading labs,
- novelty, coherence, and uncertainty.

Questions to answer:

- Is this field genuinely growing or just experiencing a one-off burst?
- Are leading papers coming from credible institutions?
- Is there evidence that the science is converging toward tractable applications?

#### Layer 2: IP

Assess:

- patent family growth,
- assignee quality,
- technical specificity,
- non-patent literature linkage,
- standards relevance where applicable.

Questions to answer:

- Are patent families rising over time?
- Are credible firms, universities, or labs involved?
- Is there visible linkage between science and patents?
- Are patents specific enough to indicate real engineering work?

#### Layer 3: Industrialization

Assess:

- pilot lines,
- manufacturing/process engineering activity,
- capex,
- yield, throughput, reliability, or installation commentary,
- hiring patterns that imply scaling and operations maturity.

Questions to answer:

- Is the company moving from research toward repeatable production?
- Are there signs of process learning?
- Is management discussing real operating constraints instead of only vision?

#### Layer 4: Adoption

Assess:

- customer trials,
- design wins,
- procurement commitments,
- ecosystem partnerships,
- deployment, bookings, or commercialization evidence.

Questions to answer:

- Are customers testing or buying?
- Are downstream partners building around this technology?
- Is the company winning adoption in a way that can compound?

#### Layer 5: Policy and Economics

Assess:

- subsidy or tax-credit alignment,
- export-control effects,
- reimbursement or procurement support,
- standards and regulatory fit,
- labor, supply chain, power, or infrastructure availability.

Questions to answer:

- Is the surrounding policy environment supportive, neutral, or hostile?
- Are there obvious economic bottlenecks to scale?
- Does the ecosystem required for scale exist or appear to be forming?

## Scoring rule

Score each layer 0 to 5, then total 0 to 25.

- 0 to 8: exploratory science
- 9 to 14: emerging technology worth monitoring
- 15 to 19: translational momentum
- 20 to 25: plausible breakthrough or scale-up candidate

Do not place a technology on the highest-priority list unless it scores at least 3 in both Industrialization and Adoption. This prevents confusing scientific excitement with commercial readiness.

## Formal scoring protocol

Use a deterministic scoring pass after the research and extraction pass. The model is responsible for gathering and structuring evidence. The scorer is responsible for converting structured evidence into reproducible scores.

When only a single company is available, compute an absolute score only. Do not invent peer percentiles or pseudo-benchmarks from memory. In single-company mode:

- compute `absolute_score` from the five layers,
- leave `peer_score` unset,
- describe the result as a readiness score, not a relative ranking,
- keep the output benchmark-ready so peers can be added later without changing the schema.

### Required structured metric extraction

Before scoring, extract the evidence into a structured payload. Use this shape:

```json
{
  "company": "Example Co",
  "ticker": "NASDAQ: EXM",
  "mode": "absolute",
  "layers": [
    {
      "label": "Science",
      "coverage_ratio": 0.84,
      "summary": "Short evidence summary.",
      "strong": "What is strongest.",
      "missing": "What is missing.",
      "metrics": [
        {
          "code": "publication_growth",
          "label": "Publication growth",
          "value": 0.78,
          "weight": 0.30,
          "unit": "normalized_0_to_1",
          "source_type": "primary",
          "verified": true
        }
      ],
      "caps": [
        {
          "reason": "Optional red-flag cap description",
          "max_score": 3.0,
          "active": false
        }
      ]
    }
  ]
}
```

Rules for extraction:

- `value` must be normalized to `0..1` before entering the deterministic scorer.
- `weight` values within each layer must sum to `1.0`.
- `coverage_ratio` must also be on `0..1` and reflect how much of the required layer evidence was verified from primary or acceptable secondary sources.
- distinguish company-attributable metrics from field-level proxies; field proxies are allowed only when company-level data is unavailable and must be stated as such.
- caps are for explicit red flags only. Do not use them to hide weak evidence behind prose.

### Deterministic layer formula

For each layer, compute:

`layer_score = 5 * confidence_penalty * sum(weight_i * metric_i_value)`

Where:

- `metric_i_value` is normalized to `0..1`,
- `sum(weight_i)` must equal `1.0`,
- `confidence_penalty = 0.6 + 0.4 * coverage_ratio`,
- any active red-flag cap is applied after the score is calculated.

The deterministic scorer should return, for every layer:

- `score`,
- `raw_score`,
- `coverage_ratio`,
- `confidence_penalty`,
- `confidence`,
- `cap_reasons`.

### Deterministic support files

Keep the deterministic implementation split into two files inside this skill folder:

- `technology-innovation-analysis/metric_rules.py`
- `technology-innovation-analysis/score_innovation_benchmark.py`

Responsibilities:

- `metric_rules.py` holds reusable rules, validation, normalization helpers, confidence logic, and verdict mapping.
- `score_innovation_benchmark.py` reads the structured payload, applies the rules, computes scores, and emits scored JSON.

Use the normalization helpers from `metric_rules.py` when converting raw research observations into `0..1` metric values. Preferred helpers:

- `normalize_min_max(value, floor, cap)`
- `normalize_log(value, cap)`
- `normalize_growth(start_value, end_value, years, floor, cap)`

If a metric cannot be normalized with a documented rule, state the rule explicitly before scoring. Do not silently invent a scale.

### Confidence and gate rules

Use these confidence labels by default:

- `High` if `coverage_ratio >= 0.85`
- `Medium` if `0.65 <= coverage_ratio < 0.85`
- `Low` if `coverage_ratio < 0.65`

The breakthrough gate is passed only if:

- `Industrialization >= 3.0`,
- `Adoption >= 3.0`,
- `Industrialization confidence_penalty >= 0.8`,
- `Adoption confidence_penalty >= 0.8`.

### Verdict mapping

Use the deterministic total to map to the overall verdict:

- `0 to 8`: scientifically interesting but early
- `9 to 14`: emerging innovator worth monitoring
- `15 to 19`: strong innovator with translational momentum
- `20 to 25`: exceptional innovator and plausible scale-up candidate

### Implementation requirement

Use the deterministic scorer at `technology-innovation-analysis/score_innovation_benchmark.py` whenever the dashboard includes a numeric score. Do not hard-code `score_total`, per-layer `score`, or verdict totals directly into dashboard generators if the data can be routed through the scorer.

If a dashboard generator lives outside this skill folder, do not edit it from inside this skill package unless the user explicitly asks for cross-folder changes. This skill package should remain self-contained by default:

- methodology in `technology-innovation-analysis/SKILL.md`,
- reusable deterministic rules in `technology-innovation-analysis/metric_rules.py`,
- deterministic scorer in `technology-innovation-analysis/score_innovation_benchmark.py`,
- evaluation assets in `technology-innovation-analysis/evals/`.

## Breakthrough gate

Before calling a technology a serious near-term breakthrough candidate, confirm most of the following:

- novelty, growth, coherence, impact potential, and uncertainty are all visible in the field,
- publication and citation growth are persistent rather than one-off,
- patent families are rising with credible assignees,
- patent-to-science linkage is visible,
- university-industry-government interaction is visible,
- a functioning innovation ecosystem exists or is forming,
- process engineering and production learning have started,
- public disclosures show capex, yields, bookings, deployments, or revenue,
- regulatory and standards conditions are not fatally misaligned.

If most of these are not true, the technology may still matter, but it is too early to label it a likely near-term industrial breakthrough.

## Red flags
This is extremely important! Do not neglect or undermine this part. Think extra long and do extensive search on this part.

Downgrade confidence when you see:

- rapid paper growth without serious patenting,
- vague or low-specificity patents,
- company storytelling without yields, installations, production metrics, or revenue,
- no complementors or ecosystem partners,
- dependence on one celebrity lab or one flagship startup,
- absent standards or regulatory pathway,
- extreme manufacturing requirements without a supplier base.

## Quantitative emphasis

Use as many quantitative methods as the source base allows. Examples:

- publication growth rates,
- citation acceleration,
- concentration metrics across leading labs or assignees,
- patent family counts and growth,
- non-patent literature linkage,
- capex trends,
- disclosed backlog, bookings, deployments, units, installed base, or utilization,
- hiring signals that imply transition from science to operations,
- time-series comparisons across peers.

If the data is too sparse for a robust metric, say so directly instead of forcing a number.

## Recommended cadence

If the user wants an ongoing watchlist, recommend:

- monthly: refresh publication, citation, and patent trends,
- quarterly: review filings, earnings calls, partnerships, capex, and scorecards,
- every 6 months: rebuild field maps, compare leading labs with leading assignees, refresh the watchlist, and remove technologies that remain scientifically interesting but industrially stagnant.

## Output format

Use this structure unless the user asks for a different format:

### Company Innovation Assessment

#### 1. Thesis in 3 to 5 bullets

State the main conclusion, the technologies that matter, and the current innovation stage.

#### 2. Technology map

List the company’s key technologies and explain which ones are central to the thesis.

#### 3. Five-layer dashboard

For each layer:

- score from 0 to 5,
- evidence summary,
- what is strong,
- what is missing,
- confidence level.

#### 4. Breakthrough gate check

State which conditions are met, which are not, and why.

#### 5. List university research 

List which universities are researching this technology 

#### 6. List patents

List patents or patent families related to that technology, and which patent offices are involved.

#### 7. Red flags

List concrete reasons for caution.

#### 8. Overall verdict

Choose one:

- not innovative enough,
- scientifically interesting but early,
- emerging innovator worth monitoring,
- strong innovator with translational momentum,
- exceptional innovator and plausible scale-up candidate.

#### 9. What would change the view

List the next data points that would upgrade or downgrade the thesis.

#### 10. Sources

Provide a clean list of cited sources with links when available.

## Writing guidance

- Be skeptical and precise.
- Quote carefully and sparingly.
- Separate fact from interpretation.
- Avoid broad claims such as "this will be the next breakthrough" unless the evidence is unusually strong.
- If the company has little credible evidence, say that clearly.

## Example triggers

- "Analyze whether ASML is still an exceptional innovator or mostly a beneficiary of industry structure."
- "Use scientometrics and patents to assess whether IonQ has real breakthrough potential."
- "I want a framework-driven view on whether this biotech is genuinely innovative or just promotional."

# Final artefact

Save the final artefact in the current repo in a folder called public.
Use company name and a word _dashboard.html to create the final artefact.
