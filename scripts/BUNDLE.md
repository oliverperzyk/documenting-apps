# Pakowanie rozwiązania TiDPI

```sh
bun run bundle TiDPI_01
bun run bundle TiDPI_01 --check
bun run bundle TiDPI_01 --force
bun run test:bundle
```

Skrypt wymaga Bun (sprawdzony na 1.4.0), systemowych `zip` i `unzip`. Brakujące, **zadeklarowane** eksporty raportu głównego tworzy Pandoc; PDF wymaga również XeLaTeX. Nie instaluje narzędzi, nie uruchamia rozwiązań, nie scala raportów poziomów i niczego nie wysyła. YAML odczytuje przez `import { YAML } from "bun"`.

ZIP trafia do `submissions/TiDPI_NN_<kryptonim>.zip`. Ma jeden katalog o tej samej nazwie, zachowujący ścieżki z manifestu. `submission.json` jest dołączany automatycznie. Wszystkie pozostałe pliki pochodzą wyłącznie z listy `artifacts`, nigdy z rekurencyjnego przeglądania rozwiązania.

Nazwy w archiwum mają jawne oznaczenie UTF-8, również przy systemowym `zip` macOS. Skrypt obsługuje jednoczęściowy ZIP32: poniżej 4 GiB i 65535 wpisów; ZIP64 jest odrzucany. Lista nazw jest sprawdzana bezpośrednio w nagłówkach ZIP, a dane przez `unzip` i porównanie bajtów po rozpakowaniu.

## Przygotowanie manifestu

Utwórz `solutions/TiDPI_NN/submission.json`. Poniżej **przykład struktury**, nie gotowe rozwiązanie. Zastąp przykładowy kryptonim swoim przydzielonym kryptonimem i wskazuj faktycznie ukończone prace oraz niezmienione dowody.

```json
{
    "version": 1,
    "task": "TiDPI_01",
    "codename": "KRYPTONIM_TIDPI",
    "levels": [],
    "stages": [1, 2, 3],
    "extensions": [],
    "artifacts": [
        { "path": "raport.md", "role": "report" },
        { "path": "wyniki.log", "role": "raw-results", "evidenceId": "D01" },
        { "path": "raport.docx", "role": "export-docx" },
        { "path": "raport.pdf", "role": "export-pdf" },
        { "path": "environment.log", "role": "log", "shared": "environment" }
    ],
    "pdfRoute": "xelatex",
    "reviewedContentSha256": null
}
```

Przykład poziomu A w zadaniu 02 (te artefakty zastępują listę powyżej, `task` zmienia się na `TiDPI_02`, `levels` na `["a"]`, a pole `stages` znika):

```json
[
    { "path": "raport.md", "role": "report" },
    { "path": "a/raport.md", "role": "level-report", "level": "a" },
    { "path": "a/main.cpp", "role": "source-cpp", "level": "a" },
    { "path": "a/wyniki.log", "role": "raw-results", "level": "a", "evidenceId": "D01" }
]
```

Każdy kolejny ukończony poziom dodaj do ciągu `levels`: `a`, `a–b`, `a–c` albo `a–d`. Dla każdego wymagane są `<poziom>/raport.md`, źródło i surowy log/wyniki z `evidenceId`. Pliki przypisane poziomowi muszą leżeć w jego katalogu. W zadaniach 02–04 źródło każdego poziomu musi mieć rolę `source-cpp`. Nie deklaruj planowanych poziomów. Zadanie 01 zamiast poziomów wymaga wszystkich trzech etapów.

Pola artefaktu:

- `path`: względna ścieżka w katalogu zadania, separatory `/`.
- `role`: jedna z ról opisanych poniżej.
- `level`: opcjonalne `a`, `b`, `c` lub `d` z deklarowanego zakresu.
- `evidenceId`: opcjonalne `D01`, `D02` itd.; raport główny musi cytować wszystkie zadeklarowane identyfikatory. Kilka plików może tworzyć jeden dowód.
- `scenario`: opcjonalna nazwa scenariusza z małych liter, cyfr i myślników. Scenariusz zalicza się tylko przy roli dowodowej i `evidenceId`.
- `shared`: jedyny dozwolony wyjątek to `"environment"` dla `environment.log` o roli `log`, bez `level` i `scenario`. Plik pochodzi wtedy z `solutions/general/environment.log`, a w ZIP jest kopią o nazwie `environment.log`. Sprawdź, czy opisuje środowisko rzeczywiście użyte w tym zadaniu.

