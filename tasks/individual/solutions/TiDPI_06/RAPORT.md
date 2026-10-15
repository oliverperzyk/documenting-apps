---
title: "TiDPI 06 - Ustrukturyzowany output, parser, CSV i walidacja danych"
author: "Kryptonim TiDPI: Regulus"
date: "2026-10-15"
lang: pl-PL
---

# Sprawozdanie TiDPI 06 — ustrukturyzowany output, parser i CSV

## Kryptonim TiDPI i wykonany poziom

- Kryptonim: **Regulus**.
- Lekcja: **TiDPI 06 — ustrukturyzowany output, parser, CSV i walidacja danych**.
- Zakres: **lokalna część poziomu A oraz wykonane kontrole poziomów B–D**, adaptacja na macOS/arm64 i Apple Clang.
- Data prób: **2026-10-15**. Identyfikatory poszczególnych serii podano w metryczce i rejestrze dowodów.
- [x] A — producent C++ w Release, rzeczywiste 18 rekordów, bezpośredni CSV, parser i niezależna kontrola obu CSV.
- [ ] A — import w Microsoft Excel; niewykonany, ograniczenie opisano w sekcji „Ograniczenia eksperymentu”.
- [x] B — cztery odrzucone kontrakty, poprawne dane z nieudanym testem i dowód usunięcia starego CSV.
- [x] C — kontrakt v2 z `seed` i kontrola kompletności konfigurowana w JSON.
- [x] D — 18 fixture v1, raporty JSON, automat i osiem dodatkowych scenariuszy wykonania.
- Odstępstwa: nie wykonano szkolnej procedury Windows/MSVC ani importu w Excelu. **Pełna realizacja A–D pozostaje niewykazana.** Historyczne testy jednostkowe nie zastępują dowodów B–D.

Podstawą są kontrakt i schemat z materiału TiDPI_06 (s. 2–3), przykład producenta i parsera (s. 5–12) oraz wymagania poziomów A–D (s. 14–16). Z wcześniejszych raportów zachowano sposób organizacji: kryteria, środowisko, procedura, identyfikatory dowodów i ograniczenia. Nie wykonano szkolnej procedury Windows/MSVC.

### Oddane pliki

Układ plików przeznaczonych do przekazania (nazwy katalogów historycznych zachowano):

```text
TiDPI_06/
├── RAPORT.md
├── main.cpp
├── main.py
├── raw_output.txt
├── results.csv
├── results_verified.csv
├── logs/                     — metryczki, źródła i dowody A–C
├── przypadki/                — pięć kontrolowanych przypadków B
└── rozszerzenia/
    ├── C/
    │   ├── seed/             — producent i parser v2 oraz testy
    │   └── kompletnosc/      — producent, parser, konfiguracja i testy
    └── D/
        ├── parse_results.py
        ├── run_fixtures.py
        ├── fixtures/         — 18 sztucznych wejść i manifest
        └── wyniki/           — oddzielne przebiegi i raporty JSON
```

- **A:** [main.cpp](main.cpp), [main.py](main.py), [raw_output.txt](raw_output.txt), [results.csv](results.csv) i [results_verified.csv](results_verified.csv). Nazwa `main.py` zastępuje przykładowe `parse_results.py` z materiału. Kopie danych odpowiadają historycznej serii A.
- **B:** [przypadki/](przypadki/) — wejścia, strumienie i osobne kody producenta oraz parsera (producent w `process_logs.json`).
- **C1:** [seed/](rozszerzenia/C/seed/) — osobne źródła v2 i testy; główny [main.py](main.py) pozostaje parserem v1.
- **C2:** [kompletnosc/](rozszerzenia/C/kompletnosc/) — osobne źródła v1, [expected.json](rozszerzenia/C/kompletnosc/expected.json) i testy.
- **D:** [parse_results.py](rozszerzenia/D/parse_results.py), [run_fixtures.py](rozszerzenia/D/run_fixtures.py), [fixtures/](rozszerzenia/D/fixtures/) i [wyniki/](rozszerzenia/D/wyniki/).
- **Dowody:** [logs/](logs/) — polecenia, metryczki, źródła, strumienie i kontrole A–C; dokładne powiązania D01–D35 zawiera rejestr dowodów.

Nie dołącza się szkolnego PDF, pliku wykonywalnego ani prywatnych materiałów z `_build/`. Nie użyto obrazów, więc katalog `images/` nie jest potrzebny. Nie wykonywano eksportu raportu do DOCX/PDF ani wysyłki zewnętrznej.

### Archiwum wcześniejszych prób i źródeł

Po przeglądzie wymagań PDF scalono pomocnicze logi procesów w `process_logs.json`. Zachowano dokładną treść każdego wpisu, a obowiązkowe strumienie i kody parsera pozostały osobnymi plikami. W D pozostawiono kompletny końcowy przebieg, podsumowania poprzednich prób i szczegółowe dowody wykrytego ujawnienia ścieżki. Usunięto powielone pliki `execution.json`; ich kody są w `parser_exit_code.txt`. [Podsumowanie porządkowania](logs/cleanup.json) podaje zakres zmian i wynik ponownej kontroli automatu. Historyczne manifesty integralności opisują stan sprzed porządkowania.

Po wykonaniu serii usunięto robocze skrypty automatyzacji i testów oraz plik wykonywalny. Ich historyczne źródła pozostały w [sources/](logs/20261015_213621_537968_a/sources/) jako dokumentacja sposobu uzyskania dowodów D01–D07. Zachowano również prywatny oryginał diagnostyki kompilatora; nie jest plikiem tymczasowym ani załącznikiem do oddania.

Pierwotna seria A to `20261015_213621_537968_a`, a kontrole B — `20261015_214715_193570_b`. Końcowa seria C to `20261015_215518_245294_c`; przerwaną próbę `20261015_215452_063831_c` zachowano w D20. Końcowa seria D to `20261015_220614_093174`; podsumowania wcześniejszych prób i dowody usterki opisano w D34. Późniejsze kontrole nie zastępują wyników A.

## Cel i hipoteza — kryteria akceptacji danych

Celem jest sprawdzenie łańcucha: producent C++ → surowy kontrakt → parser Python → zweryfikowany CSV. Dodatkowo producent sam zapisuje CSV; jego pełna zawartość ma być zgodna z wynikiem parsera. Nie badano, który układ danych jest najszybszy.

### Poziom A — poprawny łańcuch danych

Przed kompilacją i pomiarami zapisano [criteria.txt](logs/20261015_213621_537968_a/criteria.txt), dowód D01. Oczekiwano:

1. Kodów kompilacji, producenta i parsera równych 0.
2. Protokołu `TIDPI_RESULTS;1`, dokładnego nagłówka oraz 18 unikalnych rekordów: trzy układy × dwa rozmiary × trzy próby.
3. Pełnej zgodności każdego sortowania z `std::sort`, czyli 18 wartości `correct=true`.
4. Identycznych pól w surowym output i obu CSV, separatora `;`, BOM UTF-8 oraz liczb bez jednostek w komórkach.
5. Liczników `n − 1` dla `sorted` oraz `n × (n − 1) / 2` dla `reversed`.

Kryterium importu w Excelu wyodrębniono jako niewykonane. Sukces kontroli lokalnych nie oznacza spełnienia tego wymagania.

### Poziom B — odrzucenie usterek i zachowanie nieudanego testu

Przed kompilacją B zapisano [criteria.txt](logs/20261015_214715_193570_b/criteria.txt), D09. Oczekiwano kodu parsera 2 i braku CSV dla `invalid-number`, `missing-field`, `duplicate-row`, `wrong-version`; kodu 1 i CSV z jednym `false` dla `failed-test`; oraz usunięcia poprawnego CSV pozostawionego przed `invalid-number`. Dodatkowo zaplanowano odrzucenie nieistniejącego wejścia i regresję zwykłego trybu producenta. To testy decyzji parsera, nie konkurs czasowy.

### Poziom C — wersjonowanie i kompletność

Wybrano dwa badania: dodanie ziarna oraz kontrolę kompletności; pola `note` nie wybrano. Przed kompilacjami obu prób zapisano kryteria, a dla serii końcowej zachowano [criteria.txt](logs/20261015_215518_245294_c/criteria.txt), D19. Dla C1 oczekiwano akceptacji poprawnego v2, odrzucenia obu niezgodności wersji i ujemnego `seed`. Dla C2 oczekiwano akceptacji dokładnie 18 wymaganych tożsamości oraz odrzucenia braku, nadmiaru i `trials=0`. Przed kontrolą braku zaplanowano pozostawienie poprawnego CSV i dowód jego usunięcia.

### Poziom D — niezależne oczekiwania fixture

Przed uruchomieniem parsera D zapisano [manifest fixture](rozszerzenia/D/fixtures/manifest.json) z niezależnie określonymi oczekiwaniami: kodem, obecnością CSV, regułami i wierszami błędów oraz pełnymi wartościami zaakceptowanych rekordów. Każdy przebieg zachowuje jego kopię jako [criteria.json](rozszerzenia/D/wyniki/20261015_220614_093174/criteria.json), D31. Wszystkie 18 wejść to **sztuczne dane dydaktyczne**, nie wyniki pomiarów. Nie zmieniano oczekiwań na podstawie wyników parsera.

Kryterium automatu: zgodność wszystkich 18 fixture i ośmiu dodatkowych scenariuszy, nienaruszenie wcześniejszych materiałów i brak prywatnych ścieżek w wynikach. Kod 1 parsera jest oczekiwanym sukcesem testu F03, natomiast kod 0 automatu oznacza zgodność wszystkich oczekiwań. Automat musi zachować także niezgodności i kontynuować pozostałe próby.

## Środowisko oraz konfiguracja

Tabela 1 — metryczka wykonanych serii, na podstawie D02, D09, D19 i D31.

| Element               | Faktycznie użyta konfiguracja                                                             | Dowód                      |
| --------------------- | ----------------------------------------------------------------------------------------- | -------------------------- |
| System i architektura | macOS 27.0.1, arm64; build 26A434 zapisany w metryczkach A–C                              | D02, D09, D19, D31         |
| C++ w A–C             | Apple Clang 21.0.0; C++17, Release, `-O2 -DNDEBUG -Wall -Wextra -pedantic`; bez debuggera | D03, D09, D19              |
| Python w A–D          | CPython 3.14.4, biblioteka standardowa                                                    | D02, D09, D19, D31         |
| Pomiar producenta     | `steady_clock`, zapis całkowitych mikrosekund; tylko sortowanie z licznikiem              | D03 i źródła producentów   |
| Automat D             | Osobne procesy parsera, limit 10 s; bez kompilacji i pomiarów sortowania                  | D31–D33                    |
| Adaptacja procedury   | Narzędzia macOS zamiast Windows/MSVC; import w Excelu niewykonany                         | D08 i ograniczenia raportu |

### Poziom A — metryczka i ustawienia kompilacji, D02–D03

Metryczka D02: [environment.txt](logs/20261015_213621_537968_a/environment.txt).

