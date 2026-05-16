"use client";

import { useMemo, useState } from "react";
import {
  Activity,
  ArrowUpRight,
  BadgeCheck,
  Braces,
  BookOpenText,
  Circle,
  Database,
  FileJson,
  Gauge,
  Layers3,
  Library,
  LineChart,
  Search,
  Server,
  ShieldCheck,
  Table2
} from "lucide-react";

function formatNumber(value) {
  return new Intl.NumberFormat("en-US").format(value ?? 0);
}

function scoreClass(score) {
  const numeric = Number(score);
  if (numeric >= 18) return "scoreHigh";
  if (numeric >= 14) return "scoreMid";
  return "scoreWatch";
}

function Pill({ children, tone = "neutral" }) {
  return <span className={`pill ${tone}`}>{children}</span>;
}

function StatLine({ icon: Icon, label, value }) {
  return (
    <div className="statLine">
      <Icon size={17} strokeWidth={1.8} />
      <span>{label}</span>
      <strong>{formatNumber(value)}</strong>
    </div>
  );
}

function SystemMap({ status }) {
  const steps = [
    { label: "JSON", value: status.analysis_runs, icon: FileJson },
    { label: "SQLite", value: status.analysis_metrics, icon: Database },
    { label: "API", value: status.json_ingestion_events, icon: Server },
    { label: "Next.js", value: status.content_artifacts, icon: Table2 }
  ];

  return (
    <div className="systemMap" aria-label="Storage flow">
      {steps.map((step, index) => {
        const Icon = step.icon;
        return (
          <div className="systemNode" key={step.label} style={{ "--delay": `${index * 80}ms` }}>
            <div className="nodeIcon">
              <Icon size={18} />
            </div>
            <div>
              <span>{step.label}</span>
              <strong>{formatNumber(step.value)}</strong>
            </div>
          </div>
        );
      })}
    </div>
  );
}

function RunList({ runs, selectedRunUid, onSelect }) {
  return (
    <section className="workspaceSection runsSection" aria-labelledby="runs-heading">
      <div className="sectionHeader">
        <div>
          <p className="eyebrow">Portfolio</p>
          <h2 id="runs-heading">Analysis runs</h2>
        </div>
        <Pill tone="ink">{runs.length} runs</Pill>
      </div>

      <div className="runTable" role="list">
        {runs.map((run) => (
          <button
            className={`runRow ${selectedRunUid === run.run_uid ? "active" : ""}`}
            key={run.run_uid}
            onClick={() => onSelect(run.run_uid)}
            type="button"
          >
            <span className="companyBlock">
              <strong>{run.company}</strong>
              <small>{run.ticker || "No ticker"} · {run.research_date || "No date"}</small>
            </span>
            <span className={`scoreBadge ${scoreClass(run.display_total_score)}`}>
              {run.display_total_score || "n/a"}
            </span>
            <span className="runMeta">
              <span>{run.metric_count} metrics</span>
              <span>{run.evidence_count} evidence</span>
            </span>
            <span className={`gate ${run.gate_pass ? "pass" : "watch"}`}>
              <Circle size={8} fill="currentColor" />
              {run.gate_pass ? "Pass" : "Watch"}
            </span>
          </button>
        ))}
      </div>
    </section>
  );
}

function LayerBars({ layers = [] }) {
  return (
    <div className="layerBars">
      {layers.map((layer) => {
        const score = Number(layer.score || 0);
        return (
          <div className="layerBar" key={layer.label}>
            <div className="layerTop">
              <span>{layer.label}</span>
              <strong>{layer.display_score || score.toFixed(1)}</strong>
            </div>
            <div className="barTrack">
              <span style={{ width: `${Math.min(score / 5, 1) * 100}%` }} />
            </div>
          </div>
        );
      })}
    </div>
  );
}

