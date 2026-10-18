"""Append D subsections to the preserved C report, without changing historical results."""

import json
import re
from decimal import Decimal
from pathlib import Path

D = Path("rozszerzenia/D")
latest = json.loads((D / "latest.json").read_text())
root = D / latest["root"]
r1 = root / "seria_1"
r2 = root / "seria_2"
st = json.loads((D / "analysis/stats.json").read_text())
tests = D / json.loads((D / "test_latest.json").read_text())["root"]


def link(label, path):
    return f"[{label}]({path})"


def fmt(x, places=None):
    x = Decimal(x)
    if places is not None:
        return f"{x:.{places}f}".replace(".", ",")
    return format(x, "f").replace(".", ",")


def ms(x):
    return fmt(Decimal(x) / 1000000)


def pct(a, b):
    return fmt((Decimal(a) / Decimal(b) - 1) * 100, 2)


text = Path("archiwum_C/raport.md").read_text()
text = text.replace("**A–C, z uzgodnionym odstępstwem danych C**", "**A–D w opisanej adaptacji danych i narzędzi**", 1)
text = text.replace(
    "C wykonano w dwóch kontrolowanych badaniach opisanych poniżej; D nie wykonywano.",
    "C wykonano w dwóch kontrolowanych badaniach opisanych poniżej; D obejmuje badanie harmonogramu kolejności w dwóch seriach.",
    1,
)
text = text.replace(
    "Materiały historyczne A–B zachowano; D nie wykonywano.",
    "Materiały historyczne A–B zachowano; na etapie C nie wykonywano D.",
    1,
)
parts = {}
parts[1] = """### Poziom D - zakres i odstępstwo danych

W D wykonano kontrolowane badanie kolejności: dwa harmonogramy, dwie serie,
80 par i 160 świeżych procesów. Operacja i status uzgodnienia z prowadzącym
pochodzą wprost z aktualnego polecenia użytkownika: ręczna suma odległości od 500,
100 rund. Nie posiadamy odrębnej korespondencji z prowadzącym.

**Rozbieżność danych:** A ma 20 020 wartości. D używa jego dokładnego prefiksu
10 000 wierszy, identycznego z C1. To jawna decyzja interpretacyjna dla D,
nie dodatkowe uzgodnienie z prowadzącym ani twierdzenie, że historyczne A
miało 10 000 liczb. Nie deklaruje się literalnej zgodności z nieistniejącym
plikiem 10 000 z A. Wcześniejsze odstępstwo C2 pozostaje opisane powyżej.

Raport i eksport C zachowano w [archiwum C](archiwum_C/raport.md) oraz
[PDF C](archiwum_C/raport.pdf); odsyłacze tych migawek odnoszą się do pierwotnego
katalogu TiDPI_07. D25–D31 i TC-21–TC-27 są nowymi identyfikatorami.

Źródła D: [C++](rozszerzenia/D/benchmark.cpp), [Python](rozszerzenia/D/benchmark.py),
[przygotowanie](rozszerzenia/D/prepare_D.py), [automat](rozszerzenia/D/run_D.py),
[walidator](rozszerzenia/D/validate_D.py), [niezależna analiza](rozszerzenia/D/analyze_D.py).
Benchmarki są niezmienionymi kopiami wersji C. Plan wymaga nowych harmonogramów,
a nie kolejnych rozszerzeń C. AGENTS.md nadal jest pusty i nie był edytowany.
"""
parts[2] = """### Poziom D - pytanie i hipoteza

Czy przy wspólnych danych i poprawnym wyniku harmonogram zmienia rozkład czasów
oraz relację median Python/C++? Hipoteza D25: harmonogram **może** zmienić oba
opisy; nie zakładano istnienia ani kierunku efektu. Brak powtarzalnej różnicy
również jest wynikiem. Analiza jest opisowa, bez progu istotności i bez wyboru
zwycięzcy z góry. D jest jednym rozszerzeniem: kontrolowanym badaniem harmonogramu;
wykres i metryczki służą temu badaniu.
"""
parts[3] = """### Poziom D - środowisko obu serii

D27 i D28 zapisują rzeczywiste zapytania i wyniki: Apple M4 Pro, arm64,
24 GiB RAM, macOS 27.0.1 (26A434), Apple Clang 21.0.0
(clang-2100.3.34.2), **CPython 3.14.4**, zgodny z A–C. To adaptacja na
macOS/arm64/Clang; nie używano Windows, Visual Studio ani MSVC.

C++ zbudowano raz: `clang++ -std=c++17 -O2 -DNDEBUG`, bez debuggera.
Seria 2 otrzymała kopię tego samego pliku binarnego; hashe obu są identyczne.
W każdym przebiegu są rzeczywiste argv, kody kompilacji/kopiowania i hashe
źródeł oraz binariów. Nie zbierano prywatnej ścieżki instalacji Clanga:
z polecenia wersji od początku przechwytywano wyłącznie pierwsze dwa wiersze.

Zegary (stderr wszystkich procesów): C++ `steady_clock`, `is_steady=1`,
nominalny okres `1/1000000000` s; Python `mach_absolute_time()`, zgłoszona
rozdzielczość około **41,667 ns**. `time_ns` to jednostka zapisu; efektywnej
rozdzielczości C++ ani dokładności eksperymentu nie zmierzono.
"""
parts[4] = """### Poziom D - czynniki i dane

Zmieniany czynnik: naprzemienny albo losowany harmonogram 20 par.
Stałe: maszyna, wspólny prefiks i jego kolejność, źródła, binarny C++ Release,
Python 3.14.4, 100 rund, 2 rozgrzewki i 1 próba w każdym procesie.
Seria jest blokiem replikacji; odwrócono kolejność harmonogramów między seriami.
Pozycja 1/2 jest dodatkowym przekrojem analizy tego samego badania.

D26: dane ASCII/LF, 10 000 liczb, zakres 0…1000. Generator źródła A:
`[i % 1001 for i in range(20020)]`, następnie
`random.Random(20261017).shuffle(values)`; D bierze pierwszych 10 000 wierszy.
Pełny odcisk prefiksu (połączyć dwa wiersze bez spacji):

```text
9e19f79d6545d7af30356b633e33183c7de
db859ad6f9b2f40391ff5a908eb07
```

Właściwy pełny SHA-256 zapisano też w manifeście D26, bez łamania wiersza.
Odcisk danych rozpoznaje plik; checksum obliczeń to **251 042 700**.
Oba procesy każdej pary czytają tę samą kopię pliku. Walidacja odtwarza dane
A i sprawdza tożsamość prefiksu oraz odciski przed i po badaniu.
"""
# fix exact split hash to valid 32 +32
h = json.loads((D / "data_manifest.json").read_text())["sha256"]
parts[4] = parts[4].replace(
    "9e19f79d6545d7af30356b633e33183c7de\ndb859ad6f9b2f40391ff5a908eb07", h[:32] + "\n" + h[32:]
)
parts[5] = """### Poziom D - wzorzec i walidacja

Przed pomiarami D26 wyznaczył niezależnie:
`100 × (500 × 4965 − 1239730 + 3781157 − 500 × 5027)`
= `100 × 2510427` = **251042700**. Osiem wartości równych 500 wnosi zero.
To sumy i liczności partycji, bez funkcji obliczeniowych benchmarków.
D30 później potwierdził wynik z pełnego histogramu innym algorytmem.

Obie implementacje wykonują ręczne pętle: `x − 500`, warunkowa zmiana znaku,
dodanie, 100 rund. Różnica mieści się w −500…500, składnik w 0…500,
a suma i wszystkie sumy pośrednie są nie większe niż
`10000 × 500 × 100 = 500000000 < 9223372036854775807`.
C++ używa `int64_t`; iloczyny kontroli parametrów typu `long long` są bezpieczne
także dla limitu wejścia programu 50 000. Python używa `int`.

Walidator wymaga zgodności pełnego harmonogramu, równowagi pozycji,
niezmienności plików, flag, wersji, poleceń i kolejności zdarzeń bez nakładania
przedziałów monotonicznych. Wymaga kodów 0, dokładnego nagłówka,
jednego rekordu stdout z `trial=1`, całkowitych nieujemnych ns, niezależnego
checksumu i `true`. Sprawdza również obie rozgrzewki każdego procesu.
Metadane serii, harmonogramu, pary, pozycji i parametrów są w oddzielnym planie,
logu wykonania i pochodnym CSV. Kontrakt stdout nie został rozszerzony.

TC-21: nowy audyt źródeł i dowodów A–C oraz zachowanie zastanych plików — zgodne (D25, D30).
TC-22: plan i oba harmonogramy przed pomiarami, dokładne 10+10 kolejności — zgodne (D25).
TC-23: dane, wzorzec, zakres arytmetyki — zgodne (D26, D30).
TC-24: seria 1 i seria 2, każda 80 rekordów i 160 rozgrzewek — zaakceptowane (D27–D28).
TC-25: sześć kontroli walidatora — sześć zgodnych decyzji (D29).
TC-26: każdy wiersz raw/CSV, wszystkie statystyki i wybrane przeliczenia — zgodne (D30).
TC-27: komplet, linki, anonimizacja, render eksportu — wynik D31.

Kontrole D29 to oznaczone **kopie fixture**, nie dodatkowe benchmarki:
poprawna kopia oraz checksum mimo `true`, brak rekordu, zła kolejność planu,
błędna rozgrzewka i nakładające się zdarzenia. Odrzucono pięć wadliwych kopii,
bez `results.csv` ani `warmups.csv` w końcowej serii kontroli.
Pierwsza kontrola ujawniła pozostawanie odziedziczonego CSV rozgrzewek po odrzuceniu.
Poprawiono usuwanie obu plików pochodnych, zachowano stare źródło w dowodach
pierwszej kontroli i ponowiono sześć kontroli oraz walidację obu rzeczywistych serii.
Źródeł benchmarków i surowych pomiarów nie zmieniano; kopie historycznego walidatora
w przebiegach pozostają zachowane. D29 dokumentuje obie wersje i przeniesienie
starego pliku pochodnego do oznaczonego dowodu usterki.
"""
parts[6] = f"""### Poziom D - wykonana procedura

1. Zbadano podstawy A–C, zapisano ich manifest i migawkę raportu C.
   Zapisano plan D25, dane D26, oba harmonogramy i pełne metadane 160 procesów.
   `prepared_at=2026-10-17T11:27:57.547968+02:00`; nie jest to deklaracja
   o powstaniu planów przed dawnymi pomiarami A–C.
2. Pierwsze przygotowanie `{D}/przebiegi/20261017_112757_745453`
   zatrzymało się na zablokowanym `sysctl`, **przed kompilacją i pomiarami**.
   Zachowano strumienie i kod. Po zgodzie wykonano nowy pełny przebieg poza piaskownicą.
3. Seria 1: naprzemienny, potem losowany. Seria 2: losowany, potem naprzemienny.
   Każdy harmonogram ma 20 par. Naprzemienny zaczyna C++/Python; następna para
   Python/C++. Losowany jest tasowaniem listy dziesięciu par każdego rodzaju
   przez `random.Random(20260402).shuffle()`. W obu seriach użyto tego samego
   utrwalonego losowania. Rotacja dotyczy par, odwrócenie harmonogramów — serii.
4. Para oznacza dwa osobne procesy uruchomione kolejno. Każdy czyta plik,
   wykonuje 2 rozgrzewki i 1 próbę; start nowego procesu dla następnej implementacji.
   Nie stosowano celowych przerw, odrzucania skrajnych czasów ani powtórzeń zastępujących.
5. Stoper obejmuje wywołanie `calculate(values)` i jego pętle. Odczyt, importy,
   przygotowanie, walidacja, wypisywanie oraz start/koniec procesu są poza pomiarem.
   Wynik jest obserwowalny i sprawdzany, co nie wyklucza przekształceń optymalizatora.
6. Najpierw zwalidowano obie kompletne serie. Potem D30 osobno odczytał raw,
   przeliczył histogram i statystyki, przygotował CSV wykresu i wykres PGFPlots.
   Wykonano kontrole D29, poprawkę publikacji i ponowną walidację bez nowych pomiarów.
   Uzupełniono wspólny raport i eksport oraz sprawdzono render (D31).

Odtworzenie nowego przebiegu z katalogu `rozszerzenia/D`: `python3 run_D.py`.
Istniejący plan jest niezmienny; `prepare_D.py` odmawia jego nadpisania.
Po nowym przebiegu: `python3 analyze_D.py`, `python3 test_D.py`.
Eksport raportu z katalogu TiDPI_07: `sh rozszerzenia/D/export_D.sh`.
Pełny automat zapisuje osobne katalogi; nie należy nakładać uruchomień benchmarków.
"""
parts[7] = f"""### Poziom D - rejestr dowodów i pełne strumienie

- **D25** — {link("plan D", D / "plan_D.md")}, {link("czas i hashe przygotowania", D / "prepared.json")}, {link("oba harmonogramy", D / "schedules.json")}, {link("metadane wszystkich zaplanowanych procesów", D / "planned_trials.json")}, {link("manifest zastanych plików", D / "preexisting_sha256.json")}, {link("przerwane przygotowanie", D / "przebiegi/20261017_112757_745453/seria_1/exit_codes.txt")}.
- **D26** — {link("dane 10 000", D / "data/input_10000.txt")}, {link("generator, pochodzenie, SHA-256 i wzorzec", D / "data_manifest.json")}.
- **D27** — seria 1: {link("metryczka", r1 / "environment.json")}, {link("kolejność", r1 / "schedule.json")}, {link("polecenia", r1 / "commands.json")}, {link("czasy wykonania procesów", r1 / "execution.json")}, {link("kody", r1 / "exit_codes.txt")}, {link("walidacja", r1 / "validation.json")}, {link("zaakceptowane pomiary", r1 / "results.csv")}, {link("rozgrzewki osobno", r1 / "warmups.csv")}.
- **D28** — seria 2: {link("metryczka", r2 / "environment.json")}, {link("kolejność", r2 / "schedule.json")}, {link("polecenia", r2 / "commands.json")}, {link("czasy wykonania procesów", r2 / "execution.json")}, {link("kody", r2 / "exit_codes.txt")}, {link("walidacja", r2 / "validation.json")}, {link("zaakceptowane pomiary", r2 / "results.csv")}, {link("rozgrzewki osobno", r2 / "warmups.csv")}.
- **D29** — {link("końcowe 6 kontroli walidatora", tests / "summary.json")}, {link("źródło kontroli", D / "test_D.py")}, {link("rejestr poprawki sprzątania CSV", D / "kontrole/cleanup_fix.json")}.
- **D30** — {link("niezależny audyt i rachunki", D / "analysis/independent_check.json")}, {link("statystyki wszystkich przekrojów", D / "analysis/stats.json")}, {link("160 źródłowych punktów wykresu", D / "analysis/plot_data.csv")}, {link("źródło PGFPlots", D / "analysis/distribution.tex")}, {link("skrypt analizy", D / "analyze_D.py")}.
- **D31** — {link("kontrola końcowa", D / "kontrole/final_check.json")}, {link("weryfikator artefaktów", D / "check_D.py")}, {link("manifest plików do oddania", D / "submission_files.txt")}.

Pełne, niezmienione stdout i stderr są zachowane osobno dla każdego procesu,
np. pierwszy stdout C++ serii 1:

```text
naprzemienny_p01_1_cpp_stdout.txt
```

i odpowiadający `stderr.txt`.
Jest 160 par takich plików w D27–D28; puste strumienie narzędzi również zachowano.
Nazwa zawiera harmonogram, parę, pozycję i implementację. `commands.json` i
`execution.json` stanowią pełny indeks. CSV wskazuje dokładny plik i numer wiersza.
Wszystkie właściwe rekordy mają lokalny `trial=1`; tożsamość pomiaru wyznaczają
łącznie seria, harmonogram, para, pozycja i implementacja, nie samo `trial`.
Rozgrzewki pozostają w stderr i osobnym pochodnym `warmups.csv`.

W raporcie nie powiela się 160 pełnych wierszy; komplet znajduje się w linkowanych
strumieniach i CSV. Poniżej wyłącznie **fragment**, pierwsza para D27:

```text
{(r1 / "naprzemienny_p01_1_cpp_stdout.txt").read_text().strip()}
{(r1 / "naprzemienny_p01_2_python_stdout.txt").read_text().strip()}
```
"""
# stats tables are part of requested report artifact, not a separate chat table.
table = [
    "Tabela 6. D: **ms**, 20 pomiarów w każdej grupie; źródła D27–D28, kontrola D30.",
    "",
    "| Seria | Układ | Program | Minimum | Maksimum | Rozstęp | Mediana |",
    "| --- | --- | --- | ---: | ---: | ---: | ---: |",
]
for key, v in st["groups"].items():
    series, s, lang = key.split("/")
    table.append(
        "| "
        + " | ".join(
            [series, "N" if s == "naprzemienny" else "L", "C++" if lang == "cpp" else "Py"]
            + [ms(v[k]) for k in ["min_ns", "max_ns", "range_ns", "median_ns"]]
        )
        + " |"
    )
