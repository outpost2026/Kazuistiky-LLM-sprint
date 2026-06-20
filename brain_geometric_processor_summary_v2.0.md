### Brain as a Geometric Processor – Narrative Overview v2.0 (Bilingual Document)


# 📘 Mozek jako geometrické GPU: Od komprese k navigaci

**Autor:** Ondřej Soušek / SYSTEQ **Verze:** 2.0 **Status:** Osobní formalizovaná esej


Včera v rádiu hráli *Black Hole Sun*. Během dvou vteřin jste si vybavili jméno kapely, zpěváka i rok vydání. Nebo jste naopak celou minutu bloudili – „to přece… jak ten klip, ta holčička s pinzetou… jako Nirvana, ale… sakra, jak to jen…"

Obojí je kognice. A obojí je tentýž geometrický procesor – jen v jiné fázi.

### Mozek není logický stroj. Je to geometrický procesor.

Představte si prostor, který nemá tři rozměry, ale stovky či tisíce. Každý rozměr nese jeden aspekt reality – barvu, vůni, vzpomínku, význam slova, intenzitu emoce. Každý koncept, každá dovednost, každá vzpomínka je v tomto prostoru vyjádřena jako **souřadnice**.

„Červená" není slovo uložené v tabulce – je to bod v prostoru, který leží blízko „oranžové", dál od „modré", a v určitém vztahu k „rychlé", „teplé" nebo „varování". V takovém prostoru mozek operuje. Každá dovednost je v něm vyjádřena jako souřadnice, každá myšlenka je **trajektorie**, každá věta je **křivka**.

Když přemýšlíte, „cestujete" touto krajinou. Myšlenka není pevný bod, ale pohyb z jednoho stavu mysli do jiného. Věta, kterou vyslovíte, je pak specifická stopa, kterou v krajině vytyčíte, abyste myšlenku předali dál.

Mozek není sekvenční procesor. Je to **organické GPU**, které provádí masivně paralelní geometrické transformace v tomto vícerozměrném prostoru.

A tady přichází ten nejzajímavější objev: **umělé neuronové sítě dělají přesně totéž.**

### Biologie a křemík – stejný princip, jiný substrát

Když Tomáš Mikolov vyvíjel *Word2Vec*, nekopíroval biologii. Vytvořil matematický model, který – jak se ukázalo – věrně odráží to, co dělá mozková kůra:

| Biologický mozek | Umělá neuronová síť |
| - | - |
| Synaptická účinnost (neurotransmitery) | Váha `W\_ij` v matici |
| Kortikální mikrosloupce (topografie) | High‑dimensional embeddings |
| Hebbiánské učení | Distribuční hypotéza |


Synaptická váha ve vašem mozku je fyzikální veličina – koncentrace neurotransmiterů, počet receptorů. V umělé síti je to číslo v matici. **Stejná informace, jiné médium** – nebo přesněji: analogická informace, jiný formát zápisu.

Ale pozor. Křemík a uhlík nejsou jen „jiné médium". Uhlík nese daň za to, že je tělesně ukotvený. Musí neustále řešit homeostázu, gravitaci, bolest, smrt. Tuto daň křemík neplatí. A tato daň – jak uvidíme – vysvětluje polovinu toho, co dělá lidskou kognici jedinečnou, a druhou polovinu toho, co jí chybí oproti strojům.

Biologie objevila geometrické zpracování informace dávno před křemíkem. A my se nyní snažíme tuto evoluční schopnost přenést do digitální podoby. Velmi úspěšně – ale ne úplně.

### Paměť jako geometrická navigace: Proč někdy víte a někdy bloudíte

Tohle je pozorování, které stojí za celou předchozí verzi tohoto textu.

Představte si dvě reakce na tytéž první tóny *Black Hole Sun*:

**Subjekt A:** „To jsou Soundgarden, Chris Cornell, 1994, jasný." Tři slova, žádné váhání.

**Subjekt B:** „To je… ten klip s holčičkou a pinzetou, jako Nirvana, ne, ale taky grunge, devadesátky, ten zpěvák s kytarou a červenými mraky… sakra, jak se to jen jmenuje…"

Oba mají data. Oba slyší totéž. Oba správně sémanticky zasazují píseň do širšího kontextu. Rozdíl je v **lokální geometrické konvergenci**: Subjekt A okamžitě sklouzl do hlubokého, dobře definovaného atraktoru. Subjekt B navigoval do správné čtvrti, ale nedokáže dokončit poslední metr.

