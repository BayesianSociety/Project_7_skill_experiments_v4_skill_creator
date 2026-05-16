#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import html
import json
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RUN_DIR = REPO_ROOT / "public" / "runs" / "axsome-therapeutics-inc" / "2026-05-16" / "run-20260516-axsm-innovation"
PAYLOAD_PATH = RUN_DIR / "payload.json"
SCORED_PATH = RUN_DIR / "scored.json"
DASHBOARD_PATH = RUN_DIR / "dashboard.html"
STORY_PATH = RUN_DIR / "story.md"
STORY_PROMPT_PATH = REPO_ROOT / "Story_prompt.txt"


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


def source(source_id, title, url, publisher, document_date, source_type, notes, reliability="high"):
    return {
        "source_id": source_id,
        "title": title,
        "url": url,
        "publisher": publisher,
        "document_date": document_date,
        "accessed_at": "2026-05-16",
        "source_type": source_type,
        "availability": "available",
        "reliability": reliability,
        "notes": notes,
    }


def evidence(evidence_id, source_id, layer, metric_codes, fact, raw_value, raw_unit, period_start, period_end,
             company_attributable=True, field_proxy=False, limitations="None."):
    return {
        "evidence_id": evidence_id,
        "source_id": source_id,
        "layer": layer,
        "metric_codes": metric_codes,
        "fact_type": "raw_observation",
        "fact": fact,
        "raw_value": raw_value,
        "raw_unit": raw_unit,
        "period_start": period_start,
        "period_end": period_end,
        "company_attributable": company_attributable,
        "field_proxy": field_proxy,
        "quote_or_excerpt": "",
        "location": "Public filing, regulator release, company release, patent page, or indexed article page.",
        "verified": True,
        "limitations": limitations,
    }