- System: macOS 27.0.1, build 26A434; architektura arm64.
- Kompilator: Apple Clang 21.0.0 (`clang-2100.3.34.2`), target `arm64-apple-darwin27.0.0`.
- Python: CPython 3.14.4; parser i automat korzystają wyłącznie z biblioteki standardowej.
- Konfiguracja C++: Release, `-std=c++17 -O2 -DNDEBUG -Wall -Wextra -pedantic`, bez debuggera.
- Początek przebiegu: `2026-10-15T21:36:21.537968+02:00`, strefa Europe/Warsaw.
- Wersje źródeł: [source_sha256.json](logs/20261015_213621_537968_a/source_sha256.json) i [sources/](logs/20261015_213621_537968_a/sources/). Skróty identyfikują bajty użytych źródeł; nie dowodzą ich poprawności.

`-std=c++17` wybiera standard, `-O2` włącza optymalizację, `-DNDEBUG` definiuje `NDEBUG`, a pozostałe flagi włączają diagnostykę. Sam brak debuggera lub makra `_DEBUG` nie określa optymalizacji. Nie użyto MSVC ani Developer PowerShell.

Pełny stdout `clang++ --version` zawiera prywatną ścieżkę instalacji. Oryginał zachowano lokalnie w wyłączonym z załączników `_build/`; metryczka jest osobno przygotowanym wyciągiem obejmującym wyłącznie identyfikację kompilatora i target. Nie zmieniano surowych wyników sortowania. Wyjaśnienie: [compiler_version_stdout_note.txt](logs/20261015_213621_537968_a/compiler_version_stdout_note.txt).

### Metryczka poziomu B — D09

Ponownie sprawdzono narzędzia: [environment.txt](logs/20261015_214715_193570_b/environment.txt). Serię rozpoczęto `2026-10-15T21:47:15.239970+02:00`; użyto macOS 27.0.1, build 26A434, arm64, CPython 3.14.4 i Apple Clang 21.0.0. Kompilacja Release zachowała flagi `-std=c++17 -O2 -DNDEBUG -Wall -Wextra -pedantic`; bez debuggera. [process_logs.json](logs/20261015_214715_193570_b/process_logs.json), wpis `compile_exit_code.txt`, zawiera 0, oba strumienie kompilatora są puste.

Zmieniony producent oraz niezmieniony parser są zapisane w [sources/](logs/20261015_214715_193570_b/sources/), ich skróty w [source_sha256.json](logs/20261015_214715_193570_b/source_sha256.json). Historyczne źródło producenta A pozostaje w D02. Metadane zegara potwierdzono osobnym `--clock-info`; efektywnej rozdzielczości nadal nie mierzono. Pełną diagnostykę wersji kompilatora zachowano prywatnie w `_build/`, a publiczna metryczka jest wyciągiem bez ścieżki instalacji.

### Metryczka poziomu C — D19

[environment.txt](logs/20261015_215518_245294_c/environment.txt) potwierdza macOS 27.0.1, build 26A434, arm64, CPython 3.14.4 oraz Apple Clang 21.0.0. Kontrolę końcową rozpoczęto `2026-10-15T21:55:18.292543+02:00`. Oba źródła skompilowano osobno w C++17 z `-O2 -DNDEBUG -Wall -Wextra -pedantic`, bez debuggera. Obie kompilacje zakończyły się kodem 0 i pustymi strumieniami. Dokładne argumenty i katalogi robocze są w [commands.json](logs/20261015_215518_245294_c/commands.json), skróty czterech nowych źródeł, parsera v1 i konfiguracji w [source_sha256.json](logs/20261015_215518_245294_c/source_sha256.json). Powtórzono `--clock-info`; efektywna rozdzielczość nadal pozostaje niezmierzona. Pełna wersja kompilatora z prywatną ścieżką jest zachowana wyłącznie w pomijanym `_build/`; metryczka jest jawnym wyciągiem.

### Metryczka poziomu D — D31

[environment.json](rozszerzenia/D/wyniki/20261015_220614_093174/environment.json) potwierdza macOS 27.0.1, arm64 i CPython 3.14.4; początek końcowej serii: `2026-10-15T22:06:14.093174+02:00`, Europe/Warsaw. D bada wyłącznie Python i pliki; nie wykonywano nowej kompilacji C++. Wersję interpretera potwierdzono także osobnym procesem w [python_check.json](rozszerzenia/D/wyniki/20261015_220614_093174/python_check.json).

Limit procesu parsera wynosił 10 s. Interpreter zgłaszał `int_max_str_digits=4300`. Nie zmieniano tego ustawienia i nie dodano własnego ograniczenia wartości pól liczbowych v1. Użyto wyłącznie biblioteki standardowej. Źródła, manifest i wszystkie fixture identyfikuje [source_fixture_sha256.json](rozszerzenia/D/wyniki/20261015_220614_093174/source_fixture_sha256.json). Jednostka `time_us` w sztucznych danych nie jest pomiarem D; nie uruchamiano stopera i nie obliczano statystyk czasu dla fixture.

## Zmienne i warunki eksperymentu

### Poziom A — wejścia, kolejność i zakres pomiaru

Zmieniano układ danych (`sorted`, `reversed`, `random`), rozmiar (16, 32) i numer próby (1–3). Stałe były algorytm, typ `int`, kompilacja, komputer i metoda walidacji. W każdej próbie powstaje nowe wejście zawierające permutację liczb od 0 do `size − 1`.

Dla `random` użyto świeżego `std::mt19937` z ziarnem `20260600 + size × 10 + trial` i `std::shuffle`. Dla 16 elementów ziarna wynoszą 20260761–20260763, dla 32 elementów 20260921–20260923; wynikają z formuły w źródle D02. Konkretna permutacja `std::shuffle` zależy także od implementacji biblioteki standardowej; sam seed nie gwarantuje identycznego układu między różnymi toolchainami.

W obrębie każdego rozmiaru rotowano kolejność układów:

1. Próba 1: `sorted`, `reversed`, `random`.
2. Próba 2: `reversed`, `random`, `sorted`.
3. Próba 3: `random`, `sorted`, `reversed`.

Wykonania były sekwencyjne, bez rozgrzewek. Stoper obejmuje wyłącznie Bubble Sort wraz ze zliczaniem porównań. Wyklucza generowanie wejścia, kopiowanie, `std::sort`, porównanie wyników, zapis CSV i drukowanie.

D03, [clock_stdout.txt](logs/20261015_213621_537968_a/process_logs.json): `steady_clock::is_steady=true`, okres typu zegara `1/1000000000 s`, czyli nominalnie 1 ns. **Nie zmierzono efektywnej rozdzielczości zegara ani dokładności pomiaru**; okres typu nie jest takim pomiarem. Wynik jest obcinany do całkowitych mikrosekund. `0 µs` oznacza przedział poniżej jednostki zapisu po tej konwersji, nie zerowy koszt pracy.

### Poziom B — zmieniany tryb emisji

Zmieniano tylko tryb emisji `--fault MODE`. Generator, ziarna, rozmiary, rotacja i kontrola sortowania pozostały jak w A. Usterki są celowe i dotyczą wyjścia po wykonaniu obliczeń. `failed-test` symuluje nieudany test przez wyemitowanie pierwszego `correct=false`; nie jest wykrytą wadą sortowania.

W pięciu trybach awarii producent wypisuje wyłącznie surowy protokół na stdout i **nie tworzy CSV**. Dzięki temu `results.csv` w katalogu przypadku może pochodzić wyłącznie z parsera, poza jawnie pozostawioną kopią starego wyniku w D15. Zwykły tryb bez argumentów nadal bezpośrednio zapisuje CSV.

Producent ma kod 0 dla czterech celowo uszkodzonych kontraktów, 1 dla `failed-test`, a 2 dla nieobsługiwanych argumentów lub błędu wykonania. Kod 0 producenta oznacza zakończenie generowania, nie poprawność kontraktu. Parser podejmuje osobną decyzję według opisanych dalej kodów 0/1/2. Nowe czasy pozostają w surowych plikach B; nie włączono ich do statystyk A.

### Poziom C — zmieniany kontrakt i oczekiwany zbiór

Oba badania mają oddzielne źródła w katalogach rozszerzeń. Główne źródła A–B pozostały bez zmian. Stałe są algorytm, zakresy danych, trzy próby na podstawową grupę, rotacja i granice stopera; sortowanie nadal jest sprawdzane w całości z `std::sort`.

W C1 zmieniono schemat na siedmiopolowy v2. W C2 pozostał v1, natomiast dodano oczekiwany komplet identyfikatorów. Zwykłe uruchomienia producentów zapisują `results.csv` bezpośrednio; parsery zapisują odrębny `results_verified.csv`. Tryby awarii produkują tylko raw. Testy odrzuceń wersji mają osobne katalogi z niezmienionymi kopiami wejść i plikami `input_origin.txt`, więc nie zawierają mylącego CSV producenta.

`missing-row` pomija pierwszy rekord podczas emisji. `extra-row` wykonuje dodatkową rzeczywistą próbę `reversed;32;4` i dodaje jej wynik; nie kopiuje czasu z innej próby. Nowe pomiary C, w tym pierwsza przerwana seria, pozostają w surowych plikach. Nie łączono ich ze statystykami A i nie interpretowano jako porównania wydajności.

### Poziom D — model zagrożeń i warunki

Przedmiotem D jest wiarygodność parsera v1 i publikacji wyników. Model przygotowany z pomocą AI obejmuje:

- Nieobsługiwany protokół i przesunięte kolumny: wersja i kolejność nagłówka muszą być dokładne (F05–F06).
- Cicho pominięty, powielony lub obcy wiersz: kontrola liczby pól, pustych wierszy, powtórzonego nagłówka i tożsamości po konwersji liczb (F07, F11–F13, F16, F18).
- Pozornie poprawne wartości: typy, dolne granice i zamknięte słowniki; zbieranie wielu niezależnych błędów rekordu (F08–F10, F17).
- Pomylenie nieudanego testu z uszkodzeniem formatu: `false` jest legalne i daje kod 1, dopóki reszta kontraktu jest poprawna (F03, F17).
- Stary lub częściowy wynik: przed odrzuceniami pozostawiano poprawny CSV; publikacja następuje dopiero po walidacji całości (F05–F18 i dodatkowy brak wejścia).
- Utrata cyfr: liczby są konwertowane przez `int`, bez pośredniego `float`; F04 sprawdza dokładny zapis 100 cyfr.
- Usunięcie wejścia lub pozorny sukces po awarii I/O: kontrola aliasów oraz osobne scenariusze błędów zapisu CSV i JSON.

Nie jest to model bezpieczeństwa całego systemu plików ani dowód odporności na wyczerpanie zasobów. Parser nie mierzy sortowania i nie ustala prawdziwości deklaracji `correct`; bada kontrakt. Dlatego ogromny licznik w F04 może być poprawnym polem v1, mimo że nie byłby licznikiem tego małego Bubble Sortu.

### Kontrakty danych i diagnostyki

#### A–B i D — kontrakt v1

Surowy plik rozpoczynają dokładnie te dwa wiersze:

```text
TIDPI_RESULTS;1
case;size;trial;time_us;comparisons;correct
```

`TIDPI_RESULTS` jest nazwą protokołu, a `1` jego obsługiwaną wersją. CSV do importu pomija wiersz protokołu i zaczyna się nagłówkiem. Oba CSV mają UTF-8 BOM; parser odczytuje surowy UTF-8 także z BOM. Separator pól to średnik.

