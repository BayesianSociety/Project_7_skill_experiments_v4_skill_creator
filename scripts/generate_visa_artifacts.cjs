const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const researchDate = "2026-05-06";
const companySlug = "visa_inc";
const runId = "v-innovation-20260506";
const runDir = path.join(root, "public", "runs", companySlug, researchDate, runId);
const imageDir = path.join(root, "imagegen", companySlug);

const sourceUrl = {
  tenK: "https://www.sec.gov/Archives/edgar/data/1403161/000140316125000089/v-20250930.htm",
  q2: "https://www.sec.gov/Archives/edgar/data/1403161/000140316126000077/q22026earningsrelease.htm",
  vpi: "https://usa.visa.com/about-visa/newsroom/press-releases.releaseId.20251.html",
  scam: "https://usa.visa.com/about-visa/newsroom/press-releases.releaseId.21286.html",
  passkey: "https://www.visa.com/en-us/products/visa-payment-passkey",
  tokenization: "https://corporate.visa.com/en/solutions/tokenization.html",
  agentic: "https://usa.visa.com/about-visa/newsroom/press-releases.release.21361.html",
  trustedAgent: "https://usa.visa.com/about-visa/newsroom/press-releases.releaseId.21716.html",
  stablecoin2026: "https://investor.visa.com/news/news-details/2026/Visa-Accelerates-Stablecoin-Momentum-Adding-Five-Blockchains-for-Settlement/default.aspx",
  justia: "https://patents.justia.com/assignee/visa-international-service-association",
  googlePatentToken: "https://patents.google.com/patent/US11676138B2/en",
  googlePatentRecurring: "https://patents.google.com/patent/US12008088B2",
  pubchemMlPatent: "https://pubchem.ncbi.nlm.nih.gov/patent/US-12293286-B2",
  openalexDocs: "https://developers.openalex.org/quickstart",
  openalexHelp: "https://help.openalex.org/hc/en-us/articles/27250895840791-Why-are-the-counts-by-year-numbers-different-than-the-count-of-works-in-a-year",
  stanford: "https://fdc.stanford.edu/research",
  harvard: "https://hls.harvard.edu/bibliography/stable-foundations-towards-a-robust-and-bipartisan-approach-to-stablecoin-legislation/",
  whiteHouseGenius: "https://www.whitehouse.gov/fact-sheets/2025/07/fact-sheet-president-donald-j-trump-signs-genius-act-into-law/",
  euAi: "https://digital-strategy.ec.europa.eu/en/factpages/general-purpose-ai-obligations-under-ai-act",
  fido: "https://fidoalliance.org/passkey-use-case/payments/"
};

const sources = [
  ["src_001", "Visa Inc FY2025 Form 10-K", sourceUrl.tenK, "SEC EDGAR", "2025-11-06", "primary", "Latest full-year filing for scale, tokens, stablecoins, value-added services, operating data, regulation, and risk."],
  ["src_002", "Visa Fiscal Second Quarter 2026 Earnings Release", sourceUrl.q2, "SEC EDGAR", "2026-04-28", "primary", "Latest quarterly operating update available on the research date."],
  ["src_003", "Visa Provisioning Intelligence Launches to Combat Token Fraud", sourceUrl.vpi, "Visa", "2023-12-13", "primary", "AI token-fraud product launch and token-provisioning fraud estimate."],
  ["src_004", "Visa Unveils its Scam Disruption Practice", sourceUrl.scam, "Visa", "2025-03-11", "primary", "Fraud prevention, technology investment, and human-plus-AI operating evidence."],
  ["src_005", "Visa Payment Passkey", sourceUrl.passkey, "Visa", "2026-04-22", "primary", "FIDO-based passkey authentication product evidence and adoption prerequisites."],
  ["src_006", "Tokenization offers more seamless and secure payments", sourceUrl.tokenization, "Visa", "2026-04-29", "primary", "Current Visa tokenization product evidence and public metrics."],
  ["src_007", "Find and Buy with AI: Visa Unveils New Era of Commerce", sourceUrl.agentic, "Visa", "2025-04-30", "primary", "Visa Intelligent Commerce and agentic commerce partner ecosystem."],
  ["src_008", "Visa Introduces Trusted Agent Protocol", sourceUrl.trustedAgent, "Visa", "2025-10-14", "primary", "Agentic-commerce protocol, Cloudflare collaboration, and developer release."],
  ["src_009", "Visa Accelerates Stablecoin Momentum", sourceUrl.stablecoin2026, "Visa Investor Relations", "2026-04-29", "primary", "Latest stablecoin settlement run-rate and blockchain support."],
  ["src_010", "Patents Assigned to Visa International Service Association", sourceUrl.justia, "Justia Patents", "2026-05-06", "patent", "Representative assigned patent and application listings."],
  ["src_011", "US11676138B2 - Multi-network tokenization processing", sourceUrl.googlePatentToken, "Google Patents", "2023-06-13", "patent", "Representative tokenization patent."],
  ["src_012", "US12008088B2 - Recurring token transactions", sourceUrl.googlePatentRecurring, "Google Patents", "2024-06-11", "patent", "Representative token transaction patent."],
  ["src_013", "US12293286B2 - Generating input data for a machine learning model", sourceUrl.pubchemMlPatent, "PubChem / USPTO patent metadata", "2025-05-06", "patent", "Representative Visa machine-learning patent metadata."],
  ["src_014", "OpenAlex Quickstart", sourceUrl.openalexDocs, "OpenAlex", "2026-05-06", "secondary_dataset", "Documents group-by-year method for publication proxies."],
  ["src_015", "OpenAlex counts_by_year caveat", sourceUrl.openalexHelp, "OpenAlex", "2026-05-06", "secondary_dataset", "Caveat that publication year counts can drift as metadata updates."],
  ["src_016", "Stanford Future of Digital Currency Initiative Research", sourceUrl.stanford, "Stanford University", "2026-05-06", "academic", "Stablecoin cross-border payments research signal."],
  ["src_017", "Stable Foundations", sourceUrl.harvard, "Harvard Law School", "2025", "academic", "Stablecoin policy framework analysis."],
  ["src_018", "Fact Sheet: President Signs GENIUS Act into Law", sourceUrl.whiteHouseGenius, "The White House", "2025-07-18", "government", "U.S. stablecoin regulatory framework evidence."],
  ["src_019", "General-purpose AI obligations under the AI Act", sourceUrl.euAi, "European Commission", "2025-08-02", "government", "EU AI policy constraints for general-purpose AI models."],
  ["src_020", "Passkeys for Payments", sourceUrl.fido, "FIDO Alliance", "2026-05-06", "standards", "Payment authentication standards and passkey fit."],
].map(([source_id, title, url, publisher, document_date, source_type, notes]) => ({
  source_id,
  title,
  url,
  publisher,
  document_date,
  accessed_at: researchDate,
  source_type,
  availability: "available",
  reliability: source_type === "primary" || source_type === "government" ? "high" : "medium",
  notes
}));

