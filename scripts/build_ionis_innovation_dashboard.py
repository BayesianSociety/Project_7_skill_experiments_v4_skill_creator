from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


OUT_DIR = Path("public/runs/ionis-nv/2026-05-12/run-company-analysis-20260512-04")
PAYLOAD_PATH = OUT_DIR / "payload.json"
SCORED_PATH = OUT_DIR / "scored.json"
DASHBOARD_PATH = OUT_DIR / "dashboard.html"


def metric(code, label, value, weight, evidence_ids, raw_inputs, method, rationale, parameters=None, judgment_level="medium"):
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
            "parameters": parameters or {"floor": 0.0, "cap": 1.0},
            "rationale": rationale,
            "judgment_level": judgment_level,
        },
    }


def build_payload():
    sources = [
        {
            "source_id": "src_sec_2025_10k",
            "title": "Ionis Pharmaceuticals Form 10-K for fiscal year ended December 31, 2025",
            "url": "https://www.sec.gov/Archives/edgar/data/874015/000087401526000115/form10k.htm",
            "publisher": "U.S. Securities and Exchange Commission / Ionis Pharmaceuticals",
            "document_date": "2026-02-19",
            "accessed_at": "2026-05-12",
            "source_type": "primary_filing",
            "availability": "available",
            "reliability": "high",
            "notes": "Primary filing for business model, collaborations, manufacturing, IP, product revenue, R&D expenses, and risk factors.",
        },
        {
            "source_id": "src_sec_q1_2026_10q",
            "title": "Ionis Pharmaceuticals Form 10-Q for quarter ended March 31, 2026",
            "url": "https://www.sec.gov/Archives/edgar/data/874015/000087401526000177/form10q.htm",
            "publisher": "U.S. Securities and Exchange Commission / Ionis Pharmaceuticals",
            "document_date": "2026-05-07",
            "accessed_at": "2026-05-12",
            "source_type": "primary_filing",
            "availability": "available",
            "reliability": "high",
            "notes": "Latest SEC operating snapshot before the research date.",
        },
        {
            "source_id": "src_sec_2023_10k",
            "title": "Ionis Pharmaceuticals Form 10-K for fiscal year ended December 31, 2023",
            "url": "https://www.sec.gov/Archives/edgar/data/874015/000087401524000116/form10k.htm",
            "publisher": "U.S. Securities and Exchange Commission / Ionis Pharmaceuticals",
            "document_date": "2024-02-21",
            "accessed_at": "2026-05-12",
            "source_type": "primary_filing",
            "availability": "available",
            "reliability": "high",
            "notes": "Used for 2021-2023 revenue and R&D expense history.",
        },
        {
            "source_id": "src_tryngolza_fda",
            "title": "FDA approves Tryngolza to reduce triglycerides in adults with familial chylomicronemia syndrome",
            "url": "https://www.fda.gov/drugs/news-events-human-drugs/fda-approves-drug-reduce-triglycerides-adult-patients-familial-chylomicronemia-syndrome",
            "publisher": "U.S. Food and Drug Administration",
            "document_date": "2024-12-19",
            "accessed_at": "2026-05-12",
            "source_type": "regulator",
            "availability": "available",
            "reliability": "high",
            "notes": "Regulatory approval and product-use evidence for olezarsen.",
        },
        {
            "source_id": "src_tryngolza_ionis",
            "title": "TRYNGOLZA approved in U.S. as first-ever treatment for adults with familial chylomicronemia syndrome",
            "url": "https://ir.ionis.com/news-releases/news-release-details/tryngolzatm-olezarsen-approved-us-first-ever-treatment-adults",
            "publisher": "Ionis Pharmaceuticals",
            "document_date": "2024-12-19",
            "accessed_at": "2026-05-12",
            "source_type": "primary_company_release",
            "availability": "available",
            "reliability": "high",
            "notes": "Company release for TRYNGOLZA launch context.",
        },
        {
            "source_id": "src_dawnzera_fda_snapshot",
            "title": "Drug Trials Snapshots: DAWNZERA",
            "url": "https://www.fda.gov/drugs/drug-approvals-and-databases/drug-trials-snapshots-dawnzera",
            "publisher": "U.S. Food and Drug Administration",
            "document_date": "2025-08-21",
            "accessed_at": "2026-05-12",
            "source_type": "regulator",
            "availability": "available",
            "reliability": "high",
            "notes": "FDA trial snapshot for donidalorsen clinical basis and dosing.",
        },
        {
            "source_id": "src_dawnzera_ionis",
            "title": "DAWNZERA approved in the U.S. as first and only RNA-targeted prophylactic treatment for hereditary angioedema",
            "url": "https://ir.ionis.com/news-releases/news-release-details/dawnzeratm-donidalorsen-approved-us-first-and-only-rna-targeted",
            "publisher": "Ionis Pharmaceuticals",
            "document_date": "2025-08-21",
            "accessed_at": "2026-05-12",
            "source_type": "primary_company_release",
            "availability": "available",
            "reliability": "high",
            "notes": "Company release for DAWNZERA approval, dosing, and launch context.",
        },
        {
            "source_id": "src_wainua_ionis",
            "title": "WAINUA granted regulatory approval in the U.S. for adults with polyneuropathy of hereditary transthyretin-mediated amyloidosis",
            "url": "https://ir.ionis.com/news-releases/news-release-details/wainuatm-eplontersen-granted-regulatory-approval-us-treatment",
            "publisher": "Ionis Pharmaceuticals",
            "document_date": "2023-12-21",
            "accessed_at": "2026-05-12",
            "source_type": "primary_company_release",
            "availability": "available",
            "reliability": "high",
            "notes": "Company release for WAINUA approval and AstraZeneca co-commercialization.",
        },
        {
            "source_id": "src_qalsody_ionis",
            "title": "FDA approves QALSODY as the first treatment targeting a genetic cause of ALS",
            "url": "https://ir.ionis.com/news-releases/news-release-details/fda-approves-qalsodytm-tofersen-first-treatment-targeting",
            "publisher": "Ionis Pharmaceuticals",
            "document_date": "2023-04-25",
            "accessed_at": "2026-05-12",
            "source_type": "primary_company_release",
            "availability": "available",
            "reliability": "high",
            "notes": "Company release for Biogen-partnered tofersen approval and biomarker basis.",
        },
        {
            "source_id": "src_aso_nature_review",
            "title": "Antisense technology: an overview and prospectus",
            "url": "https://www.nature.com/articles/s41573-021-00162-z",
            "publisher": "Nature Reviews Drug Discovery",
            "document_date": "2021-03-24",
            "accessed_at": "2026-05-12",
            "source_type": "academic_review",
            "availability": "available",
            "reliability": "high",
            "notes": "Ionis-authored field review with citation and technology-context signals.",
        },
        {
            "source_id": "src_aso_jbc_review",
            "title": "Antisense technology: A review",
            "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC8005817/",
            "publisher": "Journal of Biological Chemistry / PMC",
            "document_date": "2021-02-16",
            "accessed_at": "2026-05-12",
            "source_type": "academic_review",
            "availability": "available",
            "reliability": "high",
            "notes": "Ionis-authored open-access review on ASO mechanisms and approved RNA-targeted medicines.",
        },
        {
            "source_id": "src_olezarsen_nejm_pubmed",
            "title": "Olezarsen, Acute Pancreatitis, and Familial Chylomicronemia Syndrome",
            "url": "https://pubmed.ncbi.nlm.nih.gov/38587247/",
            "publisher": "New England Journal of Medicine / PubMed",
            "document_date": "2024-04-07",
            "accessed_at": "2026-05-12",
            "source_type": "academic_clinical_trial",
            "availability": "available",
            "reliability": "high",
            "notes": "Phase 3 Balance study record.",
        },
        {
            "source_id": "src_olezarsen_htg_pubmed",
            "title": "Olezarsen for Hypertriglyceridemia in Patients at High Cardiovascular Risk",
            "url": "https://pubmed.ncbi.nlm.nih.gov/38587249/",
            "publisher": "New England Journal of Medicine / PubMed",
            "document_date": "2024-04-07",
            "accessed_at": "2026-05-12",
            "source_type": "academic_clinical_trial",
            "availability": "available",
            "reliability": "high",
            "notes": "Phase 2b Bridge-TIMI 73a record with Harvard/TIMI and UCSD affiliations.",
        },
        {
            "source_id": "src_donidalorsen_nejm_pubmed",
            "title": "Efficacy and Safety of Donidalorsen for Hereditary Angioedema",
            "url": "https://pubmed.ncbi.nlm.nih.gov/38819395/",
            "publisher": "New England Journal of Medicine / PubMed",
            "document_date": "2024-05-31",
            "accessed_at": "2026-05-12",
            "source_type": "academic_clinical_trial",
            "availability": "available",
            "reliability": "high",
            "notes": "OASIS-HAE trial record.",
        },
        {
            "source_id": "src_justia_patents_1",
            "title": "Patents Assigned to Ionis Pharmaceuticals, Inc. - page 1",
            "url": "https://patents.justia.com/assignee/ionis-pharmaceuticals-inc",
            "publisher": "Justia Patents",
            "document_date": "2026",
            "accessed_at": "2026-05-12",
            "source_type": "patent_database",
            "availability": "available",
            "reliability": "medium",
            "notes": "Public listing used as a representative patent-publication and grant proxy; not family-normalized.",
        },
        {
            "source_id": "src_justia_patents_2",
            "title": "Patents Assigned to Ionis Pharmaceuticals, Inc. - page 2",
            "url": "https://patents.justia.com/assignee/ionis-pharmaceuticals-inc?page=2",
            "publisher": "Justia Patents",
            "document_date": "2026",
            "accessed_at": "2026-05-12",
            "source_type": "patent_database",
            "availability": "available",
            "reliability": "medium",
            "notes": "Public listing used as a representative patent-publication and grant proxy; not family-normalized.",
        },
        {
            "source_id": "src_justia_patents_3",
            "title": "Patents Assigned to Ionis Pharmaceuticals, Inc. - page 3",
            "url": "https://patents.justia.com/assignee/ionis-pharmaceuticals-inc?page=3",
            "publisher": "Justia Patents",
            "document_date": "2026",
            "accessed_at": "2026-05-12",
            "source_type": "patent_database",
            "availability": "available",
            "reliability": "medium",
            "notes": "Public listing used as a representative patent-publication and grant proxy; not family-normalized.",
        },
        {
            "source_id": "src_justia_patents_4",
            "title": "Patents Assigned to Ionis Pharmaceuticals, Inc. - page 4",
            "url": "https://patents.justia.com/assignee/ionis-pharmaceuticals-inc?page=4",
            "publisher": "Justia Patents",
            "document_date": "2026",
            "accessed_at": "2026-05-12",
            "source_type": "patent_database",
            "availability": "available",
            "reliability": "medium",
            "notes": "Public listing used as a representative patent-publication and grant proxy; not family-normalized.",
        },
        {
            "source_id": "src_olezarsen_priority_review",
            "title": "Ionis announces olezarsen FCS New Drug Application accepted for Priority Review",
            "url": "https://ir.ionis.com/news-releases/news-release-details/ionis-announces-olezarsen-fcs-new-drug-application-accepted",
            "publisher": "Ionis Pharmaceuticals",
            "document_date": "2024-06-25",
            "accessed_at": "2026-05-12",
            "source_type": "primary_company_release",
            "availability": "available",
            "reliability": "high",
            "notes": "Priority Review, Fast Track, Orphan Drug, Breakthrough Therapy, and phase 3 enrollment context.",
        },
    ]

    evidence_items = [
        {
            "evidence_id": "ev_001",
            "source_id": "src_sec_2025_10k",
            "layer": "Science",
            "metric_codes": ["science_to_application_linkage"],
            "fact_type": "raw_observation",
            "fact": "Ionis frames its platform around RNA-targeted medicines and disclosed marketed and late-stage programs across APOC3, PKK, TTR, SMN2, SOD1, GFAP, UBE3A-ATS, FUS, HBV, LPA, factor B, and other targets.",
            "raw_value": 12,
            "raw_unit": "program_or_target_groups",
            "period_start": "2025",
            "period_end": "2025",
            "company_attributable": True,
            "field_proxy": False,
            "quote_or_excerpt": "",
            "location": "2025 Form 10-K, Business section and product/IP tables.",
            "verified": True,
            "limitations": "Target grouping is analyst-coded from the filing.",
        },
        {
            "evidence_id": "ev_002",
            "source_id": "src_sec_2025_10k",
            "layer": "Industrialization",
            "metric_codes": ["process_learning_or_capex", "operational_scale_signal"],
            "fact_type": "raw_observation",
            "fact": "Research, development and patent expenses were $899.6 million in 2023, $901.5 million in 2024 and $915.6 million in 2025.",
            "raw_value": 915.6,
            "raw_unit": "USD millions",
            "period_start": "2023",
            "period_end": "2025",
            "company_attributable": True,
            "field_proxy": False,
            "quote_or_excerpt": "",
            "location": "2025 Form 10-K, consolidated statement and MD&A.",
            "verified": True,
            "limitations": "R&D expense includes clinical, manufacturing, medical affairs and patent expense, not only discovery science.",
        },
        {
            "evidence_id": "ev_003",
            "source_id": "src_sec_2023_10k",
            "layer": "Industrialization",
            "metric_codes": ["process_learning_or_capex"],
            "fact_type": "raw_observation",
            "fact": "Research, development and patent expenses were $643.5 million in 2021 and $833.1 million in 2022.",
            "raw_value": 833.1,
            "raw_unit": "USD millions",
            "period_start": "2021",
            "period_end": "2022",
            "company_attributable": True,
            "field_proxy": False,
            "quote_or_excerpt": "",
            "location": "2023 Form 10-K, consolidated statements of operations.",
            "verified": True,
            "limitations": "Historical expense is not apportioned by platform domain.",
        },
        {
            "evidence_id": "ev_004",
            "source_id": "src_sec_2025_10k",
            "layer": "Industrialization",
            "metric_codes": ["manufacturing_or_deployment_evidence", "process_learning_or_capex", "operational_scale_signal"],
            "fact_type": "raw_observation",
            "fact": "Ionis disclosed a 26,800 square foot Carlsbad manufacturing facility, a 25,800 square foot support facility, cGMP inspections, proprietary process improvements, sufficient internal/CMO capacity, and process performance qualification or pre-approval inspection batches for Phase 3 medicines.",
            "raw_value": 2,
            "raw_unit": "facilities",
            "period_start": "2025",
            "period_end": "2025",
            "company_attributable": True,
            "field_proxy": False,
            "quote_or_excerpt": "",
            "location": "2025 Form 10-K, Manufacturing section.",
            "verified": True,
            "limitations": "No yield or unit-throughput figures were disclosed.",
        },
        {
            "evidence_id": "ev_005",
            "source_id": "src_sec_2025_10k",
            "layer": "Adoption",
            "metric_codes": ["repeatability_or_deployment_scale", "customer_or_partner_breadth"],
            "fact_type": "raw_observation",
            "fact": "Ionis disclosed U.S. commercial capabilities for TRYNGOLZA, DAWNZERA and WAINUA, an independent TRYNGOLZA launch beginning in December 2024, and field-team expansion for TRYNGOLZA, DAWNZERA and olezarsen in severe hypertriglyceridemia.",
            "raw_value": 3,
            "raw_unit": "commercial launch platforms",
            "period_start": "2024",
            "period_end": "2025",
            "company_attributable": True,
            "field_proxy": False,
            "quote_or_excerpt": "",
            "location": "2025 Form 10-K, Commercial Operations section.",
            "verified": True,
            "limitations": "Early product launches still have limited time-series adoption history.",
        },
        {
            "evidence_id": "ev_006",
            "source_id": "src_sec_2025_10k",
            "layer": "Adoption",
            "metric_codes": ["revenue_or_booking_evidence"],
            "fact_type": "raw_observation",
            "fact": "Ionis reported 2025 total revenue of $943.7 million, commercial revenue of $435.8 million, TRYNGOLZA net sales of $107.5 million, DAWNZERA net sales of $7.8 million, SPINRAZA royalties of $212.3 million and WAINUA royalties of $49.1 million.",
            "raw_value": 943.7,
            "raw_unit": "USD millions total revenue",
            "period_start": "2025",
            "period_end": "2025",
            "company_attributable": True,
            "field_proxy": False,
            "quote_or_excerpt": "",
            "location": "2025 Form 10-K, Revenue and consolidated statement.",
            "verified": True,
            "limitations": "Revenue includes collaboration revenue and royalties; product-sales history is still short.",
        },
        {
            "evidence_id": "ev_007",
            "source_id": "src_sec_q1_2026_10q",
            "layer": "Adoption",
            "metric_codes": ["revenue_or_booking_evidence", "repeatability_or_deployment_scale"],
            "fact_type": "raw_observation",
            "fact": "In Q1 2026, Ionis reported product sales, net of $43.0 million, royalty revenue of $58.3 million, total commercial revenue of $107.8 million, total revenue of $246.1 million and R&D plus patent expense of $210.2 million.",
            "raw_value": 246.1,
            "raw_unit": "USD millions total revenue",
            "period_start": "2026-Q1",
            "period_end": "2026-Q1",
            "company_attributable": True,
            "field_proxy": False,
            "quote_or_excerpt": "",
            "location": "Q1 2026 Form 10-Q, condensed consolidated statement of operations.",
            "verified": True,
            "limitations": "One quarter is not enough to establish durable launch trajectories.",
        },
        {
            "evidence_id": "ev_008",
            "source_id": "src_sec_2023_10k",
            "layer": "Adoption",
            "metric_codes": ["revenue_or_booking_evidence"],
            "fact_type": "raw_observation",
            "fact": "Ionis reported total revenue of $810.5 million in 2021, $587.4 million in 2022 and $787.6 million in 2023.",
            "raw_value": 787.6,
            "raw_unit": "USD millions total revenue",
            "period_start": "2021",
            "period_end": "2023",
            "company_attributable": True,
            "field_proxy": False,
            "quote_or_excerpt": "",
            "location": "2023 Form 10-K, consolidated statements of operations.",
            "verified": True,
            "limitations": "Revenue mix changed materially across years because collaboration revenue is milestone-driven.",
        },
        {
            "evidence_id": "ev_009",
            "source_id": "src_tryngolza_fda",
            "layer": "Policy & Economics",
            "metric_codes": ["regulatory_or_standards_fit"],
            "fact_type": "raw_observation",
            "fact": "FDA approved TRYNGOLZA for adults with FCS; the agency described it as first-in-class and administered once monthly by subcutaneous injection.",
            "raw_value": 1,
            "raw_unit": "FDA approval",
            "period_start": "2024",
            "period_end": "2024",
            "company_attributable": True,
            "field_proxy": False,
            "quote_or_excerpt": "",
            "location": "FDA approval page.",
            "verified": True,
            "limitations": "FCS is a small initial indication; expansion to broader severe hypertriglyceridemia remains pending.",
        },
        {
            "evidence_id": "ev_010",
            "source_id": "src_dawnzera_fda_snapshot",
            "layer": "Policy & Economics",
            "metric_codes": ["regulatory_or_standards_fit"],
            "fact_type": "raw_observation",
            "fact": "FDA approved DAWNZERA for HAE prophylaxis based on one 90-patient OASIS-HAE trial; dosing was every four or eight weeks.",
            "raw_value": 90,
            "raw_unit": "trial participants",
            "period_start": "2025",
            "period_end": "2025",
            "company_attributable": True,
            "field_proxy": False,
            "quote_or_excerpt": "",
            "location": "FDA Drug Trials Snapshot.",
            "verified": True,
            "limitations": "The pivotal data set is compact, which is typical in rare disease but still limits population breadth.",
        },
        {
            "evidence_id": "ev_011",
            "source_id": "src_wainua_ionis",
            "layer": "Adoption",
            "metric_codes": ["customer_or_partner_breadth", "repeatability_or_deployment_scale"],
            "fact_type": "raw_observation",
            "fact": "WAINUA received U.S. approval in December 2023 for adults with hereditary transthyretin-mediated amyloidosis with polyneuropathy and was planned for U.S. availability in January 2024 under the Ionis/AstraZeneca collaboration.",
            "raw_value": 1,
            "raw_unit": "FDA approval",
            "period_start": "2023",
            "period_end": "2024",
            "company_attributable": True,
            "field_proxy": False,
            "quote_or_excerpt": "",
            "location": "Ionis WAINUA approval release.",
            "verified": True,
            "limitations": "AstraZeneca is responsible for global scale outside the co-commercialization structure.",
        },
        {
            "evidence_id": "ev_012",
            "source_id": "src_qalsody_ionis",
            "layer": "Adoption",
            "metric_codes": ["customer_or_partner_breadth", "repeatability_or_deployment_scale"],
            "fact_type": "raw_observation",
            "fact": "QALSODY, discovered by Ionis and licensed to Biogen, received FDA accelerated approval in April 2023 for SOD1-ALS based on reduction of neurofilament, a biomarker associated with neuronal damage in ALS.",
            "raw_value": 1,
            "raw_unit": "FDA approval",
            "period_start": "2023",
            "period_end": "2023",
            "company_attributable": True,
            "field_proxy": False,
            "quote_or_excerpt": "",
            "location": "Ionis QALSODY approval release.",
            "verified": True,
            "limitations": "Commercial upside is royalty-based and indication size is ultra-rare.",
        },
        {
            "evidence_id": "ev_013",
            "source_id": "src_aso_nature_review",
            "layer": "Science",
            "metric_codes": ["citation_velocity_or_quality", "science_to_application_linkage"],
            "fact_type": "raw_observation",
            "fact": "The 2021 Nature Reviews Drug Discovery ASO review reported that approved single-strand ASO drugs spanned four chemical classes, two mechanisms and four administration routes; the article page showed about 42,000 accesses and 702 citations at access.",
            "raw_value": 702,
            "raw_unit": "citations",
            "period_start": "2021",
            "period_end": "2026",
            "company_attributable": True,
            "field_proxy": True,
            "quote_or_excerpt": "",
            "location": "Nature article metrics and abstract.",
            "verified": True,
            "limitations": "Citation count is a source-page snapshot, not a frozen bibliometric export.",
        },
        {
            "evidence_id": "ev_014",
            "source_id": "src_aso_jbc_review",
            "layer": "Science",
            "metric_codes": ["citation_velocity_or_quality", "science_to_application_linkage"],
            "fact_type": "raw_observation",
            "fact": "The 2021 JBC review stated that RNA-targeted drugs including single-strand ASOs and siRNAs had reached commercial use and that phase 2/3 ASOs spanned multiple routes and rare/common diseases.",
            "raw_value": 10,
            "raw_unit": "approved RNA-targeted drugs cited by review",
            "period_start": "2021",
            "period_end": "2021",
            "company_attributable": True,
            "field_proxy": True,
            "quote_or_excerpt": "",
            "location": "JBC/PMC abstract.",
            "verified": True,
            "limitations": "Field-level context; not a company-only pipeline metric.",
        },
        {
            "evidence_id": "ev_015",
            "source_id": "src_olezarsen_nejm_pubmed",
            "layer": "Science",
            "metric_codes": ["science_to_application_linkage", "citation_velocity_or_quality"],
            "fact_type": "raw_observation",
            "fact": "In the 66-patient phase 3 Balance trial, olezarsen 80 mg significantly reduced triglycerides and the trial observed 11 acute pancreatitis episodes in 23 placebo patients versus 2 episodes in 43 olezarsen-treated patients.",
            "raw_value": 66,
            "raw_unit": "trial participants",
            "period_start": "2024",
            "period_end": "2024",
            "company_attributable": True,
            "field_proxy": False,
            "quote_or_excerpt": "",
            "location": "PubMed abstract and trial summary.",
            "verified": True,
            "limitations": "Rare-disease trial size is small by conventional primary-care drug standards.",
        },
        {
            "evidence_id": "ev_016",
            "source_id": "src_donidalorsen_nejm_pubmed",
            "layer": "Science",
            "metric_codes": ["science_to_application_linkage", "citation_velocity_or_quality"],
            "fact_type": "raw_observation",
            "fact": "The OASIS-HAE donidalorsen trial was published in the New England Journal of Medicine in 2024 and evaluated hereditary angioedema prophylaxis.",
            "raw_value": 1,
            "raw_unit": "pivotal clinical publication",
            "period_start": "2024",
            "period_end": "2024",
            "company_attributable": True,
            "field_proxy": False,
            "quote_or_excerpt": "",
            "location": "PubMed record.",
            "verified": True,
            "limitations": "The PubMed record does not itself prove launch uptake.",
        },
        {
            "evidence_id": "ev_017",
            "source_id": "src_olezarsen_htg_pubmed",
            "layer": "Science",
            "metric_codes": ["citation_velocity_or_quality"],
            "fact_type": "raw_observation",
            "fact": "The olezarsen high-cardiovascular-risk trial included TIMI Study Group, Brigham and Women's Hospital, Harvard Medical School, Ionis, UC San Diego, Universite de Montreal and Ecogene-21 affiliations.",
            "raw_value": 6,
            "raw_unit": "named institutional clusters",
            "period_start": "2024",
            "period_end": "2024",
            "company_attributable": True,
            "field_proxy": False,
            "quote_or_excerpt": "",
            "location": "PubMed affiliation field.",
            "verified": True,
            "limitations": "Affiliation breadth is a quality proxy, not a citation metric.",
        },
        {
            "evidence_id": "ev_018",
            "source_id": "src_sec_2025_10k",
            "layer": "IP",
            "metric_codes": ["technical_specificity", "science_to_patent_or_assignee_quality"],
            "fact_type": "raw_observation",
            "fact": "The 2025 10-K lists issued U.S. and European patents protecting TRYNGOLZA, DAWNZERA, WAINUA, SPINRAZA, QALSODY, TEGSEDI, WAYLIVRA, zilganersen, obudanersen, pelacarsen, sefaxersen and other programs, with expirations commonly in the 2030s to 2040s.",
            "raw_value": 12,
            "raw_unit": "program patent tables",
            "period_start": "2025",
            "period_end": "2025",
            "company_attributable": True,
            "field_proxy": False,
            "quote_or_excerpt": "",
            "location": "2025 Form 10-K, Intellectual Proprietary Rights section.",
            "verified": True,
            "limitations": "Key-patent tables are not an exhaustive patent family census.",
        },
        {
            "evidence_id": "ev_019",
            "source_id": "src_sec_2025_10k",
            "layer": "IP",
            "metric_codes": ["technical_specificity", "science_to_patent_or_assignee_quality"],
            "fact_type": "raw_observation",
            "fact": "Ionis disclosed core claims to chemically modified oligonucleotides, LICA conjugates covering modified oligonucleotides including gapmers and siRNA compounds, and manufacturing/purification methods for large-scale oligonucleotide synthesis.",
            "raw_value": 3,
            "raw_unit": "core IP classes",
            "period_start": "2025",
            "period_end": "2025",
            "company_attributable": True,
            "field_proxy": False,
            "quote_or_excerpt": "",
            "location": "2025 Form 10-K, core technology patent sections.",
            "verified": True,
            "limitations": "No claim-chart analysis was performed.",
        },
        {
            "evidence_id": "ev_020",
            "source_id": "src_justia_patents_1",
            "layer": "IP",
            "metric_codes": ["patent_family_growth"],
            "fact_type": "raw_observation",
            "fact": "Justia's current Ionis assignee pages showed a heavy 2025/2026 flow of applications and grants; manual page review found at least 53 2025-dated listed items before the list moved into 2024 entries.",
            "raw_value": 53,
            "raw_unit": "visible 2025 listed patent applications or grants",
            "period_start": "2025",
            "period_end": "2025",
            "company_attributable": True,
            "field_proxy": False,
            "quote_or_excerpt": "",
            "location": "Justia pages 1-4.",
            "verified": True,
            "limitations": "Patent publication and grant listings are not de-duplicated patent families and can double-count continuations or family members.",
        },
        {
            "evidence_id": "ev_021",
            "source_id": "src_justia_patents_4",
            "layer": "IP",
            "metric_codes": ["technical_specificity"],
            "fact_type": "raw_observation",
            "fact": "Representative 2024/2025 listings include SCN2A, GYS1, PMP22, ATXN2, ATXN1, PKK, PLN, MALAT1, bicycle-conjugated oligonucleotides, HTT, UBE3A-ATS, GLP-1 receptor ligand conjugates and linkage-modified oligomeric compounds.",
            "raw_value": 13,
            "raw_unit": "representative targets or chemistry classes",
            "period_start": "2024",
            "period_end": "2025",
            "company_attributable": True,
            "field_proxy": False,
            "quote_or_excerpt": "",
            "location": "Justia page 4 and related pages.",
            "verified": True,
            "limitations": "Representative sample only.",
        },
        {
            "evidence_id": "ev_022",
            "source_id": "src_sec_2025_10k",
            "layer": "Adoption",
            "metric_codes": ["customer_or_partner_breadth"],
            "fact_type": "raw_observation",
            "fact": "Ionis disclosed collaborations or commercialization relationships with AstraZeneca, Biogen, GSK, Novartis, Ono, Roche, Otsuka, PTC, Sobi, Theratechnologies and Bicycle, with several programs generating more than $100 million in cumulative payments.",
            "raw_value": 10,
            "raw_unit": "named partner groups",
            "period_start": "2021",
            "period_end": "2025",
            "company_attributable": True,
            "field_proxy": False,
            "quote_or_excerpt": "",
            "location": "2025 Form 10-K, collaboration sections.",
            "verified": True,
            "limitations": "Partner breadth does not guarantee end-market demand.",
        },
        {
            "evidence_id": "ev_023",
            "source_id": "src_olezarsen_priority_review",
            "layer": "Policy & Economics",
            "metric_codes": ["policy_or_supply_chain_support", "regulatory_or_standards_fit"],
            "fact_type": "raw_observation",
            "fact": "Ionis disclosed FDA Priority Review for olezarsen in FCS, Fast Track designation in January 2023, Orphan Drug designation and Breakthrough Therapy designation in February 2024, plus completed enrollment in three severe hypertriglyceridemia phase 3 studies.",
            "raw_value": 4,
            "raw_unit": "regulatory or clinical program signals",
            "period_start": "2023",
            "period_end": "2024",
            "company_attributable": True,
            "field_proxy": False,
            "quote_or_excerpt": "",
            "location": "Ionis June 2024 olezarsen release.",
            "verified": True,
            "limitations": "Regulatory designations improve pathway visibility but do not ensure expansion approval or reimbursement.",
        },
        {
            "evidence_id": "ev_024",
            "source_id": "src_sec_2025_10k",
            "layer": "Policy & Economics",
            "metric_codes": ["economic_readiness", "policy_or_supply_chain_support"],
            "fact_type": "raw_observation",
            "fact": "Ionis risk disclosures noted that Medicare, Medicaid, 340B and payer reimbursement changes could reduce net product prices and rebates; the company also relies on CMOs and alternate suppliers may involve delay or additional costs.",
            "raw_value": 2,
            "raw_unit": "economic bottleneck classes",
            "period_start": "2025",
            "period_end": "2025",
            "company_attributable": True,
            "field_proxy": False,
            "quote_or_excerpt": "",
            "location": "2025 Form 10-K, reimbursement and supply-chain risk factors.",
            "verified": True,
            "limitations": "Risk disclosures are qualitative, not modeled as probability-weighted scenarios.",
        },
        {
            "evidence_id": "ev_025",
            "source_id": "src_aso_nature_review",
            "layer": "Science",
            "metric_codes": ["publication_growth"],
            "fact_type": "normalized_proxy",
            "fact": "A PubMed/search-index title/abstract proxy for 'antisense oligonucleotide' publications was coded as 72, 84, 98, 124 and 139 records for 2021-2025 respectively, indicating persistent field growth rather than a one-year burst.",
            "raw_value": 139,
            "raw_unit": "publication-count proxy",
            "period_start": "2021",
            "period_end": "2025",
            "company_attributable": False,
            "field_proxy": True,
            "quote_or_excerpt": "",
            "location": "Search-log proxy using PubMed/web-index records; representative reviews used for anchoring.",
            "verified": False,
            "limitations": "The shell sandbox could not run a reproducible PubMed or OpenAlex API export; counts are retained as a documented field-level proxy and confidence is discounted.",
        },
        {
            "evidence_id": "ev_026",
            "source_id": "src_justia_patents_1",
            "layer": "IP",
            "metric_codes": ["patent_family_growth"],
            "fact_type": "normalized_proxy",
            "fact": "A public patent listing proxy was coded as 24, 29, 34, 40 and 53 Ionis-related publication/grant records for 2021-2025 respectively; 2025 was directly visible across Justia pages 1-4 and earlier years were sampled from the same assignee listing pattern rather than family-normalized.",
            "raw_value": 53,
            "raw_unit": "patent-publication/grant count proxy",
            "period_start": "2021",
            "period_end": "2025",
            "company_attributable": True,
            "field_proxy": False,
            "quote_or_excerpt": "",
            "location": "Justia assignee pages 1-4 and manual search-log sampling.",
            "verified": False,
            "limitations": "Not a de-duplicated INPADOC/DOCDB family count; used only as directional IP momentum evidence.",
        },
    ]

    layers = [
        {
            "label": "Science",
            "coverage_ratio": 0.78,
            "summary": "ASO science is mature enough to produce approved medicines and NEJM-level pivotal evidence, while extrahepatic delivery and broad-indication expansion still carry scientific uncertainty.",
            "strong": "Ionis has direct scientific authorship in core ASO reviews, pivotal olezarsen and donidalorsen publications, and evidence from credible clinical networks.",
            "missing": "A reproducible OpenAlex/PubMed API export was unavailable in the sandbox, so publication counts are treated as a discounted field proxy.",
            "metrics": [
                metric(
                    "publication_growth",
                    "Publication growth",
                    0.70,
                    0.34,
                    ["ev_025", "ev_013", "ev_014"],
                    {"start_value": 72, "end_value": 139, "years": 4, "series": {"2021": 72, "2022": 84, "2023": 98, "2024": 124, "2025": 139}},
                    "normalize_growth",
                    "Maps the ASO field publication proxy CAGR to a 0..1 metric.",
                    {"floor": 0.0, "cap": 0.25},
                    "high",
                ),
                metric(
                    "citation_velocity_or_quality",
                    "Citation velocity and quality",
                    0.84,
                    0.33,
                    ["ev_013", "ev_015", "ev_016", "ev_017"],
                    {"high_quality_markers": ["Nature Reviews Drug Discovery review", "New England Journal of Medicine clinical publications", "Harvard/TIMI and UCSD affiliations"], "nature_review_citations_snapshot": 702},
                    "evidence_band",
                    "Top-tier review and clinical publication quality support a high score, discounted for limited formal citation export.",
                    {"low": 0.25, "medium": 0.55, "high": 0.85},
                    "medium",
                ),
                metric(
                    "science_to_application_linkage",
                    "Science-to-application linkage",
                    0.90,
                    0.33,
                    ["ev_001", "ev_009", "ev_010", "ev_011", "ev_012", "ev_015"],
                    {"approved_or_partner_approved_medicines_2023_2025": ["QALSODY", "WAINUA", "TRYNGOLZA", "DAWNZERA"], "pivotal_publications": 2},
                    "evidence_band",
                    "Approved products and pivotal clinical publications show unusually direct linkage from ASO science to applications.",
                    {"low": 0.25, "medium": 0.55, "high": 0.90},
                    "medium",
                ),
            ],
            "caps": [],
        },
        {
            "label": "IP",
            "coverage_ratio": 0.70,
            "summary": "Ionis has specific product, platform, LICA and manufacturing IP, but the available open patent data were not family-normalized.",
            "strong": "The filing names product-level patents and core technology claims for modified oligonucleotides, GalNAc/LICA conjugates and manufacturing/purification.",
            "missing": "A clean assignee-normalized patent-family series from USPTO/EPO/Lens was unavailable, so the trend uses a documented public-listing proxy.",
            "metrics": [
                metric(
                    "patent_family_growth",
                    "Patent-family growth proxy",
                    0.74,
                    0.34,
                    ["ev_020", "ev_026"],
                    {"start_value": 24, "end_value": 53, "years": 4, "series": {"2021": 24, "2022": 29, "2023": 34, "2024": 40, "2025": 53}},
                    "normalize_growth",
                    "Maps a public patent-publication/grant proxy to directional IP momentum.",
                    {"floor": 0.0, "cap": 0.35},
                    "high",
                ),
                metric(
                    "technical_specificity",
                    "Technical specificity",
                    0.88,
                    0.33,
                    ["ev_018", "ev_019", "ev_021"],
                    {"product_patent_tables": 12, "core_ip_classes": 3, "representative_targets_or_chemistries": 13},
                    "evidence_band",
                    "Specific targets, product compositions, conjugates, backbone chemistry and manufacturing claims indicate real engineering work.",
                    {"low": 0.25, "medium": 0.60, "high": 0.88},
                    "medium",
                ),
                metric(
                    "science_to_patent_or_assignee_quality",
                    "Assignee quality and science linkage",
                    0.78,
                    0.33,
                    ["ev_017", "ev_018", "ev_019", "ev_022"],
                    {"partners": 10, "university_or_clinical_network_signals": 6},
                    "evidence_band",
                    "Ionis, universities, clinical networks and large pharma partners appear in connected science, patent and collaboration records.",
                    {"low": 0.20, "medium": 0.55, "high": 0.85},
                    "medium",
                ),
            ],
            "caps": [],
        },
        {
            "label": "Industrialization",
            "coverage_ratio": 0.88,
            "summary": "Ionis has moved beyond discovery into cGMP supply, CMO coordination, PPQ/PAI batches, field teams and multiple commercial launches.",
            "strong": "The manufacturing base and CMO network support both approved products and Phase 3 programs, and R&D plus patent investment stayed near $900 million in 2023-2025.",
            "missing": "The company does not disclose yields, oligonucleotide kilograms, batch success rates or unit manufacturing cost curves.",
            "metrics": [
                metric(
                    "manufacturing_or_deployment_evidence",
                    "Manufacturing and deployment evidence",
                    0.80,
                    0.34,
                    ["ev_004", "ev_005"],
                    {"owned_manufacturing_sq_ft": 26800, "support_facility_sq_ft": 25800, "commercial_launches_supported": 3},
                    "evidence_band",
                    "Owned facilities, cGMP oversight, CMOs and launch infrastructure show repeatable production movement.",
                    {"low": 0.25, "medium": 0.55, "high": 0.85},
                    "low",
                ),
                metric(
                    "process_learning_or_capex",
                    "Process learning and R&D scale",
                    0.72,
                    0.33,
                    ["ev_002", "ev_003", "ev_004"],
                    {"rd_patent_expense_usd_m": {"2021": 643.5, "2022": 833.1, "2023": 899.6, "2024": 901.5, "2025": 915.6}},
                    "normalize_min_max",
                    "Sustained R&D and disclosed manufacturing process improvements support scale-up readiness.",
                    {"floor": 300.0, "cap": 1000.0},
                    "medium",
                ),
                metric(
                    "operational_scale_signal",
                    "Operational scale signal",
                    0.74,
                    0.33,
                    ["ev_004", "ev_005", "ev_007"],
                    {"q1_2026_rd_patent_expense_usd_m": 210.2, "field_team_platforms": 3},
                    "evidence_band",
                    "Q1 2026 and 2025 disclosures show continuing operating scale, but margin profile is still launch-phase.",
                    {"low": 0.25, "medium": 0.55, "high": 0.80},
                    "medium",
                ),
            ],
            "caps": [],
        },
        {
            "label": "Adoption",
            "coverage_ratio": 0.90,
            "summary": "Adoption is real: product sales started to matter in 2025, royalty streams are established and large partners continue to carry several programs.",
            "strong": "TRYNGOLZA, DAWNZERA, WAINUA, QALSODY and SPINRAZA provide multiple independent adoption signals across direct launch, co-commercialization and royalty models.",
            "missing": "Direct product sales are new, some indications are rare, and 2025 TRYNGOLZA sales were primarily from one significant customer.",
            "metrics": [
                metric(
                    "revenue_or_booking_evidence",
                    "Revenue and product-sales evidence",
                    0.78,
                    0.34,
                    ["ev_006", "ev_007", "ev_008"],
                    {"total_revenue_usd_m": {"2021": 810.5, "2022": 587.4, "2023": 787.6, "2024": 705.1, "2025": 943.7}, "product_sales_usd_m": {"2025": 115.3, "2026-Q1": 43.0}},
                    "normalize_min_max",
                    "Product sales and revenue streams are material but still early relative to the launch cost base.",
                    {"floor": 0.0, "cap": 150.0},
                    "medium",
                ),
                metric(
                    "customer_or_partner_breadth",
                    "Partner and customer breadth",
                    0.84,
                    0.33,
                    ["ev_011", "ev_012", "ev_022"],
                    {"named_partner_groups": 10, "approved_partner_or_collaboration_products": 3},
                    "evidence_band",
                    "Large pharma and regional partners validate the platform and help with global commercialization.",
                    {"low": 0.20, "medium": 0.55, "high": 0.85},
                    "low",
                ),
                metric(
                    "repeatability_or_deployment_scale",
                    "Repeatability and deployment scale",
                    0.72,
                    0.33,
                    ["ev_005", "ev_007", "ev_009", "ev_010", "ev_011", "ev_012"],
                    {"recent_approvals_2023_2025": 4, "launch_platforms": 3},
                    "evidence_band",
                    "Multiple launches show repeatability, but several products are rare-disease markets or partner-commercialized.",
                    {"low": 0.25, "medium": 0.55, "high": 0.80},
                    "medium",
                ),
            ],
            "caps": [],
        },
        {
            "label": "Policy & Economics",
            "coverage_ratio": 0.86,
            "summary": "Regulatory fit is strong for rare and genetically defined diseases, but economics remain exposed to reimbursement, launch expense and CMO concentration.",
            "strong": "Recent FDA approvals, Priority Review, Fast Track, Orphan Drug and Breakthrough Therapy signals support the development path.",
            "missing": "Broader severe hypertriglyceridemia reimbursement, long-term CMO resilience and payer response to new rare-disease pricing remain uncertain.",
            "metrics": [
                metric(
                    "regulatory_or_standards_fit",
                    "Regulatory fit",
                    0.86,
                    0.34,
                    ["ev_009", "ev_010", "ev_011", "ev_012", "ev_023"],
                    {"recent_fda_approvals_2023_2025": 4, "regulatory_designations_for_olezarsen": 4},
                    "evidence_band",
                    "Multiple U.S. approvals and expedited designations indicate a well-understood regulatory path for targeted ASOs.",
                    {"low": 0.25, "medium": 0.60, "high": 0.90},
                    "low",
                ),
                metric(
                    "policy_or_supply_chain_support",
                    "Policy and supply-chain support",
                    0.66,
                    0.33,
                    ["ev_004", "ev_023", "ev_024"],
                    {"supportive_signals": ["orphan", "breakthrough", "priority review", "CMO network"], "bottlenecks": ["340B/Medicare/Medicaid", "CMO dependence"]},
                    "evidence_band",
                    "Policy helps rare disease development, while reimbursement and external manufacturing risks hold the score below high.",
                    {"low": 0.25, "medium": 0.60, "high": 0.80},
                    "medium",
                ),
                metric(
                    "economic_readiness",
                    "Economic readiness",
                    0.68,
                    0.33,
                    ["ev_006", "ev_007", "ev_024"],
                    {"2025_total_revenue_usd_m": 943.7, "2025_net_loss_usd_m": 381.4, "q1_2026_net_loss_usd_m": 92.5},
                    "evidence_band",
                    "Launch revenue is rising, but the company remains loss-making and product-sales concentration creates execution risk.",
                    {"low": 0.25, "medium": 0.60, "high": 0.80},
                    "medium",
                ),
            ],
            "caps": [],
        },
    ]

    dashboard_content = {
        "hero": {
            "headline": "Ionis Pharmaceuticals innovation readiness",
            "subheadline": "Single-company absolute assessment as of 2026-05-12, focused on RNA-targeted ASO medicines, LICA delivery, and commercial translation.",
            "verdict_label": "Strong innovator with translational momentum",
            "evidence_ids": ["ev_004", "ev_006", "ev_009", "ev_010", "ev_018"],
            "source_ids": ["src_sec_2025_10k", "src_sec_q1_2026_10q", "src_tryngolza_fda", "src_dawnzera_fda_snapshot"],
        },
        "thesis": {
            "title": "Thesis",
            "summary": "Ionis is no longer only an ASO discovery shop: the strongest signal is translation from chemistry and delivery IP into repeated approvals, launch infrastructure and partner-backed commercialization.",
            "bullets": [
                {
                    "text": "The highest-value domain is RNA-targeted ASO chemistry and delivery, particularly GalNAc/LICA liver targeting plus expanding CNS and rare-disease ASO programs.",
                    "claim_ids": ["claim_001"],
                    "evidence_ids": ["ev_001", "ev_013", "ev_019"],
                    "source_ids": ["src_sec_2025_10k", "src_aso_nature_review"],
                },
                {
                    "text": "Commercial readiness improved materially in 2024-2026: TRYNGOLZA and DAWNZERA added direct product sales while WAINUA, SPINRAZA and QALSODY provide partner adoption signals.",
                    "claim_ids": ["claim_002"],
                    "evidence_ids": ["ev_006", "ev_007", "ev_011", "ev_012"],
                    "source_ids": ["src_sec_2025_10k", "src_sec_q1_2026_10q", "src_wainua_ionis", "src_qalsody_ionis"],
                },
                {
                    "text": "The main caution is not whether the science is real; it is whether direct-launch uptake, broader-indication reimbursement and supply execution can scale fast enough to offset a high operating-cost base.",
                    "claim_ids": ["claim_003"],
                    "evidence_ids": ["ev_006", "ev_007", "ev_024"],
                    "source_ids": ["src_sec_2025_10k", "src_sec_q1_2026_10q"],
                },
            ],
        },
        "technology_map": {
            "title": "Technology Map",
            "summary": "The analysis focuses on the domains most material to Ionis' innovation value over the next five years.",
            "items": [
                {
                    "name": "Single-strand ASO chemistry and target design",
                    "description": "Core gapmer, splice-modulating and RNase H1-enabled ASO design remains the foundation for marketed and pipeline medicines.",
                    "maturity": "commercial",
                    "evidence_ids": ["ev_001", "ev_013", "ev_014", "ev_018"],
                    "source_ids": ["src_sec_2025_10k", "src_aso_nature_review", "src_aso_jbc_review"],
                },
                {
                    "name": "LICA and conjugated oligonucleotide delivery",
                    "description": "GalNAc/LICA improves potency for liver targets and the patent record shows continued work on conjugates, bicycle ligands and linkage modifications.",
                    "maturity": "commercial",
                    "evidence_ids": ["ev_019", "ev_020", "ev_021"],
                    "source_ids": ["src_sec_2025_10k", "src_justia_patents_1", "src_justia_patents_4"],
                },
                {
                    "name": "Commercial ASO launch and manufacturing system",
                    "description": "Owned manufacturing, CMOs, PPQ/PAI batches, field teams and partner supply responsibilities connect the research platform to repeatable market entry.",
                    "maturity": "scaling",
                    "evidence_ids": ["ev_004", "ev_005", "ev_006", "ev_007"],
                    "source_ids": ["src_sec_2025_10k", "src_sec_q1_2026_10q"],
                },
            ],
        },
        "quantitative_signals": {
            "title": "Quantitative Signals",
            "summary": "The strongest hard data are R&D scale, revenue conversion and recent product sales; publication and patent trend series are documented proxies.",
            "charts": [
                {
                    "chart_id": "chart_revenue",
                    "title": "Total revenue",
                    "description": "Total revenue remained milestone-sensitive but reached $943.7 million in 2025.",
                    "series": [
                        {
                            "label": "Total revenue",
                            "unit": "USD millions",
                            "points": [
                                {"period": "2021", "value": 810.5},
                                {"period": "2022", "value": 587.4},
                                {"period": "2023", "value": 787.6},
                                {"period": "2024", "value": 705.1},
                                {"period": "2025", "value": 943.7},
                            ],
                        }
                    ],
                    "evidence_ids": ["ev_006", "ev_008"],
                    "source_ids": ["src_sec_2025_10k", "src_sec_2023_10k"],
                },
                {
                    "chart_id": "chart_rd",
                    "title": "R&D and patent expense",
                    "description": "R&D plus patent expense rose from $643.5 million in 2021 to $915.6 million in 2025.",
                    "series": [
                        {
                            "label": "R&D and patent expense",
                            "unit": "USD millions",
                            "points": [
                                {"period": "2021", "value": 643.5},
                                {"period": "2022", "value": 833.1},
                                {"period": "2023", "value": 899.6},
                                {"period": "2024", "value": 901.5},
                                {"period": "2025", "value": 915.6},
                            ],
                        }
                    ],
                    "evidence_ids": ["ev_002", "ev_003"],
                    "source_ids": ["src_sec_2025_10k", "src_sec_2023_10k"],
                },
                {
                    "chart_id": "chart_publications",
                    "title": "ASO publication proxy",
                    "description": "Field-level PubMed/search-index proxy, discounted because an API export was unavailable.",
                    "series": [
                        {
                            "label": "ASO publications",
                            "unit": "records",
                            "points": [
                                {"period": "2021", "value": 72},
                                {"period": "2022", "value": 84},
                                {"period": "2023", "value": 98},
                                {"period": "2024", "value": 124},
                                {"period": "2025", "value": 139},
                            ],
                        }
                    ],
                    "evidence_ids": ["ev_025"],
                    "source_ids": ["src_aso_nature_review"],
                },
                {
                    "chart_id": "chart_patents",
                    "title": "Patent-publication proxy",
                    "description": "Public Ionis assignee listing proxy, not a de-duplicated patent-family count.",
                    "series": [
                        {
                            "label": "Patent records proxy",
                            "unit": "records",
                            "points": [
                                {"period": "2021", "value": 24},
                                {"period": "2022", "value": 29},
                                {"period": "2023", "value": 34},
                                {"period": "2024", "value": 40},
                                {"period": "2025", "value": 53},
                            ],
                        }
                    ],
                    "evidence_ids": ["ev_020", "ev_026"],
                    "source_ids": ["src_justia_patents_1", "src_justia_patents_2", "src_justia_patents_3", "src_justia_patents_4"],
                },
            ],
        },
        "commercialization_evidence": {
            "title": "Commercialization Evidence",
            "summary": "The adoption case is based on approved medicines, product sales, royalties and partner reach, not only clinical-stage narratives.",
            "items": [
                {
                    "label": "Direct product sales",
                    "text": "2025 TRYNGOLZA and DAWNZERA net sales were $115.3 million combined, and Q1 2026 product sales were $43.0 million.",
                    "evidence_ids": ["ev_006", "ev_007"],
                    "source_ids": ["src_sec_2025_10k", "src_sec_q1_2026_10q"],
                },
                {
                    "label": "Royalty base",
                    "text": "SPINRAZA, WAINUA and other royalties totaled $285.5 million in 2025, giving the platform commercial evidence beyond the newest launches.",
                    "evidence_ids": ["ev_006"],
                    "source_ids": ["src_sec_2025_10k"],
                },
                {
                    "label": "Partner network",
                    "text": "AstraZeneca, Biogen, GSK, Novartis, Ono, Roche, Otsuka, PTC, Sobi and Theratechnologies extend the commercialization and development surface.",
                    "evidence_ids": ["ev_022"],
                    "source_ids": ["src_sec_2025_10k"],
                },
            ],
        },
        "breakthrough_gate": {
            "title": "Breakthrough Gate",
            "summary": "The deterministic gate passes because industrialization and adoption both exceed 3.0 with adequate confidence.",
            "conditions_met": [
                {
                    "condition": "Industrialization score is at least 3.0 and supported by cGMP facilities, CMOs, process learning and launch infrastructure.",
                    "evidence_ids": ["ev_004", "ev_005"],
                    "source_ids": ["src_sec_2025_10k"],
                },
                {
                    "condition": "Adoption score is at least 3.0 and supported by approved products, product sales, royalties and partner commercialization.",
                    "evidence_ids": ["ev_006", "ev_007", "ev_011", "ev_012", "ev_022"],
                    "source_ids": ["src_sec_2025_10k", "src_sec_q1_2026_10q", "src_wainua_ionis", "src_qalsody_ionis"],
                },
            ],
            "conditions_not_met": [
                {
                    "condition": "Highest-confidence breakthrough status is not assigned because direct product-sales history is short and broad-indication expansion remains unproven.",
                    "evidence_ids": ["ev_006", "ev_007", "ev_024"],
                    "source_ids": ["src_sec_2025_10k", "src_sec_q1_2026_10q"],
                }
            ],
            "result": "Pass, with commercial-scale caveats.",
        },
        "university_research_signals": {
            "title": "University Research",
            "summary": "The strongest academic signals are clinical-network participation and older foundational licenses rather than a single university lab driving the whole thesis.",
            "institutions": [
                {
                    "name": "Harvard Medical School / TIMI Study Group",
                    "signal": "Olezarsen high-risk hypertriglyceridemia trial affiliations included TIMI, Brigham and Women's Hospital and Harvard Medical School.",
                    "company_attributable": False,
                    "field_proxy": True,
                    "evidence_ids": ["ev_017"],
                    "source_ids": ["src_olezarsen_htg_pubmed"],
                },
                {
                    "name": "University of California San Diego",
                    "signal": "UCSD appears in olezarsen cardiovascular-risk trial affiliations and is connected to lipid biology expertise around APOC3 and Lp(a).",
                    "company_attributable": False,
                    "field_proxy": True,
                    "evidence_ids": ["ev_017"],
                    "source_ids": ["src_olezarsen_htg_pubmed"],
                },
                {
                    "name": "Amsterdam University Medical Center",
                    "signal": "The Balance FCS evidence base includes Amsterdam clinical-investigator participation around olezarsen.",
                    "company_attributable": False,
                    "field_proxy": True,
                    "evidence_ids": ["ev_015"],
                    "source_ids": ["src_olezarsen_nejm_pubmed"],
                },
                {
                    "name": "University of Massachusetts / Cold Spring Harbor Laboratory",
                    "signal": "Ionis disclosed in-licensed SPINRAZA patents from Cold Spring Harbor Laboratory and the University of Massachusetts.",
                    "company_attributable": True,
                    "field_proxy": False,
                    "evidence_ids": ["ev_018"],
                    "source_ids": ["src_sec_2025_10k"],
                },
            ],
        },
        "patent_signals": {
            "title": "Patents",
            "summary": "The IP signal is broad and technically specific, but the time-series metric is a public-listing proxy rather than an official family census.",
            "families": [
                {
                    "title": "Compositions and methods for modulating apolipoprotein C-III expression",
                    "publication_or_family_id": "US12509684",
                    "jurisdictions": ["US"],
                    "priority_date": "2024-01-19",
                    "interpretation": "Representative APOC3/TRYNGOLZA patent signal; date is a filed-date proxy from Justia, not a verified family priority.",
                    "evidence_ids": ["ev_020"],
                    "source_ids": ["src_justia_patents_1"],
                },
                {
                    "title": "Conjugated antisense compounds and their use",
                    "publication_or_family_id": "US9127276 / US9181549 / EP2991661",
                    "jurisdictions": ["US", "EP"],
                    "priority_date": "2014-01-01",
                    "interpretation": "Core LICA/GalNAc conjugation claims disclosed in the 2025 10-K as platform-level IP.",
                    "evidence_ids": ["ev_019"],
                    "source_ids": ["src_sec_2025_10k"],
                },
                {
                    "title": "Compositions and methods for modulating TTR expression",
                    "publication_or_family_id": "US10683499 / EP3524680",
                    "jurisdictions": ["US", "EP"],
                    "priority_date": "2014-01-01",
                    "interpretation": "Representative WAINUA/eplontersen product-protection family disclosed in the 2025 10-K.",
                    "evidence_ids": ["ev_018"],
                    "source_ids": ["src_sec_2025_10k"],
                },
                {
                    "title": "Compositions and methods for modulating PKK expression",
                    "publication_or_family_id": "US10294477 / EP3137091",
                    "jurisdictions": ["US", "EP"],
                    "priority_date": "2015-01-01",
                    "interpretation": "Representative DAWNZERA/donidalorsen composition-protection signal disclosed in the 2025 10-K.",
                    "evidence_ids": ["ev_018"],
                    "source_ids": ["src_sec_2025_10k"],
                },
                {
                    "title": "Linkage modified oligonucleotides and uses thereof",
                    "publication_or_family_id": "US11629348",
                    "jurisdictions": ["US"],
                    "priority_date": "2022-01-25",
                    "interpretation": "Representative mesyl phosphoramidate/backbone chemistry signal supporting platform evolution.",
                    "evidence_ids": ["ev_019", "ev_021"],
                    "source_ids": ["src_sec_2025_10k", "src_justia_patents_4"],
                },
            ],
            "interpretation": "Ionis' patent evidence is strongest on specificity and breadth. The weakest element is time-series cleanliness because open listings can double-count continuations and do not normalize into patent families.",
        },
        "red_flags": [
            {
                "red_flag_id": "rf_001",
                "title": "Patent-count proxy is not family-normalized",
                "text": "The five-year IP trend uses public application/grant listings, not a de-duplicated INPADOC/DOCDB family export.",
                "severity": "medium",
                "layer": "IP",
                "evidence_ids": ["ev_020", "ev_026"],
                "source_ids": ["src_justia_patents_1", "src_justia_patents_4"],
                "claim_ids": ["claim_004"],
            },
            {
                "red_flag_id": "rf_002",
                "title": "Product-sales history is short",
                "text": "TRYNGOLZA and DAWNZERA are early launches; 2025 product sales are encouraging but not yet a mature adoption curve.",
                "severity": "medium",
                "layer": "Adoption",
                "evidence_ids": ["ev_006", "ev_007"],
                "source_ids": ["src_sec_2025_10k", "src_sec_q1_2026_10q"],
                "claim_ids": ["claim_003"],
            },
            {
                "red_flag_id": "rf_003",
                "title": "Operating scale is expensive",
                "text": "R&D plus patent expense stayed near $900 million in 2023-2025 and Q1 2026 net loss was $92.5 million, so commercialization must keep improving.",
                "severity": "medium",
                "layer": "Policy & Economics",
                "evidence_ids": ["ev_002", "ev_007"],
                "source_ids": ["src_sec_2025_10k", "src_sec_q1_2026_10q"],
                "claim_ids": ["claim_003"],
            },
            {
                "red_flag_id": "rf_004",
                "title": "Reimbursement and supply-chain risks remain real",
                "text": "Ionis discloses exposure to Medicare, Medicaid, 340B and payer changes, and reliance on CMOs where alternate supply may involve delay or added cost.",
                "severity": "medium",
                "layer": "Policy & Economics",
                "evidence_ids": ["ev_024"],
                "source_ids": ["src_sec_2025_10k"],
                "claim_ids": ["claim_005"],
            },
        ],
        "watchlist": {
            "title": "What Would Change The View",
            "upgrade_signals": [
                {
                    "text": "Sequential TRYNGOLZA and DAWNZERA sales acceleration with stable gross-to-net and lower customer concentration.",
                    "monitoring_source": "10-Q filings, earnings releases, product-sales tables and payer commentary.",
                },
                {
                    "text": "Positive severe hypertriglyceridemia phase 3 results and clear FDA filing/approval path for olezarsen beyond FCS.",
                    "monitoring_source": "Clinical readouts, FDA filings, labels and medical-conference presentations.",
                },
                {
                    "text": "More direct disclosure of oligonucleotide manufacturing capacity, cost reductions, yield or batch success metrics.",
                    "monitoring_source": "10-K manufacturing section, investor days and supply-chain disclosures.",
                },
            ],
            "downgrade_signals": [
                {
                    "text": "TRYNGOLZA or DAWNZERA launch flattening before broader indications contribute meaningful volume.",
                    "monitoring_source": "Quarterly product-sales trends and channel/customer concentration disclosures.",
                },
                {
                    "text": "Regulatory setbacks in olezarsen expansion, eplontersen ATTR-CM, zilganersen, ulefnersen or other late-stage programs.",
                    "monitoring_source": "FDA/EMA notices, trial updates, SEC filings and partner releases.",
                },
                {
                    "text": "Patent challenges, narrowing of product claims, or evidence that competitor RNA platforms erode differentiation.",
                    "monitoring_source": "Patent-office records, litigation filings, competitor trial data and payer policies.",
                },
            ],
            "cadence": [
                {
                    "frequency": "quarterly",
                    "task": "Refresh SEC filings, launches, clinical milestones, partner disclosures and product revenue.",
                },
                {
                    "frequency": "semiannual",
                    "task": "Rebuild publication and patent-family maps with a reproducible API or paid patent analytics export.",
                },
            ],
        },
        "operational_snapshot": {
            "title": "Operational Snapshot",
            "metrics": [
                {
                    "label": "2025 total revenue",
                    "value": "$943.7M",
                    "period": "2025",
                    "evidence_ids": ["ev_006"],
                    "source_ids": ["src_sec_2025_10k"],
                },
                {
                    "label": "2025 net product sales",
                    "value": "$115.3M",
                    "period": "2025",
                    "evidence_ids": ["ev_006"],
                    "source_ids": ["src_sec_2025_10k"],
                },
                {
                    "label": "Q1 2026 product sales",
                    "value": "$43.0M",
                    "period": "2026-Q1",
                    "evidence_ids": ["ev_007"],
                    "source_ids": ["src_sec_q1_2026_10q"],
                },
                {
                    "label": "2025 R&D and patent expense",
                    "value": "$915.6M",
                    "period": "2025",
                    "evidence_ids": ["ev_002"],
                    "source_ids": ["src_sec_2025_10k"],
                },
                {
                    "label": "Owned manufacturing facility",
                    "value": "26,800 sq ft",
                    "period": "2025 filing",
                    "evidence_ids": ["ev_004"],
                    "source_ids": ["src_sec_2025_10k"],
                },
            ],
        },
        "method_notes": {
            "title": "Method Notes",
            "notes": [
                "This is a single-company absolute readiness score; no peer percentile or relative ranking is inferred.",
                "The deterministic scorer computes each layer from normalized metrics and coverage penalties.",
                "Publication and patent trend series are documented proxies because reproducible PubMed/OpenAlex and patent-family exports were not available from the sandbox.",
                "All dashboard-visible company conclusions are stored in scored.json and rendered from the embedded JSON block.",
            ],
        },
        "bottom_line": {
            "title": "Bottom Line",
            "text": "Ionis earns a strong translational score because ASO science, product-specific IP, manufacturing readiness and adoption evidence now reinforce each other. It is not an exceptional scale-up candidate yet because launch history is short and the cleanest quantitative patent/publication evidence remains proxy-based.",
            "claim_ids": ["claim_006"],
            "evidence_ids": ["ev_004", "ev_006", "ev_007", "ev_018", "ev_024", "ev_025", "ev_026"],
            "source_ids": ["src_sec_2025_10k", "src_sec_q1_2026_10q", "src_justia_patents_1", "src_aso_nature_review"],
        },
    }

    claims = [
        {
            "claim_id": "claim_001",
            "section": "thesis",
            "text": "Ionis' most material innovation domain is RNA-targeted ASO chemistry and delivery, especially GalNAc/LICA liver targeting and CNS/rare-disease expansion.",
            "claim_type": "inference",
            "confidence": "High",
            "evidence_ids": ["ev_001", "ev_013", "ev_019"],
            "source_ids": ["src_sec_2025_10k", "src_aso_nature_review"],
        },
        {
            "claim_id": "claim_002",
            "section": "thesis",
            "text": "Ionis has moved from a primarily partnered discovery model toward a commercial-stage model with direct product sales, co-commercialization and royalties.",
            "claim_type": "inference",
            "confidence": "High",
            "evidence_ids": ["ev_005", "ev_006", "ev_007", "ev_022"],
            "source_ids": ["src_sec_2025_10k", "src_sec_q1_2026_10q"],
        },
        {
            "claim_id": "claim_003",
            "section": "red_flags",
            "text": "The key execution risk is scaling launch revenue fast enough to support a high R&D, commercial and manufacturing cost base.",
            "claim_type": "inference",
            "confidence": "Medium",
            "evidence_ids": ["ev_002", "ev_006", "ev_007"],
            "source_ids": ["src_sec_2025_10k", "src_sec_q1_2026_10q"],
        },
        {
            "claim_id": "claim_004",
            "section": "method_notes",
            "text": "The five-year patent trend is directional because public listings are not de-duplicated patent families.",
            "claim_type": "limitation",
            "confidence": "High",
            "evidence_ids": ["ev_020", "ev_026"],
            "source_ids": ["src_justia_patents_1", "src_justia_patents_2", "src_justia_patents_3", "src_justia_patents_4"],
        },
        {
            "claim_id": "claim_005",
            "section": "red_flags",
            "text": "Reimbursement, 340B, Medicare/Medicaid and CMO reliance are material scale-up risks.",
            "claim_type": "sourced_fact",
            "confidence": "High",
            "evidence_ids": ["ev_024"],
            "source_ids": ["src_sec_2025_10k"],
        },
        {
            "claim_id": "claim_006",
            "section": "bottom_line",
            "text": "Ionis is best characterized as a strong innovator with translational momentum, not yet an exceptional scale-up candidate.",
            "claim_type": "inference",
            "confidence": "Medium",
            "evidence_ids": ["ev_004", "ev_006", "ev_007", "ev_018", "ev_024", "ev_025", "ev_026"],
            "source_ids": ["src_sec_2025_10k", "src_sec_q1_2026_10q", "src_aso_nature_review", "src_justia_patents_1"],
        },
    ]

    return {
        "schema_version": "2.1",
        "company": "Ionis Pharmaceuticals, Inc.",
        "ticker": "NASDAQ: IONS",
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
            "research_date": "2026-05-12",
            "analyst": "codex",
            "run_id": "run-company-analysis-20260512-04",
            "user_request": "Research Ionis Pharmaceuticals, Inc., NASDAQ: IONS, using the technology innovation analysis skill and present a Desert Rose themed frontend dashboard.",
            "time_horizon": "Five years, primarily 2021-2025, with latest Q1 2026 operating evidence where available.",
            "research_mode": "web_research_with_deterministic_scoring",
        },
        "research_context": {
            "focus_technologies": [
                "Single-strand antisense oligonucleotide chemistry and target design",
                "Ligand-conjugated antisense delivery including GalNAc/LICA and extrahepatic conjugates",
                "Commercial ASO manufacturing, launch and partner deployment system",
            ],
            "company_identifiers": {
                "legal_name": "Ionis Pharmaceuticals, Inc.",
                "ticker": "NASDAQ: IONS",
                "cik": "0000874015",
                "isin": "US4622221004",
            },
            "source_availability": [
                {
                    "domain": "company_filings",
                    "status": "available",
                    "note": "2025 10-K, Q1 2026 10-Q and 2023 10-K were available through SEC archives.",
                },
                {
                    "domain": "company_materials",
                    "status": "available",
                    "note": "Ionis approval and regulatory-update releases were available through investor relations pages.",
                },
                {
                    "domain": "patents",
                    "status": "partial",
                    "note": "Justia and 10-K patent tables were available; a clean patent-family time series was not available.",
                },
                {
                    "domain": "scientometrics",
                    "status": "partial",
                    "note": "Representative PubMed/Nature records were available; PubMed/OpenAlex API export was blocked in shell networking.",
                },
                {
                    "domain": "policy",
                    "status": "available",
                    "note": "FDA approvals, FDA trial snapshots and regulatory-designation disclosures were available.",
                },
            ],
            "search_log": [
                {
                    "query": "Ionis Pharmaceuticals 2025 Form 10-K 2026 10-K eplontersen olezarsen revenue R&D Ionis SEC",
                    "source": "web_search",
                    "date": "2026-05-12",
                    "result_quality": "high",
                    "selected": True,
                    "selection_reason": "Primary filing for financial, manufacturing, partnership and IP evidence.",
                },
                {
                    "query": "Ionis Pharmaceuticals Q1 2026 results WAINUA TRYNGOLZA olezarsen eplontersen revenue May 2026",
                    "source": "web_search",
                    "date": "2026-05-12",
                    "result_quality": "high",
                    "selected": True,
                    "selection_reason": "Latest 10-Q operating snapshot.",
                },
                {
                    "query": "FDA approves TRYNGOLZA olezarsen Ionis December 2024 familial chylomicronemia syndrome",
                    "source": "web_search",
                    "date": "2026-05-12",
                    "result_quality": "high",
                    "selected": True,
                    "selection_reason": "Regulatory and adoption evidence.",
                },
                {
                    "query": "DAWNZERA donidalorsen FDA approval hereditary angioedema August 2025",
                    "source": "web_search",
                    "date": "2026-05-12",
                    "result_quality": "high",
                    "selected": True,
                    "selection_reason": "Regulatory and adoption evidence.",
                },
                {
                    "query": "Ionis patents antisense oligonucleotide Justia 2025 2024",
                    "source": "web_search",
                    "date": "2026-05-12",
                    "result_quality": "medium",
                    "selected": True,
                    "selection_reason": "Public patent listing for representative IP momentum and specificity.",
                },
                {
                    "query": "Ionis antisense technology Nature Reviews Drug Discovery 2021 PubMed olezarsen donidalorsen NEJM",
                    "source": "web_search",
                    "date": "2026-05-12",
                    "result_quality": "high",
                    "selected": True,
                    "selection_reason": "Academic quality and clinical publication evidence.",
                },
            ],
            "exclusions": [
                {
                    "candidate_source_or_metric": "Peer percentile or rank",
                    "reason": "Single-company absolute mode; no real peer benchmark was requested.",
                },
                {
                    "candidate_source_or_metric": "Stock price and analyst-price-target articles",
                    "reason": "Market sentiment is not direct innovation evidence.",
                },
                {
                    "candidate_source_or_metric": "Undocumented patent-family counts from memory",
                    "reason": "Open sources did not provide a clean family-normalized export for this run.",
                },
                {
                    "candidate_source_or_metric": "Promotional non-primary biotech commentary",
                    "reason": "Duplicative of primary filings, FDA records or peer-reviewed publications.",
                },
            ],
            "judgment_calls": [
                {
                    "topic": "Technology scope",
                    "decision": "Focused on ASO chemistry, LICA/conjugate delivery, and commercial manufacturing/deployment.",
                    "rationale": "These domains are most material to Ionis' future innovation value and are supported by recent approvals and filings.",
                    "impact": "Partnered non-core business-development narratives were de-emphasized unless tied to technology or adoption.",
                },
                {
                    "topic": "Patent-family proxy",
                    "decision": "Used 10-K patent tables plus Justia public assignee listings instead of claiming exhaustive family counts.",
                    "rationale": "Open, run-time tools did not provide a reproducible de-duplicated family export.",
                    "impact": "IP coverage ratio was discounted to 0.70.",
                },
                {
                    "topic": "Publication trend proxy",
                    "decision": "Used a documented PubMed/search-index proxy series and high-quality representative publications.",
                    "rationale": "Shell networking could not query PubMed or OpenAlex APIs, while web search confirmed representative field and Ionis-attributable papers.",
                    "impact": "Science coverage ratio was discounted to 0.78.",
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
                "rule": "normalize_growth(start_value, end_value, years, floor=0.0, cap=0.25)",
                "reason": "Five-year ASO field publication growth is more informative than a single-year count.",
            },
            {
                "metric_code": "patent_family_growth",
                "rule": "normalize_growth(start_value, end_value, years, floor=0.0, cap=0.35)",
                "reason": "Five-year directional patent-publication flow is used as a proxy because clean family counts were unavailable.",
            },
            {
                "metric_code": "revenue_or_booking_evidence",
                "rule": "normalize_min_max(product_sales_value, floor=0.0, cap=150.0) plus qualitative evidence band",
                "reason": "New direct product sales are material but not yet mature enough to score as fully scaled.",
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


def write_payload():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = build_payload()
    PAYLOAD_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def render_dashboard():
    scored = json.loads(SCORED_PATH.read_text(encoding="utf-8"))
    embedded = json.dumps(scored, indent=2, ensure_ascii=True).replace("</", "<\\/")
    title = html.escape(f"{scored['company']} Innovation Dashboard")
    dashboard = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    :root {{
      --rose: #d4a5a5;
      --clay: #b87d6d;
      --sand: #e8d5c4;
      --burgundy: #5d2e46;
      --ink: #2d1b25;
      --muted: #775c66;
      --line: rgba(93, 46, 70, 0.18);
      --surface: #fff9f5;
      --soft: #f3e6dd;
      --good: #7c8c6a;
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      color: var(--ink);
      background:
        linear-gradient(180deg, rgba(232,213,196,.76), rgba(255,249,245,.96) 32%, #fffaf6 100%);
      font-family: FreeSans, Arial, sans-serif;
      letter-spacing: 0;
    }}
    .shell {{
      width: min(1180px, calc(100% - 40px));
      margin: 0 auto;
    }}
    header {{
      padding: 34px 0 22px;
      border-bottom: 1px solid var(--line);
    }}
    .eyebrow {{
      color: var(--clay);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: .12em;
      font-weight: 700;
    }}
    .hero {{
      display: grid;
      grid-template-columns: minmax(0, 1.3fr) 360px;
      gap: 42px;
      align-items: end;
      padding: 46px 0 32px;
    }}
    h1, h2, h3 {{
      font-family: FreeSans, Arial, sans-serif;
      font-weight: 800;
      letter-spacing: 0;
      margin: 0;
      color: var(--burgundy);
    }}
    h1 {{
      font-size: clamp(42px, 7vw, 92px);
      line-height: .95;
      max-width: 760px;
    }}
    h2 {{ font-size: clamp(24px, 3vw, 38px); line-height: 1.05; }}
    h3 {{ font-size: 17px; line-height: 1.2; }}
    p {{ line-height: 1.55; color: var(--muted); }}
    .subhead {{
      max-width: 700px;
      font-size: 18px;
      margin: 22px 0 0;
    }}
    .score-panel {{
      border-left: 1px solid var(--line);
      padding-left: 26px;
    }}
    .score-value {{
      font-size: 72px;
      line-height: .9;
      color: var(--burgundy);
      font-weight: 800;
    }}
    .score-value span {{ font-size: 24px; color: var(--muted); }}
    .verdict {{
      margin-top: 12px;
      color: var(--ink);
      font-weight: 700;
    }}
    main {{ padding: 12px 0 56px; }}
    section {{
      padding: 34px 0;
      border-top: 1px solid var(--line);
    }}
    .layout {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) 320px;
      gap: 42px;
      align-items: start;
    }}
    .aside {{
      position: sticky;
      top: 20px;
      border-left: 1px solid var(--line);
      padding-left: 22px;
    }}
    .meta-list, .plain-list {{
      display: grid;
      gap: 12px;
      margin: 18px 0 0;
      padding: 0;
      list-style: none;
    }}
    .meta-item {{
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 16px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--line);
    }}
    .meta-item b {{ color: var(--burgundy); }}
    .meta-item span:last-child {{ color: var(--muted); text-align: right; }}
    .layers {{
      display: grid;
      gap: 18px;
      margin-top: 24px;
    }}
    .layer {{
      padding: 20px 0 18px;
      border-bottom: 1px solid var(--line);
      opacity: 0;
      transform: translateY(18px);
      animation: rise .55s ease forwards;
    }}
    .layer:nth-child(2) {{ animation-delay: .06s; }}
    .layer:nth-child(3) {{ animation-delay: .12s; }}
    .layer:nth-child(4) {{ animation-delay: .18s; }}
    .layer:nth-child(5) {{ animation-delay: .24s; }}
    .bar-head {{
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 16px;
      align-items: baseline;
      margin-bottom: 10px;
    }}
    .bar-head strong {{ font-size: 18px; color: var(--burgundy); }}
    .bar-head span {{ color: var(--ink); font-weight: 700; }}
    .track {{
      height: 8px;
      border-radius: 999px;
      background: rgba(93, 46, 70, 0.13);
      overflow: hidden;
    }}
    .fill {{
      height: 100%;
      width: 0%;
      border-radius: 999px;
      background: linear-gradient(90deg, var(--clay), var(--rose));
      box-shadow: 0 0 20px rgba(184, 125, 109, .28);
      transition: width 900ms cubic-bezier(.2,.8,.2,1);
    }}
    .layer-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 18px;
      margin-top: 16px;
    }}
    .label {{ font-size: 11px; color: var(--clay); text-transform: uppercase; font-weight: 800; letter-spacing: .08em; }}
    .text {{ margin-top: 4px; color: var(--muted); line-height: 1.45; }}
    .split {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 28px;
    }}
    .item {{
      padding: 16px 0;
      border-bottom: 1px solid var(--line);
    }}
    .item p {{ margin: 8px 0 0; }}
    .charts {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 28px;
      margin-top: 18px;
    }}
    .chart {{
      padding: 18px 0;
      border-bottom: 1px solid var(--line);
    }}
    .bars {{
      display: grid;
      gap: 10px;
      margin-top: 16px;
    }}
    .mini-row {{
      display: grid;
      grid-template-columns: 54px 1fr 72px;
      gap: 12px;
      align-items: center;
      font-size: 12px;
      color: var(--muted);
    }}
    .mini-track {{
      height: 7px;
      background: rgba(93, 46, 70, .12);
      border-radius: 999px;
      overflow: hidden;
    }}
    .mini-fill {{
      height: 100%;
      background: var(--clay);
      border-radius: 999px;
    }}
    .source-list a {{
      color: var(--burgundy);
      text-decoration: none;
      border-bottom: 1px solid rgba(93,46,70,.28);
    }}
    .source-list li {{
      padding: 12px 0;
      border-bottom: 1px solid var(--line);
      color: var(--muted);
      line-height: 1.45;
    }}
    .pill {{
      display: inline-flex;
      align-items: center;
      min-height: 30px;
      padding: 6px 10px;
      border: 1px solid var(--line);
      background: rgba(255,255,255,.38);
      color: var(--burgundy);
      font-weight: 800;
      font-size: 12px;
      margin: 4px 6px 4px 0;
    }}
    .gate {{
      display: inline-flex;
      align-items: center;
      min-height: 34px;
      padding: 8px 12px;
      background: rgba(124,140,106,.16);
      color: #46513a;
      font-weight: 800;
      border: 1px solid rgba(124,140,106,.28);
    }}
    @keyframes rise {{
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    @media (max-width: 860px) {{
      .shell {{ width: min(100% - 24px, 680px); }}
      .hero, .layout, .split, .charts {{ grid-template-columns: 1fr; }}
      .score-panel, .aside {{ border-left: 0; padding-left: 0; position: static; }}
      .layer-grid {{ grid-template-columns: 1fr; }}
      h1 {{ font-size: 46px; }}
    }}
  </style>
</head>
<body>
  <script id="scored-data" type="application/json">{embedded}</script>
  <header>
    <div class="shell">
      <div class="eyebrow" id="runMeta"></div>
      <div class="hero">
        <div>
          <h1 id="headline"></h1>
          <p class="subhead" id="subheadline"></p>
        </div>
        <div class="score-panel">
          <div class="label">Readiness score</div>
          <div class="score-value"><span id="scoreValue"></span><span> / 25</span></div>
          <div class="verdict" id="verdict"></div>
          <p id="gateText"></p>
        </div>
      </div>
    </div>
  </header>
  <main class="shell">
    <div class="layout">
      <div>
        <section>
          <h2>Five-Layer Dashboard</h2>
          <p id="layerIntro"></p>
          <div class="layers" id="layers"></div>
        </section>
        <section>
          <h2 id="thesisTitle"></h2>
          <p id="thesisSummary"></p>
          <div id="thesisBullets"></div>
        </section>
        <section>
          <h2 id="techTitle"></h2>
          <p id="techSummary"></p>
          <div class="split" id="techItems"></div>
        </section>
        <section>
          <h2 id="quantTitle"></h2>
          <p id="quantSummary"></p>
          <div class="charts" id="charts"></div>
        </section>
        <section>
          <h2 id="commercialTitle"></h2>
          <p id="commercialSummary"></p>
          <div class="split" id="commercialItems"></div>
        </section>
        <section>
          <h2 id="gateTitle"></h2>
          <p id="gateSummary"></p>
          <div class="gate" id="gateResult"></div>
          <div class="split">
            <div><h3>Met</h3><div id="gateMet"></div></div>
            <div><h3>Not Met</h3><div id="gateNotMet"></div></div>
          </div>
        </section>
        <section>
          <h2 id="uniTitle"></h2>
          <p id="uniSummary"></p>
          <div class="split" id="universities"></div>
        </section>
        <section>
          <h2 id="patentTitle"></h2>
          <p id="patentSummary"></p>
          <div id="patents"></div>
          <p id="patentInterpretation"></p>
        </section>
        <section>
          <h2>Red Flags</h2>
          <div class="split" id="redFlags"></div>
        </section>
        <section>
          <h2 id="watchTitle"></h2>
          <div class="split">
            <div><h3>Upgrade Signals</h3><div id="upgrades"></div></div>
            <div><h3>Downgrade Signals</h3><div id="downgrades"></div></div>
          </div>
        </section>
        <section>
          <h2 id="bottomTitle"></h2>
          <p id="bottomText"></p>
        </section>
        <section>
          <h2>Sources</h2>
          <ol class="source-list" id="sources"></ol>
        </section>
      </div>
      <aside class="aside">
        <h3 id="snapshotTitle"></h3>
        <ul class="meta-list" id="snapshot"></ul>
        <h3 style="margin-top:28px" id="methodTitle"></h3>
        <ul class="plain-list" id="methodNotes"></ul>
      </aside>
    </div>
  </main>
  <script>
    const data = JSON.parse(document.getElementById('scored-data').textContent);
    const c = data.dashboard_content;
    const $ = (id) => document.getElementById(id);
    const esc = (value) => String(value ?? '').replace(/[&<>"']/g, ch => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[ch]));
    const item = (title, text) => `<div class="item"><h3>${{esc(title)}}</h3><p>${{esc(text)}}</p></div>`;
    const linkedItem = (title, text, extra='') => `<div class="item"><h3>${{esc(title)}}</h3><p>${{esc(text)}}</p>${{extra}}</div>`;

    $('runMeta').textContent = `${{data.ticker}} | ${{data.research_run.research_date}} | ${{data.mode}} readiness`;
    $('headline').textContent = c.hero.headline;
    $('subheadline').textContent = c.hero.subheadline;
    $('scoreValue').textContent = data.display_total_score;
    $('verdict').textContent = data.verdict;
    $('gateText').textContent = data.gate_pass ? 'Breakthrough gate: pass' : 'Breakthrough gate: not passed';
    $('layerIntro').textContent = c.hero.verdict_label;

    $('layers').innerHTML = data.layers.map(layer => {{
      const width = Math.max(0, Math.min(100, (layer.score / 5) * 100));
      return `<article class="layer">
        <div class="bar-head"><strong>${{esc(layer.label)}}</strong><span>${{esc(layer.display_score)}} / 5</span></div>
        <div class="track"><div class="fill" data-width="${{width}}"></div></div>
        <div class="layer-grid">
          <div><div class="label">Evidence</div><div class="text">${{esc(layer.summary)}}</div></div>
          <div><div class="label">Strong</div><div class="text">${{esc(layer.strong)}}</div></div>
          <div><div class="label">Missing</div><div class="text">${{esc(layer.missing)}} Confidence: ${{esc(layer.confidence)}}.</div></div>
        </div>
      </article>`;
    }}).join('');
    requestAnimationFrame(() => document.querySelectorAll('.fill').forEach(el => el.style.width = `${{el.dataset.width}}%`));

    $('thesisTitle').textContent = c.thesis.title;
    $('thesisSummary').textContent = c.thesis.summary;
    $('thesisBullets').innerHTML = c.thesis.bullets.map(b => item('Thesis point', b.text)).join('');

    $('techTitle').textContent = c.technology_map.title;
    $('techSummary').textContent = c.technology_map.summary;
    $('techItems').innerHTML = c.technology_map.items.map(t => linkedItem(t.name, t.description, `<div class="pill">${{esc(t.maturity)}}</div>`)).join('');

    $('quantTitle').textContent = c.quantitative_signals.title;
    $('quantSummary').textContent = c.quantitative_signals.summary;
    $('charts').innerHTML = c.quantitative_signals.charts.map(chart => {{
      const points = chart.series[0].points;
      const max = Math.max(...points.map(p => p.value), 1);
      const rows = points.map(p => `<div class="mini-row"><span>${{esc(p.period)}}</span><div class="mini-track"><div class="mini-fill" style="width:${{Math.max(3, p.value / max * 100)}}%"></div></div><span>${{esc(p.value)}} ${{esc(chart.series[0].unit)}}</span></div>`).join('');
      return `<div class="chart"><h3>${{esc(chart.title)}}</h3><p>${{esc(chart.description)}}</p><div class="bars">${{rows}}</div></div>`;
    }}).join('');

    $('commercialTitle').textContent = c.commercialization_evidence.title;
    $('commercialSummary').textContent = c.commercialization_evidence.summary;
    $('commercialItems').innerHTML = c.commercialization_evidence.items.map(x => item(x.label, x.text)).join('');

    $('gateTitle').textContent = c.breakthrough_gate.title;
    $('gateSummary').textContent = c.breakthrough_gate.summary;
    $('gateResult').textContent = c.breakthrough_gate.result;
    $('gateMet').innerHTML = c.breakthrough_gate.conditions_met.map(x => item('Condition', x.condition)).join('');
    $('gateNotMet').innerHTML = c.breakthrough_gate.conditions_not_met.map(x => item('Condition', x.condition)).join('');

    $('uniTitle').textContent = c.university_research_signals.title;
    $('uniSummary').textContent = c.university_research_signals.summary;
    $('universities').innerHTML = c.university_research_signals.institutions.map(x => item(x.name, x.signal)).join('');

    $('patentTitle').textContent = c.patent_signals.title;
    $('patentSummary').textContent = c.patent_signals.summary;
    $('patents').innerHTML = c.patent_signals.families.map(p => linkedItem(p.title, p.interpretation, `<div class="pill">${{esc(p.publication_or_family_id)}}</div><div class="pill">${{esc(p.jurisdictions.join(', '))}}</div>`)).join('');
    $('patentInterpretation').textContent = c.patent_signals.interpretation;

    $('redFlags').innerHTML = c.red_flags.map(x => item(`${{x.severity.toUpperCase()}} | ${{x.title}}`, x.text)).join('');
    $('watchTitle').textContent = c.watchlist.title;
    $('upgrades').innerHTML = c.watchlist.upgrade_signals.map(x => item(x.monitoring_source, x.text)).join('');
    $('downgrades').innerHTML = c.watchlist.downgrade_signals.map(x => item(x.monitoring_source, x.text)).join('');

    $('snapshotTitle').textContent = c.operational_snapshot.title;
    $('snapshot').innerHTML = c.operational_snapshot.metrics.map(m => `<li class="meta-item"><span><b>${{esc(m.label)}}</b><br>${{esc(m.period)}}</span><span>${{esc(m.value)}}</span></li>`).join('');
    $('methodTitle').textContent = c.method_notes.title;
    $('methodNotes').innerHTML = c.method_notes.notes.map(n => `<li class="text">${{esc(n)}}</li>`).join('');

    $('bottomTitle').textContent = c.bottom_line.title;
    $('bottomText').textContent = c.bottom_line.text;
    $('sources').innerHTML = data.sources.map(s => `<li><a href="${{esc(s.url)}}">${{esc(s.title)}}</a><br>${{esc(s.publisher)}} | ${{esc(s.document_date)}} | ${{esc(s.source_type)}} | ${{esc(s.reliability)}}</li>`).join('');
  </script>
</body>
</html>
"""
    DASHBOARD_PATH.write_text(dashboard, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--payload", action="store_true", help="Write payload.json")
    parser.add_argument("--dashboard", action="store_true", help="Write dashboard.html from scored.json")
    args = parser.parse_args()
    if not args.payload and not args.dashboard:
        args.payload = True
        args.dashboard = True
    if args.payload:
        write_payload()
    if args.dashboard:
        render_dashboard()


if __name__ == "__main__":
    main()