- `case`: tekst ze zbioru `sorted`, `reversed`, `random`; układ wejścia.
- `size`: liczba całkowita co najmniej 2; liczba sortowanych elementów.
- `trial`: liczba całkowita co najmniej 1; numer próby.
- `time_us`: liczba całkowita co najmniej 0; czas sortowania w mikrosekundach.
- `comparisons`: liczba całkowita co najmniej 0; liczba porównań sąsiednich elementów.
- `correct`: dokładnie `true` lub `false`; wynik porównania pełnej tablicy z wzorcem.

Tożsamość rekordu tworzy `(case, size, trial)`. Parser odrzuca duplikaty, złą wersję, zmieniony nagłówek, niewłaściwą liczbę pól, błędne typy, zakresy i słowniki oraz pusty zbiór. Nie pomija po cichu błędnych wierszy i nie publikuje częściowego CSV. Zgodnie z PDF konwertuje liczby przez `int()`; nie narzuca dodatkowego kanonicznego zapisu cyfr. Ściślejsza kontrola cyfr w automacie dotyczy emitowanego w tej serii zbioru.

#### C1 — kontrakt v2 z ziarnem

```text
TIDPI_RESULTS;2
case;size;trial;time_us;comparisons;correct;seed
```

Sześć pierwszych pól zachowuje znaczenie i reguły v1. `seed` jest liczbą całkowitą w zakresie **0–4294967295** (zakres `uint32_t`). Dla `random` producent oblicza ziarno raz, przekazuje je do `std::mt19937` i zapisuje tę samą wartość w wyniku. Dla `sorted` i `reversed` wartość 0 oznacza, że generator nie był używany. Pole to nie oznacza losowania z ziarnem 0 dla tych dwóch układów.

Parser v2 ([main.py](rozszerzenia/C/seed/main.py)) akceptuje tylko wersję 2 i dokładny nagłówek siedmiu pól. Zachowuje reguły pozostałych pól, unikalność, obsługę BOM, walidację całego pliku i atomową publikację CSV. Sprawdza zakres ziarna, lecz nie odtwarza generatora ani nie narzuca formuły ziarna dla dowolnego producenta. Zgodność rzeczywistych ziaren tej serii sprawdzono osobno. Parser v1 pozostaje w [głównym main.py](main.py); wersje nie są automatycznie zgadywane.

#### C2 — kontrakt v1 i konfiguracja kompletności

[expected.json](rozszerzenia/C/kompletnosc/expected.json) zawiera konfigurację eksperymentu:

```json
{
    "cases": ["sorted", "reversed", "random"],
    "sizes": [16, 32],
    "trials": 3
}
```

Osobny [parser kompletności](rozszerzenia/C/kompletnosc/main.py) wymaga `--expected-config`. Konfiguracja musi mieć dokładnie te trzy pola. `cases` to niepusta lista unikalnych dozwolonych nazw, `sizes` — niepusta lista unikalnych całkowitych rozmiarów ≥ 2, `trials` — liczba całkowita ≥ 1. Wartości logiczne zamiast liczb, nieznane pola i powtórzone klucze JSON są odrzucane. Próby mają numery od 1 do `trials`.

Oczekiwany zbiór jest iloczynem `cases × sizes × {1,…,trials}`; tutaj ma `3 × 2 × 3 = 18` tożsamości. Dopiero po poprawnej walidacji kontraktu parser porównuje zbiory. Zgłasza brakujące tożsamości, a dla nadmiarowych także wiersz. Brak nie ma własnego wiersza w pliku, dlatego jest wskazywany tożsamością. Każda niezgodność kompletności lub konfiguracji daje kod 2 bez CSV. Oczekiwanej konfiguracji nie można użyć jako pliku wyjściowego; chroni ją ta sama kontrola aliasów co wejście. Stary plik docelowy jest usuwany również przed odrzuceniem błędnej konfiguracji.

#### D — raport walidacji JSON

D zachowuje sześciopolowy protokół v1 i osobny parser. Uruchomienie wymaga jawnego miejsca zapisu raportu:

```sh
python3 parse_results.py input.txt results.csv --report-json validation.json
```

Schemat raportu JSON w wersji 1 obejmuje:

- `schema_version`: 1 — wersja raportu diagnostycznego, niezależna od wersji danych wejściowych.
- `decision`: `accepted`, `failed_tests` lub `rejected`.
- `exit_code`: 0, 1 lub 2; zgodny z kodem procesu.
- `published_records`: liczba opublikowanych rekordów; przy odrzuceniu 0, także gdy część rekordów przeszła walidację.
- `failed_tests`: liczba `false` w opublikowanym zbiorze; przy odrzuceniu 0.
- `csv_created`: wartość logiczna informująca o publikacji CSV przez ten przebieg.
- `errors`: lista obiektów `rule`, `line`, `message`. Wiersze liczy się od 1; `null` oznacza błąd bez konkretnego wiersza, np. odczytu lub zapisu.

Stabilne identyfikatory to m.in. `PROTOCOL`, `HEADER`, `FIELD_COUNT`, `INTEGER`, `RANGE`, `CASE`, `BOOLEAN`, `DUPLICATE`, `BLANK_ROW`, `REPEATED_HEADER`, `READ`, `CSV_SYNTAX`, `EMPTY_DATA`, `PATH`, `OUTPUT`, `REPORT`. Parser zachowuje ogólne sprawdzanie struktury i zakaz wielowierszowych rekordów v1. JSON pozostaje diagnostyką odrzuconego wejścia, a nie częściowym eksportem danych.

Przed usuwaniem plików parser sprawdza parami odrębność wejścia, CSV i JSON, również przez `resolve()` i `samefile()`. Niebezpieczne argumenty dają kod 2 oraz stderr `PATH` bez modyfikowania chronionego wejścia i bez zapisywania JSON w kolidującym miejscu. Przy normalnych ścieżkach wcześniejsze pliki docelowe są usuwane. CSV i JSON zapisuje się przez osobne pliki tymczasowe i atomową zmianę nazwy. Jeśli po utworzeniu CSV zawiedzie wymagany JSON, parser usuwa CSV, nie drukuje sukcesu i zwraca 2.

Błąd niemożliwego zapisu JSON nie może zostać zapisany do tego samego niedostępnego JSON; wtedy dowodem jest stderr i kod procesu. Jeśli zapis JSON jest dostępny, błąd CSV otrzymuje raport `rejected`, kod 2 i `csv_created=false`. Przyczyna I/O jest zapisywana bez nazwy pliku, aby diagnostyka biblioteki nie ujawniała prywatnych ścieżek.

## Kontrola poprawności

**Producent:** przed pomiarem tworzy kopię wejścia i sortuje ją przez `std::sort`. Po pomiarze porównuje pełne wektory operatorem `==`. Wzorzec jest niezależny od ręcznie zaimplementowanego Bubble Sortu. W tej serii, ponieważ wejścia są permutacjami, oczekiwany wynik to `0…15` albo `0…31`. Samo sprawdzenie rosnącej kolejności nie wykryłoby utraconych lub powielonych elementów.

**Parser:** kontroluje odczyt i kontrakt, lecz nie odtwarza sortowania. `correct=true` jest deklaracją producenta potwierdzoną przeglądem jego kontroli pełnych wyników. Kod 0 oznacza poprawny zbiór z samymi `true`; kod 1 oznacza poprawny zbiór z co najmniej jednym `false`, przy zachowanym CSV; kod 2 oznacza błąd wejścia, kontraktu lub zapisu. Przed walidacją usuwa wcześniejszy plik docelowy, sprawdzając wcześniej, że nie jest on wejściem. Publikację wykonuje atomowo dopiero po walidacji całości.

**Bezpośredni CSV C++:** dane liczbowe i zamknięte słowniki v1 nie zawierają średników, cudzysłowów ani nowych wierszy w polach; dlatego jawne wypisywanie tych pól jest w tej wersji wystarczające. Dodanie dowolnego tekstu wymagałoby kodowania CSV. Producent odmawia nadpisania istniejącego `results.csv` lub `results.csv.tmp`; zamyka kompletny plik tymczasowy przed zmianą nazwy. W zwykłym trybie błąd zapisu daje kod 2 i stderr, a niezgodny wynik sortowania — kod 1. W serii A kod producenta wyniósł 0; dodatkowy kod 1 w trybie `failed-test` jest jawną symulacją B.

**Niezależny odczyt D06:** automat nie importuje badanego parsera. Ponownie czyta oba CSV modułem `csv`, sprawdza wszystkie pola, pełen oczekiwany zbiór identyfikatorów oraz zgodność z surowymi rekordami. Kontrola kompletności jest tu kontrolą tej konkretnej serii, nie rozszerzeniem kontraktu poziomu C. Wynik: 18 rekordów, 18 unikalnych identyfikatorów, 18 `true`, zgodność obu CSV i danych surowych — [verification.txt](logs/20261015_213621_537968_a/verification.txt).

### Parsowanie a walidacja

Rzeczywisty wiersz 3 z D04 to `sorted;16;1;0;15;true`. Parsowanie dzieli go na sześć komórek. Walidacja sprawdza m.in., czy `16` jest liczbą całkowitą ≥ 2, `sorted` należy do słownika, a tożsamość nie jest powtórzona.

**Przykład dydaktyczny, nie wynik eksperymentu:** `random;dużo;1;5;120;true` nadal daje sześć pól podczas parsowania, lecz walidacja odrzuca `size=dużo`. Z kolei poprawnie zapisane `correct=false` opisuje nieudany test i nie jest uszkodzeniem formatu. Takiego rekordu nie było w rzeczywistym zbiorze D04.

## Procedura

### Poziom A — poprawny przebieg i kontrola CSV

1. Ponownie odczytano wymagania PDF i porównano strukturę wcześniejszych raportów. Zachowano istniejący parser i jego testy.
2. Dodano producenta i automat. Automat zapisał D01 przed kompilacją oraz skopiował źródła i ich skróty do nowego katalogu dowodów.
3. Sprawdzono narzędzia, zbudowano producenta Release, odczytano metadane zegara przez `--clock-info`, a następnie wykonano jedną serię 18 prób bez debuggera.
4. Producent zapisał `results.csv`; stdout przechwycono bez zmian jako `producer_stdout.txt` i `raw_output.txt`. Zachowano także stderr i kod procesu.
5. Uruchomiono parser na surowym pliku z odrębnym celem `results_verified.csv`. Zachowano oba strumienie i kod.
6. Wykonano niezależny odczyt, kontrolę kompletu, porównanie wszystkich wartości, obliczenie statystyk i istniejące testy parsera. Kopie trzech plików danych w katalogu zadania są identyczne z plikami serii.
7. Kontrolę tekstową i podgląd raportu opisuje D08. Importu w Excelu nie wykonano.

Ręczne odtworzenie z katalogu zadania (nowy katalog na każdy przebieg; polecenia poniżej są instrukcją, nie dodatkowo wykonaną serią):

```sh
mkdir -p _build
clang++ -std=c++17 -O2 -DNDEBUG -Wall -Wextra -pedantic main.cpp -o _build/tidpi06
mkdir runs
cd runs
../_build/tidpi06 > raw_output.txt 2> producer_stderr.txt
producer_code=$?
printf '%s\n' "$producer_code" > producer_exit_code.txt
python3 -B ../main.py raw_output.txt results_verified.csv > parser_stdout.txt 2> parser_stderr.txt
parser_code=$?
printf '%s\n' "$parser_code" > parser_exit_code.txt
cd ..
```