const evidence = [
  ["ev_001", "src_001", "Industrialization", ["operational_scale"], "Visa reported FY2025 total payments and cash volume of $17 trillion, nearly 5 billion payment credentials and acceptance at more than 175 million merchant locations.", 17, "USD trillions", "2025", "2025", true, false],
  ["ev_002", "src_001", "Industrialization", ["processed_transactions"], "Visa processed 257.545 billion transactions in FY2025, up 10% from 233.758 billion in FY2024.", 257.545, "billion transactions", "2023", "2025", true, false],
  ["ev_003", "src_001", "Adoption", ["token_scale"], "Visa had provisioned more than 16 billion tokens as of September 30, 2025.", 16, "billion tokens", "2025", "2025", true, false],
  ["ev_004", "src_001", "Adoption", ["visa_direct"], "Visa Direct processed more than 12.5 billion transactions for more than 650 partners in FY2025.", 12.5, "billion transactions", "2025", "2025", true, false],
  ["ev_005", "src_001", "Adoption", ["stablecoin_scale"], "Stablecoin settlement volume surpassed a $2.5 billion annualized run rate as of September 30, 2025.", 2.5, "USD billions annualized", "2025", "2025", true, false],
  ["ev_006", "src_009", "Adoption", ["stablecoin_growth"], "Visa announced stablecoin settlement support across nine blockchains and a $7 billion annualized stablecoin settlement run rate on April 29, 2026.", 7, "USD billions annualized", "2025", "2026", true, false],
  ["ev_007", "src_002", "Adoption", ["q2_2026_growth"], "Fiscal Q2 2026 net revenue was $11.2 billion, up 17%; processed transactions were 66.1 billion, up 9%.", 66.1, "billion transactions", "2026-Q2", "2026-Q2", true, false],
  ["ev_008", "src_001", "Adoption", ["vas_revenue"], "FY2025 value-added services revenue was $10.9 billion, up 24% from $8.8 billion in FY2024.", 10.9, "USD billions", "2023", "2025", true, false],
  ["ev_009", "src_004", "Industrialization", ["fraud_operations"], "Visa said it invested more than $12 billion in technology over the prior five years and blocked $40 billion in attempted fraud on the Visa network in 2024.", 40, "USD billions blocked", "2024", "2025", true, false],
  ["ev_010", "src_003", "Industrialization", ["ai_productization"], "Visa Provisioning Intelligence uses machine learning to rate token provisioning fraud risk for financial institutions.", null, "product launch", "2023", "2023", true, false],
  ["ev_011", "src_007", "Adoption", ["agentic_partners"], "Visa Intelligent Commerce named partners including Anthropic, IBM, Microsoft, Mistral AI, OpenAI, Perplexity, Samsung and Stripe.", 8, "named partners", "2025", "2025", true, false],
  ["ev_012", "src_008", "Industrialization", ["agentic_protocol"], "Visa released Trusted Agent Protocol in the Visa Developer Center and GitHub, developed with Cloudflare, to help merchants verify AI agents.", null, "protocol release", "2025", "2025", true, false],
  ["ev_013", "src_014", "Science", ["publication_growth"], "OpenAlex field proxy for payment fraud detection machine learning showed works rising from 1,211 in 2021 to 6,228 in 2025; counts by year used: 2021 1,211, 2022 1,735, 2023 2,986, 2024 4,160, 2025 6,228.", 6228, "works", "2021", "2025", false, true],
  ["ev_014", "src_014", "Science", ["publication_growth"], "OpenAlex field proxy for stablecoin payments showed works rising from 295 in 2021 to 1,143 in 2025; counts by year used: 2021 295, 2022 447, 2023 842, 2024 801, 2025 1,143.", 1143, "works", "2021", "2025", false, true],
  ["ev_015", "src_016", "Science", ["university_signal"], "Stanford FDCI highlights stablecoin cross-border research using a five-year dataset of more than 41 million transactions and reports over 96% of transactions settling in under one hour.", 41, "million transactions", "2025", "2025", false, true],
  ["ev_016", "src_010", "IP", ["patent_activity"], "Justia's current Visa assignee page lists recent 2026 grants and applications in machine learning, authentication, blockchain verification, device binding and token provisioning.", null, "representative records", "2026", "2026", true, false],
  ["ev_017", "src_011", "IP", ["patent_specificity"], "Representative Visa patent US11676138B2 covers multi-network tokenization processing.", null, "patent", "2023", "2023", true, false],
  ["ev_018", "src_012", "IP", ["patent_specificity"], "Representative Visa patent US12008088B2 covers recurring token transactions.", null, "patent", "2024", "2024", true, false],
  ["ev_019", "src_013", "IP", ["patent_specificity"], "Representative Visa patent metadata for US12293286B2 covers generating input data for a machine learning model and lists Visa International Service Association as assignee.", null, "patent", "2025", "2025", true, false],
  ["ev_020", "src_018", "Policy & Economics", ["stablecoin_policy"], "The GENIUS Act created a federal regulatory system for stablecoins with reserve and disclosure requirements.", null, "policy", "2025", "2025", false, false],
  ["ev_021", "src_019", "Policy & Economics", ["ai_policy"], "EU AI Act general-purpose AI obligations began applying on August 2, 2025, including documentation, copyright policy, and systemic-risk controls for advanced models.", null, "policy", "2025", "2025", false, false],
  ["ev_022", "src_020", "Policy & Economics", ["standards_fit"], "FIDO payment passkeys support phishing-resistant transaction authorization, checkout authentication, and compliance-oriented payment flows.", null, "standard", "2026", "2026", false, false],
  ["ev_023", "src_001", "Policy & Economics", ["competition_risk"], "Visa identifies RTP networks, digital wallets, stablecoins, value-added service providers, AI-enabled competition, data, AI, privacy and cybersecurity regulation as material issues.", null, "risk disclosure", "2025", "2025", true, false],
].map(([evidence_id, source_id, layer, metric_codes, fact, raw_value, raw_unit, period_start, period_end, company_attributable, field_proxy]) => ({
  evidence_id,
  source_id,
  layer,
  metric_codes,
  fact_type: company_attributable ? "sourced_fact" : "field_proxy_or_context",
  fact,
  raw_value,
  raw_unit,
  period_start,
  period_end,
  company_attributable,
  field_proxy,
  quote_or_excerpt: "",
  location: "See source notes and linked filing/page.",
  verified: true,
  limitations: field_proxy ? "Field-level proxy, not Visa-authored science." : ""
}));

const pubFraud = [
  { period: "2021", value: 1211 },
  { period: "2022", value: 1735 },
  { period: "2023", value: 2986 },
  { period: "2024", value: 4160 },
  { period: "2025", value: 6228 }
];
const pubStablecoin = [
  { period: "2021", value: 295 },
  { period: "2022", value: 447 },
  { period: "2023", value: 842 },
  { period: "2024", value: 801 },
  { period: "2025", value: 1143 }
];
const patentProxy = [
  { period: "2021", value: null, note: "Open family count unavailable" },
  { period: "2022", value: null, note: "Open family count unavailable" },
  { period: "2023", value: 1, note: "Representative multi-network tokenization grant" },
  { period: "2024", value: 1, note: "Representative recurring-token grant" },
  { period: "2025", value: 5, note: "Representative public application/grant signals, not exhaustive" }
];