Nieznane pola, kolizje nazw (również różniących się wyłącznie wielkością liter), ścieżki absolutne, `..`, dowiązania i nieprzenośne nazwy są błędem. Nie dołączaj katalogów budowania, zależności, plików wykonywalnych, poprzednich ZIP-ów ani szablonów projektu. Materiały szkolne w `pdfs/` są wykluczone; również ich kopia o innej nazwie zostanie odrzucona przy zgodnych bajtach. Nie jest to detektor przerobionych kopii materiałów.

## Role i wymagania zadania

Role raportów to `report` (dokładnie jeden `raport.md`), `level-report` oraz `reproduction` (instrukcja odtworzenia danych w Markdown). Źródła: `source-cpp`, `source-python`, `source`, `generator`, `automation`, `parser`. Źródło C++/Python wymaga właściwego rozszerzenia; oznaczaj rolę zgodnie z rzeczywistą funkcją pliku. Jeżeli generator jest jednym z kodów Python, dodaj osobne źródło implementacji Python, nie powielaj tej samej ścieżki w manifeście.

Role dowodowe to `raw-results`, `log`, `evidence`, `csv`, `chart`, `input` i `reproduction`. `asset` oznacza np. lokalną ilustrację; samo nie spełnia wymogu dowodu. `csv` wymaga `.csv`. Puste `log`/`evidence` są dopuszczalne (np. poprawny pusty stderr); pozostałe artefakty nie mogą być puste.

Eksporty raportu głównego mają role i ustalone nazwy: `export-docx` → `raport.docx`, `export-pdf` → `raport.pdf`, `export-html` → `raport.html`. Opcjonalny `docx-reference` wskazuje jeden referencyjny `.docx`. Eksporty poziomów nie są generowane. Istniejące eksporty są zachowywane; ręcznie sprawdź ich zgodność z MD.

Dodatkowe automatyczne bramki:

- **01:** surowy fikcyjny log z identyfikatorem, deklaracje DOCX i PDF. Raport jawnie opisuje fikcyjność i zawiera `TC-01`–`TC-06`. Rozszerzenia R1–R5 mają `level: "r"` i `evidenceIds`. R1 wymaga `docx-reference` i `evidence`; R2 `source` i `log`; R3 `source-python`, `evidence` i `log`; R4 `source-python` i `log`; R5 `evidence`.
- **02:** wykres na C. Trzy wymagane rodzaje danych C opisuje się w raporcie, nie jako opcjonalne rozszerzenia.
- **03, 04:** wykres na B.
- **05:** `source-cpp`, `automation` i dowody scenariuszy `manual`, `pass-1`, `pass-2`; od B także `run-failure`, `compile-failure`, `restored`.
- **06:** `source-cpp`, `parser`, `csv`, `raw-results` i scenariusz `pass`; od B również `invalid-number`, `missing-field`, `duplicate-row`, `wrong-version`, `failed-test`, `stale-csv`. D wymaga co najmniej dziesięciu różnych scenariuszy dowodowych na poziomie D.
- **07:** `source-cpp`, `source-python`, `generator`, `automation`, `csv`, `log`, co najmniej dwa osobne `raw-results`, wspólne `input` albo `reproduction`, DOCX lub PDF. Scenariusz `run-1`; od B także `invalid` i `run-2`.

Przykładowy artefakt scenariusza: `{"path":"b/failed/stderr.log","role":"log","level":"b","evidenceId":"D04","scenario":"compile-failure"}`. To deklaracja klasy dowodu, **nie automatyczna weryfikacja oczekiwanego kodu czy poprawności eksperymentu**.

Na C w zadaniach 03–07 wpisz przynajmniej dwa rozszerzenia:

- 03: `allocation`, `stack-limit`, `x86-x64`.
- 04: `seeds`, `early-exit`, `almost-sorted`.
- 05: `repeat`, `size`, `file-manifest`.
- 06: `seed-v2`, `completeness`, `csv-escaping`.
- 07: `debug-release`, `sizes`, `warmup`, `library`, `rounds`.

Przykład: `{"id":"allocation","level":"c","evidenceIds":["D08"]}`. Dowody rozszerzenia muszą istnieć i należeć do tego poziomu. D wymaga co najmniej jednego własnego rozszerzenia z opisowym, unikalnym `id`, `level: "d"` i dowodami. Szczegółowe kryteria treści zawsze pochodzą z `AGENTS.md` i `solutions/general/BASE_RAPORT.md`.

