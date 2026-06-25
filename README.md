<div align="left">
  <a href="https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/main/readme_en.md">
    <img src="https://flagcdn.com/24x18/gb.png" alt="English" height="18"> English
  </a>
</div>

# Od nuly k produkci: LLM augmentovaný vývojový sprint

**Případová studie v AI augmentovaném učení**

---

Tento repozitář, respektive sada kazuistik ukazuje, jak při učení softwaru využít postupy z technické praxe a urychlit tak práci s AI. Obsahuje rozbory spolehlivosti modelů, metodiku pro stavbu IoT systémů, reverzní inženýrství proprietárního CAM formátu a příklady automatizace, která řeší konkrétní úkoly v reálném světě.
Cílem tohoto dokumentu není popsat vývojáře (k němu se autor ani nehlásí).

Je popsat metody – konkrétně které přístupy fungovaly, které selhaly a co o tom říkají data.


---


## Co tyto případové studie zkoumají

1. **Metodologie reverzního inženýrství proprietárního CAM formátu** — Jak z binárního souboru bez dokumentace extrahovat geometrii s přesností >99,98 %. 29 dní, 22 verzí parseru, 7 feature branchí, 5 LLM modelů včetně paid API. Od hex dumpu po cloud deployment na GCP. Klíčový objev: LightBurn ACI divergence od AutoCAD standardu. **[Reverse Engineering Case Study: Ruida VCF & LightBurn DXF](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/main/RE_CASE_STUDY_VCUTWORKS_LIGHTBURN_v2.md)**

2. Jak byly LLM nástroje používány, které konkrétní postupy produkovaly spolehlivý výstup vs. které způsobovaly regrese - **[kazuistika Gemini překlad](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/main/Kazuistika_Gemini_preklad.md)** a kazuistika z jiného repa, kde halucinace Gemini narůstaly geometrickou řadou: [RAG_indexer](https://github.com/outpost2026/RAG-indexer/blob/main/development_notes.md) - tato je ještě více ilustrativní než *gemini_preklad*.

3. Jakou roli hrály předchozí ne-softwarové zkušenosti v urychlení adopce - **[Kód, který už dávno znáte](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/main/block_05_transfer_learning_cz.md)**

4. Příběh o tom, jak automatizace přestává být jen nástrojem a stává se generátorem reálných zdrojů - **[Můj kód je lepší nákupčí než já: Jak mi Python sehnal Dell za 2 000 Kč](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/main/block_04_case_self_bootstrapping_cz.md)**

5. Součástí repozitáře je rovněž **[metodologie práce s LLM](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/main/metodika_prace_s_LLM.md)** jako user case z fyzického světa - rozhodovací procesy pro realizaci komplexního úkolu vývoje IoT telemetrie začátečníkem

6. Jak si vedlo pět nejlepších AI modelů v mé krátké praxi - **[Empirická evaluace LLM modelů v deterministickém workflow](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/main/Empiricka_evaluace_v2.md)** - Gemini stále naráží na stejné problémy

7. Jak vypadá střet s trhem — na prvním IT pohovoru v životě (případ člověka, který během přibližně 45 aktivních dní přešel z manuální profese k nabídce placeného testu od e-commerce firmy) **[Kariérní přechody v éře saturace AI (2026)](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/main/karierni_prechody_v_ere_saturace_AI_rok_2026_revidovano_v2.md)**

8. **Metodologický rámec pro B2B validaci** — Jak dokumentovat metodiku reverse inženýrství bez odhalení IP. 6-fázový proces, epistemický rámec (CLASS_A–D), golden master princip, detekční taxonomie 23 defektů ve 3 třídách, ROI kalkulace. Určeno pro B2B partnery, auditory a technologické partnery. **[Methodology & Validation Framework](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/main/METHODOLOGY_VALIDATION_FRAMEWORK.md)**


## Co bylo dosaženo

- Off-grid solární telemetrická pipeline - **predikce SOC LFP baterie** - BMS data, LAZ LiDAR geodata, pvlib solární modelování, branch **[LFP_predict_pipeline](https://github.com/outpost2026/Kazuistiky-LLM-sprint/tree/LFP_soc_predict_pipeline)**
- **GCP infrastruktura** - Podrobný popis stacku (Cloud Run, Scheduler, Firestore, BigQuery) najdete v **[GCP_ingest.md](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/GCP/gcp_stack_ingest_v3.md)** 
- ETL scraping pipeline nasazené na GCP Cloud Run s Cloud Scheduler - **[main_pipeline.py](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/GCP/transfer_dump_main.py)**
- Ingest meteorologických dat z ČHMÚ - **[meteo_miner.py](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/GCP/transfer_dump_meteo_miner.py)**
- Telegram notifikace pro všechny výstupy pipeline
- **Reverzní inženýrství formátu .VCF (Ruida/VCutWorks)** — extrakce geometrie a technologických parametrů CNC souborů s přesností >99,98 %, validováno vůči LightBurn měření. 22 verzí parseru, 7 feature branchí.
- **LightBurn DXF ACI divergence** — objev a řešení odchylky LightBurn od standardního AutoCAD mapování barev pomocí euklidovské RGB interpolace.
- **Golden master regression testing framework** — 10 testů, determinismus, baseline diff proti historickým výstupům.


Všechny systémy běží 24/7 s téměř nulovými náklady na serverless infrastruktuře.


## Pro koho to je

Vývojáři začínající s LLM asistovanými workflow. Lidé, kteří narazili na situaci, kdy "AI mi pořád dává nefunkční kód". Kdokoliv, kdo zvažuje, zda samostatné LLM augmentované učení může produkovat produkční výsledky bez formálního školení nebo týmu. Uživatelé LightBurn a CNC zařízení, kteří řeší automatizaci CAM workflow.