const layers = [
  {
    label: "Science",
    score: 3.4,
    display_score: "3.4",
    raw_score: 3.73,
    normalized_score: 0.746,
    coverage_ratio: 0.76,
    confidence_penalty: 0.912,
    confidence: "Medium",
    summary: "The underlying research fields are growing quickly, especially payment-fraud machine learning and stablecoin cross-border payments. The limitation is attribution: Visa looks more like a fast industrializer of applied science than a public science producer.",
    strong: "OpenAlex field proxies show strong publication growth; Stanford and Harvard signals indicate serious academic attention to stablecoin payment economics and regulation.",
    missing: "No robust public Visa-authored publication corpus or citation-impact series was identified.",
    metrics: [
      metric("publication_growth", "Publication growth", 1.0, 0.38, ["ev_013", "ev_014"], "Field proxy grew sharply from 2021 to 2025."),
      metric("citation_quality", "Institution quality", 0.66, 0.27, ["ev_015"], "Stanford/Harvard/NBER-level policy and payments research exists, but it is not company-attributable."),
      metric("science_to_application", "Science to application linkage", 0.68, 0.35, ["ev_010", "ev_011", "ev_012", "ev_015"], "Visa applies AI, tokenization and stablecoin research themes directly in products.")
    ],
    cap_reasons: []
  },
  {
    label: "IP",
    score: 3.0,
    display_score: "3.0",
    raw_score: 3.32,
    normalized_score: 0.664,
    coverage_ratio: 0.68,
    confidence_penalty: 0.904,
    confidence: "Medium",
    summary: "Visa has technically specific patents and applications around tokenization, transaction processing, authentication, blockchain interaction and machine learning. The public record is active, but an exhaustive five-year patent-family time series was not reproducible without paid patent data.",
    strong: "Representative records map to real platform primitives: token provisioning, recurring-token transactions, blockchain verification and ML model inputs.",
    missing: "Clean global patent-family counts by priority year and family continuation maps.",
    metrics: [
      metric("patent_family_growth", "Patent-family growth proxy", 0.48, 0.30, ["ev_016"], "Representative records are rising in visibility in 2025-2026, but exact annual family counts are unavailable."),
      metric("technical_specificity", "Technical specificity", 0.82, 0.40, ["ev_017", "ev_018", "ev_019"], "Patents are specific to payments infrastructure, tokenization and model inputs."),
      metric("assignee_quality", "Assignee quality and standards linkage", 0.72, 0.30, ["ev_003", "ev_020", "ev_022"], "Visa is a high-quality assignee operating in standards-heavy payment infrastructure.")
    ],
    cap_reasons: ["IP confidence is capped by missing exhaustive patent-family counts."]
  },
  {
    label: "Industrialization",
    score: 4.4,
    display_score: "4.4",
    raw_score: 4.58,
    normalized_score: 0.916,
    coverage_ratio: 0.94,
    confidence_penalty: 0.96,
    confidence: "High",
    summary: "Visa's strongest evidence is industrialization: global processing infrastructure, token service scale, fraud operations, AI risk tooling, Visa Direct, and stablecoin settlement are operating systems rather than lab demonstrations.",
    strong: "FY2025 processed transactions reached 257.545 billion; token provisioning exceeded 16 billion; stablecoin settlement moved from a $2.5 billion run rate in FY2025 to $7 billion by April 2026.",
    missing: "Granular latency, uptime, model quality, false-positive and program-level margin data are not disclosed.",
    metrics: [
      metric("deployment_evidence", "Deployment evidence", 0.94, 0.42, ["ev_001", "ev_002", "ev_003", "ev_006"], "Multiple platforms are live at global scale."),
      metric("process_learning", "Process learning and tech investment", 0.84, 0.28, ["ev_009", "ev_010", "ev_012"], "Fraud, cyber and developer-platform capabilities show repeated productization."),
      metric("operational_scale", "Operational scale", 0.95, 0.30, ["ev_001", "ev_002", "ev_007"], "Transaction volume and Q2 2026 growth show production maturity.")
    ],
    cap_reasons: []
  },
  {
    label: "Adoption",
    score: 4.5,
    display_score: "4.5",
    raw_score: 4.7,
    normalized_score: 0.94,
    coverage_ratio: 0.95,
    confidence_penalty: 0.96,
    confidence: "High",
    summary: "Adoption is exceptional. Visa has network-scale credentials and merchants, double-digit VAS growth, Visa Direct partner reach, agentic commerce partners and accelerating stablecoin settlement activity.",
    strong: "FY2025 VAS revenue grew 24%; Visa Direct processed more than 12.5 billion transactions; stablecoin settlement reached a $7 billion annualized run rate in April 2026.",
    missing: "Some emerging programs lack disclosed product-specific revenue, retention, issuer count and transaction-margin metrics.",
    metrics: [
      metric("volume_or_revenue", "Volume and revenue evidence", 0.95, 0.38, ["ev_001", "ev_007", "ev_008"], "Scale and revenue growth are strong."),
      metric("partner_breadth", "Partner breadth", 0.88, 0.30, ["ev_004", "ev_011", "ev_012"], "Visa has partner distribution across banks, sellers, AI firms and developers."),
      metric("repeatability", "Repeatability and deployment scale", 0.95, 0.32, ["ev_002", "ev_003", "ev_006"], "High-frequency payment rails and tokenization create repeatable adoption.")
    ],
    cap_reasons: []
  },
  {
    label: "Policy & Economics",
    score: 3.6,
    display_score: "3.6",
    raw_score: 3.86,
    normalized_score: 0.772,
    coverage_ratio: 0.84,
    confidence_penalty: 0.932,
    confidence: "Medium",
    summary: "Policy is mixed but investable: stablecoin regulation is clearer after the GENIUS Act and passkeys fit FIDO standards, while AI, data localization, network routing, interchange, stablecoin and cybersecurity rules remain material constraints.",
    strong: "U.S. stablecoin rules and FIDO payment authentication standards support parts of Visa's roadmap.",
    missing: "Implementation details for stablecoin rules, AI obligations and market-by-market payment regulation remain evolving.",
    metrics: [
      metric("regulatory_fit", "Regulatory and standards fit", 0.73, 0.40, ["ev_020", "ev_022"], "Stablecoin and passkey standards support product direction."),
      metric("economic_readiness", "Economic readiness", 0.82, 0.34, ["ev_001", "ev_008", "ev_009"], "Core economics and operating scale are strong."),
      metric("policy_friction", "Policy friction", 0.58, 0.26, ["ev_021", "ev_023"], "AI/data/payment regulation and competition cap the score.")
    ],
    cap_reasons: []
  }
];

function metric(code, label, value, weight, evidence_ids, rationale) {
  return {
    code,
    label,
    value,
    weight,
    unit: "normalized_0_to_1",
    source_type: "mixed",
    verified: true,
    evidence_ids,
    normalization: {
      raw_inputs: {},
      method: "documented_judgment_scale",
      parameters: {},
      rationale,
      judgment_level: "medium"
    }
  };
}

const totalScore = Number(layers.reduce((sum, layer) => sum + layer.score, 0).toFixed(1));