function SelectedRun({ selectedRun, selectedSummary }) {
  const metrics = selectedRun?.metrics || [];
  const layers = selectedRun?.layers || [];
  const topMetrics = [...metrics].sort((a, b) => Number(b.value || 0) - Number(a.value || 0)).slice(0, 6);

  return (
    <section className="workspaceSection detailSection" aria-labelledby="selected-heading">
      <div className="detailHead">
        <div>
          <p className="eyebrow">Selected run</p>
          <h2 id="selected-heading">{selectedSummary.company}</h2>
          <p className="detailCopy">{selectedSummary.verdict}</p>
        </div>
        <div className="scoreLockup">
          <span>Total score</span>
          <strong>{selectedSummary.display_total_score}</strong>
        </div>
      </div>

      <div className="detailGrid">
        <div className="plainPanel">
          <div className="panelTitle">
            <Layers3 size={18} />
            Layer scores
          </div>
          <LayerBars layers={layers} />
        </div>

        <div className="plainPanel">
          <div className="panelTitle">
            <Gauge size={18} />
            Highest metrics
          </div>
          <div className="metricList">
            {topMetrics.map((metric) => (
              <div className="metricRow" key={`${metric.layer}-${metric.metric_code}`}>
                <span>
                  <strong>{metric.metric_code.replaceAll("_", " ")}</strong>
                  <small>{metric.layer}</small>
                </span>
                <b>{Number(metric.value || 0).toFixed(2)}</b>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

function EvidenceInspector({ evidence = [], metricEvidence = [] }) {
  const [query, setQuery] = useState("");
  const filteredEvidence = useMemo(() => {
    const needle = query.trim().toLowerCase();
    if (!needle) return evidence.slice(0, 8);
    return evidence
      .filter((item) => [item.fact, item.source_title, item.publisher, item.layer_label].join(" ").toLowerCase().includes(needle))
      .slice(0, 8);
  }, [evidence, query]);

  return (
    <section className="workspaceSection inspectorSection" aria-labelledby="evidence-heading">
      <div className="sectionHeader">
        <div>
          <p className="eyebrow">Evidence</p>
          <h2 id="evidence-heading">Source trail</h2>
        </div>
        <Pill>{metricEvidence.length} links</Pill>
      </div>

      <label className="searchBox">
        <Search size={17} />
        <input
          aria-label="Search evidence"
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Search evidence"
          value={query}
        />
      </label>

      <div className="evidenceList">
        {filteredEvidence.length ? (
          filteredEvidence.map((item) => (
            <article className="evidenceItem" key={item.local_evidence_id}>
              <div className="evidenceTop">
                <Pill tone={item.verified ? "green" : "neutral"}>{item.verified ? "Verified" : "Review"}</Pill>
                <span>{item.local_evidence_id}</span>
              </div>
              <p>{item.fact}</p>
              <small>{item.publisher || "Unknown publisher"} · {item.layer_label || "No layer"}</small>
            </article>
          ))
        ) : (
          <div className="emptyState">
            <Library size={22} />
            <span>No evidence matched this search.</span>
          </div>
        )}
      </div>
    </section>
  );
}

function SchemaHealth({ observations = [] }) {
  const issues = observations.filter((item) => item.unmapped.length || item.missing.length);
  return (
    <section className="workspaceSection schemaSection" aria-labelledby="schema-heading">
      <div className="sectionHeader">
        <div>
          <p className="eyebrow">Schema health</p>
          <h2 id="schema-heading">Ingestion checks</h2>
        </div>
        <Pill tone={issues.length ? "amber" : "green"}>
          {issues.length ? `${issues.length} issues` : "Clean"}
        </Pill>
      </div>

      <div className="schemaRows">
        {observations.slice(0, 6).map((item) => (
          <div className="schemaRow" key={item.id}>
            <Braces size={17} />
            <span>
              <strong>{item.document_role}</strong>
              <small>{item.run_uid} · {item.declared_schema_version}</small>
            </span>
            <b>{item.unmapped.length + item.missing.length}</b>
          </div>
        ))}
      </div>
    </section>
  );
}

function titleFromKey(key) {
  return key
    .replaceAll("_", " ")
    .replace(/\b\w/gu, (letter) => letter.toUpperCase());
}

const referenceKeys = new Set(["evidence_ids", "source_ids", "claim_ids"]);

function compactText(value, limit = 180) {
  const text = String(value || "").replace(/\s+/gu, " ").trim();
  if (!text) return "";
  if (text.length <= limit) return text;
  return `${text.slice(0, limit - 3).trimEnd()}...`;
}

function joinMeta(parts) {
  return parts.filter(Boolean).join(" · ");
}

function asArray(value) {
  return Array.isArray(value) ? value : [];
}

function storyParagraphs(story = {}) {
  if (asArray(story.paragraphs).length) return asArray(story.paragraphs);
  return String(story.body_markdown || "")
    .split(/\n{2,}/u)
    .map((paragraph) => paragraph.replace(/^#+\s*/u, "").trim())
    .filter(Boolean);
}

function itemHeading(item) {
  return item?.title || item?.name || item?.label || item?.condition || item?.frequency || item?.period || "";
}

function itemBody(item) {
  return item?.text || item?.summary || item?.description || item?.signal || item?.interpretation || item?.monitoring_source || item?.task || "";
}

function itemMeta(item) {
  return joinMeta([
    item?.maturity,
    item?.severity,
    item?.layer,
    item?.period,
    item?.value,
    item?.claim_type,
    item?.confidence,
    item?.company_attributable === false ? "Field proxy" : null
  ]);
}

function resolveReference(type, id, referenceIndex = {}) {
  const key = String(id);

  if (type === "claim") {
    const claim = referenceIndex.claimsById?.[key];
    return {
      text: compactText(claim?.text) || "Claim not found in this run.",
      meta: joinMeta([claim?.section, claim?.claim_type, claim?.confidence]),
      missing: !claim
    };
  }

  if (type === "evidence") {
    const evidence = referenceIndex.evidenceById?.[key];
    return {
      text: compactText(evidence?.fact) || "Evidence not found in this run.",
      meta: joinMeta([evidence?.layer_label, evidence?.publisher]),
      missing: !evidence
    };
  }

  const source = referenceIndex.sourcesById?.[key];
  return {
    text: compactText(source?.title) || "Source not found in this run.",
    meta: joinMeta([source?.publisher, source?.document_date, source?.source_type]),
    href: source?.canonical_url || null,
    missing: !source
  };
}

function ReferenceLine({ id, resolved }) {
  return (
    <li className={`narrativeRefItem ${resolved.missing ? "missing" : ""}`}>
      <code className="refCode">{id}</code>
      <span className="refSummary">
        {resolved.href ? (
          <a href={resolved.href} target="_blank" rel="noreferrer">
            {resolved.text}
          </a>
        ) : (
          resolved.text
        )}
        {resolved.meta && <small>{resolved.meta}</small>}
      </span>
    </li>
  );
}

function ViewSwitcher({ viewMode, onChange }) {
  const options = [
    { value: "storage", label: "Storage audit", icon: Database },
    { value: "dashboard", label: "Dashboard", icon: LineChart }
  ];

  return (
    <div className="viewSwitch" role="tablist" aria-label="View mode">
      {options.map((option) => {
        const Icon = option.icon;
        return (
          <button
            aria-selected={viewMode === option.value}
            className={viewMode === option.value ? "active" : ""}
            key={option.value}
            onClick={() => onChange(option.value)}
            role="tab"
            type="button"
          >
            <Icon size={15} />
            {option.label}
          </button>
        );
      })}
    </div>
  );
}

function NarrativeRefs({ item, referenceIndex }) {
  const refs = [
    { label: "Claims", type: "claim", values: item.claim_ids },
    { label: "Evidence", type: "evidence", values: item.evidence_ids },
    { label: "Sources", type: "source", values: item.source_ids }
  ].filter(({ values }) => Array.isArray(values) && values.length);

  if (!refs.length) return null;

  return (
    <div className="narrativeRefs" aria-label="Resolved references">
      {refs.map(({ label, type, values }) => (
        <div className="narrativeRefGroup" key={label}>
          <b>{label}</b>
          <ul className="narrativeRefList">
            {values.map((id, index) => (
              <ReferenceLine
                id={String(id)}
                key={`${label}-${id}-${index}`}
                resolved={resolveReference(type, id, referenceIndex)}
              />
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}

function DashboardProgress({ label, score, confidence }) {
  const numeric = Number(score || 0);
  return (
    <div className="dashboardProgress">
      <div>
        <span>{label}</span>
        <strong>{numeric ? numeric.toFixed(1) : "0.0"} / 5</strong>
      </div>
      <div className="dashboardTrack">
        <span style={{ width: `${Math.min(Math.max(numeric / 5, 0), 1) * 100}%` }} />
      </div>
      {confidence && <small>Confidence: {confidence}</small>}
    </div>
  );
}

function DashboardItem({ item, referenceIndex, tone = "" }) {
  const heading = itemHeading(item);
  const body = itemBody(item);
  const meta = itemMeta(item);

  return (
    <article className={`dashboardItem ${tone}`}>
      {heading && <h4>{heading}</h4>}
      {body && <p>{body}</p>}
      {meta && <small>{meta}</small>}
      <NarrativeRefs item={item} referenceIndex={referenceIndex} />
    </article>
  );
}

function DashboardSection({ eyebrow, title, summary, children }) {
  if (!children) return null;

  return (
    <section className="companyDashSection">
      <div className="companyDashSectionHead">
        {eyebrow && <p className="eyebrow">{eyebrow}</p>}
        <h3>{title}</h3>
        {summary && <p>{summary}</p>}
      </div>
      <div className="companyDashSectionBody">{children}</div>
    </section>
  );
}

function DashboardChart({ chart, referenceIndex }) {
  const series = asArray(chart?.series);
  const values = series.flatMap((serie) => asArray(serie.points).map((point) => Number(point.value || 0)));
  const max = Math.max(...values, 1);

  return (
    <article className="dashboardItem chartDashboardItem">
      <h4>{chart?.title || chart?.chart_id || "Chart"}</h4>
      {chart?.description && <p>{chart.description}</p>}
      <div className="dashboardChart">
        {series.map((serie) => (
          <div className="dashboardChartSeries" key={serie.label || serie.unit}>
            <div className="dashboardChartSeriesHead">
              <strong>{serie.label || "Series"}</strong>
              {serie.unit && <small>{serie.unit}</small>}
            </div>
            {asArray(serie.points).map((point) => {
              const value = Number(point.value || 0);
              return (
                <div className="dashboardBarRow" key={`${serie.label}-${point.period}`}>
                  <span>{point.period}</span>
                  <div className="dashboardMiniTrack">
                    <b style={{ width: `${Math.max(2, (value / max) * 100)}%` }} />
                  </div>
                  <strong>{formatNumber(value)}</strong>
                </div>
              );
            })}
          </div>
        ))}
      </div>
      <NarrativeRefs item={chart} referenceIndex={referenceIndex} />
    </article>
  );
}

function CompanyDashboard({ selectedRun, selectedSummary }) {
  const [storyVariant, setStoryVariant] = useState("original");
  const dashboardContent = selectedRun?.narrative?.dashboard_content || {};
  const referenceIndex = selectedRun?.referenceIndex || {};
  const layers = selectedRun?.layers || [];
  const sources = selectedRun?.sources || [];
  const claims = selectedRun?.narrative?.claims || [];
  const thesis = dashboardContent.thesis || {};
  const breakthrough = dashboardContent.breakthrough_gate || {};
  const technologyMap = dashboardContent.technology_map || {};
  const quantitative = dashboardContent.quantitative_signals || {};
  const commercial = dashboardContent.commercialization_evidence || {};
  const university = dashboardContent.university_research_signals || {};
  const patent = dashboardContent.patent_signals || {};
  const redFlags = asArray(dashboardContent.red_flags);
  const watchlist = dashboardContent.watchlist || {};
  const operational = dashboardContent.operational_snapshot || {};
  const methodNotes = dashboardContent.method_notes || {};
  const bottomLine = dashboardContent.bottom_line || {};
  const story = dashboardContent.story || {};
  const originalStory = story.original || (story.paragraphs || story.body_markdown
    ? { label: "Original", title: story.title, paragraphs: story.paragraphs, body_markdown: story.body_markdown }
    : null);
  const storyChoices = {
    original: originalStory,
    basic: story.variants?.basic,
    informed: story.variants?.informed,
    expert: story.variants?.expert
  };
  const activeStory = storyChoices[storyVariant] || originalStory || story.variants?.basic || story.variants?.informed || story.variants?.expert || {};
  const activeStoryParagraphs = storyParagraphs(activeStory);
  const storyButtons = [
    ["basic", "Basic"],
    ["informed", "Informed"],
    ["expert", "Expert"]
  ].filter(([key]) => storyChoices[key]);
  const hero = dashboardContent.hero || {};

  if (!selectedRun) return null;

  return (
    <section className="companyDashboard" aria-labelledby="dashboard-heading">
      <header className="companyDashHero">
        <div>
          <p className="eyebrow">{selectedSummary.ticker || selectedSummary.research_date || "Selected run"}</p>
          <h2 id="dashboard-heading">{hero.headline || selectedSummary.company}</h2>
          <p>{hero.subheadline || selectedSummary.verdict}</p>
          <div className="companyDashMeta">
            <Pill tone={selectedSummary.gate_pass ? "green" : "amber"}>{selectedSummary.gate_pass ? "Gate pass" : "Watch"}</Pill>
            <Pill>{selectedSummary.research_date || "No date"}</Pill>
            <Pill>{layers.length} layers</Pill>
          </div>
        </div>
        <div className="companyDashScore">
          <span>Readiness</span>
          <strong>{selectedSummary.display_total_score || "n/a"}</strong>
          <small>/ 25</small>
        </div>
      </header>

      <DashboardSection eyebrow="Thesis" title={thesis.title || "Investment Thesis"} summary={thesis.summary}>
        <div className="companyDashGrid two">
          <div className="dashboardItem">
            {asArray(thesis.bullets).length ? (
              <div className="dashboardBulletList">
                {asArray(thesis.bullets).map((item, index) => (
                  <DashboardItem item={item} key={item.label || item.text || index} referenceIndex={referenceIndex} />
                ))}
              </div>
            ) : (
              <p>{thesis.text || selectedSummary.verdict}</p>
            )}
          </div>
          <div className="dashboardItem">
            <h4>{breakthrough.title || "Breakthrough Gate"}</h4>
            {breakthrough.summary && <p>{breakthrough.summary}</p>}
            {breakthrough.result && <strong className="dashboardVerdict">{breakthrough.result}</strong>}
            <div className="dashboardMiniList">
              {asArray(breakthrough.conditions_met).slice(0, 2).map((item, index) => (
                <DashboardItem item={item} key={`met-${index}`} referenceIndex={referenceIndex} tone="positive" />
              ))}
              {asArray(breakthrough.conditions_not_met).slice(0, 2).map((item, index) => (
                <DashboardItem item={item} key={`not-met-${index}`} referenceIndex={referenceIndex} tone="watch" />
              ))}
            </div>
          </div>
        </div>
      </DashboardSection>

      <DashboardSection eyebrow="Scores" title="Five-Layer Dashboard">
        <div className="layerDashboardList">
          {layers.map((layer) => (
            <article className="layerDashboardRow" key={layer.layer_code || layer.label}>
              <div>
                <h4>{layer.label}</h4>
                {layer.coverage_ratio !== null && layer.coverage_ratio !== undefined && (
                  <small>Coverage {Math.round(Number(layer.coverage_ratio || 0) * 100)}%</small>
                )}
              </div>
              <DashboardProgress label={layer.label} score={layer.score} confidence={layer.confidence} />
              <div>
                {layer.summary && <p>{layer.summary}</p>}
                {layer.strong && <small><b>Strong:</b> {layer.strong}</small>}
                {layer.missing && <small><b>Missing:</b> {layer.missing}</small>}
              </div>
            </article>
          ))}
        </div>
      </DashboardSection>

      <DashboardSection eyebrow="Technology" title={technologyMap.title || "Technology Map"} summary={technologyMap.summary}>
        <div className="companyDashGrid">
          {asArray(technologyMap.items).map((item, index) => (
            <DashboardItem item={item} key={item.name || item.title || index} referenceIndex={referenceIndex} />
          ))}
        </div>
      </DashboardSection>

      <DashboardSection eyebrow="Quantitative" title={quantitative.title || "Quantitative Signals"} summary={quantitative.summary}>
        <div className="companyDashGrid two">
          {asArray(quantitative.charts).map((chart, index) => (
            <DashboardChart chart={chart} key={chart.chart_id || chart.title || index} referenceIndex={referenceIndex} />
          ))}
        </div>
      </DashboardSection>

      <DashboardSection eyebrow="Commercial" title={commercial.title || "Commercialization Evidence"} summary={commercial.summary}>
        <div className="companyDashGrid">
          {asArray(commercial.items).map((item, index) => (
            <DashboardItem item={item} key={item.label || item.title || index} referenceIndex={referenceIndex} />
          ))}
        </div>
      </DashboardSection>

      <DashboardSection eyebrow="Research" title="Research And IP" summary={university.summary || patent.summary}>
        <div className="companyDashGrid two">
          <div className="dashboardItem">
            <h4>{university.title || "University Research"}</h4>
            <div className="dashboardMiniList">
              {asArray(university.institutions).map((item, index) => (
                <DashboardItem item={item} key={item.name || index} referenceIndex={referenceIndex} />
              ))}
            </div>
          </div>
          <div className="dashboardItem">
            <h4>{patent.title || "Patents"}</h4>
            {patent.interpretation && <p>{patent.interpretation}</p>}
            <div className="dashboardMiniList">
              {asArray(patent.families).map((item, index) => (
                <DashboardItem item={item} key={item.publication_or_family_id || item.title || index} referenceIndex={referenceIndex} />
              ))}
            </div>
          </div>
        </div>
      </DashboardSection>

      <DashboardSection eyebrow="Risk" title="Red Flags">
        <div className="companyDashGrid">
          {redFlags.map((flag, index) => (
            <DashboardItem item={flag} key={flag.red_flag_id || flag.title || index} referenceIndex={referenceIndex} tone="risk" />
          ))}
        </div>
      </DashboardSection>

      <DashboardSection eyebrow="Monitoring" title={watchlist.title || "What Would Change The View"}>
        <div className="companyDashGrid three">
          <div className="dashboardItem">
            <h4>Upgrade Signals</h4>
            <div className="dashboardMiniList">
              {asArray(watchlist.upgrade_signals).map((item, index) => (
                <DashboardItem item={item} key={`upgrade-${index}`} referenceIndex={referenceIndex} tone="positive" />
              ))}
            </div>
          </div>
          <div className="dashboardItem">
            <h4>Downgrade Signals</h4>
            <div className="dashboardMiniList">
              {asArray(watchlist.downgrade_signals).map((item, index) => (
                <DashboardItem item={item} key={`downgrade-${index}`} referenceIndex={referenceIndex} tone="risk" />
              ))}
            </div>
          </div>
          <div className="dashboardItem">
            <h4>Cadence</h4>
            <div className="dashboardMiniList">
              {asArray(watchlist.cadence).map((item, index) => (
                <DashboardItem item={item} key={`cadence-${index}`} referenceIndex={referenceIndex} />
              ))}
            </div>
          </div>
        </div>
      </DashboardSection>

      <DashboardSection eyebrow="Operations" title={operational.title || "Operational Snapshot"}>
        <div className="companyDashGrid">
          {asArray(operational.metrics).map((metric, index) => (
            <article className="dashboardMetric" key={metric.label || index}>
              <span>{metric.label}</span>
              <strong>{metric.value}</strong>
              <small>{metric.period}</small>
              <NarrativeRefs item={metric} referenceIndex={referenceIndex} />
            </article>
          ))}
        </div>
      </DashboardSection>

      <DashboardSection eyebrow="Conclusion" title={bottomLine.title || "Bottom Line"}>
        <div className="companyDashGrid two">
          <div className="dashboardItem conclusionItem">
            <p>{bottomLine.text || selectedSummary.verdict}</p>
            <NarrativeRefs item={bottomLine} referenceIndex={referenceIndex} />
          </div>
          <div className="dashboardItem">
            <h4>{methodNotes.title || "Method Notes"}</h4>
            <ul className="methodList">
              {asArray(methodNotes.notes).map((note, index) => (
                <li key={`${note}-${index}`}>{note}</li>
              ))}
            </ul>
          </div>
        </div>
      </DashboardSection>

      <DashboardSection eyebrow="Story" title={activeStory.title || story.title || "Story"}>
        {activeStoryParagraphs.length ? (
          <div className="dashboardItem conclusionItem">
            {storyButtons.length > 0 && (
              <div className="viewSwitch" role="group" aria-label="Story level">
                {storyButtons.map(([key, label]) => (
                  <button
                    className={storyVariant === key ? "active" : ""}
                    key={key}
                    onClick={() => setStoryVariant(storyVariant === key ? "original" : key)}
                    type="button"
                  >
                    {label}
                  </button>
                ))}
              </div>
            )}
            {activeStoryParagraphs.map((paragraph, index) => (
              <p key={`${paragraph.slice(0, 32)}-${index}`}>{paragraph}</p>
            ))}
          </div>
        ) : null}
      </DashboardSection>

      <DashboardSection eyebrow="Audit" title="Claims And Sources">
        <div className="companyDashGrid two">
          <div className="dashboardItem">
            <h4>Claims Register</h4>
            <div className="dashboardMiniList">
              {claims.map((claim) => (
                <DashboardItem item={{ ...claim, title: claim.claim_id }} key={claim.claim_id} referenceIndex={referenceIndex} />
              ))}
            </div>
          </div>
          <div className="dashboardItem">
            <h4>Sources</h4>
            <div className="sourceRegister">
              {sources.map((source) => (
                <a href={source.canonical_url} key={source.local_source_id} rel="noreferrer" target="_blank">
                  <code>{source.local_source_id}</code>
                  <span>
                    <strong>{source.title}</strong>
                    <small>{joinMeta([source.publisher, source.document_date, source.source_type])}</small>
                  </span>
                </a>
              ))}
            </div>
          </div>
        </div>
      </DashboardSection>
    </section>
  );
}

function NarrativeTextBlock({ item, referenceIndex }) {
  const heading = item.title || item.name || item.label || item.condition || item.frequency || item.period;
  const body = item.text || item.summary || item.description || item.signal || item.interpretation || item.monitoring_source;
  const meta = [item.maturity, item.severity, item.layer, item.claim_type, item.confidence, item.value].filter(Boolean).join(" · ");

  return (
    <div className="narrativeItem">
      {heading && <h4>{heading}</h4>}
      {body && <p>{body}</p>}
      {meta && <small>{meta}</small>}
      <NarrativeRefs item={item} referenceIndex={referenceIndex} />
    </div>
  );
}

function NarrativeChart({ chart, referenceIndex }) {
  const series = Array.isArray(chart.series) ? chart.series : [];
  return (
    <div className="narrativeItem chartItem">
      <h4>{chart.title || chart.chart_id}</h4>
      {chart.description && <p>{chart.description}</p>}
      <div className="chartSeries">
        {series.map((serie) => (
          <div className="chartSeriesRow" key={serie.label}>
            <span>
              <strong>{serie.label}</strong>
              <small>{serie.unit}</small>
            </span>
            <div>
              {(serie.points || []).map((point) => (
                <b key={`${serie.label}-${point.period}`}>{point.period}: {point.value}</b>
              ))}
            </div>
          </div>
        ))}
      </div>
      <NarrativeRefs item={chart} referenceIndex={referenceIndex} />
    </div>
  );
}

function NarrativeCollection({ label, items, referenceIndex }) {
  if (!Array.isArray(items) || !items.length) return null;

  return (
    <div className="narrativeCollection">
      <h3>{titleFromKey(label)}</h3>
      <div className="narrativeList">
        {items.map((item, index) => {
          if (typeof item === "string") {
            return <div className="narrativeItem" key={`${label}-${index}`}><p>{item}</p></div>;
          }
          if (item?.series) {
            return <NarrativeChart chart={item} key={item.chart_id || item.title || `${label}-${index}`} referenceIndex={referenceIndex} />;
          }
          return <NarrativeTextBlock item={item} key={item.red_flag_id || item.claim_id || item.name || item.title || item.label || `${label}-${index}`} referenceIndex={referenceIndex} />;
        })}
      </div>
    </div>
  );
}

function NarrativeSection({ sectionKey, section, referenceIndex }) {
  if (!section) return null;

  if (Array.isArray(section)) {
    return (
      <section className="narrativeBlock">
        <div className="narrativeBlockHead">
          <p className="eyebrow">{titleFromKey(sectionKey)}</p>
          <h2>{titleFromKey(sectionKey)}</h2>
        </div>
        <NarrativeCollection label={sectionKey} items={section} referenceIndex={referenceIndex} />
      </section>
    );
  }

  const reserved = new Set(["title", "headline", "summary", "subheadline", "text", "verdict_label", ...referenceKeys]);
  const collections = Object.entries(section).filter(([key, value]) => Array.isArray(value) && !reserved.has(key));
  const scalarRows = Object.entries(section).filter(([key, value]) => !reserved.has(key) && value && typeof value !== "object");

  return (
    <section className="narrativeBlock">
      <div className="narrativeBlockHead">
        <p className="eyebrow">{titleFromKey(sectionKey)}</p>
        <h2>{section.title || section.headline || titleFromKey(sectionKey)}</h2>
        {(section.summary || section.subheadline || section.text) && (
          <p>{section.summary || section.subheadline || section.text}</p>
        )}
        {section.verdict_label && <Pill tone="green">{section.verdict_label}</Pill>}
        <NarrativeRefs item={section} referenceIndex={referenceIndex} />
      </div>

      {scalarRows.length > 0 && (
        <div className="narrativeFacts">
          {scalarRows.map(([key, value]) => (
            <div key={key}>
              <span>{titleFromKey(key)}</span>
              <strong>{String(value)}</strong>
            </div>
          ))}
        </div>
      )}

      {collections.map(([key, items]) => (
        <NarrativeCollection items={items} key={key} label={key} referenceIndex={referenceIndex} />
      ))}
    </section>
  );
}

function NarrativeView({ selectedRun, selectedSummary }) {
  const dashboardContent = selectedRun?.narrative?.dashboard_content;
  const claims = selectedRun?.narrative?.claims || [];
  const referenceIndex = selectedRun?.referenceIndex || {};
  const sectionEntries = dashboardContent ? Object.entries(dashboardContent) : [];

  return (
    <section className="narrativeView" aria-labelledby="narrative-heading">
      <div className="narrativeIntro">
        <div>
          <p className="eyebrow">Narrative</p>
          <h2 id="narrative-heading">Raw scored dashboard content</h2>
          <p>
            Rendered from analysis_runs.raw_scored_json.dashboard_content and analysis_runs.raw_scored_json.claims for {selectedSummary.company}.
          </p>
        </div>
        <Pill tone={sectionEntries.length ? "ink" : "amber"}>
          {sectionEntries.length ? `${sectionEntries.length} sections` : "No narrative"}
        </Pill>
      </div>

      {sectionEntries.length ? (
        <div className="narrativeStack">
          {sectionEntries.map(([key, section]) => (
            <NarrativeSection key={key} section={section} sectionKey={key} referenceIndex={referenceIndex} />
          ))}

          <section className="narrativeBlock claimsBlock">
            <div className="narrativeBlockHead">
              <p className="eyebrow">Claims</p>
              <h2>Claims register</h2>
              <p>{claims.length} claims are linked back to evidence and sources in the raw scored JSON.</p>
            </div>
            <div className="claimsGrid">
              {claims.map((claim) => (
                <div className="claimRow" key={claim.claim_id}>
                  <span>
                    <strong>{claim.claim_id}</strong>
                    <small>{claim.section} · {claim.claim_type} · {claim.confidence}</small>
                  </span>
                  <p>{claim.text}</p>
                  <NarrativeRefs item={claim} referenceIndex={referenceIndex} />
                </div>
              ))}
            </div>
          </section>
        </div>
      ) : (
        <div className="narrativeEmpty">
          <BookOpenText size={24} />
          <span>This run has no dashboard_content or claims inside raw_scored_json.</span>
        </div>
      )}
    </section>
  );
}

export default function DashboardClient({ data }) {
  const [selectedRunUid, setSelectedRunUid] = useState(data.runs[0]?.run_uid);
  const [viewMode, setViewMode] = useState("storage");
  const selectedRun = data.runDetails[selectedRunUid];
  const selectedSummary = selectedRun?.summary || data.runs[0];
  const lastUpdated = new Intl.DateTimeFormat("en-US", {
    dateStyle: "medium",
    timeStyle: "short"
  }).format(new Date(data.generatedAt));

  return (
    <main className="appShell">
      <aside className="sideRail">
        <div className="brandMark">
          <Database size={22} />
          <span>Storage Console</span>
        </div>
        <nav aria-label="Workspace">
          <a href="#runs-heading" onClick={() => setViewMode("storage")}><LineChart size={17} /> Runs</a>
          <a href="#selected-heading" onClick={() => setViewMode("storage")}><Activity size={17} /> Analysis</a>
          <a href="#evidence-heading" onClick={() => setViewMode("storage")}><Library size={17} /> Evidence</a>
          <a href="#schema-heading" onClick={() => setViewMode("storage")}><ShieldCheck size={17} /> Schema</a>
          <a href="#narrative-heading" onClick={() => setViewMode("storage")}><BookOpenText size={17} /> Narrative</a>
          <a href="#dashboard-heading" onClick={() => setViewMode("dashboard")}><Gauge size={17} /> Dashboard</a>
        </nav>
        <div className="railFooter">
          <span>Last sync</span>
          <strong>{lastUpdated}</strong>
        </div>
      </aside>

      <div className="mainSurface">
        <header className="topBar">
          <div>
            <p className="eyebrow">SQLite · Next.js</p>
            <h1>Company analysis storage</h1>
          </div>
          <div className="topActions">
            <ViewSwitcher viewMode={viewMode} onChange={setViewMode} />
            <a className="apiLink" href="/api/runs" title="Open Next.js API route">
              API route
              <ArrowUpRight size={16} />
            </a>
          </div>
        </header>

        {viewMode === "storage" ? (
          <>
            <section className="overviewBand" aria-label="Storage overview">
              <div className="overviewText">
                <p className="eyebrow">Operational view</p>
                <h2>Runs, evidence, and schema drift in one workspace.</h2>
                <p>Data is read directly from storage_js.db; raw JSON remains preserved for audit and future schema migration.</p>
              </div>
              <SystemMap status={data.status} />
            </section>

            <section className="statusStrip" aria-label="Database status">
              <StatLine icon={BadgeCheck} label="Companies" value={data.status.companies} />
              <StatLine icon={Layers3} label="Metrics" value={data.status.analysis_metrics} />
              <StatLine icon={Library} label="Evidence" value={data.status.evidence_items} />
              <StatLine icon={ShieldCheck} label="Schema events" value={data.status.json_ingestion_events} />
            </section>

            <div className="workspaceGrid">
              <RunList runs={data.runs} selectedRunUid={selectedRunUid} onSelect={setSelectedRunUid} />
              {selectedRun && <SelectedRun selectedRun={selectedRun} selectedSummary={selectedSummary} />}
              {selectedRun && <EvidenceInspector evidence={selectedRun.evidence} metricEvidence={selectedRun.metricEvidence} />}
              <SchemaHealth observations={data.schemaObservations} />
            </div>
            {selectedRun && <NarrativeView selectedRun={selectedRun} selectedSummary={selectedSummary} />}
          </>
        ) : (
          <div className="dashboardWorkspace">
            <RunList runs={data.runs} selectedRunUid={selectedRunUid} onSelect={setSelectedRunUid} />
            {selectedRun && <CompanyDashboard selectedRun={selectedRun} selectedSummary={selectedSummary} />}
          </div>
        )}
      </div>
    </main>
  );
}
