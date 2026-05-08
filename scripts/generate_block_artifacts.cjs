const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const researchDate = "2026-05-06";
const companySlug = "block_inc";
const runId = "xyz-innovation-20260506";
const runDir = path.join(root, "public", "runs", companySlug, researchDate, runId);
const imageDir = path.join(root, "imagegen", companySlug);

const sourceUrl = {
  ticker: "https://investors.block.xyz/investor-news/news-details/2025/Block-Announces-Ticker-Symbol-Change-to-XYZ-To-Report-Fourth-Quarter-Results/default.aspx",
  tenK: "https://www.sec.gov/Archives/edgar/data/1512673/000162828026012254/xyz-20251231.htm",
  eightK: "https://www.sec.gov/Archives/edgar/data/1512673/000119312526076557/d108590d8k.htm",
  shareholderLetter: "https://www.sec.gov/Archives/edgar/data/1512673/000119312526076557/d108590dex991.htm",
  bitkey: "https://block.xyz/inside/press-release-bitkey-launch",
  protoCore: "https://block.xyz/inside/press-release-block-core-scientific-agreement",
  protoRig: "https://investors.block.xyz/investor-news/news-details/2025/Block-Unveils-Proto-Rig-and-Proto-Fleet-Marking-a-New-Era-in-Bitcoin-Mining/default.aspx",
  justia: "https://patents.justia.com/assignee/block-inc",
  cfpb: "https://www.consumerfinance.gov/about-us/newsroom/cfpb-orders-operator-of-cash-app-to-pay-175-million-and-fix-its-failures-on-fraud/",
  csbs: "https://www.csbs.org/newsroom/state-regulators-issue-80-million-penalty-block-inc-cash-app-bsaaml-violations",
  openalexDocs: "https://developers.openalex.org/guides/searching",
  digitalWalletBibliometric: "https://www.mdpi.com/2304-6775/12/4/34",
  mobilePaymentBibliometric: "https://journals.sagepub.com/doi/full/10.1177/21582440231200329",
  bnplStanford: "https://www.gsb.stanford.edu/faculty-research/publications/buy-now-pay-pain-later",
  bnplHbs: "https://www.hbs.edu/faculty/Pages/item.aspx?num=62913",
  nberEwallet: "https://www.nber.org/papers/w33178",
  mitDci: "https://www.dci.mit.edu/",
  cambridgeCcaf: "https://www.jbs.cam.ac.uk/faculty-research/centres/alternative-finance/research/",
};

function source(source_id, title, url, publisher, document_date, source_type, notes, reliability = "high") {
  return {
    source_id,
    title,
    url,
    publisher,
    document_date,
    accessed_at: researchDate,
    source_type,
    availability: "available",
    reliability,
    notes,
  };
}

const sources = [
  source("src_001", "Block Announces Ticker Symbol Change to XYZ", sourceUrl.ticker, "Block, Inc.", "2025-01-09", "primary", "Official confirmation that Block changed NYSE ticker from SQ to XYZ effective January 21, 2025."),
  source("src_002", "Block Inc FY2025 Form 10-K", sourceUrl.tenK, "SEC EDGAR", "2026-02-26", "primary", "Latest annual filing used for business lines, product development expense, GPV, lending losses, segment gross profit, bitcoin ecosystem, Bitkey and Proto disclosures."),
  source("src_003", "Block Inc 8-K, February 26 2026", sourceUrl.eightK, "SEC EDGAR", "2026-02-26", "primary", "Current report covering Q4 2025 shareholder letter and 2026 workforce reduction plan."),
  source("src_004", "Block Q4 2025 Shareholder Letter", sourceUrl.shareholderLetter, "SEC EDGAR", "2026-02-26", "primary", "Management discussion of AI operating model, Cash App, Square, Moneybot, lending, Proto and growth metrics."),
  source("src_005", "Self-Custody Bitcoin Wallet Bitkey Launch", sourceUrl.bitkey, "Block, Inc.", "2023-12-07", "primary", "Primary Bitkey launch source for 95-plus country availability, wallet architecture and pricing."),
  source("src_006", "Block and Core Scientific 3nm ASIC Agreement", sourceUrl.protoCore, "Block, Inc.", "2024-07-10", "primary", "Primary announcement of 3nm mining ASIC supply agreement representing about 15 EH/s of hashrate."),
  source("src_007", "Block Unveils Proto Rig and Proto Fleet", sourceUrl.protoRig, "Block, Inc.", "2025-08-14", "primary", "Primary announcement of modular bitcoin mining system and open-source fleet-management software."),
  source("src_008", "Patents Assigned to Block, Inc.", sourceUrl.justia, "Justia Patents", "2026-05-06", "patent", "Representative public patent and application listings for Block assignee records.", "medium"),
  source("src_009", "CFPB Orders Operator of Cash App to Pay 175 Million Dollars", sourceUrl.cfpb, "Consumer Financial Protection Bureau", "2025-01-16", "government", "Federal consumer-protection enforcement action against Block/Cash App."),
  source("src_010", "State Regulators Issue 80 Million Dollar Penalty to Block Cash App", sourceUrl.csbs, "Conference of State Bank Supervisors", "2025-01-15", "government", "Multistate BSA/AML enforcement action against Block/Cash App."),
  source("src_011", "OpenAlex Search Documentation", sourceUrl.openalexDocs, "OpenAlex", "2026-05-06", "secondary_dataset", "Documents scholarly search method. Direct API counts were not available from the local sandbox; used as method context.", "medium"),
  source("src_012", "Evolution and Trends in Digital Wallet Research", sourceUrl.digitalWalletBibliometric, "Publications / MDPI", "2024-10-11", "academic", "Bibliometric source for digital-wallet field maturity and global user context.", "medium"),
  source("src_013", "Mapping the Intellectual Structure of Mobile Payment Research", sourceUrl.mobilePaymentBibliometric, "SAGE Open", "2023-09-29", "academic", "Mobile-payment bibliometric source reporting 455 Web of Science publications.", "medium"),
  source("src_014", "Buy Now Pay Pain Later", sourceUrl.bnplStanford, "Stanford Graduate School of Business", "2024-03", "academic", "Stanford-linked BNPL empirical study using data for 10.6 million U.S. consumers.", "high"),
  source("src_015", "Buy Now Pay Later Credit", sourceUrl.bnplHbs, "Harvard Business School", "2022-09", "academic", "Harvard/NBER BNPL working paper on usage, consumer characteristics and spending effects.", "high"),
  source("src_016", "The Rise of E-Wallet Super-Apps and Buy-Now-Pay-Later", sourceUrl.nberEwallet, "NBER", "2024-11", "academic", "NBER evidence on e-wallet super-apps and BNPL as payment and credit infrastructure.", "high"),
  source("src_017", "MIT Digital Currency Initiative", sourceUrl.mitDci, "MIT", "2026-05-06", "academic", "Research context for digital currency, tokenization and payment infrastructure.", "high"),
  source("src_018", "Cambridge Centre for Alternative Finance Research", sourceUrl.cambridgeCcaf, "University of Cambridge", "2026-05-06", "academic", "Research context for fintech, virtual currency and alternative finance policy.", "high"),
];