pt = [
    "Tabela 7. D: pozycje w parze, **ms**, po 10 pomiarów; D30.",
    "",
    "| Grupa | Poz. | Minimum | Maksimum | Rozstęp | Mediana |",
    "| --- | --- | ---: | ---: | ---: | ---: |",
]
for key, v in st["positions"].items():
    ser, s, lang, p = key.split("/")
    pt.append(
        "| "
        + " | ".join(
            [f"{ser}/{'N' if s == 'naprzemienny' else 'L'}/{'C++' if lang == 'cpp' else 'Py'}", p]
            + [ms(v[k]) for k in ["min_ns", "max_ns", "range_ns", "median_ns"]]
        )
        + " |"
    )
rt = [
    "Tabela 8. D: iloraz median **Python/C++** i mediany pozycji **2/1**, bez jednostki; D30.",
    "",
    "| Seria / układ | Python/C++ | C++ poz. 2/1 | Python poz. 2/1 |",
    "| --- | ---: | ---: | ---: |",
]
for ser, s in [("1", "naprzemienny"), ("1", "losowany"), ("2", "losowany"), ("2", "naprzemienny")]:
    prefix = f"{ser}/{s}"
    rt.append(
        "| "
        + " | ".join(
            [
                f"{ser} / {'N' if s == 'naprzemienny' else 'L'}",
                fmt(st["ratios"][prefix + "/python_over_cpp"], 3),
                fmt(st["ratios"][prefix + "/cpp/position_2_over_1"], 3),
                fmt(st["ratios"][prefix + "/python/position_2_over_1"], 3),
            ]
        )
        + " |"
    )
