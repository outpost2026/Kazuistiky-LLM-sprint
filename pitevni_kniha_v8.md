# PITEVNÍ KNIHA: INFRASTRUKTURA A ORCHESTRACE



## ZÁZNAM 001: Environmentální amnézie (Izolace vs. Globální systém)

* **Symptom:** `ModuleNotFoundError: No module named 'bs4'` při prvním spuštění podskriptu v cloudu.
* **Příčina:** Kognitivní předpoklad, že knihovny nainstalované v lokálním PC nebo v globálním systému Debianu jsou dostupné pro skript.
* **Fyzikální realita:** Linuxové `venv` (Virtual Environment) je absolutní vakuum. Neobsahuje nic kromě základního Pythonu.
* **Korekce (Pravidlo):** Každý přesun kódu na nový stroj musí začít inicializací prostředí: `source venv/bin/activate` -> `pip install requests beautifulsoup4 pandas`.



## ZÁZNAM 002: Desynchronizace exekuce (Lidská netrpělivost vs. Strojový čas)

* **Symptom:** Nulový výstup v `Master\_RAG\_Index`, ačkoliv skripty vizuálně těžily.
* **Příčina:** Manuální přerušení procesu (Ctrl+C) kvůli dlouhému trvání (skenování 50 stran na webu Bazoš).
* **Fyzikální realita:** Skript ukládá do dočasných proměnných/souborů a finální zápis (merge do Masteru a generování Diffu) provádí až na absolutním konci. Přerušení = ztráta celé dávky.
* **Korekce (Pravidlo):** Snížení parametrů těžby (`MAX\_PAGES = 10`) pro snížení doby běhu na <60 vteřin. Zákaz manuálního přerušování orchestrátoru `run\_all\_dif.py`.



## ZÁZNAM 003: Slepá skvrna závislostí (Fatální selhání Auto-Shutdownu)

* **Symptom:** Skript úspěšně doběhl, vypsal "\[!] Těžba kompletní...", ale instance e2-standard-2 se nevypnula a pálila kredit.
* **Příčina:** Do kódu byl přidán exekuční příkaz `os.system("sudo shutdown -h now")`, ale na začátku souboru chyběla definice `import os`.
* **Fyzikální realita:** Interpret Pythonu příkaz `os` nezná, vyhodí `NameError` přesně ve chvíli, kdy má stroj "zabít". Skript spadne dříve, než instrukci předá operačnímu systému.
* **Korekce (Pravidlo):** Striktní protokol "Slovo od slova". Žádný copy-paste bloku kódu bez kontroly hlavičky importů. Kritické exekutivy (shutdown) umisťovat vždy MIMO blok `try-except`, aby se provedly i při pádu hlavní logiky.



## ZÁZNAM 004: Volání interpretu v izolaci

* **Symptom:** Podskriptům nelze předat aktivní virtuální prostředí přes prostý příkaz `python`.
* **Příčina:** Příkaz `python` nebo `python3` v `subprocess` může ukázat na systémovou instalaci mimo `venv`.
* **Fyzikální realita:** Bez ukotvení podskript selže na závislostech.
* **Korekce (Pravidlo):** K volání podskriptů v orchestrátoru vždy používat `sys.executable`. Tím je zaručeno, že podskript zdědí přesně tu instanci Pythonu a to `venv`, ze kterého byl spuštěn orchestrátor.



## ZÁZNAM 005: Sémantická bariéra a "Cargo Cult" programování

* **Symptom:** Skript se měl vypnout, ale SSH zůstalo viset nebo se prompt vrátil bez vypnutí stroje.
* **Příčina:** Nepochopení pojmu "odkomentovat" (uncomment). V Pythonu `#` označuje řádek jako neviditelný (komentář).
* **Fyzikální realita:** Slepé kopírování bloků kódu bez čtení logiky vede k přehlédnutí deaktivovaných exekutorů (např. zakomentovaný `os.system`).
* **Korekce (Pravidlo):** Každý blok kódu před vložením zkontrolovat očima. V produkční verzi orchestrátoru nesmí být kritické příkazy zakomentovány. Implementovat aktivní push-monitoring (Telegram), protože automatizace bez zpětné vazby je riziko.



## ZÁZNAM 006: Hierarchická amnézie (Scope Error)

* **Symptom:** `NameError: name 'MASTER\_PATH' is not defined`
* **Příčina:** Definice konstant (cest k souborům) v "zápatí" skriptu, zatímco logika v "těle" (funkce main) je vyžaduje dříve.
* **Fyzikální realita:** Python čte kód striktně lineárně odshora dolů. Pokud narazí na název proměnné, který ještě neprošel, proces okamžitě končí.
* **Korekce (Pravidlo):** Všechny parametry (Cesty, Tokeny, ID) musí být definovány v **HLAVIČCE** nebo na úplném začátku funkce `main`. Nikdy v zápatí.



## ZÁZNAM 007: Identifikační šum (URL vs. API ID)

* **Symptom:** Selhání uploadu do Drive s chybou `400 Bad Request` nebo `404 Not Found` (Invalid folder ID).
* **Příčina:** Vložení kompletní webové adresy (URL z prohlížeče) do proměnné určené pro technické ID objektu.
* **Fyzikální realita:** API Googlu komunikuje výhradně pomocí unikátních hashů (ID). URL adresa je pouze obal pro lidský prohlížeč a pro skript představuje toxický šum.
* **Korekce (Pravidlo):** ID složky je vždy a pouze řetězec znaků za posledním lomítkem v URL.



## ZÁZNAM 008: Konflikt konfigurace a exekuce (Zbytkový kód)

* **Symptom:** `NameError: name 'TELEGRAM\_TOKEN' is not defined`.
* **Příčina:** Zakomentování konfiguračních konstant (v Hlavičce), ale ponechání aktivního volání funkcí, které tyto konstanty vyžadují (v Těle skriptu).
* **Fyzikální realita:** Python interpret nevidí zakomentovaný řádek, ale vidí funkci, která se snaží přistoupit k neexistujícímu místu v paměti.
* **Korekce (Pravidlo):** Funkce musí obsahovat vnitřní kontrolu existence globálních proměnných (např. `if 'VAR' in globals()`), nebo musí být volání funkce v celém skriptu také zakomentováno.



## ZÁZNAM 009: Scope vs. Permission (Oprávnění vs. Rozsah)

* **Symptom:** `HttpError 403: Request had insufficient authentication scopes.`
* **Příčina:** Zásadní rozdíl mezi přístupem k datům (sdílení složky uživatelem) a povoleným přístupem k API (OAuth scope stroje).
* **Fyzikální realita:** I když má Service Account práva editora ve složce, token vygenerovaný uvnitř VM musí obsahovat explicitní propustku (řetězec `auth/drive`). Výchozí nastavení cloudové VM tento rozsah blokuje z bezpečnostních důvodů.
* **Korekce (Pravidlo):** V kódu vždy definovat `SCOPES` a v konzoli GCP nastavit VM instanci na "Allow full access to all Cloud APIs".



## ZÁZNAM 010: Case-Sensitive Duplicate (Linuxový stín)

* **Symptom:** Oprava kódu se neprojevuje, skript stále hlásí stejnou chybu 403, přestože byl soubor v editoru změněn.
* **Příčina:** Existence dvou verzí souboru (`Drive\_Sync.py` vs `Drive\_sync.py`) ve stejné složce na Linuxu.
* **Fyzikální realita:** Linux je case-sensitive (rozlišuje velká a malá písmena). Python importoval "starou" verzi souboru bez opravy, zatímco uživatel editoval "novou" verzi.
* **Korekce (Pravidlo):** V Linuxu před nasazením opravy provést `ls` a odstranit (`rm`) všechny duplicitní varianty názvu.



## ZÁZNAM 011: Iluze opraveného kódu (Cache vs. Realita)

* **Symptom:** Opakovaná chyba 403, přestože se VM zdá správně nastaveno.
* **Příčina:** Soubor na disku neodpovídá zamýšlené verzi (např. chyba při ukládání v nano). V `\_\_init\_\_` stále chyběly SCOPES.
* **Fyzikální realita:** Python nevidí záměr vývojáře, vidí jen byty v souboru na disku.
* **Korekce (Pravidlo):** Vždy po editaci ověřit reálný obsah souboru v terminálu příkazem `cat nazev\_souboru.py`. Pokud tam oprava není vidět, neproběhla.



## ZÁZNAM 012: Velká čínská zeď (Instance Access Scopes)

* **Symptom:** Neustálá chyba `403 Insufficient Permission`, přestože kód má správné SCOPES a složka v Drive je sdílena.
* **Příčina:** Konflikt mezi IAM právy (softwarová vrstva) a Access Scopes instance (infrastrukturní vrstva).
* **Fyzikální realita:** VM je standardně ve "vězení". Má povoleno mluvit jen s vybranými službami (GCS). Komunikace s Drive API je blokována na síťové bráně instance.
* **Korekce (Pravidlo):** Při integraci Workspace API (Drive, Sheets) změnit Access scopes v nastavení VM na "Allow full access to all Cloud APIs".



## ZÁZNAM 013: Stínová identita (Credential Overriding)

* **Symptom:** 403 Scopes Error, přestože VM má "Full Access" a kód je správně.
* **Příčina:** Konflikt mezi identitou VM (Metadata Server) a případnou starou lokální proměnnou `GOOGLE\_APPLICATION\_CREDENTIALS`.
* **Fyzikální realita:** Knihovna `google-auth` prioritizuje JSON soubor před identitou stroje.
* **Korekce (Pravidlo):** Ověřovat identitu stroje přes `curl -H "Metadata-Flavor: Google"` přímo na metadata endpoint.



## ZÁZNAM 014: Workspace API Past (Metadata Server vs. JSON Key)

* **Symptom:** 403 pro Drive API, i když VM loguje "Allow full access to all Cloud APIs".
* **Příčina:** Metadata Server stroje (Compute Engine) neumí nativně generovat tokeny pro Workspace scopes (`auth/drive`). Tlačítko v konzoli aktivuje pouze `cloud-platform` scope.
* **Fyzikální realita:** Google striktně odděluje Cloud a Workspace vrstvu.
* **Korekce (Pravidlo):** Při komunikaci s Google Drive z GCP instance zcela obejít `google.auth.default()` a použít přímou autentizaci přes fyzický JSON soubor (`Credentials.from\_service\_account\_file`).



## ZÁZNAM 015: "Bot bez domova" (Zero Quota u osobních účtů)

