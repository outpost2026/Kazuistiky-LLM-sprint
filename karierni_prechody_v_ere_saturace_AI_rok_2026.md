# Kariérní přechody v éře saturace AI (2026)

## Případová studie + přenositelný návod

**Jak uspět na prvním IT pohovoru bez IT školy, bez praxe a s vědomím, že AI umí kód za vás.**

---

## Abstrakt

Reálný případ člověka, který během přibližně 45 aktivních dní přešel z manuální profese (CNC operátor)
k nabídce placeného testu od e-commerce firmy — na prvním IT pohovoru v životě.

Klíčové zjištění: V roce 2026 už není paměťová znalost programovacích jazyků bariérou vstupu do IT.
Tou bariérou je schopnost systémového myšlení, rychlé abstrakce a řízení AI nástrojů.

Tento text slouží jako:
- **Kazuistika** — co se stalo a proč to fungovalo
- **Template** — jak postupovat, pokud máte podobné kognitivní nastavení
- **Upozornění** — tato cesta není vhodná pro každého; předpoklady jsou popsány explicitně v sekci 5

---

## Poznámka k časové ose

Autor ukončil zaměstnání na konci ledna 2026. Únor byl věnován dekompresi — žádný cílený vývoj,
žádný strukturovaný sprint. Aktivní adopce začala ve druhé polovině února 2026.

Pohovor proběhl 2. dubna 2026.

Reálný časový rámec adopce: přibližně 45 aktivních dní.

Číslo "45 dní" není zaokrouhlení ani marketingový claim. Je to autorův vlastní odhad
aktivně odpracovaného období, nikoli kalendářní vzdálenost od libovolného bodu.

---

## 1. Nová realita: AI jako vyrovnávač (ale ne pro všechny)

Do roku 2026 se nástroje jako GPT, Claude, DeepSeek nebo Gemini staly běžnou součástí vývoje.
Generování kódu na úrovni junior–medior je otázkou sekund.

Důsledek: firmy přestávají platit za syntaxi. Platí za řešení problémů, za architekturu,
za schopnost vidět strukturu v chaosu.

To otevírá dveře lidem z netradičních prostředí — ale jen těm, kteří mají určité
kognitivní předpoklady. Jaké přesně, je předmětem sekce 2.

---

## 2. Klíčový determinant: schopnost přenášet principy přes domény

Zde je nutné pojmenovat věc přímo.

Existuje psychologický konstrukt zvaný fluidní inteligence (Gf) — schopnost řešit nové problémy
bez spoléhání se na naučené znalosti. Je to opak krystalizované inteligence (Gc),
která zahrnuje paměť, syntaxi a naučená fakta.

Teorie (Cattell, Carroll) předpovídá, že v prostředí kde AI přebírá Gc,
roste relativní hodnota Gf. Tato kazuistika je konzistentní s touto předpovědí.

**Je ale nutné říct co o tom víme a co nevíme.**

Co víme: autor během 45 dní zvládl přejít z nulové IT znalosti k funkčním produkčním systémům
na GCP, IoT telemetrii, predikci stavů baterie a sémantickému indexování dokumentů.
To je pozorovatelný fakt, doložitelný artefakty na GitHubu.

Co nevíme: zda je příčinou "vysoká Gf" v psychometrickém smyslu. Gf autora nebyla
standardizovaně měřena. "Vysoká Gf" je hypotéza — interpretační rámec,
který dává pozorovanému chování smysl, ale není v tomto textu verifikována.

Pozorovatelné chování, které hypotézu podporuje:
- přenos diagnostického vzorce z CNC (symptom → mechanismus → minimální oprava)
  přímo do LLM debuggingu bez explicitního "učení" tohoto přístupu
- přenos tolerančního myšlení (±0.05 mm = výmět) do datové validace (±0.75 °C = flag)
- rychlá orientace v nových doménách bez memorování základů

Tato chování jsou popsatelná a čtenář může posoudit, zda je rozpoznává u sebe.
Psychometrický konstrukt Gf k tomu není nutný.

**Praktický závěr bez přehnaných claims:**
Pokud jste v minulosti opakovaně a rychle přecházeli do nových domén a nacházeli
v nich strukturální analogie k tomu, co již umíte — tato cesta stojí za zvážení.
Pokud vaše silná stránka spočívá v systematickém, postupném učení nazpaměť,
tradiční cesta (kurz → praxe → junior role) je pravděpodobně spolehlivější.

---

## 3. Případová studie: Z CNC operátora na prvním IT pohovoru za 45 dní

### Výchozí stav (leden 2026)
- Několik let v manuálních profesích: zahradník, práce s koňmi, montáže, CNC operátor
- Žádná IT historie, žádný IT titul
- Odchod z CNC kvůli systémovému stropu — prostředí neumožňovalo optimalizaci ani smysluplnou zpětnou vazbu

### Spouštěč
Únor 2026: dekomprese po ukončení zaměstnání. Žádný cílený vývoj.
Druhá polovina února: první experimenty s LLM-asistovaným vývojem.