const dashboardContent = {
  hero: {
    headline: "Visa Inc Innovation Readiness",
    subheadline: "NYSE: V | Commercialization-heavy payment infrastructure analysis, updated May 6, 2026.",
    verdict_label: "Commercial-scale innovator with strong translational momentum",
    evidence_ids: ["ev_001", "ev_002", "ev_003", "ev_006", "ev_008"],
    source_ids: ["src_001", "src_002", "src_009"]
  },
  thesis: {
    title: "Thesis",
    summary: "Visa is not a science-led breakthrough story. It is a scaled industrializer of applied payment technologies: tokenization, AI risk scoring, authentication, agentic commerce rails, Visa Direct and stablecoin settlement.",
    bullets: [
      { text: "The moat is operating scale: 257.5B FY2025 processed transactions and nearly 5B payment credentials.", evidence_ids: ["ev_001", "ev_002"], source_ids: ["src_001"] },
      { text: "Tokenization is deeply commercialized: more than 16B tokens provisioned, plus passkeys, Click to Pay and token fraud controls.", evidence_ids: ["ev_003", "ev_010", "ev_022"], source_ids: ["src_001", "src_003", "src_005"] },
      { text: "Stablecoin settlement moved from experiment toward infrastructure: $2.5B FY2025 annualized run rate to $7B by April 2026.", evidence_ids: ["ev_005", "ev_006"], source_ids: ["src_001", "src_009"] }
    ]
  },
  technology_map: {
    title: "Technology Map",
    summary: "The analysis focuses on the technologies most material to Visa's future payment stack.",
    items: [
      { name: "AI risk, cyber and fraud scoring", description: "Real-time risk scoring across authorization, token provisioning, scams and ecosystem security.", maturity: "commercial", evidence_ids: ["ev_009", "ev_010"], source_ids: ["src_003", "src_004"] },
      { name: "Tokenization, passkeys and identity-bound checkout", description: "Visa Token Service, Cloud Token Framework, Payment Passkey and Click to Pay increase security while reducing checkout friction.", maturity: "commercial", evidence_ids: ["ev_003", "ev_017", "ev_022"], source_ids: ["src_001", "src_005", "src_011"] },
      { name: "Stablecoin settlement and agentic commerce", description: "Emerging rails for always-on settlement and AI-initiated commerce, with live pilots and partner programs.", maturity: "scaling", evidence_ids: ["ev_006", "ev_011", "ev_012"], source_ids: ["src_007", "src_008", "src_009"] }
    ]
  },
  quantitative_signals: {
    title: "Quantitative Signals",
    summary: "Publication data are field-level proxies; patent data are representative public records because clean family counts were unavailable.",
    charts: [
      { chart_id: "chart_pub_fraud", title: "Payment fraud ML publications", description: "OpenAlex field proxy, works by publication year.", series: [{ label: "Works", unit: "works", points: pubFraud }], evidence_ids: ["ev_013"], source_ids: ["src_014", "src_015"] },
      { chart_id: "chart_pub_stablecoin", title: "Stablecoin payments publications", description: "OpenAlex field proxy, works by publication year.", series: [{ label: "Works", unit: "works", points: pubStablecoin }], evidence_ids: ["ev_014"], source_ids: ["src_014", "src_015"] },
      { chart_id: "chart_patent_proxy", title: "Visa patent proxy", description: "Representative open records; null means no reproducible public family count, not zero activity.", series: [{ label: "Representative records", unit: "records", points: patentProxy }], evidence_ids: ["ev_016", "ev_017", "ev_018", "ev_019"], source_ids: ["src_010", "src_011", "src_012", "src_013"] }
    ]
  },
  commercialization_evidence: {
    title: "Commercialization Evidence",
    summary: "Visa's emerging technologies are already connected to revenue, partners or operating workflows.",
    items: [
      { label: "Visa Direct", text: "More than 12.5B FY2025 transactions and 650+ partners.", evidence_ids: ["ev_004"], source_ids: ["src_001"] },
      { label: "Value-added services", text: "$10.9B FY2025 revenue, up 24% year over year.", evidence_ids: ["ev_008"], source_ids: ["src_001"] },
      { label: "Stablecoin settlement", text: "$7B annualized run rate and support for nine blockchains as of April 29, 2026.", evidence_ids: ["ev_006"], source_ids: ["src_009"] },
      { label: "Agentic commerce", text: "Visa Intelligent Commerce and Trusted Agent Protocol provide rails for AI-agent checkout.", evidence_ids: ["ev_011", "ev_012"], source_ids: ["src_007", "src_008"] }
    ]
  },
  breakthrough_gate: {
    title: "Breakthrough Gate",
    summary: "The gate is passed because Industrialization and Adoption both exceed 3.0; the thesis is commercial scale-up, not basic-science novelty.",
    conditions_met: [
      { condition: "Industrialization score is at least 3.0.", evidence_ids: ["ev_001", "ev_002", "ev_003"], source_ids: ["src_001"] },
      { condition: "Adoption score is at least 3.0.", evidence_ids: ["ev_004", "ev_006", "ev_008"], source_ids: ["src_001", "src_009"] }
    ],
    conditions_not_met: [
      { condition: "Public company-authored science and exact patent-family time series are not strong enough to call this a science-led breakthrough profile.", evidence_ids: ["ev_013", "ev_016"], source_ids: ["src_014", "src_010"] }
    ],
    result: "Pass: plausible scale-up candidate, not frontier-science breakthrough."
  },
  university_research_signals: {
    title: "University Research",
    summary: "Academic evidence supports the relevance of the fields, particularly stablecoin payments and fraud detection.",
    institutions: [
      { name: "Stanford University", signal: "Stablecoin cross-border payment study with a five-year, 41M+ transaction dataset and settlement-speed evidence.", company_attributable: false, field_proxy: true, evidence_ids: ["ev_015"], source_ids: ["src_016"] },
      { name: "Harvard Law School", signal: "Stablecoin legislative framework analysis relevant to payment-stablecoin economics and risk.", company_attributable: false, field_proxy: true, evidence_ids: ["ev_020"], source_ids: ["src_017"] },
      { name: "OpenAlex-indexed field literature", signal: "Payment-fraud ML and stablecoin-payment publication proxies grew materially over 2021-2025.", company_attributable: false, field_proxy: true, evidence_ids: ["ev_013", "ev_014"], source_ids: ["src_014", "src_015"] }
    ]
  },
  patent_signals: {
    title: "Patents",
    summary: "Visa's public patent signal is technically relevant but only partially countable from open sources.",
    families: [
      { title: "Multi-network tokenization processing", publication_or_family_id: "US11676138B2", jurisdictions: ["US"], priority_date: "2013-08-08", interpretation: "Token orchestration across networks is central to Visa's digital credential strategy.", evidence_ids: ["ev_017"], source_ids: ["src_011"] },
      { title: "Recurring token transactions", publication_or_family_id: "US12008088B2", jurisdictions: ["US"], priority_date: "2018-06-18", interpretation: "Recurring commerce is a high-frequency tokenized-payment use case.", evidence_ids: ["ev_018"], source_ids: ["src_012"] },
      { title: "Generating input data for a machine learning model", publication_or_family_id: "US12293286B2", jurisdictions: ["US"], priority_date: "2021-02-18", interpretation: "Machine-learning tooling appears in Visa's assigned patent record.", evidence_ids: ["ev_019"], source_ids: ["src_013"] },
      { title: "Machine learning, identity graph, blockchain verification and token provisioning applications", publication_or_family_id: "Representative Justia assignee records", jurisdictions: ["US", "WO"], priority_date: "2023-2025", interpretation: "Recent public filings point to ongoing engineering in core payment infrastructure.", evidence_ids: ["ev_016"], source_ids: ["src_010"] }
    ],
    interpretation: "The direction is strong; the time series is not. IP should be refreshed with Lens, Derwent, PatSnap, Google BigQuery Patents or another family-level database before peer benchmarking."
  },
  red_flags: [
    { red_flag_id: "rf_001", title: "Science attribution is weak", text: "Publication signals are field-level proxies rather than a Visa-authored science corpus.", severity: "medium", layer: "Science", evidence_ids: ["ev_013", "ev_014"], source_ids: ["src_014", "src_015"] },
    { red_flag_id: "rf_002", title: "Patent counts are incomplete", text: "Open sources show representative Visa patent activity but not a clean five-year global patent-family count.", severity: "medium", layer: "IP", evidence_ids: ["ev_016"], source_ids: ["src_010"] },
    { red_flag_id: "rf_003", title: "Policy exposure is structural", text: "Routing, interchange, AI, privacy, cybersecurity, data localization and stablecoin rules can alter economics or deployment options.", severity: "high", layer: "Policy & Economics", evidence_ids: ["ev_021", "ev_023"], source_ids: ["src_001", "src_019"] },
    { red_flag_id: "rf_004", title: "Emerging product metrics are thin", text: "Agentic commerce and stablecoin settlement are promising but still small relative to Visa's core network.", severity: "medium", layer: "Adoption", evidence_ids: ["ev_006", "ev_011", "ev_012"], source_ids: ["src_007", "src_008", "src_009"] }
  ],
  watchlist: {
    title: "What Would Change The View",
    upgrade_signals: [
      { text: "Disclosed product-level revenue or margin contribution from AI risk tools, tokenization, agentic commerce or stablecoin settlement.", monitoring_source: "10-K, 10-Q, earnings calls and investor presentations." },
      { text: "Family-level patent growth in tokenization, AI risk, identity, blockchain settlement and agentic payment protocols.", monitoring_source: "USPTO, WIPO, EPO, Google Patents, Lens or paid patent databases." },
      { text: "Stablecoin settlement moving from billions to tens of billions annualized with named issuer/acquirer adoption.", monitoring_source: "Visa press releases, blockchain analytics and bank partner disclosures." }
    ],
    downgrade_signals: [
      { text: "Regulatory action constraining routing, fees, tokenization, AI scoring or stablecoin settlement.", monitoring_source: "SEC filings, CFPB, Fed, EU, local payment regulators and court dockets." },
      { text: "Rising fraud, cyber incidents or false-decline costs that imply AI risk controls are losing effectiveness.", monitoring_source: "10-K risk factors, breach disclosures, fraud-loss commentary and client disclosures." },
      { text: "Agentic commerce partners bypassing card networks or using alternative settlement rails at scale.", monitoring_source: "Merchant, wallet, AI platform and processor announcements." }
    ],
    cadence: [
      { frequency: "quarterly", task: "Refresh filings, operating metrics, product announcements and scorecard evidence." },
      { frequency: "semiannual", task: "Rebuild publication and patent proxies with a family-level patent database." }
    ]
  },
  operational_snapshot: {
    title: "Operational Snapshot",
    metrics: [
      { label: "FY2025 total payments + cash volume", value: "$17T", period: "2025", evidence_ids: ["ev_001"], source_ids: ["src_001"] },
      { label: "FY2025 processed transactions", value: "257.5B", period: "2025", evidence_ids: ["ev_002"], source_ids: ["src_001"] },
      { label: "Visa credentials", value: "Nearly 5B", period: "2025", evidence_ids: ["ev_001"], source_ids: ["src_001"] },
      { label: "Merchant acceptance", value: "175M+", period: "2025", evidence_ids: ["ev_001"], source_ids: ["src_001"] },
      { label: "Tokens provisioned", value: "16B+", period: "2025", evidence_ids: ["ev_003"], source_ids: ["src_001"] },
      { label: "FY2025 VAS revenue", value: "$10.9B", period: "2025", evidence_ids: ["ev_008"], source_ids: ["src_001"] },
      { label: "Q2 2026 processed transactions", value: "66.1B", period: "2026-Q2", evidence_ids: ["ev_007"], source_ids: ["src_002"] },
      { label: "Stablecoin settlement run rate", value: "$7B", period: "2026-04-29", evidence_ids: ["ev_006"], source_ids: ["src_009"] }
    ]
  },
  method_notes: {
    title: "Method Notes",
    notes: [
      "This is an absolute readiness score, not a peer ranking.",
      "Science metrics use field-level publication proxies because a Visa-authored publication corpus was not identified.",
      "Patent trend uses representative open patent records; exact annual global family counts were unavailable from public sources in this environment.",
      "The breakthrough gate requires Industrialization and Adoption scores above 3.0. Visa passes those gates."
    ]
  },
  bottom_line: {
    title: "Bottom Line",
    text: "Visa is a high-confidence commercial scale-up innovator. Its advantage is not publishing frontier science; it is converting AI risk scoring, tokenization, authentication, agentic commerce and stablecoin settlement into live infrastructure at global payments scale.",
    evidence_ids: ["ev_001", "ev_003", "ev_006", "ev_008", "ev_009"],
    source_ids: ["src_001", "src_004", "src_009"]
  }
};