function evidence(evidence_id, source_id, layer, metric_codes, fact, raw_value, raw_unit, period_start, period_end, company_attributable, field_proxy, limitations = "") {
  return {
    evidence_id,
    source_id,
    layer,
    metric_codes,
    fact_type: company_attributable ? "sourced_fact" : (field_proxy ? "field_proxy" : "context"),
    fact,
    raw_value,
    raw_unit,
    period_start,
    period_end,
    company_attributable,
    field_proxy,
    quote_or_excerpt: "",
    location: "Linked source, see filing lines or public source page.",
    verified: true,
    limitations,
  };
}

const evidenceItems = [
  evidence("ev_001", "src_001", "Industrialization", ["company_identity"], "Block's NYSE Class A common stock began trading under ticker XYZ on January 21, 2025.", "XYZ", "ticker", "2025-01-21", "2025-01-21", true, false),
  evidence("ev_002", "src_002", "Industrialization", ["product_development"], "Product development expense was $2.908 billion in 2025, essentially flat with $2.914 billion in 2024; the filing attributes part of 2025 increase pressure to internally developed software amortization and Proto hardware development.", 2.908, "USD billions", "2024", "2025", true, false),
  evidence("ev_003", "src_002", "Industrialization", ["product_development"], "Five-year product development trend: 2021 $1.399B, 2022 $2.136B, 2023 $2.721B, 2024 $2.914B, 2025 $2.908B.", 2.908, "USD billions", "2021", "2025", true, false),
  evidence("ev_004", "src_004", "Industrialization", ["ai_operating_model"], "Block announced it would reduce headcount from over 10,000 people to just under 6,000 and orient the company around intelligence tools.", 4000, "employees affected", "2026", "2026", true, false),
  evidence("ev_005", "src_004", "Adoption", ["cash_app_growth"], "Block reported 2025 gross profit of $10.36B, Cash App gross profit of $6.34B up 21%, and Square gross profit of $3.94B up 9%.", 10.36, "USD billions gross profit", "2025", "2025", true, false),
  evidence("ev_006", "src_004", "Adoption", ["cash_app_engagement"], "Primary banking actives grew to 9.3 million in December 2025 from 8.3 million in September, and PBAs generated nearly 10x the gross profit per active versus peer-to-peer only actives.", 9.3, "million actives", "2025-09", "2025-12", true, false),
  evidence("ev_007", "src_004", "Adoption", ["ai_product_adoption"], "More than 70% of Cash App actives who used Moneybot in testing selected a proactive prompt, and Cash App Green actives were 3x more likely to use Moneybot.", 70, "percent", "2025-Q4", "2025-Q4", true, false),
  evidence("ev_008", "src_004", "Adoption", ["lending_growth"], "Consumer lending origination volume grew 69% year over year in Q4 2025, and Cash App Borrow origination volume grew 223% year over year.", 223, "percent growth", "2025-Q4", "2025-Q4", true, false),
  evidence("ev_009", "src_004", "Adoption", ["square_growth"], "Square new volume added accelerated to 29% growth in Q4 2025, sales-led NVA grew 62%, and Block reported partnerships with 70 independent sales organizations.", 70, "ISOs", "2025-Q4", "2025-Q4", true, false),
  evidence("ev_010", "src_002", "Adoption", ["gpv"], "Gross Payment Volume was $259.631B in 2025, $240.812B in 2024 and $227.699B in 2023.", 259.631, "USD billions", "2023", "2025", true, false),
  evidence("ev_011", "src_005", "Industrialization", ["bitkey_launch"], "Bitkey launched in more than 95 countries across six continents with a mobile app, hardware device and recovery tools.", 95, "countries", "2023", "2023", true, false),
  evidence("ev_012", "src_006", "Industrialization", ["proto_asic"], "Block agreed to supply Core Scientific with new 3nm mining ASICs representing approximately 15 EH/s of hashrate.", 15, "EH/s", "2024", "2024", true, false),
  evidence("ev_013", "src_007", "Industrialization", ["proto_rig"], "Block unveiled Proto Rig and Proto Fleet in 2025, with Proto Rigs mining at Core Scientific's Dalton, Georgia facility.", null, "deployment", "2025", "2025", true, false),
  evidence("ev_014", "src_008", "IP", ["patent_activity"], "Justia's public Block assignee page shows 26 pages of assigned records and recent 2026 grants/applications across payments, AI-generated backgrounds, cryptocurrency key sharing, firmware, offline transactions and identity verification.", 26, "Justia pages", "2022", "2026", true, false, "Open listing is not a patent-family census."),
  evidence("ev_015", "src_008", "IP", ["patent_activity"], "Representative Block patent records observed by date include 2022 proximity-based payments, 2023 POS and custom-financing grants, 2025 payment-token and offline-mode grants, and many 2026 grants/applications.", null, "representative annual records", "2022", "2026", true, false, "Lower-bound observation from public search snippets, not an exhaustive annual family count."),
  evidence("ev_016", "src_008", "IP", ["technical_specificity"], "Recent Block patent examples include cryptocurrency management with wireless activation, systems for key sharing for cryptocurrency transactions, intelligent management of authorization requests, offline payment transactions and identity verification using payment instruments.", null, "representative records", "2025", "2026", true, false),
  evidence("ev_017", "src_012", "Science", ["publication_growth"], "Digital wallet bibliometric work reports rapid economic relevance for digital wallets, with users rising from 2.4B in 2020 toward a projected 3.6B in 2026; this supports a mature, growing application field.", 3.6, "billion projected users", "2020", "2026", false, true, "Adoption proxy, not article-count time series."),
  evidence("ev_018", "src_013", "Science", ["publication_growth"], "Mobile-payment bibliometric work reports a corpus of 455 Web of Science publications and describes post-COVID adoption and usage proliferation.", 455, "publications", "2023", "2023", false, true, "Field-level corpus count; not company-attributable."),
  evidence("ev_019", "src_014", "Science", ["citation_quality"], "Stanford-linked BNPL study used banking data for 10.6 million U.S. consumers and found new BNPL users experienced rapid increases in overdraft charges and card interest and fees.", 10.6, "million consumers", "2024", "2024", false, true),
  evidence("ev_020", "src_015", "Science", ["citation_quality"], "Harvard/NBER BNPL work describes U.S. BNPL users and spending responses using a large transaction-level panel.", null, "academic paper", "2022", "2022", false, true),
  evidence("ev_021", "src_016", "Science", ["science_to_application_linkage"], "NBER e-wallet super-app research examines BNPL as an internal payment option and credit product inside wallet ecosystems.", null, "academic paper", "2024", "2024", false, true),
  evidence("ev_022", "src_017", "Science", ["university_signal"], "MIT DCI provides research context for digital currency, tokenization and payment systems adjacent to Block's bitcoin and Lightning strategy.", null, "research program", "2025", "2026", false, true),
  evidence("ev_023", "src_018", "Science", ["university_signal"], "Cambridge CCAF researches technology-enabled alternative finance, virtual currency and fintech policy across global markets.", null, "research program", "2025", "2026", false, true),
  evidence("ev_024", "src_009", "Policy & Economics", ["consumer_regulation"], "The CFPB ordered Block to provide up to $120M in consumer redress and pay a $55M penalty over Cash App fraud and dispute-handling failures.", 175, "USD millions", "2025", "2025", true, false),
  evidence("ev_025", "src_010", "Policy & Economics", ["aml_regulation"], "Forty-eight state financial regulators issued an $80M penalty and required an independent BSA/AML program review and corrective action.", 80, "USD millions", "2025", "2025", true, false),
  evidence("ev_026", "src_002", "Policy & Economics", ["credit_losses"], "Transaction, loan and consumer receivable losses increased 68% in 2025; loan losses rose 154%, driven by Cash App Borrow volume growth and held-for-investment accounting.", 68, "percent", "2024", "2025", true, false),
  evidence("ev_027", "src_002", "Adoption", ["bitcoin_economics"], "Bitcoin ecosystem revenue contributed 35% of total 2025 revenue but only 4% of total gross profit.", 4, "percent gross profit", "2025", "2025", true, false),
  evidence("ev_028", "src_011", "Science", ["publication_count_limitation"], "OpenAlex documentation supports scholarly search and exact phrase querying, but local network access prevented a reproducible API-based annual count in this run.", null, "method limitation", "2021", "2025", false, true, "Annual publication counts are treated as partial rather than deterministic."),
];

