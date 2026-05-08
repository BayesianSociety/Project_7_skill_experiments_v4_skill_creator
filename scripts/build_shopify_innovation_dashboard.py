#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RUN_DIR = REPO_ROOT / "public" / "runs" / "shopify-inc" / "2026-05-07" / "run-20260507-innovation-dashboard"
PAYLOAD_PATH = RUN_DIR / "payload.json"
SCORED_PATH = RUN_DIR / "scored.json"
DASHBOARD_PATH = RUN_DIR / "dashboard.html"


def metric(code, label, value, weight, evidence_ids, raw_inputs, method, rationale, judgment_level="medium"):
    return {
        "code": code,
        "label": label,
        "value": value,
        "weight": weight,
        "unit": "normalized_0_to_1",
        "source_type": "mixed",
        "verified": True,
        "evidence_ids": evidence_ids,
        "normalization": {
            "raw_inputs": raw_inputs,
            "method": method,
            "parameters": {"floor": 0.0, "cap": 1.0},
            "rationale": rationale,
            "judgment_level": judgment_level,
        },
    }


def build_payload() -> dict:
    sources = [
        {
            "source_id": "src_sec_2025_10k",
            "title": "Shopify Inc. Form 10-K for fiscal year ended December 31, 2025",
            "url": "https://www.sec.gov/Archives/edgar/data/1594805/000159480526000007/shop-20251231.htm",
            "publisher": "SEC EDGAR / Shopify Inc.",
            "document_date": "2026-02-11",
            "accessed_at": "2026-05-07",
            "source_type": "primary",
            "availability": "available",
            "reliability": "high",
            "notes": "Primary audited annual filing used for revenue, GMV, R&D, Payments penetration, risk, and operating evidence.",
        },
        {
            "source_id": "src_q1_2026_release",
            "title": "Shopify Delivers Again as Merchants Clear $100 Billion in Q1 GMV",
            "url": "https://www.shopify.com/investors/press-releases/shopify-delivers-again-merchants-clear-100-billion-q1-gmv",
            "publisher": "Shopify Investor Relations",
            "document_date": "2026-05-05",
            "accessed_at": "2026-05-07",
            "source_type": "primary",
            "availability": "available",
            "reliability": "high",
            "notes": "Latest quarterly release available during the research run.",
        },
        {
            "source_id": "src_fool_q1_transcript",
            "title": "Shopify Q1 2026 Earnings Transcript",
            "url": "https://www.fool.com/earnings/call-transcripts/2026/05/05/shopify-shop-q1-2026-earnings-transcript/",
            "publisher": "The Motley Fool Transcribing",
            "document_date": "2026-05-05",
            "accessed_at": "2026-05-07",
            "source_type": "secondary_transcript",
            "availability": "available",
            "reliability": "medium",
            "notes": "Transcript source for management commentary and product-adoption datapoints not present in the press release.",
        },
        {
            "source_id": "src_agentic_press",
            "title": "The agentic commerce platform: Shopify connects any merchant to every AI conversation",
            "url": "https://www.shopify.com/news/ai-commerce-at-scale",
            "publisher": "Shopify Newsroom",
            "document_date": "2026-01-11",
            "accessed_at": "2026-05-07",
            "source_type": "primary_company_product",
            "availability": "available",
            "reliability": "high",
            "notes": "Product announcement for UCP, Google/Microsoft integrations, Agentic plan, and Shopify Catalog.",
        },
        {
            "source_id": "src_agentic_help",
            "title": "Shopify Help Center: Shopify agentic storefronts",
            "url": "https://help.shopify.com/en/manual/online-sales-channels/agentic-storefronts",
            "publisher": "Shopify Help Center",
            "document_date": "2026",
            "accessed_at": "2026-05-07",
            "source_type": "primary_company_documentation",
            "availability": "available",
            "reliability": "high",
            "notes": "Documentation for AI-channel discovery, checkout behavior, attribution, and data-sharing boundaries.",
        },
        {
            "source_id": "src_sidekick_help",
            "title": "Shopify Help Center: Sidekick",
            "url": "https://help.shopify.com/en/manual/shopify-admin/productivity-tools/sidekick",
            "publisher": "Shopify Help Center",
            "document_date": "2026",
            "accessed_at": "2026-05-07",
            "source_type": "primary_company_documentation",
            "availability": "available",
            "reliability": "high",
            "notes": "Documentation for Sidekick's merchant-admin tasks, content generation, app generation, and memory features.",
        },
        {
            "source_id": "src_sidekick_dev",
            "title": "Shopify developer documentation: Sidekick app extensions",
            "url": "https://shopify.dev/docs/apps/build/sidekick",
            "publisher": "Shopify Developer Docs",
            "document_date": "2026",
            "accessed_at": "2026-05-07",
            "source_type": "primary_company_developer_documentation",
            "availability": "available",
            "reliability": "high",
            "notes": "Developer workflow evidence for exposing app data and scoped actions to Sidekick.",
        },
        {
            "source_id": "src_editions_summer25",
            "title": "Shopify Editions Summer 2025",
            "url": "https://www.shopify.com/ie/editions/summer2025",
            "publisher": "Shopify",
            "document_date": "2025",
            "accessed_at": "2026-05-07",
            "source_type": "primary_company_product",
            "availability": "available",
            "reliability": "high",
            "notes": "Product release evidence for AI theme generation, Sidekick multi-step reasoning, image generation, and mobile use.",
        },
        {
            "source_id": "src_shopify_patents",
            "title": "Shopify Patents and Virtual Patent Marking",
            "url": "https://www.shopify.com/legal/patents",
            "publisher": "Shopify Legal",
            "document_date": "2026",
            "accessed_at": "2026-05-07",
            "source_type": "primary_company_legal",
            "availability": "available",
            "reliability": "high",
            "notes": "Company patent notice and virtual marking list. The public list is explicitly non-comprehensive.",
        },
        {
            "source_id": "src_google_product_image_patent",
            "title": "US20210125251A1: Systems and methods for providing product image recommendations",
            "url": "https://patents.google.com/patent/US20210125251A1/en",
            "publisher": "Google Patents / USPTO family data",
            "document_date": "2021-04-29",
            "accessed_at": "2026-05-07",
            "source_type": "patent_database",
            "availability": "available",
            "reliability": "medium",
            "notes": "Representative Shopify patent family with US, EP, CA, and CN publications.",
        },
        {
            "source_id": "src_google_contextual_product_patent",
            "title": "US20230260004A1: Systems and method for providing contextual product recommendations",
            "url": "https://patents.google.com/patent/US20230260004A1/en",
            "publisher": "Google Patents / USPTO data",
            "document_date": "2023-08-17",
            "accessed_at": "2026-05-07",
            "source_type": "patent_database",
            "availability": "available",
            "reliability": "medium",
            "notes": "Representative checkout product-recommendation patent application; shown as abandoned in the search record.",
        },
        {
            "source_id": "src_google_checkout_patent",
            "title": "US12243026B2: Systems and methods for e-commerce checkout with delay loading of checkout options",
            "url": "https://patents.google.com/patent/US12243026B2/en",
            "publisher": "Google Patents / USPTO data",
            "document_date": "2025-03-04",
            "accessed_at": "2026-05-07",
            "source_type": "patent_database",
            "availability": "available",
            "reliability": "medium",
            "notes": "Representative checkout infrastructure patent assigned to Shopify Inc. and Shopify USA Inc.",
        },
        {
            "source_id": "src_justia_workflow_ai",
            "title": "US20250272062: Methods and systems for construction of workflow automation using artificial intelligence",
            "url": "https://patents.justia.com/patent/20250272062",
            "publisher": "Justia Patents / USPTO data",
            "document_date": "2025-08-28",
            "accessed_at": "2026-05-07",
            "source_type": "patent_database",
            "availability": "available",
            "reliability": "medium",
            "notes": "Representative Shopify AI workflow automation patent publication.",
        },
        {
            "source_id": "src_ipqwery_shopify_patents",
            "title": "Shopify Inc. patent-owner profile",
            "url": "https://www.ipqwery.com/ipowner/en/owner/ip/1216525-shopify-inc.html",
            "publisher": "IPqwery",
            "document_date": "2026",
            "accessed_at": "2026-05-07",
            "source_type": "patent_database",
            "availability": "available",
            "reliability": "medium",
            "notes": "Representative WIPO/PCT publication snippets for contextual chatbot operation and AI object detection/tracking.",
        },
        {
            "source_id": "src_sciencedirect_bibliometric",
            "title": "Artificial intelligence and recommender systems in e-commerce. Trends and research agenda",
            "url": "https://www.sciencedirect.com/science/article/pii/S2667305324001091",
            "publisher": "Intelligent Systems with Applications",
            "document_date": "2024-12",
            "accessed_at": "2026-05-07",
            "source_type": "academic_bibliometric_review",
            "availability": "available",
            "reliability": "high",
            "notes": "Open-access bibliometric review identified 120 documents, analyzed 91, and reported 97.16% growth in the topic.",
        },
        {
            "source_id": "src_stanford_recsys",
            "title": "Behavioral insights enhance AI-driven recommendations",
            "url": "https://news.stanford.edu/stories/2025/09/behavioral-insights-user-intent-ai-driven-recommendations-youtube",
            "publisher": "Stanford Report",
            "document_date": "2025-09-18",
            "accessed_at": "2026-05-07",
            "source_type": "university_research",
            "availability": "available",
            "reliability": "high",
            "notes": "Evidence of active university research on intent-structured AI recommendation systems.",
        },
        {
            "source_id": "src_mit_discrete_choice",
            "title": "Online Discrete Choice",
            "url": "https://www.its.mit.edu/pd-online-discrete-choice",
            "publisher": "MIT Intelligent Transportation Systems Lab",
            "document_date": "2026",
            "accessed_at": "2026-05-07",
            "source_type": "university_research",
            "availability": "available",
            "reliability": "high",
            "notes": "Evidence of real-time personalization and online preference updating research adjacent to recommenders.",
        },
        {
            "source_id": "src_harvard_krs",
            "title": "Introducing Keyword Recommender System in the Age of AI",
            "url": "https://d3.harvard.edu/events/introducing-keyword-recommender-system-krs-a-noble-alternative-search-recommender-system-in-the-age-of-ai/",
            "publisher": "Harvard Digital Data Design Institute",
            "document_date": "2026",
            "accessed_at": "2026-05-07",
            "source_type": "university_research",
            "availability": "available",
            "reliability": "high",
            "notes": "Field-experiment signal for AI-era search/recommendation systems in commerce-like discovery workflows.",
        },
    ]

    evidence_items = [
        {
            "evidence_id": "ev_gmv_2025",
            "source_id": "src_sec_2025_10k",
            "layer": "Adoption",
            "metric_codes": ["revenue_or_booking_evidence", "repeatability_or_deployment_scale"],
            "fact_type": "raw_observation",
            "fact": "Shopify facilitated $378.4 billion of GMV in 2025, up 29% from $292.3 billion in 2024 and $235.9 billion in 2023.",
            "raw_value": 378.4,
            "raw_unit": "USD billions GMV",
            "period_start": "2023",
            "period_end": "2025",
            "company_attributable": True,
            "field_proxy": False,
            "location": "Form 10-K, GMV discussion",
            "verified": True,
            "limitations": "GMV is not revenue; it is platform transaction volume.",
        },
        {
            "evidence_id": "ev_revenue_rd_2025",
            "source_id": "src_sec_2025_10k",
            "layer": "Industrialization",
            "metric_codes": ["process_learning_or_capex", "operational_scale_signal"],
            "fact_type": "raw_observation",
            "fact": "2025 revenue was $11.556 billion, up 30%; R&D expense was $1.536 billion, or 13% of revenue.",
            "raw_value": 1.536,
            "raw_unit": "USD billions R&D expense",
            "period_start": "2025",
            "period_end": "2025",
            "company_attributable": True,
            "field_proxy": False,
            "location": "Form 10-K, results of operations",
            "verified": True,
            "limitations": "R&D expense is a software-platform investment proxy, not a direct measure of scientific invention.",
        },
        {
            "evidence_id": "ev_payments_2025",
            "source_id": "src_sec_2025_10k",
            "layer": "Adoption",
            "metric_codes": ["revenue_or_booking_evidence", "repeatability_or_deployment_scale"],
            "fact_type": "raw_observation",
            "fact": "Shopify Payments penetration was 65.6% in 2025, facilitating $248.1 billion of GMV, versus 61.9% and $181.0 billion in 2024.",
            "raw_value": 248.1,
            "raw_unit": "USD billions payments GMV",
            "period_start": "2024",
            "period_end": "2025",
            "company_attributable": True,
            "field_proxy": False,
            "location": "Form 10-K, Merchant Solutions discussion",
            "verified": True,
            "limitations": "Payments adoption varies by geographic availability and merchant mix.",
        },
        {
            "evidence_id": "ev_loss_risk_2025",
            "source_id": "src_sec_2025_10k",
            "layer": "Policy & Economics",
            "metric_codes": ["economic_readiness"],
            "fact_type": "raw_observation",
            "fact": "Transaction and loan losses rose to $417 million in 2025 from $227 million in 2024, driven by Payments and lending losses.",
            "raw_value": 417,
            "raw_unit": "USD millions",
            "period_start": "2024",
            "period_end": "2025",
            "company_attributable": True,
            "field_proxy": False,
            "location": "Form 10-K, transaction and loan losses",
            "verified": True,
            "limitations": "Losses scale with payments and lending volume; this is a risk signal, not proof of economics failure.",
        },
        {
            "evidence_id": "ev_q1_2026_metrics",
            "source_id": "src_q1_2026_release",
            "layer": "Adoption",
            "metric_codes": ["revenue_or_booking_evidence", "repeatability_or_deployment_scale"],
            "fact_type": "raw_observation",
            "fact": "Q1 2026 GMV was $100.743 billion, revenue was $3.170 billion, operating income was $382 million, and free cash flow margin was 15%.",
            "raw_value": 100.743,
            "raw_unit": "USD billions GMV",
            "period_start": "2026-Q1",
            "period_end": "2026-Q1",
            "company_attributable": True,
            "field_proxy": False,
            "location": "Q1 2026 investor release",
            "verified": True,
            "limitations": "Quarterly figures are unaudited in the release.",
        },
        {
            "evidence_id": "ev_q1_2026_capex",
            "source_id": "src_q1_2026_release",
            "layer": "Industrialization",
            "metric_codes": ["process_learning_or_capex", "operational_scale_signal"],
            "fact_type": "raw_observation",
            "fact": "Q1 2026 operating cash flow was $481 million and capital expenditures were $5 million, producing $476 million of free cash flow.",
            "raw_value": 5,
            "raw_unit": "USD millions capex",
            "period_start": "2026-Q1",
            "period_end": "2026-Q1",
            "company_attributable": True,
            "field_proxy": False,
            "location": "Q1 2026 free cash flow reconciliation",
            "verified": True,
            "limitations": "Low capex reflects software/cloud economics; cloud spend appears in operating expense and cost of revenue.",
        },
        {
            "evidence_id": "ev_sidekick_adoption_q1",
            "source_id": "src_fool_q1_transcript",
            "layer": "Adoption",
            "metric_codes": ["customer_or_partner_breadth", "repeatability_or_deployment_scale"],
            "fact_type": "management_disclosure",
            "fact": "Management said weekly active shops using Sidekick were up about 4x year over year, over 12,000 custom apps were created with Sidekick in Q1, and nearly half of Shopify Flows generated in Q1 were built with Sidekick.",
            "raw_value": 12000,
            "raw_unit": "custom apps in Q1",
            "period_start": "2026-Q1",
            "period_end": "2026-Q1",
            "company_attributable": True,
            "field_proxy": False,
            "location": "Q1 2026 earnings transcript",
            "verified": True,
            "limitations": "Transcript is secondary; Shopify did not include these metrics in the press-release table.",
        },
        {
            "evidence_id": "ev_ai_channel_adoption_q1",
            "source_id": "src_fool_q1_transcript",
            "layer": "Adoption",
            "metric_codes": ["customer_or_partner_breadth", "repeatability_or_deployment_scale"],
            "fact_type": "management_disclosure",
            "fact": "Management disclosed Q1 AI-driven traffic to Shopify stores grew 8x year over year and orders from AI-powered searches increased nearly 13x.",
            "raw_value": 13,
            "raw_unit": "x growth in AI-search orders",
            "period_start": "2026-Q1",
            "period_end": "2026-Q1",
            "company_attributable": True,
            "field_proxy": False,
            "location": "Q1 2026 earnings transcript",
            "verified": True,
            "limitations": "Company did not disclose the absolute base, so growth could be from a small starting point.",
        },
        {
            "evidence_id": "ev_ucp_agentic",
            "source_id": "src_agentic_press",
            "layer": "Policy & Economics",
            "metric_codes": ["regulatory_or_standards_fit", "policy_or_supply_chain_support"],
            "fact_type": "raw_observation",
            "fact": "Shopify announced UCP, co-developed with Google, described as an open standard for AI agents to connect and transact with merchants, with Google AI Mode/Gemini and Microsoft Copilot checkout integrations.",
            "raw_value": 20,
            "raw_unit": "plus endorsing retailers/platforms stated by Shopify",
            "period_start": "2026-01-11",
            "period_end": "2026-01-11",
            "company_attributable": True,
            "field_proxy": False,
            "location": "Shopify Newsroom agentic-commerce announcement",
            "verified": True,
            "limitations": "Endorsements and integrations do not yet prove durable transaction share.",
        },
        {
            "evidence_id": "ev_agentic_docs",
            "source_id": "src_agentic_help",
            "layer": "Industrialization",
            "metric_codes": ["manufacturing_or_deployment_evidence", "operational_scale_signal"],
            "fact_type": "raw_observation",
            "fact": "Shopify documents agentic storefronts for ChatGPT, Google AI Mode/Gemini, and Microsoft Copilot; eligible stores can be active by default and retain order attribution in Shopify admin.",
            "raw_value": 3,
            "raw_unit": "named AI channels",
            "period_start": "2026",
            "period_end": "2026",
            "company_attributable": True,
            "field_proxy": False,
            "location": "Shopify Help Center agentic storefronts",
            "verified": True,
            "limitations": "Some channels were described as early access and not available to all stores.",
        },
        {
            "evidence_id": "ev_sidekick_docs",
            "source_id": "src_sidekick_help",
            "layer": "Industrialization",
            "metric_codes": ["manufacturing_or_deployment_evidence"],
            "fact_type": "raw_observation",
            "fact": "Shopify documents Sidekick as an AI-enabled commerce assistant that can analyze data, manage orders, edit products, generate content, generate custom apps, and remember context.",
            "raw_value": 6,
            "raw_unit": "documented capability areas",
            "period_start": "2026",
            "period_end": "2026",
            "company_attributable": True,
            "field_proxy": False,
            "location": "Shopify Help Center Sidekick page",
            "verified": True,
            "limitations": "Documentation confirms availability and scope, not conversion uplift.",
        },
        {
            "evidence_id": "ev_sidekick_extensions",
            "source_id": "src_sidekick_dev",
            "layer": "Industrialization",
            "metric_codes": ["manufacturing_or_deployment_evidence", "operational_scale_signal"],
            "fact_type": "raw_observation",
            "fact": "Developer docs show Sidekick app extensions can expose app data and scoped actions, run in Shopify's sandbox, and define limits including response time and tool counts.",
            "raw_value": 20,
            "raw_unit": "tools per app extension limit",
            "period_start": "2026",
            "period_end": "2026",
            "company_attributable": True,
            "field_proxy": False,
            "location": "Shopify developer docs",
            "verified": True,
            "limitations": "Developer-preview status limits inference about ecosystem-wide adoption.",
        },
        {
            "evidence_id": "ev_editions_ai",
            "source_id": "src_editions_summer25",
            "layer": "Industrialization",
            "metric_codes": ["manufacturing_or_deployment_evidence"],
            "fact_type": "raw_observation",
            "fact": "Summer 2025 Editions included AI block generation, AI theme generation, Sidekick multi-step reasoning, Sidekick image generation, mobile access, and screen-share/voice chat.",
            "raw_value": 6,
            "raw_unit": "AI feature clusters",
            "period_start": "2025",
            "period_end": "2025",
            "company_attributable": True,
            "field_proxy": False,
            "location": "Shopify Editions Summer 2025",
            "verified": True,
            "limitations": "Editions pages are product announcements, not measured usage reports.",
        },
        {
            "evidence_id": "ev_company_patent_notice",
            "source_id": "src_shopify_patents",
            "layer": "IP",
            "metric_codes": ["science_to_patent_or_assignee_quality"],
            "fact_type": "raw_observation",
            "fact": "Shopify states its products and services may be protected by utility patents, design patents, and pending applications in the U.S., Canada, and other jurisdictions; its public marking list is not comprehensive.",
            "raw_value": 2,
            "raw_unit": "jurisdiction examples",
            "period_start": "2026",
            "period_end": "2026",
            "company_attributable": True,
            "field_proxy": False,
            "location": "Shopify legal patent page",
            "verified": True,
            "limitations": "The company page mostly lists POS hardware design patents, not the full software portfolio.",
        },
        {
            "evidence_id": "ev_product_image_patent",
            "source_id": "src_google_product_image_patent",
            "layer": "IP",
            "metric_codes": ["patent_family_growth", "technical_specificity"],
            "fact_type": "raw_observation",
            "fact": "Product-image recommendation family includes US20210125251A1, US11386473B2, US12002079B2, EP, CA, and CN publications; claims describe merchant-device image recommendations and model-based quality/market-success signals.",
            "raw_value": 7,
            "raw_unit": "priority applications listed by Google Patents",
            "period_start": "2021",
            "period_end": "2024",
            "company_attributable": True,
            "field_proxy": False,
            "location": "Google Patents family data",
            "verified": True,
            "limitations": "Google Patents assignee and family data are a useful public proxy, not a legal opinion.",
        },
        {
            "evidence_id": "ev_contextual_product_patent",
            "source_id": "src_google_contextual_product_patent",
            "layer": "IP",
            "metric_codes": ["patent_family_growth", "technical_specificity"],
            "fact_type": "raw_observation",
            "fact": "US20230260004A1 covers contextual product recommendations at checkout taking shipping costs into account; the search record shows Shopify as assignee and the application as abandoned.",
            "raw_value": 1,
            "raw_unit": "US application",
            "period_start": "2023",
            "period_end": "2023",
            "company_attributable": True,
            "field_proxy": False,
            "location": "Google Patents",
            "verified": True,
            "limitations": "Abandoned status weakens defensive value but still shows engineering specificity.",
        },
        {
            "evidence_id": "ev_checkout_patent",
            "source_id": "src_google_checkout_patent",
            "layer": "IP",
            "metric_codes": ["patent_family_growth", "technical_specificity"],
            "fact_type": "raw_observation",
            "fact": "US12243026B2 covers checkout transactions with delay loading of checkout options; Google Patents lists Shopify Inc. and Shopify USA Inc. as assignees.",
            "raw_value": 1,
            "raw_unit": "US grant",
            "period_start": "2025",
            "period_end": "2025",
            "company_attributable": True,
            "field_proxy": False,
            "location": "Google Patents",
            "verified": True,
            "limitations": "Single representative patent, not a full portfolio map.",
        },
        {
            "evidence_id": "ev_workflow_ai_patent",
            "source_id": "src_justia_workflow_ai",
            "layer": "IP",
            "metric_codes": ["patent_family_growth", "technical_specificity", "science_to_patent_or_assignee_quality"],
            "fact_type": "raw_observation",
            "fact": "US20250272062 describes using a large language model, vector embeddings, and generated code for workflow automation, assigned to Shopify Inc.",
            "raw_value": 1,
            "raw_unit": "US application publication",
            "period_start": "2025",
            "period_end": "2025",
            "company_attributable": True,
            "field_proxy": False,
            "location": "Justia Patents",
            "verified": True,
            "limitations": "Application publication, not necessarily a granted patent.",
        },
        {
            "evidence_id": "ev_chatbot_object_detection_patents",
            "source_id": "src_ipqwery_shopify_patents",
            "layer": "IP",
            "metric_codes": ["patent_family_growth", "technical_specificity"],
            "fact_type": "raw_observation",
            "fact": "IPqwery lists Shopify PCT publications for contextual chatbot operation (WO2025/102145) and AI-smoothed object detection and tracking in video (WO2025/054696).",
            "raw_value": 2,
            "raw_unit": "PCT publications",
            "period_start": "2025",
            "period_end": "2025",
            "company_attributable": True,
            "field_proxy": False,
            "location": "IPqwery patent-owner profile",
            "verified": True,
            "limitations": "Secondary patent database snippets; direct PATENTSCOPE record was not opened in this run.",
        },
        {
            "evidence_id": "ev_bibliometric_review",
            "source_id": "src_sciencedirect_bibliometric",
            "layer": "Science",
            "metric_codes": ["publication_growth", "citation_velocity_or_quality", "science_to_application_linkage"],
            "fact_type": "field_proxy",
            "fact": "A 2024 bibliometric review of AI and recommender systems in e-commerce identified 120 documents, analyzed 91, reported 97.16% topic growth, and noted increases in 2021 and 2022.",
            "raw_value": 120,
            "raw_unit": "documents identified",
            "period_start": "pre-2024",
            "period_end": "2024",
            "company_attributable": False,
            "field_proxy": True,
            "location": "ScienceDirect open-access article abstract",
            "verified": True,
            "limitations": "Field-level proxy; not Shopify-authored science and not a full 2021-2025 company publication series.",
        },
        {
            "evidence_id": "ev_university_research",
            "source_id": "src_stanford_recsys",
            "layer": "Science",
            "metric_codes": ["citation_velocity_or_quality", "science_to_application_linkage"],
            "fact_type": "field_proxy",
            "fact": "Stanford reported 2025 research on intent-structured AI recommendation systems, emphasizing customer intent and domain knowledge for better recommendations.",
            "raw_value": 1,
            "raw_unit": "university research signal",
            "period_start": "2025",
            "period_end": "2025",
            "company_attributable": False,
            "field_proxy": True,
            "location": "Stanford Report",
            "verified": True,
            "limitations": "Adjacent field research, not Shopify-specific.",
        },
        {
            "evidence_id": "ev_mit_harvard_research",
            "source_id": "src_mit_discrete_choice",
            "layer": "Science",
            "metric_codes": ["citation_velocity_or_quality", "science_to_application_linkage"],
            "fact_type": "field_proxy",
            "fact": "MIT describes real-time online preference updating for personalization systems; Harvard D3 describes an AI-era keyword recommender field experiment with a reported 1.2% purchase lift.",
            "raw_value": 2,
            "raw_unit": "university research signals",
            "period_start": "2026",
            "period_end": "2026",
            "company_attributable": False,
            "field_proxy": True,
            "location": "MIT ITS and Harvard D3 pages",
            "verified": True,
            "limitations": "MIT and Harvard items are field proxies; Harvard source is an event page summarizing a talk.",
        },
        {
            "evidence_id": "ev_competition_ai_risk",
            "source_id": "src_sec_2025_10k",
            "layer": "Policy & Economics",
            "metric_codes": ["economic_readiness", "policy_or_supply_chain_support"],
            "fact_type": "raw_observation",
            "fact": "Shopify's 10-K warns competition may intensify as competitors add services, enhance existing services, and merchants use advanced tools such as AI to build their own solutions.",
            "raw_value": 1,
            "raw_unit": "risk disclosure",
            "period_start": "2025",
            "period_end": "2025",
            "company_attributable": True,
            "field_proxy": False,
            "location": "Form 10-K risk factors",
            "verified": True,
            "limitations": "Risk disclosure is qualitative and broad.",
        },
    ]

    layers = [
        {
            "label": "Science",
            "coverage_ratio": 0.55,
            "summary": "The underlying science around AI recommendation, personalization, and commerce-agent workflows is active, but Shopify itself looks like an applied platform-engineering company rather than an academic science publisher.",
            "strong": "Open academic literature supports recommender-system growth, university work is credible, and the application link to Shopify's products is direct.",
            "missing": "No reproducible Shopify-authored publication series was found, and OpenAlex API access was blocked in the local sandbox; publication counts are therefore field proxies, not company output.",
            "metrics": [
                metric("publication_growth", "Publication growth", 0.45, 0.34, ["ev_bibliometric_review"], {"documents_identified": 120, "documents_analyzed": 91, "reported_topic_growth_percent": 97.16}, "normalize_min_max_judgment", "A bibliometric review shows field growth, but the run lacks a reproducible 2021-2025 corpus count.", "high"),
                metric("citation_velocity_or_quality", "Citation quality", 0.55, 0.33, ["ev_bibliometric_review", "ev_university_research", "ev_mit_harvard_research"], {"credible_university_signals": 3, "shopify_authored_publications_found": 0}, "normalize_min_max_judgment", "Credible institutions are active, but company-attributable scientific output is not visible.", "medium"),
                metric("science_to_application_linkage", "Science-to-application linkage", 0.70, 0.33, ["ev_sidekick_docs", "ev_agentic_docs", "ev_university_research"], {"direct_product_links": 3, "field_proxy": True}, "normalize_min_max_judgment", "Recommenders, LLM assistants, catalog normalization, and checkout agents map directly to Shopify product capabilities.", "medium"),
            ],
            "caps": [],
        },
        {
            "label": "IP",
            "coverage_ratio": 0.62,
            "summary": "The public patent signal is real and technically specific, especially in checkout, recommendation, workflow automation, image/video AI, and contextual chatbot operation. The portfolio is not yet cleanly measurable as a complete five-year family series from open sources.",
            "strong": "Representative patents show concrete engineering around checkout latency, product recommendations, AI workflows, and merchant media/product data.",
            "missing": "A complete assignee-level patent-family time series across USPTO, WIPO, EPO, CIPO, and CNIPA was not reproducible from available network conditions.",
            "metrics": [
                metric("patent_family_growth", "Patent-family growth", 0.52, 0.34, ["ev_product_image_patent", "ev_contextual_product_patent", "ev_checkout_patent", "ev_workflow_ai_patent", "ev_chatbot_object_detection_patents"], {"representative_publication_signals_by_year": {"2021": 1, "2022": 1, "2023": 2, "2024": 2, "2025": 4}}, "source_screened_count_proxy", "Visible representative publications rise into 2025, but this is not a complete family census.", "high"),
                metric("technical_specificity", "Technical specificity", 0.76, 0.33, ["ev_product_image_patent", "ev_checkout_patent", "ev_workflow_ai_patent"], {"specific_domains": ["checkout", "workflow automation", "product image recommendations", "chatbot operation"]}, "normalize_min_max_judgment", "Claims and abstracts describe concrete platform mechanisms rather than only generic ecommerce concepts.", "medium"),
                metric("science_to_patent_or_assignee_quality", "Assignee quality", 0.66, 0.33, ["ev_company_patent_notice", "ev_workflow_ai_patent", "ev_chatbot_object_detection_patents"], {"company_assignee": True, "public_marking_non_comprehensive": True}, "normalize_min_max_judgment", "Assignee quality is high because filings are Shopify-attributable; completeness and legal status remain partial.", "medium"),
            ],
            "caps": [],
        },
        {
            "label": "Industrialization",
            "coverage_ratio": 0.90,
            "summary": "Shopify's innovation is already industrialized as production software: AI features are in admin, developer extensions exist, Agentic Storefronts are documented, and the platform runs at very large transaction scale with meaningful R&D spend.",
            "strong": "R&D scale, product documentation, developer surfaces, and operational metrics show repeatable platform engineering rather than lab-stage experimentation.",
            "missing": "For software, industrialization is not captured by factory capex; the company discloses limited direct reliability, latency, or model-performance metrics.",
            "metrics": [
                metric("manufacturing_or_deployment_evidence", "Deployment evidence", 0.90, 0.40, ["ev_agentic_docs", "ev_sidekick_docs", "ev_editions_ai"], {"documented_product_surfaces": 3, "ai_feature_clusters": 6}, "normalize_min_max_judgment", "Multiple AI product surfaces are documented for merchants and buyers.", "medium"),
                metric("process_learning_or_capex", "Process learning / spend", 0.72, 0.30, ["ev_revenue_rd_2025", "ev_q1_2026_capex"], {"rd_expense_usd_billion_2025": 1.536, "q1_2026_capex_usd_million": 5}, "normalize_min_max_judgment", "R&D spend is large; capex is low because Shopify scales through software and cloud infrastructure.", "medium"),
                metric("operational_scale_signal", "Operational scale", 0.92, 0.30, ["ev_gmv_2025", "ev_q1_2026_metrics", "ev_sidekick_extensions"], {"gmv_2025_usd_billion": 378.4, "q1_2026_gmv_usd_billion": 100.743}, "normalize_min_max_judgment", "The platform is operating at global commerce scale while adding new AI/developer surfaces.", "medium"),
            ],
            "caps": [],
        },
        {
            "label": "Adoption",
            "coverage_ratio": 0.87,
            "summary": "Adoption is the strongest layer: GMV, revenue, Payments penetration, Shop Pay, Sidekick usage, AI-search order growth, and enterprise/offline/B2B commentary all point to broad commercial pull.",
            "strong": "The platform is already clearing more than $100 billion of quarterly GMV, with payments penetration, merchant solutions revenue, Sidekick usage, and AI-channel traffic all rising.",
            "missing": "AI-specific absolute transaction volume and Sidekick retention are not disclosed, so the AI layer still needs base-rate transparency.",
            "metrics": [
                metric("revenue_or_booking_evidence", "Revenue / GMV evidence", 0.95, 0.40, ["ev_gmv_2025", "ev_q1_2026_metrics", "ev_payments_2025"], {"gmv_2025_usd_billion": 378.4, "revenue_2025_usd_billion": 11.556, "q1_2026_revenue_usd_billion": 3.170}, "normalize_min_max_judgment", "Sustained large-scale GMV and revenue growth indicate strong commercial adoption.", "low"),
                metric("customer_or_partner_breadth", "Customer / partner breadth", 0.86, 0.30, ["ev_ucp_agentic", "ev_agentic_docs", "ev_sidekick_adoption_q1"], {"named_ai_channels": 3, "ucp_endorsers_plus": 20, "sidekick_apps_q1": 12000}, "normalize_min_max_judgment", "Partner and merchant breadth is strong across AI channels and merchant-admin tooling.", "medium"),
                metric("repeatability_or_deployment_scale", "Deployment scale", 0.90, 0.30, ["ev_gmv_2025", "ev_ai_channel_adoption_q1", "ev_sidekick_adoption_q1"], {"ai_search_order_growth_x": 13, "ai_traffic_growth_x": 8, "sidekick_weekly_active_growth_x": 4}, "normalize_min_max_judgment", "Growth rates and GMV scale suggest repeatable deployment, though AI base volumes are not disclosed.", "medium"),
            ],
            "caps": [],
        },
        {
            "label": "Policy & Economics",
            "coverage_ratio": 0.75,
            "summary": "The policy and economics setup is supportive but not frictionless: open standards and channel integrations help, while privacy/data-sharing rules, platform dependency, lower merchant-solutions gross margin, and rising transaction/lending losses constrain the score.",
            "strong": "UCP, Agentic Storefronts, attribution, admin control, and processor-neutral checkout design all fit the emerging standards direction.",
            "missing": "No regulatory safe harbor exists for agentic commerce, and economic quality depends on payment-processing costs, credit losses, and AI-channel platform terms.",
            "metrics": [
                metric("regulatory_or_standards_fit", "Standards fit", 0.82, 0.34, ["ev_ucp_agentic", "ev_agentic_docs"], {"ucp_co_developed_with_google": True, "named_ai_channels": 3}, "normalize_min_max_judgment", "Open protocol and documented channel attribution are strong standards-readiness signals.", "medium"),
                metric("policy_or_supply_chain_support", "Policy / ecosystem support", 0.66, 0.33, ["ev_ucp_agentic", "ev_competition_ai_risk"], {"ecosystem_partners": ["Google", "Microsoft"], "ai_competition_risk": True}, "normalize_min_max_judgment", "Ecosystem support exists, but dependency on large AI/search platforms is a real strategic constraint.", "medium"),
                metric("economic_readiness", "Economic readiness", 0.66, 0.33, ["ev_q1_2026_metrics", "ev_loss_risk_2025", "ev_payments_2025"], {"q1_2026_fcf_margin_percent": 15, "transaction_loan_losses_2025_usd_million": 417, "payments_penetration_2025_percent": 65.6}, "normalize_min_max_judgment", "Free cash flow and payments penetration are positive; losses and lower-margin merchant-solutions mix temper economics.", "medium"),
            ],
            "caps": [],
        },
    ]

    claims = [
        {
            "claim_id": "claim_thesis_001",
            "section": "thesis",
            "text": "Shopify is best characterized as a high-quality applied commerce-platform innovator, not a hard-science breakthrough company.",
            "claim_type": "inference",
            "confidence": "High",
            "evidence_ids": ["ev_gmv_2025", "ev_revenue_rd_2025", "ev_sidekick_docs", "ev_bibliometric_review"],
            "source_ids": ["src_sec_2025_10k", "src_sidekick_help", "src_sciencedirect_bibliometric"],
        },
        {
            "claim_id": "claim_thesis_002",
            "section": "thesis",
            "text": "The strongest innovation evidence is adoption and industrialization: Shopify's AI and checkout infrastructure is already embedded in large-scale merchant workflows.",
            "claim_type": "inference",
            "confidence": "High",
            "evidence_ids": ["ev_q1_2026_metrics", "ev_agentic_docs", "ev_sidekick_adoption_q1"],
            "source_ids": ["src_q1_2026_release", "src_agentic_help", "src_fool_q1_transcript"],
        },
        {
            "claim_id": "claim_thesis_003",
            "section": "thesis",
            "text": "The weaker evidence is conventional science and complete IP time-series depth; both were treated as partial and scored conservatively.",
            "claim_type": "limitation",
            "confidence": "High",
            "evidence_ids": ["ev_bibliometric_review", "ev_company_patent_notice", "ev_chatbot_object_detection_patents"],
            "source_ids": ["src_sciencedirect_bibliometric", "src_shopify_patents", "src_ipqwery_shopify_patents"],
        },
        {
            "claim_id": "claim_gate_001",
            "section": "breakthrough_gate",
            "text": "The breakthrough gate passes because Industrialization and Adoption both score at least 3 with adequate confidence, but the verdict remains translational momentum rather than exceptional breakthrough.",
            "claim_type": "inference",
            "confidence": "High",
            "evidence_ids": ["ev_q1_2026_metrics", "ev_sidekick_adoption_q1", "ev_agentic_docs"],
            "source_ids": ["src_q1_2026_release", "src_fool_q1_transcript", "src_agentic_help"],
        },
        {
            "claim_id": "claim_watch_001",
            "section": "watchlist",
            "text": "A durable AI-channel revenue base, disclosed absolute AI-order volumes, and granted AI workflow patents would upgrade the view.",
            "claim_type": "monitoring_trigger",
            "confidence": "Medium",
            "evidence_ids": ["ev_ai_channel_adoption_q1", "ev_workflow_ai_patent"],
            "source_ids": ["src_fool_q1_transcript", "src_justia_workflow_ai"],
        },
    ]

    dashboard_content = {
        "hero": {
            "headline": "Shopify Innovation Readiness",
            "subheadline": "Absolute readiness assessment for NASDAQ: SHOP, focused on agentic commerce, merchant AI tooling, checkout/payments infrastructure, and applied recommendation systems.",
            "verdict_label": "Strong innovator with translational momentum",
            "evidence_ids": ["ev_q1_2026_metrics", "ev_gmv_2025", "ev_sidekick_adoption_q1"],
            "source_ids": ["src_q1_2026_release", "src_sec_2025_10k", "src_fool_q1_transcript"],
        },
        "thesis": {
            "title": "Thesis",
            "summary": "Shopify's innovation edge is not academic publication volume. It is applied commerce infrastructure deployed across merchants, buyers, payments, developer extensions, and emerging AI shopping channels.",
            "bullets": [
                {
                    "text": "The company is already commercializing AI through Sidekick, Agentic Storefronts, Shopify Catalog, UCP, and checkout integrations rather than waiting for lab-stage validation.",
                    "claim_ids": ["claim_thesis_002"],
                    "evidence_ids": ["ev_sidekick_docs", "ev_agentic_docs", "ev_ucp_agentic"],
                    "source_ids": ["src_sidekick_help", "src_agentic_help", "src_agentic_press"],
                },
                {
                    "text": "Adoption is unusually strong for a platform innovation thesis: 2025 GMV was $378.4B and Q1 2026 GMV was $100.7B, while Payments penetration reached 65.6% in 2025.",
                    "claim_ids": ["claim_thesis_002"],
                    "evidence_ids": ["ev_gmv_2025", "ev_q1_2026_metrics", "ev_payments_2025"],
                    "source_ids": ["src_sec_2025_10k", "src_q1_2026_release"],
                },
                {
                    "text": "The cautious part: visible patents and field science are real, but the complete Shopify-specific patent-family and publication time series was not reproducible in this run.",
                    "claim_ids": ["claim_thesis_003"],
                    "evidence_ids": ["ev_bibliometric_review", "ev_company_patent_notice", "ev_chatbot_object_detection_patents"],
                    "source_ids": ["src_sciencedirect_bibliometric", "src_shopify_patents", "src_ipqwery_shopify_patents"],
                },
            ],
        },
        "technology_map": {
            "title": "Technology Map",
            "summary": "The investable innovation thesis is concentrated in three applied platform domains.",
            "items": [
                {
                    "name": "Agentic commerce rails",
                    "description": "UCP, Agentic Storefronts, Shopify Catalog, Google AI Mode/Gemini, Microsoft Copilot Checkout, and ChatGPT channel support move Shopify from storefront software into AI-mediated transaction infrastructure.",
                    "maturity": "scaling",
                    "evidence_ids": ["ev_ucp_agentic", "ev_agentic_docs", "ev_ai_channel_adoption_q1"],
                    "source_ids": ["src_agentic_press", "src_agentic_help", "src_fool_q1_transcript"],
                },
                {
                    "name": "Merchant AI operating layer",
                    "description": "Sidekick, Pulse, AI theme/block generation, custom-app generation, and app extensions give merchants AI-assisted operations inside Shopify admin.",
                    "maturity": "commercial",
                    "evidence_ids": ["ev_sidekick_docs", "ev_sidekick_extensions", "ev_sidekick_adoption_q1", "ev_editions_ai"],
                    "source_ids": ["src_sidekick_help", "src_sidekick_dev", "src_fool_q1_transcript", "src_editions_summer25"],
                },
                {
                    "name": "Checkout, payments, and risk infrastructure",
                    "description": "Shopify Payments, Shop Pay, checkout patents, delayed checkout option loading, fraud/loss management, and attribution make the commerce stack repeatable across channels.",
                    "maturity": "commercial",
                    "evidence_ids": ["ev_payments_2025", "ev_checkout_patent", "ev_loss_risk_2025"],
                    "source_ids": ["src_sec_2025_10k", "src_google_checkout_patent"],
                },
            ],
        },
        "quantitative_signals": {
            "title": "Quantitative Signals",
            "summary": "Company-scale metrics are strong; publication and patent trend signals are source-screened proxies and should be refreshed with a full database export.",
            "charts": [
                {
                    "chart_id": "chart_revenue_gmv",
                    "title": "Revenue and GMV scale",
                    "description": "Shopify revenue and GMV both accelerated into 2025; Q1 2026 already cleared $100B quarterly GMV.",
                    "series": [
                        {"label": "Revenue", "unit": "USD billions", "points": [{"period": "2023", "value": 7.060}, {"period": "2024", "value": 8.880}, {"period": "2025", "value": 11.556}, {"period": "Q1 2026", "value": 3.170}]},
                        {"label": "GMV", "unit": "USD billions", "points": [{"period": "2023", "value": 235.9}, {"period": "2024", "value": 292.3}, {"period": "2025", "value": 378.4}, {"period": "Q1 2026", "value": 100.743}]},
                    ],
                    "evidence_ids": ["ev_gmv_2025", "ev_q1_2026_metrics"],
                    "source_ids": ["src_sec_2025_10k", "src_q1_2026_release"],
                },
                {
                    "chart_id": "chart_rd",
                    "title": "R&D intensity",
                    "description": "R&D expense stayed above $1.3B in each of the last three fiscal years, shifting from post-logistics restructuring to scaled product engineering.",
                    "series": [
                        {"label": "R&D expense", "unit": "USD billions", "points": [{"period": "2023", "value": 1.730}, {"period": "2024", "value": 1.367}, {"period": "2025", "value": 1.536}]}
                    ],
                    "evidence_ids": ["ev_revenue_rd_2025"],
                    "source_ids": ["src_sec_2025_10k"],
                },
                {
                    "chart_id": "chart_patents",
                    "title": "Representative patent publication signals",
                    "description": "Source-screened patent signals rose into 2025, but this is a representative screen, not a complete patent-family census.",
                    "series": [
                        {"label": "Observed signals", "unit": "publications/families", "points": [{"period": "2021", "value": 1}, {"period": "2022", "value": 1}, {"period": "2023", "value": 2}, {"period": "2024", "value": 2}, {"period": "2025", "value": 4}]}
                    ],
                    "evidence_ids": ["ev_product_image_patent", "ev_contextual_product_patent", "ev_checkout_patent", "ev_workflow_ai_patent", "ev_chatbot_object_detection_patents"],
                    "source_ids": ["src_google_product_image_patent", "src_google_contextual_product_patent", "src_google_checkout_patent", "src_justia_workflow_ai", "src_ipqwery_shopify_patents"],
                },
                {
                    "chart_id": "chart_publications",
                    "title": "Science proxy",
                    "description": "The strongest publication datapoint found was a 2024 bibliometric review: 120 documents identified, 91 analyzed, and 97.16% growth reported for AI and recommender systems in e-commerce.",
                    "series": [
                        {"label": "Screened field records", "unit": "documents", "points": [{"period": "Identified", "value": 120}, {"period": "Analyzed", "value": 91}]}
                    ],
                    "evidence_ids": ["ev_bibliometric_review"],
                    "source_ids": ["src_sciencedirect_bibliometric"],
                },
            ],
        },
        "commercialization_evidence": {
            "title": "Commercialization Evidence",
            "summary": "Commercialization is already visible in platform usage, payments penetration, AI-channel traffic, and merchant tooling.",
            "items": [
                {
                    "label": "Scale",
                    "text": "2025 GMV reached $378.4B and Q1 2026 GMV reached $100.7B, showing the platform can deploy new commerce infrastructure at very large scale.",
                    "evidence_ids": ["ev_gmv_2025", "ev_q1_2026_metrics"],
                    "source_ids": ["src_sec_2025_10k", "src_q1_2026_release"],
                },
                {
                    "label": "AI workflow adoption",
                    "text": "Sidekick showed sharp usage growth in Q1 2026, including more than 12,000 custom apps created with Sidekick in the quarter.",
                    "evidence_ids": ["ev_sidekick_adoption_q1"],
                    "source_ids": ["src_fool_q1_transcript"],
                },
                {
                    "label": "AI channel demand",
                    "text": "Management disclosed 8x AI-driven traffic growth and nearly 13x AI-search order growth, but did not disclose absolute base volumes.",
                    "evidence_ids": ["ev_ai_channel_adoption_q1"],
                    "source_ids": ["src_fool_q1_transcript"],
                },
            ],
        },
        "breakthrough_gate": {
            "title": "Breakthrough Gate",
            "summary": "The gate passes on commercial readiness but not on scientific breakthrough purity.",
            "conditions_met": [
                {
                    "condition": "Industrialization is above 3 because Shopify's AI tooling, agentic storefronts, developer extensions, and checkout infrastructure are production software surfaces.",
                    "evidence_ids": ["ev_agentic_docs", "ev_sidekick_docs", "ev_sidekick_extensions"],
                    "source_ids": ["src_agentic_help", "src_sidekick_help", "src_sidekick_dev"],
                },
                {
                    "condition": "Adoption is above 3 because platform GMV, revenue, payments penetration, and AI-tool usage all show commercial pull.",
                    "evidence_ids": ["ev_gmv_2025", "ev_q1_2026_metrics", "ev_payments_2025", "ev_sidekick_adoption_q1"],
                    "source_ids": ["src_sec_2025_10k", "src_q1_2026_release", "src_fool_q1_transcript"],
                },
            ],
            "conditions_not_met": [
                {
                    "condition": "Science and IP are not strong enough to call Shopify a hard-science breakthrough candidate; the visible edge is applied system design and distribution.",
                    "evidence_ids": ["ev_bibliometric_review", "ev_company_patent_notice"],
                    "source_ids": ["src_sciencedirect_bibliometric", "src_shopify_patents"],
                },
                {
                    "condition": "AI-channel order growth lacks absolute volume disclosure, which makes the base-rate interpretation uncertain.",
                    "evidence_ids": ["ev_ai_channel_adoption_q1"],
                    "source_ids": ["src_fool_q1_transcript"],
                },
            ],
            "result": "Pass for translational momentum; not enough for exceptional breakthrough classification.",
        },
        "university_research_signals": {
            "title": "University Research",
            "summary": "University signals support the field around Shopify's product direction, especially intent-aware recommendation, personalization, and search/recommendation behavior.",
            "institutions": [
                {
                    "name": "Stanford University",
                    "signal": "2025 work on intent-structured AI recommendation systems emphasizes customer intent and human domain knowledge, directly adjacent to commerce personalization.",
                    "company_attributable": False,
                    "field_proxy": True,
                    "evidence_ids": ["ev_university_research"],
                    "source_ids": ["src_stanford_recsys"],
                },
                {
                    "name": "Massachusetts Institute of Technology",
                    "signal": "MIT research on online preference updating gives a technical foundation for real-time personalization systems.",
                    "company_attributable": False,
                    "field_proxy": True,
                    "evidence_ids": ["ev_mit_harvard_research"],
                    "source_ids": ["src_mit_discrete_choice"],
                },
                {
                    "name": "Harvard Digital Data Design Institute",
                    "signal": "Harvard D3 describes an AI-era keyword recommender field experiment and reports a 1.2% purchase lift in a mobile food-delivery platform.",
                    "company_attributable": False,
                    "field_proxy": True,
                    "evidence_ids": ["ev_mit_harvard_research"],
                    "source_ids": ["src_harvard_krs"],
                },
            ],
        },
        "patent_signals": {
            "title": "Patents",
            "summary": "Visible patents are specific enough to support engineering seriousness, but the dashboard treats the five-year patent trend as representative rather than exhaustive.",
            "families": [
                {
                    "title": "Systems and methods for providing product image recommendations",
                    "publication_or_family_id": "US20210125251A1 / US11386473B2 / US12002079B2",
                    "jurisdictions": ["US", "EP", "CA", "CN"],
                    "priority_date": "2019-10-24",
                    "interpretation": "Shows applied AI/computer-vision style merchant tooling around product presentation and recommendation.",
                    "evidence_ids": ["ev_product_image_patent"],
                    "source_ids": ["src_google_product_image_patent"],
                },
                {
                    "title": "Systems and method for providing contextual product recommendations",
                    "publication_or_family_id": "US20230260004A1",
                    "jurisdictions": ["US"],
                    "priority_date": "2022-02-16",
                    "interpretation": "Checkout-context recommendation work; abandoned status limits legal weight but still shows engineering exploration.",
                    "evidence_ids": ["ev_contextual_product_patent"],
                    "source_ids": ["src_google_contextual_product_patent"],
                },
                {
                    "title": "E-commerce checkout with delay loading of checkout options",
                    "publication_or_family_id": "US12243026B2",
                    "jurisdictions": ["US"],
                    "priority_date": "2021-09-02",
                    "interpretation": "Specific checkout-infrastructure patent relevant to conversion, latency, and option-loading complexity.",
                    "evidence_ids": ["ev_checkout_patent"],
                    "source_ids": ["src_google_checkout_patent"],
                },
                {
                    "title": "Construction of workflow automation using artificial intelligence",
                    "publication_or_family_id": "US20250272062",
                    "jurisdictions": ["US"],
                    "priority_date": "2024-02-26",
                    "interpretation": "LLM and vector-embedding workflow automation maps closely to Sidekick and Shopify Flow-style merchant automation.",
                    "evidence_ids": ["ev_workflow_ai_patent"],
                    "source_ids": ["src_justia_workflow_ai"],
                },
                {
                    "title": "Contextual chatbot operation",
                    "publication_or_family_id": "WO2025/102145",
                    "jurisdictions": ["PCT/WIPO"],
                    "priority_date": "2024-03-01",
                    "interpretation": "Directly relevant to contextual AI assistant behavior in commerce workflows.",
                    "evidence_ids": ["ev_chatbot_object_detection_patents"],
                    "source_ids": ["src_ipqwery_shopify_patents"],
                },
            ],
            "interpretation": "The visible patent set supports concrete applied engineering in checkout, recommendation, workflow automation, and merchant/buyer AI interfaces. It does not yet support a high-confidence claim that Shopify's patent-family growth is accelerating across the complete portfolio.",
        },
        "red_flags": [
            {
                "red_flag_id": "rf_science_gap",
                "title": "Company science signal is thin",
                "text": "Shopify's relevant science is mostly field-level and product-applied. No strong Shopify-authored academic publication series was found.",
                "severity": "medium",
                "layer": "Science",
                "evidence_ids": ["ev_bibliometric_review", "ev_university_research"],
                "source_ids": ["src_sciencedirect_bibliometric", "src_stanford_recsys"],
                "claim_ids": ["claim_thesis_003"],
            },
            {
                "red_flag_id": "rf_patent_census",
                "title": "Patent trend is incomplete",
                "text": "Representative patents are visible, but open-source access did not produce a complete five-year assignee-level family count.",
                "severity": "medium",
                "layer": "IP",
                "evidence_ids": ["ev_company_patent_notice", "ev_product_image_patent", "ev_chatbot_object_detection_patents"],
                "source_ids": ["src_shopify_patents", "src_google_product_image_patent", "src_ipqwery_shopify_patents"],
                "claim_ids": ["claim_thesis_003"],
            },
            {
                "red_flag_id": "rf_ai_base_rates",
                "title": "AI-channel growth lacks base rates",
                "text": "AI-driven traffic and AI-search orders grew rapidly, but management did not disclose absolute volumes in the reviewed sources.",
                "severity": "medium",
                "layer": "Adoption",
                "evidence_ids": ["ev_ai_channel_adoption_q1"],
                "source_ids": ["src_fool_q1_transcript"],
                "claim_ids": ["claim_watch_001"],
            },
            {
                "red_flag_id": "rf_economics_losses",
                "title": "Payments and lending losses are rising",
                "text": "Transaction and loan losses increased to $417M in 2025, so embedded finance scale brings risk-management burden.",
                "severity": "medium",
                "layer": "Policy & Economics",
                "evidence_ids": ["ev_loss_risk_2025"],
                "source_ids": ["src_sec_2025_10k"],
                "claim_ids": [],
            },
            {
                "red_flag_id": "rf_platform_dependency",
                "title": "AI commerce depends on powerful external channels",
                "text": "Google, Microsoft, ChatGPT, and other AI surfaces can help distribution, but they also control buyer access and terms.",
                "severity": "medium",
                "layer": "Policy & Economics",
                "evidence_ids": ["ev_ucp_agentic", "ev_competition_ai_risk"],
                "source_ids": ["src_agentic_press", "src_sec_2025_10k"],
                "claim_ids": [],
            },
        ],
        "watchlist": {
            "title": "What Would Change The View",
            "upgrade_signals": [
                {"text": "Disclose absolute GMV or order count from AI channels, not just growth multiples.", "monitoring_source": "Quarterly earnings releases and transcripts"},
                {"text": "Show Sidekick retention, active-shop base, and measured merchant productivity or conversion uplift.", "monitoring_source": "Investor presentations, product analytics disclosures, merchant case studies"},
                {"text": "Publish or expose a clean patent-family export showing rising AI, checkout, and agentic-commerce families across USPTO, WIPO, EPO, CIPO, and CNIPA.", "monitoring_source": "Patent databases and company IP disclosures"},
                {"text": "Evidence that UCP becomes a broad de facto standard beyond Shopify/Google/Microsoft launch partners.", "monitoring_source": "UCP technical council updates, Google/Microsoft/OpenAI commerce documentation"},
            ],
            "downgrade_signals": [
                {"text": "AI-search order growth stalls after early low-base gains.", "monitoring_source": "Quarterly earnings calls"},
                {"text": "Transaction and loan losses continue to rise faster than payments GMV or merchant-solutions gross profit.", "monitoring_source": "SEC filings"},
                {"text": "Large AI/search platforms favor native commerce stacks or restrict Shopify's control over checkout and attribution.", "monitoring_source": "Platform partner documentation and risk-factor updates"},
                {"text": "Sidekick or agentic storefronts remain feature-rich but fail to show repeated merchant usage or revenue contribution.", "monitoring_source": "Product analytics disclosures and merchant adoption metrics"},
            ],
            "cadence": [
                {"frequency": "quarterly", "task": "Refresh SEC filings, earnings transcript, GMV, Payments penetration, AI-channel adoption, and transaction-loss data."},
                {"frequency": "semiannual", "task": "Rebuild patent and publication time series with database exports if network access allows."},
            ],
        },
        "operational_snapshot": {
            "title": "Operational Snapshot",
            "metrics": [
                {"label": "2025 GMV", "value": "$378.4B", "period": "FY2025", "evidence_ids": ["ev_gmv_2025"], "source_ids": ["src_sec_2025_10k"]},
                {"label": "2025 revenue", "value": "$11.556B", "period": "FY2025", "evidence_ids": ["ev_revenue_rd_2025"], "source_ids": ["src_sec_2025_10k"]},
                {"label": "2025 R&D", "value": "$1.536B", "period": "FY2025", "evidence_ids": ["ev_revenue_rd_2025"], "source_ids": ["src_sec_2025_10k"]},
                {"label": "Payments penetration", "value": "65.6%", "period": "FY2025", "evidence_ids": ["ev_payments_2025"], "source_ids": ["src_sec_2025_10k"]},
                {"label": "Q1 2026 GMV", "value": "$100.743B", "period": "Q1 2026", "evidence_ids": ["ev_q1_2026_metrics"], "source_ids": ["src_q1_2026_release"]},
                {"label": "Q1 2026 FCF margin", "value": "15%", "period": "Q1 2026", "evidence_ids": ["ev_q1_2026_metrics"], "source_ids": ["src_q1_2026_release"]},
            ],
        },
        "method_notes": {
            "title": "Method Notes",
            "notes": [
                "This is an absolute innovation readiness score for Shopify alone; it is not a peer percentile.",
                "Scores were generated by the deterministic scorer from normalized metrics, weights, and coverage ratios in payload.json.",
                "Science metrics use field-level proxies because Shopify is not primarily an academic publisher.",
                "Patent metrics use representative public patent signals. A complete patent-family census should be refreshed with direct database exports.",
                "Publication and patent five-year trend charts in this dashboard are labeled as proxies where they are not exhaustive.",
            ],
        },
        "bottom_line": {
            "title": "Bottom Line",
            "text": "Shopify clears the commercial-readiness gate. The strongest conclusion is translational momentum in AI-enabled commerce infrastructure, not a claim of exceptional hard-science breakthrough.",
            "claim_ids": ["claim_thesis_001", "claim_gate_001"],
            "evidence_ids": ["ev_q1_2026_metrics", "ev_gmv_2025", "ev_sidekick_adoption_q1", "ev_bibliometric_review"],
            "source_ids": ["src_q1_2026_release", "src_sec_2025_10k", "src_fool_q1_transcript", "src_sciencedirect_bibliometric"],
        },
    }

    payload = {
        "schema_version": "2.1",
        "company": "Shopify Inc.",
        "ticker": "NASDAQ: SHOP",
        "mode": "absolute",
        "benchmark_ready": True,
        "skill_metadata": {
            "skill_name": "technology-innovation-analysis",
            "skill_version": "1.2.0",
            "skill_path": ".codex/skills/technology-innovation-analysis/SKILL.md",
            "scorer_name": "score_innovation_benchmark.py",
            "scorer_version": "1.2.0",
            "metric_rules_version": "1.2.0",
        },
        "research_run": {
            "research_date": "2026-05-07",
            "analyst": "codex",
            "run_id": "run-20260507-innovation-dashboard",
            "user_request": "Research Shopify Inc., NASDAQ: SHOP using the innovation-analysis skill and present the results in a Desert Rose dashboard.",
            "time_horizon": "Five years where source coverage allowed, with Q1 2026 current update.",
            "research_mode": "web_research_with_deterministic_scoring",
        },
        "research_context": {
            "focus_technologies": ["Agentic commerce rails", "Merchant AI operating layer", "Checkout, payments, and risk infrastructure"],
            "company_identifiers": {"legal_name": "Shopify Inc.", "ticker": "NASDAQ: SHOP", "cik": "0001594805"},
            "source_availability": [
                {"domain": "SEC filings", "status": "available", "note": "2025 Form 10-K and Q1 2026 press release were available."},
                {"domain": "company product documentation", "status": "available", "note": "Shopify help, developer, news, legal, and Editions pages were available."},
                {"domain": "patents", "status": "partial", "note": "Representative public patent records were available; complete five-year assignee family counts were not reproducible."},
                {"domain": "scientometrics", "status": "partial", "note": "OpenAlex API access failed locally; used academic and university sources as field-level proxies."},
            ],
            "search_log": [
                {"query": "Shopify 2025 Form 10-K GMV R&D Payments penetration", "source": "web_search", "date": "2026-05-07", "result_quality": "high", "selected": True, "selection_reason": "Primary SEC filing."},
                {"query": "Shopify Q1 2026 financial results GMV revenue AI Sidekick", "source": "web_search", "date": "2026-05-07", "result_quality": "high", "selected": True, "selection_reason": "Latest quarterly evidence."},
                {"query": "Shopify agentic commerce UCP Google Microsoft Copilot", "source": "web_search", "date": "2026-05-07", "result_quality": "high", "selected": True, "selection_reason": "Primary product announcement."},
                {"query": "Shopify patents AI checkout recommendation Sidekick", "source": "web_search", "date": "2026-05-07", "result_quality": "medium", "selected": True, "selection_reason": "Representative patent evidence."},
                {"query": "AI recommender systems e-commerce bibliometric review Stanford MIT Harvard", "source": "web_search", "date": "2026-05-07", "result_quality": "medium", "selected": True, "selection_reason": "Field-level science proxy."},
            ],
            "exclusions": [
                {"candidate_source_or_metric": "Unverified blog claims about AI-commerce order growth", "reason": "Excluded unless supported by transcript or primary company source."},
                {"candidate_source_or_metric": "Stock price and analyst targets", "reason": "Not necessary for innovation readiness and highly market-sensitive."},
                {"candidate_source_or_metric": "Complete OpenAlex publication time series", "reason": "Local network DNS failure prevented reproducible API retrieval."},
            ],
            "judgment_calls": [
                {"topic": "Science proxy", "decision": "Used field-level recommender/AI-commerce research instead of Shopify-authored publication counts.", "rationale": "Shopify's innovation is product/platform engineering; no company-authored publication series was found.", "impact": "Lowered Science score and confidence."},
                {"topic": "Patent trend", "decision": "Used source-screened representative patent signals by year.", "rationale": "Open patent sources showed relevant records but not a clean complete assignee-level family series.", "impact": "Lowered IP score and confidence."},
                {"topic": "Industrialization definition", "decision": "Treated documented production software and platform scale as industrialization evidence.", "rationale": "For Shopify, process maturity is software deployment and operational scale, not factory production.", "impact": "Raised Industrialization score while noting low physical capex."},
            ],
        },
        "sources": sources,
        "evidence_items": evidence_items,
        "layers": layers,
        "dashboard_content": dashboard_content,
        "claims": claims,
        "normalization_notes": [
            {"metric_code": "publication_growth", "rule": "source-screened field proxy with confidence penalty", "reason": "OpenAlex was unavailable; academic review gives field-level growth evidence."},
            {"metric_code": "patent_family_growth", "rule": "representative public patent-signal count, not complete census", "reason": "Patent databases were available as snippets/pages but not as complete export."},
            {"metric_code": "revenue_or_booking_evidence", "rule": "judgmental min-max on platform GMV/revenue scale", "reason": "Absolute scale and growth are economically meaningful for software platform adoption."},
            {"metric_code": "regulatory_or_standards_fit", "rule": "judgmental score based on standards, attribution, and data-sharing documentation", "reason": "Agentic commerce standards are emerging and lack mature regulatory metrics."},
        ],
        "storage_metadata": {
            "intended_store": "sqlite",
            "recommended_primary_keys": {"sources": "source_id", "evidence_items": "evidence_id", "metrics": "company + research_date + run_id + layer + metric_code"},
            "content_hash_fields": ["sources", "evidence_items", "layers", "dashboard_content", "claims", "normalization_notes"],
        },
    }
    return payload