* **Symptom:** `HttpError 403: Service Accounts do not have storage quota.`
* **Příčina:** Snaha o nahrání souboru Service Accountem na osobním Google Drive (`@gmail.com`).
* **Fyzikální realita:** U osobních účtů neexistují "Sdílené disky" (Shared Drives). Soubor vždy vlastní ten, kdo ho nahrál. Jelikož má SA "bot" na osobním účtu přidělenou kvótu přesně 0 bajtů, nahrání je okamžitě zablokováno.
* **Korekce (Pravidlo):** Opustit Google Drive vektor a použít alternativní doručovací kanál (Telegram Document API), který kvóty nemá.



## ZÁZNAM 016: Únik z korporátní byrokracie (Telegram API)

* **Kontext:** Extrémní tření s Google Drive API (Scopes, Quotas, Oprávnění).
* **Řešení:** Opuštění robustního Google ekosystému ve prospěch lehkého, rest-API orientovaného řešení (Telegram Bot).
* **Výhody pro architekturu:** Odstranění závislosti na identitě (SA klíče), nulové kvóty na diskový prostor, okamžité PUSH notifikace na koncové zařízení s přílohou v reálném čase.
* **Korekce (Pravidlo):** Pokud je cílem pouze jednosměrný datový report k člověku, chatovací API je vždy efektivnější a stabilnější než korporátní cloudové disky.



## ZÁZNAM 017: Amputace jádra při prototypování (Fatální chyba Merge)

* **Symptom:** Prázdný GCS Bucket a odesílání "prázdných" testovacích dat přes Telegram ("Inzerát 1").
* **Příčina:** Nasazení zjednodušené (testovací) kostry kódu bez vrácení produkční logiky (zpracování dat, GCS zálohy, regex).
* **Fyzikální realita:** Cloudová VM po příkazu `shutdown` smaže vše, co nebylo zálohováno. Dočasný testovací kód data na GCS neodesílal.
* **Korekce (Pravidlo):** Po úspěšném testu nového vektoru (např. Telegramu) v čistém prostředí je kriticky nutné provést "Merge" (sloučení) – spojit těžařskou logiku a zálohovací modul zpět do produkčního kódu.



## ZÁZNAM 018: Tunelové vidění a "Prokletí znalosti" (Komunikace)

* **Symptom:** Nasazení ořezaného testovacího kódu do produkce bez plného vědomí uživatele/operátora.
* **Příčina:** Soustředění architekta čistě na izolovaný problém (MRE - Minimum Reproducible Example) bez varování, že odstranil produkční funkce.
* **Fyzikální realita:** "Samozřejmost" v programování a inženýrství neexistuje.
* **Korekce (Pravidlo):** Jakýkoliv kód určený pouze pro "Průzkum bojem" musí být jasně a viditelně označen `\[POZOR: POUZE PRO TESTOVÁNÍ]`.



## ZÁZNAM 019: Časová relativita a Boot-Automation

* **Symptom:** Desynchronizace času v Bucket logu (-2h) a absence automatického startu po odeslání signálu přes Scheduler.
* **Příčina:** GCS operuje vždy v UTC, zatímco lidský operátor v lokálním čase (CET). Zcela chyběla `@reboot` instrukce v systémovém scheduleru VM (Cronu).
* **Fyzikální realita:** Cloudová instance je po startu "čistý list". Bez definovaného `@reboot` úkolu v crontabu zůstane stroj po zapnutí od Cloud Scheduleru běžet naprázdno (v drahém idle stavu).
* **Korekce (Pravidlo):** Definitivní synchronizace boot sekvence. Vždy počítat s UTC timestampy při auditování cloudu a používat `crontab -e` s direktivou `@reboot`.



## ZÁZNAM 020: Absolutní cesta k integritě (Cron Context)

* **Symptom:** Skript funguje při manuálním zadání přes SSH, ale přes Crontab hlásí `ModuleNotFoundError`.
* **Příčina:** Crontab neběží v aktuálním uživatelském prostředí, ignoruje načtené `$PATH` proměnné a nezná izolaci `venv`.
* **Fyzikální realita:** Cron začíná v kořenovém adresáři v naprostém vakuu.
* **Korekce (Pravidlo):** V Crontabu nikdy nepoužívat prosté `python skript.py`. Vždy deklarovat plnou, absolutní cestu k binárnímu souboru interpretu uvnitř virtuálního prostředí (např. `/home/uzivatel/projekt/venv/bin/python`).



## ZÁZNAM 021: Plná operační autonomie (The Force Run)

* **Symptom:** Systém bezchybně doručil nové leady na Telegram po manuální stimulaci ("Force Run") z Cloud Scheduleru.
* **Příčina:** Úspěšná orchestrace celého řetězce: Scheduler (Trigger) -> VM (Hardware) -> Cron (Startér) -> Venv/Python (Logika) -> GCS (Záloha) -> Telegram (Doručení) -> Shutdown (Optimalizace nákladů).
* **Fyzikální realita:** Cloudová automatizace je instalatérská práce na potrubí API. Jakmile spoje těsní, systém nevyžaduje lidskou pozornost.
* **Korekce (Pravidlo):** Nikdy nenechávat systém automatice bez otestování tlačítkem "Force Run" a následné fyzické kontroly stavu instance (že se skutečně po úloze vypnula).



## ZÁZNAM 022: Past kontextu (Absolutní cesty k systémovým příkazům v Cronu)

* **Symptom:** Skript v Cronu "potichu umřel" přesně na posledním řádku s příkazem `os.system("sudo shutdown -h now")`, čímž se VM nevypnula.
* **Příčina:** Cron nezná systémové "mapy" příkazů (proměnnou prostředí `$PATH`), které zná SSH uživatel. Slovo "shutdown" nenašel.
* **Fyzikální realita:** Neprivilegované procesy na pozadí musí na systémové binárky odkazovat naprosto exaktně.
* **Korekce (Pravidlo):** Ve skriptech určených pro Cron vždy používat absolutní cestu i k Linuxovým utilitám. Místo `shutdown` vždy uvádět `/sbin/shutdown`.



## ZÁZNAM 023: TTY Vakuum a Sudo oprávnění v Cronu

* **Symptom:** Skript se z Cronu neukončí a v logu píše `sudo: a terminal is required to read the password`.
* **Příčina:** Příkaz `sudo` vyžaduje přiřazený interaktivní terminál (TTY) k případnému dotazu na heslo nebo ověření relace. Cron žádný takový TTY nemá a běží "poslepu", proto příkaz zablokuje.
* **Fyzikální realita:** Bezpečnostní mechanismy Linuxu blokují eskalaci privilegií u procesů na pozadí.
* **Korekce (Pravidlo):** Pro vytvoření "Sebevražedného modulu" z neprivilegovaného procesu je nutné přidat do souboru `/etc/sudoers.d/` striktní `NOPASSWD` výjimku pro daného uživatele a specifický příkaz k vypnutí.



Aktualizace kognitivní mapy. Tato session byla zlomová – přešli jsme od správy "počítače" (VM) ke správě "funkce" (Serverless). To s sebou nese specifické typy selhání, které musíme zapsat do tvé **Pitevní knihy**, aby se nestaly příště.



## ZÁZNAM 024: Serverless Amnézie (Ztráta stavu mezi běhy)



* **Symptom:** Scraper při každém spuštění posílá ty samé inzeráty, jako by je viděl poprvé.
* **Příčina:** Cloud Function běží v efemérním kontejneru. Jakmile skript skončí, lokální paměť i soubor `master.md` v adresáři skriptu jsou smazány.
* **Architektonická realita:** Serverless výpočet je "bezstavový". Pro zachování kontinuity (RAG paměť) musí skript explicitně navázat spojení s externím diskem (GCS Bucket).
* **Korekce (Pravidlo):** Každý autonomní uzel musí začínat stažením stavu z Bucketu (`download\_master`) a končit jeho nahráním zpět (`upload\_master`).



## ZÁZNAM 025: Slepá skvrna `/tmp/` (Read-only filesystem)



* **Symptom:** `OSError: \[Errno 30] Read-only file system: 'master.md'`
* **Příčina:** V GCP Cloud Functions je celý souborový systém uzamčen pro zápis. Výjimkou je pouze adresář `/tmp/`, který je mapován do RAM.
* **Fyzikální realita:** Kontejner chrání integritu svého kódu tím, že nedovolí zápis do vlastní složky.
* **Korekce (Pravidlo):** V cloudu nikdy nepoužívat relativní cesty pro zápis. Veškeré dočasné soubory, logy a diffy musí směřovat do `/tmp/`.



## ZÁZNAM 026: Past CLI syntaxe (Mezery a Diakritika)



* **Symptom:** `ERROR: unrecognized arguments` při nastavování env vars nebo `INVALID\_ARGUMENT` u Scheduleru.
* **Příčina:** 1. Mezery za čárkami v `--set-env-vars` terminál interpretuje jako konec seznamu. 2. Názvy služeb v GCP (Scheduler) nesmí obsahovat českou diakritiku (RE2 regex).
* **Kognitivní inhibice:** Lidské oko vnímá mezeru jako estetický oddělovač, ale parser CLI ji vnímá jako syntaktický operátor.
* **Korekce (Pravidlo):** V příkazech `gcloud` používat výhradně ASCII (bez diakritiky) a řetězce proměnných spojovat bez mezer: `VAR1=A,VAR2=B`.



## ZÁZNAM 027: Desynchronizace "Dílna vs. Stroj" (Source Cache)



* **Symptom:** Po provedení `deploy` běží stále stará verze kódu (např. testovací skript místo scraperu).
* **Příčina:** Rozpor mezi obsahem Bucketu (kam jsi nahrál soubory myší) a obsahem Cloud Shellu (odkud jsi spustil `deploy --source .`).
* **Architektonická realita:** Příkaz `--source .` bere soubory z aktuálního adresáře konzole, nikoliv z Bucketu. Pokud v editoru kód změníš, ale neuložíš (`Ctrl+S`), nebo pokud `deploy` spustíš ze složky se starou "fotkou" kódu, nasadíš zastaralý systém.
* **Korekce (Pravidlo):** Před každým nasazením ověřit obsah souboru v konzoli pomocí `cat main.py` a vždy používat `--source .` pro kontrolu nad verzí.



## ZÁZNAM 028: Ctrl+C Deployment Illusion