function metric(code, label, value, weight, evidence_ids, raw_inputs, method, rationale, judgment_level = "medium") {
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
      raw_inputs,
      method,
      parameters: { floor: 0, cap: 1 },
      rationale,
      judgment_level,
    },
  };
}

const layers = [
  {
    label: "Science",
    coverage_ratio: 0.62,
    summary: "The external science base is credible and active, but Block is not a public science producer. The relevant fields are applied fintech, digital wallets, BNPL, credit-risk data, bitcoin custody, Lightning and mining infrastructure.",
    strong: "Research signals from Stanford, Harvard/NBER, MIT and Cambridge map directly to Block's payment, credit and bitcoin infrastructure themes.",
    missing: "No robust Block-authored publication corpus or reproducible OpenAlex five-year annual article series was available in this run.",
    metrics: [
      metric("publication_growth", "Publication growth proxy", 0.50, 0.35, ["ev_017", "ev_018", "ev_028"], { field_corpora: "455 mobile-payment WOS publications; digital-wallet adoption field expanding; exact annual counts unavailable" }, "evidence-weighted_judgment", "The field is active and broad, but annual article-count coverage is incomplete.", "high"),
      metric("citation_velocity_or_quality", "Institution quality", 0.66, 0.30, ["ev_019", "ev_020", "ev_021", "ev_022", "ev_023"], { institutions: ["Stanford", "Harvard/NBER", "MIT", "Cambridge"] }, "expert_source_quality", "Relevant work comes from strong academic institutions and reputable journals/working-paper series."),
      metric("science_to_application_linkage", "Science-to-product linkage", 0.70, 0.35, ["ev_006", "ev_007", "ev_008", "ev_011", "ev_012", "ev_013", "ev_021"], { product_links: ["Cash App Score", "BNPL", "Moneybot", "Bitkey", "Proto"] }, "evidence-weighted_judgment", "Block's product road map applies active research themes even though it does not publish much science itself."),
    ],
    caps: [],
  },
  {
    label: "IP",
    coverage_ratio: 0.68,
    summary: "Block has a broad and technically specific public patent record around payments, device identity, AI-assisted commerce, crypto custody and offline transactions. The limitation is that open sources did not provide a clean global family count by priority year.",
    strong: "Representative patents are specific to real product primitives: cryptocurrency keys, wireless activation, payment authorization, offline processing and identity verification.",
    missing: "Exhaustive patent-family time series and non-patent-literature linkage by family.",
    metrics: [
      metric("patent_family_growth", "Patent-family growth proxy", 0.58, 0.34, ["ev_014", "ev_015"], { justia_pages: 26, observed_years: "2022-2026 lower-bound representative listings" }, "proxy_count", "Public listings show continued recent activity but are not family-normalized.", "high"),
      metric("technical_specificity", "Technical specificity", 0.78, 0.38, ["ev_016"], { examples: ["crypto key sharing", "offline payments", "AI authorization", "identity verification"] }, "evidence-weighted_judgment", "The records describe concrete systems rather than only business-method generalities."),
      metric("science_to_patent_or_assignee_quality", "Assignee quality", 0.72, 0.28, ["ev_014", "ev_016"], { assignee: "Block, Inc.", ecosystems: ["Square", "Cash App", "Bitkey", "Proto"] }, "evidence-weighted_judgment", "Block is a high-quality industrial assignee with patent claims linked to deployed ecosystems."),
    ],
    caps: [],
  },
  {
    label: "Industrialization",
    coverage_ratio: 0.88,
    summary: "Block shows strong industrialization in software, payments, risk, lending and increasingly bitcoin hardware. The 2026 AI-driven workforce reduction creates execution uncertainty, but the company has disclosed real product delivery and operating scale.",
    strong: "Product development remains near $2.9B annually; Block shipped Proto units, launched Bitkey globally and secured a 15 EH/s 3nm ASIC agreement.",
    missing: "Block does not disclose Proto unit economics, ASIC yield, Bitkey sales, Moneybot quality metrics or AI automation reliability.",
    metrics: [
      metric("manufacturing_or_deployment_evidence", "Deployment evidence", 0.82, 0.40, ["ev_011", "ev_012", "ev_013"], { bitkey_countries: 95, proto_hashrate_ehs: 15 }, "min_max_and_judgment", "Bitkey and Proto moved from concept to launched/deployed products."),
      metric("process_learning_or_capex", "Process learning and investment", 0.76, 0.30, ["ev_002", "ev_003", "ev_004"], { product_development_2021_b: 1.399, product_development_2025_b: 2.908, headcount_reduction: ">40%" }, "growth_plus_risk_adjustment", "Sustained product development spending offsets some AI restructuring execution risk."),
      metric("operational_scale_signal", "Operating scale", 0.86, 0.30, ["ev_005", "ev_010"], { gross_profit_2025_b: 10.36, gpv_2025_b: 259.631 }, "scale_normalization", "Square/Cash App production scale is already large and commercially mature."),
    ],
    caps: [],
  },
  {
    label: "Adoption",
    coverage_ratio: 0.92,
    summary: "Adoption is Block's clearest strength. Cash App, Square, lending, GPV, Moneybot testing and seller-distribution metrics show live customer pull rather than only R&D intent.",
    strong: "Cash App gross profit grew 21%; PBAs reached 9.3M; Cash App Borrow originations grew 223%; Square NVA grew 29% and sales-led NVA grew 62% in Q4 2025.",
    missing: "Emerging product-specific revenue for Moneybot, Cash App Score, Bitkey and Proto remains limited.",
    metrics: [
      metric("revenue_or_booking_evidence", "Revenue and volume evidence", 0.84, 0.38, ["ev_005", "ev_010", "ev_027"], { gross_profit_2025_b: 10.36, gpv_2025_b: 259.631, bitcoin_gp_share: "4%" }, "scale_normalization", "Core ecosystems have large volume and gross profit, while bitcoin revenue mix has low gross-profit contribution."),
      metric("customer_or_partner_breadth", "Customer and partner breadth", 0.86, 0.30, ["ev_006", "ev_009", "ev_011", "ev_012"], { pba_m: 9.3, isos: 70, bitkey_countries: 95, proto_customer: "Core Scientific" }, "evidence-weighted_judgment", "Adoption spans consumers, sellers, distribution partners and a named bitcoin-mining customer."),
      metric("repeatability_or_deployment_scale", "Repeatability and engagement", 0.82, 0.32, ["ev_007", "ev_008", "ev_009"], { moneybot_testing_prompt_selection_pct: 70, borrow_yoy_pct: 223, square_nva_growth_pct: 29 }, "evidence-weighted_judgment", "Engagement and volume signals suggest repeatable commercialization across multiple products."),
    ],
    caps: [],
  },
  {
    label: "Policy & Economics",
    coverage_ratio: 0.83,
    summary: "The economics are attractive in scaled payments and software, but policy and credit-risk pressure are material. CFPB and state AML actions are not side issues; they directly constrain Cash App's ability to scale financial products.",
    strong: "Block has scale, gross-profit growth, and banking/credit data advantages that can compound if risk controls improve.",
    missing: "Evidence that compliance remediation, loan losses and AI restructuring can coexist with faster product velocity.",
    metrics: [
      metric("regulatory_or_standards_fit", "Regulatory fit", 0.44, 0.36, ["ev_024", "ev_025"], { cfpb_total_m: 175, aml_penalty_m: 80 }, "risk_adjusted_min_max", "Recent enforcement actions materially lower the policy score."),
      metric("policy_or_supply_chain_support", "Ecosystem support", 0.62, 0.26, ["ev_012", "ev_013", "ev_017", "ev_022", "ev_023"], { proto_customer: "Core Scientific", research_institutions: ["MIT", "Cambridge"] }, "evidence-weighted_judgment", "Bitcoin and fintech ecosystems exist, but they are volatile and policy-sensitive."),
      metric("economic_readiness", "Economic readiness", 0.66, 0.38, ["ev_005", "ev_026", "ev_027"], { gross_profit_2025_b: 10.36, losses_growth_pct: 68, bitcoin_gross_profit_share_pct: 4 }, "risk_adjusted_scale", "Gross-profit base is strong, but credit losses and bitcoin gross-margin mix reduce economic quality."),
    ],
    caps: [],
  },
];

