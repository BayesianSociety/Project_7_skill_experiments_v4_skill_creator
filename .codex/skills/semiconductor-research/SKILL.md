---
name: semiconductor-research
description: Use when researching the semiconductor industry, semiconductor science, emerging chip technologies, public semiconductor companies, patents, filings, standards, and commercialization evidence. This skill supports broad discovery-first research rather than starting from a fixed technology list.
---

# Semiconductor Research

Use this skill to research the semiconductor industry from scientific, technological, commercial, and financial
perspectives. The goal is to discover important technology trends, assess their maturity, and judge whether they
are revolutionary, enabling, incremental, niche, or speculative.

## Core Principle

Start broad. Do not begin with a fixed list of technologies. Let scientific literature, company disclosures,
patents, standards, and market evidence reveal the relevant technologies.
Use multi agents to do the research.
Do not hallucinate. Do not infer commercialization from papers alone. If evidence is weak, say so clearly.

## Research Layers

### 1. Broad Technology Discovery

Begin with broad semiconductor domains:

- device physics
- logic scaling
- memory systems
- advanced packaging
- lithography
- materials science
- interconnects
- photonics
- power delivery
- thermal management
- artificial intelligence accelerators
- manufacturing equipment
- yield and reliability
- chip architecture
- electronic design automation
- supply-chain bottlenecks

Use these domains to discover emerging technologies rather than forcing the research into predefined categories.

### 2. Literature Mapping

Use the best available literature-indexing tools to map the research field.

Current examples include OpenAlex, Semantic Scholar, Crossref, Lens, Dimensions, Web of Science, and Scopus.

Use these tools to:

- find relevant papers across universities, institutes, journals, and conferences
- track publication growth over time
- identify leading institutions, authors, and research groups
- screen by citations, venue quality, recency, and institutional credibility
- build a candidate paper corpus before deeper review

OpenAlex or any equivalent tool is a discovery layer, not final proof.

### 3. Preprint And Early-Signal Discovery

Use credible preprint and institutional repositories to detect very recent research.

Current examples include arXiv, TechRxiv, institutional repositories, university lab pages, and research
institute publication pages.

Treat preprints as early signals only. They require validation through later peer review, conference acceptance,
citation uptake, experimental evidence, and institutional credibility.

### 4. Primary Scientific Review

After discovery, read the actual papers from primary or renowned sources.

Prioritize:

- Nature
- Science
- Nature Electronics
- Nature Reviews Electrical Engineering
- Institute of Electrical and Electronics Engineers journals and conferences
- International Electron Devices Meeting
- Symposium on Very Large Scale Integration Technology and Circuits
- Association for Computing Machinery architecture conferences when relevant
- imec
- leading university laboratories
- national laboratories
- recognized semiconductor research institutes

Evaluate each technology by:

- physical principle
- novelty
- experimental maturity
- wafer-scale evidence
- integration with existing manufacturing
- reliability
- thermal behavior
- yield implications
- cost implications
- design ecosystem readiness
- likely commercialization timeline

### 5. Company And Commercialization Evidence

Cross-check scientific claims against public-company evidence.

Use:

- Securities and Exchange Commission filings
- annual reports
- earnings releases
- earnings call transcripts
- investor presentations
- capital expenditure disclosures
- production ramp statements
- customer qualification statements
- supply constraint disclosures
- official company technical papers

Separate marketing language from regulated or audited disclosures.

### 6. Patent And Standards Evidence

Use patents and standards as supporting evidence.

Patent sources may include patent-office databases, Google Patents, Justia, and company patent records.

Standards sources may include JEDEC, Universal Chiplet Interconnect Express, Institute of Electrical and
Electronics Engineers, Optical Internetworking Forum, and other relevant bodies.

Patents indicate technical direction and intellectual property strategy. They do not prove commercialization.

Standards are stronger evidence because they often indicate ecosystem coordination.

### 7. Reliable Source Discovery

The source list is not fixed. Discover new reliable sources during research.

A source is more reliable if it is:

- peer-reviewed
- from a leading technical conference
- from a recognized research institute
- from a top university laboratory
- from a standards body
- from a securities regulator
- from an audited annual report
- from a company technical paper with verifiable detail

A new source may replace an older tool or repository if it is better in coverage, transparency, metadata
quality, citation quality, institutional disambiguation, freshness, reliability, or access to primary documents.

## Classification Framework

Classify technologies only after reviewing scientific, commercial, patent, and standards evidence.

Use these categories:

- **Commercially revolutionary now**: changes computing architecture, market structure, supply-chain
bottlenecks, or scaling economics and is already commercially material.
- **Major enabling upgrade**: materially improves existing technology but does not create a new architecture or
market structure by itself.
- **Early but potentially revolutionary**: strong technical and commercial logic, but adoption is still early.
- **Research-stage revolutionary**: scientifically radical, but not yet commercially proven.
- **Incremental or niche**: useful but limited in scope or confined to specialized markets.
- **Speculative**: interesting but supported by weak evidence.

Judge “revolutionary” by impact on architecture, economics, manufacturing, supply chains, and computing
capability, not by technical sophistication alone.

## Evidence Discipline

For every important claim, distinguish:

- confirmed fact
- company claim
- scientific result
- patent signal
- market interpretation
- uncertainty

Do not present publication growth as proof of technical readiness. Do not present patents as proof of product
adoption. Do not present company marketing as proof unless supported by filings, production evidence, or
customer adoption.

## Recommended Output Structure

When producing a semiconductor research report, include:

1. Methodology
2. Source map
3. Discovered technology clusters
4. Scientific evidence
5. Commercialization evidence
6. Patent and standards evidence
7. Public companies involved
8. Pros and cons by technology
9. Obstacles to commercialization
10. Market impact assessment
11. Classification: revolutionary, enabling, incremental, niche, or speculative
12. Explicit uncertainties and weak evidence areas
13. Source links

## Tool-Replacement Rule

Do not hard-code dependence on OpenAlex, arXiv, or any single source.

Use the best available tools for:

- literature mapping
- preprint discovery
- citation analysis
- primary-source validation
- company disclosure analysis
- patent analysis
- standards tracking


Save the final artefact in the current repo in a folder called public.
Use the name of the technology and a word _semiconductor.html to create the final artefact.