Jeżeli `runs` już istnieje, należy wybrać nową nazwę i nie wykonywać kolejnych poleceń w starym katalogu. Producent tworzy `results.csv` w swoim katalogu roboczym. Przed przejściem do następnego etapu należy sprawdzić kod kompilacji i producenta. Powyższa instrukcja nie podmienia danych opisanej serii. Oryginalny automat i jego polecenia pozostają w dowodach historycznych; nie jest już potrzebny do zwykłego uruchomienia producenta i parsera.

Rzeczywiste polecenie kompilacji D03, z katalogu zadania:

```sh
clang++ -std=c++17 -O2 -DNDEBUG -Wall -Wextra -pedantic logs/20261015_213621_537968_a/sources/main.cpp -o _build/20261015_213621_537968_a/tidpi06
```

Producent był wywołany z nowego katalogu dowodów; dokładna lista argumentów jest w [producer_command.json](logs/20261015_213621_537968_a/process_logs.json). Rzeczywiste polecenie parsera D05, z katalogu zadania:

```sh
python3 -B logs/20261015_213621_537968_a/sources/main.py logs/20261015_213621_537968_a/raw_output.txt logs/20261015_213621_537968_a/results_verified.csv
```

### Poziom B — kontrolowane ścieżki niepowodzenia

1. Zapisano kryteria i identyfikację źródeł, ponownie sprawdzono środowisko i zbudowano Release. Dokładne listy argumentów i katalogi robocze są w [commands.json](logs/20261015_214715_193570_b/commands.json). Procesy uruchamiano kolejno z listą argumentów, `shell=False`, przechwyceniem obu strumieni i kodu oraz limitem 60 s.
2. Wykonano kolejno `invalid-number`, `missing-field`, `duplicate-row`, `wrong-version`, a potem `failed-test`. stdout producenta zapisano bez zmian jako `raw_output.txt` w odrębnym katalogu każdego przypadku; stderr i kod zachowano osobno. Nie poprawiano surowych wejść ręcznie.
3. Przed parserem pierwszego przypadku pozostawiono poprawny CSV z A i zapisano jego obecność, skrót i kontrolę wszystkich 18 wartości `correct=true`. Po odrzuceniu sprawdzono brak pliku. Oryginał A pozostał bez zmian.
4. Parser czytał wejście i zapisywał `results.csv` w tym samym katalogu przypadku; zachowano jego stdout, stderr i kod. Dla `failed-test` niezależnie odczytano cały CSV i porównano wszystkie pola z raw, 18 tożsamości i dokładnie jeden `false`.
5. Osobno sprawdzono nieistniejące wejście. W nowym katalogu wykonano także regresję zwykłego producenta i parsera: kody 0, zgodne CSV i komplet 18 rekordów. Sprawdzono zachowanie `--clock-info` oraz odrzucenie nieznanego trybu kodem 2.
6. Porównano skróty wszystkich wcześniejszych plików dowodowych A, trzech głównych plików danych i parsera przed B i po B. Wszystkie pozostały identyczne. Usunięto wygenerowany program wykonywalny; nie dodano nowego stałego skryptu pomocniczego.

Przykład odtworzenia jednego przypadku po kompilacji aktualnego `main.cpp`, z nowego katalogu roboczego obok pozostałych przypadków:

```sh
../../_build/tidpi06 --fault invalid-number > raw_output.txt 2> producer_stderr.txt
producer_code=$?
printf '%s\n' "$producer_code" > producer_exit_code.txt
python3 -B ../../main.py raw_output.txt results.csv > parser_stdout.txt 2> parser_stderr.txt
parser_code=$?
printf '%s\n' "$parser_code" > parser_exit_code.txt
```

Zastąpienie trybu pozwala odtworzyć pozostałe przypadki. Należy używać świeżych katalogów, nie nadpisywać oddanych dowodów oraz sprawdzać kod producenta osobno od kodu parsera. Test starego CSV wymaga przed parserem kopii poprawnego pliku z A i osobnej kontroli obecności przed oraz po wykonaniu.

### Poziom C — dwa rozszerzenia kontraktu

1. Ponownie przeczytano wymagania, przygotowano osobne źródła i konfigurację, a przed wykonaniem zapisano kryteria. Procesy uruchamiano sekwencyjnie, z listą argumentów, `shell=False`, przechwyceniem strumieni i kodów oraz limitem 60 s.
2. Pierwszą kontrolę C przerwano przy sprawdzaniu odrzucenia v1 przez parser v2: kod wyniósł prawidłowe 2, lecz diagnostyka mylnie podawała oczekiwaną wersję 1. Zachowano źródło sprzed poprawki i wszystkie powstałe dane oraz logi (D20). Poprawiono wyłącznie komunikat i wykonano nową serię; wcześniejszych wyników nie zastąpiono.
3. W serii końcowej wykonano cztery testy C1 i cztery testy C2. W katalogach testów są wejścia, strumienie i kody parserów. Dla generowanych wejść zachowano także stderr i kod producenta; przy skopiowanych wejściach `input_origin.txt` wskazuje oryginalny przebieg producenta. Pełne polecenia są w D19.
4. Poprawne CSV odczytano niezależnie modułem `csv`, bez importowania badanych parserów. Porównano wszystkie pola obu eksportów z raw, BOM i pełen zbiór 18 identyfikatorów; dla v2 także wszystkie wartości `seed`. Sprawdzono pełne wyniki producenta, pola liczbowe i wzory liczników dla `sorted`/`reversed`.
5. Przed testem `missing-row` skopiowano poprawny zweryfikowany CSV C2 i zapisano zgodne skróty oraz obecność. Po kodzie 2 potwierdzono brak pliku (D29).
6. Dodatkowo sprawdzono pięć granic i typów `seed` oraz 12 konfiguracji funkcji walidującej. Są to jawnie syntetyczne fixture z wejściami i wynikami w JSON, nie pomiary generatora i nie realizacja D. Zachowano zbiorcze strumienie i kody tych kontroli.
7. Skróty wcześniejszych źródeł, danych i logów A–B porównano przed C i po C. Pozostały bez zmian. Programy wykonywalne usunięto po sprawdzeniu; nie dodano stałego skryptu automatyzacji.

Przykładowe polecenia parserów z katalogu zadania (odtwarzanie w nowych katalogach, bez nadpisywania dowodów):

```sh
python3 -B rozszerzenia/C/seed/main.py raw_v2.txt verified_v2.csv
python3 -B main.py raw_v2.txt rejected_v1.csv
python3 -B rozszerzenia/C/kompletnosc/main.py raw_v1.txt verified_complete.csv --expected-config rozszerzenia/C/kompletnosc/expected.json
```

Nazwy `raw_v2.txt` i `raw_v1.txt` są nazwami wejść do zastąpienia, nie dodatkowymi załącznikami. Producentów buduje się jak w A, wybierając odpowiedni plik C++ w katalogu badania i nowy katalog roboczy. Kontrolowane wejścia otrzymuje się przez `--fault invalid-seed`, `--fault missing-row` lub `--fault extra-row`. Rzeczywiste polecenia i lokalizacje tej serii są w D19.

### Poziom D — automatyczne wykonanie fixture

1. Utworzono osobny parser, 18 plików fixture i niezależny manifest oczekiwań. Automat wykonano z katalogu D przez `python3 -B run_fixtures.py`; każde wywołanie tworzy nowy katalog `wyniki/`.
2. Każdy parser uruchamiano osobno i sekwencyjnie, z listą argumentów, `shell=False`, przechwytywaniem stdout/stderr, `check=False` i limitem 10 s. Dla każdej próby zachowano `command.json`, oba strumienie, kod procesu, stan przed i po oraz `comparison.json`.
3. Przed każdym z 14 odrzuceń fixture kopiowano zweryfikowany CSV F01. Sprawdzano jego skrót i obecność przed próbą, brak po niej oraz nienaruszenie wejścia. To samo wykonano przy dodatkowym braku wejścia. CSV pierwszego testu musi najpierw przejść niezależną kontrolę — inaczej automat oznacza brak wiarygodnego przygotowania próby.
4. Automat porównywał rzeczywisty kod z manifestem, dokładną strukturę JSON, decyzję, liczniki, listę reguł i wierszy oraz fragmenty komunikatów na stderr. Dla akceptacji odczytywał CSV niezależnie modułem `csv`, sprawdzał BOM, nagłówek, wszystkie komórki i oczekiwany stdout. Weryfikacja nie importuje badanego parsera.
5. Dodatkowo wykonano brak wejścia, pięć kolizji ścieżek/aliasów oraz błędy zapisu CSV i JSON. Dowiązania były tworzone tylko do kopii fixture, następnie usuwane po potwierdzeniu ochrony jej bajtów.
6. Pierwszy przebieg spełnił 26 kryteriów funkcjonalnych, lecz przegląd wykrył prywatną ścieżkę w komunikatach `tempfile`. Oryginały zachowano prywatnie; publiczny katalog pierwszej próby jest oznaczoną kopią z redakcją, nie niezmienionym raw (D34). Poprawiono diagnostykę i powtórzono testy. Następnie dodano kontrolę prywatnych ścieżek do automatu i wykonano końcowy przebieg D32–D33.
7. Końcowy automat zwrócił 0, wszystkie 26 porównań było zgodnych, wcześniejsze materiały A–C nie zmieniły się, a kontrola anonimizacji przeszła. Nie mierzono czasów D, nie uruchamiano nowego C++ i nie wygenerowano eksportów raportu.

Odtworzenie z katalogu zadania:

```sh
python3 -B rozszerzenia/D/run_fixtures.py
```

Automat pozostaje w rozwiązaniu, ponieważ wymaga go poziom D. Nie nadpisuje starszych przebiegów i nie przepisuje manifestu. Niezgodność pojedynczej próby, brak/niepoprawny JSON, nieoczekiwany kod, awaria lub timeout są zachowywane i nie blokują wykonania kolejnych przypadków; końcowy kod automatu wynosi wtedy 1. Kontrolę kompletności plików i samego raportu wykonano także po serii (D35).

## Surowe wyniki

### Rejestr dowodów

Dowody pozostają przypisane do pierwotnych serii; późniejsze poprawki mają własne identyfikatory.

#### Poziom A — D01–D08

- **D01:** [criteria.txt](logs/20261015_213621_537968_a/criteria.txt) — kryteria ustalone przed wykonaniem.
- **D02:** [environment.txt](logs/20261015_213621_537968_a/environment.txt), [source_sha256.json](logs/20261015_213621_537968_a/source_sha256.json) i [sources/](logs/20261015_213621_537968_a/sources/) — środowisko i użyte źródła.
- **D03:** [process_logs.json](logs/20261015_213621_537968_a/process_logs.json) — kompilacja i metadane zegara. Oba strumienie kompilacji są puste, kod 0.
- **D04:** [raw_output.txt](logs/20261015_213621_537968_a/raw_output.txt), [process_logs.json](logs/20261015_213621_537968_a/process_logs.json), [results.csv](logs/20261015_213621_537968_a/results.csv) — rzeczywiste wyniki producenta; stderr pusty, kod 0.
- **D05:** [parser_stdout.txt](logs/20261015_213621_537968_a/parser_stdout.txt), [parser_stderr.txt](logs/20261015_213621_537968_a/parser_stderr.txt), [parser_exit_code.txt](logs/20261015_213621_537968_a/parser_exit_code.txt), [results_verified.csv](logs/20261015_213621_537968_a/results_verified.csv) — wynik parsera; stderr pusty, kod 0.
- **D06:** [verification.txt](logs/20261015_213621_537968_a/verification.txt), [summary.json](logs/20261015_213621_537968_a/summary.json) — niezależny odczyt, komplet i statystyki.
- **D07:** [process_logs.json](logs/20261015_213621_537968_a/process_logs.json) — sześć zakończonych sukcesem testów technicznych; unittest wypisuje wynik na stderr.
- **D08:** [review.txt](logs/20261015_213621_537968_a/review.txt) — kontrola tekstu, podglądu, arytmetyki, odwołań i anonimizacji.