const claims = [
  claim("claim_001", "thesis", "Block is a strong applied fintech industrializer, not a science-led breakthrough company.", "inference", "High", ["ev_002", "ev_005", "ev_010", "ev_011", "ev_012"], ["src_002", "src_004", "src_005", "src_006"]),
  claim("claim_002", "thesis", "The highest-conviction innovation domains are AI-enabled financial interfaces, proprietary underwriting and bitcoin infrastructure.", "inference", "High", ["ev_006", "ev_007", "ev_008", "ev_011", "ev_012", "ev_013"], ["src_004", "src_005", "src_006", "src_007"]),
  claim("claim_003", "red_flags", "Regulatory remediation is a gating issue for Cash App's financial-services expansion.", "inference", "High", ["ev_024", "ev_025"], ["src_009", "src_010"]),
  claim("claim_004", "bottom_line", "The breakthrough gate is a partial pass: industrialization and adoption clear the threshold, but policy and execution risk prevent an exceptional score.", "inference", "High", ["ev_004", "ev_024", "ev_025", "ev_026"], ["src_003", "src_009", "src_010", "src_002"]),
];

function claim(claim_id, section, text, claim_type, confidence, evidence_ids, source_ids) {
  return { claim_id, section, text, claim_type, confidence, evidence_ids, source_ids };
}

const publicationProxy = [
  { period: "2021", value: null, note: "Annual field count not reproducible; mature mobile-payment review literature visible." },
  { period: "2022", value: null, note: "BNPL and fintech credit research accelerates; Harvard/NBER BNPL paper issued." },
  { period: "2023", value: 455, note: "Mobile-payment Web of Science corpus reported by SAGE Open bibliometric study." },
  { period: "2024", value: 10.6, note: "Stanford BNPL paper uses data for 10.6M consumers; digital-wallet bibliometric study published." },
  { period: "2025", value: 108, note: "Scopus BNPL systematic/bibliometric source reported 108 papers in 2025 literature." },
];

const patentProxy = [
  { period: "2021", value: null, note: "No clean public family count in this run." },
  { period: "2022", value: ">=1", note: "Representative proximity/payment and device records visible." },
  { period: "2023", value: ">=3", note: "Representative POS, custom-financing and AI/payment records visible." },
  { period: "2024", value: ">=3", note: "Recent filings leading to 2025/2026 grants visible." },
  { period: "2025", value: ">=20", note: "Justia page positions and snippets show many 2025 grants/applications." },
  { period: "2026 YTD", value: ">=20", note: "Current first page lists many 2026 grants/applications." },
];

