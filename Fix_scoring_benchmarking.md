# Fix Scoring Benchmarking

## Conversation Transcript

### User
I'm going to give you a skill. I want you to analyze it. Also look into the folder public and analyze all the
files listed in that folder.
Answer the question how you set benchmarks for comparison of scoring number between companies if all of them have around 19 out of 25, despite being totaly different companies.
Investigate if the benchmarking algorithem is properly set up. Be critical.

Here's the skill:
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

### Assistant
**Findings**

1. There is no real benchmarking algorithm in the skill. The skill defines a rubric, not a benchmarked scoring system. It says “score each layer from 0 to 5” and gives bucket cutoffs (`0-8`, `9-14`, `15-19`, `20-25`), but it never defines how raw metrics map to those scores, how peers are chosen, or how cross-industry normalization works.

2. The generated dashboards mostly use manual judgment with proxy inputs, not algorithmic calibration. The clearest evidence is in `scripts/generate_ionq_artifacts.py`, where `SCORES` are hard-coded as `4, 3, 3, 4, 3`, and in `tools/generate_csl_dashboard_assets.py`, where `score_total` and per-layer `score` values are also hard-coded. That is editorial synthesis, not an algorithm.

3. Cross-company comparability is weak because the same 0-5 rubric is applied to very different businesses without sector baselines. A logistics operator, a plasma biotech, a hearing-device company, a semiconductor company, and a quantum company are all pushed through the same five buckets. That is why unrelated companies cluster around `18-19 / 25`.

4. The system uses field-level proxies where company-level measures are needed, which inflates similarity across companies. Several dashboards explicitly say science counts come from OpenAlex or PubMed topic searches rather than company-authored output.

5. Patent benchmarking is also mostly proxy-based and incomplete, so the IP layer is not robust enough for precise scoring.

6. Missing data handling is ad hoc, not systematic. In some cases sparse data lowers a score manually; in others the company still lands near 19. There is no formal penalty function for incomplete patent-family coverage, no confidence-adjusted scoring, and no rule for when a score should be withheld instead of estimated.

7. The skill itself overpromises impossible source coverage. It says to check “all universities, all patent offices and all documents published by the company.” That is not operationally realistic, so the actual artefacts inevitably fall back to selective proxies and judgment.

**Answer to your benchmark question**

The honest answer is: the benchmarks are not properly set. The scores are being set by a coarse, evidence-backed editorial rubric, not by a calibrated benchmarking algorithm.

Why so many companies land around `19 / 25`:
- The rubric has strong ceiling compression.
- Mature public companies with real revenue, some R&D, visible products, and decent adoption will often get `3-5` in Industrialization and Adoption.
- Science and IP are often scored with broad field proxies, so they rarely collapse to `0-1` unless evidence is obviously absent.
- Policy/Economics tends to sit around `3`.
- Add that up and many firms converge around `17-19`.

In other words, `19` here does not mean “this company is as innovative as another company with 19.” It means “the analyst judged this company to have strong translational momentum under the same loose rubric.” Those are not the same thing.

**Public folder summary**

The `public` folder contains 10 dashboards. Score outcomes are:
- `19`: Cochlear, CSL, Deutsche Post, DSM-Firmenich, Philips, NXP, Sonova
- `18`: WiseTech
- `17`: IonQ
- `15`: PostNL

That distribution is a warning sign. For a benchmark system spanning biotech, medtech, semis, logistics, and quantum, this is too narrow unless the rubric is heavily compressed or lenient.

**Critical verdict**

The benchmarking algorithm is not properly set up if the goal is fair cross-company comparison.

It is acceptable as a structured qualitative assessment framework.
It is not acceptable as a rigorous cross-sector scoring algorithm.

**What a proper setup would need**

- Define sector-specific peer groups first.
- Convert raw metrics to normalized scores within sector and stage.
- Separate company-attributable metrics from field-level proxies.
- Use explicit mappings like percentile-to-score, not prose-to-score.
- Penalize missing data formally.
- Report uncertainty bands, not just point scores.
- Keep two outputs:
  - `absolute readiness score`
  - `relative peer percentile`

