const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const dataPath = path.join(root, "public", "data", "paypal_holdings_inc_scored.json");
const outPath = path.join(root, "public", "paypal_holdings_inc_dashboard.html");
const data = JSON.parse(fs.readFileSync(dataPath, "utf8"));

const escapeHtml = (value) =>
  String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");

const json = JSON.stringify(data).replaceAll("<", "\\u003c");

const html = `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${escapeHtml(data.company)} Innovation Dashboard</title>
  <style>
    :root {
      --dusty-rose: #d4a5a5;
      --clay: #b87d6d;
      --sand: #e8d5c4;
      --burgundy: #5d2e46;
      --paper: #fff9f5;
      --surface: #f7ece7;
      --ink: #241b20;
      --muted: #705f62;
      --line: rgba(93, 46, 70, 0.16);
      --line-strong: rgba(93, 46, 70, 0.32);
      --green: #2f7a69;
      --amber: #966a25;
      --red: #9a3b3f;
      --max: 1480px;
      --body: "FreeSans", "Helvetica Neue", Arial, sans-serif;
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      min-height: 100vh;
      color: var(--ink);
      font-family: var(--body);
      background:
        linear-gradient(90deg, rgba(93, 46, 70, 0.045) 1px, transparent 1px),
        linear-gradient(0deg, rgba(93, 46, 70, 0.035) 1px, transparent 1px),
        linear-gradient(180deg, #fffaf6 0%, #f6e8df 55%, #ead2c8 100%);
      background-size: 64px 64px, 64px 64px, auto;
      overflow-x: hidden;
    }
    a { color: var(--burgundy); text-underline-offset: 0.16em; }
    .shell { width: min(calc(100% - 28px), var(--max)); margin: 0 auto; padding: 18px 0 54px; }
    .topbar {
      display: flex; justify-content: space-between; gap: 16px; align-items: center;
      padding: 8px 2px 18px; color: var(--muted); font-size: 0.9rem;
    }
    .topbar strong { color: var(--burgundy); }
    .app {
      overflow: hidden; border: 1px solid var(--line); border-radius: 8px;
      background: rgba(255, 249, 245, 0.92);
      box-shadow: 0 28px 80px rgba(93, 46, 70, 0.12);
    }
    .header {
      display: grid; grid-template-columns: minmax(0, 1fr) 360px; gap: 26px;
      padding: 30px; border-bottom: 1px solid var(--line);
      background:
        radial-gradient(circle at 88% 14%, rgba(184, 125, 109, 0.2), transparent 34%),
        linear-gradient(135deg, rgba(212, 165, 165, 0.28), transparent 42%),
        linear-gradient(180deg, rgba(255, 249, 245, 0.98), rgba(247, 236, 231, 0.86));
      animation: rise 600ms ease both;
    }
    .kicker { color: var(--muted); font-size: 11px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; }
    h1, h2, h3 { margin: 0; color: var(--burgundy); font-weight: 700; letter-spacing: 0; }
    h1 { margin-top: 8px; max-width: 14ch; font-size: clamp(2.25rem, 4.4vw, 5rem); line-height: 0.96; }
    h2 { margin-bottom: 10px; font-size: clamp(1.22rem, 2vw, 1.72rem); line-height: 1.08; }
    h3 { margin-bottom: 8px; font-size: 1rem; line-height: 1.2; }
    p { margin: 0; color: var(--muted); line-height: 1.58; }
    .summary { max-width: 82ch; margin-top: 14px; font-size: 1rem; }
    .score-panel { display: grid; gap: 18px; align-content: start; border-left: 1px solid var(--line); padding-left: 24px; }
    .score-ring {
      --p: 68.8%;
      width: 184px; aspect-ratio: 1; display: grid; place-items: center; justify-self: end;
      border-radius: 50%;
      background: radial-gradient(circle at center, var(--paper) 58%, transparent 60%),
        conic-gradient(var(--clay) var(--p), rgba(93, 46, 70, 0.11) 0);
      box-shadow: inset 0 0 0 1px rgba(93, 46, 70, 0.12), 0 12px 36px rgba(93, 46, 70, 0.12);
      animation: settle 700ms ease both;
    }
    .score-ring strong { display: block; color: var(--burgundy); font-size: 2.8rem; line-height: 1; text-align: center; }
    .score-ring span { display: block; margin-top: 4px; color: var(--muted); font-size: 0.78rem; text-align: center; }
    .badge-row { display: flex; flex-wrap: wrap; gap: 8px; }
    .badge {
      display: inline-flex; align-items: center; min-height: 30px; width: fit-content;
      padding: 7px 10px; border: 1px solid rgba(93, 46, 70, 0.15); border-radius: 6px;
      background: rgba(212, 165, 165, 0.28); color: var(--burgundy); font-size: 0.81rem; font-weight: 700;
    }
    .badge.good { background: rgba(47, 122, 105, 0.13); color: #254c43; border-color: rgba(47, 122, 105, 0.25); }
    .badge.warn { background: rgba(150, 106, 37, 0.13); color: #674817; border-color: rgba(150, 106, 37, 0.24); }
    .content { display: grid; grid-template-columns: minmax(0, 1fr) 370px; gap: 0; }
    .main { padding: 30px; }
    .side { border-left: 1px solid var(--line); padding: 30px 24px; background: rgba(247, 236, 231, 0.48); }
    section { padding: 26px 0; border-bottom: 1px solid var(--line); opacity: 0; transform: translateY(14px); transition: opacity 520ms ease, transform 520ms ease; }
    section.visible { opacity: 1; transform: translateY(0); }
    section:first-child { padding-top: 0; }
    section:last-child { border-bottom: 0; }
    .split { display: grid; grid-template-columns: 0.9fr 1.1fr; gap: 26px; align-items: start; }
    .stack { display: grid; gap: 14px; }
    .list { display: grid; gap: 12px; margin: 0; padding: 0; list-style: none; }
    .list li { padding-left: 14px; border-left: 3px solid var(--dusty-rose); color: var(--ink); line-height: 1.48; }
    .tech-grid { display: grid; gap: 12px; }
    .tech-item, .evidence-item, .risk-item, .source-item {
      border-top: 1px solid var(--line);
      padding-top: 12px;
    }
    .tech-item p, .evidence-item p, .risk-item p { font-size: 0.93rem; }
    .meta { color: var(--muted); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 700; }
    .layers { display: grid; gap: 16px; }
    .layer {
      padding: 16px 0 18px; border-top: 1px solid var(--line);
      transition: background 180ms ease, transform 180ms ease;
    }
    .layer:hover { transform: translateX(4px); }
    .bar-head { display: flex; justify-content: space-between; align-items: baseline; gap: 12px; margin-bottom: 8px; }
    .bar-head b { color: var(--burgundy); }
    .bar-head span { color: var(--ink); font-weight: 700; font-variant-numeric: tabular-nums; }
    .bar-track { height: 8px; overflow: hidden; border-radius: 999px; background: rgba(93, 46, 70, 0.12); }
    .bar-fill {
      height: 100%; width: var(--w); border-radius: inherit;
      background: linear-gradient(90deg, var(--clay), var(--burgundy));
      box-shadow: 0 0 16px rgba(184, 125, 109, 0.35);
      transform-origin: left; animation: grow 900ms ease both;
    }
    .layer-body { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 12px; }
    .small-label { display: block; margin-bottom: 4px; color: var(--burgundy); font-size: 0.76rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; }
    .chart { display: grid; gap: 10px; margin-top: 14px; }
    .chart-row { display: grid; grid-template-columns: 74px minmax(0, 1fr) 84px; gap: 10px; align-items: center; font-size: 0.86rem; color: var(--muted); }
    .chart-row .track { height: 9px; background: rgba(93, 46, 70, 0.11); border-radius: 999px; overflow: hidden; }
    .chart-row .fill { height: 100%; width: var(--w); background: var(--clay); border-radius: inherit; }
    .snapshot { display: grid; gap: 10px; }
    .metric { display: flex; justify-content: space-between; gap: 14px; padding: 10px 0; border-bottom: 1px solid var(--line); }
    .metric span { color: var(--muted); font-size: 0.86rem; }
    .metric b { color: var(--burgundy); font-variant-numeric: tabular-nums; }
    .risk-item { border-color: rgba(154, 59, 63, 0.2); }
    .risk-item .severity { color: var(--red); font-weight: 700; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.08em; }
    .source-list { display: grid; gap: 10px; max-height: 470px; overflow: auto; padding-right: 6px; }
    .source-item a { font-weight: 700; }
    .source-item p { font-size: 0.82rem; }
    .note { color: var(--muted); font-size: 0.9rem; line-height: 1.5; }
    @keyframes rise { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes settle { from { transform: scale(0.96); opacity: 0; } to { transform: scale(1); opacity: 1; } }
    @keyframes grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }
    @media (max-width: 980px) {
      .header, .content, .split, .layer-body { grid-template-columns: 1fr; }
      .score-panel, .side { border-left: 0; padding-left: 0; }
      .score-ring { justify-self: start; width: 152px; }
      .main, .side, .header { padding: 22px; }
      h1 { max-width: 11ch; }
    }
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after { animation: none !important; transition: none !important; scroll-behavior: auto !important; }
      section { opacity: 1; transform: none; }
    }
  </style>
</head>
<body>
  <script id="score-data" type="application/json">${json}</script>
  <div class="shell">
    <div class="topbar">
      <div><strong id="topCompany"></strong> <span id="topTicker"></span></div>
      <div id="topDate"></div>
    </div>
    <div class="app">
      <header class="header">
        <div>
          <div class="kicker">Innovation Readiness Dashboard</div>
          <h1 id="headline"></h1>
          <p class="summary" id="subheadline"></p>
          <div class="badge-row" id="heroBadges" style="margin-top:18px"></div>
        </div>
        <aside class="score-panel">
          <div class="score-ring" id="scoreRing"><div><strong id="scoreValue"></strong><span>out of 25</span></div></div>
          <div class="stack">
            <div class="meta">Deterministic Verdict</div>
            <h2 id="verdict"></h2>
            <p class="note" id="gate"></p>
          </div>
        </aside>
      </header>
      <div class="content">
        <main class="main">
          <section id="thesis"></section>
          <section id="layers"></section>
          <section id="technology"></section>
          <section id="quant"></section>
          <section id="commercial"></section>
          <section id="gateSection"></section>
          <section id="research"></section>
          <section id="patents"></section>
          <section id="risks"></section>
          <section id="watchlist"></section>
          <section id="bottom"></section>
          <section id="sources"></section>
        </main>
        <aside class="side">
          <section class="visible" id="snapshot"></section>
          <section class="visible" id="method"></section>
        </aside>
      </div>
    </div>
  </div>
  <script>
    const data = JSON.parse(document.getElementById("score-data").textContent);
    const dc = data.dashboard_content;
    const el = (id) => document.getElementById(id);
    const html = (strings, ...vals) => strings.map((s, i) => s + (vals[i] ?? "")).join("");
    const esc = (value) => String(value ?? "").replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;");
    const pct = (value, max = 5) => Math.max(0, Math.min(100, (Number(value) / max) * 100));
    const list = (items) => '<ul class="list">' + items.map((item) => '<li>' + esc(item.text || item.condition || item) + '</li>').join("") + '</ul>';

    el("topCompany").textContent = data.company;
    el("topTicker").textContent = data.ticker;
    el("topDate").textContent = "Research date: " + data.research_run.research_date;
    el("headline").textContent = dc.hero.headline;
    el("subheadline").textContent = dc.hero.subheadline;
    el("scoreValue").textContent = data.display_total_score;
    el("scoreRing").style.setProperty("--p", (data.total_score / 25 * 100).toFixed(1) + "%");
    el("verdict").textContent = data.verdict;
    el("gate").textContent = data.gate_pass ? "Breakthrough commercialization gate passes; interpretation remains constrained by Science and IP evidence." : "Breakthrough commercialization gate does not pass.";
    el("heroBadges").innerHTML = [
      '<span class="badge good">Gate: ' + (data.gate_pass ? 'Pass' : 'Fail') + '</span>',
      '<span class="badge">Mode: ' + esc(data.mode) + '</span>',
      '<span class="badge warn">Readiness: ' + esc(data.display_total_score) + ' / 25</span>'
    ].join("");

    el("thesis").innerHTML = html\`
      <div class="split">
        <div><h2>\${esc(dc.thesis.title)}</h2><p>\${esc(dc.thesis.summary)}</p></div>
        <div>\${list(dc.thesis.bullets)}</div>
      </div>\`;

    el("layers").innerHTML = '<h2>Five-Layer Score</h2><div class="layers">' + data.layers.map(layer => html\`
      <article class="layer">
        <div class="bar-head"><b>\${esc(layer.label)}</b><span>\${esc(layer.display_score)} / 5</span></div>
        <div class="bar-track"><div class="bar-fill" style="--w:\${pct(layer.score).toFixed(1)}%"></div></div>
        <div class="layer-body">
          <p><span class="small-label">Evidence</span>\${esc(layer.summary)}</p>
          <p><span class="small-label">Strong</span>\${esc(layer.strong)}</p>
          <p><span class="small-label">Missing</span>\${esc(layer.missing)}</p>
          <p><span class="small-label">Confidence</span>\${esc(layer.confidence)}; coverage \${Math.round(layer.coverage_ratio * 100)}%</p>
        </div>
      </article>\`).join("") + '</div>';

    el("technology").innerHTML = '<h2>' + esc(dc.technology_map.title) + '</h2><p>' + esc(dc.technology_map.summary) + '</p><div class="tech-grid" style="margin-top:16px">' +
      dc.technology_map.items.map(item => html\`<article class="tech-item"><div class="meta">\${esc(item.maturity)}</div><h3>\${esc(item.name)}</h3><p>\${esc(item.description)}</p></article>\`).join("") + '</div>';

    const chartHtml = (chart) => {
      const all = chart.series.flatMap(s => s.points.map(p => p.value));
      const max = Math.max(...all);
      return html\`<article class="evidence-item"><h3>\${esc(chart.title)}</h3><p>\${esc(chart.description)}</p><div class="chart">\${chart.series.map(series =>
        series.points.map(point => html\`<div class="chart-row"><span>\${esc(point.period)}</span><div class="track"><div class="fill" style="--w:\${(point.value / max * 100).toFixed(1)}%"></div></div><b>\${esc(point.value)} \${esc(series.unit.replace("USD ", ""))}</b></div>\`).join("")
      ).join("")}</div></article>\`;
    };
    el("quant").innerHTML = '<h2>' + esc(dc.quantitative_signals.title) + '</h2><p>' + esc(dc.quantitative_signals.summary) + '</p><div class="stack" style="margin-top:14px">' + dc.quantitative_signals.charts.map(chartHtml).join("") + '</div>';

    el("commercial").innerHTML = '<h2>' + esc(dc.commercialization_evidence.title) + '</h2><p>' + esc(dc.commercialization_evidence.summary) + '</p><div class="stack" style="margin-top:14px">' +
      dc.commercialization_evidence.items.map(item => html\`<article class="evidence-item"><div class="meta">\${esc(item.label)}</div><p>\${esc(item.text)}</p></article>\`).join("") + '</div>';

    el("gateSection").innerHTML = html\`<h2>\${esc(dc.breakthrough_gate.title)}</h2><p>\${esc(dc.breakthrough_gate.summary)}</p>
      <div class="split" style="margin-top:16px"><div><h3>Conditions Met</h3>\${list(dc.breakthrough_gate.conditions_met)}</div><div><h3>Conditions Not Met</h3>\${list(dc.breakthrough_gate.conditions_not_met)}</div></div>\`;

    el("research").innerHTML = '<h2>' + esc(dc.university_research_signals.title) + '</h2><p>' + esc(dc.university_research_signals.summary) + '</p><div class="stack" style="margin-top:14px">' +
      dc.university_research_signals.institutions.map(item => html\`<article class="evidence-item"><h3>\${esc(item.name)}</h3><p>\${esc(item.signal)}</p></article>\`).join("") + '</div>';

    el("patents").innerHTML = '<h2>' + esc(dc.patent_signals.title) + '</h2><p>' + esc(dc.patent_signals.summary) + '</p><div class="stack" style="margin-top:14px">' +
      dc.patent_signals.families.map(item => html\`<article class="evidence-item"><div class="meta">\${esc(item.publication_or_family_id)} | \${esc(item.jurisdictions.join(", "))}</div><h3>\${esc(item.title)}</h3><p>\${esc(item.interpretation)}</p></article>\`).join("") +
      '</div><p class="note" style="margin-top:12px">' + esc(dc.patent_signals.interpretation) + '</p>';

    el("risks").innerHTML = '<h2>Red Flags</h2><div class="stack">' + dc.red_flags.map(risk => html\`
      <article class="risk-item"><div class="severity">\${esc(risk.severity)} | \${esc(risk.layer)}</div><h3>\${esc(risk.title)}</h3><p>\${esc(risk.text)}</p></article>\`).join("") + '</div>';

    el("watchlist").innerHTML = html\`<h2>\${esc(dc.watchlist.title)}</h2><div class="split"><div><h3>Upgrade Signals</h3>\${list(dc.watchlist.upgrade_signals)}</div><div><h3>Downgrade Signals</h3>\${list(dc.watchlist.downgrade_signals)}</div></div>\`;
    el("bottom").innerHTML = '<h2>' + esc(dc.bottom_line.title) + '</h2><p>' + esc(dc.bottom_line.text) + '</p>';

    el("snapshot").innerHTML = '<h2>' + esc(dc.operational_snapshot.title) + '</h2><div class="snapshot">' + dc.operational_snapshot.metrics.map(metric =>
      html\`<div class="metric"><span>\${esc(metric.label)}</span><b>\${esc(metric.value)}</b></div>\`).join("") + '</div>';
    el("method").innerHTML = '<h2>' + esc(dc.method_notes.title) + '</h2>' + dc.method_notes.notes.map(note => '<p class="note" style="margin-bottom:10px">' + esc(note) + '</p>').join("");

    el("sources").innerHTML = '<h2>Sources</h2><div class="source-list">' + data.sources.map(source => html\`
      <article class="source-item"><a href="\${esc(source.url)}">\${esc(source.title)}</a><p>\${esc(source.publisher)} | \${esc(source.document_date)} | \${esc(source.source_type)}</p></article>\`).join("") + '</div>';

    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => { if (entry.isIntersecting) entry.target.classList.add("visible"); });
    }, { threshold: 0.08 });
    document.querySelectorAll("main section").forEach(section => observer.observe(section));
  </script>
</body>
</html>
`;

fs.writeFileSync(outPath, html, "utf8");
console.log(outPath);