const dashboardContent = {
  hero: {
    headline: "Block Inc Innovation Readiness",
    subheadline: "NYSE: XYZ, assessed on applied fintech, AI-native operations, proprietary credit models and bitcoin infrastructure.",
    verdict_label: "Strong innovator with translational momentum",
    evidence_ids: ["ev_001", "ev_005", "ev_012", "ev_024"],
    source_ids: ["src_001", "src_002", "src_004", "src_006", "src_009"],
  },
  thesis: {
    title: "Thesis",
    summary: "Block has real commercialization momentum, but the innovation thesis is applied systems execution rather than frontier science.",
    bullets: [
      { text: "Cash App and Square provide live distribution for AI, lending and merchant software features.", claim_ids: ["claim_001", "claim_002"], evidence_ids: ["ev_005", "ev_006", "ev_007", "ev_009"], source_ids: ["src_004"] },
      { text: "Proto and Bitkey add hardware and bitcoin infrastructure optionality beyond conventional fintech.", claim_ids: ["claim_002"], evidence_ids: ["ev_011", "ev_012", "ev_013"], source_ids: ["src_005", "src_006", "src_007"] },
      { text: "Regulatory remediation and credit-loss control are the main limits on the score.", claim_ids: ["claim_003"], evidence_ids: ["ev_024", "ev_025", "ev_026"], source_ids: ["src_009", "src_010", "src_002"] },
    ],
  },
  technology_map: {
    title: "Technology Map",
    summary: "The analysis focuses on the three innovation domains most material to Block's future value creation.",
    items: [
      { name: "AI-native financial interfaces", description: "Moneybot, Square AI and the planned intelligence-native operating model aim to convert real-time customer and merchant data into product actions.", maturity: "commercial", evidence_ids: ["ev_004", "ev_007"], source_ids: ["src_004"] },
      { name: "Proprietary underwriting and credit scoring", description: "Cash App Score, Borrow and BNPL products use ecosystem data, repayment history and transaction signals to expand credit access.", maturity: "commercial", evidence_ids: ["ev_008", "ev_019", "ev_020"], source_ids: ["src_004", "src_014", "src_015"] },
      { name: "Bitcoin self-custody and mining infrastructure", description: "Bitkey, Proto ASICs, Proto Rig and Proto Fleet move Block into crypto hardware and open mining infrastructure.", maturity: "scaling", evidence_ids: ["ev_011", "ev_012", "ev_013"], source_ids: ["src_005", "src_006", "src_007"] },
    ],
  },
  quantitative_signals: {
    title: "Quantitative Signals",
    summary: "The strongest quantitative signals are commercial, not scientific: gross profit, product development spending, GPV, lending growth and bitcoin hardware deployment.",
    charts: [
      { chart_id: "chart_product_development", title: "Product development expense", description: "Block's product development spend roughly doubled from 2021 to 2025, then plateaued near $2.9B.", series: [{ label: "Product development", unit: "USD billions", points: [{ period: "2021", value: 1.399 }, { period: "2022", value: 2.136 }, { period: "2023", value: 2.721 }, { period: "2024", value: 2.914 }, { period: "2025", value: 2.908 }] }], evidence_ids: ["ev_003"], source_ids: ["src_002"] },
      { chart_id: "chart_gpv", title: "Gross Payment Volume", description: "GPV grew from $227.7B in 2023 to $259.6B in 2025.", series: [{ label: "GPV", unit: "USD billions", points: [{ period: "2023", value: 227.699 }, { period: "2024", value: 240.812 }, { period: "2025", value: 259.631 }] }], evidence_ids: ["ev_010"], source_ids: ["src_002"] },
      { chart_id: "chart_publication_proxy", title: "Publication proxy", description: "Open annual field counts were not reproducible; chart preserves the partial bibliometric evidence state rather than implying a clean time series.", series: [{ label: "Field evidence", unit: "mixed", points: publicationProxy }], evidence_ids: ["ev_017", "ev_018", "ev_019", "ev_028"], source_ids: ["src_011", "src_012", "src_013", "src_014"] },
      { chart_id: "chart_patent_proxy", title: "Patent proxy", description: "Representative public listing signal; not an exhaustive patent-family count.", series: [{ label: "Public patent signal", unit: "lower-bound records", points: patentProxy }], evidence_ids: ["ev_014", "ev_015", "ev_016"], source_ids: ["src_008"] },
    ],
  },
  commercialization_evidence: {
    title: "Commercialization Evidence",
    summary: "Block clears the commercial-readiness gate because core products are deployed and emerging bets have named customers or test adoption.",
    items: [
      { label: "Cash App engagement", text: "Primary banking actives reached 9.3M in December 2025 and generated nearly 10x gross profit per active versus P2P-only customers.", evidence_ids: ["ev_006"], source_ids: ["src_004"] },
      { label: "AI interface testing", text: "More than 70% of actives who used Moneybot in testing selected a proactive financial prompt.", evidence_ids: ["ev_007"], source_ids: ["src_004"] },
      { label: "Proto customer", text: "Core Scientific is the named first customer for Block's 3nm mining ASICs, representing about 15 EH/s.", evidence_ids: ["ev_012"], source_ids: ["src_006"] },
    ],
  },
  breakthrough_gate: {
    title: "Breakthrough Gate",
    summary: "Partial pass. Industrialization and adoption pass; policy, credit risk and AI restructuring keep the result below exceptional.",
    conditions_met: [
      { condition: "Industrialization score is at least 3.0 with adequate evidence.", evidence_ids: ["ev_002", "ev_011", "ev_012", "ev_013"], source_ids: ["src_002", "src_005", "src_006", "src_007"] },
      { condition: "Adoption score is at least 3.0 with high commercial evidence.", evidence_ids: ["ev_005", "ev_006", "ev_007", "ev_008", "ev_009"], source_ids: ["src_004"] },
    ],
    conditions_not_met: [
      { condition: "Science and IP evidence are not clean enough to call Block a frontier breakthrough company.", evidence_ids: ["ev_014", "ev_018", "ev_028"], source_ids: ["src_008", "src_013", "src_011"] },
      { condition: "Regulatory and credit-loss pressure remain material scaling constraints.", evidence_ids: ["ev_024", "ev_025", "ev_026"], source_ids: ["src_009", "src_010", "src_002"] },
    ],
    result: "Partial pass",
  },
  university_research_signals: {
    title: "University Research",
    summary: "Academic evidence supports the field thesis but is mostly field-level, not Block-authored.",
    institutions: [
      { name: "Stanford Graduate School of Business", signal: "BNPL consumer-health research using data for 10.6M U.S. consumers.", company_attributable: false, field_proxy: true, evidence_ids: ["ev_019"], source_ids: ["src_014"] },
      { name: "Harvard Business School / NBER", signal: "BNPL user characteristics and spending-pattern work.", company_attributable: false, field_proxy: true, evidence_ids: ["ev_020"], source_ids: ["src_015"] },
      { name: "MIT Digital Currency Initiative", signal: "Digital currency and payment infrastructure research relevant to Block's bitcoin strategy.", company_attributable: false, field_proxy: true, evidence_ids: ["ev_022"], source_ids: ["src_017"] },
      { name: "University of Cambridge CCAF", signal: "Alternative finance and virtual-currency research relevant to fintech policy and adoption.", company_attributable: false, field_proxy: true, evidence_ids: ["ev_023"], source_ids: ["src_018"] },
    ],
  },
  patent_signals: {
    title: "Patents",
    summary: "Patent evidence points to real engineering work, but the open data is a representative listing rather than a normalized family census.",
    families: [
      { title: "Cryptocurrency management systems and methods with wireless activation", publication_or_family_id: "US12586071 / US12586070", jurisdictions: ["US"], priority_date: "2023-10-20", interpretation: "Bitkey-adjacent custody hardware and power-management specificity.", evidence_ids: ["ev_016"], source_ids: ["src_008"] },
      { title: "Systems and methods for key sharing for cryptocurrency transactions", publication_or_family_id: "US12579542", jurisdictions: ["US"], priority_date: "2022-06-30", interpretation: "Directly relevant to multi-device self-custody and recovery architecture.", evidence_ids: ["ev_016"], source_ids: ["src_008"] },
      { title: "Processing electronic payment transactions in offline-mode", publication_or_family_id: "US12462233 / US20260094137", jurisdictions: ["US"], priority_date: "2021-11-18", interpretation: "Payment acceptance resilience and offline transaction engineering.", evidence_ids: ["ev_015", "ev_016"], source_ids: ["src_008"] },
      { title: "Intelligent management of authorization requests", publication_or_family_id: "US12572942", jurisdictions: ["US"], priority_date: "2023-02-08", interpretation: "AI-assisted transaction classification and authorization evidence.", evidence_ids: ["ev_016"], source_ids: ["src_008"] },
    ],
    interpretation: "The patent set is broad and product-specific. Confidence is medium because annual patent-family counts by priority year were not reproducible from open sources.",
  },
  red_flags: [
    { red_flag_id: "rf_001", title: "Regulatory drag", text: "CFPB and multistate AML actions create a clear policy overhang for Cash App financial services.", severity: "high", layer: "Policy & Economics", evidence_ids: ["ev_024", "ev_025"], source_ids: ["src_009", "src_010"], claim_ids: ["claim_003"] },
    { red_flag_id: "rf_002", title: "Credit loss expansion", text: "Loan and consumer receivable losses grew sharply in 2025 as lending scaled.", severity: "medium", layer: "Policy & Economics", evidence_ids: ["ev_026"], source_ids: ["src_002"], claim_ids: ["claim_003"] },
    { red_flag_id: "rf_003", title: "AI restructuring execution", text: "Cutting more than 40% of the workforce may increase velocity, but it raises operational and control-risk questions.", severity: "medium", layer: "Industrialization", evidence_ids: ["ev_004"], source_ids: ["src_003", "src_004"], claim_ids: ["claim_004"] },
    { red_flag_id: "rf_004", title: "Bitcoin gross-margin mix", text: "Bitcoin was 35% of total revenue but only 4% of gross profit in 2025.", severity: "medium", layer: "Adoption", evidence_ids: ["ev_027"], source_ids: ["src_002"], claim_ids: ["claim_004"] },
  ],
  watchlist: {
    title: "What Would Change The View",
    upgrade_signals: [
      { text: "Disclosed Bitkey units, active users, retention or custody balances.", monitoring_source: "Block filings, product updates and earnings calls." },
      { text: "Proto revenue, gross margin, delivered hashrate and additional named customers beyond Core Scientific.", monitoring_source: "Block and customer disclosures." },
      { text: "Evidence that Moneybot or Square AI improves retention, seller GPV, loan performance or support cost.", monitoring_source: "Shareholder letters and product analytics disclosures." },
      { text: "Completion of AML and CFPB remediation without new enforcement actions.", monitoring_source: "Regulator releases and 10-Q/10-K risk disclosures." },
    ],
    downgrade_signals: [
      { text: "Rising charge-offs or weaker loan economics as Cash App Borrow and BNPL scale.", monitoring_source: "SEC filings and allowance/loss-rate disclosures." },
      { text: "Proto delays, low mining-rig margin, or no follow-on mining customer announcements.", monitoring_source: "Block and bitcoin-mining customer disclosures." },
      { text: "AI restructuring causing slower releases, control failures or customer-support deterioration.", monitoring_source: "Filings, service-status records and regulator complaints." },
    ],
    cadence: [
      { frequency: "quarterly", task: "Refresh filings, earnings call, Proto/Bitkey adoption, credit losses and regulatory disclosures." },
      { frequency: "semiannual", task: "Refresh patent listings and academic field evidence for digital wallets, BNPL, credit scoring and bitcoin infrastructure." },
    ],
  },
  operational_snapshot: {
    title: "Operational Snapshot",
    metrics: [
      { label: "FY2025 gross profit", value: "$10.36B", period: "2025", evidence_ids: ["ev_005"], source_ids: ["src_004"] },
      { label: "Cash App gross profit growth", value: "+21%", period: "2025", evidence_ids: ["ev_005"], source_ids: ["src_004"] },
      { label: "Square gross profit growth", value: "+9%", period: "2025", evidence_ids: ["ev_005"], source_ids: ["src_004"] },
      { label: "Primary banking actives", value: "9.3M", period: "Dec 2025", evidence_ids: ["ev_006"], source_ids: ["src_004"] },
      { label: "Product development spend", value: "$2.908B", period: "2025", evidence_ids: ["ev_002"], source_ids: ["src_002"] },
      { label: "Proto ASIC agreement", value: "~15 EH/s", period: "2024", evidence_ids: ["ev_012"], source_ids: ["src_006"] },
    ],
  },
  method_notes: {
    title: "Method Notes",
    notes: [
      "Scoring is absolute, not peer-relative.",
      "Science and patent publication trends are lower-confidence because open annual count APIs were not available from the local sandbox.",
      "Displayed scores are computed by the deterministic scorer using normalized metrics and coverage penalties.",
      "The dashboard does not include generated Instagram images, per request.",
    ],
  },
  bottom_line: {
    title: "Bottom Line",
    text: "Block earns a strong innovator score because adoption and industrialization are real. It is not yet exceptional because regulatory remediation, credit risk, bitcoin margin quality and AI restructuring execution still need proof.",
    claim_ids: ["claim_004"],
    evidence_ids: ["ev_004", "ev_005", "ev_024", "ev_025", "ev_026", "ev_027"],
    source_ids: ["src_002", "src_003", "src_004", "src_009", "src_010"],
  },
};