Without that, a `19/25` biotech and a `19/25` logistics operator are not benchmark-comparable.

### User
Explain how you would turn this into a concrete redesign of the scoring algorithm with formulas and a benchmark
table structure.

### Assistant
**Redesign**

I would stop pretending one raw `0-25` score can compare a quantum company, a plasma biotech, and a logistics operator directly. The redesign should produce two different outputs:

- `Absolute readiness score`: how far the company’s technology is from scalable commercialization on its own terms.
- `Relative peer score`: how strong the company is versus relevant peers in its sector and stage.

That gives you one score for maturity and one for competitive position.

**1. Build The Benchmark Structure**

Each company should be assigned to:
- `Sector`: semis, biotech, medtech, logistics software, quantum, industrial automation, etc.
- `Stage`: frontier science, translational, scaled commercial platform.
- `Technology lane`: the 1-3 domains actually being scored.

Then benchmark only against a peer set with the same `sector + stage + lane`.

Example benchmark table structure:

| company | sector | stage | tech_lane | year | science_raw | ip_raw | industrial_raw | adoption_raw | policy_raw | science_pct | ip_pct | industrial_pct | adoption_pct | policy_pct | abs_score | peer_score |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| IonQ | quantum | translational | trapped-ion QC | 2025 | 61 | 48 | 35 | 52 | 44 | 82 | 67 | 54 | 79 | 60 | 16.2 | 72.4 |
| NXP | semis | scaled platform | auto radar/UWB | 2025 | 43 | 77 | 85 | 81 | 62 | 58 | 84 | 88 | 86 | 70 | 18.4 | 77.1 |

**2. Replace Editorial 0-5 Scores With Formula Scores**

Each layer should be calculated from submetrics. Example:

`LayerScore_j = 5 * ConfidencePenalty_j * sum(w_i * Metric_i_norm)`

Where:
- `j` is Science, IP, Industrialization, Adoption, Policy
- `Metric_i_norm` is each submetric normalized to `0..1`
- `w_i` sums to `1`
- `ConfidencePenalty_j` is between `0.6` and `1.0`

So if IP data is incomplete, you do not just “feel” a `3/5`; you mathematically reduce the score.

**3. Normalize Metrics Properly**

Use two normalizations:

- `Absolute normalization`: maps raw evidence to commercialization readiness
- `Peer normalization`: percentile rank within peer set

Examples:

For monotonic metrics:
`norm(x) = min(1, max(0, (x - floor) / (cap - floor)))`

For skewed metrics like patents or citations:
`norm_log(x) = ln(1 + x) / ln(1 + cap)`

For growth rates:
`growth = (x_t / x_t-5)^(1/5) - 1`
`norm_growth = min(1, max(0, (growth - floor_g) / (cap_g - floor_g)))`

For percentile benchmarking:
`pct = percentile_rank(peer_group, x)`

**4. Example Layer Formulas**

**Science**
Use company-attributable science first. Field proxies only as secondary context.

`Science_raw = 0.30*PubGrowth + 0.20*CitationVelocity + 0.15*TopInstitutionShare + 0.15*TopicCoherence + 0.10*CompanyPaperShare + 0.10*ScienceToPatentLinkage`

Then:
`Science_score = 5 * ConfidencePenalty_science * Science_raw`

Notes:
- `PubGrowth`: 5-year CAGR of relevant publications
- `CitationVelocity`: citations per paper adjusted for age
- `TopInstitutionShare`: share of publications from top labs
- `TopicCoherence`: concentration around material technology themes
- `CompanyPaperShare`: company-affiliated output as share of field
- `ScienceToPatentLinkage`: fraction of patents citing non-patent literature or overlapping paper topics

**IP**
`IP_raw = 0.25*PatentFamilyGrowth + 0.20*PatentSpecificity + 0.20*AssigneeQuality + 0.15*JurisdictionBreadth + 0.10*NPLLinkage + 0.10*ForwardCitationQuality`

`IP_score = 5 * ConfidencePenalty_ip * IP_raw`