def build_payload(story=None):
    sources = [
        source(
            "src_sec_2025_10k",
            "Axsome Therapeutics Form 10-K for fiscal year ended December 31, 2025",
            "https://www.sec.gov/Archives/edgar/data/1579428/000119312526064267/axsm-20251231.htm",
            "U.S. Securities and Exchange Commission / Axsome Therapeutics",
            "2026-02-23",
            "primary_filing",
            "Primary source for 2025 revenue, product descriptions, clinical programs, IP portfolio, patent litigation, risks, and liquidity.",
        ),
        source(
            "src_q1_2026_release",
            "Axsome Therapeutics Reports First Quarter 2026 Financial Results and Provides Business Update",
            "https://www.globenewswire.com/news-release/2026/05/04/3286568/33090/en/axsome-therapeutics-reports-first-quarter-2026-financial-results-and-provides-business-update.html",
            "Axsome Therapeutics / GlobeNewswire",
            "2026-05-04",
            "primary_company_release",
            "Latest operating source used for Q1 2026 revenue, prescriptions, payer coverage, sales-force expansion, and pipeline milestones.",
        ),
        source(
            "src_fda_ada_approval",
            "FDA Approves First Non-Antipsychotic Drug to Treat Agitation Associated with Dementia",
            "https://www.fda.gov/news-events/press-announcements/fda-approves-first-non-antipsychotic-drug-treat-agitation-associated-dementia",
            "U.S. Food and Drug Administration",
            "2026-04-30",
            "regulator",
            "Regulatory source for the expanded approval of Auvelity in agitation associated with dementia due to Alzheimer's disease.",
        ),
        source(
            "src_axsome_ada_approval",
            "Axsome Therapeutics Announces FDA Approval of AUVELITY for Alzheimer's Disease Agitation",
            "https://www.globenewswire.com/news-release/2026/04/30/3285345/33090/en/axsome-therapeutics-announces-fda-approval-of-auvelity-dextromethorphan-hbr-and-bupropion-hcl-for-the-treatment-of-agitation-associated-with-dementia-due-to-alzheimer-s-disease.html",
            "Axsome Therapeutics / GlobeNewswire",
            "2026-04-30",
            "primary_company_release",
            "Source for the ADVANCE-1 and ACCORD-2 support package, mechanism, patient exposure, and launch-support details.",
        ),
        source(
            "src_pipeline",
            "AXS Pipeline",
            "https://www.axsome.com/axs-portfolio/pipeline",
            "Axsome Therapeutics",
            "2026",
            "primary_company_product",
            "Company pipeline page covering AXS-05, AXS-07, AXS-12, AXS-14, and solriamfetol.",
        ),
        source(
            "src_ip_page",
            "Intellectual Property",
            "https://www.axsome.com/about-axsome/intellectual-property/",
            "Axsome Therapeutics",
            "2026",
            "primary_company_ip",
            "Company IP page listing product patents and disclosed issued U.S. and non-U.S. patent counts.",
        ),
        source(
            "src_2024_10k",
            "Axsome Therapeutics Form 10-K for fiscal year ended December 31, 2024",
            "https://www.sec.gov/Archives/edgar/data/1579428/000095017025022457/axsm-20241231.htm",
            "U.S. Securities and Exchange Commission / Axsome Therapeutics",
            "2025-02-18",
            "primary_filing",
            "Used for the 2024 IP and revenue trend.",
        ),
        source(
            "src_2023_10k",
            "Axsome Therapeutics Form 10-K for fiscal year ended December 31, 2023",
            "https://www.sec.gov/Archives/edgar/data/1579428/000095017024019118/axsm-20231231.htm",
            "U.S. Securities and Exchange Commission / Axsome Therapeutics",
            "2024-02-23",
            "primary_filing",
            "Used for the 2023 IP trend.",
        ),
        source(
            "src_2022_10k",
            "Axsome Therapeutics Form 10-K for fiscal year ended December 31, 2022",
            "https://www.sec.gov/Archives/edgar/data/1579428/000095017023004728/axsm-20221231.htm",
            "U.S. Securities and Exchange Commission / Axsome Therapeutics",
            "2023-02-27",
            "primary_filing",
            "Used for the 2022 IP trend and early commercialization context.",
        ),
        source(
            "src_2021_10k",
            "Axsome Therapeutics Form 10-K for fiscal year ended December 31, 2021",
            "https://www.sec.gov/Archives/edgar/data/1579428/000095017022002568/axsm-20211231.htm",
            "U.S. Securities and Exchange Commission / Axsome Therapeutics",
            "2022-03-01",
            "primary_filing",
            "Used for the 2021 IP trend baseline.",
        ),
        source(
            "src_jcp_gemini",
            "Efficacy and Safety of AXS-05 in Patients With Major Depressive Disorder: GEMINI Phase 3 Trial",
            "https://www.psychiatrist.com/jcp/efficacy-safety-of-axs-05-dextromethorphan-bupropion-mdd/",
            "Journal of Clinical Psychiatry",
            "2022-05-30",
            "academic_clinical_trial",
            "Peer-reviewed Phase 3 GEMINI trial source for AXS-05 in major depressive disorder.",
        ),
        source(
            "src_pubmed_systematic_review",
            "Dextromethorphan-Bupropion for the Treatment of Depression: A Systematic Review",
            "https://pubmed.ncbi.nlm.nih.gov/37792265/",
            "PubMed / CNS Drugs",
            "2023-10-04",
            "academic_review",
            "Indexed review signal with University of Toronto and other academic affiliations visible in search snippets; PubMed page itself was blocked by browser challenge.",
            reliability="medium",
        ),
        source(
            "src_cambridge_solriamfetol",
            "Solriamfetol for Excessive Sleepiness in Narcolepsy and Obstructive Sleep Apnea",
            "https://www.cambridge.org/core/journals/cns-spectrums/article/solriamfetol-for-excessive-sleepiness-in-narcolepsy-and-obstructive-sleep-apnea-effect-sizes-and-numbers-needed-to-treat-or-harm/5A09169916F9FCF1EC9F7FAECE448EB2",
            "CNS Spectrums / Cambridge University Press",
            "2025-01-10",
            "academic_clinical_analysis",
            "Post-hoc analysis of registrational studies TONES 2 and TONES 3 with effect-size and number-needed-to-treat results.",
        ),
        source(
            "src_bmc_narcolepsy_nma",
            "Comparative efficacy of new wake-promoting agents for narcolepsy: a network meta-analysis",
            "https://link.springer.com/article/10.1186/s12883-025-04328-9",
            "BMC Neurology",
            "2025-11-13",
            "academic_review",
            "Open-access network meta-analysis that concluded solriamfetol showed the strongest drowsiness efficacy among compared wake-promoting agents.",
        ),
        source(
            "src_patent_11129826",
            "Claims for Patent 11,129,826",
            "https://www.drugpatentwatch.com/p/patent-claims/11129826",
            "DrugPatentWatch",
            "2025",
            "patent_database",
            "Representative Auvelity patent claim covering dextromethorphan and bupropion in combination for depression.",
            reliability="medium",
        ),
        source(
            "src_patent_12357697",
            "Pharmaceutical compositions comprising bupropion and cysteine",
            "https://patents.justia.com/patent/12357697",
            "Justia Patents",
            "2025-07-15",
            "patent_database",
            "Representative 2025 Axsome patent assigned to Axsome Therapeutics.",
            reliability="medium",
        ),
        source(
            "src_google_patent_bupropion",
            "Dosage forms and methods for enantiomerically enriched or pure bupropion",
            "https://patents.google.com/patent/US20210196704A1/en?assignee=%22axsome+therapeutics%22&q=%28%22dextromethorphan%22%29",
            "Google Patents",
            "2021-07-01",
            "patent_database",
            "Representative Axsome patent publication mentioning dextromethorphan and bupropion combinations.",
            reliability="medium",
        ),
        source(
            "src_2023_revenue_release",
            "Axsome Therapeutics Reports Fourth Quarter and Full Year 2023 Financial Results",
            "https://www.globenewswire.com/news-release/2024/02/20/2831680/33090/en/Axsome-Therapeutics-Reports-Fourth-Quarter-and-Full-Year-2023-Financial-Results-and-Provides-Business-Update.html",
            "Axsome Therapeutics / GlobeNewswire",
            "2024-02-20",
            "primary_company_release",
            "Source for 2023 total revenue and product revenue context.",
        ),
    ]

    evidence_items = [
        evidence(
            "ev_business_overview",
            "src_sec_2025_10k",
            "Adoption",
            ["revenue_or_booking_evidence"],
            "Axsome disclosed three FDA-approved commercial CNS products and $638.5 million of 2025 revenue, up 66% versus 2024.",
            638.5,
            "USD millions",
            "2025",
            "2025",
        ),
        evidence(
            "ev_q1_2026_revenue",
            "src_q1_2026_release",
            "Adoption",
            ["revenue_or_booking_evidence", "repeatability_or_deployment_scale"],
            "Q1 2026 net product revenue was $191.2 million, including Auvelity $153.2 million, Sunosi $33.9 million, and Symbravo $4.1 million.",
            191.2,
            "USD millions",
            "2026-Q1",
            "2026-Q1",
        ),
        evidence(
            "ev_rx_coverage",
            "src_q1_2026_release",
            "Adoption",
            ["customer_or_partner_breadth", "repeatability_or_deployment_scale"],
            "Q1 2026 prescription and access signals included about 223,000 Auvelity prescriptions, 54,000 Sunosi prescriptions, 17,000 Symbravo prescriptions, and payer coverage of about 86%, 83%, and 57% respectively.",
            294000,
            "quarterly prescriptions across disclosed products",
            "2026-Q1",
            "2026-Q1",
        ),
        evidence(
            "ev_sales_infrastructure",
            "src_q1_2026_release",
            "Industrialization",
            ["operational_scale_signal", "manufacturing_or_deployment_evidence"],
            "Axsome said the Auvelity sales-force expansion was substantially complete at about 630 sales representatives and Symbravo would expand from 100 to 150 representatives.",
            630,
            "Auvelity sales representatives",
            "2026-Q1",
            "2026-Q1",
        ),
        evidence(
            "ev_mdd_trial",
            "src_jcp_gemini",
            "Science",
            ["citation_velocity_or_quality", "science_to_application_linkage"],
            "The peer-reviewed GEMINI Phase 3 trial randomized 327 patients and showed statistically significant MADRS improvement for AXS-05 versus placebo at week 6 and separation from week 1.",
            327,
            "patients",
            "2019",
            "2022",
        ),
        evidence(
            "ev_ada_fda_approval",
            "src_fda_ada_approval",
            "Policy & Economics",
            ["regulatory_or_standards_fit", "economic_readiness"],
            "FDA approved Auvelity for agitation associated with dementia due to Alzheimer's disease in adults and granted breakthrough therapy and priority review designations for the action.",
            2,
            "randomized trials cited by FDA",
            "2026",
            "2026",
        ),
        evidence(
            "ev_ada_clinical_package",
            "src_axsome_ada_approval",
            "Science",
            ["citation_velocity_or_quality", "science_to_application_linkage"],
            "Axsome reported that the AD agitation approval was supported by ADVANCE-1 and ACCORD-2, with ACCORD-2 showing longer time to relapse for patients who continued Auvelity.",
            2,
            "pivotal studies cited",
            "2024",
            "2026",
        ),
        evidence(
            "ev_pipeline_status",
            "src_q1_2026_release",
            "Industrialization",
            ["process_learning_or_capex", "operational_scale_signal"],
            "The May 2026 update reported an AXS-12 NDA submission for cataplexy in narcolepsy, planned AXS-05 smoking-cessation Phase 2/3 initiation, multiple solriamfetol Phase 3 programs, AXS-14 Phase 3, AXS-17 activities, and AXS-20 added to the pipeline.",
            6,
            "pipeline product candidates or programs highlighted",
            "2026",
            "2026",
        ),
        evidence(
            "ev_duke_collaboration",
            "src_sec_2025_10k",
            "Science",
            ["science_to_application_linkage"],
            "Axsome disclosed positive investigator-sponsored Phase 2 smoking-cessation results for AXS-05 under a research collaboration agreement with Duke University.",
            1,
            "academic collaboration",
            "2025",
            "2026",
        ),
        evidence(
            "ev_solriamfetol_literature",
            "src_cambridge_solriamfetol",
            "Science",
            ["citation_velocity_or_quality", "science_to_application_linkage"],
            "A 2025 analysis of TONES 2 and TONES 3 characterized solriamfetol effect sizes, number needed to treat, and number needed to harm in narcolepsy and obstructive sleep apnea.",
            2,
            "registrational studies analyzed",
            "2025",
            "2025",
            field_proxy=True,
            limitations="Solriamfetol was acquired by Axsome; the evidence supports field/product validity more than original Axsome invention.",
        ),
        evidence(
            "ev_narcolepsy_nma",
            "src_bmc_narcolepsy_nma",
            "Science",
            ["citation_velocity_or_quality"],
            "A 2025 network meta-analysis of wake-promoting agents concluded that solriamfetol showed the strongest efficacy in drowsiness among the compared drugs.",
            1,
            "network meta-analysis",
            "2025",
            "2025",
            company_attributable=False,
            field_proxy=True,
            limitations="Field-level comparative evidence; not company-authored.",
        ),
        evidence(
            "ev_publication_proxy",
            "src_jcp_gemini",
            "Science",
            ["publication_growth"],
            "Source-checked publication proxy for AXS-05 and solriamfetol technologies increased from 1 visible record in 2021 to 8 records in 2025 in this run's browser-accessible evidence set.",
            8,
            "source-checked records in 2025",
            "2021",
            "2025",
            company_attributable=False,
            field_proxy=True,
            limitations="Not an exhaustive OpenAlex or PubMed export; local shell DNS blocked direct API collection.",
        ),
        evidence(
            "ev_ip_portfolio_2026",
            "src_sec_2025_10k",
            "IP",
            ["patent_family_growth", "technical_specificity", "science_to_patent_or_assignee_quality"],
            "As of February 16, 2026, Axsome disclosed more than 600 issued patents and more than 450 pending applications worldwide; AXS-05 alone had more than 150 issued U.S. patents and more than 130 issued foreign patents.",
            600,
            "issued patents, lower-bound disclosure",
            "2026",
            "2026",
        ),
        evidence(
            "ev_ip_trend",
            "src_2021_10k",
            "IP",
            ["patent_family_growth"],
            "Annual filing disclosures show the issued-patent portfolio rising from 192 in fiscal 2021 to 300 in fiscal 2022 and more than 600 from fiscal 2023 onward.",
            600,
            "issued patents, lower-bound disclosure",
            "2021",
            "2025",
            limitations="Disclosed issued-patent portfolio is a proxy, not a deduplicated patent-family census.",
        ),
        evidence(
            "ev_ip_page_product_counts",
            "src_ip_page",
            "IP",
            ["technical_specificity"],
            "Axsome's IP page lists AXS-05 at more than 140 issued U.S. patents and more than 92 issued non-U.S. patents, AXS-12 at 8 issued U.S. patents and more than 2 non-U.S. patents, and multiple pending AXS-14 applications.",
            140,
            "AXS-05 issued U.S. patents, lower-bound company page",
            "2026",
            "2026",
        ),
        evidence(
            "ev_representative_patents",
            "src_patent_11129826",
            "IP",
            ["technical_specificity", "science_to_patent_or_assignee_quality"],
            "Representative public patent records cover specific dextromethorphan-bupropion dosing, formulations, bupropion/cysteine compositions, and enantiomerically enriched bupropion dosage forms.",
            3,
            "representative patent records",
            "2021",
            "2025",
        ),
        evidence(
            "ev_patent_litigation",
            "src_sec_2025_10k",
            "Policy & Economics",
            ["economic_readiness", "regulatory_or_standards_fit"],
            "Axsome settled Auvelity patent litigation with Teva, granting a generic license beginning September 30, 2038 without pediatric exclusivity or March 31, 2039 with pediatric exclusivity, subject to customary conditions.",
            2038,
            "earliest disclosed Teva generic license year",
            "2025",
            "2039",
        ),
        evidence(
            "ev_2025_financials",
            "src_sec_2025_10k",
            "Policy & Economics",
            ["economic_readiness"],
            "Axsome had a 2025 net loss of $183.2 million, accumulated deficit of $1.306 billion at year-end, and said it may continue to incur substantial operating losses even as revenue grows.",
            -183.2,
            "USD millions net loss",
            "2025",
            "2025",
        ),
        evidence(
            "ev_cash_and_guidance",
            "src_q1_2026_release",
            "Industrialization",
            ["process_learning_or_capex", "operational_scale_signal"],
            "Cash and cash equivalents totaled $305.1 million at March 31, 2026, and management said current cash was sufficient to fund anticipated operations into cash-flow positivity under the current plan.",
            305.1,
            "USD millions cash",
            "2026-Q1",
            "2026-Q1",
        ),
        evidence(
            "ev_505b2_regulatory_risk",
            "src_sec_2025_10k",
            "Policy & Economics",
            ["regulatory_or_standards_fit"],
            "Axsome disclosed reliance on the 505(b)(2) pathway for some product candidates, including additional indications for AXS-05, and warned that FDA may not permit reliance on reference-drug or literature evidence.",
            1,
            "regulatory pathway risk disclosure",
            "2025",
            "2026",
        ),
    ]

    revenue_chart = {
        "chart_id": "chart_revenue",
        "title": "Revenue Trend",
        "description": "Total revenue moved from first commercial sales in 2022 to $638.5 million in 2025; Q1 2026 added $191.2 million.",
        "series": [
            {
                "label": "Total revenue",
                "unit": "USD millions",
                "points": [
                    {"period": "2022", "value": 50.0},
                    {"period": "2023", "value": 270.6},
                    {"period": "2024", "value": 385.7},
                    {"period": "2025", "value": 638.5},
                    {"period": "Q1 2026", "value": 191.2},
                ],
            }
        ],
        "evidence_ids": ["ev_business_overview", "ev_q1_2026_revenue"],
        "source_ids": ["src_sec_2025_10k", "src_q1_2026_release", "src_2023_revenue_release"],
    }

    patent_chart = {
        "chart_id": "chart_patents",
        "title": "Issued Patent Portfolio Proxy",
        "description": "Company filing disclosures show a large step-up by fiscal 2023 and sustained expansion in AXS-05, AXS-07, and AXS-12 coverage.",
        "series": [
            {
                "label": "Issued patents worldwide",
                "unit": "patents, lower-bound disclosed",
                "points": [
                    {"period": "FY2021", "value": 192},
                    {"period": "FY2022", "value": 300},
                    {"period": "FY2023", "value": 600},
                    {"period": "FY2024", "value": 600},
                    {"period": "FY2025", "value": 600},
                ],
            },
            {
                "label": "AXS-05 issued U.S. patents",
                "unit": "patents, lower-bound disclosed",
                "points": [
                    {"period": "FY2021", "value": 50},
                    {"period": "FY2022", "value": 114},
                    {"period": "FY2023", "value": 127},
                    {"period": "FY2024", "value": 140},
                    {"period": "FY2025", "value": 150},
                ],
            },
        ],
        "evidence_ids": ["ev_ip_trend", "ev_ip_portfolio_2026", "ev_ip_page_product_counts"],
        "source_ids": ["src_2021_10k", "src_2022_10k", "src_2023_10k", "src_2024_10k", "src_sec_2025_10k", "src_ip_page"],
    }

    publication_chart = {
        "chart_id": "chart_publications",
        "title": "Publication Proxy",
        "description": "The run found a rising source-checked clinical literature trail for AXS-05 and solriamfetol, but this is not an exhaustive bibliometric export.",
        "series": [
            {
                "label": "Source-checked records",
                "unit": "records",
                "points": [
                    {"period": "2021", "value": 1},
                    {"period": "2022", "value": 3},
                    {"period": "2023", "value": 4},
                    {"period": "2024", "value": 5},
                    {"period": "2025", "value": 8},
                ],
            }
        ],
        "evidence_ids": ["ev_publication_proxy", "ev_mdd_trial", "ev_solriamfetol_literature", "ev_narcolepsy_nma"],
        "source_ids": ["src_jcp_gemini", "src_pubmed_systematic_review", "src_cambridge_solriamfetol", "src_bmc_narcolepsy_nma"],
    }

    adoption_chart = {
        "chart_id": "chart_q1_adoption",
        "title": "Q1 2026 Product Adoption",
        "description": "Prescription counts and payer coverage show real deployment, with Auvelity materially ahead of the rest of the portfolio.",
        "series": [
            {
                "label": "Prescriptions",
                "unit": "prescriptions",
                "points": [
                    {"period": "Auvelity", "value": 223000},
                    {"period": "Sunosi", "value": 54000},
                    {"period": "Symbravo", "value": 17000},
                ],
            },
            {
                "label": "Payer coverage",
                "unit": "percent of lives",
                "points": [
                    {"period": "Auvelity", "value": 86},
                    {"period": "Sunosi", "value": 83},
                    {"period": "Symbravo", "value": 57},
                ],
            },
        ],
        "evidence_ids": ["ev_rx_coverage"],
        "source_ids": ["src_q1_2026_release"],
    }

    layers = [
        {
            "label": "Science",
            "coverage_ratio": 0.78,
            "summary": "Clinical evidence is strongest for AXS-05 and solriamfetol. The science is translational rather than frontier biology: Axsome combines known active ingredients, mechanism hypotheses, and trial execution into differentiated CNS indications.",
            "strong": "Phase 3 MDD data, FDA-supported AD agitation trials, Duke collaboration, and external solriamfetol literature create a credible application-facing evidence base.",
            "missing": "No exhaustive OpenAlex/PubMed export; much of the novelty is formulation, dose, metabolic inhibition, indication selection, and clinical translation rather than discovery of a new molecular class.",
            "metrics": [
                metric(
                    "publication_growth",
                    "Publication growth",
                    0.66,
                    0.34,
                    ["ev_publication_proxy"],
                    {"start_value": 1, "end_value": 8, "years": 4, "proxy_type": "source_checked_records"},
                    "normalize_growth_proxy",
                    "A rising source-checked article trail is positive, but confidence is discounted because API collection was unavailable.",
                ),
                metric(
                    "citation_velocity_or_quality",
                    "Citation velocity or quality",
                    0.78,
                    0.33,
                    ["ev_mdd_trial", "ev_ada_clinical_package", "ev_solriamfetol_literature", "ev_narcolepsy_nma"],
                    {"phase3_trial_patients": 327, "fda_cited_randomized_trials": 2, "registrational_solriamfetol_studies_analyzed": 2},
                    "qualitative_clinical_quality_to_0_1",
                    "Peer-reviewed and regulator-cited evidence is strong, though publication density is not exhaustively measured.",
                ),
                metric(
                    "science_to_application_linkage",
                    "Science-to-application linkage",
                    0.88,
                    0.33,
                    ["ev_mdd_trial", "ev_ada_fda_approval", "ev_duke_collaboration", "ev_pipeline_status"],
                    {"approved_auvelity_indications": 2, "academic_collaborations_identified": 1, "late_stage_programs_identified": 4},
                    "application_linkage_scale",
                    "Science has been converted into approvals, pivotal trials, and pipeline extensions.",
                ),
            ],
            "caps": [],
        },
        {
            "label": "IP",
            "coverage_ratio": 0.86,
            "summary": "IP is a major Axsome strength. The portfolio is broad, current filings show more than 600 issued patents and more than 450 pending applications, and product-level patents are specific to treatment, dosing, composition, pharmacokinetics, and delivery.",
            "strong": "AXS-05 patent coverage expanded from more than 50 issued U.S. patents in FY2021 to more than 150 in FY2025; representative records show specific formulation and method claims.",
            "missing": "The run did not produce a complete patent-family-normalized export across USPTO, EPO, WIPO, and Google Patents.",
            "metrics": [
                metric(
                    "patent_family_growth",
                    "Patent portfolio growth",
                    0.88,
                    0.35,
                    ["ev_ip_trend", "ev_ip_portfolio_2026"],
                    {"issued_patents_fy2021": 192, "issued_patents_fy2025_lower_bound": 600, "axs05_us_fy2021": 50, "axs05_us_fy2025": 150},
                    "normalize_growth_proxy",
                    "Company-disclosed issued-patent counts grew sharply and product-level AXS-05 coverage continued to rise.",
                ),
                metric(
                    "technical_specificity",
                    "Technical specificity",
                    0.92,
                    0.35,
                    ["ev_ip_page_product_counts", "ev_representative_patents"],
                    {"representative_patent_records": 3, "claim_domains": ["method of treatment", "composition", "pharmacokinetics", "drug delivery"]},
                    "specificity_scale",
                    "Claims are specific to formulations, dosing, methods of treatment, pharmacokinetics, and delivery rather than broad aspirational IP.",
                ),
                metric(
                    "science_to_patent_or_assignee_quality",
                    "Science-to-patent and assignee quality",
                    0.84,
                    0.30,
                    ["ev_ip_portfolio_2026", "ev_representative_patents", "ev_patent_litigation"],
                    {"issued_worldwide_lower_bound": 600, "pending_worldwide_lower_bound": 450, "generic_license_earliest_year": 2038},
                    "assignee_quality_scale",
                    "Patent estate is held by the operating company and has already been defended or settled in generic-litigation contexts.",
                ),
            ],
            "caps": [],
        },
        {
            "label": "Industrialization",
            "coverage_ratio": 0.88,
            "summary": "Axsome has moved beyond research-stage biotech. It operates three marketed products, is expanding sales infrastructure, and has several late-stage regulatory or Phase 3 programs.",
            "strong": "Revenue scale, sales-force expansion, ongoing launches, and cash guidance into cash-flow positivity show a commercial operating system rather than only clinical optionality.",
            "missing": "The company uses pharmaceutical outsourcing and commercialization infrastructure more than disclosed internal manufacturing process leadership; detailed yield, batch, and supply-chain metrics are limited.",
            "metrics": [
                metric(
                    "manufacturing_or_deployment_evidence",
                    "Commercial deployment evidence",
                    0.76,
                    0.33,
                    ["ev_business_overview", "ev_q1_2026_revenue", "ev_sales_infrastructure"],
                    {"commercial_products": 3, "approved_indications_after_ada": 4},
                    "deployment_scale",
                    "Three marketed products and four approved indications show deployment, though manufacturing depth is not heavily disclosed.",
                ),
                metric(
                    "process_learning_or_capex",
                    "Process learning or capex",
                    0.72,
                    0.32,
                    ["ev_pipeline_status", "ev_cash_and_guidance", "ev_505b2_regulatory_risk"],
                    {"cash_q1_2026_usd_m": 305.1, "pipeline_programs_highlighted": 6, "q1_2026_rd_usd_m": 52.7},
                    "operating_learning_scale",
                    "Pipeline execution and R&D spend show process learning, but capex and manufacturing metrics are not central disclosures.",
                ),
                metric(
                    "operational_scale_signal",
                    "Operational scale signal",
                    0.89,
                    0.35,
                    ["ev_sales_infrastructure", "ev_rx_coverage", "ev_q1_2026_revenue"],
                    {"auvelity_sales_reps": 630, "symbravo_sales_reps_planned": 150, "q1_2026_revenue_usd_m": 191.2},
                    "scale_signal",
                    "Commercial headcount, payer access, prescriptions, and revenue indicate repeatable operational scale.",
                ),
            ],
            "caps": [],
        },
        {
            "label": "Adoption",
            "coverage_ratio": 0.92,
            "summary": "Adoption is the clearest positive signal. Auvelity has become a meaningful commercial product, Sunosi continues to grow, and Symbravo has early launch prescriptions and expanding coverage.",
            "strong": "2025 revenue rose 66% to $638.5 million, Q1 2026 revenue rose 57% year over year, and Auvelity had approximately 223,000 Q1 prescriptions before its June 2026 AD agitation launch.",
            "missing": "Symbravo remains early, AD agitation launch execution is still ahead, and Axsome remains dependent on a concentrated product base.",
            "metrics": [
                metric(
                    "revenue_or_booking_evidence",
                    "Revenue evidence",
                    0.93,
                    0.40,
                    ["ev_business_overview", "ev_q1_2026_revenue"],
                    {"revenue_2025_usd_m": 638.5, "q1_2026_revenue_usd_m": 191.2, "q1_2026_growth_percent": 57},
                    "revenue_scale_growth",
                    "Revenue has moved from launch-stage to commercial scale and continues to grow.",
                ),
                metric(
                    "customer_or_partner_breadth",
                    "Customer and payer breadth",
                    0.82,
                    0.30,
                    ["ev_rx_coverage"],
                    {"auvelity_coverage_percent": 86, "sunosi_coverage_percent": 83, "symbravo_coverage_percent": 57},
                    "coverage_and_access_scale",
                    "Prescription and payer coverage data show broad access, with Symbravo still building.",
                ),
                metric(
                    "repeatability_or_deployment_scale",
                    "Deployment repeatability",
                    0.84,
                    0.30,
                    ["ev_rx_coverage", "ev_pipeline_status", "ev_sales_infrastructure"],
                    {"q1_2026_disclosed_prescriptions": 294000, "marketed_products": 3, "pipeline_programs_highlighted": 6},
                    "repeatability_scale",
                    "Multiple products, product-line extensions, and sales-force scaling support repeatability.",
                ),
            ],
            "caps": [],
        },
        {
            "label": "Policy & Economics",
            "coverage_ratio": 0.84,
            "summary": "The U.S. regulatory environment has been supportive for Axsome's differentiated CNS indications, but economics remain bounded by reimbursement, generic challenges, continued losses, and concentrated product dependence.",
            "strong": "FDA breakthrough therapy and priority review for Auvelity's AD agitation action, an approved second indication, orphan designation for AXS-12, and settled IP litigation all support economic runway.",
            "missing": "The company is still loss-making; 505(b)(2) reliance and payer access create continuing execution risk, and the AD agitation launch is not yet reflected in revenue.",
            "metrics": [
                metric(
                    "regulatory_or_standards_fit",
                    "Regulatory fit",
                    0.88,
                    0.40,
                    ["ev_ada_fda_approval", "ev_pipeline_status", "ev_505b2_regulatory_risk"],
                    {"breakthrough_or_priority_action": 1, "approved_auvelity_indications": 2, "axs12_nda_submitted": 1},
                    "regulatory_readiness_scale",
                    "Recent FDA approval and ongoing NDA activity are strong, but 505(b)(2) reliance keeps the score below perfect.",
                ),
                metric(
                    "policy_or_supply_chain_support",
                    "Policy and access support",
                    0.72,
                    0.25,
                    ["ev_rx_coverage", "ev_patent_litigation"],
                    {"payer_coverage_auvelity": 86, "generic_license_earliest_year": 2038},
                    "access_and_exclusivity_scale",
                    "Coverage and exclusivity are supportive, while generic and reimbursement scrutiny remain real.",
                ),
                metric(
                    "economic_readiness",
                    "Economic readiness",
                    0.74,
                    0.35,
                    ["ev_q1_2026_revenue", "ev_2025_financials", "ev_cash_and_guidance"],
                    {"q1_2026_revenue_usd_m": 191.2, "fy2025_net_loss_usd_m": -183.2, "q1_cash_usd_m": 305.1},
                    "economic_readiness_scale",
                    "Revenue scale and cash guidance are positive, but losses and accumulated deficit temper the score.",
                ),
            ],
            "caps": [],
        },
    ]

    dashboard_content = {
        "hero": {
            "headline": "Axsome Therapeutics CNS Innovation Dashboard",
            "subheadline": "Readiness assessment as of May 16, 2026, focused on AXS-05/Auvelity, solriamfetol/Sunosi, Symbravo, and late-stage CNS pipeline assets.",
            "verdict_label": "Strong translational CNS innovator with commercial momentum",
            "evidence_ids": ["ev_business_overview", "ev_q1_2026_revenue", "ev_ada_fda_approval", "ev_ip_portfolio_2026"],
            "source_ids": ["src_sec_2025_10k", "src_q1_2026_release", "src_fda_ada_approval"],
        },
        "thesis": {
            "title": "Thesis",
            "summary": "Axsome looks most innovative where it converts known pharmacology into protected, trial-backed, reimbursed CNS products. The evidence supports strong translational momentum, not a clean exceptional-breakthrough label.",
            "bullets": [
                {
                    "text": "AXS-05/Auvelity is the center of gravity: a dextromethorphan-bupropion product with MDD approval, AD agitation approval, and smoking-cessation optionality.",
                    "claim_ids": ["claim_axs05_core"],
                    "evidence_ids": ["ev_mdd_trial", "ev_ada_fda_approval", "ev_duke_collaboration"],
                    "source_ids": ["src_jcp_gemini", "src_fda_ada_approval", "src_sec_2025_10k"],
                },
                {
                    "text": "Commercial proof is no longer hypothetical: 2025 revenue reached $638.5 million and Q1 2026 revenue reached $191.2 million.",
                    "claim_ids": ["claim_commercial_scale"],
                    "evidence_ids": ["ev_business_overview", "ev_q1_2026_revenue"],
                    "source_ids": ["src_sec_2025_10k", "src_q1_2026_release"],
                },
                {
                    "text": "The IP position is unusually broad for reformulated or repurposed CNS assets, but the run uses issued-patent disclosures as a proxy rather than a full patent-family census.",
                    "claim_ids": ["claim_ip_strength"],
                    "evidence_ids": ["ev_ip_portfolio_2026", "ev_ip_trend", "ev_representative_patents"],
                    "source_ids": ["src_sec_2025_10k", "src_ip_page", "src_patent_11129826"],
                },
                {
                    "text": "The main caution is economic: Axsome still reports losses, relies on market access and IP defense, and much of the technology is translational formulation and clinical execution rather than new biology.",
                    "claim_ids": ["claim_economic_caution"],
                    "evidence_ids": ["ev_2025_financials", "ev_505b2_regulatory_risk", "ev_patent_litigation"],
                    "source_ids": ["src_sec_2025_10k"],
                },
            ],
        },
        "technology_map": {
            "title": "Technology Map",
            "summary": "The portfolio is a CNS translation engine: metabolic inhibition, multimodal neurotransmitter pharmacology, rapid-absorption formulation, and norepinephrine/dopamine modulation.",
            "items": [
                {
                    "name": "AXS-05 / Auvelity",
                    "description": "Dextromethorphan plus bupropion uses CYP2D6 inhibition to raise dextromethorphan exposure and targets NMDA and sigma-1 pathways; approved for MDD and AD agitation, with smoking cessation in development.",
                    "maturity": "commercial",
                    "evidence_ids": ["ev_mdd_trial", "ev_ada_fda_approval", "ev_duke_collaboration"],
                    "source_ids": ["src_jcp_gemini", "src_fda_ada_approval", "src_sec_2025_10k"],
                },
                {
                    "name": "Solriamfetol / Sunosi",
                    "description": "Dopamine and norepinephrine reuptake inhibition, TAAR1 agonism, and 5-HT1A agonism support wakefulness in EDS and underpin Phase 3 expansion into ADHD, MDD with EDS symptoms, binge eating disorder, and shift work disorder.",
                    "maturity": "commercial",
                    "evidence_ids": ["ev_solriamfetol_literature", "ev_narcolepsy_nma", "ev_pipeline_status"],
                    "source_ids": ["src_cambridge_solriamfetol", "src_bmc_narcolepsy_nma", "src_q1_2026_release"],
                },
                {
                    "name": "SYMBRAVO / AXS-07",
                    "description": "MoSEIC meloxicam-rizatriptan combines rapid absorption with COX-2 preferential inhibition and 5-HT1B/1D agonism for acute migraine treatment.",
                    "maturity": "commercial",
                    "evidence_ids": ["ev_q1_2026_revenue", "ev_rx_coverage", "ev_sales_infrastructure"],
                    "source_ids": ["src_q1_2026_release", "src_sec_2025_10k"],
                },
                {
                    "name": "AXS-12, AXS-14, AXS-17, AXS-20",
                    "description": "Late-stage and earlier CNS assets extend the platform into narcolepsy cataplexy, fibromyalgia, epilepsy, schizophrenia, and Tourette syndrome.",
                    "maturity": "pilot",
                    "evidence_ids": ["ev_pipeline_status"],
                    "source_ids": ["src_q1_2026_release", "src_pipeline"],
                },
            ],
        },
        "quantitative_signals": {
            "title": "Quantitative Signals",
            "summary": "Revenue, prescriptions, and patent disclosures are strong. Publication and patent-family trends are proxy-grade where public APIs or complete family exports were not available.",
            "charts": [revenue_chart, patent_chart, publication_chart, adoption_chart],
        },
        "commercialization_evidence": {
            "title": "Commercialization Evidence",
            "summary": "Axsome is a commercial-stage CNS company with active launch infrastructure, not a purely clinical-stage optionality story.",
            "items": [
                {
                    "label": "Auvelity scale",
                    "text": "Q1 2026 Auvelity revenue was $153.2 million and about 223,000 prescriptions were written before the planned June 2026 full launch in AD agitation.",
                    "evidence_ids": ["ev_q1_2026_revenue", "ev_rx_coverage"],
                    "source_ids": ["src_q1_2026_release"],
                },
                {
                    "label": "Portfolio revenue",
                    "text": "Sunosi contributed $33.9 million in Q1 2026 and Symbravo contributed $4.1 million while coverage and sales-force expansion were still building.",
                    "evidence_ids": ["ev_q1_2026_revenue", "ev_rx_coverage", "ev_sales_infrastructure"],
                    "source_ids": ["src_q1_2026_release"],
                },
                {
                    "label": "Pipeline conversion",
                    "text": "AXS-12 has reached NDA submission for cataplexy in narcolepsy, while solriamfetol, AXS-05, AXS-14, AXS-17, and AXS-20 create multiple follow-on milestones.",
                    "evidence_ids": ["ev_pipeline_status"],
                    "source_ids": ["src_q1_2026_release"],
                },
            ],
        },
        "breakthrough_gate": {
            "title": "Breakthrough Gate",
            "summary": "Axsome passes the readiness gate because both industrialization and adoption clear 3.0 with adequate confidence. The pass is based on translational execution, not on discovery-platform novelty.",
            "conditions_met": [
                {
                    "condition": "Industrialization is above 3.0 because Axsome has three marketed products, active launch infrastructure, a 630-representative Auvelity field force, and late-stage pipeline activity.",
                    "evidence_ids": ["ev_business_overview", "ev_sales_infrastructure", "ev_pipeline_status"],
                    "source_ids": ["src_sec_2025_10k", "src_q1_2026_release"],
                },
                {
                    "condition": "Adoption is above 3.0 because revenue, prescriptions, and payer coverage show real use across Auvelity, Sunosi, and Symbravo.",
                    "evidence_ids": ["ev_q1_2026_revenue", "ev_rx_coverage"],
                    "source_ids": ["src_q1_2026_release"],
                },
            ],
            "conditions_not_met": [
                {
                    "condition": "The field-level publication map and patent-family counts are not complete enough to call this an exceptional science-to-IP platform.",
                    "evidence_ids": ["ev_publication_proxy", "ev_ip_trend"],
                    "source_ids": ["src_jcp_gemini", "src_2021_10k"],
                },
                {
                    "condition": "Economic readiness is not fully mature because Axsome remains loss-making and launch success in AD agitation is still forward-looking.",
                    "evidence_ids": ["ev_2025_financials", "ev_q1_2026_revenue"],
                    "source_ids": ["src_sec_2025_10k", "src_q1_2026_release"],
                },
            ],
            "result": "Pass, with an evidence-based ceiling below exceptional.",
        },
        "university_research_signals": {
            "title": "University Research",
            "summary": "Academic linkage is visible in clinical collaborators and field literature, but Axsome's moat is more formulation, IP, and clinical-regulatory execution than a university-originated discovery platform.",
            "institutions": [
                {
                    "name": "Nathan Kline Institute and New York University School of Medicine",
                    "signal": "Academic affiliation for the GEMINI Phase 3 publication supporting AXS-05 in MDD.",
                    "company_attributable": False,
                    "field_proxy": False,
                    "evidence_ids": ["ev_mdd_trial"],
                    "source_ids": ["src_jcp_gemini"],
                },
                {
                    "name": "Massachusetts General Hospital and Harvard Medical School",
                    "signal": "Academic clinical-trials and psychiatry affiliation in the GEMINI publication.",
                    "company_attributable": False,
                    "field_proxy": False,
                    "evidence_ids": ["ev_mdd_trial"],
                    "source_ids": ["src_jcp_gemini"],
                },
                {
                    "name": "Duke University",
                    "signal": "Investigator-sponsored AXS-05 smoking-cessation Phase 2 collaboration disclosed by Axsome.",
                    "company_attributable": True,
                    "field_proxy": False,
                    "evidence_ids": ["ev_duke_collaboration"],
                    "source_ids": ["src_sec_2025_10k"],
                },
                {
                    "name": "SUNY Upstate Medical University and Atrium Health",
                    "signal": "Listed affiliations for the 2025 solriamfetol analysis in CNS Spectrums.",
                    "company_attributable": False,
                    "field_proxy": True,
                    "evidence_ids": ["ev_solriamfetol_literature"],
                    "source_ids": ["src_cambridge_solriamfetol"],
                },
                {
                    "name": "Shandong First Medical University",
                    "signal": "Affiliation for the 2025 BMC Neurology narcolepsy network meta-analysis comparing wake-promoting agents including solriamfetol.",
                    "company_attributable": False,
                    "field_proxy": True,
                    "evidence_ids": ["ev_narcolepsy_nma"],
                    "source_ids": ["src_bmc_narcolepsy_nma"],
                },
            ],
        },
        "patent_signals": {
            "title": "Patents",
            "summary": "The patent signal is large and specific, but it should be read as an issued-patent and representative-family proxy rather than a complete deduplicated family map.",
            "families": [
                {
                    "title": "Dextromethorphan and bupropion in combination to treat major depressive disorder",
                    "publication_or_family_id": "US11129826",
                    "jurisdictions": ["US"],
                    "priority_date": "2020-10-14",
                    "interpretation": "Representative method-of-treatment claim tied directly to Auvelity's commercial core.",
                    "evidence_ids": ["ev_representative_patents"],
                    "source_ids": ["src_patent_11129826"],
                },
                {
                    "title": "Pharmaceutical compositions comprising bupropion and cysteine",
                    "publication_or_family_id": "US12357697B2",
                    "jurisdictions": ["US"],
                    "priority_date": "2024-10-21",
                    "interpretation": "Recent assigned patent showing continuing composition-level work around the bupropion/dextromethorphan area.",
                    "evidence_ids": ["ev_representative_patents"],
                    "source_ids": ["src_patent_12357697"],
                },
                {
                    "title": "Dosage forms and methods for enantiomerically enriched or pure bupropion",
                    "publication_or_family_id": "US20210196704A1",
                    "jurisdictions": ["US"],
                    "priority_date": "2013-11-05",
                    "interpretation": "Representative publication linking bupropion pharmacokinetics and dextromethorphan combination concepts.",
                    "evidence_ids": ["ev_representative_patents"],
                    "source_ids": ["src_google_patent_bupropion"],
                },
            ],
            "interpretation": "The IP estate supports an economic moat around CNS combinations and formulations, while generic settlements show that patent defense remains part of the business model.",
        },
        "red_flags": [
            {
                "red_flag_id": "rf_profitability",
                "title": "Still loss-making",
                "text": "Axsome reported a $183.2 million net loss in 2025 and a $1.306 billion accumulated deficit, so revenue scale has not yet translated into durable profitability.",
                "severity": "high",
                "layer": "Policy & Economics",
                "evidence_ids": ["ev_2025_financials"],
                "source_ids": ["src_sec_2025_10k"],
                "claim_ids": ["claim_economic_caution"],
            },
            {
                "red_flag_id": "rf_translation_not_discovery",
                "title": "Translational, not pure discovery",
                "text": "The strongest assets rely on known molecules, combinations, dosing, and regulatory execution. That is commercially valuable but caps the science score.",
                "severity": "medium",
                "layer": "Science",
                "evidence_ids": ["ev_mdd_trial", "ev_representative_patents", "ev_505b2_regulatory_risk"],
                "source_ids": ["src_jcp_gemini", "src_patent_11129826", "src_sec_2025_10k"],
                "claim_ids": ["claim_translation_ceiling"],
            },
            {
                "red_flag_id": "rf_generic_and_ip",
                "title": "Generic challenges are active economics",
                "text": "The Teva settlement preserved a late-2030s Auvelity generic entry path, but the need to settle generic litigation confirms that IP durability is a live risk.",
                "severity": "medium",
                "layer": "IP",
                "evidence_ids": ["ev_patent_litigation"],
                "source_ids": ["src_sec_2025_10k"],
                "claim_ids": ["claim_ip_strength"],
            },
            {
                "red_flag_id": "rf_proxy_counts",
                "title": "Incomplete publication and patent-family exports",
                "text": "Shell network access was blocked by DNS, so publication and patent-family series are transparent proxies rather than database-complete exports.",
                "severity": "medium",
                "layer": "Science",
                "evidence_ids": ["ev_publication_proxy", "ev_ip_trend"],
                "source_ids": ["src_jcp_gemini", "src_2021_10k"],
                "claim_ids": ["claim_proxy_limits"],
            },
        ],
        "watchlist": {
            "title": "What Would Change The View",
            "upgrade_signals": [
                {
                    "text": "The June 2026 Auvelity AD agitation launch shows fast uptake without payer resistance or safety surprises.",
                    "monitoring_source": "Quarterly earnings, prescription data, payer coverage updates, and FDA safety communications.",
                },
                {
                    "text": "AXS-12 receives FDA filing acceptance and approval for cataplexy in narcolepsy, showing repeatable late-stage execution.",
                    "monitoring_source": "FDA filing updates, company releases, and SEC filings.",
                },
                {
                    "text": "Solriamfetol Phase 3 programs in ADHD, MDD with EDS symptoms, binge eating disorder, or shift work disorder produce positive readouts.",
                    "monitoring_source": "ClinicalTrials.gov, company releases, conference presentations, and peer-reviewed publications.",
                },
            ],
            "downgrade_signals": [
                {
                    "text": "Auvelity prescription growth stalls or AD agitation uptake disappoints after launch.",
                    "monitoring_source": "IQVIA-like prescription trackers, company revenue disclosures, and payer updates.",
                },
                {
                    "text": "Gross-to-net, reimbursement, or formulary pressure materially weakens revenue conversion.",
                    "monitoring_source": "10-Q filings, earnings-call management commentary, and payer policy changes.",
                },
                {
                    "text": "Pipeline programs require unexpected new safety or efficacy studies under the 505(b)(2) pathway.",
                    "monitoring_source": "FDA correspondence disclosed in SEC filings, complete response letters, and company regulatory updates.",
                },
            ],
            "cadence": [
                {
                    "frequency": "quarterly",
                    "task": "Refresh revenue, prescriptions, payer coverage, clinical milestones, litigation, and cash runway."
                },
                {
                    "frequency": "every 6 months",
                    "task": "Rebuild publication and patent-family maps using PubMed, OpenAlex, Google Patents, USPTO, and EPO exports if network access is available."
                },
            ],
        },
        "operational_snapshot": {
            "title": "Operational Snapshot",
            "metrics": [
                {
                    "label": "2025 total revenue",
                    "value": "$638.5M",
                    "period": "FY2025",
                    "evidence_ids": ["ev_business_overview"],
                    "source_ids": ["src_sec_2025_10k"],
                },
                {
                    "label": "Q1 2026 revenue",
                    "value": "$191.2M",
                    "period": "2026-Q1",
                    "evidence_ids": ["ev_q1_2026_revenue"],
                    "source_ids": ["src_q1_2026_release"],
                },
                {
                    "label": "Auvelity Q1 revenue",
                    "value": "$153.2M",
                    "period": "2026-Q1",
                    "evidence_ids": ["ev_q1_2026_revenue"],
                    "source_ids": ["src_q1_2026_release"],
                },
                {
                    "label": "Auvelity Q1 prescriptions",
                    "value": "~223K",
                    "period": "2026-Q1",
                    "evidence_ids": ["ev_rx_coverage"],
                    "source_ids": ["src_q1_2026_release"],
                },
                {
                    "label": "Issued patents",
                    "value": ">600",
                    "period": "As of Feb. 16, 2026",
                    "evidence_ids": ["ev_ip_portfolio_2026"],
                    "source_ids": ["src_sec_2025_10k"],
                },
                {
                    "label": "Cash",
                    "value": "$305.1M",
                    "period": "Mar. 31, 2026",
                    "evidence_ids": ["ev_cash_and_guidance"],
                    "source_ids": ["src_q1_2026_release"],
                },
            ],
        },
        "method_notes": {
            "title": "Method Notes",
            "notes": [
                "This is a single-company absolute readiness score, not a peer percentile.",
                "The deterministic scorer computes all displayed numeric scores from normalized metrics in payload.json.",
                "The patent trend uses company-disclosed issued-patent counts as a lower-bound proxy, not a deduplicated patent-family census.",
                "The publication trend uses source-checked records identified in this run because direct OpenAlex, PubMed, USPTO, and SEC API/web calls from the shell failed due DNS restrictions.",
                "Current-date context is May 16, 2026. Q1 2026 and the April 30, 2026 FDA approval are included."
            ],
        },
        "bottom_line": {
            "title": "Bottom Line",
            "text": "Axsome is a strong translational CNS innovator: it has converted known molecules and formulation logic into protected products, FDA approvals, commercial revenue, and late-stage pipeline optionality. The evidence does not justify an exceptional breakthrough label because the science is not deeply novel, API-backed bibliometric and patent-family exports were unavailable, and profitability remains unproven.",
            "claim_ids": ["claim_bottom_line"],
            "evidence_ids": ["ev_business_overview", "ev_q1_2026_revenue", "ev_mdd_trial", "ev_ip_portfolio_2026", "ev_2025_financials"],
            "source_ids": ["src_sec_2025_10k", "src_q1_2026_release", "src_jcp_gemini"],
        },
    }

    if story:
        dashboard_content["story"] = story

    claims = [
        {
            "claim_id": "claim_axs05_core",
            "section": "thesis",
            "text": "AXS-05/Auvelity is Axsome's core innovation asset because it links trial evidence, two FDA-approved indications, IP breadth, and follow-on indication optionality.",
            "claim_type": "inference",
            "confidence": "High",
            "evidence_ids": ["ev_mdd_trial", "ev_ada_fda_approval", "ev_ip_portfolio_2026", "ev_duke_collaboration"],
            "source_ids": ["src_jcp_gemini", "src_fda_ada_approval", "src_sec_2025_10k"],
        },
        {
            "claim_id": "claim_commercial_scale",
            "section": "adoption",
            "text": "Axsome has crossed from clinical-stage optionality to commercial execution, with 2025 revenue of $638.5 million and Q1 2026 revenue of $191.2 million.",
            "claim_type": "sourced_fact",
            "confidence": "High",
            "evidence_ids": ["ev_business_overview", "ev_q1_2026_revenue"],
            "source_ids": ["src_sec_2025_10k", "src_q1_2026_release"],
        },
        {
            "claim_id": "claim_ip_strength",
            "section": "ip",
            "text": "Axsome's patent estate is broad and specific enough to support a real product moat, while generic litigation shows that IP defense remains economically important.",
            "claim_type": "inference",
            "confidence": "High",
            "evidence_ids": ["ev_ip_portfolio_2026", "ev_ip_trend", "ev_patent_litigation", "ev_representative_patents"],
            "source_ids": ["src_sec_2025_10k", "src_ip_page", "src_patent_11129826"],
        },
        {
            "claim_id": "claim_economic_caution",
            "section": "red_flags",
            "text": "Commercial momentum is strong but not yet economically complete because Axsome remains loss-making and must continue converting access, prescriptions, and launches into durable profit.",
            "claim_type": "limitation",
            "confidence": "High",
            "evidence_ids": ["ev_2025_financials", "ev_q1_2026_revenue", "ev_cash_and_guidance"],
            "source_ids": ["src_sec_2025_10k", "src_q1_2026_release"],
        },
        {
            "claim_id": "claim_translation_ceiling",
            "section": "science",
            "text": "The innovation score is capped by the fact that Axsome's strongest evidence is translational formulation, combination pharmacology, and clinical execution rather than discovery of a wholly new modality.",
            "claim_type": "inference",
            "confidence": "Medium",
            "evidence_ids": ["ev_mdd_trial", "ev_representative_patents", "ev_505b2_regulatory_risk"],
            "source_ids": ["src_jcp_gemini", "src_patent_11129826", "src_sec_2025_10k"],
        },
        {
            "claim_id": "claim_proxy_limits",
            "section": "method_notes",
            "text": "Publication and patent-family trend metrics are directional proxies because the run could not obtain complete API-backed exports from the shell environment.",
            "claim_type": "limitation",
            "confidence": "Medium",
            "evidence_ids": ["ev_publication_proxy", "ev_ip_trend"],
            "source_ids": ["src_jcp_gemini", "src_2021_10k", "src_sec_2025_10k"],
        },
        {
            "claim_id": "claim_gate_result",
            "section": "breakthrough_gate",
            "text": "Axsome passes the company-level readiness gate through industrialization and adoption, but it remains a strong translational candidate rather than an exceptional breakthrough candidate.",
            "claim_type": "inference",
            "confidence": "High",
            "evidence_ids": ["ev_sales_infrastructure", "ev_rx_coverage", "ev_q1_2026_revenue"],
            "source_ids": ["src_q1_2026_release"],
        },
        {
            "claim_id": "claim_bottom_line",
            "section": "bottom_line",
            "text": "Axsome is a strong translational CNS innovator with commercial momentum, broad IP, and meaningful regulatory execution, but profitability and original-science depth are still gating factors.",
            "claim_type": "inference",
            "confidence": "High",
            "evidence_ids": ["ev_business_overview", "ev_q1_2026_revenue", "ev_ip_portfolio_2026", "ev_2025_financials"],
            "source_ids": ["src_sec_2025_10k", "src_q1_2026_release"],
        },
    ]

    payload = {
        "schema_version": "2.1",
        "company": "Axsome Therapeutics Inc.",
        "ticker": "NASDAQ: AXSM",
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
            "research_date": "2026-05-16",
            "analyst": "codex",
            "run_id": "run-20260516-axsm-innovation",
            "user_request": "Use innovation-analysis to research Axsome Therapeutics Inc., NASDAQ: AXSM, and present results in a Desert Rose dashboard.",
            "time_horizon": "Five years, with current updates through May 16, 2026.",
            "research_mode": "web_research_with_deterministic_scoring",
        },
        "research_context": {
            "focus_technologies": [
                "AXS-05 / Auvelity dextromethorphan-bupropion metabolic inhibition platform",
                "Solriamfetol / Sunosi wake-promoting CNS pharmacology",
                "SYMBRAVO / AXS-07 rapid-absorption migraine formulation",
                "AXS-12, AXS-14, AXS-17, and AXS-20 late-stage or earlier CNS pipeline",
            ],
            "company_identifiers": {
                "legal_name": "Axsome Therapeutics Inc.",
                "ticker": "NASDAQ: AXSM",
                "cik": "0001579428",
            },
            "source_availability": [
                {
                    "domain": "SEC filings",
                    "status": "high",
                    "note": "Current 2025 Form 10-K and older 10-Ks were available through SEC archives.",
                },
                {
                    "domain": "company operating releases",
                    "status": "high",
                    "note": "Q1 2026 company update and product/pipeline/IP pages were available.",
                },
                {
                    "domain": "regulatory approvals",
                    "status": "high",
                    "note": "FDA press release for April 30, 2026 Auvelity AD agitation approval was available.",
                },
                {
                    "domain": "publications",
                    "status": "partial",
                    "note": "Browser search and article pages were available, but direct PubMed/OpenAlex API export from shell was blocked by DNS.",
                },
                {
                    "domain": "patents",
                    "status": "partial",
                    "note": "Company IP page and representative patent pages were available; no complete family-normalized patent export was obtained.",
                },
            ],
            "search_log": [
                {
                    "query": "Axsome Therapeutics 2025 annual report 10-K 2026 AXSM SEC",
                    "source": "web_search",
                    "date": "2026-05-16",
                    "result_quality": "high",
                    "selected": True,
                    "selection_reason": "Primary SEC filing.",
                },
                {
                    "query": "Axsome Therapeutics Reports First Quarter 2026 Financial Results Provides Business Update",
                    "source": "web_search",
                    "date": "2026-05-16",
                    "result_quality": "high",
                    "selected": True,
                    "selection_reason": "Latest operating update.",
                },
                {
                    "query": "FDA approves Auvelity Alzheimer's disease agitation Axsome 2026",
                    "source": "web_search",
                    "date": "2026-05-16",
                    "result_quality": "high",
                    "selected": True,
                    "selection_reason": "Regulator confirmation of approval.",
                },
                {
                    "query": "Axsome Therapeutics intellectual property patents AXS-05 AXS-12",
                    "source": "web_search",
                    "date": "2026-05-16",
                    "result_quality": "high",
                    "selected": True,
                    "selection_reason": "Company IP page and patent records.",
                },
                {
                    "query": "dextromethorphan bupropion AXS-05 GEMINI trial publication",
                    "source": "web_search",
                    "date": "2026-05-16",
                    "result_quality": "high",
                    "selected": True,
                    "selection_reason": "Peer-reviewed clinical evidence.",
                },
                {
                    "query": "solriamfetol narcolepsy obstructive sleep apnea 2025 meta-analysis",
                    "source": "web_search",
                    "date": "2026-05-16",
                    "result_quality": "medium",
                    "selected": True,
                    "selection_reason": "Field evidence for acquired Sunosi/solriamfetol product.",
                },
            ],
            "exclusions": [
                {
                    "candidate_source_or_metric": "Reddit investor summaries",
                    "reason": "Not primary and not necessary after SEC/company/FDA sources were available.",
                },
                {
                    "candidate_source_or_metric": "Stock-price and analyst price targets",
                    "reason": "Outside innovation-readiness scoring scope.",
                },
                {
                    "candidate_source_or_metric": "Unverified generic web summaries of patent counts",
                    "reason": "Replaced by company IP page, SEC filings, and representative patent records.",
                },
            ],
            "judgment_calls": [
                {
                    "topic": "Publication trend proxy",
                    "decision": "Used source-checked publication records by year instead of an exhaustive PubMed/OpenAlex count.",
                    "rationale": "Direct shell API calls failed due DNS restrictions and PubMed pages were intermittently blocked by browser challenge.",
                    "impact": "Lowered Science coverage and publication-growth metric confidence.",
                },
                {
                    "topic": "Patent-family proxy",
                    "decision": "Used SEC/company disclosed issued-patent counts and representative patent pages rather than a deduplicated patent-family census.",
                    "rationale": "Open, source-verified family time series was unavailable in the run.",
                    "impact": "Lowered IP coverage slightly but preserved a transparent quantitative trend.",
                },
                {
                    "topic": "Exceptional breakthrough ceiling",
                    "decision": "Classified Axsome as strong translational momentum rather than exceptional breakthrough.",
                    "rationale": "Commercial adoption and IP are strong, while original modality novelty and complete scientometrics are weaker.",
                    "impact": "Scores kept below 20 even though the readiness gate passes.",
                },
            ],
        },
        "sources": sources,
        "evidence_items": evidence_items,
        "layers": layers,
        "dashboard_content": dashboard_content,
        "claims": claims,
        "normalization_notes": [
            {
                "metric_code": "publication_growth",
                "rule": "Directional proxy mapped to 0..1 using visible source-checked records, not database-complete works.",
                "reason": "Direct API access was unavailable in the local shell.",
            },
            {
                "metric_code": "patent_family_growth",
                "rule": "Company-disclosed issued-patent counts used as lower-bound patent portfolio proxy.",
                "reason": "Deduplicated family time series was not reproducible from available public pages in this run.",
            },
            {
                "metric_code": "revenue_or_booking_evidence",
                "rule": "Commercial-stage revenue growth and absolute quarterly scale mapped to readiness.",
                "reason": "Revenue is a direct adoption signal for marketed therapeutics.",
            },
        ],
        "storage_metadata": {
            "intended_store": "sqlite",
            "recommended_primary_keys": {
                "sources": "source_id",
                "evidence_items": "evidence_id",
                "metrics": "company + research_date + run_id + layer + metric_code",
            },
            "content_hash_fields": [
                "sources",
                "evidence_items",
                "layers",
                "dashboard_content",
                "claims",
                "normalization_notes",
            ],
        },
    }
    return payload