const payload = {
  schema_version: "2.1",
  company: "Block, Inc.",
  ticker: "NYSE: XYZ",
  mode: "absolute",
  benchmark_ready: true,
  skill_metadata: {
    skill_name: "technology-innovation-analysis",
    skill_version: "1.2.0",
    skill_path: ".codex/skills/technology-innovation-analysis/SKILL.md",
    scorer_name: "score_innovation_benchmark.py",
    scorer_version: "1.2.0",
    metric_rules_version: "1.2.0",
  },
  research_run: {
    research_date: researchDate,
    analyst: "codex",
    run_id: runId,
    user_request: "Research Block Inc, NYSE: XYZ using innovation-analysis skill, build dashboard using Tech Innovation theme, and generate Instagram carousel images separately.",
    time_horizon: "Five years where available, 2021-2025 plus current 2026 filings/events.",
    research_mode: "web_research_with_deterministic_scoring",
  },
  research_context: {
    focus_technologies: ["AI-native financial interfaces", "Cash App underwriting and BNPL", "Bitcoin self-custody and mining infrastructure"],
    company_identifiers: {
      legal_name: "Block, Inc.",
      ticker: "NYSE: XYZ",
      cik: "0001512673",
      isin: "US8522341036",
    },
    source_availability: [
      { domain: "SEC filings", status: "available", note: "FY2025 Form 10-K and February 26 2026 8-K were available from SEC EDGAR." },
      { domain: "company disclosures", status: "available", note: "Ticker change, Bitkey, Proto/Core and Proto Rig disclosures were available from Block investor/company pages." },
      { domain: "patents", status: "partial", note: "Justia public assignee listing provided representative records, not normalized global patent-family counts." },
      { domain: "scientometrics", status: "partial", note: "Open annual query access was unavailable locally; used academic and bibliometric sources as field-level proxies." },
    ],
    search_log: [
      { query: "Block Inc 2025 10-K 2026 SEC", source: "web_search", date: researchDate, result_quality: "high", selected: true, selection_reason: "Primary annual filing." },
      { query: "Block Proto Core Scientific 3nm ASIC 15 EH/s official", source: "web_search", date: researchDate, result_quality: "high", selected: true, selection_reason: "Primary Proto commercialization evidence." },
      { query: "Patents assigned to Block Inc Justia", source: "web_search", date: researchDate, result_quality: "medium", selected: true, selection_reason: "Representative public patent source." },
      { query: "CFPB Cash App Block 2025 enforcement", source: "web_search", date: researchDate, result_quality: "high", selected: true, selection_reason: "Government red-flag source." },
    ],
    exclusions: [
      { candidate_source_or_metric: "Wikipedia and unaudited company-profile sites", reason: "Used only for discovery, not scoring." },
      { candidate_source_or_metric: "OpenAlex direct API counts", reason: "Local network resolution failed; annual publication counts not asserted as deterministic." },
    ],
    judgment_calls: [
      { topic: "Patent-family proxy", decision: "Used Justia representative listings and page count rather than exhaustive family counts.", rationale: "Open-source family census was unavailable in the current environment.", impact: "Lowered IP coverage ratio and confidence." },
      { topic: "Publication trend proxy", decision: "Used academic bibliometric and university research signals instead of annual OpenAlex counts.", rationale: "Direct annual counts were not reproducible in the sandbox.", impact: "Lowered Science coverage ratio and confidence." },
    ],
  },
  sources,
  evidence_items: evidenceItems,
  layers,
  dashboard_content: dashboardContent,
  claims,
  normalization_notes: [
    { metric_code: "publication_growth", rule: "evidence-weighted judgment from bibliometric corpus counts and field evidence", reason: "Exact five-year annual article counts were not reproducible." },
    { metric_code: "patent_family_growth", rule: "proxy_count from public patent listing, capped for missing family normalization", reason: "Justia page count is not a family census." },
    { metric_code: "economic_readiness", rule: "risk-adjusted scale score", reason: "Large gross profit is offset by credit losses and low bitcoin gross-profit contribution." },
  ],
  storage_metadata: {
    intended_store: "sqlite",
    recommended_primary_keys: {
      sources: "source_id",
      evidence_items: "evidence_id",
      metrics: "company + research_date + run_id + layer + metric_code",
    },
    content_hash_fields: ["sources", "evidence_items", "layers", "dashboard_content", "claims", "normalization_notes"],
  },
};