**Industrialization**
`Industrial_raw = 0.25*CapexIntensity + 0.20*ManufacturingEvidence + 0.20*ProcessMetrics + 0.20*ScaleOpsHiring + 0.15*InstalledCapacity`

`Industrial_score = 5 * ConfidencePenalty_ind * Industrial_raw`

If process metrics are absent:
- do not infer them from narrative
- reduce `ConfidencePenalty_ind`

**Adoption**
`Adoption_raw = 0.30*RevenueEvidence + 0.20*CustomerBreadth + 0.20*DeploymentScale + 0.15*PartnerDepth + 0.15*Repeatability`

`Adoption_score = 5 * ConfidencePenalty_adopt * Adoption_raw`

**Policy & Economics**
`Policy_raw = 0.25*RegulatoryFit + 0.20*SubsidyAlignment + 0.20*SupplyChainSupport + 0.20*UnitEconomicsPath + 0.15*StandardsAlignment`

`Policy_score = 5 * ConfidencePenalty_policy * Policy_raw`

**5. Confidence Penalty**

Right now missing data is handled informally. I would formalize it:

`ConfidencePenalty_j = 0.6 + 0.4 * DataCoverage_j`

Where:
- `DataCoverage_j` is share of required submetrics with verified primary data
- if 100% covered, penalty = `1.0`
- if 50% covered, penalty = `0.8`

You can also report:
- `confidence = high` if coverage > `0.85`
- `medium` if `0.65-0.85`
- `low` if `<0.65`

**6. Total Score Design**

I would compute two totals.

Absolute readiness:
`AbsScore = Science_score + IP_score + Industrial_score + Adoption_score + Policy_score`

Relative peer strength:
`PeerScore = 20 * (0.20*Science_pct + 0.20*IP_pct + 0.25*Industrial_pct + 0.25*Adoption_pct + 0.10*Policy_pct) / 100`

Then report:
- `Absolute readiness: 16.8 / 25`
- `Peer strength: 74 / 100 vs translational quantum peers`

This prevents fake equivalence between sectors.

**7. Gating Rules**

Keep explicit gates, but formalize them:

- `Breakthrough gate pass` only if:
  - `Industrial_score >= 3.0`
  - `Adoption_score >= 3.0`
  - `ConfidencePenalty_ind >= 0.8`
  - `ConfidencePenalty_adopt >= 0.8`

- `Exceptional innovator` only if:
  - `AbsScore >= 20`
  - `PeerScore >= 80`
  - no red-flag override triggered

**8. Red-Flag Overrides**

Some situations should cap the score.

Examples:
- No verified recent patent families:
  - `IP_score = min(IP_score, 2.0)`
- No revenue/deployment evidence:
  - `Adoption_score = min(Adoption_score, 2.5)`
- No yields/process metrics for manufacturing-heavy business:
  - `Industrial_score = min(Industrial_score, 3.0)`

That is much better than letting a company drift to `19` on narrative strength.

**9. Benchmark Table Tabs**

I would maintain these tables:

`peer_groups`
| peer_group_id | sector | stage | lane | ruleset_version |

`companies`
| company_id | company | ticker | country | sector |

`metrics_raw`
| company_id | year | metric_code | raw_value | unit | source_type | source_url | verified |

`metrics_norm_absolute`
| company_id | year | metric_code | norm_value |

`metrics_norm_peer`
| company_id | year | metric_code | percentile_value | peer_group_id |

`layer_scores`
| company_id | year | layer | raw_component_score | confidence_penalty | final_layer_score |

`final_scores`
| company_id | year | abs_score | peer_score | gate_pass | verdict |

**10. What This Fixes**

This redesign fixes the current problems:
- stops score compression around `18-19`
- separates maturity from peer leadership
- makes missing data visible mathematically
- makes the same score mean the same thing
- allows auditability back to formulas and sources

**Practical rule**

If you want one line:
- `25-point score` should mean absolute commercialization readiness
- `100-point peer score` should mean relative excellence within a comparable cohort

That is the cleanest redesign.

codex resume 019da731-2749-7420-b1a7-e3a21cdddf6c