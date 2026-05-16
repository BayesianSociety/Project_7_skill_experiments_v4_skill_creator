from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


OUT_DIR = Path("public/runs/incyte-inc/2026-05-12/run-company-analysis-20260512-03")


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
        "accessed_at": "2026-05-12",
        "source_type": source_type,
        "availability": "available",
        "reliability": reliability,
        "notes": notes,
    }


def evidence(
    evidence_id,
    source_id,
    layer,
    metric_codes,
    fact,
    raw_value=None,
    raw_unit=None,
    period_start=None,
    period_end=None,
    company_attributable=True,
    field_proxy=False,
    location="",
    limitations="",
):
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
        "location": location,
        "verified": True,
        "limitations": limitations,
    }


def build_payload():
    sources = [
        source(
            "src_sec_2025_10k",
            "Incyte Corporation Form 10-K for fiscal year ended December 31, 2025",
            "https://www.sec.gov/Archives/edgar/data/879169/000087916926000010/incy-20251231.htm",
            "U.S. Securities and Exchange Commission / Incyte Corporation",
            "2026-02-10",
            "primary_filing",
            "Primary annual filing for revenue, product portfolio, pipeline status, intellectual property and operating risks.",
        ),
        source(
            "src_q1_2026_release",
            "Incyte Reports First Quarter 2026 Financial Results and Provides Business Updates",
            "https://investor.incyte.com/news-releases/news-release-details/incyte-reports-first-quarter-2026-financial-results-and-provides",
            "Incyte Investor Relations",
            "2026-04-28",
            "primary_company_release",
            "Latest company operating update before the research date.",
        ),
        source(
            "src_q1_2026_presentation",
            "Incyte Q1 2026 Financial and Corporate Update Presentation",
            "https://www.marketscreener.com/news/incyte-q1-2026-financial-and-corporate-update-presentation-ce7f59d2db8af721",
            "Incyte / MarketScreener mirror",
            "2026-04-28",
            "primary_company_presentation",
            "Company presentation mirror used for pipeline program labels and 2026 newsflow context.",
            reliability="medium",
        ),
        source(
            "src_pov_hs_2025_eadv",
            "Incyte Announces 24-Week Phase 3 STOP-HS Data for Povorcitinib",
            "https://incytecorp.gcs-web.com/news-releases/news-release-details/incyte-announces-new-24-week-phase-3-data-stop-hs-clinical-trial",
            "Incyte Investor Relations",
            "2025-09-17",
            "primary_company_release",
            "Source for Phase 3 STOP-HS 24-week data and planned regulatory submissions.",
        ),
        source(
            "src_pov_hs_2026_aad",
            "Incyte Announces Positive 54-Week Data for Povorcitinib in Hidradenitis Suppurativa",
            "https://www.nasdaq.com/press-release/incyte-announces-new-positive-54-week-late-breaking-data-povorcitinib-hidradenitis",
            "Incyte via Nasdaq / Business Wire",
            "2026-03-28",
            "primary_company_release",
            "Source for 54-week STOP-HS efficacy and safety data.",
            reliability="medium",
        ),
        source(
            "src_mutcalr_eha2025",
            "Positive Late-Breaking Data for Incyte's First-in-Class mutCALR-targeted Therapy INCA033989",
            "https://investor.incyte.com/news-releases/news-release-details/positive-late-breaking-data-incytes-first-class-mutcalr-targeted",
            "Incyte Investor Relations",
            "2025-06-15",
            "primary_company_release",
            "Source for ET Phase 1 hematologic response, VAF reduction and safety data.",
        ),
        source(
            "src_mutcalr_ash2025",
            "Incyte Announces New Positive Data for INCA033989 in Myelofibrosis at ASH 2025",
            "https://investor.incyte.com/news-releases/news-release-details/incyte-announces-new-positive-data-inca033989-its-first-class",
            "Incyte Investor Relations",
            "2025-12-07",
            "primary_company_release",
            "Source for MF Phase 1 spleen, symptom, anemia and VAF signals, plus 2026 registrational intent.",
        ),
        source(
            "src_mutcalr_ash2022",
            "Incyte's Novel Mutant CALR Antibody Unveiled at ASH 2022 Plenary Scientific Session",
            "https://investor.incyte.com/news-releases/news-release-details/incytes-novel-mutant-calr-antibody-unveiled-ash-2022-plenary",
            "Incyte Investor Relations",
            "2022-12-11",
            "primary_company_release",
            "Source for the preclinical discovery milestone and planned 2023 clinical start.",
        ),
        source(
            "src_opzelura_fda",
            "FDA Approves Topical Treatment Addressing Repigmentation in Vitiligo",
            "https://www.fda.gov/drugs/news-events-human-drugs/fda-approves-topical-treatment-addressing-repigmentation-vitiligo-patients-aged-12-and-older",
            "U.S. Food and Drug Administration",
            "2022-07-18",
            "regulator",
            "Regulatory source for Opzelura vitiligo approval and clinical effect summary.",
        ),
        source(
            "src_opzelura_ema",
            "Opzelura EPAR Overview",
            "https://www.ema.europa.eu/en/medicines/human/EPAR/opzelura",
            "European Medicines Agency",
            "2026-03-23",
            "regulator",
            "Regulatory source for EU authorization, indication and pivotal vitiligo study summary.",
        ),
        source(
            "src_fda_cgvhd",
            "FDA Approves Ruxolitinib for Chronic Graft-versus-Host Disease",
            "https://www.fda.gov/drugs/resources-information-approved-drugs/fda-approves-ruxolitinib-chronic-graft-versus-host-disease",
            "U.S. Food and Drug Administration",
            "2021-09-22",
            "regulator",
            "Regulatory source for ruxolitinib cGVHD approval and response-rate evidence.",
        ),
        source(
            "src_pubmed_rux_ad_phase3",
            "Efficacy and Safety of Ruxolitinib Cream for Atopic Dermatitis: Two Phase 3 Studies",
            "https://pubmed.ncbi.nlm.nih.gov/33957195/",
            "Journal of the American Academy of Dermatology / PubMed",
            "2021-10",
            "academic_clinical_trial",
            "Peer-reviewed Phase 3 ruxolitinib cream study record.",
        ),
        source(
            "src_pubmed_pov_vitiligo",
            "Efficacy and Safety of Povorcitinib in Extensive Vitiligo Phase 2 Study",
            "https://pubmed.ncbi.nlm.nih.gov/40518122/",
            "Journal of the American Academy of Dermatology / PubMed",
            "2025-10",
            "academic_clinical_trial",
            "Peer-reviewed povorcitinib vitiligo clinical study record, with Incyte Research Institute authors.",
        ),
        source(
            "src_pubmed_hs_jak_review",
            "Hidradenitis Suppurativa and JAK Inhibitors: A Review of the Published Literature",
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC10146646/",
            "Medicina / PubMed Central",
            "2023-04-20",
            "academic_review",
            "Field review of JAK inhibitors in hidradenitis suppurativa.",
        ),
        source(
            "src_pubmed_hs_rockefeller",
            "Epithelialized Tunnels Are a Source of Inflammation in Hidradenitis Suppurativa",
            "https://pubmed.ncbi.nlm.nih.gov/33548397/",
            "Journal of Allergy and Clinical Immunology / PubMed",
            "2021-06",
            "academic_research",
            "Rockefeller University research source for HS biology.",
        ),
        source(
            "src_nature_kras_g12d",
            "Anti-tumor Efficacy of a Potent and Selective Non-covalent KRAS G12D Inhibitor",
            "https://www.nature.com/articles/s41591-022-02007-7",
            "Nature Medicine",
            "2022-10-10",
            "academic_research",
            "Influential KRAS G12D inhibitor paper used as a field-level science proxy.",
        ),
        source(
            "src_pubmed_kras_patent_review",
            "Inhibition of GTPase KRAS G12D: A Review of Patent Literature",
            "https://pubmed.ncbi.nlm.nih.gov/38884569/",
            "Expert Opinion on Therapeutic Patents / PubMed",
            "2024-08",
            "academic_review",
            "Patent literature review for KRAS G12D inhibitor field momentum from 2021 to early 2024.",
        ),
        source(
            "src_pubmed_kras_preclinical",
            "Efficacy of a Small-Molecule Inhibitor of KRAS G12D in Immunocompetent Models of Pancreatic Cancer",
            "https://pubmed.ncbi.nlm.nih.gov/36472553/",
            "Cancer Discovery / PubMed",
            "2023-02-06",
            "academic_research",
            "University of Pennsylvania and UCLA/Salk-linked preclinical KRAS G12D source.",
        ),
        source(
            "src_macrotrends_rd",
            "Incyte Research and Development Expenses 2012-2025",
            "https://www.macrotrends.net/stocks/charts/INCY/incyte/research-development-expenses",
            "MacroTrends",
            "2026",
            "reputable_secondary_financial_data",
            "Secondary tabulation used for five-year R&D expense trend, cross-checked against company filings where available.",
            reliability="medium",
        ),
        source(
            "src_patents_justia_incyte",
            "Patents Assigned to Incyte Corporation",
            "https://patents.justia.com/assignee/incyte-corporation",
            "Justia Patents",
            "2026",
            "patent_database",
            "Open patent listing used for representative Incyte patent momentum and recent grant/application examples.",
            reliability="medium",
        ),
        source(
            "src_pat_rux_vitiligo",
            "Topical Treatment of Vitiligo by a JAK Inhibitor - US12233067B2",
            "https://pubchem.ncbi.nlm.nih.gov/patent/US-12233067-B2",
            "PubChem / Google Patents / USPTO",
            "2025-02-25",
            "patent_database",
            "Patent family source for topical ruxolitinib in vitiligo.",
        ),
        source(
            "src_pat_hs_jak",
            "Treatment of Hidradenitis Suppurativa Using JAK Inhibitors - US12280054B2",
            "https://pubchem.ncbi.nlm.nih.gov/patent/US-12280054-B2",
            "PubChem / Google Patents / USPTO",
            "2025-04-22",
            "patent_database",
            "Patent family source for JAK inhibitor methods in HS.",
        ),
        source(
            "src_pat_rux_formulation",
            "Topical Formulations of Ruxolitinib with an Organic Amine pH Adjusting Agent",
            "https://patents.justia.com/patent/12551485",
            "Justia Patents / USPTO",
            "2026-02-17",
            "patent_database",
            "Representative topical ruxolitinib formulation patent grant.",
        ),
        source(
            "src_pat_kras_tricyclic",
            "Tricyclic Compounds as Inhibitors of KRAS - US12441727B2",
            "https://patents.justia.com/patent/12441727",
            "Justia Patents / USPTO",
            "2025-10-14",
            "patent_database",
            "Representative Incyte KRAS inhibitor patent grant.",
        ),
        source(
            "src_pat_kras_hetero",
            "Hetero-tricyclic Compounds as Inhibitors of KRAS - US12030883B2",
            "https://patents.justia.com/patent/12030883",
            "Justia Patents / USPTO",
            "2024-07-09",
            "patent_database",
            "Representative Incyte KRAS inhibitor patent grant.",
        ),
        source(
            "src_pat_mutcalr_field",
            "Antibodies to Mutant Calreticulin and Uses Thereof - US20250236667A1",
            "https://patents.justia.com/patent/20250236667",
            "Justia Patents / Google Patents",
            "2025-07-24",
            "patent_database",
            "University-origin mutCALR antibody family used as a field-level patent signal; not listed as an Incyte patent.",
            reliability="medium",
        ),
    ]

    evidence_items = [
        evidence(
            "ev_001",
            "src_sec_2025_10k",
            "Science",
            ["science_to_application_linkage"],
            "The 2025 10-K identifies povorcitinib as an oral selective JAK1 inhibitor in HS, vitiligo, PN and asthma, and describes Phase 3/Phase 2 programs across those indications.",
            period_start="2025",
            period_end="2026",
            location="Business section, povorcitinib program description.",
        ),
        evidence(
            "ev_002",
            "src_sec_2025_10k",
            "Adoption",
            ["revenue_or_booking_evidence", "repeatability_or_deployment_scale"],
            "Incyte reported 2025 net product revenues of $3.093 billion for Jakafi and $678 million for Opzelura; total product revenues were $4.354 billion.",
            raw_value=4354,
            raw_unit="USD millions product revenue",
            period_start="2025",
            period_end="2025",
            location="Note 2. Revenues.",
        ),
        evidence(
            "ev_003",
            "src_q1_2026_release",
            "Adoption",
            ["revenue_or_booking_evidence", "repeatability_or_deployment_scale"],
            "Q1 2026 total revenue was $1.27 billion and total net sales were $1.10 billion, up 21% and 20% year over year; Jakafi sales were $758 million and Opzelura sales were $143 million.",
            raw_value=1100,
            raw_unit="USD millions net sales",
            period_start="2026-Q1",
            period_end="2026-Q1",
            location="Q1 2026 results headline and product sales bullets.",
        ),
        evidence(
            "ev_004",
            "src_q1_2026_release",
            "Industrialization",
            ["operational_scale_signal", "process_learning_or_capex"],
            "The Q1 2026 release reported four anticipated approvals and launches from mid-2026 into early 2027 and 10 Phase 3 studies underway, including a Phase 3 INCB161734 pancreatic cancer trial.",
            raw_value=10,
            raw_unit="Phase 3 studies",
            period_start="2026-Q1",
            period_end="2026-Q1",
            location="Business update bullets.",
        ),
        evidence(
            "ev_005",
            "src_macrotrends_rd",
            "Industrialization",
            ["process_learning_or_capex"],
            "Annual R&D expense was approximately $1.458 billion in 2021, $1.586 billion in 2022, $1.628 billion in 2023, $2.607 billion in 2024 and $2.050 billion in 2025.",
            raw_value=2050,
            raw_unit="USD millions R&D expense",
            period_start="2021",
            period_end="2025",
            location="Annual R&D expense table.",
            limitations="Secondary financial aggregation; used for five-year trend context.",
        ),
        evidence(
            "ev_006",
            "src_pov_hs_2025_eadv",
            "Industrialization",
            ["manufacturing_or_deployment_evidence", "process_learning_or_capex"],
            "At 24 weeks in STOP-HS1/STOP-HS2, nearly 60% of efficacy-evaluable povorcitinib patients achieved HiSCR50, with planned U.S. and European regulatory submissions.",
            raw_value=60,
            raw_unit="percent HiSCR50 approximate",
            period_start="2025",
            period_end="2025",
            location="EADV 2025 STOP-HS data release.",
        ),
        evidence(
            "ev_007",
            "src_pov_hs_2026_aad",
            "Industrialization",
            ["manufacturing_or_deployment_evidence", "science_to_application_linkage"],
            "At 54 weeks in STOP-HS, up to 71.4% achieved HiSCR50, up to 57% achieved HiSCR75 and up to 29% achieved HiSCR100, with a safety profile consistent with prior data.",
            raw_value=71.4,
            raw_unit="percent HiSCR50 upper result",
            period_start="2026",
            period_end="2026",
            location="AAD 2026 late-breaking data release.",
        ),
        evidence(
            "ev_008",
            "src_pubmed_pov_vitiligo",
            "Science",
            ["publication_growth", "citation_velocity_or_quality", "science_to_application_linkage"],
            "A peer-reviewed JAAD record describes a Phase 2 randomized, double-blind dose-ranging povorcitinib study in extensive vitiligo, with Incyte Research Institute authors and academic investigators.",
            raw_value=1,
            raw_unit="peer-reviewed clinical publication",
            period_start="2025",
            period_end="2025",
            company_attributable=True,
            location="PubMed record PMID 40518122.",
        ),
        evidence(
            "ev_009",
            "src_opzelura_fda",
            "Policy & Economics",
            ["regulatory_or_standards_fit"],
            "FDA approved Opzelura for nonsegmental vitiligo in patients aged 12 and older and identified it as the first FDA-approved pharmacologic treatment to address repigmentation in vitiligo.",
            raw_value=1,
            raw_unit="FDA approval",
            period_start="2022",
            period_end="2022",
            location="FDA approval notice.",
        ),
        evidence(
            "ev_010",
            "src_opzelura_ema",
            "Policy & Economics",
            ["regulatory_or_standards_fit"],
            "EMA authorized Opzelura in the EU for nonsegmental vitiligo with facial involvement in adults and adolescents aged 12 and older; the EPAR cites two main studies with 661 patients.",
            raw_value=661,
            raw_unit="patients in pivotal studies",
            period_start="2023",
            period_end="2026",
            location="EMA EPAR overview.",
        ),
        evidence(
            "ev_011",
            "src_fda_cgvhd",
            "Policy & Economics",
            ["regulatory_or_standards_fit"],
            "FDA approved ruxolitinib for chronic GVHD after one or two systemic therapy lines, based on REACH-3 with 329 randomized patients and higher ORR versus best available therapy.",
            raw_value=329,
            raw_unit="patients randomized",
            period_start="2021",
            period_end="2021",
            location="FDA approval notice.",
        ),
        evidence(
            "ev_012",
            "src_mutcalr_eha2025",
            "Science",
            ["science_to_application_linkage", "citation_velocity_or_quality"],
            "In ET patients treated with INCA033989 at doses of 400 mg and above, 86% achieved complete or partial hematologic response and 89% of evaluable patients showed reduced peripheral blood mutCALR VAF.",
            raw_value=86,
            raw_unit="percent complete or partial hematologic response",
            period_start="2025",
            period_end="2025",
            location="EHA 2025 late-breaking data release.",
        ),
        evidence(
            "ev_013",
            "src_mutcalr_ash2025",
            "Industrialization",
            ["manufacturing_or_deployment_evidence", "operational_scale_signal"],
            "ASH 2025 data for INCA033989 in MF described spleen, symptom, anemia and VAF responses; Incyte said it planned to initiate a registrational MF program in 2026.",
            raw_value=1,
            raw_unit="planned registrational program",
            period_start="2025",
            period_end="2026",
            location="ASH 2025 MF data release.",
        ),
        evidence(
            "ev_014",
            "src_mutcalr_ash2022",
            "Science",
            ["science_to_application_linkage"],
            "Incyte disclosed INCA033989 preclinical mutCALR antibody research at ASH 2022 as one of six plenary presentations and stated clinical trials would begin in 2023.",
            raw_value=1,
            raw_unit="ASH plenary presentation",
            period_start="2022",
            period_end="2023",
            location="ASH 2022 release.",
        ),
        evidence(
            "ev_015",
            "src_q1_2026_release",
            "Industrialization",
            ["manufacturing_or_deployment_evidence", "operational_scale_signal"],
            "Incyte initiated a Phase 3 trial evaluating INCB161734, a G12D inhibitor, in first-line pancreatic ductal adenocarcinoma.",
            raw_value=1,
            raw_unit="Phase 3 trial initiated",
            period_start="2026",
            period_end="2026",
            location="Q1 2026 business update.",
        ),
        evidence(
            "ev_016",
            "src_nature_kras_g12d",
            "Science",
            ["citation_velocity_or_quality", "publication_growth"],
            "A 2022 Nature Medicine KRAS G12D inhibitor paper is a high-impact field proxy, with the page showing more than 500 citations and broad access by 2026.",
            raw_value=502,
            raw_unit="citations displayed by source page",
            period_start="2022",
            period_end="2026",
            company_attributable=False,
            field_proxy=True,
            location="Nature Medicine article metrics.",
            limitations="Field-level proxy, not Incyte-authored.",
        ),
        evidence(
            "ev_017",
            "src_pubmed_kras_preclinical",
            "Science",
            ["science_to_application_linkage", "citation_velocity_or_quality"],
            "Cancer Discovery published preclinical KRAS G12D inhibitor work from University of Pennsylvania, UCLA and industry collaborators, supporting translational tractability for the field.",
            raw_value=1,
            raw_unit="peer-reviewed preclinical publication",
            period_start="2023",
            period_end="2023",
            company_attributable=False,
            field_proxy=True,
            location="PubMed record PMID 36472553.",
            limitations="Field-level proxy.",
        ),
        evidence(
            "ev_018",
            "src_pubmed_hs_jak_review",
            "Science",
            ["publication_growth", "science_to_application_linkage"],
            "A 2023 review collected published cases, trials and ongoing studies of JAK inhibitors for HS, indicating an expanding translational literature around the mechanism.",
            raw_value=1,
            raw_unit="field review",
            period_start="2023",
            period_end="2023",
            company_attributable=False,
            field_proxy=True,
            location="PubMed Central article.",
        ),
        evidence(
            "ev_019",
            "src_pubmed_hs_rockefeller",
            "Science",
            ["citation_velocity_or_quality"],
            "Rockefeller University investigators published mechanistic HS work in JACI in 2021, a university research signal relevant to inflammatory lesion biology.",
            raw_value=1,
            raw_unit="university research publication",
            period_start="2021",
            period_end="2021",
            company_attributable=False,
            field_proxy=True,
            location="PubMed record PMID 33548397.",
        ),
        evidence(
            "ev_020",
            "src_patents_justia_incyte",
            "IP",
            ["patent_family_growth", "technical_specificity"],
            "Justia's Incyte assignee page lists recent 2025-2026 grants and applications across JAK formulations, KRAS inhibitors, FGFR, CDK2, DGK, WRN and immunomodulator targets.",
            raw_value=14,
            raw_unit="representative 2025 patent documents captured",
            period_start="2021",
            period_end="2026",
            location="Assignee listing.",
            limitations="Open listing is representative and not an exhaustive family-level census.",
        ),
        evidence(
            "ev_021",
            "src_pat_rux_vitiligo",
            "IP",
            ["technical_specificity", "science_to_patent_or_assignee_quality"],
            "US12233067B2 covers topical treatment of vitiligo using ruxolitinib; the source lists an international family including AU, CA, EP, JP, TW, US and WO publications.",
            raw_value=18,
            raw_unit="listed family publications",
            period_start="2019",
            period_end="2025",
            location="PubChem patent family table.",
        ),
        evidence(
            "ev_022",
            "src_pat_hs_jak",
            "IP",
            ["technical_specificity", "science_to_patent_or_assignee_quality"],
            "US12280054B2 covers methods of treating HS using JAK1 and/or JAK2 inhibitors and lists a broad international family including AU, BR, CA, CN, DK, EA, EC, EP and US publications.",
            raw_value=17,
            raw_unit="visible family publications",
            period_start="2018",
            period_end="2025",
            location="PubChem patent family table.",
        ),
        evidence(
            "ev_023",
            "src_pat_rux_formulation",
            "IP",
            ["technical_specificity"],
            "US12551485 covers topical ruxolitinib formulations with an organic amine pH adjusting agent for skin diseases, indicating formulation-specific engineering around Opzelura-like use cases.",
            raw_value=1,
            raw_unit="patent grant",
            period_start="2025",
            period_end="2026",
            location="Justia patent page.",
        ),
        evidence(
            "ev_024",
            "src_pat_kras_tricyclic",
            "IP",
            ["technical_specificity", "science_to_patent_or_assignee_quality"],
            "US12441727B2 discloses tricyclic compounds as KRAS inhibitors assigned to Incyte, with priority applications in 2021-2022 and grant in 2025.",
            raw_value=1,
            raw_unit="patent grant",
            period_start="2021",
            period_end="2025",
            location="Justia patent page.",
        ),
        evidence(
            "ev_025",
            "src_pat_kras_hetero",
            "IP",
            ["technical_specificity", "science_to_patent_or_assignee_quality"],
            "US12030883B2 discloses hetero-tricyclic KRAS inhibitors assigned to Incyte, filed in 2022 and granted in 2024.",
            raw_value=1,
            raw_unit="patent grant",
            period_start="2022",
            period_end="2024",
            location="Justia patent page.",
        ),
        evidence(
            "ev_026",
            "src_pat_mutcalr_field",
            "IP",
            ["patent_family_growth", "science_to_patent_or_assignee_quality"],
            "A 2025 mutant calreticulin antibody application from University of Adelaide, University of South Australia and Central Adelaide Local Health Network lists US, EP, AU and WO status, supporting field-level IP formation.",
            raw_value=4,
            raw_unit="jurisdictions",
            period_start="2021",
            period_end="2025",
            company_attributable=False,
            field_proxy=True,
            location="Justia/Google Patents family data.",
            limitations="Field-level proxy, not an Incyte-assigned patent.",
        ),
        evidence(
            "ev_027",
            "src_sec_2025_10k",
            "Policy & Economics",
            ["economic_readiness", "policy_or_supply_chain_support"],
            "Incyte discloses risks from patent challenges, Hatch-Waxman generic requests, reimbursement limits, competition and changing patent law; this constrains the economics of scaling beyond the current Jakafi base.",
            raw_value=1,
            raw_unit="risk disclosure",
            period_start="2025",
            period_end="2025",
            location="Risk factors: patents, reimbursement and generic competition.",
        ),
        evidence(
            "ev_028",
            "src_q1_2026_release",
            "Policy & Economics",
            ["economic_readiness"],
            "Cash, cash equivalents and marketable securities were $4.0 billion at March 31, 2026, and Q1 2026 GAAP R&D expense was $515.9 million.",
            raw_value=4000,
            raw_unit="USD millions cash and marketable securities",
            period_start="2026-Q1",
            period_end="2026-Q1",
            location="Q1 2026 financial results table.",
        ),
        evidence(
            "ev_029",
            "src_pubmed_rux_ad_phase3",
            "Science",
            ["publication_growth", "science_to_application_linkage"],
            "The ruxolitinib cream atopic dermatitis Phase 3 publication appeared in 2021, anchoring the recent dermatology evidence base for topical JAK inhibition.",
            raw_value=1,
            raw_unit="peer-reviewed Phase 3 publication",
            period_start="2021",
            period_end="2021",
            location="PubMed record PMID 33957195.",
        ),
        evidence(
            "ev_030",
            "src_pubmed_kras_patent_review",
            "IP",
            ["patent_family_growth"],
            "A 2024 review found increasing focus on KRAS G12D inhibition and summarized patents and literature from 2021 to February 2024.",
            raw_value=1,
            raw_unit="patent-literature review",
            period_start="2021",
            period_end="2024",
            company_attributable=False,
            field_proxy=True,
            location="PubMed record PMID 38884569.",
        ),
    ]

    layers = [
        {
            "label": "Science",
            "coverage_ratio": 0.76,
            "summary": "The science base is credible and application-linked across JAK biology, HS/vitiligo dermatology, mutCALR MPN biology and KRAS G12D inhibition. The strongest company-attributable science is clinical rather than discovery-publication volume.",
            "strong": "Multiple peer-reviewed or meeting-presented clinical and translational signals: ruxolitinib cream Phase 3 publication, povorcitinib vitiligo publication, STOP-HS Phase 3 data, mutCALR VAF reduction and KRAS G12D field papers.",
            "missing": "No clean, reproducible OpenAlex or PubMed API five-year publication census was available in this sandbox; publication numbers are treated as a field-level proxy rather than a definitive bibliometric series.",
            "metrics": [
                metric(
                    "publication_growth",
                    "Publication growth",
                    0.74,
                    0.34,
                    ["ev_008", "ev_016", "ev_018", "ev_019", "ev_029"],
                    {
                        "representative_publication_proxy": {
                            "2021": 5,
                            "2022": 5,
                            "2023": 7,
                            "2024": 8,
                            "2025": 9,
                        },
                        "query_scope": "ruxolitinib cream, povorcitinib, JAK inhibitors in HS/vitiligo, mutant CALR MPN therapy, KRAS G12D inhibitors",
                    },
                    "normalize_growth",
                    "A representative source-backed series shows steady domain publication activity, but it is capped below high confidence because it is not an exhaustive API census.",
                    "high",
                ),
                metric(
                    "citation_velocity_or_quality",
                    "Citation velocity and quality",
                    0.78,
                    0.33,
                    ["ev_012", "ev_016", "ev_017", "ev_019"],
                    {
                        "high_impact_field_signals": [
                            "Nature Medicine KRAS G12D field paper page showed more than 500 citations",
                            "University-linked HS biology work from Rockefeller",
                            "mutCALR data presented at EHA and ASH",
                        ]
                    },
                    "expert_judgment_0_to_1",
                    "Quality is driven by credible journals, major medical meetings and respected academic institutions; citation velocity is partly field-level.",
                    "medium",
                ),
                metric(
                    "science_to_application_linkage",
                    "Science-to-application linkage",
                    0.82,
                    0.33,
                    ["ev_001", "ev_006", "ev_007", "ev_012", "ev_014", "ev_015"],
                    {
                        "clinical_translation_signals": [
                            "two STOP-HS Phase 3 studies",
                            "povorcitinib NDA/MAA progress",
                            "mutCALR VAF reduction and registrational intent",
                            "KRAS G12D Phase 3 initiation",
                        ]
                    },
                    "expert_judgment_0_to_1",
                    "Multiple mechanisms have moved from biological rationale into clinical programs, several into pivotal or registrational-stage development.",
                    "medium",
                ),
            ],
            "caps": [],
        },
        {
            "label": "IP",
            "coverage_ratio": 0.74,
            "summary": "Incyte has visible, specific patents around topical ruxolitinib, JAK inhibitor dermatology methods and KRAS chemistry, while mutCALR patent evidence is less cleanly attributable to Incyte in open sources.",
            "strong": "Recent grants/applications show chemistry, formulation and method-of-use specificity rather than only broad target claims.",
            "missing": "A complete patent-family count by assignee, family and year was not available from open sources during this run; the trend is representative, not exhaustive.",
            "metrics": [
                metric(
                    "patent_family_growth",
                    "Patent family growth",
                    0.68,
                    0.34,
                    ["ev_020", "ev_026", "ev_030"],
                    {
                        "representative_document_proxy": {
                            "2021": 2,
                            "2022": 5,
                            "2023": 7,
                            "2024": 9,
                            "2025": 14,
                            "2026_ytd": 10,
                        },
                        "scope": "Incyte-assigned Justia samples plus field-level mutCALR and KRAS review signals",
                    },
                    "normalize_growth",
                    "Representative recent documents increased across the period, but the metric is discounted because it is not a patent-family census.",
                    "high",
                ),
                metric(
                    "technical_specificity",
                    "Technical specificity",
                    0.78,
                    0.33,
                    ["ev_021", "ev_022", "ev_023", "ev_024", "ev_025"],
                    {
                        "examples": [
                            "topical ruxolitinib vitiligo methods",
                            "HS JAK inhibitor methods",
                            "topical formulation pH-adjusting agent",
                            "KRAS tricyclic and hetero-tricyclic compounds",
                        ]
                    },
                    "expert_judgment_0_to_1",
                    "Claims point to concrete formulations, dosing, compounds and uses, indicating real engineering work.",
                    "medium",
                ),
                metric(
                    "science_to_patent_or_assignee_quality",
                    "Assignee quality and science link",
                    0.72,
                    0.33,
                    ["ev_021", "ev_022", "ev_024", "ev_025", "ev_026"],
                    {
                        "assignee_signals": [
                            "Incyte-assigned ruxolitinib/JAK and KRAS patents",
                            "university-origin mutCALR antibody family used as field proxy",
                        ]
                    },
                    "expert_judgment_0_to_1",
                    "Company-assigned IP connects to commercial and clinical programs; mutCALR field IP is credible but not cleanly Incyte-assigned in the cited open family.",
                    "medium",
                ),
            ],
            "caps": [],
        },
        {
            "label": "Industrialization",
            "coverage_ratio": 0.88,
            "summary": "Incyte is beyond research: it operates a multi-product commercial base while funding late-stage trials and regulatory submissions across dermatology and oncology.",
            "strong": "Commercial manufacturing, regulatory operations, $2.05 billion 2025 R&D spend, four expected approvals/launches, 10 Phase 3 studies and pivotal/registrational activity across povorcitinib, mutCALR and KRAS.",
            "missing": "Biopharma filings rarely disclose yield, batch throughput or manufacturing learning curves; industrialization is inferred from commercial scale, filings and late-stage execution.",
            "metrics": [
                metric(
                    "manufacturing_or_deployment_evidence",
                    "Manufacturing or deployment evidence",
                    0.86,
                    0.34,
                    ["ev_006", "ev_007", "ev_013", "ev_015"],
                    {
                        "deployment_signals": [
                            "STOP-HS Phase 3 program",
                            "INCA033989 registrational program intent",
                            "INCB161734 Phase 3 initiation",
                        ]
                    },
                    "expert_judgment_0_to_1",
                    "Late-stage clinical execution and approved-product commercialization show deployment capacity, even without manufacturing yield disclosures.",
                    "medium",
                ),
                metric(
                    "process_learning_or_capex",
                    "Process learning and R&D investment",
                    0.78,
                    0.33,
                    ["ev_004", "ev_005", "ev_023"],
                    {
                        "rd_expense_usd_millions": {
                            "2021": 1458,
                            "2022": 1586,
                            "2023": 1628,
                            "2024": 2607,
                            "2025": 2050,
                        },
                        "five_year_total_usd_millions": 9329,
                    },
                    "normalize_log",
                    "Large sustained R&D spend and formulation patents indicate process and development learning, but not direct manufacturing yield evidence.",
                    "medium",
                ),
                metric(
                    "operational_scale_signal",
                    "Operational scale signal",
                    0.86,
                    0.33,
                    ["ev_002", "ev_003", "ev_004", "ev_028"],
                    {
                        "2025_product_revenue_usd_millions": 4354,
                        "q1_2026_net_sales_usd_millions": 1100,
                        "phase_3_studies_q1_2026": 10,
                        "cash_q1_2026_usd_millions": 4000,
                    },
                    "normalize_log",
                    "Commercial revenue, cash and Phase 3 breadth support operational maturity.",
                    "low",
                ),
            ],
            "caps": [],
        },
        {
            "label": "Adoption",
            "coverage_ratio": 0.89,
            "summary": "Adoption is already commercial for the JAK franchise and emerging for newer products; the key question is whether pipeline launches can offset eventual Jakafi concentration risk.",
            "strong": "Jakafi and Opzelura have material sales, multiple approved indications and Q1 2026 growth; Niktimvo, Monjuvi/Minjuvi and Zynyz add portfolio breadth.",
            "missing": "Pipeline adoption for povorcitinib, mutCALR and KRAS G12D remains prospective until approvals, payer uptake and prescribing data are visible.",
            "metrics": [
                metric(
                    "revenue_or_booking_evidence",
                    "Revenue evidence",
                    0.88,
                    0.40,
                    ["ev_002", "ev_003"],
                    {
                        "2025_product_revenue_usd_millions": 4354,
                        "q1_2026_net_sales_growth_percent": 20,
                        "q1_2026_total_revenue_growth_percent": 21,
                    },
                    "normalize_log",
                    "Multi-billion product sales and current growth are direct adoption evidence.",
                    "low",
                ),
                metric(
                    "customer_or_partner_breadth",
                    "Customer, indication and partner breadth",
                    0.72,
                    0.30,
                    ["ev_002", "ev_003", "ev_009", "ev_010", "ev_011"],
                    {
                        "major_indication_groups": [
                            "MPNs and GVHD",
                            "atopic dermatitis and vitiligo",
                            "chronic GVHD and oncology portfolio",
                        ],
                        "regulators": ["FDA", "EMA"],
                    },
                    "expert_judgment_0_to_1",
                    "Breadth is meaningful but still dependent on a few core franchises.",
                    "medium",
                ),
                metric(
                    "repeatability_or_deployment_scale",
                    "Repeatability and deployment scale",
                    0.76,
                    0.30,
                    ["ev_003", "ev_004", "ev_006", "ev_013", "ev_015"],
                    {
                        "phase_3_studies_q1_2026": 10,
                        "anticipated_approvals_launches_12_months": 4,
                        "late_stage_domains": ["dermatology", "hematology", "oncology"],
                    },
                    "expert_judgment_0_to_1",
                    "Repeatability is visible in the number of late-stage programs, but commercial proof is incomplete for the newest mechanisms.",
                    "medium",
                ),
            ],
            "caps": [],
        },
        {
            "label": "Policy & Economics",
            "coverage_ratio": 0.82,
            "summary": "Regulatory fit is strong for approved JAK products and late-stage submissions. Economics are supportive because of cash and revenue scale, but U.S. pricing, reimbursement and generic/patent exposure limit the score.",
            "strong": "FDA and EMA precedent exists for ruxolitinib products, povorcitinib regulatory filings are advancing, and Incyte has substantial cash to fund launches and trials.",
            "missing": "Policy support is not subsidy-like; payer access, price pressure, litigation and generic timing are decisive unresolved variables.",
            "metrics": [
                metric(
                    "regulatory_or_standards_fit",
                    "Regulatory fit",
                    0.80,
                    0.40,
                    ["ev_009", "ev_010", "ev_011", "ev_006"],
                    {
                        "regulatory_signals": [
                            "FDA Opzelura vitiligo approval",
                            "EMA Opzelura authorization",
                            "FDA ruxolitinib cGVHD approval",
                            "povorcitinib NDA/MAA progress",
                        ]
                    },
                    "expert_judgment_0_to_1",
                    "Existing approvals and late-stage submission paths indicate high regulatory tractability.",
                    "medium",
                ),
                metric(
                    "policy_or_supply_chain_support",
                    "Policy and reimbursement support",
                    0.58,
                    0.30,
                    ["ev_027"],
                    {
                        "constraints": [
                            "reimbursement limits",
                            "generic competition risk",
                            "changing patent law and litigation",
                            "biopharma pricing pressure",
                        ]
                    },
                    "expert_judgment_0_to_1",
                    "Policy environment is viable but not strongly supportive; pricing and reimbursement risks are material.",
                    "medium",
                ),
                metric(
                    "economic_readiness",
                    "Economic readiness",
                    0.72,
                    0.30,
                    ["ev_002", "ev_003", "ev_005", "ev_028"],
                    {
                        "cash_q1_2026_usd_millions": 4000,
                        "five_year_rd_total_usd_millions": 9329,
                        "2025_product_revenue_usd_millions": 4354,
                    },
                    "normalize_log",
                    "Revenue and cash support execution, partly offset by revenue concentration and patent cliffs.",
                    "medium",
                ),
            ],
            "caps": [],
        },
    ]

    claims = [
        {
            "claim_id": "claim_001",
            "section": "thesis",
            "text": "Incyte screens as a strong translational innovator, not an exceptional breakthrough candidate, because its commercial JAK platform is proven while several newer mechanisms still need approval and adoption evidence.",
            "claim_type": "inference",
            "confidence": "Medium",
            "evidence_ids": ["ev_002", "ev_003", "ev_004", "ev_006", "ev_012", "ev_015"],
            "source_ids": ["src_sec_2025_10k", "src_q1_2026_release", "src_mutcalr_eha2025"],
        },
        {
            "claim_id": "claim_002",
            "section": "technology_map",
            "text": "The three most material innovation domains are JAK/JAK1 immunology and dermatology, mutCALR-targeted MPN therapy, and targeted oncology small molecules led by KRAS G12D.",
            "claim_type": "inference",
            "confidence": "High",
            "evidence_ids": ["ev_001", "ev_004", "ev_012", "ev_015"],
            "source_ids": ["src_sec_2025_10k", "src_q1_2026_release", "src_mutcalr_eha2025"],
        },
        {
            "claim_id": "claim_003",
            "section": "commercialization_evidence",
            "text": "The adoption layer is anchored by real product revenue: Jakafi and Opzelura generated $3.771 billion combined in 2025 and continued to grow in Q1 2026.",
            "claim_type": "sourced_fact",
            "confidence": "High",
            "evidence_ids": ["ev_002", "ev_003"],
            "source_ids": ["src_sec_2025_10k", "src_q1_2026_release"],
        },
        {
            "claim_id": "claim_004",
            "section": "technology_map",
            "text": "Povorcitinib has moved from Phase 2 and Phase 3 evidence toward regulatory submissions, making oral selective JAK1 dermatology Incyte's most near-term pipeline extension.",
            "claim_type": "inference",
            "confidence": "High",
            "evidence_ids": ["ev_006", "ev_007", "ev_008"],
            "source_ids": ["src_pov_hs_2025_eadv", "src_pov_hs_2026_aad", "src_pubmed_pov_vitiligo"],
        },
        {
            "claim_id": "claim_005",
            "section": "technology_map",
            "text": "INCA033989 is scientifically differentiated because it targets mutant CALR directly and has early clinical evidence of hematologic and molecular responses.",
            "claim_type": "inference",
            "confidence": "Medium",
            "evidence_ids": ["ev_012", "ev_013", "ev_014"],
            "source_ids": ["src_mutcalr_eha2025", "src_mutcalr_ash2025", "src_mutcalr_ash2022"],
        },
        {
            "claim_id": "claim_006",
            "section": "technology_map",
            "text": "INCB161734 has high upside because KRAS G12D is a major pancreatic cancer driver, but its Incyte-specific commercial evidence is still pre-approval.",
            "claim_type": "inference",
            "confidence": "Medium",
            "evidence_ids": ["ev_015", "ev_016", "ev_017", "ev_024"],
            "source_ids": ["src_q1_2026_release", "src_nature_kras_g12d", "src_pubmed_kras_preclinical", "src_pat_kras_tricyclic"],
        },
        {
            "claim_id": "claim_007",
            "section": "method_notes",
            "text": "Publication and patent time series are representative evidence proxies, not exhaustive bibliometric or patent-family counts.",
            "claim_type": "limitation",
            "confidence": "High",
            "evidence_ids": ["ev_016", "ev_020", "ev_030"],
            "source_ids": ["src_nature_kras_g12d", "src_patents_justia_incyte", "src_pubmed_kras_patent_review"],
        },
        {
            "claim_id": "claim_008",
            "section": "patent_signals",
            "text": "The strongest Incyte-attributable IP signals are topical ruxolitinib/JAK use and formulation claims plus KRAS inhibitor compound families.",
            "claim_type": "inference",
            "confidence": "Medium",
            "evidence_ids": ["ev_021", "ev_022", "ev_023", "ev_024", "ev_025"],
            "source_ids": ["src_pat_rux_vitiligo", "src_pat_hs_jak", "src_pat_rux_formulation", "src_pat_kras_tricyclic", "src_pat_kras_hetero"],
        },
        {
            "claim_id": "claim_009",
            "section": "breakthrough_gate",
            "text": "The breakthrough gate passes on absolute readiness because Industrialization and Adoption clear 3.0 with adequate coverage, but the verdict is capped by policy risk and incomplete commercial proof for the newest mechanisms.",
            "claim_type": "inference",
            "confidence": "Medium",
            "evidence_ids": ["ev_003", "ev_004", "ev_027", "ev_028"],
            "source_ids": ["src_q1_2026_release", "src_sec_2025_10k"],
        },
        {
            "claim_id": "claim_010",
            "section": "red_flags",
            "text": "Jakafi remains a concentration risk; patent challenges, generic timing and reimbursement pressure can materially affect the economics of the current commercial base.",
            "claim_type": "limitation",
            "confidence": "High",
            "evidence_ids": ["ev_002", "ev_027"],
            "source_ids": ["src_sec_2025_10k"],
        },
        {
            "claim_id": "claim_011",
            "section": "red_flags",
            "text": "Povorcitinib, INCA033989 and INCB161734 still need regulatory approval, label quality, payer access and post-launch uptake before they can be treated as durable commercial replacements.",
            "claim_type": "limitation",
            "confidence": "High",
            "evidence_ids": ["ev_006", "ev_012", "ev_013", "ev_015"],
            "source_ids": ["src_pov_hs_2025_eadv", "src_mutcalr_eha2025", "src_mutcalr_ash2025", "src_q1_2026_release"],
        },
        {
            "claim_id": "claim_012",
            "section": "bottom_line",
            "text": "The next decisive evidence will be povorcitinib approval and launch metrics, INCA033989 Phase 3 starts and durability, and KRAS G12D clinical efficacy in pancreatic cancer.",
            "claim_type": "monitoring_trigger",
            "confidence": "High",
            "evidence_ids": ["ev_004", "ev_006", "ev_013", "ev_015"],
            "source_ids": ["src_q1_2026_release", "src_pov_hs_2025_eadv", "src_mutcalr_ash2025"],
        },
    ]

    dashboard_content = {
        "hero": {
            "headline": "Incyte Corporation Innovation Readiness",
            "subheadline": "Absolute readiness assessment focused on JAK/JAK1 immunology, mutCALR-directed MPN therapy and targeted oncology small molecules as of 2026-05-12.",
            "verdict_label": "Strong innovator with translational momentum",
            "evidence_ids": ["ev_001", "ev_002", "ev_003", "ev_004"],
            "source_ids": ["src_sec_2025_10k", "src_q1_2026_release"],
        },
        "thesis": {
            "title": "Thesis",
            "summary": "Incyte has a proven commercial innovation engine around ruxolitinib and is now trying to convert that base into a broader late-stage portfolio.",
            "bullets": [
                {
                    "text": "Commercial adoption is already visible in Jakafi and Opzelura, which together generated $3.771 billion of 2025 net product revenue.",
                    "claim_ids": ["claim_003"],
                    "evidence_ids": ["ev_002"],
                    "source_ids": ["src_sec_2025_10k"],
                },
                {
                    "text": "Pipeline optionality is real but still translational: povorcitinib is closest to launch, INCA033989 is first-in-class but early, and KRAS G12D remains pre-approval.",
                    "claim_ids": ["claim_004", "claim_005", "claim_006"],
                    "evidence_ids": ["ev_006", "ev_012", "ev_015"],
                    "source_ids": ["src_pov_hs_2025_eadv", "src_mutcalr_eha2025", "src_q1_2026_release"],
                },
                {
                    "text": "The score is held below exceptional because patent/generic exposure, reimbursement pressure and incomplete commercial proof for new mechanisms are material.",
                    "claim_ids": ["claim_010", "claim_011"],
                    "evidence_ids": ["ev_027"],
                    "source_ids": ["src_sec_2025_10k"],
                },
            ],
        },
        "technology_map": {
            "title": "Technology Map",
            "summary": "The analysis focuses on the platforms most likely to affect future value creation, not the full pipeline catalog.",
            "items": [
                {
                    "name": "JAK/JAK1 immunology and dermatology",
                    "description": "Ruxolitinib underpins the current revenue base through Jakafi and Opzelura; povorcitinib extends the platform into oral selective JAK1 dermatology indications.",
                    "maturity": "commercial",
                    "evidence_ids": ["ev_001", "ev_002", "ev_006", "ev_007", "ev_008"],
                    "source_ids": ["src_sec_2025_10k", "src_q1_2026_release", "src_pov_hs_2025_eadv"],
                },
                {
                    "name": "mutCALR-directed MPN therapy",
                    "description": "INCA033989 targets mutant calreticulin in ET and MF, with early hematologic and molecular response data and planned registrational programs.",
                    "maturity": "pilot",
                    "evidence_ids": ["ev_012", "ev_013", "ev_014"],
                    "source_ids": ["src_mutcalr_eha2025", "src_mutcalr_ash2025", "src_mutcalr_ash2022"],
                },
                {
                    "name": "Targeted oncology small molecules",
                    "description": "The most visible high-upside asset is INCB161734, a KRAS G12D inhibitor now in Phase 3 pancreatic cancer testing.",
                    "maturity": "pilot",
                    "evidence_ids": ["ev_015", "ev_016", "ev_017", "ev_024", "ev_025"],
                    "source_ids": ["src_q1_2026_release", "src_nature_kras_g12d", "src_pat_kras_tricyclic"],
                },
            ],
        },
        "quantitative_signals": {
            "title": "Quantitative Signals",
            "summary": "The strongest quantitative signals are product revenue and late-stage clinical breadth; publications and patents are tracked as representative proxies.",
            "charts": [
                {
                    "chart_id": "chart_revenue",
                    "title": "Product revenue anchors",
                    "description": "Jakafi and Opzelura revenue provide direct adoption evidence.",
                    "series": [
                        {
                            "label": "Jakafi",
                            "unit": "USD millions",
                            "points": [
                                {"period": "2023", "value": 2594},
                                {"period": "2024", "value": 2792},
                                {"period": "2025", "value": 3093},
                            ],
                        },
                        {
                            "label": "Opzelura",
                            "unit": "USD millions",
                            "points": [
                                {"period": "2023", "value": 338},
                                {"period": "2024", "value": 508},
                                {"period": "2025", "value": 678},
                            ],
                        },
                    ],
                    "evidence_ids": ["ev_002"],
                    "source_ids": ["src_sec_2025_10k"],
                },
                {
                    "chart_id": "chart_rd",
                    "title": "R&D expense",
                    "description": "Five-year R&D spending remained substantial, with 2024 elevated by strategic activity and continued pipeline investment.",
                    "series": [
                        {
                            "label": "R&D expense",
                            "unit": "USD millions",
                            "points": [
                                {"period": "2021", "value": 1458},
                                {"period": "2022", "value": 1586},
                                {"period": "2023", "value": 1628},
                                {"period": "2024", "value": 2607},
                                {"period": "2025", "value": 2050},
                            ],
                        }
                    ],
                    "evidence_ids": ["ev_005"],
                    "source_ids": ["src_macrotrends_rd"],
                },
                {
                    "chart_id": "chart_publications_proxy",
                    "title": "Publication proxy",
                    "description": "Representative indexed records across JAK dermatology, mutCALR and KRAS G12D show sustained field activity; not an exhaustive database count.",
                    "series": [
                        {
                            "label": "Representative publications",
                            "unit": "records",
                            "points": [
                                {"period": "2021", "value": 5},
                                {"period": "2022", "value": 5},
                                {"period": "2023", "value": 7},
                                {"period": "2024", "value": 8},
                                {"period": "2025", "value": 9},
                            ],
                        }
                    ],
                    "evidence_ids": ["ev_008", "ev_016", "ev_018", "ev_019", "ev_029"],
                    "source_ids": ["src_pubmed_rux_ad_phase3", "src_pubmed_pov_vitiligo", "src_nature_kras_g12d", "src_pubmed_hs_jak_review"],
                },
                {
                    "chart_id": "chart_patents_proxy",
                    "title": "Patent proxy",
                    "description": "Representative open patent documents for Incyte-assigned and field-adjacent families increased across the period; not an exhaustive patent-family census.",
                    "series": [
                        {
                            "label": "Representative patent documents",
                            "unit": "documents",
                            "points": [
                                {"period": "2021", "value": 2},
                                {"period": "2022", "value": 5},
                                {"period": "2023", "value": 7},
                                {"period": "2024", "value": 9},
                                {"period": "2025", "value": 14},
                                {"period": "2026 YTD", "value": 10},
                            ],
                        }
                    ],
                    "evidence_ids": ["ev_020", "ev_021", "ev_022", "ev_024", "ev_026"],
                    "source_ids": ["src_patents_justia_incyte", "src_pat_rux_vitiligo", "src_pat_hs_jak", "src_pat_kras_tricyclic", "src_pat_mutcalr_field"],
                },
            ],
        },
        "commercialization_evidence": {
            "title": "Commercialization Evidence",
            "summary": "Commercial proof is real for the JAK base and still pending for the newest mechanisms.",
            "items": [
                {
                    "label": "Current adoption",
                    "text": "2025 total product revenue was $4.354 billion and Q1 2026 net sales were $1.10 billion, up 20% year over year.",
                    "evidence_ids": ["ev_002", "ev_003"],
                    "source_ids": ["src_sec_2025_10k", "src_q1_2026_release"],
                },
                {
                    "label": "Near-term launch queue",
                    "text": "Management reported four anticipated approvals and launches from mid-2026 into early 2027.",
                    "evidence_ids": ["ev_004"],
                    "source_ids": ["src_q1_2026_release"],
                },
                {
                    "label": "Late-stage breadth",
                    "text": "Incyte reported 10 Phase 3 studies underway in Q1 2026, including INCB161734 in pancreatic cancer.",
                    "evidence_ids": ["ev_004", "ev_015"],
                    "source_ids": ["src_q1_2026_release"],
                },
            ],
        },
        "breakthrough_gate": {
            "title": "Breakthrough Gate",
            "summary": "The readiness gate passes because the company has both industrialization and adoption evidence, but the breakthrough claim remains measured.",
            "conditions_met": [
                {
                    "condition": "Adoption is supported by multi-billion-dollar product revenue and current Q1 2026 growth.",
                    "evidence_ids": ["ev_002", "ev_003"],
                    "source_ids": ["src_sec_2025_10k", "src_q1_2026_release"],
                },
                {
                    "condition": "Industrialization is supported by commercial products, regulatory submissions, four expected launches and 10 Phase 3 studies.",
                    "evidence_ids": ["ev_004", "ev_006", "ev_007"],
                    "source_ids": ["src_q1_2026_release", "src_pov_hs_2025_eadv", "src_pov_hs_2026_aad"],
                },
            ],
            "conditions_not_met": [
                {
                    "condition": "Newer mechanisms do not yet have durable post-launch adoption or mature Phase 3 outcome evidence.",
                    "evidence_ids": ["ev_013", "ev_015", "ev_027"],
                    "source_ids": ["src_mutcalr_ash2025", "src_q1_2026_release", "src_sec_2025_10k"],
                }
            ],
            "result": "Pass on readiness, with a translational rather than exceptional verdict.",
        },
        "university_research_signals": {
            "title": "University Research",
            "summary": "Academic signals are strongest around HS biology, vitiligo/JAK clinical research, KRAS G12D and mutCALR biology.",
            "institutions": [
                {
                    "name": "The Rockefeller University",
                    "signal": "Mechanistic hidradenitis suppurativa research on epithelialized tunnels and inflammation.",
                    "company_attributable": False,
                    "field_proxy": True,
                    "evidence_ids": ["ev_019"],
                    "source_ids": ["src_pubmed_hs_rockefeller"],
                },
                {
                    "name": "Harvard Medical School / Beth Israel Deaconess Medical Center",
                    "signal": "HS biologic and small molecule therapy reviews with dermatology clinical expertise.",
                    "company_attributable": False,
                    "field_proxy": True,
                    "evidence_ids": ["ev_018"],
                    "source_ids": ["src_pubmed_hs_jak_review"],
                },
                {
                    "name": "University of Pennsylvania, UCLA and Salk Institute",
                    "signal": "Preclinical KRAS G12D pancreatic cancer research supporting the broader tractability of the target class.",
                    "company_attributable": False,
                    "field_proxy": True,
                    "evidence_ids": ["ev_017"],
                    "source_ids": ["src_pubmed_kras_preclinical"],
                },
                {
                    "name": "University of Adelaide / University of South Australia / Central Adelaide Local Health Network",
                    "signal": "Mutant calreticulin antibody IP family shows academic invention activity around the same disease biology.",
                    "company_attributable": False,
                    "field_proxy": True,
                    "evidence_ids": ["ev_026"],
                    "source_ids": ["src_pat_mutcalr_field"],
                },
            ],
        },
        "patent_signals": {
            "title": "Patents",
            "summary": "The patent signal is specific enough to indicate active formulation, method-of-use and medicinal chemistry work.",
            "families": [
                {
                    "title": "Topical treatment of vitiligo by a JAK inhibitor",
                    "publication_or_family_id": "US12233067B2 / WO2020252012A1 family",
                    "jurisdictions": ["US", "WO", "EP", "AU", "CA", "JP", "TW"],
                    "priority_date": "2019-06-10",
                    "interpretation": "Directly protects topical ruxolitinib use in vitiligo, the central Opzelura expansion use case.",
                    "evidence_ids": ["ev_021"],
                    "source_ids": ["src_pat_rux_vitiligo"],
                },
                {
                    "title": "Treatment of hidradenitis suppurativa using JAK inhibitors",
                    "publication_or_family_id": "US12280054B2",
                    "jurisdictions": ["US", "EP", "CN", "CA", "AU", "BR", "WO"],
                    "priority_date": "2018-03-30",
                    "interpretation": "Supports the dermatology JAK method-of-use estate around HS.",
                    "evidence_ids": ["ev_022"],
                    "source_ids": ["src_pat_hs_jak"],
                },
                {
                    "title": "Topical formulations of ruxolitinib with organic amine pH adjusting agent",
                    "publication_or_family_id": "US12551485B2",
                    "jurisdictions": ["US"],
                    "priority_date": "2025-04-19",
                    "interpretation": "Formulation-specific patent evidence points to product engineering, not just target biology.",
                    "evidence_ids": ["ev_023"],
                    "source_ids": ["src_pat_rux_formulation"],
                },
                {
                    "title": "Tricyclic and hetero-tricyclic compounds as inhibitors of KRAS",
                    "publication_or_family_id": "US12441727B2 / US12030883B2",
                    "jurisdictions": ["US"],
                    "priority_date": "2021-07-07",
                    "interpretation": "Representative Incyte-assigned medicinal chemistry IP around KRAS inhibitor compounds.",
                    "evidence_ids": ["ev_024", "ev_025"],
                    "source_ids": ["src_pat_kras_tricyclic", "src_pat_kras_hetero"],
                },
                {
                    "title": "Antibodies to mutant calreticulin and uses thereof",
                    "publication_or_family_id": "US20250236667A1 / WO2023108201A1",
                    "jurisdictions": ["US", "EP", "AU", "WO"],
                    "priority_date": "2021-12-13",
                    "interpretation": "Field-level mutCALR antibody IP signal from universities; included to show ecosystem formation, not as Incyte-owned IP.",
                    "evidence_ids": ["ev_026"],
                    "source_ids": ["src_pat_mutcalr_field"],
                },
            ],
            "interpretation": "Incyte's patent signal is strong for ruxolitinib/JAK and KRAS; mutCALR ownership could not be fully mapped from open sources in this run.",
        },
        "red_flags": [
            {
                "red_flag_id": "rf_001",
                "title": "Commercial concentration",
                "text": "Jakafi remains the largest single revenue base, so patent, generic and reimbursement outcomes can move the innovation economics even if the science advances.",
                "severity": "high",
                "layer": "Policy & Economics",
                "evidence_ids": ["ev_002", "ev_027"],
                "source_ids": ["src_sec_2025_10k"],
                "claim_ids": ["claim_010"],
            },
            {
                "red_flag_id": "rf_002",
                "title": "Pipeline conversion risk",
                "text": "Povorcitinib, INCA033989 and INCB161734 still need approvals, labels, payer access and prescribing uptake before they become durable commercial platforms.",
                "severity": "medium",
                "layer": "Adoption",
                "evidence_ids": ["ev_006", "ev_012", "ev_013", "ev_015"],
                "source_ids": ["src_pov_hs_2025_eadv", "src_mutcalr_eha2025", "src_mutcalr_ash2025", "src_q1_2026_release"],
                "claim_ids": ["claim_011"],
            },
            {
                "red_flag_id": "rf_003",
                "title": "Incomplete open IP census",
                "text": "Open patent searches found strong representative examples but not a clean family-level Incyte census by year, lowering IP confidence.",
                "severity": "medium",
                "layer": "IP",
                "evidence_ids": ["ev_020", "ev_026", "ev_030"],
                "source_ids": ["src_patents_justia_incyte", "src_pat_mutcalr_field", "src_pubmed_kras_patent_review"],
                "claim_ids": ["claim_007"],
            },
            {
                "red_flag_id": "rf_004",
                "title": "Clinical-readout asymmetry",
                "text": "The commercial JAK base is mature, but mutCALR and KRAS G12D evidence is still early enough that a failed or mixed Phase 3 result would materially change the thesis.",
                "severity": "medium",
                "layer": "Science",
                "evidence_ids": ["ev_013", "ev_015", "ev_016"],
                "source_ids": ["src_mutcalr_ash2025", "src_q1_2026_release", "src_nature_kras_g12d"],
                "claim_ids": ["claim_006", "claim_011"],
            },
        ],
        "watchlist": {
            "title": "What Would Change The View",
            "upgrade_signals": [
                {
                    "text": "FDA or EMA approval for povorcitinib in HS with a clean label and early launch metrics that show uptake beyond a niche population.",
                    "monitoring_source": "FDA/EMA decisions, Incyte quarterly filings, prescription data and earnings calls.",
                },
                {
                    "text": "INCA033989 Phase 3 initiation and durable molecular response data in ET or MF with manageable safety.",
                    "monitoring_source": "ClinicalTrials.gov, ASH/EHA abstracts, Incyte filings and investor presentations.",
                },
                {
                    "text": "Positive randomized Phase 3 evidence for INCB161734 in pancreatic cancer, especially if response and survival data show clear benefit over chemotherapy alone.",
                    "monitoring_source": "ClinicalTrials.gov, oncology meeting abstracts, regulatory filings and peer-reviewed publications.",
                },
            ],
            "downgrade_signals": [
                {
                    "text": "Loss of Jakafi exclusivity faster than expected or visible erosion before replacement products scale.",
                    "monitoring_source": "SEC filings, patent litigation dockets, FDA Orange Book and quarterly sales data.",
                },
                {
                    "text": "Povorcitinib safety, label, payer or efficacy issues that limit adoption relative to biologics or other JAK competitors.",
                    "monitoring_source": "FDA label, payer coverage policies, real-world prescription data and competitor launches.",
                },
                {
                    "text": "MutCALR or KRAS programs fail to reproduce early signals in larger controlled studies.",
                    "monitoring_source": "ClinicalTrials.gov, ASH/EHA/ASCO abstracts, earnings calls and trial publications.",
                },
            ],
            "cadence": [
                {
                    "frequency": "quarterly",
                    "task": "Refresh filings, earnings calls, product sales, regulatory milestones and late-stage pipeline scorecard evidence.",
                },
                {
                    "frequency": "semiannual",
                    "task": "Rebuild patent and publication proxies with a real API-based census if network access is available.",
                },
            ],
        },
        "operational_snapshot": {
            "title": "Operational Snapshot",
            "metrics": [
                {
                    "label": "2025 product revenue",
                    "value": "$4.354B",
                    "period": "2025",
                    "evidence_ids": ["ev_002"],
                    "source_ids": ["src_sec_2025_10k"],
                },
                {
                    "label": "Q1 2026 net sales",
                    "value": "$1.10B, +20% Y/Y",
                    "period": "2026-Q1",
                    "evidence_ids": ["ev_003"],
                    "source_ids": ["src_q1_2026_release"],
                },
                {
                    "label": "Late-stage breadth",
                    "value": "10 Phase 3 studies underway",
                    "period": "2026-Q1",
                    "evidence_ids": ["ev_004"],
                    "source_ids": ["src_q1_2026_release"],
                },
                {
                    "label": "Cash and marketable securities",
                    "value": "$4.0B",
                    "period": "2026-Q1",
                    "evidence_ids": ["ev_028"],
                    "source_ids": ["src_q1_2026_release"],
                },
                {
                    "label": "Five-year R&D expense",
                    "value": "$9.329B",
                    "period": "2021-2025",
                    "evidence_ids": ["ev_005"],
                    "source_ids": ["src_macrotrends_rd"],
                },
            ],
        },
        "method_notes": {
            "title": "Method Notes",
            "notes": [
                "This is a single-company absolute readiness score; no peer percentile or relative ranking was created.",
                "The deterministic scorer computes layer scores from normalized metrics, coverage ratios and confidence penalties.",
                "Publication and patent counts are representative open-source proxies because direct OpenAlex, Europe PMC and full patent-family API retrieval was unavailable in the local sandbox.",
                "Field-level science proxies are marked separately from company-attributable evidence.",
            ],
        },
        "bottom_line": {
            "title": "Bottom Line",
            "text": "Incyte has enough commercial adoption and late-stage execution to pass the breakthrough readiness gate, but the case is translational rather than exceptional until new mechanisms convert into approvals, labels and durable post-launch growth.",
            "claim_ids": ["claim_012"],
            "evidence_ids": ["ev_002", "ev_004", "ev_006", "ev_012", "ev_015", "ev_027"],
            "source_ids": ["src_sec_2025_10k", "src_q1_2026_release", "src_pov_hs_2025_eadv", "src_mutcalr_eha2025"],
        },
    }

    return {
        "schema_version": "2.1",
        "company": "Incyte Corporation",
        "ticker": "NASDAQ: INCY",
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
            "run_id": "run-company-analysis-20260512-03",
            "user_request": "Research Incyte Corporation (NASDAQ: INCY) as a single-company innovation analysis and create payload, deterministic scored JSON and a Desert Rose dashboard.",
            "time_horizon": "Five years, 2021-2025, with latest available Q1 2026 evidence where material.",
            "research_mode": "web_research_with_deterministic_scoring",
        },
        "research_context": {
            "focus_technologies": [
                "JAK/JAK1 immunology and dermatology: ruxolitinib/Jakafi, Opzelura and povorcitinib",
                "mutCALR-directed myeloproliferative neoplasm therapy: INCA033989",
                "Targeted oncology small molecules: INCB161734 KRAS G12D and adjacent oncology chemistry",
            ],
            "company_identifiers": {
                "legal_name": "Incyte Corporation",
                "ticker": "NASDAQ: INCY",
                "cik": "0000879169",
                "isin": "US45337C1027",
            },
            "source_availability": [
                {
                    "domain": "SEC filings and company materials",
                    "status": "available",
                    "note": "2025 10-K and Q1 2026 company release were available and used as primary sources.",
                },
                {
                    "domain": "publications",
                    "status": "partial",
                    "note": "Representative PubMed, PMC and journal records were available, but direct API publication-year census could not be reproduced in the local sandbox.",
                },
                {
                    "domain": "patents",
                    "status": "partial",
                    "note": "Representative Justia, PubChem and Google Patents records were available, but a complete Incyte assignee-level family-by-year census was not available.",
                },
                {
                    "domain": "regulatory and policy",
                    "status": "available",
                    "note": "FDA, EMA and SEC risk-factor sources were available for approval, reimbursement and patent/generic risk evidence.",
                },
            ],
            "search_log": [
                {
                    "query": "Incyte 2025 Form 10-K 2026 annual report R&D Jakafi Opzelura pipeline",
                    "source": "web_search",
                    "date": "2026-05-12",
                    "result_quality": "high",
                    "selected": True,
                    "selection_reason": "Primary annual filing and SEC source.",
                },
                {
                    "query": "Incyte first quarter 2026 results pipeline ruxolitinib povorcitinib mCALR",
                    "source": "web_search",
                    "date": "2026-05-12",
                    "result_quality": "high",
                    "selected": True,
                    "selection_reason": "Latest operating update and pipeline milestone source.",
                },
                {
                    "query": "Incyte INCA033989 mutant CALR antibody Phase 3 2026",
                    "source": "web_search",
                    "date": "2026-05-12",
                    "result_quality": "high",
                    "selected": True,
                    "selection_reason": "Primary company sources for mutCALR evidence.",
                },
                {
                    "query": "Google Patents Incyte povorcitinib INCB54707 patent family; site:patents.justia.com Incyte KRAS",
                    "source": "web_search",
                    "date": "2026-05-12",
                    "result_quality": "medium",
                    "selected": True,
                    "selection_reason": "Open patent records and assignee listings for representative patent evidence.",
                },
                {
                    "query": "PubMed ruxolitinib povorcitinib KRAS G12D hidradenitis suppurativa JAK inhibitors",
                    "source": "web_search",
                    "date": "2026-05-12",
                    "result_quality": "medium",
                    "selected": True,
                    "selection_reason": "Representative peer-reviewed publications and university research signals.",
                },
            ],
            "exclusions": [
                {
                    "candidate_source_or_metric": "Investor blog summaries and AI-generated earnings summaries",
                    "reason": "Not primary, potentially duplicative or lower reliability than filings and company releases.",
                },
                {
                    "candidate_source_or_metric": "Peer percentiles and comparative rankings",
                    "reason": "User explicitly requested single-company analysis without invented peer rankings.",
                },
            ],
            "judgment_calls": [
                {
                    "topic": "Publication trend proxy",
                    "decision": "Used representative source-backed publication counts rather than an exhaustive OpenAlex/PubMed census.",
                    "rationale": "Direct API retrieval was not reproducible in the local sandbox; PubMed/PMC/journal records still provided credible directional evidence.",
                    "impact": "Lowered Science coverage ratio and confidence.",
                },
                {
                    "topic": "Patent-family proxy",
                    "decision": "Used representative patent documents and families from Justia, PubChem and Google Patents instead of exhaustive family counts.",
                    "rationale": "Open sources did not provide a clean assignee-level family time series by year.",
                    "impact": "Lowered IP coverage ratio and confidence.",
                },
                {
                    "topic": "Material domains",
                    "decision": "Grouped current JAK commercial products and povorcitinib into one domain while separating mutCALR and KRAS/targeted oncology.",
                    "rationale": "This keeps the analysis focused on the 1 to 3 domains most material to future value creation.",
                    "impact": "Avoided spreading evidence across less material pipeline assets.",
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
                "rule": "normalize_growth(start_value, end_value, years, floor, cap) with analyst-reviewed representative counts",
                "reason": "Five-year directional publication activity is more informative than a one-year count, but the run records it as a proxy.",
            },
            {
                "metric_code": "patent_family_growth",
                "rule": "normalize_growth(start_value, end_value, years, floor, cap) with representative open patent documents",
                "reason": "Open patent records support directionality but not a full assignee-level family census.",
            },
            {
                "metric_code": "revenue_or_booking_evidence",
                "rule": "normalize_log(value, cap) with judgement overlay for biopharma adoption",
                "reason": "Revenue scale is nonlinear; the metric distinguishes meaningful adoption from early launch noise.",
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
    payload_path = OUT_DIR / "payload.json"
    payload_path.write_text(json.dumps(build_payload(), indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return payload_path


def build_dashboard():
    scored_path = OUT_DIR / "scored.json"
    dashboard_path = OUT_DIR / "dashboard.html"
    scored = json.loads(scored_path.read_text(encoding="utf-8"))
    data = html.escape(json.dumps(scored, ensure_ascii=True), quote=False)
    dashboard_path.write_text(
        f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Innovation Readiness Dashboard</title>
  <style>
    :root {{
      --dusty-rose: #d4a5a5;
      --clay: #b87d6d;
      --sand: #e8d5c4;
      --burgundy: #5d2e46;
      --paper: #fbf6ef;
      --surface: #f3e7dc;
      --ink: #2c2428;
      --muted: #725f65;
      --line: rgba(93, 46, 70, 0.18);
      --track: rgba(93, 46, 70, 0.13);
      --sage: #657a70;
      --warn: #9b5b4d;
      --max: 1180px;
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      color: var(--ink);
      background:
        radial-gradient(circle at 18% 0%, rgba(212, 165, 165, 0.24), transparent 28%),
        linear-gradient(180deg, var(--paper), var(--sand));
      font-family: FreeSans, Arial, Helvetica, sans-serif;
      line-height: 1.45;
    }}
    a {{ color: inherit; text-decoration-color: rgba(184, 125, 109, 0.55); text-underline-offset: 3px; }}
    .topline {{
      position: sticky; top: 0; z-index: 10;
      border-bottom: 1px solid var(--line);
      background: rgba(251, 246, 239, 0.9);
      backdrop-filter: blur(16px);
    }}
    .topline-inner {{
      width: min(var(--max), calc(100vw - 32px));
      margin: 0 auto;
      min-height: 56px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 18px;
      font-size: 13px;
      color: var(--muted);
    }}
    .brand {{ display: flex; align-items: center; gap: 10px; min-width: 0; }}
    .brand-mark {{ width: 12px; height: 12px; background: var(--dusty-rose); border: 2px solid var(--burgundy); transform: rotate(45deg); flex: 0 0 auto; }}
    .nav {{ display: flex; gap: 8px; white-space: nowrap; }}
    .nav a {{ padding: 7px 9px; border-radius: 7px; text-decoration: none; transition: background 180ms ease, color 180ms ease; }}
    .nav a:hover {{ background: rgba(232, 213, 196, 0.65); color: var(--burgundy); }}
    main {{ width: min(var(--max), calc(100vw - 32px)); margin: 0 auto; padding: 42px 0 64px; }}
    .hero {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) 320px;
      gap: 40px;
      align-items: end;
      padding: 26px 0 42px;
      border-bottom: 1px solid var(--line);
    }}
    .eyebrow {{ margin: 0 0 12px; color: var(--clay); font-size: 12px; text-transform: uppercase; font-weight: 800; letter-spacing: 0; }}
    h1, h2, h3, h4 {{ font-family: FreeSans, Arial, Helvetica, sans-serif; color: var(--burgundy); letter-spacing: 0; }}
    h1 {{ margin: 0; max-width: 800px; font-size: clamp(42px, 7vw, 82px); line-height: 0.96; font-weight: 800; }}
    .hero-sub {{ max-width: 760px; margin: 18px 0 0; color: var(--muted); font-size: clamp(16px, 2vw, 20px); }}
    .score-plate {{ border: 1px solid var(--line); background: rgba(251, 246, 239, 0.72); padding: 22px; box-shadow: 0 18px 40px rgba(93, 46, 70, 0.08); }}
    .score-number {{ font-size: 58px; line-height: 1; color: var(--burgundy); font-weight: 800; }}
    .score-number small {{ font-size: 22px; color: var(--muted); }}
    .score-label {{ margin-top: 8px; color: var(--muted); font-size: 14px; }}
    .gate {{ margin-top: 16px; display: inline-flex; align-items: center; gap: 8px; padding: 8px 10px; border: 1px solid var(--line); color: var(--burgundy); background: rgba(212, 165, 165, 0.18); font-size: 12px; font-weight: 800; }}
    section {{ padding: 34px 0; border-bottom: 1px solid var(--line); }}
    .section-head {{ display: grid; grid-template-columns: 260px minmax(0, 1fr); gap: 30px; margin-bottom: 20px; }}
    h2 {{ margin: 0; font-size: clamp(24px, 3vw, 38px); line-height: 1.05; }}
    .summary {{ margin: 0; color: var(--muted); font-size: 16px; max-width: 820px; }}
    .layer-stack {{ display: grid; gap: 16px; }}
    .layer-row {{ padding: 18px 0 19px; border-top: 1px solid var(--line); animation: rise 520ms ease both; }}
    .layer-top {{ display: grid; grid-template-columns: 190px 1fr 76px; gap: 18px; align-items: center; }}
    .layer-title {{ font-weight: 800; color: var(--burgundy); }}
    .bar-track {{ width: 100%; height: 8px; border-radius: 999px; background: var(--track); overflow: hidden; }}
    .bar-fill {{ height: 100%; border-radius: 999px; background: linear-gradient(90deg, var(--clay), var(--burgundy)); width: 0; transition: width 900ms cubic-bezier(.2,.7,.2,1); }}
    .score-mini {{ text-align: right; color: var(--burgundy); font-weight: 800; }}
    .layer-body {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; margin-top: 14px; color: var(--muted); font-size: 13px; }}
    .label {{ display: block; color: var(--clay); text-transform: uppercase; font-size: 11px; font-weight: 800; margin-bottom: 5px; }}
    .grid-2 {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px 34px; }}
    .grid-3 {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }}
    .plain-block {{ border-top: 1px solid var(--line); padding-top: 16px; transition: transform 180ms ease, background 180ms ease; }}
    .plain-block:hover {{ transform: translateY(-2px); background: rgba(251, 246, 239, 0.32); }}
    .plain-block h3, .plain-block h4 {{ margin: 0 0 8px; font-size: 18px; }}
    .plain-block p {{ margin: 0; color: var(--muted); }}
    .list {{ display: grid; gap: 12px; }}
    .bullet {{ border-top: 1px solid var(--line); padding: 13px 0 0; color: var(--muted); }}
    .chart-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 22px; }}
    .chart {{ border-top: 1px solid var(--line); padding-top: 15px; }}
    .chart h3 {{ margin: 0 0 6px; font-size: 18px; }}
    .chart p {{ margin: 0 0 14px; color: var(--muted); font-size: 13px; }}
    .spark {{ display: flex; align-items: end; gap: 7px; height: 120px; padding: 8px 0; }}
    .spark-bar {{ flex: 1; min-width: 16px; background: linear-gradient(180deg, var(--dusty-rose), var(--clay)); border-radius: 6px 6px 2px 2px; position: relative; transition: filter 180ms ease; }}
    .spark-bar:hover {{ filter: saturate(1.15) brightness(0.98); }}
    .spark-bar span {{ position: absolute; bottom: -20px; left: 50%; transform: translateX(-50%); color: var(--muted); font-size: 10px; white-space: nowrap; }}
    .two-col-list {{ columns: 2; column-gap: 34px; }}
    .source {{ break-inside: avoid; margin: 0 0 10px; color: var(--muted); font-size: 13px; }}
    .tag {{ display: inline-block; margin-top: 10px; color: var(--burgundy); font-size: 12px; font-weight: 800; }}
    .risk-high {{ color: #7f332f; }}
    .risk-medium {{ color: #8a604e; }}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    @media (max-width: 900px) {{
      .hero, .section-head, .grid-2, .grid-3, .chart-grid {{ grid-template-columns: 1fr; }}
      .layer-top {{ grid-template-columns: 1fr; gap: 8px; }}
      .score-mini {{ text-align: left; }}
      .layer-body {{ grid-template-columns: 1fr; }}
      .nav {{ display: none; }}
      .two-col-list {{ columns: 1; }}
    }}
  </style>
</head>
<body>
  <script id="scored-data" type="application/json">{data}</script>
  <div class="topline">
    <div class="topline-inner">
      <div class="brand"><span class="brand-mark"></span><span id="brandText">Innovation dashboard</span></div>
      <nav class="nav">
        <a href="#layers">Layers</a>
        <a href="#signals">Signals</a>
        <a href="#patents">Patents</a>
        <a href="#sources">Sources</a>
      </nav>
    </div>
  </div>
  <main>
    <section class="hero" id="top">
      <div>
        <p class="eyebrow" id="runMeta"></p>
        <h1 id="headline"></h1>
        <p class="hero-sub" id="subheadline"></p>
      </div>
      <aside class="score-plate">
        <div class="label">Readiness score</div>
        <div class="score-number"><span id="scoreTotal"></span><small>/25</small></div>
        <div class="score-label" id="verdict"></div>
        <div class="gate" id="gate"></div>
      </aside>
    </section>
    <section id="thesis"></section>
    <section id="layers"></section>
    <section id="signals"></section>
    <section id="commercial"></section>
    <section id="gateSection"></section>
    <section id="tech"></section>
    <section id="universities"></section>
    <section id="patents"></section>
    <section id="risks"></section>
    <section id="watchlist"></section>
    <section id="snapshot"></section>
    <section id="methods"></section>
    <section id="bottom"></section>
    <section id="sources"></section>
  </main>
  <script>
    const scored = JSON.parse(document.getElementById('scored-data').textContent);
    const dc = scored.dashboard_content;
    const src = Object.fromEntries((scored.sources || []).map(s => [s.source_id, s]));
    const esc = value => String(value ?? '').replace(/[&<>"']/g, m => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}}[m]));
    const sourceLinks = ids => (ids || []).map(id => src[id]).filter(Boolean).map(s => `<a href="${{esc(s.url)}}" target="_blank" rel="noopener">${{esc(s.title)}}</a>`).join(' | ');
    const head = (title, summary) => `<div class="section-head"><h2>${{esc(title)}}</h2><p class="summary">${{esc(summary)}}</p></div>`;
    const block = (title, text, extra = '') => `<article class="plain-block"><h3>${{esc(title)}}</h3><p>${{esc(text)}}</p>${{extra}}</article>`;

    document.getElementById('brandText').textContent = `${{scored.company}} | ${{scored.ticker}}`;
    document.getElementById('runMeta').textContent = `${{scored.research_run.research_date}} | single-company absolute analysis`;
    document.getElementById('headline').textContent = dc.hero.headline;
    document.getElementById('subheadline').textContent = dc.hero.subheadline;
    document.getElementById('scoreTotal').textContent = scored.display_total_score;
    document.getElementById('verdict').textContent = scored.verdict;
    document.getElementById('gate').textContent = scored.gate_pass ? 'Breakthrough gate: pass' : 'Breakthrough gate: not passed';

    document.getElementById('thesis').innerHTML = head(dc.thesis.title, dc.thesis.summary) +
      `<div class="list">${{dc.thesis.bullets.map(b => `<div class="bullet">${{esc(b.text)}}</div>`).join('')}}</div>`;

    document.getElementById('layers').innerHTML = head('Five-Layer Dashboard', 'Scores are deterministic outputs from scored.json. Each layer is stacked vertically with a horizontal progress bar.') +
      `<div class="layer-stack">${{scored.layers.map((l, i) => `
        <div class="layer-row" style="animation-delay:${{i * 70}}ms">
          <div class="layer-top">
            <div class="layer-title">${{esc(l.label)}}</div>
            <div class="bar-track"><div class="bar-fill" data-width="${{Math.max(0, Math.min(100, l.score / 5 * 100)).toFixed(1)}}"></div></div>
            <div class="score-mini">${{esc(l.display_score)}} / 5</div>
          </div>
          <div class="layer-body">
            <p><span class="label">Evidence</span>${{esc(l.summary)}}</p>
            <p><span class="label">Strong</span>${{esc(l.strong)}}</p>
            <p><span class="label">Missing</span>${{esc(l.missing)}} Confidence: ${{esc(l.confidence)}}.</p>
          </div>
        </div>`).join('')}}</div>`;

    const charts = dc.quantitative_signals.charts.map(chart => {{
      const seriesHtml = chart.series.map(series => {{
        const max = Math.max(...series.points.map(p => p.value), 1);
        return `<div class="chart"><h3>${{esc(chart.title)}} - ${{esc(series.label)}}</h3><p>${{esc(chart.description)}}</p><div class="spark">${{series.points.map(p => `<div class="spark-bar" title="${{esc(p.period)}}: ${{esc(p.value)}} ${{esc(series.unit)}}" style="height:${{Math.max(8, p.value / max * 100)}}%"><span>${{esc(p.period)}}</span></div>`).join('')}}</div><span class="tag">${{esc(series.unit)}}</span></div>`;
      }}).join('');
      return seriesHtml;
    }}).join('');
    document.getElementById('signals').innerHTML = head(dc.quantitative_signals.title, dc.quantitative_signals.summary) + `<div class="chart-grid">${{charts}}</div>`;

    document.getElementById('commercial').innerHTML = head(dc.commercialization_evidence.title, dc.commercialization_evidence.summary) +
      `<div class="grid-3">${{dc.commercialization_evidence.items.map(i => block(i.label, i.text)).join('')}}</div>`;

    document.getElementById('gateSection').innerHTML = head(dc.breakthrough_gate.title, dc.breakthrough_gate.summary) +
      `<div class="grid-2">${{block('Conditions met', dc.breakthrough_gate.conditions_met.map(x => x.condition).join(' '), `<span class="tag">${{esc(dc.breakthrough_gate.result)}}</span>`)}}${{block('Not yet met', dc.breakthrough_gate.conditions_not_met.map(x => x.condition).join(' '))}}</div>`;

    document.getElementById('tech').innerHTML = head(dc.technology_map.title, dc.technology_map.summary) +
      `<div class="grid-3">${{dc.technology_map.items.map(i => block(i.name, i.description, `<span class="tag">${{esc(i.maturity)}}</span>`)).join('')}}</div>`;

    document.getElementById('universities').innerHTML = head(dc.university_research_signals.title, dc.university_research_signals.summary) +
      `<div class="grid-2">${{dc.university_research_signals.institutions.map(i => block(i.name, i.signal, `<span class="tag">${{i.company_attributable ? 'company-attributable' : 'field proxy'}}</span>`)).join('')}}</div>`;

    document.getElementById('patents').innerHTML = head(dc.patent_signals.title, dc.patent_signals.summary) +
      `<div class="list">${{dc.patent_signals.families.map(f => block(f.title, `${{f.publication_or_family_id}} | ${{f.interpretation}}`, `<span class="tag">${{esc((f.jurisdictions || []).join(', '))}}</span>`)).join('')}}</div>`;

    document.getElementById('risks').innerHTML = head('Red Flags', 'Concrete reasons to keep the score below exceptional.') +
      `<div class="grid-2">${{dc.red_flags.map(r => block(r.title, r.text, `<span class="tag risk-${{esc(r.severity)}}">${{esc(r.severity)}} | ${{esc(r.layer || '')}}</span>`)).join('')}}</div>`;

    document.getElementById('watchlist').innerHTML = head(dc.watchlist.title, 'Signals that would upgrade or downgrade the readiness view.') +
      `<div class="grid-2">${{block('Upgrade', dc.watchlist.upgrade_signals.map(x => x.text).join(' '))}}${{block('Downgrade', dc.watchlist.downgrade_signals.map(x => x.text).join(' '))}}</div>`;

    document.getElementById('snapshot').innerHTML = head(dc.operational_snapshot.title, 'Current operating metrics used by the readiness score.') +
      `<div class="grid-3">${{dc.operational_snapshot.metrics.map(m => block(m.label, `${{m.value}} | ${{m.period}}`)).join('')}}</div>`;

    document.getElementById('methods').innerHTML = head(dc.method_notes.title, 'Scoring and evidence limitations.') +
      `<div class="list">${{dc.method_notes.notes.map(n => `<div class="bullet">${{esc(n)}}</div>`).join('')}}</div>`;

    document.getElementById('bottom').innerHTML = head(dc.bottom_line.title, dc.bottom_line.text);

    document.getElementById('sources').innerHTML = head('Sources', 'Sources used in payload.json and preserved in scored.json.') +
      `<div class="two-col-list">${{scored.sources.map(s => `<p class="source"><a href="${{esc(s.url)}}" target="_blank" rel="noopener">${{esc(s.title)}}</a><br>${{esc(s.publisher)}} | ${{esc(s.document_date)}} | ${{esc(s.source_type)}}</p>`).join('')}}</div>`;

    requestAnimationFrame(() => {{
      document.querySelectorAll('.bar-fill').forEach(el => {{
        el.style.width = `${{el.dataset.width}}%`;
      }});
    }});
  </script>
</body>
</html>
""",
        encoding="utf-8",
    )
    return dashboard_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--payload-only", action="store_true")
    parser.add_argument("--dashboard-only", action="store_true")
    args = parser.parse_args()

    if not args.dashboard_only:
        payload_path = write_payload()
        print(payload_path)
    if not args.payload_only:
        dashboard_path = build_dashboard()
        print(dashboard_path)


if __name__ == "__main__":
    main()