v = st["groups"]["1/naprzemienny/cpp"]
parts[8] = (
    """### Poziom D - rozkłady i rachunki

Nie połączono serii, harmonogramów ani implementacji w jedną statystykę.
N = naprzemienny, L = losowany; S1/S2 = seria; Py = Python. Tabele 6–8 i wykres D30
pochodzą wyłącznie ze 160 zaakceptowanych prób właściwych, bez rozgrzewek.

"""
    + "\n".join(table)
    + "\n\n"
    + "\n".join(pt)
    + "\n\n"
    + "\n".join(rt)
    + f"""

Mediana dla 20 prób jest średnią 10. i 11. czasu po sortowaniu,
a dla 10 prób — 5. i 6. Na przykład D27/N/C++:
`({v["middle_pair_ns"][0]} + {v["middle_pair_ns"][1]}) / 2 = {fmt(v["median_ns"])} ns`
= {ms(v["median_ns"])} ms; rozstęp
`{v["max_ns"]} − {v["min_ns"]} = {v["range_ns"]} ns`.
Minimum to najlepszy zaobserwowany czas, podatny na korzystny przypadek;
mediana opisuje środek tej próby i nie wskazuje jej mechanizmu ani gwarantowanego czasu.

D30 przeliczył niezależnie wszystkie 8 grup i 16 przekrojów pozycji,
porównał każdy surowy rekord z CSV i checksumem histogramowym.
Dodatkowo zapisał dokładne surowe wiersze par **1 i 20**, obu harmonogramów,
obu serii i obu implementacji, oraz ich przeliczenia ns na ms (16 wierszy).
Nie przypisuje się tej kontroli ręcznej pracy użytkownika.

![D30: wszystkie 160 właściwych pomiarów. N - naprzemienny, L - losowany; S1/S2 - serie. Kolor i kształt oznaczają pozycję w parze; czarna kreska to mediana 20 pomiarów. Rozsunięcie poziome według numeru pary służy widoczności punktów. Skale pionowe paneli są różne.](images/D_distribution.png){{width=100%}}

Dane wykresu: [CSV z każdym punktem](rozszerzenia/D/analysis/plot_data.csv).
Oś pozioma zachowuje faktyczną kolejność bloków, a wszystkie punkty mają
osobne współrzędne poziome. Nie usuwano obserwacji skrajnych.
"""
)
cpp1 = pct(st["groups"]["1/losowany/cpp"]["median_ns"], st["groups"]["1/naprzemienny/cpp"]["median_ns"])
py1 = pct(st["groups"]["1/losowany/python"]["median_ns"], st["groups"]["1/naprzemienny/python"]["median_ns"])
cpp2 = pct(st["groups"]["2/losowany/cpp"]["median_ns"], st["groups"]["2/naprzemienny/cpp"]["median_ns"])
py2 = pct(st["groups"]["2/losowany/python"]["median_ns"], st["groups"]["2/naprzemienny/python"]["median_ns"])
parts[9] = f"""### Poziom D - obserwacje bez przypisywania przyczyn

**Obserwacja:** w serii 1 losowany układ ma medianę większą od naprzemiennego
o {cpp1}% dla C++ i {py1}% dla Pythona. W serii 2 różnice wynoszą
odpowiednio {cpp2}% i {py2}%. Kierunek dla Pythona odwrócił się, a skala
różnic obu implementacji między harmonogramami zmalała. Wykres pokazuje
szerokie nakładanie się zakresów i rozrzut, szczególnie w C++.

Iloraz median Python/C++ wynosi w S1: N **215,641**, L **205,587**;
w S2: L **198,808**, N **197,313**. Sposób ułożenia pomiarów współwystępuje
więc z innymi wartościami statystyk, lecz różnica relacji nie zachowuje kierunku
po odwróceniu bloków. Nie wykazano stałej wielkości efektu harmonogramu.

**Pozycja:** C++ ma ilorazy median 2/1: **1,451** i **1,376** w S1,
ale **0,976** i **0,858** w S2 (kolejność bloków jak w Tabeli 8).
Nie ma stabilnej przewagi pierwszej lub drugiej pozycji C++.
Python ma mediany pozycji 2 większe o około **1,24–8,31%** w czterech grupach,
lecz przy tylko 10 obserwacjach na pozycję i nakładających się rozkładach
nie jest to dowód mechanizmu ani uniwersalnego efektu.

**Wniosek opisowy:** wyniki są zgodne z możliwością zmiany obserwowanych rozkładów,
jednak dwie serie nie rozdzielają przekonująco wpływu harmonogramu od trendu
w czasie i zakłóceń. Nie ma podstaw do kategorycznego potwierdzenia przyczynowej
hipotezy ani do stwierdzenia, że kolejność nigdy nie ma znaczenia.
Nie mierzono cache, temperatury, taktowania i procesów tła; nie przypisuje się
im różnic. Wnioski dotyczą tych implementacji, pliku i warunków.
"""
parts[10] = """### Poziom D - ograniczenia projektu

- Jedna maszyna i **dwie serie** z jedną ustaloną permutacją losowaną.
  Po 20 par nie oznacza 20 niezależnych serii. Brak wielu dni, maszyn,
  niezależnych losowań i przedziałów ufności ogranicza siłę wniosku.
- Odwrócenie bloków ogranicza stałe powiązanie harmonogramu z początkiem badania,
  ale dwa bloki w każdej serii nie izolują całego trendu w czasie. Numer pary,
  pozycja, czas i stan systemu nadal mogą współzmieniać wyniki.
- Świeży proces ogranicza przenoszenie stanu samego programu z poprzednich prób,
  ale nie resetuje systemu ani sprzętu. Dwie rozgrzewki są **wewnątrz każdego
  procesu**; nie dowodzą stabilności całego komputera ani usunięcia wszystkich
  efektów uruchomienia. Inicjalizacja i start procesu są poza stoperem,
  mogą jednak zmienić stan przed mierzoną pętlą.
- Stałe 100 rund zachowano zgodnie z poleceniem; krótkie próby C++ mają duży
  względny rozrzut. Jednostka ns i nominalny okres zegara nie oznaczają dokładności 1 ns.
- Nie monitorowano temperatury, cache, zasilania, częstotliwości i obciążenia tła.
  Nie da się przypisać im przyczyn różnic. Zestaw zawiera też pełne koszty
  wywołania mierzonej funkcji, lecz wyklucza odczyt, walidację i wypisywanie.
- Dane to prefiks 20 020-elementowego A, nie historyczny osobny plik 10 000.
  Nie zmieniano historycznego A; odstępstwo oraz wcześniejsze C2 są jawne.
- Fixture walidatora to wybrane mutacje, nie dowód wykrycia wszystkich awarii.
  Pierwsze przygotowanie i usterkę pliku pochodnego zachowano oddzielnie od
  pełnych zaakceptowanych serii; nie zastępowały żadnego niewygodnego pomiaru.
"""
parts[11] = """### Poziom D - wynik i decyzje do obrony

D25–D31 potwierdzają wykonanie rozszerzenia D w opisanej adaptacji danych:
harmonogramy utrwalone przed pomiarami, dwa odwrócone układy bloków,
80 par / 160 właściwych prób i 320 rozgrzewek, walidacja całych zbiorów,
statystyki i wykres wszystkich punktów. Literalnego warunku istnienia osobnego
pliku 10 000 z A nie można potwierdzić; zastosowano jego dokładny prefiks.
Nie obiecuje się oceny ani nie ukrywa odstępstw A–C.

Różnice statystyk wystąpiły, lecz kierunek i skala nie były stabilne między
seriami. Nie wykazano trwałego przyczynowego efektu harmonogramu.

Do wyjaśnienia: **równowaga 10+10** zapobiega trwałemu przypisaniu implementacji
do jednej pozycji; **odwrócenie bloków** ogranicza powiązanie harmonogramu z czasem;
**świeże procesy i 2+1** ustalają ten sam cykl przygotowania każdej obserwacji;
**osobne metadane** zachowują kontrakt i pozwalają wskazać raw;
**niezależny wzorzec** sprawdza poprawność, a SHA-256 tożsamość pliku;
**wszystkie punkty** pokazują rozrzut ukryty przez pojedynczą medianę.
"""
parts[12] = """### Poziom D - udział AI i kontrola końcowa

Codex odczytał cały PDF i zbadał istniejące źródła oraz dowody, przygotował
plan i narzędzia D, wykonał rzeczywiste procesy, naprawił publikację po odrzuceniu,
niezależnie przeliczył wyniki i opracował raport, wykres PGFPlots oraz eksport.
D30 wskazuje dokładny zakres ponownych rachunków; D31 dokumentuje sprawdzenie
linków, anonimizacji i renderu wszystkich stron.

Surowych strumieni nie zmieniano w celu anonimizacji. Metryczki od początku
zbierano bez prywatnych ścieżek. Skany dotyczą treści, logów, metadanych PDF
oraz obrazu wykresu; kod 0 eksportu nie zastąpił przeglądu renderu.
Manifest oddania wyklucza szkolny PDF, `_build` i `__pycache__`.
Nie commitowano, nie pushowano i nie wysyłano niczego zewnętrznie.
"""
# Inject D at end of each existing section; exactly one top-level heading.
sections = list(re.finditer(r"^## (\d+)\..*$", text, re.M))
out = text[: sections[0].start()]
for i, m in enumerate(sections):
    end = sections[i + 1].start() if i + 1 < len(sections) else len(text)
    out += text[m.start() : end].rstrip() + "\n\n" + parts[int(m[1])].strip() + "\n\n"
Path("raport.md").write_text(out)
print("D added to all 12 sections; historical results retained")