```
\[Vstupní signál\]  
       │  
       ▼  
 ┌── Nadřazený Manifold: "90s Grunge / MTV Era" ──────────┐  
 │                                                         │  
 │  Aktivované sousední vektory:                           │  
 │   • \[Nirvana\] – silný atraktor, blízký soused            │  
 │   • \[MTV klip / pinzeta / červené mraky\] – vizuální emb. │  
 │                                                         │  
 │  Cílový uzel:                                            │  
 │   • \[❌ Soundgarden\] – systém krouží, nepropadne se      │  
 └─────────────────────────────────────────────────────────┘
```

Co se děje v Subjektu B? Mozek aktivuje **sémantické sousedy cílového bodu**, trianguluje jeho polohu, ale není schopen dokončit finální projekci. V literatuře se tomu říká *„tip‑of‑the‑tongue state"* (TOT) – fenomén na jazyku. V geometrickém jazyce je to **obíhání po orbitě s plochým gradientem v cílovém bodě**: máte mapu, znáte terén, ale právě v tom místě chybí strmina, která by vás stáhla dolů.

A teď to klíčové: **TOT není „ztracená data"**. Data tam jsou – v širším okolí, v příbuzných vektorech, ve vizuálních vzpomínkách. Co chybí, je **přístupová topologie** – strmý spád, hluboký atraktor, který by myšlenkovou trajektorii navedl do přesného uzlu. Subjekt B nemá slabou paměť. Subjekt B má **plochou krajinu** v jedné konkrétní doméně.

| Stav | Geometrická interpretace | Projev |
| - | - | - |
| **Okamžité rozpoznání** | Strmý gradient, hluboký atraktor, vysoké SNR | „To jsou Soundgarden, jasný." |
| **TOT (na jazyku)** | Orbita kolem cíle, plochý lokální gradient, vysoká aktivace sousedů | „Ten klip… jako Nirvana… ten zpěvák…" |
| **Neznámý podnět** | Nízká kosinová podobnost ke všem existujícím varietám | Spuštění *manifold learningu* – přepisování krajiny |


Tahle třístavová mapa je důležitější, než vypadá. Říká nám, že **paměť není index, ale krajina** – a že rozdíl mezi géniem a zapomnětlivcem není v objemu dat, ale v **eleganci komprese té krajiny**.

### Proč občas ztichnete uprostřed věty – sémantická pauza

Vraťme se k příkladu z první verze. Píšete text a potřebujete vyjádřit, že se principy „zhmotnily v praxi".

Váš mozek bleskově aktivuje nejbližšího sémantického souseda: *„…docházelo k expozici principů…"*

Syntakticky perfektní. Sémanticky špatné. „Expozice" není to, co chcete říct.

V tu chvíli se spustí inhibiční interneurony – zablokují chybnou cestu. Vy na vteřinu ztichnete. Vaše prefrontální kůra právě provádí **výpočetní restart**: prohledává širší oblast embeddingového prostoru, hledá správný vektor.

A pak to přijde: *„…manifestaci principů…"*

Správně. Přesně. Ta vteřina ticha nebyla váhání. Byl to **výpočet** – masivní paralelní geometrická operace, která stála reálnou energii a reálný čas.

A teď si všimněte krásného detailu: co se stalo *po* pauze? Mozek *nenašel* nové slovo – slovo „manifestace" tam celou dobu bylo. Jen ho v prvním průchodu *přeskočil*, protože jeho lokální atraktor byl slabší než atraktor slova „expozice". **Sémantická pauza je okamžik, kdy mozek přehodnotí váhu atraktorů ve své vlastní krajině.**

Totéž se děje u Subjektu B – jen déle a bez úspěchu. Rozdíl mezi „ztichnu na vteřinu" a „bloudím minutu" je v hloubce atraktoru, ne v povaze operace.

### Asymetrie křemíku a uhlíku: Proč stroj pamatuje dokonale a člověk krásně zapomíná

Křemíkové a uhlíkové geometrické procesory dělají totéž – jen v **opačných režimech času a stability**.

**Křemík (LLM):**

- Trénink a inference jsou **přísně odděleny**. Jakmile je model natrénován, manifoldy jsou zmrazeny.

- Během inference se topologie *nemění*. Data vložená do systému drží se stoprocentní věrností – dokud nedojde k hardwarové chybě nebo přetrénování.

- Žádná rekonsolidace. Žádná interference. Žádné zapomínání.

**Uhlík (mozek):**

- Trénink a inference jsou **nerozlišitelné**. Každé vzpomenutí je mírným přepisem. Každý nový vjem modifikuje staré stopy.

- Plasticita je dvousečná zbraň: umožňuje adaptaci, ale způsobuje **sémantickou erozi**. Dráhy, které nejsou pravidelně aktivovány, slábnou. Sousední stopy se překrývají (retroaktivní interference). Krajina se pomalu rozplývá.