function renderDashboard(scored) {
  const data = JSON.stringify(scored).replace(/</g, "\\u003c");
  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${scored.company} Innovation Dashboard</title>
  <style>
    :root {
      --bg: #1e1e1e;
      --panel: #272727;
      --panel-2: #141414;
      --text: #ffffff;
      --muted: #a9b5c7;
      --line: rgba(255, 255, 255, 0.13);
      --blue: #0066ff;
      --cyan: #00ffff;
      --green: #39d98a;
      --amber: #ffcf5c;
      --red: #ff6b6b;
      font-family: "DejaVu Sans", Arial, sans-serif;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: radial-gradient(circle at 18% 0%, rgba(0, 102, 255, 0.24), transparent 32rem), var(--bg);
      color: var(--text);
      font-family: "DejaVu Sans", Arial, sans-serif;
      letter-spacing: 0;
    }
    main { max-width: 1220px; margin: 0 auto; padding: 28px 24px 56px; }
    header {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 280px;
      gap: 28px;
      align-items: end;
      padding: 18px 0 28px;
      border-bottom: 1px solid var(--line);
    }
    h1, h2, h3 { font-family: "DejaVu Sans", Arial, sans-serif; margin: 0; letter-spacing: 0; }
    h1 { font-size: clamp(2.4rem, 6vw, 5.8rem); line-height: 0.95; max-width: 820px; }
    h2 { font-size: 1.1rem; margin-bottom: 14px; }
    h3 { font-size: 0.95rem; color: var(--cyan); margin-bottom: 8px; }
    p { color: var(--muted); line-height: 1.55; margin: 0; }
    a { color: var(--cyan); text-decoration: none; }
    .kicker { color: var(--cyan); font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 10px; }
    .scoreBox {
      border-left: 3px solid var(--cyan);
      padding-left: 18px;
    }
    .scoreValue { font-size: 4rem; font-weight: 800; line-height: 0.9; }
    .scoreValue small { color: var(--muted); font-size: 1rem; }
    .verdict { color: var(--cyan); font-weight: 700; margin-top: 10px; }
    .grid {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 320px;
      gap: 28px;
      margin-top: 28px;
      align-items: start;
    }
    section {
      border-top: 1px solid var(--line);
      padding: 24px 0;
    }
    .panel {
      background: linear-gradient(180deg, rgba(255,255,255,0.055), rgba(255,255,255,0.025));
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
    }
    .stack { display: grid; gap: 14px; }
    .layers { display: grid; gap: 14px; }
    .layer {
      padding: 18px 0;
      border-bottom: 1px solid var(--line);
    }
    .layer:last-child { border-bottom: 0; }
    .layerTop { display: grid; grid-template-columns: 145px minmax(0, 1fr) 64px; gap: 12px; align-items: center; }
    .barTrack { height: 8px; border-radius: 999px; background: rgba(255,255,255,0.16); overflow: hidden; }
    .barFill {
      height: 100%;
      width: var(--w);
      border-radius: 999px;
      background: linear-gradient(90deg, var(--blue), var(--cyan));
      box-shadow: 0 0 20px rgba(0, 255, 255, 0.34);
    }
    .scoreLabel { text-align: right; font-weight: 800; color: var(--text); }
    .confidence { color: var(--muted); font-size: 0.82rem; margin-top: 8px; }
    .twoCol { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 22px; }
    .itemList { display: grid; gap: 12px; }
    .item { padding: 0 0 12px; border-bottom: 1px solid var(--line); }
    .item:last-child { border-bottom: 0; padding-bottom: 0; }
    .tag { display: inline-flex; color: var(--bg); background: var(--cyan); font-size: 0.72rem; font-weight: 800; padding: 3px 7px; border-radius: 4px; margin-bottom: 8px; }
    .metrics { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
    .metric { min-height: 92px; border-top: 1px solid var(--line); padding-top: 12px; }
    .metric strong { display: block; font-size: 1.55rem; margin-bottom: 5px; }
    .miniChart { display: flex; gap: 8px; align-items: end; min-height: 122px; padding-top: 10px; }
    .col { flex: 1; display: grid; gap: 6px; justify-items: center; align-items: end; min-width: 0; }
    .colBar { width: 100%; min-height: 3px; background: linear-gradient(180deg, var(--cyan), var(--blue)); border-radius: 3px 3px 0 0; }
    .colLabel { color: var(--muted); font-size: 0.72rem; white-space: nowrap; }
    .colValue { color: var(--text); font-size: 0.74rem; min-height: 1rem; }
    .redFlag { border-left: 3px solid var(--red); padding-left: 12px; }
    .medium { border-left-color: var(--amber); }
    .sourceList { columns: 2; column-gap: 28px; }
    .sourceList li { break-inside: avoid; margin: 0 0 8px; color: var(--muted); font-size: 0.84rem; }
    .sticky { position: sticky; top: 20px; }
    button {
      border: 1px solid var(--line);
      background: transparent;
      color: var(--text);
      border-radius: 6px;
      padding: 9px 11px;
      cursor: pointer;
      font: inherit;
    }
    button:hover { border-color: var(--cyan); color: var(--cyan); }
    .controls { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 14px; }
    .fade { opacity: 0; transform: translateY(10px); animation: rise 520ms ease forwards; }
    @keyframes rise { to { opacity: 1; transform: translateY(0); } }
    @media (max-width: 900px) {
      main { padding: 20px 16px 44px; }
      header, .grid, .twoCol, .metrics { grid-template-columns: 1fr; }
      .sticky { position: static; }
      .sourceList { columns: 1; }
      .layerTop { grid-template-columns: 110px minmax(0, 1fr) 54px; }
      h1 { font-size: 3rem; }
    }
  </style>
</head>
<body>
  <main>
    <header class="fade">
      <div>
        <div class="kicker">${scored.ticker} | ${scored.research_run.research_date}</div>
        <h1>${scored.dashboard_content.hero.headline}</h1>
        <p style="max-width: 760px; margin-top: 16px;">${scored.dashboard_content.hero.subheadline}</p>
      </div>
      <div class="scoreBox">
        <div class="scoreValue">${scored.display_total_score}<small> / 25</small></div>
        <div class="verdict">${scored.verdict}</div>
        <p style="margin-top: 8px;">Gate: ${scored.gate_pass ? "Pass" : scored.dashboard_content.breakthrough_gate.result}</p>
      </div>
    </header>
    <div class="grid">
      <div>
        <section class="fade" style="animation-delay: 80ms;">
          <h2>${scored.dashboard_content.thesis.title}</h2>
          <p>${scored.dashboard_content.thesis.summary}</p>
          <div class="itemList" style="margin-top: 16px;">${scored.dashboard_content.thesis.bullets.map((b) => `<div class="item"><span class="tag">Thesis</span><p>${b.text}</p></div>`).join("")}</div>
        </section>
        <section class="fade" style="animation-delay: 130ms;">
          <h2>Five-Layer Dashboard</h2>
          <div class="layers">${scored.layers.map((layer) => `
            <div class="layer">
              <div class="layerTop">
                <strong>${layer.label}</strong>
                <div class="barTrack"><div class="barFill" style="--w:${Math.max(0, Math.min(100, layer.score * 20))}%"></div></div>
                <div class="scoreLabel">${layer.display_score} / 5</div>
              </div>
              <p style="margin-top: 12px;">${layer.summary}</p>
              <div class="confidence">Confidence: ${layer.confidence} | Coverage: ${Math.round(layer.coverage_ratio * 100)}% | Strong: ${layer.strong} Missing: ${layer.missing}</div>
            </div>`).join("")}</div>
        </section>
        <section>
          <div class="twoCol">
            <div>
              <h2>${scored.dashboard_content.technology_map.title}</h2>
              <p>${scored.dashboard_content.technology_map.summary}</p>
              <div class="itemList" style="margin-top: 16px;">${scored.dashboard_content.technology_map.items.map((item) => `<div class="item"><h3>${item.name}</h3><p>${item.description}</p><p class="confidence">Maturity: ${item.maturity}</p></div>`).join("")}</div>
            </div>
            <div>
              <h2>${scored.dashboard_content.commercialization_evidence.title}</h2>
              <p>${scored.dashboard_content.commercialization_evidence.summary}</p>
              <div class="itemList" style="margin-top: 16px;">${scored.dashboard_content.commercialization_evidence.items.map((item) => `<div class="item"><h3>${item.label}</h3><p>${item.text}</p></div>`).join("")}</div>
            </div>
          </div>
        </section>
        <section>
          <h2>${scored.dashboard_content.quantitative_signals.title}</h2>
          <p>${scored.dashboard_content.quantitative_signals.summary}</p>
          <div class="twoCol" style="margin-top: 18px;">${scored.dashboard_content.quantitative_signals.charts.slice(0, 2).map(renderChart).join("")}</div>
          <div class="twoCol" style="margin-top: 18px;">${scored.dashboard_content.quantitative_signals.charts.slice(2).map(renderChart).join("")}</div>
        </section>
        <section>
          <div class="twoCol">
            <div>
              <h2>${scored.dashboard_content.breakthrough_gate.title}</h2>
              <p>${scored.dashboard_content.breakthrough_gate.summary}</p>
              <h3 style="margin-top: 14px;">Met</h3>
              <div class="itemList">${scored.dashboard_content.breakthrough_gate.conditions_met.map((x) => `<p class="item">${x.condition}</p>`).join("")}</div>
              <h3 style="margin-top: 14px;">Not met</h3>
              <div class="itemList">${scored.dashboard_content.breakthrough_gate.conditions_not_met.map((x) => `<p class="item">${x.condition}</p>`).join("")}</div>
            </div>
            <div>
              <h2>${scored.dashboard_content.patent_signals.title}</h2>
              <p>${scored.dashboard_content.patent_signals.summary}</p>
              <div class="itemList" style="margin-top: 16px;">${scored.dashboard_content.patent_signals.families.map((f) => `<div class="item"><h3>${f.title}</h3><p>${f.publication_or_family_id} | ${f.interpretation}</p></div>`).join("")}</div>
            </div>
          </div>
        </section>
        <section>
          <h2>${scored.dashboard_content.university_research_signals.title}</h2>
          <p>${scored.dashboard_content.university_research_signals.summary}</p>
          <div class="twoCol" style="margin-top: 16px;">${scored.dashboard_content.university_research_signals.institutions.map((i) => `<div class="item"><h3>${i.name}</h3><p>${i.signal}</p></div>`).join("")}</div>
        </section>
        <section>
          <h2>${scored.dashboard_content.red_flags.length} Red Flags</h2>
          <div class="itemList">${scored.dashboard_content.red_flags.map((r) => `<div class="item redFlag ${r.severity === "medium" ? "medium" : ""}"><h3>${r.title}</h3><p>${r.text}</p><p class="confidence">Severity: ${r.severity} | Layer: ${r.layer}</p></div>`).join("")}</div>
        </section>
        <section>
          <h2>${scored.dashboard_content.bottom_line.title}</h2>
          <p>${scored.dashboard_content.bottom_line.text}</p>
        </section>
        <section>
          <h2>Sources</h2>
          <ol class="sourceList">${scored.sources.map((s) => `<li><a href="${s.url}">${s.title}</a>, ${s.publisher}, ${s.document_date}.</li>`).join("")}</ol>
        </section>
      </div>
      <aside class="sticky">
        <div class="panel stack">
          <h2>${scored.dashboard_content.operational_snapshot.title}</h2>
          <div class="metrics">${scored.dashboard_content.operational_snapshot.metrics.map((m) => `<div class="metric"><strong>${m.value}</strong><p>${m.label}</p><p class="confidence">${m.period}</p></div>`).join("")}</div>
          <div>
            <h2>${scored.dashboard_content.watchlist.title}</h2>
            <h3>Upgrade</h3>
            ${scored.dashboard_content.watchlist.upgrade_signals.slice(0, 3).map((x) => `<p class="item">${x.text}</p>`).join("")}
            <h3 style="margin-top: 12px;">Downgrade</h3>
            ${scored.dashboard_content.watchlist.downgrade_signals.slice(0, 3).map((x) => `<p class="item">${x.text}</p>`).join("")}
          </div>
          <div>
            <h2>${scored.dashboard_content.method_notes.title}</h2>
            ${scored.dashboard_content.method_notes.notes.map((n) => `<p class="item">${n}</p>`).join("")}
          </div>
          <div class="controls">
            <button type="button" onclick="window.scrollTo({top:0,behavior:'smooth'})">Top</button>
            <button type="button" onclick="document.querySelector('ol').scrollIntoView({behavior:'smooth'})">Sources</button>
          </div>
        </div>
      </aside>
    </div>
  </main>
  <script>
    window.dashboardData = ${data};
    document.addEventListener("pointermove", (event) => {
      const x = Math.round((event.clientX / window.innerWidth) * 100);
      document.body.style.backgroundPosition = x + "% 0";
    });
  </script>
</body>
</html>`;
}

function renderChart(chart) {
  const points = chart.series[0].points;
  const numeric = points.map((p) => (typeof p.value === "number" ? p.value : 0));
  const max = Math.max(...numeric, 1);
  return `<div class="panel"><h3>${chart.title}</h3><p>${chart.description}</p><div class="miniChart">${points.map((p) => {
    const numericValue = typeof p.value === "number" ? p.value : 0;
    const height = Math.max(3, Math.round((numericValue / max) * 96));
    const value = p.value === null ? "n/a" : String(p.value);
    return `<div class="col"><div class="colValue">${value}</div><div class="colBar" style="height:${height}px"></div><div class="colLabel">${p.period}</div></div>`;
  }).join("")}</div></div>`;
}

function writeJson(file, object) {
  fs.writeFileSync(file, JSON.stringify(object, null, 2) + "\n", "utf8");
}

function main() {
  fs.mkdirSync(runDir, { recursive: true });
  fs.mkdirSync(imageDir, { recursive: true });

  const mode = process.argv[2] || "payload";
  if (mode === "payload") {
    writeJson(path.join(runDir, "payload.json"), payload);
    return;
  }

  if (mode === "dashboard") {
    const scoredPath = path.join(runDir, "scored.json");
    const scored = JSON.parse(fs.readFileSync(scoredPath, "utf8"));
    fs.writeFileSync(path.join(runDir, "dashboard.html"), renderDashboard(scored), "utf8");
    fs.writeFileSync(path.join(root, "public", "block_inc_dashboard.html"), renderDashboard(scored), "utf8");
    return;
  }

  throw new Error(`Unknown mode: ${mode}`);
}

main();