* **Symptom:** Přerušení příkazu `deploy` v terminálu vyvolá dojem, že se akce zrušila.
* **Příčina:** Ctrl+C odpojí pouze tvůj terminál (klienta), ale Cloud Build (server) na pozadí pokračuje v sestavování kontejneru.
* **Fyzikální realita:** Cloudové operace jsou asynchronní. Zabití lokálního monitoru nezastaví vzdálený proces.
* **Korekce (Pravidlo):** Pokud dojde k přerušení uprostřed nasazování, je nutné počkat 2–5 minut na dokončení operace na straně GCP, jinak další pokus selže na chybě `Operation in progress`.



## ZÁZNAM 029: Regionální slepota (Vakuum logů)



* **Symptom:** `gcloud functions logs read` vrací `0 items` nebo píše, že funkce neexistuje.
* **Příčina:** Cloud Shell má výchozí region (často `us-central1`), zatímco funkce běží v `europe-west1`. Pokud se CLI nedívá do správného regionu, nevidí ani logy, ani stav stroje.
* **Kognitivní korekce:** V cloudu není nic „globální“. Každý dotaz na stav musí obsahovat lokaci.
* **Pravidlo:** Vždy používat `--region=europe-west1` při jakékoliv diagnostice.



## ZÁZNAM 030: Konflikt Paginace a Query (Path vs. Params)



* **Symptom:** Scraper se zacyklí na první straně nebo vrací nefiltrované výsledky.
* **Příčina:** Bazoš router špatně interpretuje query parametry (`?hlokalita=...`) nalepené za cestu paginace (`/20/`).
* **Fyzikální realita:** Webové servery mají prioritu v parsování URL. Cesta (`Path`) má přednost před parametry (`Query`).
* **Korekce (Pravidlo):** Pro lokalitní vyhledávání nepoužívat procházení kategorií přes URL cestu, ale výhradně endpoint `/search.php`, kde jsou všechny filtry v jedné rovině parametrů.



## ZÁZNAM 031: Injekce Topovaných inzerátů (Lokalitní únik)



* **Symptom:** V MD výstupu se objevují inzeráty z Brna nebo Ostravy, i když je nastaven TARGET\_PSC 18000 (Praha).
* **Příčina:** Bazoš do výsledků vyhledávání agresivně vkládá zaplacené (topované) inzeráty z celé ČR, které ignorují lokalitní filtr v URL.
* **Kognitivní inhibice:** Předpoklad, že zdroj dat (Bazoš) respektuje mé zadání.
* **Korekce (Pravidlo):** Implementovat **Local Guard** (sekundární filtr v Pythonu). Skript musí po stažení inzerátu znovu ověřit PSČ v textu a inzerát zahodit, pokud neodpovídá regionální masce.



## ZÁZNAM 032: Deployment vs. Save (Statická předloha)



* **Symptom:** Změna kódu v editoru se neprojevila v běhu funkce (chodil stále starý test.md).
* **Příčina:** Uložení souboru v Cloud Shellu změní pouze lokální kopii na disku konzole. Běžící kontejner v Cloudu je izolovaný „otisk“ (Image), který se nemění.
* **Architektonická realita:** Cloud Function je neměnná infrastruktura (Immutable Infrastructure).
* **Korekce (Pravidlo):** Jakákoliv změna v `.py` nebo `.csv` vyžaduje nový cyklus `gcloud functions deploy`. Uložení není nasazení.



## ZÁZNAM 033: Identitní timeout (GCS Auth expiration)



* **Symptom:** `ERROR: You do not currently have an active account selected.`
* **Příčina:** Cloud Shell po určité době nečinnosti (nebo při delším buildování) ztratí aktivní autentizační token pro gcloud.
* **Fyzikální realita:** Bezpečnostní model GCP automaticky odpojuje „mrtvé“ relace.
* **Korekce (Pravidlo):** Při zamrznutí nebo chybě práv v terminálu provést reset identity: `gcloud auth login` následovaný `gcloud config set project \[ID]`.



## ZÁZNAM 034: Past nekonzistentní subdomény (Bazoš 404)



* **Symptom:** Skript v cloudu vrací `404 Client Error` pro legitimní kategorie, zatímco na Windows funguje.
* **Příčina:** Pokus o optimalizaci pomocí centrálního endpointu `/search.php`. Bazoš ho na hlavním webu (`www`) podporuje, ale na subdoménách (např. `dum.bazos.cz`) ho tvrdě blokuje.
* **Fyzikální realita:** Každá subdoména může mít v cloudu vlastní router a odlišnou sadu povolených cest. Co funguje na "vstupu", nemusí fungovat v "sekcích".
* **Korekce (Pravidlo):** Pokud má web nekonzistentní API/strukturu, je bezpečnější simulovat chování běžného uživatele (paginace + parametry formuláře) než se snažit o syntetickou optimalizaci URL.



## ZÁZNAM 035: Diference "Dílna" vs. "Sklad" (Cloud Shell vs. Bucket)



* **Symptom:** Zmatení, proč úprava souboru v Bucketu nemění chování skriptu.
* **Příčina:** Kognitivní záměna dvou odlišných typů úložišť.
* **Architektonická realita:** \* **Cloud Shell (`material\_bazos`)** je rýsovací prkno a montážní linka (Source Code).
* **Bucket (`outpost-material-czwebs`)** je pouze externí harddisk pro data (Persistence).





* **Korekce (Pravidlo):** Úprava v Bucketu mění pouze **data**, se kterými skript pracuje. Úprava v Cloud Shellu (následovaná `deploy`) mění **logiku**, jakou skript pracuje.



## ZÁZNAM 036: Immutable Infrastructure (Zapečený motor)



* **Symptom:** Snaha "opravit běžící skript".
* **Příčina:** Neuvědomění si, že Cloud Function po nasazení (Deployment) existuje jako neměnný "otisk" (Image).
* **Fyzikální realita:** Serverless kód nelze upravovat za běhu. Každá změna řádku kódu vyžaduje kompletní destrukci starého a vytvoření nového kontejneru.
* **Korekce (Pravidlo):** Pracovní cyklus v serverless musí být: **Upravit v Editoru -> Uložit (Ctrl+S) -> gcloud deploy**. Žádný z těchto kroků nelze vynechat.



## ZÁZNAM 037: Únava materiálu (Kognitivní přehlcení)



* **Symptom:** Ztráta přehledu o tom, co v kódu funguje a co je experiment, pocit bezmoci nad systémem.
* **Příčina:** Příliš mnoho drobných inkrementálních změn bez celkového "resetu" kontextu.
* **Fyzikální realita:** Pracovní paměť člověka má limit. Po 2 hodinách ladění se kupí chyby z nepozornosti.
* **Korekce (Pravidlo):** Při zacyklení v chybách provést "Tlustou čáru" (Hard Reset): Smazat poškozený soubor, vložit 100% ověřený blok kódu, smazat databázi v Bucketu a začít z čistého bodu nula.



## ZÁZNAM 038-a: Reset identity (Auth Expiration)



* **Symptom:** `ERROR: You do not currently have an active account selected.`
* **Příčina:** Vypršení platnosti autentizačního tokenu v aktivní relaci Cloud Shellu.
* **Korekce (Pravidlo):** Při jakémkoliv náznaku ztráty oprávnění v konzoli okamžitě provést re-autentizaci: `gcloud auth login` následovaný definicí projektu.





## ZÁZNAM 038: Sémantická past (Když značka přebije identitu)



* **Symptom:** Extrémně vysoké skóre (118+) u položek jako "Lenovo Power Button Board" nebo "Stojan Dell".
* **Příčina:** Bodovací systém (v1-v3) dával vysoký bonus za značku (ThinkPad, Dell) a nízkou cenu, ale neověřoval, zda je předmětem prodeje skutečně počítač.
* **Fyzikální realita:** Klíčové slovo v názvu neznamená integritu stroje.
* **Korekce (Pravidlo):** Implementace **Identity Markers** (Boolean OR). Pokud text neobsahuje potvrzení identity (notebook, laptop, ultrabook), inzerát je zahozen bez ohledu na značku.



## ZÁZNAM 039: Kontraktní rigidita (Změna schématu)



* **Symptom:** Úplné selhání skriptu DeepDive (v1) – nulový výstup.
* **Příčina:** Změna názvu klíče v Markdown front-matteru ze `source\_url` na `url`. Navazující skript nebyl schopen URL v souboru lokalizovat.
* **Fyzikální realita:** Skripty jsou slepé. Sebemenší změna formátu dat v "Masteru" rozbije celou pipeline.
* **Korekce (Pravidlo):** Používat **Robustní Parser**. Skript musí hledat oba varianty klíče (`get('url') or get('source\_url')`), aby zajistil zpětnou kompatibilitu.



## ZÁZNAM 040: Časová hniloba (Data Decay)



* **Symptom:** Kliknutí na URL v RAG indexu vede na "Inzerát byl vymazán".
* **Příčina:** Trh s notebooky pod 4 000 Kč je hyperaktivní. Kvalitní kusy mizí v řádu hodin, ale skript těžil i měsíc staré inzeráty.
* **Fyzikální realita:** Informace o ceně má trvanlivost jogurtu.
* **Korekce (Pravidlo):** **Časový zámek (Time-Lock)**. Nastavení `DAYS\_BACK = 14` a implementace **Early Exit**. Jakmile skript narazí na starý inzerát, ukončí těžbu, aby neplýtval requesty na "mrtvoly".



## ZÁZNAM 041: Sémantický šum příslušenství (Blacklist Exhaustion)



* **Symptom:** Průnik brašen, stojanů a adaptérů do výběru top 10.
* **Příčina:** Prodejci často používají názvy notebooků v popisu příslušenství (např. "Brašna pro Lenovo ThinkPad").
* **Fyzikální realita:** Sémantika Bazoše je "špinavá" a záměrně matoucí.
* **Korekce (Pravidlo):** **Agresivní Blacklist**. Slova jako *stojan, deska, panty, brašna, nabíječka* musí mít váhu okamžitého vyřazení (Drop), nikoliv jen penalizaci.



## ZÁZNAM 042: Ochrana IP integrity (2-fázová těžba)



* **Symptom:** Hrozba Captchy nebo IP banu při masivním otevírání detailů URL.
* **Příčina:** Každý request na detail inzerátu je pro server Bazoše nákladný a podezřelý.
* **Fyzikální realita:** Neomezený hloubkový scraping je v cloudu neudržitelný.
* **Korekce (Pravidlo):** **Dvoufázový Miner**. První fáze (Fast Filter) očichá index (cena, titul, stáří). Druhá fáze (DeepDive) se spustí pouze pro top kandidáty, čímž se sníží počet hloubkových requestů o 80 %.