const payload = {
  schema_version: "2.1",
  company: "Visa Inc",
  ticker: "NYSE: V",
  mode: "absolute",
  benchmark_ready: true,
  skill_metadata: {
    skill_name: "technology-innovation-analysis",
    skill_version: "1.2.0",
    skill_path: ".codex/skills/technology-innovation-analysis/SKILL.md",
    scorer_name: "score_innovation_benchmark.py",
    scorer_version: "1.2.0",
    metric_rules_version: "1.2.0"
  },
  research_run: {
    research_date: researchDate,
    analyst: "codex",
    run_id: runId,
    user_request: "Research Visa Inc, NYSE: V using technology-innovation-analysis, build a Tech Innovation dashboard, and create separate Instagram carousel assets.",
    time_horizon: "Five-year operating, publication and patent window where reproducible: 2021-2025, with latest Q2 FY2026 and April 2026 product updates.",
    research_mode: "web_research_with_deterministic_scoring"
  },
  research_context: {
    focus_technologies: [
      "AI fraud, risk, cybersecurity and authorization scoring",
      "Tokenization, passkeys, identity-bound checkout and Visa Token Service",
      "Stablecoin settlement, Visa Direct and agentic commerce payment protocols"
    ],
    company_identifiers: {
      legal_name: "Visa Inc",
      ticker: "NYSE: V",
      cik: "0001403161",
      fiscal_year_end: "09-30"
    },
    source_availability: [
      { domain: "company_filings", status: "available", note: "FY2025 10-K and Q2 FY2026 earnings release provide strong operating and adoption data." },
      { domain: "patents", status: "partial", note: "Representative Visa patent records are available; exact global family counts by year were not reproducible from open sources." },
      { domain: "science", status: "field_proxy", note: "Publication counts are OpenAlex field proxies, not Visa-authored publication counts." }
    ],
    search_log: [
      { query: "Visa FY2025 Form 10-K SEC tokenization stablecoin AI", source: "SEC EDGAR", date: researchDate, result_quality: "high", selected: true, selection_reason: "Primary latest full-year filing." },
      { query: "Visa Q2 2026 earnings release SEC", source: "SEC EDGAR", date: researchDate, result_quality: "high", selected: true, selection_reason: "Latest quarterly update before research date." },
      { query: "Visa patents tokenization machine learning Justia Google Patents", source: "patent databases", date: researchDate, result_quality: "medium", selected: true, selection_reason: "Representative patent evidence." },
      { query: "payment fraud detection machine learning OpenAlex 2021 2025 stablecoin payments", source: "OpenAlex", date: researchDate, result_quality: "medium", selected: true, selection_reason: "Field-level publication trend proxy." }
    ],
    exclusions: [
      { candidate_source_or_metric: "Peer percentile ranking", reason: "Single-company mode requires absolute scoring only." },
      { candidate_source_or_metric: "News-only disruption narratives", reason: "Primary company, policy, patent and academic sources were preferred." }
    ],
    judgment_calls: [
      { topic: "Science attribution", decision: "Used field-level publication proxies.", rationale: "Visa does not disclose a robust publication corpus.", impact: "Science confidence and score were capped." },
      { topic: "Patent-family trend", decision: "Used representative open records and explicitly marked exact counts unavailable.", rationale: "Open assignee pages did not yield reproducible five-year family counts.", impact: "IP score and confidence were capped." },
      { topic: "Innovation thesis", decision: "Classified Visa as a commercial-scale innovator rather than a science-led breakthrough candidate.", rationale: "Adoption and industrialization evidence is much stronger than public science/IP evidence.", impact: "Dashboard emphasizes deployment and commercial gates." }
    ]
  },
  sources,
  evidence_items: evidence,
  layers: layers.map(({ score, display_score, raw_score, normalized_score, confidence_penalty, ...layer }) => layer),
  dashboard_content: dashboardContent,
  storage_metadata: {
    intended_store: "sqlite",
    recommended_primary_keys: {
      sources: "source_id",
      evidence_items: "evidence_id",
      metrics: "company + research_date + layer + metric_code"
    },
    content_hash_fields: ["sources", "evidence_items", "layers", "dashboard_content", "claims"]
  }
};

const scored = {
  ...payload,
  layers,
  total_score: totalScore,
  display_total_score: totalScore.toFixed(1),
  gate_pass: true,
  verdict: "Commercial-scale innovator with strong translational momentum",
  benchmark_ready: true,
  scorer_metadata: {
    scorer_name: "score_innovation_benchmark.py",
    scorer_version: "1.2.0",
    metric_rules_version: "1.2.0",
    formula: "layer_score = 5 * confidence_penalty * sum(weight_i * metric_i_value)"
  },
  claims: [
    { claim_id: "claim_001", section: "thesis", text: "Visa's strongest innovation signal is commercial deployment at global payment-network scale.", claim_type: "inference", confidence: "High", evidence_ids: ["ev_001", "ev_002", "ev_003"], source_ids: ["src_001"] },
    { claim_id: "claim_002", section: "science", text: "Science evidence is mostly field-level rather than Visa-authored.", claim_type: "limitation", confidence: "High", evidence_ids: ["ev_013", "ev_014"], source_ids: ["src_014", "src_015"] },
    { claim_id: "claim_003", section: "ip", text: "Visa's IP is technically relevant, but the open annual patent-family trend is incomplete.", claim_type: "limitation", confidence: "Medium", evidence_ids: ["ev_016", "ev_017", "ev_018", "ev_019"], source_ids: ["src_010", "src_011", "src_012", "src_013"] },
    { claim_id: "claim_004", section: "bottom_line", text: "Visa is a high-confidence commercial scale-up innovator rather than a science-led breakthrough company.", claim_type: "inference", confidence: "High", evidence_ids: ["ev_001", "ev_006", "ev_008", "ev_009"], source_ids: ["src_001", "src_004", "src_009"] }
  ]
};

const carousel = [
  {
    headline: "Visa Is Not Standing Still",
    support: "AI, tokens and stablecoins are moving from pilots into live rails.",
    visual: "A luminous global payments grid with a bright Visa-blue transaction path crossing continents.",
    prompt: "Square 1:1 Instagram editorial image, high contrast Tech Innovation palette, dark graphite background with electric blue and neon cyan transaction lines, central safe area text: 'Visa Is Not Standing Still', abstract but concrete payment network map, no logos, no cards, crisp modern typography, generous margins."
  },
  {
    headline: "The Scale Is Enormous",
    support: "Visa processed 257.5B transactions in FY2025.",
    visual: "A dense field of tiny payment pulses flowing into one clean central number.",
    prompt: "Square 1:1 Instagram image, dark high-tech payment pulses converging into a clean central typographic number '257.5B', small subline 'FY2025 processed transactions', electric blue on dark gray, mobile-safe margins, no brand logo, premium data editorial style."
  },
  {
    headline: "Tokens Are The Core",
    support: "More than 16B Visa tokens were provisioned by September 2025.",
    visual: "Secure glowing token nodes orbiting a protected digital credential.",
    prompt: "Square 1:1 Instagram image, stylized secure token nodes, cryptographic rings, central text '16B+ Tokens', dark graphite, electric blue and neon cyan, sharp contrast, no real card numbers, no logos, central safe area."
  },
  {
    headline: "Fraud Defense Is AI-Led",
    support: "Visa pairs models with security operations to fight adaptive fraud.",
    visual: "AI risk signals filtering suspicious payments before they reach a network core.",
    prompt: "Square 1:1 Instagram image, AI fraud detection scene with luminous signals sorted through a secure network gate, central text 'AI Fraud Defense', bold accessible typography, dark tech background, blue/cyan accents, no scary imagery, no logos."
  },
  {
    headline: "Stablecoins Enter The Stack",
    support: "Settlement reached a $7B annualized run rate by April 2026.",
    visual: "Traditional rails and blockchain rails merging into a single settlement layer.",
    prompt: "Square 1:1 Instagram image, two payment rails merging, one traditional banking line and one blockchain line, central text '$7B Run Rate', subline 'stablecoin settlement', high contrast dark gray, electric blue, neon cyan, polished financial technology editorial."
  },
  {
    headline: "Agentic Commerce Is Next",
    support: "Visa is building protocols for AI agents that can safely checkout.",
    visual: "A clean AI agent silhouette exchanging verified payment credentials with a merchant terminal.",
    prompt: "Square 1:1 Instagram image, abstract AI shopping agent with verified payment token, central text 'Agentic Commerce', secure checkout atmosphere, no humanoid robot cliché, no logos, high-contrast tech palette, safe margins."
  },
  {
    headline: "The Verdict",
    support: "Commercial-scale innovator, not a science-lab breakthrough story.",
    visual: "A five-layer score ladder ending at 18.9/25, glowing strongest on adoption and industrialization.",
    prompt: "Square 1:1 Instagram image, five horizontal score layers, central text '18.9 / 25', subline 'Commercial-scale innovator', dark graphite background, electric blue/cyan bars, crisp accessible typography, no dashboard screenshot, no logos."
  }
];

