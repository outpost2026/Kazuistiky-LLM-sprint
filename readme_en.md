# From Zero to Production: An LLM-Augmented Development Sprint

**A Case Study in AI-Augmented Learning**

---

This repository, or rather a set of case studies, demonstrates how to use practices from technical disciplines to accelerate software learning and work with AI. It contains reliability analyses of models, methodologies for building IoT systems, reverse engineering of a proprietary CAM format, and examples of automation solving real-world tasks.
The goal of this document is not to describe the developer (the author does not even claim to be one).

It is to describe the methods — specifically which approaches worked, which failed, and what the data says about them.

---

## What These Case Studies Examine

1. **Reverse Engineering Methodology of a Proprietary CAM Format** — How to extract geometry from a binary file without documentation with >99.98% accuracy. 29 days, 22 parser versions, 7 feature branches, 5 LLM models including paid APIs. From hex dump to cloud deployment on GCP. Key discovery: LightBurn ACI divergence from the AutoCAD standard. **[Reverse Engineering Case Study: Ruida VCF & LightBurn DXF](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/main/RE_CASE_STUDY_VCUTWORKS_LIGHTBURN_v2.md)**

2.  How LLM tools were used, which specific practices produced reliable output versus which caused regressions — **[Gemini Translation Case Study](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/main/Kazuistika_Gemini_preklad.md)** and a case study from another repository where Gemini hallucinations grew exponentially: [RAG_indexer](https://github.com/outpost2026/RAG-indexer/blob/main/development_notes.md) — this one is even more illustrative than *gemini_preklad*.

3.  What role previous non-software experience played in accelerating adoption — **[The Code You Already Know](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/main/block_05_transfer_learning_cz.md)**

4.  A story about how automation stops being just a tool and becomes a generator of real resources — **[My Code Is a Better Buyer Than Me: How Python Got Me a Dell for 2,000 CZK](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/main/block_04_case_self_bootstrapping_cz.md)**

5.  The repository also includes a **[methodology for working with LLMs](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/main/metodika_prace_s_LLM.md)** as a real-world use case — decision-making processes for executing a complex IoT telemetry development task by a beginner.

6.  How the top five AI models performed in my short practice — **[Empirical Evaluation of LLM Models in a Deterministic Workflow](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/main/Empiricka_evaluace_v2.md)** — Gemini still hits the same problems.

7.  What a first encounter with the job market looks like — at the first IT interview in a lifetime (the case of a person who transitioned from a manual profession to an offer of a paid test from an e-commerce company in approximately 45 active days) **[Career Transitions in the Era of AI Saturation (2026)](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/main/career_transitions_in_the_era_of_AI_saturation_2026_en.md)**

8.  **Methodological Framework for B2B Validation** — How to document reverse engineering methodology without revealing IP. 6-phase process, epistemic framework (CLASS_A–D), golden master principle, detection taxonomy of 23 defects in 3 classes, ROI calculation. Intended for B2B partners, auditors, and technology partners. **[Methodology & Validation Framework](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/main/METHODOLOGY_VALIDATION_FRAMEWORK.md)**

## What Was Achieved

- Off-grid solar telemetry pipeline — **LFP battery SOC prediction** — BMS data, LAZ LiDAR geodata, pvlib solar modeling, branch **[LFP_predict_pipeline](https://github.com/outpost2026/Kazuistiky-LLM-sprint/tree/LFP_soc_predict_pipeline)**
- **GCP infrastructure** — Detailed stack description (Cloud Run, Scheduler, Firestore, BigQuery) can be found in **[GCP_ingest.md](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/GCP/gcp_stack_ingest_v3.md)**
- ETL scraping pipelines deployed on GCP Cloud Run with Cloud Scheduler — **[main_pipeline.py](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/GCP/transfer_dump_main.py)**
- Weather data ingestion from CHMI — **[meteo_miner.py](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/GCP/transfer_dump_meteo_miner.py)**
- Telegram notifications for all pipeline outputs
- **Reverse engineering of the .VCF format (Ruida/VCutWorks)** — extraction of geometry and technological parameters from CNC files with >99.98% accuracy, validated against LightBurn measurements. 22 parser versions, 7 feature branches.
- **LightBurn DXF ACI divergence** — discovery and resolution of LightBurn's deviation from the standard AutoCAD color mapping using Euclidean RGB interpolation.
- **Golden master regression testing framework** — 10 tests, determinism, baseline diff against historical outputs.

All systems run 24/7 on serverless infrastructure at near-zero cost.

## Who This Is For

Developers starting with LLM-assisted workflows. People who have encountered a situation where "AI keeps giving me non-functional code." Anyone considering whether self-directed LLM-augmented learning can produce production-grade results without formal training or a team. LightBurn and CNC users looking to automate CAM workflows.