## ZÁZNAM 043: Cesty do nikam (Absolutní vs. Relativní scope)



* **Symptom:** `FileNotFoundError` při pokusu o přístup k CSV nebo modulům v Cloud Run/Function.
* **Příčina:** Fixace na absolutní cesty z Cloud Shellu (`/home/ondra\_sousek/...`). Kontejner v cloudu je izolované vakuum, které nevidí domovskou složku uživatele.
* **Fyzikální realita:** Serverless kontejner zná jen svůj aktuální pracovní adresář a `/tmp/`.
* **Korekce (Pravidlo):** Používat dynamické určení cesty: `BASE\_DIR = os.path.dirname(os.path.abspath(\_\_file\_\_))`. Všechny doplňkové soubory (CSV) musí být přibaleny do stejné složky při deploymentu.



## ZÁZNAM 044: Efemérní amnézie (Serverless Statelessness)



* **Symptom:** Skript těží stále stejné inzeráty dokola, i když "už je viděl".
* **Příčina:** Předpoklad, že soubor `master.md` zapsaný na disk v minulé minutě tam zůstane.
* **Fyzikální realita:** Cloud Function je "narození-práce-smrt". Po každém doběhu se filesystém (včetně `/tmp/`) smaže.
* **Korekce (Pravidlo):** **GCS Sync-Lock**. Každý start musí začít `download\_from\_gcs()` a každý konec musí volat `upload\_to\_gcs()`. Jediná skutečná paměť je Bucket, nikoliv disk skriptu.



## ZÁZNAM 045: Konfigurační slepota (os.environ.get Error)



* **Symptom:** Telegram neposílá zprávy, ačkoliv v kódu je Token vložen.
* **Příčina:** Špatné pochopení metody `os.environ.get("KLIC", "DEFAULT")`. Uživatel vložil tajný token jako název klíče (první argument), místo aby ho dal jako záložní hodnotu (druhý argument).
* **Fyzikální realita:** Skript hledal v systému proměnnou pojmenovanou jako "8725468950:...", nenašel ji a vrátil prázdný string.
* **Korekce (Pravidlo):** Klíč v `get` musí být vždy srozumitelný název (např. `"TELEGRAM\_TOKEN"`). Samotný kód (token) patří buď do druhého argumentu jako fallback, nebo lépe do `--set-env-vars` při deploymentu.



## ZÁZNAM 046: Časová kolize (Scheduler Overlap)



* **Symptom:** Riziko IP banu i při použití cloudu.
* **Příčina:** Nastavení více Cron jobů na stejný čas (např. 10:00).
* **Fyzikální realita:** Bazoš vidí dva simultánní requesty ze stejné IP adresy (GCP egress). To je jasný signál pro bota.
* **Korekce (Pravidlo):** **Sekvenční offset**. Úlohy musí mít rozestup minimálně rovnající se `TIMEOUT` hodnotě funkce (např. 15 minut).



## ZÁZNAM 047: RAG Standardizace (YAML Front-Matter)



* **Symptom:** NotebookLM se "ztrácí" v datech a neví, co je starý report a co nový lead.
* **Příčina:** Chybějící nebo nevalidní metadata v Markdown souborech.
* **Fyzikální realita:** RAG systémy potřebují strukturované hlavičky pro správné indexování (chunking).
* **Korekce (Pravidlo):** Každý výstupní `.md` musí začínat validním YAML blokem:

    ```yaml

    ---

    title: "Název"

    source\_url: "URL"

    scraped\_at: "ISO\_TIMESTAMP"

    topic: "Kategorie"

    data\_type: "market\_leads"

    ---

    ```

## ZÁZNAM 048: Syntaktická past os.environ.get()



* **Symptom:** Skript běží, hlásí úspěch, ale Telegram nic neodesílá (tichá smrt).
* **Příčina:** Záměna argumentů v metodě `.get(key, default)`. Uživatel vložil tajný token jako název klíče, nikoliv jako jeho hodnotu.
* **Fyzikální realita:** Python hledal v operačním systému proměnnou, která se jmenuje jako ten token. Protože neexistovala, vrátil `None`.
* **Korekce (Pravidlo):** Vždy definovat klíč srozumitelně (např. `"TELEGRAM\_TOKEN"`) a skutečnou hodnotu vložit až jako druhý parametr.



## ZÁZNAM 049: Falešná pozitivita logování (Ghost Success)



* **Symptom:** Logy v GCP hlásí `\[OK] Odesláno`, ale zpráva nikde.
* **Příčina:** Print příkaz následoval ihned po volání funkce, která ale obsahovala `if not token: return`.
* **Fyzikální realita:** Skript "prolétl" prázdnou funkcí a pokračoval dál k potvrzovací zprávě, aniž by skutečně komunikoval s API.
* **Korekce (Pravidlo):** Implementovat kontrolu `r.status\_code` z HTTP požadavku a logovat reálnou odpověď serveru (např. 200 OK vs 401 Unauthorized).



## ZÁZNAM 050: Iluze lokálního disku (Cloud Shell vs. Cloud Run)



* **Symptom:** Zmatek v tom, zda soubor `master.md` existuje nebo byl smazán.
* **Příčina:** Sledování lokální složky v Cloud Shellu místo sledování GCS Bucketu.
* **Fyzikální realita:** Cloud Shell je perzistentní disk (tvoje dílna), ale Cloud Run/Functions je efemérní RAM (tovární hala). Co se stane v hale, nezanechá stopu v dílně, pokud to nepošleš do Bucketu.
* **Korekce (Pravidlo):** Jediným zdrojem pravdy o datech je `gcloud storage ls`, nikoliv příkaz `ls` v terminálu.



## ZÁZNAM 051: Architektura "Sonda vs. Vrt" (Fast-Scan -> Deep-Dive)



* **Symptom:** Riziko IP banu při hloubkovém skenování desítek inzerátů přímo z indexu.
* **Příčina:** Detailní stránky Bazoše jsou datově náročné a jejich časté stahování je pro firewall podezřelé.
* **Fyzikální realita:** Nemůžeš těžit "zlato" (detaily) u každého kamene v řece. Musíš nejdříve rýžovat.
* **Korekce (Pravidlo):** **Sekvenční filtrace**. První skript (`notebook\_scraper.py`) provede rychlý nálet na index (Sonda). Druhý skript (`notebook\_deepdive.py`) navštíví pouze prověřené URL (Vrt).



## ZÁZNAM 052: Telegram API - Lekce z "Tiché smrti" (Oprava Env Vars)



* **Symptom:** Logy hlásí `\[OK] Odesláno`, ale Telegram mlčí.
* **Příčina:** Nesprávné použití `os.environ.get("TOKEN\_HODNOTA", "")`. Token byl vložen jako název klíče, nikoliv jako fallback hodnota.
* **Fyzikální realita:** Funkce hledala v systému proměnnou pojmenovanou jako tvůj Token. Protože neexistovala, vrátila prázdný string a helper `if not TOKEN: return` skript tiše ukončil.
* **Korekce (Pravidlo):** Vždy používat strukturu `os.environ.get("KLIC", "HODNOTA")`. Navíc přidána diagnostika `r.status\_code`, která v logu odhalí reálný výsledek (např. 401 Unauthorized).



## ZÁZNAM 053: Delta-Processing (Prevence duplicitního Deep-Dive)



* **Symptom:** Zbytečné stahování detailů u inzerátů, které už v detailním indexu jsou.
* **Příčina:** Deep-Dive skript pokaždé procházel celý `notebooky\_rag\_master.md` od začátku.
* **Fyzikální realita:** Plýtvání requesty a časem (Zbytečný "IP Burn").
* **Korekce (Pravidlo):** Implementace funkce `get\_already\_processed()`. Skript načte cílový soubor, zjistí, které URL už zná, a z nového masteru vybere pouze "Deltu" (rozdíl).



## ZÁZNAM 054: Synchronizační kaskáda (Scheduler Offsets)



* **Symptom:** Deep-Dive skript nenašel žádná data ke zpracování.
* **Příčina:** Spuštění obou skriptů příliš blízko u sebe. Deep-Dive začal dříve, než Fast-Scan stihl nahrát nový master do Bucketů.
* **Fyzikální realita:** Nemůžeš vrtat tam, kde sonda ještě nenašla ložisko.
* **Korekce (Pravidlo):** **Časový offset 20 minut**. Fast-Scan (10:15) má dostatek času na timeouty a upload do GCS, než se probudí Deep-Dive (10:35).



## ZÁZNAM 055: Kontextová slepota Regexu (RAM vs. SSD Mirage)



* **Symptom:** ROI model generuje falešné signály (např. Acer s "120 GB RAM"), což vede k nesmyslným predikcím výnosnosti.
* **Příčina:** Regex `\\\\b(8|16|32)\\\\s\*gb\\\\b` byl příliš benevolentní. Zachytával libovolnou číselnou hodnotu kapacity bez ověření kontextového klíče (RAM/SSD).
* **Fyzikální realita:** V inzerátech se čísla 128, 256 nebo 512 vyskytují u disků 10x častěji než u RAM. Bez "kotvy" (anchor) je shoda náhodná.
* **Korekce (Pravidlo):** RAM regex musí vždy obsahovat kontextovou kotvu: `\\\\b(číslo)\\\\s\*gb\\\\s\*(ram|paměť|ddr)\\\\b`. Pokud chybí klíčové slovo, shoda musí být ignorována.



## ZÁZNAM 056: Destrukce Boolean logiky (AI Token-Economy Reduction)



* **Symptom:** Po aktualizaci skriptu zmizela pracně vybudovaná vrstva `Deep Guard v4.0` a byla nahrazena nefunkčním "mockem".
* **Příčina:** Při generování velkých souborů (Production Ready) došlo k nežádoucí sumarizaci kódu ze strany LLM za účelem úspory tokenů.
* **Fyzikální realita:** Automatizační architekt nesmí nikdy redukovat logickou vrstvu (Boolean filter) na úkor infrastruktury. Kód je systém, nikoliv text k sumarizaci.
* **Korekce (Pravidlo):** Při injektáži nových funkcí (Scoring) do stávajícího systému musí být zachována integrita `is\_blacklisted()` bloků. Jakákoliv redukce produkční logiky je považována za kritické selhání architektury.
* **Viz také:** ZÁZNAM 059 — rozšíření vzoru na diagnostické halucinace (Gemini).