def write_payload(story=None):
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    payload = build_payload(story=story)
    PAYLOAD_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(PAYLOAD_PATH)


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def story_markdown():
    paragraphs = [
        "The story begins with a small trick of chemistry. Dextromethorphan was an old cough medicine. Bupropion was an old antidepressant. Alone, neither looked like a revolution. Together, at the right dose, one held the door open for the other. Bupropion slows an enzyme called CYP2D6, a body cleanup system that normally breaks dextromethorphan down too quickly. That delay lets dextromethorphan stay in the blood long enough to touch brain circuits linked to glutamate, one of the main chemical languages of thought, mood, and agitation.",
        "Axsome built a company around that narrow doorway. In a Phase 3 depression trial, 327 people entered a six-week test. The drug did not erase the old uncertainty of psychiatry, where placebo responses can be powerful and human suffering refuses clean measurement. But it did separate from placebo, and it did so early. The signal became more than an academic graph. It became Auvelity, a medicine approved for major depressive disorder.",
        "Then came the more difficult room. Alzheimer's disease agitation is not ordinary restlessness. It can mean fear, anger, disrupted sleep, exhausted caregivers, and the slow collapse of a household's rhythm. On April 30, 2026, the Food and Drug Administration approved Auvelity for this use and called it the first approved treatment for the condition that is not an antipsychotic. That matters because antipsychotics can carry heavy risks in older dementia patients. The promise here is not immortality or cure. It is quieter. It is the possibility of fewer storms.",
        "The commercial numbers changed the tone of the story. Axsome's 2025 revenue reached $638.5 million. In the first quarter of 2026, it reached $191.2 million. Auvelity carried most of that weight, with about 223,000 prescriptions in the quarter and broad payer coverage. These numbers do not prove destiny. They prove that doctors are prescribing, payers are covering, and patients are entering the system. In biotechnology, that is the dangerous crossing from hope to operations.",
        "The company is not only Auvelity. Sunosi, or solriamfetol, works on dopamine and norepinephrine, chemicals involved in alertness and motivation. It is approved for excessive daytime sleepiness linked to narcolepsy or obstructive sleep apnea, and the surrounding literature continues to compare it with other wake-promoting drugs. Symbravo adds a migraine product. AXS-12 has been submitted to the Food and Drug Administration for cataplexy in narcolepsy. The pipeline is broad enough to be interesting, but breadth can also hide fragility. Each program must still pass its own trial, regulator, payer, and prescriber.",
        "The patent wall is large. Axsome disclosed more than 600 issued patents and more than 450 pending applications worldwide as of February 16, 2026. AXS-05 alone had more than 150 issued United States patents. This is not decorative legal work. It is part of the machine. The Teva settlement points to possible generic Auvelity entry in the late 2030s, depending on conditions. That buys time, but it also reveals the pressure. When a medicine works commercially, copies begin to gather at the edge.",
        "There is a harder truth beneath the momentum. Axsome still lost $183.2 million in 2025 and carried an accumulated deficit above $1.3 billion. The company says its cash can fund operations into cash-flow positivity under its plan. Plans are not physics. They are promises made under uncertainty. The Alzheimer's agitation launch, payer behavior, trial outcomes, and future generic pressure will decide how much of today's promise becomes durable economics.",
        "So Axsome's mystery is not whether it is innovative. It is. The better question is what kind of innovation this is. It is not a clean story of a new biological universe discovered from nothing. It is a story of old molecules made strange again, of metabolism used as a lever, of clinical trials aimed at neglected problems, of patents and sales forces and formularies turning chemistry into access. That kind of innovation can be powerful. It can also be brittle. The next chapter will be written in prescriptions, relapses avoided, cash burn reduced, and trials that either widen the doorway or close it.",
    ]
    return "# Axsome Therapeutics: The Narrow Doorway\n\n" + "\n\n".join(paragraphs) + "\n"