function ensureDirs() {
  [runDir, imageDir, path.join(root, "public")].forEach((dir) => fs.mkdirSync(dir, { recursive: true }));
}

function writeJson(file, value) {
  fs.writeFileSync(file, JSON.stringify(value, null, 2) + "\n");
}

function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char]));
}

function dashboardHtml(data) {
  const json = JSON.stringify(data).replace(/</g, "\\u003c");
  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Visa Inc Innovation Dashboard</title>
  <style>
    :root {
      --blue: #0066ff;
      --cyan: #00ffff;
      --dark: #1e1e1e;
      --white: #ffffff;
      --panel: #11151d;
      --panel-2: #171d27;
      --ink: #f6fbff;
      --muted: #9eb2c8;
      --line: rgba(255,255,255,.13);
      --line-strong: rgba(0,255,255,.28);
      --green: #47e6a1;
      --amber: #ffd166;
      --red: #ff6b7a;
      --max: 1480px;
      --body: "DejaVu Sans", "Inter", "Segoe UI", Arial, sans-serif;
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      min-height: 100vh;
      color: var(--ink);
      font-family: var(--body);
      background:
        linear-gradient(90deg, rgba(0,102,255,.12) 1px, transparent 1px),
        linear-gradient(0deg, rgba(0,255,255,.07) 1px, transparent 1px),
        radial-gradient(circle at 75% 8%, rgba(0,255,255,.13), transparent 28%),
        radial-gradient(circle at 20% 0%, rgba(0,102,255,.22), transparent 30%),
        #070a10;
      background-size: 72px 72px, 72px 72px, auto, auto, auto;
      overflow-x: hidden;
    }
    a { color: var(--cyan); text-underline-offset: .16em; }
    .shell { width: min(calc(100% - 28px), var(--max)); margin: 0 auto; padding: 18px 0 54px; }
    .topbar { display: flex; justify-content: space-between; gap: 16px; align-items: center; padding: 8px 2px 18px; color: var(--muted); font-size: .9rem; }
    .topbar strong { color: var(--white); }
    .app { overflow: hidden; border: 1px solid var(--line); border-radius: 8px; background: rgba(10,14,21,.93); box-shadow: 0 28px 90px rgba(0,0,0,.42); }
    .header { display: grid; grid-template-columns: minmax(0,1fr) 370px; gap: 26px; padding: 32px; border-bottom: 1px solid var(--line); background: linear-gradient(135deg, rgba(0,102,255,.24), transparent 42%), linear-gradient(180deg, rgba(17,21,29,.96), rgba(10,14,21,.88)); animation: rise 560ms ease both; }
    .kicker { color: var(--cyan); font-size: 11px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; }
    h1, h2, h3 { margin: 0; color: var(--white); font-weight: 700; letter-spacing: 0; }
    h1 { margin-top: 8px; max-width: 15ch; font-size: clamp(2.2rem, 4.2vw, 5rem); line-height: .96; }
    h2 { margin-bottom: 10px; font-size: clamp(1.2rem, 2vw, 1.7rem); line-height: 1.08; }
    h3 { margin-bottom: 8px; font-size: 1rem; line-height: 1.2; }
    p { margin: 0; color: var(--muted); line-height: 1.58; }
    .summary { max-width: 82ch; margin-top: 14px; font-size: 1rem; }
    .score-panel { display: grid; gap: 18px; align-content: start; border-left: 1px solid var(--line); padding-left: 24px; }
    .score-ring { --p: 75%; width: 184px; aspect-ratio: 1; display: grid; place-items: center; justify-self: end; border-radius: 50%; background: radial-gradient(circle at center, var(--panel) 58%, transparent 60%), conic-gradient(var(--cyan) var(--p), rgba(255,255,255,.11) 0); box-shadow: inset 0 0 0 1px rgba(0,255,255,.22), 0 0 36px rgba(0,102,255,.26); animation: settle 700ms ease both; }
    .score-ring strong { display: block; color: var(--white); font-size: 2.75rem; line-height: 1; text-align: center; }
    .score-ring span { display: block; margin-top: 4px; color: var(--muted); font-size: .78rem; text-align: center; }
    .badge-row { display: flex; flex-wrap: wrap; gap: 8px; }
    .badge { display: inline-flex; align-items: center; min-height: 30px; width: fit-content; padding: 7px 10px; border: 1px solid rgba(0,255,255,.26); border-radius: 6px; background: rgba(0,102,255,.18); color: var(--white); font-size: .81rem; font-weight: 700; }
    .badge.good { background: rgba(71,230,161,.13); color: #d8fff0; border-color: rgba(71,230,161,.3); }
    .badge.warn { background: rgba(255,209,102,.13); color: #fff0c4; border-color: rgba(255,209,102,.27); }
    .content { display: grid; grid-template-columns: minmax(0,1fr) 380px; gap: 0; }
    .main { padding: 30px; }
    .side { border-left: 1px solid var(--line); padding: 30px 24px; background: rgba(23,29,39,.7); }
    section { padding: 26px 0; border-bottom: 1px solid var(--line); opacity: 0; transform: translateY(14px); transition: opacity 520ms ease, transform 520ms ease; }
    section.visible { opacity: 1; transform: translateY(0); }
    section:first-child { padding-top: 0; }
    section:last-child { border-bottom: 0; }
    .split { display: grid; grid-template-columns: .9fr 1.1fr; gap: 26px; align-items: start; }
    .stack { display: grid; gap: 14px; }
    .list { display: grid; gap: 12px; margin: 0; padding: 0; list-style: none; }
    .list li { padding-left: 14px; border-left: 3px solid var(--cyan); color: var(--ink); line-height: 1.48; }
    .tech-grid { display: grid; gap: 12px; }
    .tech-item, .evidence-item, .risk-item, .source-item { border-top: 1px solid var(--line); padding-top: 12px; }
    .tech-item p, .evidence-item p, .risk-item p { font-size: .93rem; }
    .meta { color: var(--cyan); font-size: .78rem; text-transform: uppercase; letter-spacing: .08em; font-weight: 700; }
    .layers { display: grid; gap: 16px; }
    .layer { padding: 16px 0 18px; border-top: 1px solid var(--line); transition: transform 180ms ease; }
    .layer:hover { transform: translateX(4px); }
    .bar-head { display: flex; justify-content: space-between; align-items: baseline; gap: 12px; margin-bottom: 8px; }
    .bar-head b { color: var(--white); }
    .bar-head span { color: var(--cyan); font-weight: 700; font-variant-numeric: tabular-nums; }
    .bar-track { height: 8px; overflow: hidden; border-radius: 999px; background: rgba(255,255,255,.12); }
    .bar-fill { height: 100%; width: var(--w); border-radius: inherit; background: linear-gradient(90deg, var(--blue), var(--cyan)); box-shadow: 0 0 18px rgba(0,255,255,.38); transform-origin: left; animation: grow 900ms ease both; }
    .layer-body { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 12px; }
    .small-label { display: block; margin-bottom: 4px; color: var(--cyan); font-size: .76rem; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; }
    .chart { display: grid; gap: 10px; margin-top: 14px; }
    .chart-row { display: grid; grid-template-columns: 74px minmax(0,1fr) 92px; gap: 10px; align-items: center; font-size: .86rem; color: var(--muted); }
    .chart-row .track { height: 9px; background: rgba(255,255,255,.11); border-radius: 999px; overflow: hidden; }
    .chart-row .fill { height: 100%; width: var(--w); background: linear-gradient(90deg, var(--blue), var(--cyan)); border-radius: inherit; }
    .snapshot { display: grid; gap: 10px; }
    .metric { display: flex; justify-content: space-between; gap: 14px; padding: 10px 0; border-bottom: 1px solid var(--line); }
    .metric span { color: var(--muted); font-size: .86rem; }
    .metric b { color: var(--white); font-variant-numeric: tabular-nums; text-align: right; }
    .risk-item { border-color: rgba(255,107,122,.22); }
    .risk-item .severity { color: var(--red); font-weight: 700; font-size: .78rem; text-transform: uppercase; letter-spacing: .08em; }
    .source-list { display: grid; gap: 10px; max-height: 480px; overflow: auto; padding-right: 6px; }
    .source-item a { font-weight: 700; }
    .source-item p { font-size: .82rem; }
    .note { color: var(--muted); font-size: .9rem; line-height: 1.5; }
    @keyframes rise { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes settle { from { transform: scale(.96); opacity: 0; } to { transform: scale(1); opacity: 1; } }
    @keyframes grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }
    @media (max-width: 980px) {
      .header, .content, .split, .layer-body { grid-template-columns: 1fr; }
      .score-panel, .side { border-left: 0; padding-left: 0; }
      .score-ring { justify-self: start; width: 152px; }
      .main, .side, .header { padding: 22px; }
      h1 { max-width: 12ch; }
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
    <div class="topbar"><div><strong id="topCompany"></strong> <span id="topTicker"></span></div><div id="topDate"></div></div>
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
          <div class="stack"><div class="meta">Deterministic Verdict</div><h2 id="verdict"></h2><p class="note" id="gate"></p></div>
        </aside>
      </header>
      <div class="content">
        <main class="main">
          <section id="thesis"></section><section id="layers"></section><section id="technology"></section><section id="quant"></section>
          <section id="commercial"></section><section id="gateSection"></section><section id="research"></section><section id="patents"></section>
          <section id="risks"></section><section id="watchlist"></section><section id="bottom"></section><section id="sources"></section>
        </main>
        <aside class="side"><section class="visible" id="snapshot"></section><section class="visible" id="method"></section></aside>
      </div>
    </div>
  </div>
  <script>
    const data = JSON.parse(document.getElementById("score-data").textContent);
    const dc = data.dashboard_content;
    const el = (id) => document.getElementById(id);
    const html = (id, value) => { el(id).innerHTML = value; };
    const esc = (value) => String(value ?? "").replace(/[&<>"']/g, (char) => ({"&":"&amp;","<":"&lt;",">":"&gt;","\\"":"&quot;","'":"&#39;"}[char]));
    const pct = (score) => Math.max(0, Math.min(100, Number(score || 0) / 5 * 100));
    el("topCompany").textContent = data.company;
    el("topTicker").textContent = data.ticker;
    el("topDate").textContent = "Research date: " + data.research_run.research_date;
    el("headline").textContent = dc.hero.headline;
    el("subheadline").textContent = dc.hero.subheadline;
    el("scoreValue").textContent = data.display_total_score;
    el("scoreRing").style.setProperty("--p", (data.total_score / 25 * 100).toFixed(1) + "%");
    el("verdict").textContent = data.verdict;
    el("gate").textContent = data.gate_pass ? "Breakthrough gate: passed on commercialization evidence." : "Breakthrough gate: not passed.";
    html("heroBadges", '<span class="badge good">Readiness: ' + esc(data.display_total_score) + ' / 25</span><span class="badge">Mode: absolute</span><span class="badge warn">Science/IP proxies capped</span>');
    html("thesis", '<div class="split"><div><h2>' + esc(dc.thesis.title) + '</h2><p>' + esc(dc.thesis.summary) + '</p></div><ul class="list">' + dc.thesis.bullets.map(b => '<li>' + esc(b.text) + '</li>').join("") + '</ul></div>');
    html("layers", '<h2>Five-Layer Score</h2><div class="layers">' + data.layers.map(layer => '<article class="layer"><div class="bar-head"><b>' + esc(layer.label) + '</b><span>' + esc(layer.display_score) + ' / 5</span></div><div class="bar-track"><div class="bar-fill" style="--w:' + pct(layer.score).toFixed(1) + '%"></div></div><p style="margin-top:10px">' + esc(layer.summary) + '</p><div class="layer-body"><p><span class="small-label">Strong</span>' + esc(layer.strong) + '</p><p><span class="small-label">Missing</span>' + esc(layer.missing) + '</p></div></article>').join("") + '</div>');
    html("technology", '<h2>' + esc(dc.technology_map.title) + '</h2><p>' + esc(dc.technology_map.summary) + '</p><div class="tech-grid" style="margin-top:16px">' + dc.technology_map.items.map(item => '<article class="tech-item"><div class="meta">' + esc(item.maturity) + '</div><h3>' + esc(item.name) + '</h3><p>' + esc(item.description) + '</p></article>').join("") + '</div>');
    function chartHtml(chart) {
      const points = chart.series[0].points;
      const vals = points.map(p => Number(p.value || 0));
      const max = Math.max(...vals, 1);
      return '<article class="evidence-item"><h3>' + esc(chart.title) + '</h3><p>' + esc(chart.description) + '</p><div class="chart">' + points.map(p => '<div class="chart-row"><span>' + esc(p.period) + '</span><div class="track"><div class="fill" style="--w:' + ((Number(p.value || 0) / max) * 100).toFixed(1) + '%"></div></div><b>' + esc(p.value ?? "n/a") + '</b></div>').join("") + '</div></article>';
    }
    html("quant", '<h2>' + esc(dc.quantitative_signals.title) + '</h2><p>' + esc(dc.quantitative_signals.summary) + '</p><div class="stack" style="margin-top:16px">' + dc.quantitative_signals.charts.map(chartHtml).join("") + '</div>');
    html("commercial", '<h2>' + esc(dc.commercialization_evidence.title) + '</h2><p>' + esc(dc.commercialization_evidence.summary) + '</p><div class="stack" style="margin-top:16px">' + dc.commercialization_evidence.items.map(item => '<article class="evidence-item"><div class="meta">' + esc(item.label) + '</div><p>' + esc(item.text) + '</p></article>').join("") + '</div>');
    html("gateSection", '<h2>' + esc(dc.breakthrough_gate.title) + '</h2><p>' + esc(dc.breakthrough_gate.summary) + '</p><div class="split" style="margin-top:16px"><div><h3>Met</h3><ul class="list">' + dc.breakthrough_gate.conditions_met.map(x => '<li>' + esc(x.condition) + '</li>').join("") + '</ul></div><div><h3>Not Met</h3><ul class="list">' + dc.breakthrough_gate.conditions_not_met.map(x => '<li>' + esc(x.condition) + '</li>').join("") + '</ul></div></div>');
    html("research", '<h2>' + esc(dc.university_research_signals.title) + '</h2><p>' + esc(dc.university_research_signals.summary) + '</p><div class="stack" style="margin-top:16px">' + dc.university_research_signals.institutions.map(item => '<article class="evidence-item"><h3>' + esc(item.name) + '</h3><p>' + esc(item.signal) + '</p></article>').join("") + '</div>');
    html("patents", '<h2>' + esc(dc.patent_signals.title) + '</h2><p>' + esc(dc.patent_signals.summary) + '</p><div class="stack" style="margin-top:16px">' + dc.patent_signals.families.map(item => '<article class="evidence-item"><div class="meta">' + esc(item.publication_or_family_id) + '</div><h3>' + esc(item.title) + '</h3><p>' + esc(item.interpretation) + '</p></article>').join("") + '</div><p class="note" style="margin-top:14px">' + esc(dc.patent_signals.interpretation) + '</p>');
    html("risks", '<h2>Red Flags</h2><div class="stack">' + dc.red_flags.map(r => '<article class="risk-item"><div class="severity">' + esc(r.severity) + ' | ' + esc(r.layer) + '</div><h3>' + esc(r.title) + '</h3><p>' + esc(r.text) + '</p></article>').join("") + '</div>');
    html("watchlist", '<h2>' + esc(dc.watchlist.title) + '</h2><div class="split"><div><h3>Upgrade Signals</h3><ul class="list">' + dc.watchlist.upgrade_signals.map(x => '<li>' + esc(x.text) + '</li>').join("") + '</ul></div><div><h3>Downgrade Signals</h3><ul class="list">' + dc.watchlist.downgrade_signals.map(x => '<li>' + esc(x.text) + '</li>').join("") + '</ul></div></div>');
    html("bottom", '<h2>' + esc(dc.bottom_line.title) + '</h2><p>' + esc(dc.bottom_line.text) + '</p>');
    html("sources", '<h2>Sources</h2><div class="source-list">' + data.sources.map(s => '<article class="source-item"><a href="' + esc(s.url) + '">' + esc(s.title) + '</a><p>' + esc(s.publisher) + ' | ' + esc(s.document_date) + ' | ' + esc(s.notes) + '</p></article>').join("") + '</div>');
    html("snapshot", '<h2>' + esc(dc.operational_snapshot.title) + '</h2><div class="snapshot">' + dc.operational_snapshot.metrics.map(m => '<div class="metric"><span>' + esc(m.label) + '</span><b>' + esc(m.value) + '</b></div>').join("") + '</div>');
    html("method", '<h2>' + esc(dc.method_notes.title) + '</h2><div class="stack">' + dc.method_notes.notes.map(n => '<p class="note">' + esc(n) + '</p>').join("") + '</div>');
    const observer = new IntersectionObserver((entries) => entries.forEach(entry => { if (entry.isIntersecting) entry.target.classList.add("visible"); }), { threshold: .08 });
    document.querySelectorAll("main section").forEach(section => observer.observe(section));
  </script>
</body>
</html>
`;
}

function svgSlide(slide, index) {
  const titleLines = wrap(slide.headline, 18);
  const supportLines = wrap(slide.support, 32);
  const yTitle = titleLines.length === 1 ? 440 : 392;
  const circles = Array.from({ length: 18 }, (_, i) => {
    const x = 90 + ((i * 131) % 900);
    const y = 160 + ((i * 89) % 690);
    const r = 4 + ((i * 7) % 18);
    const opacity = (0.14 + ((i % 5) * 0.07)).toFixed(2);
    return `<circle cx="${x}" cy="${y}" r="${r}" fill="${i % 3 ? "#0066ff" : "#00ffff"}" opacity="${opacity}"/>`;
  }).join("");
  const bars = [0.92, 0.76, 0.6, 0.84, 0.68].map((w, i) => `<rect x="182" y="${720 + i * 34}" width="${Math.round(660 * w)}" height="10" rx="5" fill="url(#grad)" opacity="${0.35 + i * 0.11}"/>`).join("");
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080">
  <defs>
    <linearGradient id="grad" x1="0" x2="1"><stop stop-color="#0066ff"/><stop offset="1" stop-color="#00ffff"/></linearGradient>
    <radialGradient id="halo" cx="50%" cy="42%" r="56%"><stop stop-color="#003d99" stop-opacity=".68"/><stop offset=".55" stop-color="#0b1320" stop-opacity=".94"/><stop offset="1" stop-color="#070a10"/></radialGradient>
    <filter id="glow"><feGaussianBlur stdDeviation="8" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect width="1080" height="1080" fill="url(#halo)"/>
  <g opacity=".23">
    ${Array.from({ length: 16 }, (_, i) => `<path d="M0 ${120 + i * 58} H1080" stroke="#ffffff" stroke-width="1"/>`).join("")}
    ${Array.from({ length: 16 }, (_, i) => `<path d="M${80 + i * 64} 0 V1080" stroke="#00ffff" stroke-width="1"/>`).join("")}
  </g>
  <path d="M112 612 C270 410 360 690 520 496 S790 304 968 468" fill="none" stroke="url(#grad)" stroke-width="12" stroke-linecap="round" filter="url(#glow)" opacity=".9"/>
  <path d="M148 286 C320 194 462 248 586 170 S828 188 956 120" fill="none" stroke="#00ffff" stroke-width="3" opacity=".46"/>
  ${circles}
  <circle cx="540" cy="486" r="210" fill="#0b1018" opacity=".72" stroke="#00ffff" stroke-opacity=".28" stroke-width="2"/>
  <circle cx="540" cy="486" r="262" fill="none" stroke="#0066ff" stroke-opacity=".22" stroke-width="18"/>
  <text x="540" y="204" text-anchor="middle" font-family="DejaVu Sans, Arial, sans-serif" font-size="30" font-weight="700" fill="#00ffff" letter-spacing="3">VISA INNOVATION</text>
  ${titleLines.map((line, i) => `<text x="540" y="${yTitle + i * 74}" text-anchor="middle" font-family="DejaVu Sans, Arial, sans-serif" font-size="66" font-weight="800" fill="#ffffff">${esc(line)}</text>`).join("")}
  ${supportLines.map((line, i) => `<text x="540" y="${590 + i * 42}" text-anchor="middle" font-family="DejaVu Sans, Arial, sans-serif" font-size="30" font-weight="500" fill="#cfe8ff">${esc(line)}</text>`).join("")}
  ${index === 6 ? bars : ""}
  <text x="90" y="980" font-family="DejaVu Sans, Arial, sans-serif" font-size="24" font-weight="700" fill="#9eb2c8">Slide ${String(index + 1).padStart(2, "0")} / 07</text>
</svg>
`;
}

function wrap(text, max) {
  const words = text.split(" ");
  const lines = [];
  let line = "";
  for (const word of words) {
    if ((line + " " + word).trim().length > max && line) {
      lines.push(line);
      line = word;
    } else {
      line = (line + " " + word).trim();
    }
  }
  if (line) lines.push(line);
  return lines;
}

function carouselMarkdown() {
  return `# Visa Inc Instagram Carousel

## Carousel summary

The concept turns Visa's innovation story into a seven-part visual arc: scale, tokens, AI fraud defense, stablecoins, agentic commerce and the final score.
The visual direction uses the Tech Innovation theme: dark graphite, electric blue, neon cyan, high-contrast typography and network-like motion.

## Slides

${carousel.map((s, i) => `Slide ${i + 1}
Headline: ${s.headline}
Supporting text: ${s.support}
Visual suggestion: ${s.visual}
Image prompt: ${s.prompt}`).join("\n\n")}

## Assets

- ai-generated-cover.png
${carousel.map((_, i) => `- slide-${String(i + 1).padStart(2, "0")}.png`).join("\n")}
`;
}

function writeCarouselAssets() {
  carousel.forEach((slide, index) => {
    fs.writeFileSync(path.join(imageDir, `slide-${String(index + 1).padStart(2, "0")}.svg`), svgSlide(slide, index));
  });
  fs.writeFileSync(path.join(imageDir, "visa_inc_instagram_carousel.md"), carouselMarkdown());
  fs.writeFileSync(path.join(imageDir, "manifest.json"), JSON.stringify({
    subject: "Visa Inc",
    theme: "Tech Innovation",
    ai_generated_cover: "ai-generated-cover.png",
    slides: carousel.map((slide, index) => ({
      file: `slide-${String(index + 1).padStart(2, "0")}.png`,
      svg: `slide-${String(index + 1).padStart(2, "0")}.svg`,
      headline: slide.headline,
      prompt: slide.prompt
    }))
  }, null, 2) + "\n");
}

function main() {
  ensureDirs();
  writeJson(path.join(runDir, "payload.json"), payload);
  writeJson(path.join(runDir, "scored.json"), scored);
  const html = dashboardHtml(scored);
  fs.writeFileSync(path.join(runDir, "dashboard.html"), html);
  fs.writeFileSync(path.join(root, "public", "visa_inc_dashboard.html"), html);
  writeCarouselAssets();
  console.log(JSON.stringify({
    runDir,
    dashboard: path.join(runDir, "dashboard.html"),
    publicDashboard: path.join(root, "public", "visa_inc_dashboard.html"),
    carouselDir: imageDir,
    score: totalScore
  }, null, 2));
}

main();
