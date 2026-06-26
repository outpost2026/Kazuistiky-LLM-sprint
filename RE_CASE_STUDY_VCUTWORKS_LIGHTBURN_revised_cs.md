# Reverse Engineering Case Study: Ruida VCF & LightBurn DXF — revidováno

**Verze:** 2.1 **|** **Datum:** 12. 6. 2026

29 dní reverzního inženýrství dvou proprietárních CAM formátů — .VCF (Ruida/VCutWorks) a DXF exportovaného z LightBurn. Výstup: parser s přesností >99,98 %, nasazený na GCP Cloud Run.

---

## 1. Klíčové objevy (odlišnosti od očekávaného chování)

### 1.1 VCF je deterministická binární serializace
Není šifrovaný ani komprimovaný. IEEE 754 double floaty (little-endian), metadata Windows-1250. 74B segmentové bloky. Identifikováno párovým hex diffem.

### 1.2 Preview simulace ≠ realita
VCutWorks Preview se **systematicky liší** od reálného času na CNC plotru. Autor manuálně odečítal hodnoty z displeje stroje — zjištěná diskrepance vedla k vývoji vlastního fyzikálního modelu kinematiky (corner slowdown, plunge overhead, lift time).

### 1.3 LightBurn DXF ≠ AutoCAD DXF
**Nejkritičtější objev.** Standardní knihovny (ezdxf) předpokládají AutoCAD ACI mapování. LightBurn používá **vlastní 32barevnou CAM paletu** — např. ACI 4 (standardně cyan) je mapován jinak. Řešení: euklidovská RGB interpolace (ΔR)²+(ΔG)²+(ΔB)² do referenční palety.

### 1.4 INSERT bloky = až 50 % geometrie
LightBurn DXF ukládá geometrii jako reference na bloky (INSERT entity). Bez block explosion (extrakce definice + transformační matice) ztratíte polovinu dat.

### 1.5 Color-to-layer bit shift mapping
Vrstvy nejsou v binární struktuře explicitní — jsou odvozeny z barevného kódování. Bez této matice nelze správně přiřadit technologické parametry (rychlost, nástroj, hloubku).

### 1.6 Falešná délka z pevného offsetu (V10)
Padding float 1.0 interpretován jako délka → kruh r=500 mm vyšel na 8 mm. Řešení: rekonstrukce délky ze souřadnic bodů, ne z pevného offsetu.

### 1.7 Regrese kružnic +41 % (V14)
Refactoring barevného mapování bez unit testů → poloměr 500→707 mm. Kružnice uložena jako 4 kvadrantové oblouky, parser četl Y-souřadnice z nesouvisejících dat. Odhaleno golden master testy.

### 1.8 SNR: 25 % kódu řídí >85 % variance
27+ výpočetních modulů klasifikováno do Tier 1–5 dle prediktivní hodnoty. Umožnilo prioritizaci.

---

## 2. Metodika (co fungovalo)

| Metoda | Popis | Proč to funguje |
|--------|-------|-----------------|
| **Pair diff** | 2 téměř identické soubory lišící se v 1 elementu → hex diff → struktura formátu | Nevyžaduje znalost formátu ani endianity |
| **Synthetic ground truth** | Trial software + známá geometrie (obdélník 2790×1200 mm, kruh r=500 mm) | Vstup s absolutní jistotou |
| **Fyzikální validace** | Reálný čas z displeje CNC vs. Preview simulace | Jediná spolehlivá reference |
| **Golden master** | Baseline JSON → pytest diff | Odhalil regresi kružnic |
| **Epistemický rámec** | Každá hodnota: empirical / calibrated / hypothesis | Transparentní nejistota |

---

## 3. Problémy a řešení (pouze unikátní)

| Problém | Příčina | Řešení |
|---------|---------|--------|
| LightBurn ACI divergence | Proprietární 32barevná paleta místo standardní | Euklidovská RGB interpolace |
| INSERT bloky neparsovány | DXF reference, ne přímá geometrie | Block explosion + transformační matice |
| Preview nespolehlivá | VCutWorks simulace ≠ realita | Fyzikální model + manuální kalibrace |
| Tool assignment conflict | Dvě logiky (ACI vs. geometrie) si odporují | ACI má prioritu, konflikt logován |
| Desynchronizace (V13) | Do-while smyčka četla padding jako elementy | Segmentové čtení s pt_count |
| PNG vizualizace bugy | Střed oblouku vs. startovní bod; barvení dle typu místo vrstvy | Oprava geometrického středu + layer-aware rendering |

---

## 4. Výsledky

| Metrika | Hodnota |
|---------|---------|
| Přesnost geometrie | >99,98 % (odchylka <0,02 %) |
| Shoda rychlostí s GUI | 100 % |
| Golden master testy | 10/10 PASS |
| Deterministické testy | 2/2 PASS |
| Predikce času | ±2–5 % oproti reálnému stroji |
| Detekovatelných defektů | 23 typů ve 3 třídách |
| Úspora na defekt | 30–200 Kč/zakázka |

---

## 5. Role LLM v RE procesu

- **5 modelů:** DeepSeek V4, Gemini, Claude, Groq, ChatGPT
- **Primární nástroj:** OpenCode CLI s API (DeepSeek + Gemini) — nikoli web UI
- **Cross-validace:** Rozdíly mezi modely odhalovaly chyby v interpretaci
- **15+ handoff JSON:** Strojově čitelný kontext mezi iteracemi
- **10 Golden Rules:** Determinismus, config>code, test-first, epistemic transparency, logging, type hints, version stamping, no magic numbers, blacklist, handoff before break

---

## 6. Implikace pro komunitu

### Pro uživatele LightBurn
- Váš DXF export **není kompatibilní** s knihovnami předpokládajícími AutoCAD ACI. Při vlastním zpracování implementujte RGB interpolaci do 32barevné LightBurn palety.
- INSERT bloky jsou standardní chování LightBurn — při parsování vždy implementujte block explosion.

### Pro uživatele VCutWorks
- Preview simulace je nespolehlivá pro predikci času. Spolehněte se na fyzické měření nebo vlastní kinematický model.
- VCF formát je čitelný — párový hex diff je dostačující metoda pro extrakci struktury.

### Pro RE vývojáře
- **Pair diff** + **clean room** = nejefektivnější cesta pro nezdokumentované binární formáty
- **Golden master testing** není akademismus — chytá regrese, které by se projevily až v produkci
- **Epistemický rámec** (empirical/calibrated/hypothesis) zabraňuje falešné jistotě u heuristik
- **LLM cross-validace** (více modelů) = levný způsob detekce špatné interpretace
- **SNR trimming** (25 % kódu → 85 % variance) = priorita před perfekcionismem

### Pro každého, kdo automatizuje CNC workflow
- Transfer learning mezi doménami (vodní paprsek → oscilační nůž) funguje — fyzikální model kinematiky je přenositelný.
- Fyzikální validace je jediná smysluplná reference. Žádná simulace nenahradí reálné měření.

---

*Dokument publikován jako otevřená kazuistika RE. Obsahuje metodologii a ponaučení — nikoli proprietární detaily formátů.*