Klíčové rozhodnutí: nedelegovat syntaxi a učit se ji zpaměti,
ale naučit se klást otázky tak, aby LLM produkoval spolehlivý, verifikovatelný výstup.

### Co vzniklo za 45 dní

**Produkční GCP stack** — Cloud Run, Cloud Scheduler, GCS, Firestore, Telegram delivery.
Čtyři aktivní služby, šest scheduler jobů, vše serverless, provozní náklady blízko nule.

**Meteorologická ETL pipeline** — sběr dat z ČHMÚ Praha-Kbely, diferenciální zápis do GCS,
cross-validace s Open-Meteo (delta < ±0.75 °C).

**Predikce stavu baterie (SOC)** — vstup: BMS log LFP baterie + meteo data s horizon masking
z LiDAR transformace. Výstup: predikce na 5 dní, odchylka ±5 % oproti pozorované kapacitě.

**Sémantický RAG indexer** — klasifikace lokálních dokumentů do 18 typů,
kaskádové dekódování (UTF-8 / CP1250 / ISO-8859-2), produkce strukturovaného JSON manifestu.

**CAD-to-LLM pipeline** — SketchUp → COLLADA → deterministický JSON pro prostorovou analýzu LLM.
Testováno na 30 uzlech (Outpost Zone 2), 0 % nekonzistencí.

Vše zdokumentováno v pitevní knize (70+ záznamů), dostupné na GitHubu.

### Pohovor (2. dubna 2026, první IT pohovor v životě)

**Vstupní test — část 1:**
Zadání: identifikujte chybu v 5řádkovém code snippetu.

Chování autora: místo snahy o uhodnutí odpovědi okamžité přiznání limitu —
"Tohle si standardně vyhledám nebo nechám vygenerovat LLM. Pokud je toto podmínka přijetí,
chci to vědět hned, abych neplýtval vaším časem." Programátor odpověděl, že to nevadí,
a přešel na druhou část.

**Vstupní test — část 2:**
Zadání (zkráceně): navrhněte systém který z CSV/XML od dodavatelů automaticky určí celní kategorii
(CN/HS) a tím i DPH; zamyslete se nad cenou a rychlostí.

Odpověď autora (psáno ručně, přes hranice vyhrazeného boxu):
- Raw data → sémantická analýza + korelace s CN/HS nomenklaturou → klasifikační skript
- Validace: ingest → parsování → ruční kontrola vzorku → verzování
- Výstup: JSON/CSV dle potřeby
- Korekce: logy, post-mortem běhy, diferenční analýzy → ladění → finální výstup

Chyběly: confidence threshold, odhad nákladů, konkrétní technika klasifikace.
Tyto mezery firma zaregistrovala a zmínila je v závěrečné zpětné vazbě.

**Průběh pohovoru:**
Po vyhodnocení testu programátor přizval majitele firmy. Konverzace přešla
na téma reálné automatizace firemních procesů. Autor popsal meteo pipeline v logice
raw → parsing → korelace → predikce → validace výstupu → produkce.
Diskuze se posunula z testování paměti na architektonickou konzultaci.

Zpětná vazba programátora: "Velmi příjemný, ihned jste mě zaujal.
Oblast transfer learningu byla zajímavá, chtěl jsem se dozvědět víc."

Zpětná vazba majitele: "Evidentně se rychle učíte, jste schopen adaptace.
Z profilu je však zřejmá vaše potřeba autonomie a samostatnosti.
Ve firmě potřebujeme lidi, kteří věci dotahují do konce a jsou schopni
komunikace s týmem. To jsou věci, které o vás nevím a nelze je nyní posoudit."

**Výsledek:** nabídka placeného testu — firma zadá reálný automatizační problém
a zaplatí za jeho řešení v rámci výběrového řízení.

### Proč to fungovalo

Přenos vzorců přes domény. CNC diagnostika (symptom → mechanismus → minimální oprava)
se přímo zobrazila na architektuře ETL pipeline i na přístupu k debuggingu.
Toto přenesení nebylo vědomou strategií — bylo to přirozené chování
pro člověka, jehož defaultní mód je "povrch → mechanismus → struktura → implikace."

Artefakty jako důkaz. GitHub repozitáře s requirements.txt, měřitelnými výstupy
(predikce SOC ±5 %) a dokumentací rozhodnutí. Firma si repozitáře prohlédla před pohovorem.
Autor na ně odkázal v závěru pohovoru; programátor potvrdil, že se díval.

Diagnostická kultura. 70+ záznamů v pitevní knize znamená, že každá chyba
byla data, ne selhání. Tento přístup je přímo přenositelný na týmovou práci:
dokumentovaný failure mode je sdílitelné know-how, ne osobní ostuda.

Sociální přesnost. Proaktivní přiznání limitu u části 1 místo improvizace
zachránilo čas a vybudovalo důvěru. Závěrečný dotaz "jaký dojem jsem udělal?"
byl neobvyklý, ale výsledkem byla přímá, hodnotná zpětná vazba — informace
kterou většina kandidátů nikdy nedostane.

---

## 4. Přenositelné principy