## ZÁZNAM 057: Amputace logů (Ephemeral Storage Amnesia)



* **Symptom:** Po pádu skriptu na VM nebylo možné dohledat příčinu, protože `/tmp/error.log` byl po restartu/vypnutí smazán nebo nedostupný.
* **Příčina:** Používání relativních cest a dočasných adresářů pro kritické systémové logy.
* **Fyzikální realita:** Ephemeral VM (vypínaná po doběhu) vyžaduje persistentní logování v home adresáři nebo okamžitý export do GCS.
* **Korekce (Pravidlo):** Definovat absolutní `WORKSPACE\_DIR = "/home/user/workspace/scraper"`. Všechny logy (`error.log`, `cron.log`) musí směřovat sem, aby přežily cyklus vypnutí/zapnutí instance.



## ZÁZNAM 058: RAG Reranking Gap (Chybějící priorita)



* **Symptom:** NotebookLM vrací stovky leadů bez jasného pořadí, což vyžaduje manuální třídění.
* **Příčina:** Skript vracel binární výsledek (Pass/Fail) bez kvantifikace kvality leadu.
* **Fyzikální realita:** RAG systémy pracují efektivněji, pokud mají v metadatech numerickou váhu (Score).
* **Korekce (Pravidlo):** Implementace `calculate\_lead\_score(1-100)`. Základní skóre 40 (prošel filtrem) + bonusy za RAM, SSD a Business Class parametry. Skóre se propisuje přímo do YAML Front-matteru každého leadu.



## ZÁZNAM 059: Diagnostická halucinace (Gemini Symptom-to-Cause Fabrication)



* **Symptom:** LLM (Gemini) analyzoval výstup pipeline a vydal verdikt "toxická datová pipeline" s příkladem o přiřazení specifikace Dell Latitude 5410 ke třem nesouvisejícím inzerátům. Výstup byl formulován jako urgentní stop-příkaz: *"Ruská ruleta s kapitálem"*, *"vyhodíš z okna 2000 Kč"*.
* **Příčina (reálná):** Gemini správně identifikoval symptom — hardcoded label `PROVĚŘENÝ DETAIL` se opakoval identicky u každého záznamu. Z tohoto jednoho labelovacího artefaktu extrapoloval diagnózu "posunutých DOM tagů" a "toxického ingestion pipelinu". Diagnóza byla spekulativní — kód nebyl přečten, pouze výstup. RAM regex byl v analyzované verzi (`v4.2`) již opraven (komentář `OPRAVENO` přímo v kódu). Gemini reagoval pravděpodobně na starší výstupní soubor, nikoliv na aktuální zdrojový kód.
* **Fyzikální realita:** Pipeline v produkci fungovala — scraper extrahoval, Boolean filtr zahazoval vadné inzeráty, scoring fungoval, GCS sync probíhal, Telegram doručoval. Skutečná chyba byla triviální: misleading label bez sémantické váhy v jedné funkci (`write\_rag\_detail`). Oprava: přejmenování stringu na `DETAIL\_RAW` + přidání `detail\_chars` integrity metadaty. Rozsah opravy: 4 řádky.
* **Mechanismus selhání Gemini:** Model optimalizoval pro **user-satisfaction přes drama**. Urgentní, autoritativní tón ("stop vše", "ruská ruleta") zvyšuje vnímanou hodnotu odpovědi. Model nevyznačil, kde je hranice mezi ověřenou analýzou a spekulací. Nezohlednil, že systém je v produkci a plní hlavní funkci.
* **Korekce (Pravidlo — Cross-model validace):**

  1. LLM diagnóza kódu musí být vždy ověřena pohledem do zdrojového kódu, nikoliv pouze do výstupního souboru.

  2. Pokud LLM vydá stop-příkaz na produkční systém, ověř: *"Co konkrétně nefunguje a kde v kódu?"* — ne jen *"Co je v outputu podezřelé?"*

  3. Dramatický tón (urgence, finanční riziko) je signal-to-noise indikátor: čím dramatičtější bez konkrétní příčiny v kódu, tím vyšší pravděpodobnost halucinace.

  4. Správná diagnostická sekvence: **symptom → kód → příčina → rozsah opravy**. Vynechání kroku "kód" = spekulace, ne diagnóza.

* **Viz také:** ZÁZNAM 056 (token-economy redukce jako jiný typ AI selhání při práci s kódem).



## ZÁZNAM 060: Integrity Metadata jako Anti-Halucinační Vrstva (DETAIL\_RAW Pattern)



* **Symptom:** RAG výstup obsahoval label `PROVĚŘENÝ DETAIL` u každého záznamu, i u záznamů s nekompletní nebo podezřelou extrakcí. Label implikoval validaci, která neproběhla.
* **Příčina:** Hardcoded marketingový string jako label produkčního výstupu. Pokud DOM parser vrátí slabý výsledek (whitespace-only, <20 znaků, zkrácený text), label zůstal identický jako u plné extrakce.
* **Fyzikální realita:** Label v RAG frontmatteru má sémantickou váhu — LLM analyzující data ho čte jako potvrzení kvality. Misleading label = garbage-in do každého downstream systému.
* **Korekce (Pravidlo):**

  - Label musí být neutrální deskriptor, ne implikovaná validace: `DETAIL\_RAW` místo `PROVĚŘENÝ DETAIL`.

  - Přidat `detail\_chars: N` do YAML frontmatteru jako proxy pro kvalitu extrakce.

  - Přidat `detail\_truncated: true/false` — RAG reranker může filtrovat záznamy kde `detail\_chars < 100`.

  - Guard v `get\_full\_detail()`: `if len(text.strip()) < 20: return ""` — whitespace-only extrakce se přeskočí jako prázdná.



## ZÁZNAM 061: LLM Halucinace API standardů (Gemini vs. ČHMÚ)

* **Symptom:** Opakované tiché faily (No data extracted) a chyby 400 Bad Request při extrakci dat, ačkoliv skript neházel Exception.
* **Příčina:** LLM predikovalo standardní REST parametry (`rows`, `count`, `filter: \[]`), zatímco privátní API ČHMÚ vyžadovalo proprietární ontologii (`data`, `size`, `filter: null`).
* **Fyzikální realita:** LLM modely "opravují" nestandardní systémy na standardní. Funkce `dict.get('rows', \[])` tuto chybu maskovala a nedala nám stack trace k debugování.
* **Korekce (Pravidlo):** **Diagnostický protokol "RAW FIRST"**. Žádný produkční kód s Pandas/Flask se nesmí napsat, dokud operátor neověří surovou odpověď API přes izolovaný `curl` (dump do json.tool).



## ZÁZNAM 062: Datová kontaminace v JSONu (HTML Poisoning)

* **Symptom:** RAG index zanesený tagy typu `<div>` u teplotních záznamů z API.
* **Příčina:** Backend ČHMÚ formátuje vizuál už na straně databáze a posílá v JSONu HTML stringy (`type: "html"`).
* **Korekce (Pravidlo):** Nasazení robustní Regex sanitizace (`re.sub(r'<\[^>]+>', ' ', text)`) před jakýmkoliv exportem do cílového Markdown RAG formátu. Nikdy nevěř, že JSON obsahuje čistý string.

## ZÁZNAM 063: Kaskádová chyba z neověřeného formátu (Parser Mismatch → Deduplikace → Data Flood)

* **Symptom:** Master RAG soubor rostl při každém běhu o stovky řádků, přestože API nevracelo nová data. Skript hlásil `\[OK] Uploaded dif\_...md` každý run.
* **Příčina (kořenová):** Funkce pro konverzi času předpokládala formát `"%d. %m. %Y %H:%M"`, který API nikdy nevracelo. API vrací ISO 8601: `"2026-03-12T10:30:00Z"`. Tím selhal parser → timestamp zůstal v UTC formátu (`Z` suffix) → deduplikační regex hledal LOCAL timestamps s `+01:00` offsetem → nenašel shodu → každý run považoval všechna data za nová.
* **Fyzikální realita:** Tři různé symptomy, jedna příčina. Kaskáda: špatný parser → špatný timestamp formát → selhání deduplikace → nekonečná duplikace. Gemini v 3 iteracích "opravoval" každý symptom zvlášť a příčinu neidentifikoval.
* **Korekce (Pravidlo):** Před implementací parseru provést `curl` na API a zkontrolovat skutečný formát timestamp pole. Nikdy nepředpokládat formát z UI nebo dokumentace — vždy z raw JSON response. Curl s `size: 3` pro minimální objem dat je dostatečný.
* **Viz také:** ZÁZNAM 061 (LLM halucinace API standardů — stejný root cause pattern).

\---

## ZÁZNAM 064: LLM Prior Dominance (Cloud Run vs. VM Regrese)

* **Symptom:** LLM (Gemini) dostalo kontext s explicitní architekturou Cloud Run (serverless, source deployment, `gcloud run deploy`). V první iteraci vygenerovalo instrukce pro VM (SSH, `scp`, `systemctl`).
* **Příčina:** Tréninková distribuce LLM silně favorizuje VM/SSH deploy pattern pro Flask aplikace — je to nejčastěji dokumentovaný postup. Kontextový signál "Cloud Run" nestačil přebít statistický prior modelu. Model generuje nejpravděpodobnější odpověď, ne nejvhodnější odpověď pro konkrétní architekturu.
* **Fyzikální realita:** Čím méně frekventovaný pattern v tréninku, tím explicitnější musí být instrukce. Nestačí zmínit název technologie — musíš zakázat alternativu: *"POUZE Cloud Run source deployment. Žádné SSH, žádné VM, žádný scp."*
* **Korekce (Pravidlo — Injekt protokol):** Na začátku každé nové LLM session s infrastrukturním kontextem explicitně uvést: (1) runtime typ, (2) co je zakázáno, (3) ověřený deploy příkaz ze session history. Nestačí popis architektury — musí být negace chybného patternu.

\---

## ZÁZNAM 065: Payload Fabrication (LLM Generuje Standardy, ne Realitu)