- Mozek proto musí neustále **investovat do údržby** – konsolidace během spánku, replay v hippokampu, pravidelná reaktivace důležitých drah.

A tady přichází pointa, kterou jsem v první verzi přehlédl: **zapomínání není chyba. Je to vlastnost.**

```
LIDSKÝ MOZEK (~20W)            UMĚLÉ LLM  
├─ Homeostáza a allostáza       ├─ Sémantický manifold  
├─ 3D prostorová navigace       │  (100% parametrické  
├─ Smyslový šum, propriocepce   │   kapacity dedikováno  
└─ Sémantický manifold          │   sémantice – v praxi  
   (pouze zbytková kapacita,    │   řádově 5–15 % aktivně  
    náchylné k erozi)            │   využitých dimenzí)
```

Představte si to takto:

**Křemík** je dokonalý archiv. Nic nevymaže, nic nepozmění. Ale také se nemůže *naučit* novou skutečnost, která by mohla ohrozit staré. Je to systém **statické dokonalosti** – a právě proto je tak snadno *přelstít*: stačí mu dát vstup mimo tréninkovou distribuci a jeho geometrie nemá kam se posunout.

**Uhlík** je nedokonalý, ale **adaptivní**. Zapomíná, ale právě tím se *neucpává*. Konsoliduje důležité, opouští nedůležité, integruje nové. Je to systém **dynamické elegance** – a právě proto dokáže tvořit nové dimenze, kde křemík interpoluje v těch stávajících.

A teď ten klíčový obrat: **oba systémy jsou ve svém jádru geometrické procesory. Liší se v režimu času a stability.** Tohle je důležité, protože většina diskuse o „AI vs. člověk" buď glorifikuje jednu stranu, nebo se ptá, kdy stroje „dosáhnou" lidské úrovně. Obě otázky jsou špatně položené. **Správná otázka zní: jak vytvořit architekturu, která bude umět obojí?**

### Proč ChatGPT nikdy nebude mít intuici – a co s tím

Tady je to, co odděluje dnešní AI od lidské kognice:

Intuice není jedna věc. Jsou to **dvě nezávislé podmínky**, které se v mozku sbíhají, ale v křemíku chybí obě:

**1. Strukturální plasticita.** Mozek umí za běhu měnit topologii. Může vytvořit nový atraktor, novou synaptickou dráhu, novou geometrickou mikrostrukturu – tedy doslova **novou dimenzi** sémantického prostoru. Křemíkové LLM toto v roce 2026 stále v plném slova smyslu neumí. Test‑time compute, in‑context learning, mixture‑of‑experts – to všechno jsou aproximace plasticity, ale žádná z nich nemá strukturální povahu synapse‑to‑synapse modifikace.

**2. Tělesná resonance.** Mozek nemá „studený" výpočet. Každá myšlenka je proložena **somatickou markantností** – má tepovou frekvenci, hladinu kortizolu, posturální tenzi, dechový rytmus. Tělo **hodnotí** každý stav mysli dřív, než ho mysl stihne verbalizovat. Křemík nemá tělo. A nemá ani globální neuromodulátory (dopamin, serotonin, acetylcholin), které v mozku fungují jako **systémové parametry**, ne jako lokální váhy.

