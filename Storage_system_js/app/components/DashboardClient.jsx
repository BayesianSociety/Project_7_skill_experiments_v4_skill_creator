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

function NarrativeRefs({ item }) {
  const refs = [
    ["Claims", item.claim_ids],
    ["Evidence", item.evidence_ids],
    ["Sources", item.source_ids]
  ].filter(([, values]) => Array.isArray(values) && values.length);

  if (!refs.length) return null;

  return (
    <div className="narrativeRefs">
      {refs.map(([label, values]) => (
        <span key={label}>
          <b>{label}</b> {values.join(", ")}
        </span>
      ))}
    </div>
  );
}

function NarrativeTextBlock({ item }) {
  const heading = item.title || item.name || item.label || item.condition || item.frequency || item.period;
  const body = item.text || item.summary || item.description || item.signal || item.interpretation || item.monitoring_source;
  const meta = [item.maturity, item.severity, item.layer, item.claim_type, item.confidence, item.value].filter(Boolean).join(" · ");

  return (
    <div className="narrativeItem">
      {heading && <h4>{heading}</h4>}
      {body && <p>{body}</p>}
      {meta && <small>{meta}</small>}
      <NarrativeRefs item={item} />
    </div>
  );
}

function NarrativeChart({ chart }) {
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
    </div>
  );
}

function NarrativeCollection({ label, items }) {
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
            return <NarrativeChart chart={item} key={item.chart_id || item.title || `${label}-${index}`} />;
          }
          return <NarrativeTextBlock item={item} key={item.red_flag_id || item.claim_id || item.name || item.title || item.label || `${label}-${index}`} />;
        })}
      </div>
    </div>
  );
}

function NarrativeSection({ sectionKey, section }) {
  if (!section) return null;

  if (Array.isArray(section)) {
    return (
      <section className="narrativeBlock">
        <div className="narrativeBlockHead">
          <p className="eyebrow">{titleFromKey(sectionKey)}</p>
          <h2>{titleFromKey(sectionKey)}</h2>
        </div>
        <NarrativeCollection label={sectionKey} items={section} />
      </section>
    );
  }

  const reserved = new Set(["title", "headline", "summary", "subheadline", "text", "verdict_label", "evidence_ids", "source_ids", "claim_ids"]);
  const collections = Object.entries(section).filter(([, value]) => Array.isArray(value));
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
        <NarrativeRefs item={section} />
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
        <NarrativeCollection items={items} key={key} label={key} />
      ))}
    </section>
  );
}

function NarrativeView({ selectedRun, selectedSummary }) {
  const dashboardContent = selectedRun?.narrative?.dashboard_content;
  const claims = selectedRun?.narrative?.claims || [];
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
            <NarrativeSection key={key} section={section} sectionKey={key} />
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
                  <NarrativeRefs item={claim} />
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
          <a href="#runs-heading"><LineChart size={17} /> Runs</a>
          <a href="#selected-heading"><Activity size={17} /> Analysis</a>
          <a href="#evidence-heading"><Library size={17} /> Evidence</a>
          <a href="#schema-heading"><ShieldCheck size={17} /> Schema</a>
          <a href="#narrative-heading"><BookOpenText size={17} /> Narrative</a>
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
          <a className="apiLink" href="/api/runs" title="Open Next.js API route">
            API route
            <ArrowUpRight size={16} />
          </a>
        </header>

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
      </div>
    </main>
  );
}