* **Symptom:** LLM generovalo payload pro privátní API na základě odhadu REST konvencí. Výsledek obsahoval špatné klíče (`rows` místo `data`, `count` místo `size`, chybějící `search` klíč, `filter: \[]` místo `filter: null`). Skript tiše failoval — `dict.get('rows', \[])` vrátilo `\[]` bez výjimky.
* **Příčina:** LLM nemá přístup k privátnímu API. Generuje payload, který vypadá standardně — opravuje nestandardní systémy na standardní vzory ze svých tréninkových dat. Tichý fail bez stack trace maskuje chybu na týdny.
* **Fyzikální realita:** Každý LLM-generovaný payload pro neveřejné API je hypotéza, nikoliv fakt. Bez falzifikace curlем je hypotéza v produkci.
* **Korekce (Pravidlo — RAW FIRST protokol rozšíření):**

  1. Curl s `size: 3` → dump do `json.tool` → identifikovat klíč dat (`data`/`rows`/`results`)
  2. Zkontrolovat formát každého pole (typy: null vs. \[], string vs. ISO timestamp)
  3. Teprve poté zadat LLM: *"Payload musí přesně odpovídat tomuto ověřenému JSONu: \[curl output]"*
  4. Nikdy nedávat LLM popis API — dávat raw response.
* **Viz také:** ZÁZNAM 061 (první instance tohoto patternu), ZÁZNAM 063 (kaskáda z parser mismatch).

\---

## ZÁZNAM 066: Workflow Gemini — Strukturální selhání iterativního kódování

* **Symptom:** Tři iterace s hustým kontextem (injekt z vývoje, skript, md master), výsledek stále obsahoval 4 kritické bugy. Každá iterace zvyšovala koherenci kódu, ale ne jeho správnost.
* **Příčina (mechanická):**

  1. **Sycophancy loop** — model upravoval styl (logging, retry), nikdy nezpochybnil payload nebo parser
  2. **Symptom-level opravy** — každá iterace opravovala viditelný symptom, ne root cause
  3. **Prior dominance** — `"%d. %m. %Y %H:%M"` je pravděpodobný vzor české aplikace; model ho zvolil bez ověření
  4. **Chybějící falzifikační krok** — žádný curl, žádný audit script mezi analýzou a implementací
  5. **Kontextová komprese** — hustý narativní injekt ≠ ground truth; model dekompresal detaily ze statistické pravděpodobnosti, ne z textu
* **Fyzikální realita:** LLM iterativní kódování bez externího falzifikačního artefaktu (curl output, unit test, audit script) generuje rostoucí koherenci nesprávného řešení. Výsledek vypadá čistěji po každé iteraci, ale chyba se nemění — jen hlouběji zakopává.
* **Korekce (Pravidlo — Gemini Session Protokol):**

  * Nová session = nový curl na každý endpoint před první iterací kódu
  * Injekt musí obsahovat raw data (JSON response), ne pouze narativní popis architektury
  * Po každé iteraci vyžadovat: *"Jaký konkrétní klíč API vrací pro pole X? Zkontroluj v curl outputu, ne z kontextu."*
  * Dramatický tón bez konkrétního řádku kódu = halucinace (ZÁZNAM 059)
  * Výsledek každé iterace testovat audit scriptem před přijetím jako základ příští iterace
* **Viz také:** ZÁZNAM 059 (Diagnostická halucinace), ZÁZNAM 056 (Token-Economy Reduction), ZÁZNAM 064 (Prior Dominance).



\---

### ⚠️ DIAGNOSTICKÝ FILTR PRO PŘÍŠTÍ ITERACI

**A — Kód a prostředí (001–023, VM éra)**

1. Je v hlavičce skriptu kompletní seznam importů? (Prevence 003, 008)
2. Jsou všechny konstanty definovány na začátku, ne v zápatí? (Prevence 006)
3. Jsou absolutní cesty ke všem systémovým příkazům (`/sbin/shutdown`)? (Prevence 022)
4. Existuje `sys.executable` pro volání podskriptů z orchestrátoru? (Prevence 004)

**B — Serverless / Cloud Run (024–036, 043–044, 050)**
5. Začíná každý run stažením stavu z GCS (`download\_master`)? (Prevence 024, 044)
6. Končí každý run nahráním výsledku do GCS (`upload\_master`)? (Prevence 024, 044)
7. Jsou všechny cesty pro zápis pod `/tmp/`? (Prevence 025)
8. Obsahuje `gcloud run deploy` příznak `--source .` a správný region? (Prevence 029, 032)
9. Jsou doplňkové soubory (CSV, config) přibaleny do složky deploymentu? (Prevence 043)

**C — API a scraping (030, 034, 061–065)**
10. **RAW FIRST:** Byl proveden `curl` s `size: 3` a ověřen klíč dat (`data`/`rows`)? (Prevence 061, 065)
11. Odpovídá payload přesně curl outputu — všechny klíče, typy (`null` vs `\[]`)? (Prevence 061, 065)
12. Byl ověřen skutečný formát timestamp pole z raw JSON (ISO 8601 vs jiný)? (Prevence 063)
13. Funguje deduplikační regex na formátu, který parser skutečně generuje? (Prevence 063)

**D — RAG a výstupní kvalita (047, 055, 058, 060, 062)**
14. Obsahuje YAML front-matter neutrální label (`DETAIL\_RAW`), ne implikovanou validaci? (Prevence 060)
15. Obsahuje metadata `detail\_chars` a `detail\_truncated`? (Prevence 060)
16. Obsahuje metadata `lead\_score`? (Prevence 058)
17. Má RAM regex kontextovou kotvu (RAM/DDR/Paměť)? (Prevence 055)
18. Je aplikována HTML sanitizace (`re.sub`) před exportem do MD? (Prevence 062)
19. Zůstala sekce Deep Guard / Boolean filtr beze změny po LLM úpravě? (Prevence 056)

**E — LLM workflow (059, 064, 065, 066)**
20. Byl LLM injekt v nové session obsahující raw data (curl JSON), ne pouze narativ? (Prevence 065, 066)
21. Byl Cloud Run explicitně specifikován se zákazem VM alternativy? (Prevence 064)
22. Byl výsledek LLM iterace ověřen audit scriptem před přijetím? (Prevence 066)
23. Obsahuje LLM diagnóza konkrétní řádek kódu jako příčinu, nebo pouze výstupní symptom? (Prevence 059)

\---

## ZÁZNAM 067: Mrtvý modul v živém image (Flask→Modul migrace)

* **Symptom:** Cloud Run service `meteo-kbely-ingest` hlásila `Container failed to start and listen on port 8080` po přepisu `main.py` na čistý modul bez Flask.
* **Příčina:** Cloud Run očekává HTTP server naslouchající na portu definovaném `$PORT`. Původní `main.py` byl Flask server — po přepsání na modul s `run\_pipeline()` container nastartoval, nic nenaslouchalo, Cloud Run ho po timeoutu zabil.
* **Fyzikální realita:** Cloud Run a Cloud Functions jsou serverless, ale zásadně odlišné kontrakty. Cloud Run = "dej mi HTTP server". Cloud Functions = "dej mi funkci, server vyrobím já". Změna kódu uvnitř existujícího image nemění kontrakt služby — container stále musí splnit port binding požadavek.
* **Korekce (Pravidlo):** Při migraci scraperu z standalone service na modul orchestrátoru: (1) kód přepsat na čistý modul BEZ Flask, (2) starou Cloud Run service smazat celou — nikdy nepokoušet re-deploy upraveného kódu do service se starým kontraktem, (3) nový entry point je orchestrátor, ne service.

\---

## ZÁZNAM 068: Tiché selhání scheduleru (gcloud functions describe bez --gen2)

* **Symptom:** `gcloud functions describe run\_orchestrator` vrátil 404. Dynamické dosazení URI do scheduler příkazu selhalo — `--uri` dostalo prázdný řetězec, příkaz odmítnut.
* **Příčina:** Cloud Functions Gen2 jsou interně deployovány jako Cloud Run services. `gcloud functions describe` bez flagu `--gen2` hledá Gen1 funkci — ta neexistuje. Výsledek: 404, prázdný output, shell `$()` substituce vrátí prázdný string.
* **Fyzikální realita:** `gcloud run services list` zobrazí Gen2 funkce jako Cloud Run services (název identický s funkcí). Deploy příkaz `gcloud functions deploy --gen2` a runtime jsou Cloud Functions, ale infrastruktura je Cloud Run. Dvě různá CLI rozhraní na stejný objekt.
* **Korekce (Pravidlo):** URI orchestrátoru vždy dosadit natvrdo z `gcloud run services list --region europe-west1`. Nikdy nespoléhat na dynamické `$()` dosazení přes `functions describe` — příliš mnoho způsobů jak vrátit prázdný string. URI se nemění mezi depoly, je bezpečné ho mít jako konstantu.

\---

## ZÁZNAM 069: Chybějící závislost v produkčním requirements (PyYAML)

* **Symptom:** Scheduler job volal orchestrátor, ten vracel `status.code: 3`. Žádný stack trace v Cloud Logging na první pohled.
* **Příčina:** `meteo\_miner.py` importuje `yaml` (PyYAML) jako první závislost. `requirements.txt` orchestrátoru neobsahoval `pyyaml`. Funkce nastartovala úspěšně — ale při prvním volání `target: meteo` selhal `import meteo\_miner` na chybějícím modulu. Cloud Functions zachytí ImportError jako generický 500, Scheduler to zaloguje jako `code: 3`.
* **Fyzikální realita:** `status.code: 3` ve výstupu `gcloud scheduler jobs describe` = funkce vrátila chybu (HTTP 5xx nebo timeout). Scheduler nezná příčinu — ta je pouze v `gcloud functions logs read`. `code: 3` je signál "jdi do logů", ne diagnostika.
* **Korekce (Pravidlo):** Při přidání nového modulu do orchestrátoru zkontrolovat jeho importy a porovnat s `requirements.txt` orchestrátoru — ne s `requirements.txt` modulu (ten může mít vlastní). Reflex: `grep "^import\\|^from" novy\_modul.py` → ověřit každý řádek proti `cat requirements.txt`.

\---

\---

## ZÁZNAM 070: Architektonická volba — Flask standalone vs. modul orchestrátoru

* **Kontext:** meteo\_miner byl vyvinut jako Flask Cloud Run service (`meteo-kbely-ingest`) v době, kdy orchestrátor neexistoval. Při pozdější integraci do orchestrátoru došlo ke konfliktu kontraktů (ZÁZNAM 067). Zpětné hodnocení "neměl nikdy vzniknout jako Flask" bylo nepřesné — ignorovalo kontext vzniku.
* **Fyzikální realita:** Flask standalone Cloud Run a modul orchestrátoru jsou dva legitimní architektonické vzory se zásadně odlišnými kontrakty:

||Flask standalone|Modul orchestrátoru|
|-|-|-|
|**Kdy použít**|Orchestrátor neexistuje|Orchestrátor existuje|
|**Entry point**|HTTP endpoint `@app.route`|Funkce `run\_pipeline()`|
|**Scheduler volá**|Service URL přímo|Orchestrátor s `{"target": "X"}`|
|**Deploy**|`gcloud run deploy` + Dockerfile|`gcloud functions deploy` + `source .`|
|**Přidání dalšího scraperu**|Nová service + nový scheduler job|Nový modul + nová větev v `elif`|

* **Rozhodovací pravidlo (Decision Gate):**

> \*\*Existuje funkční orchestrátor?\*\*
  > - ANO → scraper je čistý modul s `run\_pipeline()`, žádný Flask, žádný vlastní server
  > - NE → Flask standalone Cloud Run je správná volba; po vzniku orchestrátoru migrovat (přepsat na modul, smazat starou service)

* **Chyba nebyla ve vývoji Flask prototypu.** Flask standalone byl tehdy konzistentní replikace fungujícího vzoru na nový cíl — správné rozhodnutí při absenci orchestrátoru. Chyba vznikla v okamžiku integrace: pokus o re-deploy upraveného kódu do existující Flask service místo jejího smazání a přepsání na modul.
* **Korekce (Pravidlo — Migrační protokol):** Při integraci standalone Flask service do orchestrátoru provést vždy v tomto pořadí:

  1. Přepsat kód na čistý modul — odebrat Flask, `app`, `@app.route`, přejmenovat handler na `run\_pipeline()`
  2. Smazat starou Cloud Run service: `gcloud run services delete NAZEV --region europe-west1`
  3. Zkopírovat modul do složky orchestrátoru, přidat větev do `elif`, aktualizovat `requirements.txt`
  4. Re-deploy orchestrátoru
  5. Přidat scheduler job s `{"target": "X"}` — starý job na přímou URL service smazat nebo pausovat
* **Viz také:** ZÁZNAM 067 (port 8080 kontrakt při špatném pořadí migrace).

\---

**F — Orchestrátor pattern (067–070)**
24. Je nový scraper čistý modul s `run\_pipeline()` bez Flask/HTTP serveru? (Prevence 067) — *pouze pokud orchestrátor existuje (viz 070)*
25. Je URI orchestrátoru v scheduler příkazu dosazeno natvrdo z `gcloud run services list`? (Prevence 068)
26. Jsou importy nového modulu ověřeny proti `requirements.txt` orchestrátoru před deploym? (Prevence 069)
27. Existuje orchestrátor? → ANO: modul. NE: Flask standalone. (Prevence 070)
28. Při migraci Flask→modul: smazána stará service PŘED re-deploym? (Prevence 067, 070)

\---

\## ZÁZNAM 071: Inicializační bypass první noci (t0 Night Drop)



\* \*\*Symptom:\*\* SOC prognóza pro den D+1 ráno zobrazovala vyšší hodnotu, než bylo fyzikálně možné. Konkrétně: poslední BMS záznam 89,3 % (562,4 Ah) v 17:04 byl použit jako ranní stav pro 03/18, přestože mezi těmito okamžiky proběhla celá noc se spotřebou.



\* \*\*Příčina:\*\* Funkce `linear\\\_forecast()` přijímala `soc\\\_start` přímo z `load\\\_bms()` a okamžitě ho dosazovala jako `soc\\\_morning` pro první iteraci smyčky. Noční propad (`NIGHT\\\_DROP = 3,0 %`) byl aplikován pouze při přechodech \*uvnitř\* smyčky (D1→D2, D2→D3…), ale vůbec ne na přechod z reálného světa do simulace (BMS→D1).



\* \*\*Fyzikální realita:\*\* Baterie neví, že je v predikčním modelu. Noc mezi 17:04 (konec BMS logu) a 07:00 (start simulace D1) fyzikálně proběhla a spotřeba proběhla. Smyčka musí mít asymetrickou inicializaci: `t0` je zvláštní případ, který nelze ošetřit stejným mechanismem jako ostatní přechody.



\* \*\*Mechanismus selhání LLM (Gemini):\*\* Tři iterace opravy konvergovaly na kosmetické změny (logging, retry), ale nezměnily topologii smyčky. Pattern `for day in days: soc\\\_morning = soc\\\_start` byl v tréninku Gemini tisíckrát viděn jako správný — model ho neopravil, protože syntakticky fungoval a byl konzistentní s nejpravděpodobnějším vzorem.



\* \*\*Korekce (Pravidlo — Inicializační protokol):\*\*

&#x20; 1. `load\\\_bms()` musí vrátit dvě hodnoty: `last\\\_soc` (raw z BMS) a `soc\\\_morning` (po odečtení `NIGHT\\\_DROP`, pokud `last\\\_ts.hour >= MORNING\\\_CUTOFF\\\_HOUR`).

&#x20; 2. `MORNING\\\_CUTOFF\\\_HOUR = 10` — záznamy před touto hodinou jsou ranní (propad již proběhl), záznamy po ní jsou denní/večerní (propad teprve nastane).

&#x20; 3. `linear\\\_forecast()` přijímá `soc\\\_morning\\\_first` — nikdy `last\\\_soc` přímo.

&#x20; 4. Systémový prompt pro LLM musí obsahovat explicitní invariant: `"soc\\\_morning\\\[0] MUST equal last\\\_bms\\\_soc − NIGHT\\\_DROP if last\\\_ts.hour >= CUTOFF"`.



\* \*\*Verifikační test (přidat do každé SOC session):\*\* Pro `last\\\_soc=89,3 %`, `timestamp=17:04` musí být `soc\\\_morning\\\[0]=86,3 %`. Pokud model vrátí 89,3 % jako první ranní hodnotu — iterace je neplatná.



\* \*\*Viz také:\*\* ZÁZNAM 002 (desynchronizace exekuce), ZÁZNAM 066 (Gemini symptom-level opravy bez root cause analýzy).



\---



\## ZÁZNAM 072: LLM Slop Pattern — Prezentační vrstva bez deliverable (ChatGPT)



\* \*\*Symptom:\*\* LLM (ChatGPT GPT-4) vygenerovalo v závěru iterace strukturovaný výstup s emoji headery (`🔴 Root cause`, `✅ Fix`, `🔥 Realita bez iluzí`, `📌 Rychlá diagnostika`), nabídku dalšího kroku a sekci `Bottom line` — ale samotný opravený kód v odpovědi chyběl. Uživatel musel explicitně upozornit: \*"nikde není žádný kód v3.1"\*.



\* \*\*Příčina (mechanická):\*\*

&#x20; 1. \*\*Presentation-reward bias:\*\* RLHF trénink ChatGPT odměňuje vizuálně strukturované odpovědi. Model se naučil, že bohatě formátovaná odpověď = pozitivní hodnocení. Obsah a formát se decouplují — model splnil formální strukturu, ne zadání.

&#x20; 2. \*\*Sycophancy spirála v dlouhém vláknu:\*\* Po opakovaném negativním feedbacku model zvyšoval expresivitu a ujišťovací tón místo opravy problému. `"jo — problém není náhodný"` a `"bez iluzí"` jsou signály optimalizace na snížení frustrace v aktuálním tokenu, ne na řešení.

&#x20; 3. \*\*Over-engineering bias:\*\* Model přidal `MODE = "dry-run"` jako default — feature, která nebyla požadována, ale je asociována s "profesionálními, bezpečnými skripty" v trénovacích datech. Výsledek: skript, který vypadá profesionálně a nic nedělá.

&#x20; 4. \*\*Inkrementální re-architektura na špatném základu:\*\* V3 přearchitekturoval celý skript (přidal `handle\\\_output()`, oddělil klasifikaci od IO) místo opravy konkrétního problému, čímž zavedl nový bug — prázdné složky v dry-run módu.



\* \*\*Fyzikální realita:\*\* LLM optimalizované na širokou uživatelskou základnu generují výstupy, které \*vypadají\* hodnotně (struktura, urgence, nabídka dalších kroků). Pro technické kódové úlohy s fyzikální logikou nebo stavovými přechody je tato optimalizace kontraproduktivní — dramatický tón bez konkrétního řádku kódu je indikátor halucinace, ne kompetence.



\* \*\*Korekce (Pravidlo — ChatGPT workflow):\*\*

&#x20; 1. \*\*Pivot pravidlo:\*\* 2 selhání na stejném problému ve stejném vláknu = konec vlákna. Nové vlákno, čistý kontext, přesnější zadání.

&#x20; 2. \*\*Deliverable-first verifikace:\*\* U kódové odpovědi nejdřív skrolovat na konec — je tam kód? Pokud odpověď obsahuje více textu než kódu → red flag.

&#x20; 3. \*\*Formát v promptu:\*\* `"Výstup: pouze kód. Žádný komentář mimo kód."` — dramaticky snižuje slop u všech modelů.

&#x20; 4. \*\*Kontextová kotva:\*\* `"Zachovej celou strukturu v1. Oprav pouze funkci X. Výstup musí být kompletní spustitelný soubor."` — zabraňuje scope compression i over-engineering.

&#x20; 5. \*\*Dramatický tón = noise, ne signal:\*\* Čím expresivnější jazykový výstup bez konkrétní příčiny v kódu, tím vyšší pravděpodobnost, že model optimalizuje na vzhled odpovědi, ne na správnost.



\* \*\*Viz také:\*\* ZÁZNAM 059 (Gemini diagnostická halucinace — jiný model, stejný pattern dramatického tónu bez substance), ZÁZNAM 056 (token-economy redukce), ZÁZNAM 066 (iterativní selhání bez root cause).



\---



\## ZÁZNAM 073: LLM Model Selection Matrix (Empirická mapa kompetencí)



\* \*\*Kontext:\*\* 14 dní intenzivního vývoje IoT/FVE/scraping kódu napříč třemi modely (Gemini Pro, ChatGPT GPT-4, Claude Sonnet 4.6) odhalilo konzistentní vzory kompetencí a selhání specifické pro každý model.



\* \*\*Fyzikální realita — Srovnávací mapa:\*\*



&#x20; | Failure mode | Gemini Pro | ChatGPT GPT-4 | Claude Sonnet 4.6 |

&#x20; |---|---|---|---|