## Kontrola i zatwierdzenie

1. Uzupełnij główny raport i raporty poziomów według dwunastu nagłówków ze wspólnego szkieletu. YAML ma tytuł, autora `Kryptonim TiDPI: <kryptonim>`, datę jako tekst `YYYY-MM-DD` i `lang: pl-PL`. Usuń znaczniki szablonu. Lokalne linki, obrazy i odwołania muszą prowadzić do zadeklarowanych plików wewnątrz paczki (raport poziomu może użyć np. `../environment.log`).
2. Uruchom pakowanie. Skrypt wykona kontrolę struktury, prywatności tekstu, podstawowych formatów eksportów oraz DOCX XML. Wygeneruje brakujące eksporty i zachowa stdout, stderr i kody w `.bundle/export-*/logs/`. Każdy proces ma limit 120 sekund. Przy błędzie ZIP nie powstanie.
3. Odczytaj listę plików i proponowany `reviewedContentSha256`. Bez zgodnego skrótu skrypt kończy się błędem, **nie tworząc ZIP-a**.
4. Ręcznie sprawdź wszystkie pliki: zgodność liczb i statystyk z logami, pełne wyniki i kody, zakres zadania, hipotezę, ograniczenia i ujawnienie AI. Otwórz DOCX/PDF; zweryfikuj układ, tabele, wykresy, polskie znaki, brak ucięć oraz zgodność z MD. Sprawdź również metadane, skompresowany tekst PDF, obrazy, zrzuty ekranu i dane osobowe. Detektor automatyczny nie zastępuje tej kontroli.
5. Dopiero po tej kontroli wpisz podany skrót w `reviewedContentSha256` (zamiast `null`) i uruchom ponownie. Skrót uwzględnia konfigurację manifestu poza samym polem zatwierdzenia i bajty każdego artefaktu. Zmiana treści, roli, zakresu lub innego pola wymaga ponownej kontroli. Formatowanie samego JSON nie zmienia skrótu; do ZIP trafia aktualny manifest.
6. Skrypt sprawdzi ZIP, dokładną listę plików, rozpakowane bajty i niezmienność źródeł przed publikacją. Dopiero wtedy poda gotową ścieżkę. Jeśli plik ZIP już istnieje, jawnie użyj `--force`, aby zastąpić tylko ten plik. Awaria kontroli nie zastąpi wcześniejszego ZIP-a.

`--check` nie generuje eksportów, katalogów ani ZIP-a; brakujący eksport to błąd. Sprawdza również aktualność zatwierdzenia. `--check` i `--force` są wzajemnie wykluczające. Kod wyjścia: 0 sukces, 1 niepoprawna lub niezatwierdzona paczka / błąd narzędzi, 2 błędna składnia wywołania.

Domyślny `pdfRoute` to `xelatex`. Dla `pdfRoute: "html"` zadeklaruj HTML i PDF. Skrypt wygeneruje brakujący HTML, lecz zatrzyma się przed brakującym PDF; przygotuj PDF ręcznie z HTML i opisz tę trasę w raporcie. Istniejących eksportów skrypt nie aktualizuje: po zmianie MD przygotuj nowe wersje lub przenieś stare poza katalog zadania przed ponowną generacją, a potem ponownie zatwierdź całą paczkę.

Raporty i surowe logi pozostają bez zmian. Jeżeli oryginalny log zawiera dane osobowe, zatrzymaj go prywatnie i przygotuj osobno opisaną, zanonimizowaną kopię do oddania zgodnie z `AGENTS.md`; skrypt niczego nie redaguje. Zatwierdzenie skrótu jest deklaracją ręcznej kontroli, nie podpisem kryptograficznym, oceną nauczyciela ani gwarancją poprawności merytorycznej.

## Testy

`bun run test:bundle` używa izolowanych, syntetycznych plików w katalogach tymczasowych oraz rzeczywistych `zip`/`unzip`. Eksporty awaryjne są symulowane. Test rzeczywistego Pandoc/XeLaTeX włącz przez `BUNDLE_INTEGRATION=1 bun run test:bundle`; wymaga obu narzędzi w PATH. Dane testowe nie stanowią wyników żadnego zadania szkolnego.