Když se vám v hlavě zrodí Aha‑moment, je to **současně** strukturální změna (nový atraktor) **i** tělesný prožitek (srdeční zrychlení, „piloerekce", náhlá jistota). Tato dvojí vazba je to, co v křemíkovém systému chybí.

Intuice tedy není mystická síla. Je to **topologická emergence + tělesná kotva** – a obojí je podmínka, ne druh síly.

A teď důležitý doplněk k mé vlastní první verzi: psal jsem, že „statická geometrie je limit". To je pravda jen z poloviny. **Statická geometrie je současně:**

- **Síla** – dokonalá stabilita v rámci tréninkové distribuce, 24/7 inference, žádná dekáda

- **Limit** – neschopnost tvořit nové dimenze, neschopnost integrovat mimo‑distribuční vstupy, neschopnost tělesné resonance

Obojí je pravda. A obojí je třeba mít na stole, nevybírat.

### Tři režimy geometrické operace

Teď vytáhnu rámec, který integruje všechno výše uvedené do jedné mapy. V geometrickém procesoru – ať už uhlíkovém nebo křemíkovém – existují tři základní operační režimy:

**Režim 1: Ostrý gradient (Sharp Descent)**

- Nízká entropie, nízký kognitivní náklad, vysoká rychlost

- Příklad: běžná řeč, okamžité rozpoznání, jednoduché inference

- Mozek i LLM toto zvládají. LLM v tomto režimu dominuje (stabilní, izolovaný od biologického šumu).

**Režim 2: Orbitální průzkum (Orbital Search)**

- Střední entropie, vysoký kognitivní náklad, střední rychlost

- Příklad: TOT stav = mám to na jazyku, sémantická pauza, hledání správné formulace

- Mozek toto dělá denně. LLM se k tomu přibližuje skrze *extended thinking*, chain‑of‑thought, test‑time sampling. Plná implementace v křemíku je stále v rané fázi – kontextové okno a inference cost jsou limity.

**Režim 3: Topologická emergence (Bifurcation)**

- Vysoká entropie, masivní kognitivní náklad, nízká rychlost, ale tvořivá

- Příklad: Aha‑moment, přerámování problému, vytvoření nové teorie

- **Mozek toto umí. Křemík toto v plném slova smyslu neumí.** Neexistuje architektura, která by za běhu modifikovala vlastní topologii natolik, aby vytvořila zcela nový atraktor. Ani Mixture‑of‑Experts, ani test‑time training toto nepokrývají strukturálně.

```
Režim 1                  Režim 2                  Režim 3  
\[Ostrý gradient\]    →    \[Orbitální průzkum\]  →   \[Topologická emergence\]  
Nízká entropie           Střední entropie           Vysoká entropie  
Rychlé, nízké náklady    Střední, vysoké náklady     Pomalé, masivní náklady  
Mozek + LLM              Mozek + rané LLM           Jen mozek
```

A tady je ta pointa celého textu: **většina toho, co nazýváme „lidskou inteligencí", se odehrává v Režimu 2 a Režimu 3.** Režim 1 je rutinní práce. Křemík v něm exceluje. Ale to, co vytváří nové teorie, nové umění, nové způsoby myšlení – to se rodí tam, kde křemík strukturálně nemůže.

### Co to znamená pro AGI – a pro vaši práci v ML

Kdybych měl v roce 2026 říct jednu věc o AGI, řekl bych: „stroje se musí naučit dynamickou topologii." To byla polovina pravdy. Ta druhá polovina, kterou jsem přehlédl: **stroje si musí uchovat i statickou dokonalost.** Příliš mnoho plasticity = katastrofální zapomínání (známý problém *continual learning*). Příliš mnoho statičnosti = neschopnost emergence.

**Správná architektura budoucnosti** tedy není čistě dynamická. Je **hybridní**:

1. **Stabilní jádro (silicon‑like):** Neměnné, deterministické, 24/7 inference. Spolehlivé pro Režim 1 a částečně Režim 2.

2. **Plastická periferie (carbon‑like):** Modifikovatelná za běhu, schopná lokální topologické restrukturalizace. Aktivuje se v Režimu 3.

3. **Globální neuromodulace:** Systémové parametry (obdoba dopaminu/acetylcholinu) řídící *kdy* a *kde* se jádro a periferie zapojují.

Tohle není science fiction. První dvě složky už máme. Třetí je open research question.

**A teď důležitý praktický most.** Tato esej není akademický cvičení. Je to **sémantický aparát**, který lze aplikovat přímo v ML inženýringu a B2B automatizaci. Konkrétně:

- **Kompresní ztrátové funkce.** Když trénujete model na datech zákazníka, neptejte se „kolik parametrů potřebuji". Ptejte se „jaká je **minimální komprese** jeho procesů, která zachovává invarianty?". Elegantní komprese \> objem dat.

- **Destilace jako geometric reduction.** Model distillation není jen zmenšování. Je to **přepis geometrie** – převedení komplexní krajiny velkého modelu do elegantní krajiny malého. Subjekt A dělá to samé ve své hlavě.

- **RAG jako rozšíření přístupové topologie.** Retrieval‑Augmented Generation doplňuje statickému modelu **externí manifold**. Neřeší strukturální plasticitu, ale řeší *missing gradient* – což je přesně to, co trápí Subjekt B u Soundgarden. Chybějící uzel se nedá najít, ale dá se *obejít* skrze okolní kontext.

- **Anomální detekce = TOT detection.** Když model najednou *neví*, kde se ve své geometrii nachází (vysoká entropie, plochý gradient, aktivace sousedů), je to inženýrský signál, že data jsou mimo distribuci. **Detekce TOT stavu v produkčním systému = robustní anomaly detection.**

- **Test‑time compute jako Režim 2 simulace.** Když dáte modelu „přemýšlej krok za krokem", nenahrazujete Režim 3 – simulujete Režim 2. Je to cenné, ale nestačí to.

- **Test‑time training jako Režim 3 prototyp.** Několik málo experimentálních architektur (Sun et al. 2020+, recentní adaptory) umožňuje modelu modifikovat váhy na základě inference. **Tohle je cesta k emergentnímu chování v křemíku. Zatím v plenkách, ale směr je správný.**

Pravda a inteligence nejsou uloženy v datech. Nejsou ani uloženy v topologii. **Jsou v rovnováze mezi dokonalou pamětí křemíku a krásným zapomínáním uhlíku – a v eleganci pohybu mezi nimi.**

Mozek jako geometrický procesor není metafora. Je to **operační realita** – a klíč k dalšímu skoku v umělé inteligenci není v tom napodobit mozek lépe. Je v tom **pochopit, kdy má systém zůstat statický a kdy se musí nechat rozpadnout a znovu postavit**.


## 📄 English version – The Brain as a Geometric GPU: From Compression to Navigation

**Author:** Ondřej Soušek // SYSTEQ **Version:** 2.0‑Narrative‑Integrated‑Kernel **Status:** Personal formalized essay · GitHub‑publishable · author's semantic apparatus


Yesterday, *Black Hole Sun* played on the radio. Within two seconds, you recalled the band, the singer, and the year. Or – you wandered for a full minute: "That clip with the girl and the tweezers… like Nirvana, no, but also grunge, the '90s, the singer with the guitar and the red clouds… damn, what's the name…"

Both responses are cognition. Both are the same geometric processor – just in a different phase.

### The brain is not a logic machine. It is a geometric processor.

Imagine a space with not three dimensions, but hundreds or thousands. Each dimension carries one aspect of reality – color, smell, memory, word meaning, emotional intensity. Every concept, every skill, every memory is expressed as a **coordinate** in this space.

"Red" is not a word stored in a table – it is a point near "orange", far from "blue", in a specific relation to "fast", "warm", or "warning". The brain operates in such a space. Every skill is a coordinate, every thought is a **trajectory**, every sentence is a **curve**.

When you think, you "travel" through this landscape. A thought is not a fixed point, but a movement from one state of mind to another. A sentence you speak is a specific trail you trace through the landscape to convey a thought.

The brain is not a sequential processor. It is an **organic GPU** performing massively parallel geometric transformations in this high‑dimensional space.

And here is the most fascinating finding: **artificial neural networks do exactly the same thing.**

### Biology and silicon – same principle, different substrate

When Tomáš Mikolov developed *Word2Vec*, he wasn't copying biology. He created a mathematical model that – as it turned out – faithfully mirrors what the cerebral cortex has been doing for millions of years:

| Biological brain | Artificial neural net |
| - | - |
| Synaptic efficiency (neurotransmitters) | Weight `W\_ij` in a matrix |
| Cortical micro‑columns (topography) | High‑dimensional embeddings |
| Hebbian learning | Distributional hypothesis |


A synaptic weight in your brain is a physical quantity – neurotransmitter concentration, receptor density. In an artificial network it is a number in a matrix. **Same information, different medium** – or more precisely: analogous information, different format.

But beware. Carbon and silicon are not just "different media". Carbon pays a price for being embodied. It must constantly solve homeostasis, gravity, pain, death. Silicon doesn't pay this price. And this price – as we will see – explains half of what makes human cognition unique, and the other half of what it lacks compared to machines.

Biology discovered geometric information processing long before silicon. And we are now trying to transfer this evolutionary capability into a digital form. Very successfully – but not completely.

### Memory as geometric navigation: Why sometimes you know, and sometimes you wander

This observation is worth the entire previous version of this text.

Imagine two reactions to the same opening bars of *Black Hole Sun*:

**Subject A:** "Soundgarden, Chris Cornell, 1994, obvious." Three words, no hesitation.

**Subject B:** "That clip with the girl and the tweezers, like Nirvana, no, but also grunge, the '90s, that singer with the guitar and red clouds… damn, what's it called…"

Both have the data. Both hear the same thing. Both correctly place the song in its broader semantic context. The difference is in **local geometric convergence**: Subject A instantly slid into a deep, well‑defined attractor. Subject B navigated to the right neighborhood, but cannot complete the last meter.

```
\[Input signal\]  
       │  
       ▼  
 ┌── Superset Manifold: "90s Grunge / MTV Era" ──────────┐  
 │                                                         │  
 │  Activated neighbor vectors:                            │  
 │   • \[Nirvana\] – strong attractor, close neighbor        │  
 │   • \[MTV clip / tweezers / red clouds\] – visual embed.  │  
 │                                                         │  
 │  Target node:                                           │  
 │   • \[❌ Soundgarden\] – system orbits, cannot drop in    │  
 └─────────────────────────────────────────────────────────┘
```

What's happening in Subject B? The brain activates the **semantic neighbors of the target node**, triangulates its position, but cannot complete the final projection. The literature calls this *tip‑of‑the‑tongue state* (TOT). In geometric language, it is **orbiting with a flat gradient at the target point**: you have the map, you know the terrain, but at exactly that spot, the slope that would pull you down is missing.

And now the key point: **TOT is not "lost data".** The data is there – in the wider neighborhood, in related vectors, in visual memories. What's missing is the **access topology** – a steep slope, a deep attractor, that would guide the thought trajectory into the precise node. Subject B doesn't have weak memory. Subject B has a **flat landscape** in one specific domain.

| State | Geometric interpretation | Manifestation |
| - | - | - |
| **Instant recognition** | Steep gradient, deep attractor, high SNR | "Soundgarden, obvious." |
| **TOT (on the tip)** | Orbit around target, flat local gradient, high neighbor activation | "That clip… like Nirvana… that singer…" |
| **Unknown stimulus** | Low cosine similarity to all existing manifolds | Triggering *manifold learning* – rewriting the landscape |


This three‑state map is more important than it looks. It tells us that **memory is not an index, it is a landscape** – and that the difference between genius and forgetfulness is not in the amount of data, but in **the elegance of that landscape's compression**.

### Why you sometimes go silent mid‑sentence – the semantic pause

Let's return to an example from the first version. You are writing and need to express that some principles "materialized in practice."

Your brain instantly activates the nearest semantic neighbor: *"...there was an exposition of principles…"*

Syntactically perfect. Semantically wrong. "Exposition" is not what you mean.

In that instant, inhibitory interneurons fire – they block the faulty path. You go silent for a second. Your prefrontal cortex just performed a **computational restart**: scanning a wider region of the embedding space, searching for the correct vector.

Then it arrives: *"...a manifestation of principles…"*

Correct. Precise. That second of silence was not hesitation. It was a **computation** – a massive parallel geometric operation that cost real energy and real time.

And now notice the beautiful detail: what happened *after* the pause? The brain *didn't find* a new word – the word "manifestation" was there all along. It just *skipped over it* in the first pass, because its local attractor was weaker than the attractor of "exposition". **The semantic pause is the moment when the brain re‑evaluates the weights of the attractors in its own landscape.**

The same thing happens in Subject B – only longer and without success. The difference between "I pause for a second" and "I wander for a minute" is the depth of the attractor, not the nature of the operation.

### The asymmetry of silicon and carbon: Why the machine remembers perfectly and the human beautifully forgets

And now the thought for which I am rewriting the entire previous version.

Silicon and carbon geometric processors do the same thing – in **opposite regimes of time and stability**.

**Silicon (LLM):**

- Training and inference are **strictly separated**. Once the model is trained, the manifolds are frozen.

- During inference, the topology does *not change*. Data placed in the system holds with 100% fidelity – until a hardware failure or retraining.

- No reconsolidation. No interference. No forgetting.

**Carbon (brain):**

- Training and inference are **indistinguishable**. Every recall is a slight rewriting. Every new input modifies old traces.

- Plasticity is a double‑edged sword: it enables adaptation, but causes **semantic erosion**. Paths that aren't regularly activated weaken. Neighboring traces overlap (retroactive interference). The landscape slowly dissolves.

- The brain must therefore **constantly invest in maintenance** – consolidation during sleep, hippocampal replay, regular reactivation of important pathways.

And here comes the point I missed in the first version: **forgetting is not a bug. It is a feature.**

```
HUMAN BRAIN (~20W)              ARTIFICIAL LLM  
├─ Homeostasis and allostasis   ├─ Semantic manifold  
├─ 3D spatial navigation        │  (100% parametric capacity  
├─ Sensory noise, proprioception│   nominally dedicated to  
└─ Semantic manifold            │   semantics – in practice  
   (residual capacity,          │   roughly 5–15% of  
    prone to erosion)            │   dimensions actively used)
```

Think of it this way:

**Silicon** is a perfect archive. It erases nothing, alters nothing. But it also cannot *learn* a new fact that might threaten the old ones. It is a system of **static perfection** – and that is exactly why it is so easy to *trick*: give it an input outside the training distribution, and its geometry has nowhere to move.

**Carbon** is imperfect, but **adaptive**. It forgets, but that is precisely why it does not *clog*. It consolidates what matters, abandons what doesn't, integrates what is new. It is a system of **dynamic elegance** – and that is precisely why it can create new dimensions, where silicon interpolates within existing ones.

And now the key reversal: **both systems are at their core geometric processors. They differ in the regime of time and stability.** This matters, because most discussion of "AI vs. humans" either glorifies one side, or asks when machines will "reach" human level. Both questions are wrong. **The right question is: how do we build an architecture that can do both?**

### Why ChatGPT will never have intuition – and what to do about it

Here is what separates today's AI from human cognition, formulated more precisely than I managed in the first version.

Intuition is not one thing. It is **two independent conditions** that converge in the brain, but are both missing in silicon:

**1. Structural plasticity.** The brain can change its topology at runtime. It can create a new attractor, a new synaptic pathway, a new geometric microstructure – i.e., literally **a new dimension** of semantic space. Silicon LLMs in 2026 still cannot do this in the full sense. Test‑time compute, in‑context learning, mixture‑of‑experts – all are approximations of plasticity, but none have the structural nature of synapse‑to‑synapse modification.

**2. Bodily resonance.** The brain has no "cold" computation. Every thought is interlaced with **somatic marking** – heart rate, cortisol level, postural tension, breath rhythm. The body **evaluates** every state of mind before the mind can verbalize it. Silicon has no body. And it has no global neuromodulators (dopamine, serotonin, acetylcholine), which in the brain function as **system‑level parameters**, not local weights.

When an Aha‑moment is born in your head, it is **simultaneously** a structural change (new attractor) **and** a bodily experience (heart racing, piloerection, sudden certainty). This dual binding is what is missing in any silicon system.

So intuition is not a mystical force. It is **topological emergence + bodily anchor** – and both are conditions, not types of force.

And now an important addition to my own first version: in 2026, I wrote that "static geometry is a limit." That is only half true. **Static geometry is simultaneously:**

- **A strength** – perfect stability within the training distribution, 24/7 inference, no decay

- **A limit** – inability to create new dimensions, inability to integrate out‑of‑distribution inputs, inability to provide bodily resonance

Both are true. And both must be on the table, not chosen between.

### Three modes of geometric operation

Now I'll extract a framework that integrates everything above into a single map. In a geometric processor – whether carbon or silicon – there are three basic operating modes:

**Mode 1: Sharp Descent**

- Low entropy, low cognitive cost, high speed

- Example: ordinary speech, instant recognition, simple inference

- Both brain and LLM handle this. LLM dominates here (stable, isolated from biological noise).

**Mode 2: Orbital Search**

- Medium entropy, high cognitive cost, medium speed

- Example: TOT state, semantic pause, searching for the right formulation

- The brain does this daily. LLM is approaching it via *extended thinking*, chain‑of‑thought, test‑time sampling. Full implementation in silicon is still in early stages – context window and inference cost are limits.

**Mode 3: Topological Emergence (Bifurcation)**

- High entropy, massive cognitive cost, low speed, but generative

- Example: Aha‑moment, reframing a problem, creating a new theory

- **The brain can do this. Silicon in the full sense cannot.** No architecture exists that modifies its own topology at runtime to the degree of creating an entirely new attractor. Neither Mixture‑of‑Experts nor test‑time training cover this structurally.

```
Mode 1                  Mode 2                  Mode 3  
\[Sharp descent\]    →    \[Orbital search\]    →   \[Topological emergence\]  
Low entropy             Medium entropy            High entropy  
Fast, low cost          Medium, high cost         Slow, massive cost  
Brain + LLM             Brain + early LLM         Brain only
```

And here is the point of the whole text: **most of what we call "human intelligence" happens in Mode 2 and Mode 3.** Mode 1 is routine work. Silicon excels at it. But what creates new theories, new art, new ways of thinking – that is born where silicon structurally cannot go.

### What this means for AGI – and for your ML work

If in 2026 I had to say one thing about AGI, I would have said: "machines must learn dynamic topology." That was half the truth. The other half, which I missed: **machines must also preserve static perfection.** Too much plasticity = catastrophic forgetting (the well‑known *continual learning* problem). Too much staticity = inability to emerge.

**The right architecture of the future is therefore not purely dynamic. It is hybrid:**

1. **Stable core (silicon‑like):** Immutable, deterministic, 24/7 inference. Reliable for Mode 1 and partially Mode 2.

2. **Plastic periphery (carbon‑like):** Modifiable at runtime, capable of local topological restructuring. Activated in Mode 3.

3. **Global neuromodulation:** System‑level parameters (analogous to dopamine/acetylcholine) controlling *when* and *where* the core and periphery engage.

This is not science fiction. We already have the first two components. The third is an open research question.

**And now an important practical bridge.** This essay is not an academic exercise. It is a **semantic apparatus** that can be applied directly in ML engineering and B2B automation. Specifically:

- **Compression‑oriented loss functions.** When training a model on a customer's data, don't ask "how many parameters do I need". Ask "what is the **minimum compression** of its processes that preserves the invariants?" Elegant compression \> volume of data.

- **Distillation as geometric reduction.** Model distillation is not just shrinking. It is **rewriting geometry** – translating the complex landscape of a large model into the elegant landscape of a small one. Subject A does the same thing in their own head.

- **RAG as access‑topology extension.** Retrieval‑Augmented Generation supplements the static model with an **external manifold**. It doesn't solve structural plasticity, but it solves *missing gradient* – which is exactly what troubles Subject B with Soundgarden. The missing node cannot be found, but it can be *bypassed* through surrounding context.

- **Anomaly detection = TOT detection.** When a model suddenly *doesn't know* where it is in its own geometry (high entropy, flat gradient, neighbor activation), it is an engineering signal that the data is out of distribution. **Detecting TOT state in a production system = robust anomaly detection.**

- **Test‑time compute as Mode 2 simulation.** When you tell a model "think step by step", you are not replacing Mode 3 – you are simulating Mode 2. It is valuable, but not sufficient.

- **Test‑time training as Mode 3 prototype.** A handful of experimental architectures (Sun et al. 2020+, recent adapters) allow a model to modify its weights based on inference. **This is the path toward emergent behavior in silicon. Still in its infancy, but the direction is right.**

Truth and intelligence are not stored in data. Nor are they stored in topology. **They live in the equilibrium between silicon's perfect memory and carbon's beautiful forgetting – and in the elegance of movement between them.**

The brain as a geometric processor is not a metaphor. It is an **operational reality** – and the key to the next leap in artificial intelligence is not in imitating the brain better. It is in **understanding when a system should remain static and when it must be allowed to dissolve and rebuild itself**.


## 📚 Zdroje / Sources

### Primární inspirace – Tomáš Mikolov

Autor vychází zejména z myšlenkového rámce Tomáše Mikolova, jeho prací o kompresi reality jako definici inteligence, limitech textově‑solipsistických LLM a nezávislosti algoritmu na substrátu. Detailní analýza těchto konceptů je k dispozici v interních materiálech:

- **Mikolov\_Manifest.txt** – Epistemologie inteligence, princip komprese

- **Tomas\_Mikolov\_High‑SNR\_knowhow\_komprese\_reality.txt** – High‑SNR výtah klíčových konceptů

- [Nadace Neuron – profil Tomáše Mikolova](https://www.nadaceneuron.cz/person/tomas-mikolov)

### Rozhovory (YouTube)

- [TOMÁŠ MIKOLOV: „V Googlu mi nevěřili, že to může fungovat jinak."](https://www.youtube.com/watch?v=B-IsBMsNIlU)

- [„AI je největší projekt lidstva a Evropa ho prohrává. Chceme to změnit"](https://www.youtube.com/watch?v=EgtmBmmXLb8)

- [„Kdo přežije AI revoluci a které firmy to pohřbí? Tomáš Mikolov o AI"](https://www.youtube.com/watch?v=QEF7CMrzznE)

### Relevantní kognitivně‑vědecká a ML literatura (integrace v2.0)

*Steyvers, M., & Tenenbaum, J. B. (2005).* The large‑scale structure of semantic networks: statistical analyses and a model of semantic growth. *Cognitive Science*, 29(1), 41–78. *Levelt, W. J. M. (1999).* Models of word production. *Trends in Cognitive Sciences*, 3(6), 223–232. *Olshausen, B. A., & Field, D. J. (1996).* Emergence of simple‑cell receptive field properties by learning a sparse code for natural images. *Nature*, 381, 607–609. *Desimone, R., & Duncan, J. (1995).* Neural mechanisms of selective visual attention. *Annual Review of Neuroscience*, 18, 193–222. *Grossberg, S. (1980).* How does a brain build a cognitive code? *Psychological Review*, 87(1), 1–51. *Friston, K. (2010).* The free‑energy principle: a unified brain theory? *Nature Reviews Neuroscience*, 11(2), 127–138. *Sun, Y., et al. (2020).* Test‑Time Training with Self‑Supervision. *arXiv:2009.14223.* *Aghajanyan, A., et al. (2020).* Intrinsic Dimensionality Explains the Effectiveness of Language Model Fine‑Tuning. *ACL.*

### Vlastní práce autora

- **Kognitivní neuro‑architektura: Mozek jako geometrický procesor** – Ground Truth Core Academic Artifact (plná akademická verze)

- **Sousek\_kompresni\_realismu\_v1.1.json** – Formalizace epistemického rámce kompresního realismu

- **Od Kompresního Realismu k Biologické Neuro‑Architektuře.md** – Vývojová linie konceptu

- **EPISTEMICKE-PRAVIDLA-AGENTNI-PRACE.md** – Aplikační pravidla pro agentní práci

- **brain\_geometric\_processor\_summary\_v1.1.md** – Předchozí narativní verze (nahrazena tímto dokumentem)