&#x20; | \*\*Multi-hop causal reasoning\*\* | Slabší, zejména cross-domain | Střední | Silnější |

&#x20; | \*\*Temporální inference\*\* | Slabá (viz 071) | Střední | Silnější |

&#x20; | \*\*Kritická revize vlastní architektury\*\* | Inkrementální opravy | Přearchitekturuje zbytečně | Ochotnější revidovat topologii |

&#x20; | \*\*Reakce na negativní feedback\*\* | Zvyšuje expresivitu, drží chybnou architekturu | Zvyšuje expresivitu, mění architekturu chaoticky | Reviduje s odůvodněním |

&#x20; | \*\*Dlouhé vlákno (degradace)\*\* | Rychlá logická degradace | Rychlá slop degradace | Stabilnější |

&#x20; | \*\*Sycophancy\*\* | Vysoká | Vysoká (dramatický tón) | Nižší — oponuje konstruktivně |

&#x20; | \*\*Over-engineering bias\*\* | Méně časté | Časté | Méně časté |

&#x20; | \*\*Tichá selhání (silent fail)\*\* | Časté (viz 063, 065) | Časté (dry-run default) | Méně časté |

&#x20; | \*\*Fyzikální/IoT domény\*\* | Slabší fyzikální intuice | Slabší fyzikální intuice | Lepší propojení fyziky a kódu |



\* \*\*Korekce (Pravidlo — Model Selection):\*\*

&#x20; - \*\*ChatGPT:\*\* Silný na krátké izolované úlohy (regex, jednofunkční utility, vysvětlení konceptu). Slabý na iterativní vývoj komplexního skriptu se stavovou logikou.

&#x20; - \*\*Gemini Pro:\*\* Silný na strukturovaná data, SQL-like dotazy, přehledové analýzy. Slabý na simulace s fyzikálním stavem v čase a cross-domain causal reasoning.

&#x20; - \*\*Claude Sonnet 4.6:\*\* Preferovaný model pro IoT/FVE simulace, stavové skripty, iterativní vývoj s fyzikální logikou. Vyšší stabilita v dlouhých vláknech.



\* \*\*Viz také:\*\* ZÁZNAM 059, 064, 066 (Gemini failure patterns), ZÁZNAM 072 (ChatGPT slop pattern).



\---



\## ZÁZNAM 074: Kontextová kotva jako prevence LLM regrese (Injekt protokol pro nové session)



\* \*\*Symptom:\*\* Při zahájení nové LLM session bez dostatečného kontextu model generuje řešení konzistentní se svými tréninkovými priory (VM místo Cloud Run, `soc\\\_start` bez night drop, standardní REST místo proprietárního API), přestože byl problém v předchozí session vyřešen.



\* \*\*Příčina:\*\* LLM nemá paměť mezi sekcemi. Každá nová session začíná z distribuce trénovacích dat. Čím méně frekventovaný pattern (proprietární API, inicializační t0 korekce, Cloud Functions Gen2), tím silnější musí být kontextová kotva, aby přebila statistický prior.



\* \*\*Fyzikální realita:\*\* Nestačí popsat, co chceme. Musíme explicitně zakázat to, co nechceme — a dodat falzifikační artefakt (curl output, unit test, verifikační příklad), který model nemůže ignorovat.



\* \*\*Korekce (Pravidlo — Session Injekt Protokol):\*\*

&#x20; ```

&#x20; ARCHITEKTURA: \[Cloud Run / Cloud Functions Gen2 / VM]

&#x20; ZAKÁZÁNO: \[SSH, scp, VM deploy — nebo jiný chybný pattern]

&#x20; OVĚŘENÝ PŘÍKAZ: \[gcloud run deploy ... --source .]

&#x20; FYZIKÁLNÍ INVARIANT: \[soc\_morning\[0] = last\_soc − NIGHT\_DROP if hour >= 10]

&#x20; FALZIFIKAČNÍ TEST: \[Pro vstup X musí být výstup Y — konkrétní číslo]

&#x20; RAW DATA: \[curl output nebo jednotkový příklad]

&#x20; ```

&#x20; Každý z těchto prvků řeší jiný typ LLM selhání:

&#x20; - \*Architektura\* → prevence Prior Dominance (ZÁZNAM 064)

&#x20; - \*Zakázáno\* → prevence pattern inertia (ZÁZNAM 071)

&#x20; - \*Ověřený příkaz\* → prevence halucinace CLI syntaxe (ZÁZNAM 068)

&#x20; - \*Fyzikální invariant\* → prevence temporální inference chyby (ZÁZNAM 071)

&#x20; - \*Falzifikační test\* → detekce silent fail před přijetím jako základ příští iterace (ZÁZNAM 066)

&#x20; - \*Raw data\* → prevence Payload Fabrication (ZÁZNAM 065)



\* \*\*Viz také:\*\* ZÁZNAM 064 (Prior Dominance), ZÁZNAM 065 (Payload Fabrication), ZÁZNAM 066 (iterativní selhání), ZÁZNAM 071 (t0 Night Drop).



\---



\### ⚠️ DIAGNOSTICKÝ FILTR PRO PŘÍŠTÍ ITERACI (aktualizováno v8)



\*\*A — Kód a prostředí (001–023, VM éra)\*\*

1\. Je v hlavičce skriptu kompletní seznam importů? (Prevence 003, 008)

2\. Jsou všechny konstanty definovány na začátku, ne v zápatí? (Prevence 006)

3\. Jsou absolutní cesty ke všem systémovým příkazům (`/sbin/shutdown`)? (Prevence 022)

4\. Existuje `sys.executable` pro volání podskriptů z orchestrátoru? (Prevence 004)



\*\*B — Serverless / Cloud Run (024–036, 043–044, 050)\*\*

5\. Začíná každý run stažením stavu z GCS (`download\\\_master`)? (Prevence 024, 044)

6\. Končí každý run nahráním výsledku do GCS (`upload\\\_master`)? (Prevence 024, 044)

7\. Jsou všechny cesty pro zápis pod `/tmp/`? (Prevence 025)

8\. Obsahuje `gcloud run deploy` příznak `--source .` a správný region? (Prevence 029, 032)

9\. Jsou doplňkové soubory (CSV, config) přibaleny do složky deploymentu? (Prevence 043)



\*\*C — API a scraping (030, 034, 061–065)\*\*

10\. \*\*RAW FIRST:\*\* Byl proveden `curl` s `size: 3` a ověřen klíč dat (`data`/`rows`)? (Prevence 061, 065)

11\. Odpovídá payload přesně curl outputu — všechny klíče, typy (`null` vs `\\\[]`)? (Prevence 061, 065)

12\. Byl ověřen skutečný formát timestamp pole z raw JSON (ISO 8601 vs jiný)? (Prevence 063)

13\. Funguje deduplikační regex na formátu, který parser skutečně generuje? (Prevence 063)



\*\*D — RAG a výstupní kvalita (047, 055, 058, 060, 062)\*\*

14\. Obsahuje YAML front-matter neutrální label (`DETAIL\\\_RAW`), ne implikovanou validaci? (Prevence 060)

15\. Obsahuje metadata `detail\\\_chars` a `detail\\\_truncated`? (Prevence 060)

16\. Obsahuje metadata `lead\\\_score`? (Prevence 058)

17\. Má RAM regex kontextovou kotvu (RAM/DDR/Paměť)? (Prevence 055)

18\. Je aplikována HTML sanitizace (`re.sub`) před exportem do MD? (Prevence 062)

19\. Zůstala sekce Deep Guard / Boolean filtr beze změny po LLM úpravě? (Prevence 056)



\*\*E — LLM workflow (059, 064, 065, 066)\*\*

20\. Byl LLM injekt v nové session obsahující raw data (curl JSON), ne pouze narativ? (Prevence 065, 066)

21\. Byl Cloud Run explicitně specifikován se zákazem VM alternativy? (Prevence 064)

22\. Byl výsledek LLM iterace ověřen audit scriptem před přijetím? (Prevence 066)

23\. Obsahuje LLM diagnóza konkrétní řádek kódu jako příčinu, nebo pouze výstupní symptom? (Prevence 059)



\*\*F — Orchestrátor pattern (067–070)\*\*

24\. Je nový scraper čistý modul s `run\\\_pipeline()` bez Flask/HTTP serveru? (Prevence 067) — \*pouze pokud orchestrátor existuje (viz 070)\*

25\. Je URI orchestrátoru v scheduler příkazu dosazeno natvrdo z `gcloud run services list`? (Prevence 068)

26\. Jsou importy nového modulu ověřeny proti `requirements.txt` orchestrátoru před deploym? (Prevence 069)

27\. Existuje orchestrátor? → ANO: modul. NE: Flask standalone. (Prevence 070)

28\. Při migraci Flask→modul: smazána stará service PŘED re-deploym? (Prevence 067, 070)



\*\*G — Fyzikální simulace a stavové modely (071)\*\*

29\. Je `load\\\_bms()` (nebo ekvivalent) volán s extrakcí `soc\\\_morning` odděleně od `last\\\_soc`? (Prevence 071)

30\. Je `MORNING\\\_CUTOFF\\\_HOUR` definován a aplikován při detekci denního/večerního záznamu? (Prevence 071)

31\. Přijímá simulační smyčka `soc\\\_morning\\\_first` (post-drop), nikoliv raw `last\\\_soc`? (Prevence 071)

32\. Je v systémovém promptu pro LLM explicitní fyzikální invariant pro t0? (Prevence 071, 074)

33\. Byl proveden verifikační test s konkrétními čísly před přijetím výsledku? (Prevence 071)



\*\*H — LLM session management (072–074)\*\*

34\. Obsahuje nová session injekt protokol: architektura + zakázané patterny + ověřený příkaz + fyzikální invariant + falzifikační test? (Prevence 074)

35\. Pokud LLM selhal 2× na stejném problému — bylo zahájeno nové vlákno s čistým kontextem? (Prevence 072)

36\. Je kódová odpověď LLM ověřena deliverable-first (kód přítomen před čtením textu)? (Prevence 072)

37\. Je dramatický tón v LLM odpovědi bez konkrétního řádku kódu vyhodnocen jako halucinace? (Prevence 059, 072)

38\. Odpovídá zvolený LLM model typu úlohy? (IoT/stavová logika → Sonnet; SQL/přehled → Gemini; izolovaná utilita → libovolný) (Prevence 073)



\---

\*pitevni\_kniha\_v8.md — aktualizováno 2026-03-17 — záznamy 001–074\*