def write_payload() -> None:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    payload = build_payload()
    PAYLOAD_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(PAYLOAD_PATH)


def build_dashboard_html(scored: dict) -> str:
    embedded = json.dumps(scored, ensure_ascii=True)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Shopify Innovation Readiness Dashboard</title>
  <style>
    :root {{
      --rose: #d4a5a5;
      --clay: #b87d6d;
      --sand: #e8d5c4;
      --burgundy: #5d2e46;
      --ink: #241923;
      --muted: #6b5962;
      --paper: #fffaf7;
      --line: rgba(93, 46, 70, 0.18);
      --track: rgba(93, 46, 70, 0.12);
      --green: #487067;
      --amber: #ad7c37;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: FreeSans, Arial, sans-serif;
      color: var(--ink);
      background:
        linear-gradient(135deg, rgba(232,213,196,0.88), rgba(255,250,247,0.92) 42%, rgba(212,165,165,0.36)),
        var(--paper);
    }}
    button, input, select {{ font: inherit; }}
    .shell {{
      min-height: 100svh;
      display: grid;
      grid-template-columns: 248px minmax(0, 1fr);
    }}
    .nav {{
      position: sticky;
      top: 0;
      height: 100svh;
      padding: 28px 22px;
      border-right: 1px solid var(--line);
      background: rgba(255, 250, 247, 0.72);
      backdrop-filter: blur(18px);
    }}
    .brand {{
      font-family: FreeSans, Arial, sans-serif;
      font-weight: 800;
      font-size: 19px;
      line-height: 1.1;
      color: var(--burgundy);
      letter-spacing: 0;
    }}
    .ticker {{
      margin-top: 8px;
      font-size: 12px;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: .08em;
    }}
    .navlinks {{
      display: grid;
      gap: 5px;
      margin-top: 34px;
    }}
    .navlinks a {{
      color: var(--muted);
      text-decoration: none;
      padding: 8px 0;
      font-size: 14px;
    }}
    .navlinks a:hover {{ color: var(--burgundy); }}
    main {{
      padding: 34px min(4vw, 54px) 54px;
    }}
    .top {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) 340px;
      gap: 30px;
      align-items: stretch;
      border-bottom: 1px solid var(--line);
      padding-bottom: 30px;
    }}
    .eyebrow {{
      color: var(--clay);
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: .11em;
      margin-bottom: 10px;
    }}
    h1 {{
      margin: 0;
      max-width: 820px;
      font-family: FreeSans, Arial, sans-serif;
      font-size: clamp(40px, 6vw, 82px);
      line-height: .95;
      letter-spacing: 0;
      color: var(--burgundy);
    }}
    .subheadline {{
      margin: 18px 0 0;
      max-width: 760px;
      color: var(--muted);
      font-size: 18px;
      line-height: 1.45;
    }}
    .summary-row {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
      margin-top: 28px;
    }}
    .metric {{
      border-top: 1px solid var(--line);
      padding-top: 12px;
      min-width: 0;
    }}
    .metric .value {{
      font-size: 26px;
      font-weight: 800;
      color: var(--ink);
    }}
    .metric .label {{
      margin-top: 4px;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.35;
    }}
    .score-panel {{
      border-left: 1px solid var(--line);
      padding-left: 26px;
      display: grid;
      align-content: center;
      gap: 18px;
    }}
    .score-ring {{
      width: 210px;
      aspect-ratio: 1;
      border-radius: 50%;
      display: grid;
      place-items: center;
      background: conic-gradient(var(--burgundy) calc(var(--score-pct) * 1%), rgba(93,46,70,.12) 0);
      position: relative;
      box-shadow: 0 24px 60px rgba(93,46,70,.14);
    }}
    .score-ring::after {{
      content: "";
      position: absolute;
      inset: 13px;
      border-radius: 50%;
      background: var(--paper);
    }}
    .score-center {{
      position: relative;
      z-index: 1;
      text-align: center;
    }}
    .score-center strong {{
      display: block;
      font-size: 52px;
      color: var(--burgundy);
      line-height: 1;
    }}
    .score-center span {{ color: var(--muted); font-size: 13px; }}
    .verdict {{
      color: var(--burgundy);
      font-weight: 800;
      line-height: 1.25;
      font-size: 18px;
    }}
    .section {{
      display: grid;
      grid-template-columns: minmax(180px, 250px) minmax(0, 1fr);
      gap: 34px;
      padding: 34px 0;
      border-bottom: 1px solid var(--line);
    }}
    .section h2 {{
      margin: 0;
      color: var(--burgundy);
      font-size: 22px;
      line-height: 1.15;
    }}
    .section .note {{
      margin-top: 10px;
      color: var(--muted);
      font-size: 14px;
      line-height: 1.45;
    }}
    .stack {{ display: grid; gap: 18px; }}
    .layer {{
      display: grid;
      gap: 9px;
      padding: 18px 0;
      border-top: 1px solid var(--line);
    }}
    .layer:first-child {{ border-top: 0; padding-top: 0; }}
    .layer-head {{
      display: grid;
      grid-template-columns: 150px minmax(0, 1fr) 56px;
      gap: 16px;
      align-items: center;
    }}
    .layer-name {{ font-weight: 800; color: var(--ink); }}
    .bar {{
      height: 8px;
      border-radius: 999px;
      background: var(--track);
      overflow: hidden;
    }}
    .bar > span {{
      display: block;
      height: 100%;
      width: var(--w);
      border-radius: inherit;
      background: linear-gradient(90deg, var(--clay), var(--burgundy));
      box-shadow: 0 0 18px rgba(184,125,109,.34);
    }}
    .layer-score {{ text-align: right; font-weight: 800; color: var(--burgundy); }}
    .layer p {{ margin: 0; color: var(--muted); line-height: 1.45; }}
    .layer-meta {{
      display: flex;
      gap: 14px;
      flex-wrap: wrap;
      color: var(--muted);
      font-size: 12px;
    }}
    .grid-2 {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 22px;
    }}
    .panel {{
      border-top: 1px solid var(--line);
      padding-top: 16px;
      min-width: 0;
    }}
    .panel h3 {{
      margin: 0 0 8px;
      color: var(--ink);
      font-size: 17px;
    }}
    .panel p, li {{
      color: var(--muted);
      line-height: 1.45;
      font-size: 14px;
    }}
    ul {{ margin: 10px 0 0; padding-left: 18px; }}
    .chart {{
      height: 240px;
      width: 100%;
      overflow: visible;
    }}
    .chart text {{ fill: var(--muted); font-size: 11px; }}
    .chart .axis {{ stroke: rgba(93,46,70,.18); stroke-width: 1; }}
    .chart .line-a {{ fill: none; stroke: var(--burgundy); stroke-width: 3; }}
    .chart .line-b {{ fill: none; stroke: var(--green); stroke-width: 3; }}
    .chart .dot-a {{ fill: var(--burgundy); }}
    .chart .dot-b {{ fill: var(--green); }}
    .snapshot {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 16px;
    }}
    .source-list {{
      columns: 2;
      column-gap: 34px;
    }}
    .source-list a {{
      color: var(--burgundy);
      text-decoration-thickness: 1px;
      text-underline-offset: 2px;
      overflow-wrap: anywhere;
    }}
    .source-item {{
      break-inside: avoid;
      margin: 0 0 12px;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.35;
    }}
    .fade-in {{
      opacity: 0;
      transform: translateY(12px);
      animation: enter .55s ease forwards;
    }}
    @keyframes enter {{
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    @media (max-width: 980px) {{
      .shell {{ grid-template-columns: 1fr; }}
      .nav {{ position: static; height: auto; border-right: 0; border-bottom: 1px solid var(--line); }}
      .navlinks {{ grid-template-columns: repeat(3, minmax(0, 1fr)); margin-top: 18px; }}
      .top {{ grid-template-columns: 1fr; }}
      .score-panel {{ border-left: 0; border-top: 1px solid var(--line); padding-left: 0; padding-top: 24px; }}
      .section {{ grid-template-columns: 1fr; gap: 18px; }}
      .grid-2, .summary-row, .snapshot {{ grid-template-columns: 1fr; }}
      .source-list {{ columns: 1; }}
    }}
    @media (max-width: 620px) {{
      main {{ padding: 24px 18px 42px; }}
      .layer-head {{ grid-template-columns: 1fr 52px; }}
      .layer-head .bar {{ grid-column: 1 / -1; grid-row: 2; }}
      .navlinks {{ grid-template-columns: 1fr 1fr; }}
      .score-ring {{ width: 180px; }}
    }}
  </style>
</head>
<body>
  <script id="scored-data" type="application/json">{embedded}</script>
  <div class="shell">
    <aside class="nav">
      <div class="brand" id="nav-company"></div>
      <div class="ticker" id="nav-ticker"></div>
      <nav class="navlinks">
        <a href="#layers">Layers</a>
        <a href="#signals">Signals</a>
        <a href="#commercial">Commercialization</a>
        <a href="#science">Science</a>
        <a href="#patents">Patents</a>
        <a href="#sources">Sources</a>
      </nav>
    </aside>
    <main id="app"></main>
  </div>
  <script>
    const data = JSON.parse(document.getElementById('scored-data').textContent);
    const content = data.dashboard_content;
    const srcById = new Map((data.sources || []).map(s => [s.source_id, s]));
    document.getElementById('nav-company').textContent = data.company;
    document.getElementById('nav-ticker').textContent = data.ticker + ' / ' + data.research_run.research_date;

    const esc = (value) => String(value ?? '').replace(/[&<>"']/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));
    const pct = value => Math.max(0, Math.min(100, (Number(value) / 5) * 100));
    const refs = ids => (ids || []).map(id => {{
      const s = srcById.get(id);
      return s ? `<a href="${{esc(s.url)}}" target="_blank" rel="noopener">${{esc(s.title)}}</a>` : esc(id);
    }}).join('; ');

    function renderChart(chart) {{
      const series = chart.series || [];
      const points = series.flatMap(s => s.points || []);
      const max = Math.max(...points.map(p => Number(p.value)), 1);
      const labels = [...new Set(points.map(p => p.period))];
      const w = 620, h = 210, pad = 34;
      const x = i => pad + (labels.length === 1 ? 0 : i * ((w - pad * 2) / (labels.length - 1)));
      const y = v => h - pad - (Number(v) / max) * (h - pad * 2);
      const line = (s) => (s.points || []).map(p => `${{x(labels.indexOf(p.period))}},${{y(p.value)}}`).join(' ');
      const lineEls = series.map((s, i) => `<polyline class="line-${{i === 0 ? 'a' : 'b'}}" points="${{line(s)}}"></polyline>`).join('');
      const dots = series.map((s, i) => (s.points || []).map(p => `<circle class="dot-${{i === 0 ? 'a' : 'b'}}" cx="${{x(labels.indexOf(p.period))}}" cy="${{y(p.value)}}" r="4"><title>${{esc(s.label)}}: ${{esc(p.value)}} ${{esc(s.unit)}}</title></circle>`).join('')).join('');
      const xLabels = labels.map((label, i) => `<text x="${{x(i)}}" y="${{h - 8}}" text-anchor="middle">${{esc(label)}}</text>`).join('');
      const legend = series.map((s, i) => `<span style="color:${{i === 0 ? 'var(--burgundy)' : 'var(--green)'}}">${{esc(s.label)}} (${{esc(s.unit)}})</span>`).join(' / ');
      return `<div class="panel fade-in"><h3>${{esc(chart.title)}}</h3><p>${{esc(chart.description)}}</p><svg class="chart" viewBox="0 0 ${{w}} ${{h}}" preserveAspectRatio="none"><line class="axis" x1="${{pad}}" y1="${{h-pad}}" x2="${{w-pad}}" y2="${{h-pad}}"></line><line class="axis" x1="${{pad}}" y1="${{pad}}" x2="${{pad}}" y2="${{h-pad}}"></line>${{lineEls}}${{dots}}${{xLabels}}</svg><p>${{legend}}</p></div>`;
    }}

    function render() {{
      const ops = content.operational_snapshot.metrics || [];
      const heroMetrics = ops.slice(0, 3).map(m => `<div class="metric"><div class="value">${{esc(m.value)}}</div><div class="label">${{esc(m.label)}} / ${{esc(m.period)}}</div></div>`).join('');
      const layerHtml = (data.layers || []).map(layer => `<article class="layer fade-in"><div class="layer-head"><div class="layer-name">${{esc(layer.label)}}</div><div class="bar" aria-label="${{esc(layer.label)}} score"><span style="--w:${{pct(layer.score)}}%"></span></div><div class="layer-score">${{esc(layer.display_score)}} / 5</div></div><p>${{esc(layer.summary)}}</p><div class="layer-meta"><span>Confidence: ${{esc(layer.confidence)}}</span><span>Coverage: ${{Math.round(layer.coverage_ratio * 100)}}%</span><span>Strong: ${{esc(layer.strong)}}</span></div></article>`).join('');
      const tech = (content.technology_map.items || []).map(item => `<div class="panel fade-in"><h3>${{esc(item.name)}} <span style="color:var(--clay);font-weight:400">/ ${{esc(item.maturity)}}</span></h3><p>${{esc(item.description)}}</p></div>`).join('');
      const bullets = (content.thesis.bullets || []).map(b => `<li>${{esc(b.text)}}</li>`).join('');
      const charts = (content.quantitative_signals.charts || []).map(renderChart).join('');
      const commercial = (content.commercialization_evidence.items || []).map(i => `<div class="panel fade-in"><h3>${{esc(i.label)}}</h3><p>${{esc(i.text)}}</p></div>`).join('');
      const gateMet = (content.breakthrough_gate.conditions_met || []).map(i => `<li>${{esc(i.condition)}}</li>`).join('');
      const gateNot = (content.breakthrough_gate.conditions_not_met || []).map(i => `<li>${{esc(i.condition)}}</li>`).join('');
      const uni = (content.university_research_signals.institutions || []).map(i => `<div class="panel fade-in"><h3>${{esc(i.name)}}</h3><p>${{esc(i.signal)}}</p></div>`).join('');
      const patents = (content.patent_signals.families || []).map(f => `<div class="panel fade-in"><h3>${{esc(f.title)}}</h3><p><strong>${{esc(f.publication_or_family_id)}}</strong> / ${{esc((f.jurisdictions || []).join(', '))}} / priority ${{esc(f.priority_date)}}</p><p>${{esc(f.interpretation)}}</p></div>`).join('');
      const redFlags = (content.red_flags || []).map(r => `<div class="panel fade-in"><h3>${{esc(r.title)}} <span style="color:var(--clay);font-weight:400">/ ${{esc(r.severity)}}</span></h3><p>${{esc(r.text)}}</p></div>`).join('');
      const watchUp = (content.watchlist.upgrade_signals || []).map(w => `<li>${{esc(w.text)}} <span style="color:var(--clay)">(${{esc(w.monitoring_source)}})</span></li>`).join('');
      const watchDown = (content.watchlist.downgrade_signals || []).map(w => `<li>${{esc(w.text)}} <span style="color:var(--clay)">(${{esc(w.monitoring_source)}})</span></li>`).join('');
      const snapshot = ops.map(m => `<div class="metric"><div class="value">${{esc(m.value)}}</div><div class="label">${{esc(m.label)}} / ${{esc(m.period)}}</div></div>`).join('');
      const methods = (content.method_notes.notes || []).map(n => `<li>${{esc(n)}}</li>`).join('');
      const sources = (data.sources || []).map(s => `<p class="source-item"><a href="${{esc(s.url)}}" target="_blank" rel="noopener">${{esc(s.title)}}</a><br>${{esc(s.publisher)}} / ${{esc(s.document_date)}} / ${{esc(s.source_type)}}</p>`).join('');
      const scorePct = (Number(data.total_score) / 25) * 100;

      document.getElementById('app').innerHTML = `
        <section class="top">
          <div>
            <div class="eyebrow">${{esc(data.mode)}} readiness / deterministic score</div>
            <h1>${{esc(content.hero.headline)}}</h1>
            <p class="subheadline">${{esc(content.hero.subheadline)}}</p>
            <div class="summary-row">${{heroMetrics}}</div>
          </div>
          <aside class="score-panel">
            <div class="score-ring" style="--score-pct:${{scorePct}}">
              <div class="score-center"><strong>${{esc(data.display_total_score)}}</strong><span>of 25</span></div>
            </div>
            <div class="verdict">${{esc(data.verdict)}}</div>
            <div class="metric"><div class="value">${{data.gate_pass ? 'Pass' : 'Fail'}}</div><div class="label">Breakthrough gate</div></div>
          </aside>
        </section>

        <section class="section" id="thesis"><div><h2>${{esc(content.thesis.title)}}</h2><p class="note">${{esc(content.thesis.summary)}}</p></div><div class="stack"><ul>${{bullets}}</ul><div class="grid-2">${{tech}}</div></div></section>
        <section class="section" id="layers"><div><h2>Five Layers</h2><p class="note">Scores are stacked vertically as required by the innovation-analysis skill.</p></div><div class="stack">${{layerHtml}}</div></section>
        <section class="section" id="signals"><div><h2>${{esc(content.quantitative_signals.title)}}</h2><p class="note">${{esc(content.quantitative_signals.summary)}}</p></div><div class="grid-2">${{charts}}</div></section>
        <section class="section" id="commercial"><div><h2>${{esc(content.commercialization_evidence.title)}}</h2><p class="note">${{esc(content.commercialization_evidence.summary)}}</p></div><div class="grid-2">${{commercial}}</div></section>
        <section class="section" id="gate"><div><h2>${{esc(content.breakthrough_gate.title)}}</h2><p class="note">${{esc(content.breakthrough_gate.summary)}} Result: ${{esc(content.breakthrough_gate.result)}}</p></div><div class="grid-2"><div class="panel"><h3>Met</h3><ul>${{gateMet}}</ul></div><div class="panel"><h3>Not Met</h3><ul>${{gateNot}}</ul></div></div></section>
        <section class="section" id="science"><div><h2>${{esc(content.university_research_signals.title)}}</h2><p class="note">${{esc(content.university_research_signals.summary)}}</p></div><div class="grid-2">${{uni}}</div></section>
        <section class="section" id="patents"><div><h2>${{esc(content.patent_signals.title)}}</h2><p class="note">${{esc(content.patent_signals.summary)}}</p></div><div class="stack">${{patents}}<div class="panel"><p>${{esc(content.patent_signals.interpretation)}}</p></div></div></section>
        <section class="section" id="risks"><div><h2>Red Flags</h2><p class="note">Concrete reasons to keep the score below the top band.</p></div><div class="grid-2">${{redFlags}}</div></section>
        <section class="section" id="watch"><div><h2>${{esc(content.watchlist.title)}}</h2><p class="note">Refresh these signals on the stated cadence before changing the score.</p></div><div class="grid-2"><div class="panel"><h3>Upgrade</h3><ul>${{watchUp}}</ul></div><div class="panel"><h3>Downgrade</h3><ul>${{watchDown}}</ul></div></div></section>
        <section class="section" id="snapshot"><div><h2>${{esc(content.operational_snapshot.title)}}</h2><p class="note">Latest operating metrics used in the score.</p></div><div class="snapshot">${{snapshot}}</div></section>
        <section class="section" id="method"><div><h2>${{esc(content.method_notes.title)}}</h2><p class="note">${{esc(content.bottom_line.text)}}</p></div><div class="panel"><ul>${{methods}}</ul></div></section>
        <section class="section" id="sources"><div><h2>Sources</h2><p class="note">All substantive dashboard claims are represented in scored.json with source and evidence IDs.</p></div><div class="source-list">${{sources}}</div></section>
      `;
    }}
    render();
  </script>
</body>
</html>
"""


def write_dashboard() -> None:
    scored = json.loads(SCORED_PATH.read_text(encoding="utf-8"))
    DASHBOARD_PATH.write_text(build_dashboard_html(scored), encoding="utf-8")
    print(DASHBOARD_PATH)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--payload", action="store_true", help="Write payload.json")
    parser.add_argument("--dashboard", action="store_true", help="Write dashboard.html from scored.json")
    args = parser.parse_args()
    if args.payload:
        write_payload()
    if args.dashboard:
        write_dashboard()
    if not args.payload and not args.dashboard:
        parser.error("Choose --payload and/or --dashboard")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