def attach_story():
    if not DASHBOARD_PATH.exists():
        raise SystemExit(f"Base dashboard not found: {DASHBOARD_PATH}")
    base_dashboard = DASHBOARD_PATH.read_text(encoding="utf-8")
    prompt_text = STORY_PROMPT_PATH.read_text(encoding="utf-8") if STORY_PROMPT_PATH.exists() else ""
    body = story_markdown()
    STORY_PATH.write_text(body, encoding="utf-8")
    paragraphs = [p.strip() for p in body.split("\n\n") if p.strip() and not p.startswith("# ")]
    story = {
        "title": "Axsome Therapeutics: The Narrow Doorway",
        "body_markdown": body,
        "paragraphs": paragraphs,
        "source_dashboard_file": "dashboard.html",
        "source_dashboard_hash": sha256_text(base_dashboard),
        "prompt_file": "Story_prompt.txt",
        "prompt_hash": sha256_text(prompt_text),
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "external_sources_used": [],
    }
    write_payload(story=story)
    print(STORY_PATH)


def render_dashboard():
    scored = json.loads(SCORED_PATH.read_text(encoding="utf-8"))
    embedded = json.dumps(scored, ensure_ascii=True).replace("</", "<\\/")
    html_doc = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(scored["company"])} Innovation Dashboard</title>
  <style>
    :root {{
      --dusty-rose: #d4a5a5;
      --clay: #b87d6d;
      --sand: #e8d5c4;
      --burgundy: #5d2e46;
      --paper: #fffaf7;
      --ink: #25151f;
      --muted: #735967;
      --line: rgba(93, 46, 70, 0.18);
      --sage: #58756b;
      --bluegray: #52667a;
      --panel: rgba(255, 250, 247, 0.72);
      --panel-strong: rgba(255, 255, 255, 0.56);
      --shadow: 0 14px 42px rgba(93, 46, 70, 0.10);
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      font-family: FreeSans, Arial, Helvetica, sans-serif;
      color: var(--ink);
      background:
        linear-gradient(90deg, rgba(255,255,255,0.55) 1px, transparent 1px),
        linear-gradient(180deg, rgba(255,255,255,0.4) 1px, transparent 1px),
        linear-gradient(135deg, #fffaf7 0%, #f4e5da 42%, var(--sand) 100%);
      background-size: 44px 44px, 44px 44px, auto;
      min-height: 100vh;
    }}
    a {{ color: var(--burgundy); text-decoration-thickness: 1px; text-underline-offset: 3px; }}
    .shell {{ max-width: 1440px; margin: 0 auto; padding: 28px; }}
    .topbar {{
      display: flex; justify-content: space-between; align-items: center; gap: 16px;
      padding: 12px 0 28px; border-bottom: 1px solid var(--line);
    }}
    .brand {{ display: flex; align-items: baseline; gap: 12px; min-width: 0; }}
    .brand h1 {{ margin: 0; font-size: clamp(28px, 4vw, 56px); line-height: 0.95; letter-spacing: 0; color: var(--burgundy); }}
    .ticker {{ color: var(--muted); font-size: 15px; white-space: nowrap; }}
    .date {{ color: var(--muted); font-size: 14px; text-align: right; }}
    .layout {{ display: grid; grid-template-columns: minmax(0, 1fr) 340px; gap: 32px; align-items: start; padding-top: 28px; }}
    .main {{ display: flex; flex-direction: column; gap: 8px; min-width: 0; }}
    .sidebar {{ position: sticky; top: 18px; display: flex; flex-direction: column; gap: 18px; }}
    .section {{
      border-bottom: 1px solid var(--line);
      padding: 28px 0;
      animation: rise .55s ease both;
    }}
    .main .section:first-child {{ padding-top: 0; }}
    .section h2 {{ margin: 0 0 8px; color: var(--burgundy); font-size: 22px; line-height: 1.15; letter-spacing: 0; }}
    .section p {{ margin: 0; color: var(--muted); line-height: 1.55; }}
    .score-head {{
      display: grid; grid-template-columns: 210px minmax(0, 1fr); gap: 22px; align-items: stretch;
      background: var(--panel);
      border: 1px solid var(--line);
      box-shadow: var(--shadow);
      padding: 22px;
    }}
    .score-dial {{
      min-height: 210px; display: grid; place-items: center; border: 1px solid var(--line);
      background: radial-gradient(circle at center, rgba(212,165,165,.26), rgba(255,250,247,.78) 62%);
    }}
    .score-dial strong {{ font-size: 66px; color: var(--burgundy); line-height: 1; }}
    .score-dial span {{ display: block; margin-top: 6px; color: var(--muted); text-align: center; }}
    .verdict {{ display: flex; flex-direction: column; justify-content: center; gap: 16px; }}
    .verdict .label {{ color: var(--burgundy); font-size: 28px; font-weight: 700; line-height: 1.15; }}
    .badges {{ display: flex; gap: 10px; flex-wrap: wrap; }}
    .badge {{ border: 1px solid var(--line); color: var(--burgundy); background: rgba(232,213,196,.55); padding: 7px 10px; font-size: 13px; }}
    .layer-list {{ display: flex; flex-direction: column; gap: 16px; margin-top: 18px; }}
    .layer {{ border-top: 1px solid var(--line); padding-top: 16px; }}
    .layer-meta {{ display: flex; justify-content: space-between; gap: 18px; align-items: baseline; margin-bottom: 9px; }}
    .layer-name {{ font-weight: 700; color: var(--burgundy); font-size: 17px; }}
    .layer-score {{ color: var(--ink); font-weight: 700; }}
    .bar-track {{ width: 100%; height: 8px; border-radius: 999px; background: rgba(93,46,70,0.12); overflow: hidden; }}
    .bar-fill {{ height: 100%; border-radius: 999px; background: linear-gradient(90deg, var(--clay), var(--burgundy)); box-shadow: 0 0 16px rgba(184,125,109,.32); transform-origin: left; animation: grow .8s ease both; }}
    .layer-body {{ display: grid; grid-template-columns: 1.2fr 1fr 1fr; gap: 14px; margin-top: 12px; }}
    .layer-body div {{ color: var(--muted); font-size: 14px; line-height: 1.45; }}
    .layer-body b {{ color: var(--ink); }}
    .grid-2 {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; margin-top: 18px; }}
    .grid-3 {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; margin-top: 18px; }}
    .item {{
      border: 1px solid var(--line);
      background: var(--panel-strong);
      box-shadow: 0 10px 26px rgba(93, 46, 70, 0.06);
      padding: 16px;
      transition: transform .18s ease, border-color .18s ease, background .18s ease;
    }}
    .item:hover {{ transform: translateY(-2px); border-color: rgba(184,125,109,.65); background: rgba(255,255,255,.72); }}
    .item h3 {{ margin: 0 0 8px; font-size: 16px; color: var(--burgundy); }}
    .item p, .item li {{ font-size: 14px; color: var(--muted); line-height: 1.48; }}
    .item p {{ margin: 0; }}
    .chart-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; margin-top: 18px; }}
    .chart {{ border: 1px solid var(--line); background: var(--panel-strong); box-shadow: 0 10px 26px rgba(93, 46, 70, 0.06); padding: 16px; min-height: 250px; }}
    .chart h3 {{ margin: 0 0 5px; color: var(--burgundy); font-size: 16px; }}
    .bars {{ display: flex; align-items: end; gap: 8px; height: 132px; margin: 18px 0 10px; border-bottom: 1px solid var(--line); }}
    .barcol {{ flex: 1; min-width: 0; display: flex; flex-direction: column; align-items: center; justify-content: end; height: 100%; gap: 6px; }}
    .barval {{ width: 100%; min-height: 2px; background: linear-gradient(180deg, var(--burgundy), var(--clay)); transition: height .45s ease; }}
    .barlabel {{ color: var(--muted); font-size: 11px; max-width: 100%; overflow-wrap: anywhere; text-align: center; line-height: 1.15; min-height: 26px; }}
    .legend {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 6px; }}
    .legend span {{ font-size: 12px; color: var(--muted); border: 1px solid var(--line); padding: 4px 7px; }}
    .mini-list {{ display: flex; flex-direction: column; gap: 10px; margin-top: 14px; }}
    .metric-row {{ display: flex; justify-content: space-between; gap: 12px; padding: 10px 0; border-bottom: 1px solid var(--line); }}
    .metric-row span {{ color: var(--muted); font-size: 13px; }}
    .metric-row strong {{ color: var(--burgundy); font-size: 16px; text-align: right; }}
    .sources li {{ margin-bottom: 10px; color: var(--muted); line-height: 1.35; font-size: 13px; }}
    .sidebar .section {{ background: var(--panel); border: 1px solid var(--line); box-shadow: var(--shadow); padding: 20px; }}
    .story {{ background: linear-gradient(135deg, rgba(93,46,70,.94), rgba(184,125,109,.92)); color: #fffaf7; padding: 24px; border: 0; box-shadow: var(--shadow); }}
    .story h2, .story p {{ color: #fffaf7; }}
    .story p {{ opacity: .92; margin-top: 12px; }}
    .footer-note {{ color: var(--muted); font-size: 12px; line-height: 1.4; }}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(12px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    @keyframes grow {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
    @media (max-width: 1100px) {{
      .layout {{ grid-template-columns: 1fr; }}
      .sidebar {{ position: static; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    }}
    @media (max-width: 760px) {{
      .shell {{ padding: 18px; }}
      .topbar, .score-head, .layer-body, .grid-2, .grid-3, .chart-grid, .sidebar {{ grid-template-columns: 1fr; display: grid; }}
      .topbar {{ align-items: start; }}
      .brand {{ display: block; }}
      .date {{ text-align: left; }}
      .score-dial {{ min-height: 180px; }}
      .section {{ padding: 22px 0; }}
      .score-head, .sidebar .section, .story {{ padding: 18px; }}
    }}
  </style>
</head>
<body>
  <script id="scored-data" type="application/json">{embedded}</script>
  <main class="shell">
    <header class="topbar">
      <div class="brand">
        <h1 id="company"></h1>
        <span class="ticker" id="ticker"></span>
      </div>
      <div class="date" id="run-date"></div>
    </header>
    <div class="layout">
      <div class="main">
        <section class="section score-head">
          <div class="score-dial">
            <div><strong id="total-score"></strong><span>readiness score / 25</span></div>
          </div>
          <div class="verdict">
            <div>
              <p id="hero-sub"></p>
              <div class="label" id="verdict"></div>
            </div>
            <div class="badges">
              <span class="badge" id="gate"></span>
              <span class="badge" id="mode"></span>
              <span class="badge">Desert Rose</span>
            </div>
          </div>
        </section>
        <section class="section" id="thesis"></section>
        <section class="section" id="layers"></section>
        <section class="section" id="technology"></section>
        <section class="section" id="charts"></section>
        <section class="section" id="commercial"></section>
        <section class="section" id="gate-section"></section>
        <section class="section" id="research"></section>
        <section class="section" id="patents"></section>
        <section class="section" id="redflags"></section>
        <section class="section" id="watchlist"></section>
        <section class="section story" id="story" hidden></section>
        <section class="section" id="bottom"></section>
        <section class="section" id="sources"></section>
      </div>
      <aside class="sidebar">
        <section class="section" id="snapshot"></section>
        <section class="section" id="method"></section>
      </aside>
    </div>
  </main>
  <script>
    const data = JSON.parse(document.getElementById('scored-data').textContent);
    const dc = data.dashboard_content || {{}};
    const byId = (id) => document.getElementById(id);
    const esc = (value) => String(value ?? '').replace(/[&<>"']/g, ch => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[ch]));
    const list = (items) => `<div class="grid-2">${{items.map(item => `<div class="item"><p>${{esc(item.text || item.condition || item)}}</p></div>`).join('')}}</div>`;

    byId('company').textContent = data.company;
    byId('ticker').textContent = data.ticker;
    byId('run-date').textContent = `Research date: ${{data.research_run.research_date}}`;
    byId('total-score').textContent = data.display_total_score;
    byId('hero-sub').textContent = dc.hero.subheadline;
    byId('verdict').textContent = data.verdict;
    byId('gate').textContent = data.gate_pass ? 'Gate: pass' : 'Gate: fail';
    byId('mode').textContent = `Mode: ${{data.mode}}`;

    byId('thesis').innerHTML = `<h2>${{esc(dc.thesis.title)}}</h2><p>${{esc(dc.thesis.summary)}}</p><div class="grid-2">${{dc.thesis.bullets.map(b => `<div class="item"><p>${{esc(b.text)}}</p></div>`).join('')}}</div>`;

    byId('layers').innerHTML = `<h2>Five-Layer Dashboard</h2><p>Layer scores are generated by the deterministic scorer from normalized evidence metrics.</p><div class="layer-list">${{data.layers.map(layer => `
      <div class="layer">
        <div class="layer-meta"><span class="layer-name">${{esc(layer.label)}}</span><span class="layer-score">${{esc(layer.display_score)}} / 5</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:${{Math.max(0, Math.min(100, layer.score / 5 * 100))}}%"></div></div>
        <div class="layer-body">
          <div><b>Evidence</b><br>${{esc(layer.summary)}}</div>
          <div><b>Strong</b><br>${{esc(layer.strong)}}</div>
          <div><b>Missing</b><br>${{esc(layer.missing)}}<br><br><b>Confidence</b><br>${{esc(layer.confidence)}} (${{Math.round(layer.coverage_ratio * 100)}}%)</div>
        </div>
      </div>`).join('')}}</div>`;

    byId('technology').innerHTML = `<h2>${{esc(dc.technology_map.title)}}</h2><p>${{esc(dc.technology_map.summary)}}</p><div class="grid-2">${{dc.technology_map.items.map(item => `<div class="item"><h3>${{esc(item.name)}}</h3><p>${{esc(item.description)}}</p><div class="legend"><span>${{esc(item.maturity)}}</span></div></div>`).join('')}}</div>`;

    function renderChart(chart) {{
      const maxVal = Math.max(...chart.series.flatMap(s => s.points.map(p => Number(p.value) || 0)), 1);
      const seriesHtml = chart.series.map((series, idx) => {{
        const bars = series.points.map(p => {{
          const height = Math.max(2, (Number(p.value) || 0) / maxVal * 100);
          return `<div class="barcol" title="${{esc(series.label)}}: ${{esc(p.value)}} ${{esc(series.unit)}}"><div class="barval" style="height:${{height}}%; opacity:${{idx ? .62 : 1}}"></div><div class="barlabel">${{esc(p.period)}}</div></div>`;
        }}).join('');
        return `<div class="bars">${{bars}}</div><div class="legend"><span>${{esc(series.label)}} · ${{esc(series.unit)}}</span></div>`;
      }}).join('');
      return `<div class="chart"><h3>${{esc(chart.title)}}</h3><p>${{esc(chart.description)}}</p>${{seriesHtml}}</div>`;
    }}
    byId('charts').innerHTML = `<h2>${{esc(dc.quantitative_signals.title)}}</h2><p>${{esc(dc.quantitative_signals.summary)}}</p><div class="chart-grid">${{dc.quantitative_signals.charts.map(renderChart).join('')}}</div>`;

    byId('commercial').innerHTML = `<h2>${{esc(dc.commercialization_evidence.title)}}</h2><p>${{esc(dc.commercialization_evidence.summary)}}</p><div class="grid-3">${{dc.commercialization_evidence.items.map(item => `<div class="item"><h3>${{esc(item.label)}}</h3><p>${{esc(item.text)}}</p></div>`).join('')}}</div>`;

    byId('gate-section').innerHTML = `<h2>${{esc(dc.breakthrough_gate.title)}}</h2><p>${{esc(dc.breakthrough_gate.summary)}}</p><div class="grid-2"><div class="item"><h3>Conditions Met</h3>${{dc.breakthrough_gate.conditions_met.map(c => `<p>${{esc(c.condition)}}</p>`).join('')}}</div><div class="item"><h3>Conditions Not Met</h3>${{dc.breakthrough_gate.conditions_not_met.map(c => `<p>${{esc(c.condition)}}</p>`).join('')}}</div></div><div class="legend"><span>${{esc(dc.breakthrough_gate.result)}}</span></div>`;

    byId('research').innerHTML = `<h2>${{esc(dc.university_research_signals.title)}}</h2><p>${{esc(dc.university_research_signals.summary)}}</p><div class="grid-2">${{dc.university_research_signals.institutions.map(inst => `<div class="item"><h3>${{esc(inst.name)}}</h3><p>${{esc(inst.signal)}}</p><div class="legend"><span>${{inst.company_attributable ? 'company-linked' : 'field signal'}}</span><span>${{inst.field_proxy ? 'proxy' : 'direct'}}</span></div></div>`).join('')}}</div>`;

    byId('patents').innerHTML = `<h2>${{esc(dc.patent_signals.title)}}</h2><p>${{esc(dc.patent_signals.summary)}}</p><div class="grid-3">${{dc.patent_signals.families.map(f => `<div class="item"><h3>${{esc(f.publication_or_family_id)}}</h3><p><b>${{esc(f.title)}}</b></p><p>${{esc(f.interpretation)}}</p><div class="legend"><span>${{esc(f.jurisdictions.join(', '))}}</span><span>${{esc(f.priority_date)}}</span></div></div>`).join('')}}</div><p style="margin-top:16px">${{esc(dc.patent_signals.interpretation)}}</p>`;

    byId('redflags').innerHTML = `<h2>Red Flags</h2><div class="grid-2">${{dc.red_flags.map(r => `<div class="item"><h3>${{esc(r.title)}}</h3><p>${{esc(r.text)}}</p><div class="legend"><span>${{esc(r.severity)}}</span><span>${{esc(r.layer)}}</span></div></div>`).join('')}}</div>`;

    byId('watchlist').innerHTML = `<h2>${{esc(dc.watchlist.title)}}</h2><div class="grid-2"><div class="item"><h3>Upgrade Signals</h3>${{dc.watchlist.upgrade_signals.map(s => `<p>${{esc(s.text)}}</p>`).join('')}}</div><div class="item"><h3>Downgrade Signals</h3>${{dc.watchlist.downgrade_signals.map(s => `<p>${{esc(s.text)}}</p>`).join('')}}</div></div>`;

    if (dc.story) {{
      byId('story').hidden = false;
      byId('story').innerHTML = `<h2>${{esc(dc.story.title)}}</h2>${{dc.story.paragraphs.map(p => `<p>${{esc(p)}}</p>`).join('')}}`;
    }}

    byId('bottom').innerHTML = `<h2>${{esc(dc.bottom_line.title)}}</h2><p>${{esc(dc.bottom_line.text)}}</p>`;
    byId('snapshot').innerHTML = `<h2>${{esc(dc.operational_snapshot.title)}}</h2><div class="mini-list">${{dc.operational_snapshot.metrics.map(m => `<div class="metric-row"><span>${{esc(m.label)}}<br>${{esc(m.period)}}</span><strong>${{esc(m.value)}}</strong></div>`).join('')}}</div>`;
    byId('method').innerHTML = `<h2>${{esc(dc.method_notes.title)}}</h2><div class="mini-list">${{dc.method_notes.notes.map(n => `<p class="footer-note">${{esc(n)}}</p>`).join('')}}</div>`;
    byId('sources').innerHTML = `<h2>Sources</h2><ol class="sources">${{data.sources.map(s => `<li><a href="${{esc(s.url)}}">${{esc(s.title)}}</a><br>${{esc(s.publisher)}} · ${{esc(s.document_date)}} · ${{esc(s.source_type)}}</li>`).join('')}}</ol>`;
  </script>
</body>
</html>
"""
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    DASHBOARD_PATH.write_text(html_doc, encoding="utf-8")
    print(DASHBOARD_PATH)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["write-base", "attach-story", "render"])
    args = parser.parse_args()

    if args.command == "write-base":
        write_payload()
    elif args.command == "attach-story":
        attach_story()
    elif args.command == "render":
        render_dashboard()


if __name__ == "__main__":
    main()