#### Poziom B — D09–D18

- **D09:** [criteria.txt](logs/20261015_214715_193570_b/criteria.txt), [environment.txt](logs/20261015_214715_193570_b/environment.txt), [sources/](logs/20261015_214715_193570_b/sources/), [source_sha256.json](logs/20261015_214715_193570_b/source_sha256.json), [commands.json](logs/20261015_214715_193570_b/commands.json), [process_logs.json](logs/20261015_214715_193570_b/process_logs.json) — przygotowanie i kompilacja B.
- **D10:** [invalid-number](przypadki/invalid-number/) — wejście, strumienie, polecenie odtworzone w D09 i osobne kody producenta oraz parsera.
- **D11:** [missing-field](przypadki/missing-field/) — odrzucenie rekordu z pięcioma polami.
- **D12:** [duplicate-row](przypadki/duplicate-row/) — powtórzona tożsamość w wierszu 21.
- **D13:** [wrong-version](przypadki/wrong-version/) — odrzucenie wersji 99.
- **D14:** [failed-test](przypadki/failed-test/), [results.csv](przypadki/failed-test/results.csv) — poprawny format, jeden nieudany test i zachowany wynik.
- **D15:** [stale_csv_before.txt](logs/20261015_214715_193570_b/stale_csv_before.txt), [stale_csv_after.txt](logs/20261015_214715_193570_b/stale_csv_after.txt) — poprawny stary CSV przed D10 i brak po odrzuceniu.
- **D16:** [read-error/](logs/20261015_214715_193570_b/read-error/) — brak wejścia; zachowane strumienie i kod parsera.
- **D17:** [outcomes.json](logs/20261015_214715_193570_b/outcomes.json), [verification.txt](logs/20261015_214715_193570_b/verification.txt), [level_a_integrity.json](logs/20261015_214715_193570_b/level_a_integrity.json), [baseline/](logs/20261015_214715_193570_b/baseline/) — niezależne kontrole decyzji, danych, nienaruszenia A i regresja zwykłego trybu.
- **D18:** [review.txt](logs/20261015_214715_193570_b/review.txt) — końcowy przegląd odwołań, anonimizacji i prezentacji B.

#### Poziom C — D19–D30

- **D19:** [criteria.txt](logs/20261015_215518_245294_c/criteria.txt), [environment.txt](logs/20261015_215518_245294_c/environment.txt), [source_sha256.json](logs/20261015_215518_245294_c/source_sha256.json), [commands.json](logs/20261015_215518_245294_c/commands.json), [process_logs.json](logs/20261015_215518_245294_c/process_logs.json) — plan, źródła i rzeczywiste wykonania. Strumienie i kody kompilacji oraz zegarów scalono w `process_logs.json` w tym samym katalogu.
- **D20:** [attempt_status.txt](logs/20261015_215452_063831_c/attempt_status.txt), [pierwszy parser v2](logs/20261015_215452_063831_c/seed_parser_before_fix.py), [pierwsze wejścia i logi](logs/20261015_215452_063831_c/seed_tests_before_fix/) — zachowana przerwana próba. Oryginalne polecenia wskazują lokalizacje sprzed przeniesienia tych materiałów do archiwum.
- **D21:** [poprawne-v2](rozszerzenia/C/seed/testy/poprawne-v2/), [raw_output.txt](rozszerzenia/C/seed/testy/poprawne-v2/raw_output.txt), [results_verified.csv](rozszerzenia/C/seed/testy/poprawne-v2/results_verified.csv) — akceptacja i siedem zachowanych pól.
- **D22:** [v1-odrzuca-v2](rozszerzenia/C/seed/testy/v1-odrzuca-v2/) — niezmienione wejście D21 odrzucone przez główny parser v1.
- **D23:** [invalid-seed](rozszerzenia/C/seed/testy/invalid-seed/) — kontrolowane `seed=-1`.
- **D24:** [v2-odrzuca-v1](rozszerzenia/C/seed/testy/v2-odrzuca-v1/) — niezmienione wejście A odrzucone przez parser v2.
- **D25:** [poprawne](rozszerzenia/C/kompletnosc/testy/poprawne/), [results_verified.csv](rozszerzenia/C/kompletnosc/testy/poprawne/results_verified.csv) — komplet v1 zgodny z konfiguracją.
- **D26:** [missing-row](rozszerzenia/C/kompletnosc/testy/missing-row/) — brak pierwszej tożsamości.
- **D27:** [extra-row](rozszerzenia/C/kompletnosc/testy/extra-row/) — dodatkowa rzeczywista próba 4.
- **D28:** [invalid-config](rozszerzenia/C/kompletnosc/testy/invalid-config/), [expected_invalid.json](rozszerzenia/C/kompletnosc/testy/invalid-config/expected_invalid.json) — odrzucenie `trials=0` na poprawnym wejściu D25.
- **D29:** [outcomes.json](logs/20261015_215518_245294_c/outcomes.json), [verification.txt](logs/20261015_215518_245294_c/verification.txt), [stale_csv_before.txt](logs/20261015_215518_245294_c/stale_csv_before.txt), [stale_csv_after.txt](logs/20261015_215518_245294_c/stale_csv_after.txt), [previous_integrity.json](logs/20261015_215518_245294_c/previous_integrity.json), [seed_validation.json](logs/20261015_215518_245294_c/seed_validation.json), [config_validation.json](logs/20261015_215518_245294_c/config_validation.json) — komplet decyzji, niezależne kontrole, zachowanie A–B i dodatkowe fixture. Zbiorcze strumienie i kody kontroli funkcji są wpisami z prefiksami `seed_validation_` i `config_validation_` w `process_logs.json` w tym samym katalogu.
- **D30:** [review.txt](logs/20261015_215518_245294_c/review.txt) — końcowy przegląd C.

#### Poziom D — D31–D35

- **D31:** [manifest.json](rozszerzenia/D/fixtures/manifest.json), [criteria.json](rozszerzenia/D/wyniki/20261015_220614_093174/criteria.json), [environment.json](rozszerzenia/D/wyniki/20261015_220614_093174/environment.json), [python_check.json](rozszerzenia/D/wyniki/20261015_220614_093174/python_check.json), [source_fixture_sha256.json](rozszerzenia/D/wyniki/20261015_220614_093174/source_fixture_sha256.json) — niezależne oczekiwania i identyfikacja badanego kodu oraz wejść.
- **D32:** [wyniki fixture F01–F18](rozszerzenia/D/wyniki/20261015_220614_093174/) — każdy podkatalog Fxx zawiera polecenie, strumienie, kod, raport JSON, porównanie i stan przed/po. Manifest wskazuje odpowiadający mu plik wejściowy. Szczególne przykłady: [F03 — JSON](rozszerzenia/D/wyniki/20261015_220614_093174/F03/validation.json), [F04 — CSV](rozszerzenia/D/wyniki/20261015_220614_093174/F04/results.csv), [F10 — sześć błędów](rozszerzenia/D/wyniki/20261015_220614_093174/F10/validation.json), [F18 — brak częściowego CSV](rozszerzenia/D/wyniki/20261015_220614_093174/F18/after.json).
- **D33:** [wersja automatu użyta w końcowej serii](rozszerzenia/D/wyniki/20261015_220614_093174/run_fixtures_before_cleanup.py), [outcomes.json](rozszerzenia/D/wyniki/20261015_220614_093174/outcomes.json), [summary.json](rozszerzenia/D/wyniki/20261015_220614_093174/summary.json), [runner_exit_code.txt](rozszerzenia/D/wyniki/20261015_220614_093174/runner_exit_code.txt), [previous_integrity.json](rozszerzenia/D/wyniki/20261015_220614_093174/previous_integrity.json), [anonymization.json](rozszerzenia/D/wyniki/20261015_220614_093174/anonymization.json) — porównanie 26 decyzji, nienaruszenie A–C i kontrola prywatnych ścieżek. Dodatkowe scenariusze znajdują się obok Fxx; m.in. [json_write_error](rozszerzenia/D/wyniki/20261015_220614_093174/json_write_error/).
- **D34:** [anonymization.json pierwszej próby](rozszerzenia/D/wyniki/20261015_220454_678360/anonymization.json), [pierwszy parser](rozszerzenia/D/wyniki/20261015_220454_678360/parse_results_before_privacy_fix.py), [pierwsze podsumowanie](rozszerzenia/D/wyniki/20261015_220454_678360/summary.json) — oznaczona zanonimizowana kopia z opisem redakcji. [Drugi przebieg](rozszerzenia/D/wyniki/20261015_220549_429509/summary.json) potwierdza poprawkę parsera; [poprzednia wersja automatu](rozszerzenia/D/wyniki/20261015_220549_429509/run_fixtures_before_privacy_audit.py) zachowuje kod sprzed dodania automatycznej kontroli prywatnych ścieżek. Oryginalne strumienie pierwszej próby pozostają wyłącznie w pomijanym `_build/`.
- **D35:** [review.txt](rozszerzenia/D/wyniki/20261015_220614_093174/review.txt) — końcowy przegląd fixture, raportów, odwołań, arytmetyki i prezentacji.

### Rola plików w katalogu dowodów

- `raw_output.txt` zawiera niezmieniony protokół producenta; `results.csv` lub `results_verified.csv` zawiera dane po opisanym etapie eksportu.
- `process_logs.json` zbiera dokładną treść pomocniczych logów producenta, kompilacji i testów technicznych; klucz wskazuje pierwotną nazwę pliku. Oddzielne pliki `parser_stdout.txt`, `parser_stderr.txt` i `parser_exit_code.txt` dokumentują decyzję parsera zgodnie z PDF.
- Polecenia i metryczki identyfikują sposób wykonania, a skróty źródeł — użyte bajty. Nie zastępują kontroli treści wyników.
- W D `validation.json` opisuje decyzję parsera, a pliki porównania i `summary.json` — zgodność tej decyzji z niezależnym oczekiwaniem automatu. Kod 0 automatu nie oznacza kodu 0 każdego parsera.

### D04 — pełny stdout producenta, bez zmian

```text
TIDPI_RESULTS;1
case;size;trial;time_us;comparisons;correct
sorted;16;1;0;15;true
reversed;16;1;0;120;true
random;16;1;0;110;true
reversed;16;2;0;120;true
random;16;2;0;114;true
sorted;16;2;0;15;true
random;16;3;0;105;true
sorted;16;3;0;15;true
reversed;16;3;0;120;true
sorted;32;1;0;31;true
reversed;32;1;0;496;true
random;32;1;1;475;true
reversed;32;2;0;496;true
random;32;2;1;490;true
sorted;32;2;0;31;true
random;32;3;1;493;true
sorted;32;3;0;31;true
reversed;32;3;0;496;true
```