Pokud rozpoznáváte u sebe chování popsaná v sekci 2
(rychlý přechod do nových domén, hledání strukturálních analogií),
a chcete podobnou cestu, použijte tento postup.

### Krok 1: Přestaňte soutěžit v paměťových znalostech
Neučte se syntaxi nazpaměť. Naučte se klást otázky LLM způsobem
který produkuje verifikovatelný výstup. Klíčová otázka není
"co je třetí parametr funkce X" ale "jak bych navrhl systém, který...".

### Krok 2: Postavte vlastní hřiště s měřitelným výstupem
Vytvořte projekt který produkuje číslo, soubor nebo alert —
ne jen kód, který "by mohl fungovat."
- IoT senzor s predikcí a kvantifikovanou odchylkou
- ETL pipeline z veřejných dat s dokumentovanou přesností
- Automatizace vlastní rutiny s logovatelným výstupem

### Krok 3: Dokumentujte jako inženýr, ne jako student
Veďte deník chyb. Každá chyba je data. Vytvářejte metodiky
(příklad: "Nejdřív raw data, pak model — nikdy naopak").
Komprimujete tím roky zkušeností do týdnů.

### Krok 4: Zviditelněte artefakty
Commitujte na GitHub. README, komentáře, requirements.txt, vzorová data.
Firmy nevěří tvrzením — věří kódu, který lze spustit.

### Krok 5: Na pohovoru pojmenujte svůj limit dříve, než ho pojmenují oni
Pokud nedokážete vyřešit testovou úlohu — řekněte to hned
a vysvětlete jak byste ji řešili v reálné práci.
To je silnější než špatná improvizace.

### Krok 6: Adresujte jejich obavu z vaší autonomie proaktivně
Pokud máte nelineární kariérní historii, majitel firmy ji uvidí.
Proaktivní věta — "Chápu, že moje samostatnost může být riziko.
Tady je, jak zajistím viditelnost a komunikaci průběhu" — je silnější
než čekání na otázku.

### Krok 7: Dotáhněte to do konce
Toto je nejtěžší část. Rychlá abstrakce vymyslí řešení za hodinu.
Dopsat dokumentaci, ošetřit chybové stavy, zabalit výsledek
do podoby kterou spustí kdokoli — to trvá déle a není to intelektuálně
vzrušivé. Trénujte exekutivní funkce. Bez nich zůstanete v 80 %.

---

## 5. Varování a limity

Tento přístup předpokládá:

1. **Schopnost přenášet principy přes domény** — viz sekce 2; pokud ji nemáte,
   tradiční cesta (kurz → praxe → junior pozice) je spolehlivější.

2. **Toleranci pro nejistotu** — žádná pevná cesta, žádná záruka výsledku.

3. **Energii a čas pro sprint** — prvních 45 dní vyžaduje vysokou intenzitu,
   ne pomalé lineární učení.

4. **Ochotu selhávat strukturovaně** — 70+ chyb v deníku není selhání,
   je to palivo. Ale musíte je dokumentovat, ne ignorovat.

5. **Schopnost dotáhnout věci do konce** — tato kazuistika končí nabídkou placeného testu,
   ne přijatou nabídkou. Výsledek testu závisí na krocích 4 a 7 výše.

---

## 6. Závěr: Co to znamená pro rok 2026

AI nesnížila důležitost inteligence — změnila, jaká inteligence se cení.
Paměťová znalost (Gc) ztrácí hodnotu. Schopnost abstrakce, přenosu principů
a systémového myšlení získává na ceně.

Lidé, kteří tato chování mají a pocházejí z netradičních prostředí,
mají nyní přímější cestu do IT — pokud se naučí AI orchestrovat, nikoli s ní soutěžit.

Tato kazuistika je jeden datový bod. Není to důkaz. Je to případ, který stojí za pozornost,
protože výsledek byl neobvyklý — a protože každý krok v něm je zdokumentovaný a ověřitelný.

---

## Příloha: Literatura a zdroje

Tato literatura nebyla v textu přímo citována. Slouží jako inspirační zázemí
pro čtenáře, kteří chtějí hlouběji porozumět konceptům, na které text narážel.

- **Cattell, R. B.** — Teorie fluidní a krystalizované inteligence (Gf/Gc);
  základ pro interpretační rámec použitý v sekci 2.
- **Carroll, J. B.** — Three Stratum Theory; rozšíření Cattellova modelu.
- **Csikszentmihalyi, M.** — Flow; optimální poměr výzvy a kapacity,
  relevantní pro sprint v podmínkách nejistoty.
- **Prigogine, I.** — Teorie disipativních struktur;
  rámec pro pochopení jak systémy rostou v podmínkách chaosu, nikoli navzdory němu.
- **Dokumentace k této kazuistice** — GitHub repozitář s pitevní knihou, metodikami a kódem.

---

*Vydáno pod licencí CC BY-NC 4.0. Sdílení a úpravy pro nekomerční účely jsou povoleny
s uvedením autora.*

*Soubor `LICENSE` v kořenovém adresáři repozitáře obsahuje plné znění licence.*

*Vytvořeno na základě reálné zkušenosti, duben 2026.*