### D05 — stdout parsera, bez zmian

```text
ACCEPTED: 18 record(s), failed tests: 0
```

Puste pliki stderr pozostają w dowodach. Kod 0 potwierdzono treścią danych i niezależną walidacją; samo istnienie pliku nie było kryterium powodzenia.

### D10–D16 — zachowane komunikaty parsera B

D10 — `invalid-number`, [parser_stderr.txt](przypadki/invalid-number/parser_stderr.txt), bez zmian:

```text
VALIDATION ERROR: line 3: size must be an integer, got 'many'
REJECTED: 1 validation error(s)
```

D11 — `missing-field`, [parser_stderr.txt](przypadki/missing-field/parser_stderr.txt), bez zmian:

```text
VALIDATION ERROR: line 3: expected 6 fields, got 5
REJECTED: 1 validation error(s)
```

D12 — `duplicate-row`, [parser_stderr.txt](przypadki/duplicate-row/parser_stderr.txt), bez zmian:

```text
VALIDATION ERROR: line 21: duplicate record identity ('reversed', 32, 3)
REJECTED: 1 validation error(s)
```

D13 — `wrong-version`, [parser_stderr.txt](przypadki/wrong-version/parser_stderr.txt), bez zmian:

```text
VALIDATION ERROR: line 1: expected protocol TIDPI_RESULTS;1
REJECTED: 1 validation error(s)
```

D14 — `failed-test`, [parser_stdout.txt](przypadki/failed-test/parser_stdout.txt), bez zmian:

```text
ACCEPTED: 18 record(s), failed tests: 1
```

D16 — błąd odczytu, [parser_stderr.txt](logs/20261015_214715_193570_b/read-error/parser_stderr.txt), bez zmian:

```text
VALIDATION ERROR: cannot read input: [Errno 2] No such file or directory: 'missing_input.txt'
```

### D22–D28 — komunikaty kontroli ujemnych C

D23 — [parser_stderr.txt](rozszerzenia/C/seed/testy/invalid-seed/parser_stderr.txt), bez zmian:

```text
VALIDATION ERROR: line 3: seed must be >= 0, got -1
REJECTED: 1 validation error(s)
```

D26 — [parser_stderr.txt](rozszerzenia/C/kompletnosc/testy/missing-row/parser_stderr.txt), bez zmian:

```text
VALIDATION ERROR: missing record identity ('sorted', 16, 1)
REJECTED: 1 validation error(s)
```

D27 — [parser_stderr.txt](rozszerzenia/C/kompletnosc/testy/extra-row/parser_stderr.txt), bez zmian:

```text
VALIDATION ERROR: line 21: unexpected record identity ('reversed', 32, 4)
REJECTED: 1 validation error(s)
```

D28 — [parser_stderr.txt](rozszerzenia/C/kompletnosc/testy/invalid-config/parser_stderr.txt), bez zmian:

```text
CONFIGURATION ERROR: trials must be an integer >= 1 (not boolean)
```

D22 i D24 zbierają po 20 błędów: niezgodną wersję w wierszu 1, nagłówek w wierszu 2 oraz niezgodną liczbę pól w 18 rekordach. Pełne, niezmienione komunikaty pozostają w katalogach tych testów. Nie jest to 20 niezależnych awarii producenta, lecz konsekwencje jednego nieobsługiwanego schematu.

### D32–D33 — wybrane raporty i komunikaty D, bez zmian

F03, poprawne dane z nieudanym testem — [dowód](rozszerzenia/D/wyniki/20261015_220614_093174/F03/validation.json):

```text
{
  "schema_version": 1,
  "decision": "failed_tests",
  "exit_code": 1,
  "published_records": 1,
  "failed_tests": 1,
  "csv_created": true,
  "errors": []
}
```

F12, pusty wiersz — [dowód](rozszerzenia/D/wyniki/20261015_220614_093174/F12/parser_stderr.txt):

```text
VALIDATION ERROR [BLANK_ROW]: line 4: unexpected blank row
REJECTED: 1 validation error(s)
```

Awaria wymaganego JSON — [dowód](rozszerzenia/D/wyniki/20261015_220614_093174/json_write_error/parser_stderr.txt):

```text
VALIDATION ERROR [REPORT]: cannot write JSON: No such file or directory (errno=2)
```

## Opracowanie wyników

### Poziom A — statystyki opisowe tej serii

Tabela 2 — czasy sortowania [µs] z D04, obliczenia D06, osobno dla układu i rozmiaru. To opis tej serii, nie ranking wydajności.

| Układ    | Rozmiar | Próba 1 | Próba 2 | Próba 3 | Minimum | Maksimum | Rozstęp | Mediana |
| -------- | ------: | ------: | ------: | ------: | ------: | -------: | ------: | ------: |
| sorted   |      16 |       0 |       0 |       0 |       0 |        0 |       0 |       0 |
| reversed |      16 |       0 |       0 |       0 |       0 |        0 |       0 |       0 |
| random   |      16 |       0 |       0 |       0 |       0 |        0 |       0 |       0 |
| sorted   |      32 |       0 |       0 |       0 |       0 |        0 |       0 |       0 |
| reversed |      32 |       0 |       0 |       0 |       0 |        0 |       0 |       0 |
| random   |      32 |       1 |       1 |       1 |       1 |        1 |       0 |       1 |

Rozstęp to `max − min`, a mediana trzech prób to środkowa wartość po sortowaniu. Dla `random`, rozmiar 32, sekwencja `[1, 1, 1]` daje minimum 1, maksimum 1, rozstęp `1 − 1 = 0` i medianę 1 µs. Pozostałe pięć grup ma `[0, 0, 0]`, więc wszystkie cztery statystyki wynoszą 0. Zerowy rozstęp po obcięciu nie dowodzi braku zmienności rzeczywistych czasów. Nie przygotowano wykresu, ponieważ poziom A go nie wymaga, a te czasy nie uzasadniają analizy wydajności.

Ręczna kontrola liczników D04: wiersz 3 ma `sorted;16`, więc `16 − 1 = 15`; wiersz 12 ma `sorted;32`, więc `32 − 1 = 31`. Wiersz 4 ma `reversed;16`: `16 × 15 / 2 = 120`; wiersz 13 ma `reversed;32`: `32 × 31 / 2 = 496`. Wszystkie trzy próby tych układów spełniają regułę. Ziarna sprawdzono osobno: `20260600 + 16 × 10 + 1 = 20260761`, `20260600 + 32 × 10 + 3 = 20260923`.

### Poziom B — decyzje parsera

Tabela 3 — oczekiwane i rzeczywiste decyzje parsera (D10–D17). „Brak” oznacza sprawdzoną nieobecność pliku po wykonaniu; „—” oznacza, że pozycja nie dotyczy przypadku.

| Przypadek / dowód   | Kategoria                    | Reguła                               | Wiersz wejścia | Kod producenta | Kod parsera oczekiwany / rzeczywisty | CSV oczekiwany / rzeczywisty |
| ------------------- | ---------------------------- | ------------------------------------ | -------------: | -------------: | ------------------------------------ | ---------------------------- |
| invalid-number, D10 | wartość                      | size musi być int; otrzymano many    |              3 |              0 | 2 / 2                                | brak / brak                  |
| missing-field, D11  | struktura                    | wymagane 6 pól; otrzymano 5          |              3 |              0 | 2 / 2                                | brak / brak                  |
| duplicate-row, D12  | struktura zbioru             | unikalne (case, size, trial)         |             21 |              0 | 2 / 2                                | brak / brak                  |
| wrong-version, D13  | struktura/protokół           | obsługiwana wersja 1, nie 99         |              1 |              0 | 2 / 2                                | brak / brak                  |
| failed-test, D14    | poprawne dane, nieudany test | correct=false jest dozwolone         |              3 |              1 | 1 / 1                                | jest / jest                  |
| brak wejścia, D16   | odczyt                       | plik musi istnieć i dać się odczytać |              — |              — | 2 / 2                                | brak / brak                  |

Każda z czterech prób odrzucenia zgłosiła dokładnie jeden błąd kontraktu. D10 zachował 18 rekordów z jedną błędną wartością; D11 — 18 rekordów, pierwszy z pięcioma polami; D12 — 19 rekordów, ostatni powtarza poprzedni; D13 — 18 rekordów przy nieobsługiwanej wersji. Dane te nie są częściowo eksportowane.

W D14 CSV ma dokładnie 18 unikalnych rekordów, jeden `correct=false` (pierwszy rekord, `sorted;16;1`) i 17 `true`. Wiersz 3 raw odpowiada wierszowi 2 CSV, ponieważ CSV pomija protokół. Porównano wszystkie pola CSV z raw, nie tylko liczbę rekordów. To poprawny opis symulowanego niepowodzenia; nie ma podstaw do odrzucenia struktury danych. Kod 1 sygnalizuje wynik testu, dlatego CSV powstaje.

#### Usunięcie starego CSV — D15

Przed D10 skopiowano `results_verified.csv` z A. Ponowny odczyt potwierdził 18 rekordów i same `true`. Źródło i docelowy stary CSV miały identyczny SHA-256:

```text
06112fb3f3bbe01dadb5524092837658281ecc0ba95ad4e9dedf619e739fe0ba
```

[stale_csv_before.txt](logs/20261015_214715_193570_b/stale_csv_before.txt) potwierdza `output_exists_before=true`, zgodność skrótów i `producer_created_csv=false`. Po uruchomieniu parsera na `invalid-number` kod wyniósł 2, a [stale_csv_after.txt](logs/20261015_214715_193570_b/stale_csv_after.txt) zapisuje `output_exists_after=false` i `output_recreated=false`. Nie dołączono starego pliku jako nowego wyniku. Kontrola skrótów D17 potwierdza, że źródłowy CSV A nie zmienił się.

### Poziom C — wersja i kompletność

Tabela 4 — kryteria i wyniki końcowej serii C, D21–D29. CSV oznacza wynik badanego parsera; dla poprawnych wejść plik producenta pozostaje osobno.

| Test / dowód           | Oczekiwana reguła / decyzja            | Kod producenta | Kod parsera oczekiwany / rzeczywisty | CSV oczekiwany / rzeczywisty |
| ---------------------- | -------------------------------------- | -------------- | ------------------------------------ | ---------------------------- |
| C1 poprawne v2, D21    | 18 rekordów, 7 pól i seed w zakresie   | 0              | 0 / 0                                | jest / jest                  |
| C1 v2 do v1, D22       | odrzuć wersję 2, wiersz 1              | 0, źródło D21  | 2 / 2                                | brak / brak                  |
| C1 invalid-seed, D23   | seed=-1 poza zakresem, wiersz 3        | 0              | 2 / 2                                | brak / brak                  |
| C1 v1 do v2, D24       | odrzuć wersję 1, wiersz 1              | 0, źródło A    | 2 / 2                                | brak / brak                  |
| C2 poprawne, D25       | dokładnie skonfigurowane 18 tożsamości | 0              | 0 / 0                                | jest / jest                  |
| C2 missing-row, D26    | brak (sorted,16,1), odrzuć             | 0              | 2 / 2                                | brak / brak                  |
| C2 extra-row, D27      | nadmiar (reversed,32,4), wiersz 21     | 0              | 2 / 2                                | brak / brak                  |
| C2 invalid-config, D28 | trials=0, odrzuć konfigurację          | 0, źródło D25  | 2 / 2                                | brak / brak                  |

W D21 i D25 każdy CSV ma 18 unikalnych tożsamości i same `correct=true`. Wszystkie pola CSV producenta i parsera zgadzają się z raw. Przykładowo `random;16;1` z D21 ma `seed=20260761`: ręcznie `20260600 + 16 × 10 + 1 = 20260761`. Dla `random;32;3` sprawdzono `20260600 + 32 × 10 + 3 = 20260923`. Wszystkie 12 rekordów układów `sorted`/`reversed` ma `seed=0`, a sześć rekordów `random` — ziarna zgodne z formułą.

Kontrola kompletności porównała zbiory, a nie samą liczebność. D26 ma 17 rekordów i brakuje w nim `(sorted,16,1)`; D27 ma 19 rekordów, w tym 18 oczekiwanych i `(reversed,32,4)`. To rekord poprawny według ogólnego v1 (`trial >= 1`), ale niezgodny z planem trzech prób. Schemat i plan eksperymentu są odrębnymi warstwami walidacji.

Przed D26 pozostawiono poprawny CSV D25. [stale_csv_before.txt](logs/20261015_215518_245294_c/stale_csv_before.txt) dokumentuje 18 rekordów, same `true` i zgodny skrót źródła oraz kopii:

```text
a0446c91f50e3bd1f9022a86d61b27e33c85aa9f96d0266fa11baad22c5bd4a4
```

Po odrzuceniu braku tożsamości `output_exists_after=false`, `output_recreated=false`, kod parsera 2 — [stale_csv_after.txt](logs/20261015_215518_245294_c/stale_csv_after.txt). Nie pozostawiono starego CSV w odrzuconym przypadku.

Dodatkowe fixture funkcji (D29) potwierdziły akceptację `seed=0` i `4294967295` oraz odrzucenie `-1`, `4294967296` i `many`. Są to sztuczne rekordy do kontroli zakresu, nie wyniki generowania z tymi ziarnami. Dwanaście kontroli konfiguracji obejmuje poprawny plik oraz odrzucenie logicznego `trials`, logicznego rozmiaru, powtórzonych przypadków i rozmiarów, nieznanego pola, pustych list, nieznanego przypadku, rozmiaru zmiennoprzecinkowego, rozmiaru 1 i braku wymaganego pola. Nie przypisuje się tym testom realizacji D.

#### Wykryta usterka diagnostyki — D20

W pierwszym parserze v2 warunek poprawnie wymagał wersji 2, ale tekst błędu nadal brzmiał `expected protocol TIDPI_RESULTS;1`. Test v1 do v2 zwrócił 2 i nie utworzył CSV, lecz kryterium poprawnej diagnostyki nie było spełnione. Serię przerwano; plik [seed_parser_before_fix.py](logs/20261015_215452_063831_c/seed_parser_before_fix.py) i [log odrzucenia](logs/20261015_215452_063831_c/seed_tests_before_fix/v2-odrzuca-v1/parser_stderr.txt) zachowano bez zmian. Po poprawce komunikat wskazuje wersję 2; pełna nowa seria D21–D29 dała osiem oczekiwanych decyzji. Pierwszej próby nie przedstawia się jako bezbłędnego sukcesu.

### Poziom D — fixture i błędy wykonania

Tabela 5 — 18 sztucznych fixture, niezależne oczekiwania D31 i rzeczywiste wyniki D32. Wszystkie wiersze końcowej serii były zgodne. Wiersz „—” oznacza brak błędu albo problem odczytu bez numeru wiersza.

| Fixture                                                                 | Cel                       | Reguły i wiersze błędów                               | Kod oczekiwany / rzeczywisty | CSV oczekiwany / rzeczywisty |
| ----------------------------------------------------------------------- | ------------------------- | ----------------------------------------------------- | ---------------------------- | ---------------------------- |
| [F01](rozszerzenia/D/wyniki/20261015_220614_093174/F01/comparison.json) | Minimalny rekord          | —                                                     | 0 / 0                        | jest / jest                  |
| [F02](rozszerzenia/D/wyniki/20261015_220614_093174/F02/comparison.json) | BOM i CRLF                | —                                                     | 0 / 0                        | jest / jest                  |
| [F03](rozszerzenia/D/wyniki/20261015_220614_093174/F03/comparison.json) | Poprawne false            | —                                                     | 1 / 1                        | jest / jest                  |
| [F04](rozszerzenia/D/wyniki/20261015_220614_093174/F04/comparison.json) | Liczby stucyfrowe         | —                                                     | 0 / 0                        | jest / jest                  |
| [F05](rozszerzenia/D/wyniki/20261015_220614_093174/F05/comparison.json) | Wersja 99                 | PROTOCOL:1                                            | 2 / 2                        | brak / brak                  |
| [F06](rozszerzenia/D/wyniki/20261015_220614_093174/F06/comparison.json) | Kolejność nagłówka        | HEADER:2                                              | 2 / 2                        | brak / brak                  |
| [F07](rozszerzenia/D/wyniki/20261015_220614_093174/F07/comparison.json) | Brak pola                 | FIELD_COUNT:3                                         | 2 / 2                        | brak / brak                  |
| [F08](rozszerzenia/D/wyniki/20261015_220614_093174/F08/comparison.json) | Ułamek zamiast int        | INTEGER:3                                             | 2 / 2                        | brak / brak                  |
| [F09](rozszerzenia/D/wyniki/20261015_220614_093174/F09/comparison.json) | size poniżej 2            | RANGE:3                                               | 2 / 2                        | brak / brak                  |
| [F10](rozszerzenia/D/wyniki/20261015_220614_093174/F10/comparison.json) | Kombinacja sześciu błędów | CASE:3, RANGE:3, RANGE:3, RANGE:3, RANGE:3, BOOLEAN:3 | 2 / 2                        | brak / brak                  |
| [F11](rozszerzenia/D/wyniki/20261015_220614_093174/F11/comparison.json) | Duplikat 16/016           | DUPLICATE:4                                           | 2 / 2                        | brak / brak                  |
| [F12](rozszerzenia/D/wyniki/20261015_220614_093174/F12/comparison.json) | Pusty wiersz              | BLANK_ROW:4                                           | 2 / 2                        | brak / brak                  |
| [F13](rozszerzenia/D/wyniki/20261015_220614_093174/F13/comparison.json) | Powtórzony nagłówek       | REPEATED_HEADER:4                                     | 2 / 2                        | brak / brak                  |
| [F14](rozszerzenia/D/wyniki/20261015_220614_093174/F14/comparison.json) | Błędne UTF-8              | READ:—                                                | 2 / 2                        | brak / brak                  |
| [F15](rozszerzenia/D/wyniki/20261015_220614_093174/F15/comparison.json) | Niedomknięty CSV          | CSV_SYNTAX:3                                          | 2 / 2                        | brak / brak                  |
| [F16](rozszerzenia/D/wyniki/20261015_220614_093174/F16/comparison.json) | Brak danych               | EMPTY_DATA:3                                          | 2 / 2                        | brak / brak                  |
| [F17](rozszerzenia/D/wyniki/20261015_220614_093174/F17/comparison.json) | false i błędna liczba     | INTEGER:3                                             | 2 / 2                        | brak / brak                  |
| [F18](rozszerzenia/D/wyniki/20261015_220614_093174/F18/comparison.json) | Błędny ostatni rekord     | INTEGER:4                                             | 2 / 2                        | brak / brak                  |

Spośród 18 fixture trzy otrzymały kod 0, jeden kod 1, a 14 kod 2: `3 + 1 + 14 = 18`. CSV powstał dla czterech zaakceptowanych zbiorów, w tym dla F03 z `false`. F10 wykazał sześć niezależnych problemów w wierszu 3: CASE, cztery RANGE i BOOLEAN. F17 ma legalne `false`, ale niepoprawny `size`; dlatego cały zbiór otrzymał 2, nie 1. F18 potwierdza odrzucenie całości mimo poprawnego pierwszego rekordu.

F02 odczytano z BOM i CRLF, a wyeksportowano z BOM i LF, bez zmiany komórek. F04 ma w `time_us` i `comparisons` liczbę `10^99`, czyli jedynkę i 99 zer — 100 cyfr. Automat porównał wszystkie cyfry CSV z niezależnie zapisanymi oczekiwaniami manifestu. Nie stosowano `float`. Nie oznacza to sprawdzenia importu takiej liczby w Excelu ani zgodności tego licznika z rzeczywistym sortowaniem.

Przed każdym z 14 odrzuceń fixture stan `before.json` potwierdza poprawny stary CSV z F01 i jego skrót; `after.json` potwierdza brak CSV i zachowanie wejścia. Raport JSON odrzucenia ma `published_records=0` i `csv_created=false`.

Tabela 6 — osiem dodatkowych scenariuszy wykonania, D33. Wszystkie oczekiwały i otrzymały kod parsera 2.

| Scenariusz                      | Sprawdzona reguła                 | Wynik  |
| ------------------------------- | --------------------------------- | ------ |
| Brak pliku wejściowego          | READ; bez starego CSV             | zgodny |
| Wejście jako CSV                | PATH; wejście bez zmian           | zgodny |
| Wejście jako JSON               | PATH; wejście bez zmian           | zgodny |
| Dowiązanie symboliczne jako CSV | PATH; rozpoznanie aliasu wejścia  | zgodny |
| Dowiązanie twarde jako JSON     | PATH; rozpoznanie aliasu wejścia  | zgodny |
| CSV i JSON pod tą samą ścieżką  | PATH; bez publikacji              | zgodny |
| Niedostępny katalog CSV         | OUTPUT; JSON odrzucenia, brak CSV | zgodny |
| Niedostępny katalog JSON        | REPORT na stderr; usunięcie CSV   | zgodny |

Razem `18 + 8 = 26` kontroli, wszystkie zgodne; dodatkowe scenariusze nie zastępują wymaganych plików fixture. Z uwzględnieniem brakującego wejścia było 15 prób z pozostawionym starym CSV. Końcowe `summary.json` potwierdza `passed=26`, `failed=0`, `previous_unchanged=true`, `anonymization_passed=true` i kod automatu 0. Wszystkie raporty JSON, które mogły zostać zapisane, zgadzają się z procesem; kolizje ścieżek i niemożliwy zapis JSON mają jawnie opisane wyjątki od publikacji raportu.

#### Usterka anonimizacji i ponowne próby — D34

Pierwsza seria miała 26 zgodnych decyzji funkcjonalnych, lecz komunikaty błędów zapisu z `tempfile` ujawniały prywatną ścieżkę. Taki komplet nie nadawał się do anonimowego przekazania. Oryginalne strumienie zachowano prywatnie; publiczny katalog jest **osobno przygotowaną zanonimizowaną kopią**, oznaczoną plikiem `anonymization.json`. W wymienionych tam plikach zastąpiono wyłącznie prefiks ścieżki znacznikiem `[KATALOG_ZADANIA]`; nie zmieniano kodów, decyzji ani danych fixture. Ta kopia nie jest przedstawiana jako niezmieniony raw.

Parser poprawiono tak, by błędy I/O zawierały przyczynę i errno bez nazwy pliku. Drugi przebieg potwierdził 26 decyzji po poprawce. Następnie automat rozszerzono o kontrolę prywatnych ścieżek w wynikach i wykonano trzeci, końcowy przebieg. Kod obu wcześniejszych wersji zachowano w D34. Po przeglądzie PDF usunięto powielone wyniki wcześniejszych testów D; pozostały ich podsumowania oraz szczegółowe dowody usterki I/O z pierwszej próby. Do Tabel 5–6 użyto wyłącznie końcowej serii.

## Interpretacja

### Poziom A — zachowanie danych i znaczenie liczników

**Obserwacja:** D04 zawiera komplet oczekiwanych tożsamości, a wszystkie sortowania zadeklarowały zgodność pełnych wyników. D05 i D06 potwierdzają, że parser zachował dane, a obydwa CSV są zgodne. W komórkach `time_us` i `comparisons` występują liczby bez dopisanych jednostek; jednostkę czasu określa nagłówek.

**Wyjaśnienie wynikające z kodu i liczników:** dla `sorted` pierwszy przebieg nie wykonuje zamiany, więc działa wcześniejsze wyjście. Dla odwrotnej permutacji pętle wykonują `n × (n − 1) / 2` porównań. Wartości 120 i 496 zgadzają się z tym oczekiwaniem.

**Granica interpretacji:** czasy 0 i 1 µs opisują małe zadanie przy całkowitej jednostce zapisu i z narzutem licznika. Nie wskazują stabilnej przewagi żadnego układu ani przyczyny sprzętowej. Nie mierzono pamięci podręcznej, obciążenia procesora ani kosztu importera.

### Poziom B — błąd danych a nieudany test

**Obserwacja:** rzeczywiste decyzje sześciu kontroli parsera zgadzają się z kryteriami: cztery błędne kontrakty oraz brak wejścia odrzucono, a poprawny kontrakt z nieudanym testem zachowano w CSV (Tabela 3). Stary wynik zniknął po odrzuceniu D10. Kod producenta 0 nie przesądził akceptacji przez parser.

**Zakres wniosku:** to kontrolowane testy konkretnych reguł, nie dowód wykrycia wszystkich możliwych uszkodzeń ani rzeczywistego błędu sortowania. Regresja D17 potwierdziła zgodność zwykłego eksportu po zmianie producenta, bez zastępowania pierwotnych pomiarów A.

### Poziom C — schemat a plan eksperymentu

**Obserwacja:** parsery odrzuciły obce wersje zamiast interpretować przesunięte pola; v2 zachował wszystkie wartości seed. Parser kompletności zaakceptował planowany zbiór i odrzucił brak oraz nadmiar, a poprawny stary CSV został usunięty po odrzuceniu. Pierwsza próba ujawniła niespójny komunikat, poprawiony przed końcową serią.

**Zakres wniosku:** wynik potwierdza zachowanie tych wersji programów dla opisanych wejść i konfiguracji. Sama poprawność zakresu seed nie dowodzi zgodności generatora, a spełnienie schematu nie gwarantuje zgodności z planem liczby prób. Nie badano jakości losowości ani wydajności rozszerzeń.

### Poziom D — uzasadnienie i granice potwierdzenia

**Obserwacja:** końcowy zestaw obejmuje akceptację danych, legalne `false`, granice liczbowe, wiele błędów rekordu, błędy struktury i kodowania oraz ochronę publikowanych plików. Wszystkie 26 oczekiwań automatu było zgodnych. Kontrola pozafunkcjonalna wykryła problem prywatnej ścieżki, niewykrywany przez same wcześniejsze porównania decyzji; dodano odpowiednią kontrolę wyników.

**Granica wniosku:** to dowód zachowania konkretnego parsera dla tych fixture i warunków. Nie jest dowodem braku wszystkich błędów, bezpieczeństwa dowolnych równoległych operacji plikowych ani prawdziwości wyników producenta. Model i fixture przygotował asystent; nie stanowią deklaracji samodzielnej pracy ucznia bez jego weryfikacji i obrony rozwiązania.

## Ograniczenia eksperymentu

1. Jedna maszyna; jedna historyczna seria pomiarowa A oraz osobne kontrole B i C, w tym przerwana pierwsza próba C. Dwa małe rozmiary i trzy podstawowe próby na grupę nie dają podstaw do uogólnień wydajnościowych; dodatkowa próba C2 służy kontroli nadmiaru.
2. Efektywnej rozdzielczości zegara nie zmierzono. Nominalny okres 1 ns i zapis w mikrosekundach nie określają dokładności eksperymentu. Zera oznaczają wynik poniżej jednostki zapisu po obcięciu.
3. Pomiar wyklucza tworzenie danych, wzorzec, kontrolę poprawności i obsługę plików; nie jest czasem całego procesu ani parsowania.
4. Użyto macOS/arm64/Apple Clang zamiast Windows/Visual Studio/MSVC. Nie jest to dowód wykonania kroków specyficznych dla szkolnego toolchainu.
5. **Nie wykonano kontroli importu CSV w Microsoft Excel ze względu na ograniczoną dostępność aplikacji w używanym środowisku systemowym. Ten element wymagań poziomu A pozostaje niezweryfikowany.** Nie jest to twierdzenie, że Excel nie obsługuje macOS. Kontrola tekstowa i odczyt Pythonem nie zastępują kontroli w Excelu.
6. Parsery sprawdzają kontrakt i pole `correct`, nie weryfikują samodzielnie sortowania. Ogólny v1 z A–B nie narzuca kompletu 18 rekordów; osobny parser C2 narzuca go na podstawie konfiguracji. V2 sprawdza typ i zakres seed, nie wykonuje generatora ponownie.
7. `std::shuffle` nie gwarantuje tej samej permutacji dla tego samego ziarna na wszystkich bibliotekach standardowych. Nie wykonano porównania między toolchainami.
8. B obejmuje pięć wybranych trybów, dodatkowy błąd odczytu i kontrolę regresji. Nie badano wszystkich kombinacji błędów ani wszystkich awarii systemu plików. `failed-test` jest symulacją na etapie emisji; nie oznacza rzeczywistego defektu sortowania.

9. C obejmuje dwa wybrane badania, bez `note`; D jest odrębnym badaniem v1 opisanym powyżej. Konfiguracja kompletności tworzy oczekiwany zbiór w pamięci; nie testowano skrajnie dużych konfiguracji. W próbach C sprawdzano akceptację i odrzucenie (kody 0 i 2); kod 1 opisano i wykonano wcześniej w B, bez nowej próby nieudanego testu w C.

10. D używa sztucznych fixture i nie mierzy wydajności. Sto cyfr sprawdzono dokładnie, ale nie testowano wyczerpania pamięci, wszystkich limitów modułu CSV ani granicy 4300 cyfr interpretera. Parser nie narzuca własnego limitu liczbowego, lecz pozostaje zależny od środowiska.
11. Atomowa zmiana nazwy dotyczy pojedynczego pliku, nie jednoczesnej transakcji CSV i JSON. Przy obsłużonej awarii JSON CSV jest usuwany; nie badano nagłego zakończenia procesu pomiędzy zapisami ani wyścigów z innymi procesami. Jeśli system uniemożliwi również sprzątanie, parser może jedynie zgłosić niepowodzenie.
12. Końcowy automat nie odnotował timeoutu ani awarii procesu; zachowanie jego ścieżek kontynuacji po takich zdarzeniach wynika z przeglądu kodu, nie z wymuszonego timeoutu w tej serii. Kontrola prywatnych ścieżek w automacie jest pomocnicza i nie zastępuje ręcznej anonimizacji.

## Wnioski

1. **A:** Lokalny łańcuch producent–parser działa dla tej serii: D03–D06 potwierdzają kody 0, komplet 18 rekordów i zachowanie wszystkich pól.
2. **A:** Bezpośredni CSV C++ jest zgodny z niezależnie zapisanym CSV parsera. Wszystkie kontrole pełnego wyniku sortowania zwróciły `true` (D04).
3. **Zakres:** Odczyt i komplet danych potwierdzono programowo. Nie można zadeklarować pełnej realizacji poziomu A, ponieważ nie wykonano wymaganego importu w Excelu.
4. **A:** Czasy w tej serii służą demonstracji przetwarzania danych; nie uzasadniają wniosków o przewadze algorytmu lub układu danych.
5. **B:** Kontrole B potwierdziły rozróżnienie błędnych danych (kod 2, bez CSV) i poprawnych danych z nieudanym testem (kod 1, z CSV). Wszystkie oczekiwane decyzje zgadzają się z wykonaniem (D10–D17).
6. **B:** D15 wykazał usunięcie starego CSV po odrzuceniu wejścia. To usuwa możliwość uznania poprzedniego pliku za wynik tej konkretnej nieudanej próby.
7. **Zakres:** Mimo wykonania kontroli B–D nie deklaruje się pełnego ukończenia A–D ze względu na pozostający brak importu w Excelu. Progi z PDF są pułapami, nie obietnicą oceny.
8. **C1:** D21–D24 potwierdzają zachowanie wersjonowania: v2 przenosi dodatkowe pole, v1 odrzuca v2, a v2 odrzuca v1. Zakres ziarna sprawdzono niezależnie od interpretacji pozostałych pól.
9. **C2:** D25–D29 wykazały rozróżnienie poprawnego kontraktu i kompletnego eksperymentu. Dodatkowa próba może być poprawnym rekordem v1, lecz mimo to naruszać konfigurację.
10. **C:** D20 pokazuje, że sprawdzenie samego kodu 2 nie wystarcza: poprawności wymaga też treść diagnostyki. Wykryty błąd zachowano i poprawiono przed ponowną kontrolą.
11. **D:** D31–D33 potwierdzają zgodność wszystkich 18 fixture oraz ośmiu scenariuszy dodatkowych. Poprawne dane z `false` są zachowywane, a błędny rekord odrzuca cały zbiór.
12. **D:** Stucyfrowe liczby przeszły bez utraty cyfr; puste i powtórzone wiersze oraz znormalizowany duplikat zostały rozpoznane. Obowiązkowy JSON pozwala sprawdzać decyzję i regułę niezależnie od kodu procesu.
13. **D:** Wymuszona awaria JSON usunęła CSV. Wykrycie prywatnej ścieżki pokazało, że zgodność funkcjonalna nie wystarcza do uznania anonimowego zestawu za gotowy.

## Wykorzystanie AI i sposób weryfikacji

Codex pomógł poprawić skrypty oraz procesy kompilowania kodu C++, automatyzuje procesy kompilowania i przekazywania outputu wartości do plików oraz przygotowywuje raport na podstawie mocka.

Po uporządkowaniu załączników asystent sprawdził zgodność scalonych logów, komplet wymaganych artefaktów i odwołania. Automat D zmieniono wyłącznie przez usunięcie zapisu redundantnego `execution.json`; dokładną wersję historycznego przebiegu zachowano przy D33. Wyniki ponownej kontroli automatu po tej zmianie zapisano w rejestrze porządkowania; nie są nową serią pomiarów sortowania.
