---
title: "TiDPI 05 - Automatyzacja kompilacji, uruchomienia i rejestracji wyniku"
author: "Kryptonim TiDPI: Regulus"
date: "2026-10-15"
lang: pl-PL
---

# Sprawozdanie TiDPI 05 — automatyzacja kompilacji, uruchomienia i rejestracji wyniku

## Kryptonim TiDPI i wykonany poziom

- Kryptonim: **Regulus**.
- Zakres rozwiązania: **A–D w adaptacji na macOS/arm64 i Apple Clang**. C: dwa rozszerzenia, `--repeat` i `--size`; D: bezpiecznie odczytywana konfiguracja YAML z walidacją.
- Seria historyczna: 2026-10-06, dowody D02–D13. Kontrole uzupełniające: 2026-10-15, D01 i D14–D16. Ręczna kompilacja D01 została wykonana dopiero podczas uzupełniania raportu; nie jest dowodem z 6 października.
- [x] A: ręczna kompilacja, dwa automatyczne przebiegi `release/pass`, osobne katalogi i objaśnienie plików.
- [x] B: symulowana awaria, błąd składni, zatrzymanie automatu, kontrola braku starego EXE i poprawny przebieg po przywróceniu źródła.
- [x] C: sukces i niepowodzenie obu wybranych rozszerzeń. Manifest rozmiarów i czasów modyfikacji nie został wybrany.
- [x] D: konfiguracja YAML, uzasadnienie projektu i dowody poprawnego oraz błędnych plików konfiguracji.
- Odstępstwo od polecenia: nie wykonano kroków w Developer PowerShell for VS 2022 ani kompilacji MSVC. Obecność backendu `cl` w kodzie nie dowodzi jego przetestowania. Zrealizowano opisany poniżej odpowiednik lokalny; zgodność narzędziowa z procedurą Windows pozostaje niewykazana.
- Program: [main.cpp](main.cpp); automat: [run_experiment.py](run_experiment.py). W tej korekcie raportu nie zmieniano ich treści.

Wymagania przyjęto z materiału lekcji: ustawienia kompilacji i kanały procesu (s. 2–4), ćwiczenia A–D (s. 12–14) oraz struktura i kryteria sprawozdania (s. 14–16). Raporty TiDPI_03 i TiDPI_04 posłużyły za wzorzec organizacji: cel, kontrola poprawności, procedura, dowody, interpretacja i ograniczenia. W tej lekcji przedmiotem badania jest automat, a nie szybkość sortowania.

### Oddane pliki

```text
TiDPI_05/
├── raport.md
├── main.cpp
├── run_experiment.py
├── experiment.yaml
├── requirements.txt
├── .gitignore
├── fixtures/
│   ├── config_missing_field.yaml
│   └── config_bad_case.yaml
└── logs/
    └── osobny katalog każdego przebiegu z rejestru D01–D16
```

Katalog [logs/](logs/) zawiera komplet powstałych artefaktów, również puste pliki strumieni. D00 znajduje się w raporcie i w metryczce D01. Nie użyto obrazów, więc katalog `images/` nie jest wymagany. Szkolny PDF, środowisko `.venv` i pliki wykonywalne z `_build/` nie są załącznikami rozwiązania. Umyślnie uszkodzone źródło zachowano wyłącznie jako dowód testu D15.

## Cel i hipoteza — kryteria powodzenia automatu

**A — buduję i rejestruję poprawny przebieg.** Celem jest odtworzenie łańcucha budowania, wykonania i zapisu dowodów. Kryterium akceptacji: ręczna kompilacja i wykonanie kończą się kodem 0, a dwa przebiegi automatyczne mają osobne katalogi, kod kompilacji 0, podjęte wykonanie, kod programu 0 i `final_status=passed`. Warunek nowego pliku wykonywalnego wynika z usuwania poprzedniego EXE przed kompilacją i kontroli jego istnienia po niej; osobno sprawdzono go w D14–D16.

**B — sprawdzam ścieżki niepowodzenia.** Symulacja błędu powinna pozostawić zwykły wynik w stdout, diagnostykę w stderr i kod programu 1. Błąd składni powinien dać `compile_failed`, `execution_attempted=false`, `run_exit_code=not_started` i brak EXE. Po naprawie oczekiwane jest ponowne `passed`.

**C — rozwijam automat.** Dla `--repeat 3` oczekiwane są trzy odrębne pary strumieni i trzy zapisane kody, także gdy pierwsza próba zawiedzie. Dla `--size 16` oczekiwane są zachowanie wartości w podsumowaniu, przekazanie jej do C++ i poprawny wynik. Dla `--size 0` oczekiwane są odrzucenie przed wykonaniem i brak strumieni programu.

**D — własna wiarygodna linia testowa.** Problemem jest możliwość pomylenia parametrów przy przepisywaniu rozbudowanej komendy. Plik YAML ma przechowywać jednoznaczny zestaw parametrów. Poprawny plik powinien dać `config_loaded=true` i `passed`; brak wymaganego pola oraz niedozwolony `case` powinny dać `config_error` przed kompilacją i wykonaniem.

Powyższe reguły są kryteriami oceny dowodów historycznych, a nie nową deklaracją przewidywań zapisanych przed 6 października. Przed kontrolami z 15 października ustalono oczekiwany sukces ręcznej kompilacji oraz sekwencję: poprawny build → błąd składni i brak EXE → poprawny build po przywróceniu źródła. Kryterium ręcznej próby zapisano również w [criteria.txt](logs/20261015_171412_190703_manual/criteria.txt).

## Środowisko oraz konfiguracja

Tabela 1 — metryczka środowiska i pochodzenie informacji (D00).

| Element      | Seria 2026-10-06                                                                              | Kontrole 2026-10-15                                                           |
| ------------ | --------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| System       | macOS 27.0.1, build 26A434, według wcześniejszego raportu                                     | macOS 27.0.1, build 26A434, sprawdzone w D01                                  |
| Architektura | arm64, według wcześniejszego raportu                                                          | arm64, sprawdzone w D01                                                       |
| Python       | 3.14.4, według wcześniejszego raportu                                                         | 3.14.4, sprawdzone w D01                                                      |
| Kompilator   | Apple Clang 21.0.0 według wcześniejszego raportu; backend `clang++` potwierdzają podsumowania | Apple Clang 21.0.0, sprawdzone w D01                                          |
| Konfiguracja | `release`, flagi `-O2 -DNDEBUG` w podsumowaniach                                              | `-O2 -DNDEBUG`, D01 i D14–D16                                                 |
| MSVC         | nie użyto                                                                                     | `cl_available=false` w D01                                                    |
| PyYAML       | wcześniejszy raport podaje 6.0.3; `requirements.txt` wymaga `>=6.0`                           | nie uruchamiano ponownie testów YAML ani nie sprawdzano zainstalowanej wersji |

### D00 — aktualna kontrola narzędzi

Źródło: [environment.txt](logs/20261015_171412_190703_manual/environment.txt). Wersję kompilatora zapisano bez ścieżki jego instalacji.

```text
recorded_at=2026-10-15T17:14:12.225195+02:00
timezone=Europe/Warsaw
host=macOS 27.0.1
build=26A434
arch=arm64
python=3.14.4
Apple clang version 21.0.0 (clang-2100.3.34.2)
Target: arm64-apple-darwin27.0.0
cl_available=false
```

Aktualna metryczka nie potwierdza wstecz wersji narzędzi użytych 6 października. W nowych dowodach zapisano również SHA-256 poprawnego źródła i automatu. Te skróty identyfikują sprawdzaną wersję; nie stanowią realizacji niewybranego manifestu C ani dodatkowego rozszerzenia D. W D15 hash uszkodzonego źródła znajduje się osobno w `verification.txt`; metryczka `environment.txt` wskazuje poprawną wersję odniesienia.

### Polecenie kompilacji i znaczenie ustawień

Rzeczywiste polecenie automatu w przebiegach z D02–D16, w których podjęto kompilację:

```sh
clang++ -O2 -DNDEBUG -std=c++17 -Wall -Wextra -pedantic -o _build/experiment.exe main.cpp
```

Tabela 2 — ustawienia użyte w backendzie Clang.

| Flaga lub argument         | Znaczenie                                                                                                 |
| -------------------------- | --------------------------------------------------------------------------------------------------------- |
| `-std=c++17`               | Standard języka C++17.                                                                                    |
| `-O2`                      | Optymalizacja kodu; jawna część lokalnej konfiguracji Release.                                            |
| `-DNDEBUG`                 | Definicja makra `NDEBUG`, m.in. wyłączająca standardowe `assert`; nie zastępuje opisu flag optymalizacji. |
| `-Wall -Wextra`            | Włączenie grup ostrzeżeń kompilatora.                                                                     |
| `-pedantic`                | Diagnostyka wybranych odstępstw od standardu.                                                             |
| `-o _build/experiment.exe` | Nazwa pliku wynikowego.                                                                                   |
| `main.cpp`                 | Źródło; sterownik kompilatora wykonuje również konsolidację.                                              |

Budowanie obejmuje tłumaczenie C++ na kod obiektowy i konsolidację z potrzebnymi bibliotekami. Samo wywołanie sterownika z plikiem `.cpp` może objąć oba etapy. W [executable_format.txt](logs/20261015_171412_190703_manual/executable_format.txt) polecenie `file` rozpoznało wynik ręcznej kompilacji jako `Mach-O 64-bit executable arm64`. Końcówka `.exe` jest nazwą zachowaną ze szkolnego przykładu, nie dowodem formatu Windows.

Dla porównania, materiał podaje następującą konfigurację MSVC — **nie uruchomiono jej w tej pracy**:

```text
cl /nologo /std:c++17 /EHsc /W4 /permissive- /utf-8 main.cpp /Fe:experiment.exe /O2 /MD
```

`/nologo` skraca nagłówek logu, `/std:c++17` wybiera standard, `/EHsc` model obsługi wyjątków, `/W4` poziom ostrzeżeń, `/permissive-` zgodność ze standardem, `/utf-8` kodowanie źródła, a `/Fe:` nazwę EXE. Backend automatu dodaje także `/Fo:` dla pliku obiektowego. Release w materiale to `/O2 /MD`, a Debug to `/Od /MDd`. `/MD` i `/MDd` wybierają odpowiednio zwykłą i debugową dynamiczną bibliotekę uruchomieniową MSVC; `/MDd` definiuje m.in. `_DEBUG`. `/O1 /MD` jest opisaną w materiale alternatywą nastawioną na mały kod, bez gwarancji zmniejszenia tablic lub pamięci danych. Flagi Clanga nie są tożsame z tymi ustawieniami MSVC.

## Zmienne i warunki eksperymentu

- Źródło i automat leżą obok siebie. `PROJECT_DIR` wynika z lokalizacji skryptu, a `subprocess.run` otrzymuje ten katalog jako `cwd`.
- Zmieniano `case`, liczbę powtórzeń, rozmiar wejścia i plik konfiguracji. W B zmieniono wyłącznie wskazany średnik w izolowanej kopii źródła.
- Backend jest wybierany automatycznie: najpierw `cl`, następnie `clang++`. Wszystkie zachowane podsumowania wykonanych kompilacji wskazują `clang++`.
- Przed kompilacją automat usuwa poprzedni `_build/experiment.exe`. Warunek przejścia do wykonania: kod kompilacji 0 i istnienie nowego programu.
- Limit kompilacji wynosi 60 s, a pojedynczego wykonania 10 s. Przekroczenie limitu jest oznaczane kodem umownym 124 i flagą `timeout`.
- `--repeat` z CLI jest walidowane przed kompilacją; `--size` z CLI po poprawnej kompilacji, ale przed uruchomieniem. Pola YAML są walidowane wcześniej, przed kompilacją.
- `compile_time_ms` obejmuje proces kompilatora, a `run_time_ms` cały proces programu; dla powtórzeń jest sumą czasów prób. Obejmują narzut uruchomienia i przechwytywania strumieni, nie są pomiarem samego sortowania.

### Schemat build → run → evidence

```text
argumenty / YAML → osobny katalog logs/<run_id>
    → walidacja konfiguracji i repeat
    → sprawdzenie dostępności kompilatora
    → usunięcie poprzedniego EXE
    → build → zapis compile_stdout.txt i compile_stderr.txt
        → kod != 0 lub brak nowego EXE: compile_failed, bez wykonania
        → kod 0 i nowy EXE: walidacja size z CLI
            → błąd size: validation_failed, bez wykonania
            → run: osobne stdout, stderr i kod każdej próby
                → wszystkie próby kod 0: passed
                → dowolna próba kod != 0: run_failed
    → summary.txt zachowuje decyzję i dowody wykonanych etapów
```

Dla błędnego YAML powstaje `config_error` bez kompilacji. Dla niedostępnych obu backendów powstaje `environment_error`. Utworzenie katalogu `_build/` nie oznacza, że kompilacja wystartowała.

## Kontrola poprawności

Program tworzy dwie kopie tego samego wejścia: `expected` sortuje przez `std::sort`, a `result` przez Bubble Sort. Kontrola `result == expected` porównuje wszystkie elementy, a nie tylko sam fakt rosnącej kolejności. Domyślne wejście ma osiem liczb `{8, 3, 7, 4, 9, 2, 6, 1}`; wzorzec to `{1, 2, 3, 4, 6, 7, 8, 9}`. Dla `--size 16` wejściem jest `15…0`, a wzorcem `0…15`.

`--simulate-failure` ustawia pierwszy element wyniku na `-1` już po sortowaniu. Jest to kontrolowany test reakcji automatu, a nie odkryta wada Bubble Sortu. Wynik musi wtedy różnić się od wzorca.

Umowa programu C++: 0 oznacza zgodność z wzorcem, 1 niezgodność, a 2 błąd argumentów. stdout zawiera opis przypadku i wynik; stderr zawiera diagnostykę. Pusty stderr sam nie dowodzi sukcesu. Automat podejmuje decyzję na podstawie kodów, a raport sprawdza dodatkowo treść strumieni.

Kod samego skryptu przekazuje `raise SystemExit(main())`. Sukces daje 0; błędy walidacji lub konfiguracji dają 2; błąd kompilacji przekazuje kod kompilatora, a niepowodzenie wykonania daje kod niezerowy. Dla wielu prób `run_exit_code` oznacza **ostatnią próbę**, więc trzeba czytać także `run_NN_exit_code` i `final_status`, który zależy od wszystkich prób. Kody procesu skryptu w nowych kontrolach zapisano niezależnie w `verification.txt`. Historyczne podsumowania D02–D13 nie zawierają osobnego zapisu kodu procesu skryptu.

## Procedura

### Poziom A — buduję i rejestruję poprawny przebieg

1. Zachowano dwa historyczne automatyczne przebiegi Release/pass: D02 i D03. Ich identyfikatory różnią się również mikrosekundami; oba katalogi mają komplet pięciu plików. Dostępne są oba wyniki, a podczas aktualizacji raportu porównano skróty wszystkich starych artefaktów przed pracą i po niej.
2. 15 października sprawdzono wersje narzędzi i wykonano brakującą próbę ręczną D01, bez wywoływania `run_experiment.py`, w świeżej kopii roboczej. Przechwycono oba strumienie oraz kod każdego procesu.
3. Ręczne polecenia D01, wykonywane kolejno:

```sh
mkdir -p _build
clang++ -std=c++17 -O2 -DNDEBUG -Wall -Wextra -pedantic main.cpp -o _build/manual.exe
./_build/manual.exe
file _build/manual.exe
```

4. Polecenie odtwarzające dwa automatyczne przebiegi A należy wykonać dwa razy; za każdym razem automat nada nowy identyfikator:

```sh
python3 run_experiment.py --configuration release --case pass
```

Aktualny automat zapisuje `run_01_stdout.txt` i `run_01_stderr.txt` nawet dla jednej próby. D02–D06 pochodzą ze wcześniejszej wersji i zachowują nazwy `run_stdout.txt` i `run_stderr.txt`. Nie przemianowano starych dowodów.

### Poziom B — sprawdzam ścieżki niepowodzenia

1. D04 dokumentuje wykonanie poniższego wariantu. Sprawdzono stdout, stderr i `run_exit_code=1`.

```sh
python3 run_experiment.py --configuration release --case fail
```

2. D05 dokumentuje usunięcie średnika po `const bool correct = result == expected`, błąd kompilacji i zatrzymanie przed wykonaniem. D06 to poprawny przebieg po naprawie. Stary log nie zapisuje oddzielnej obserwacji istnienia EXE, dlatego uzupełniono ją nową kontrolą.
3. D14–D16 wykonano kolejno w jednej izolowanej kopii aktualnego `main.cpp` i `run_experiment.py`. D14 utworzył prawidłowy `_build/experiment.exe`. Następnie usunięto wskazany średnik i wykonano D15 z tym samym poleceniem `release/pass`. Zewnętrzna kontrola zapisała istnienie EXE przed wywołaniem, brak po wywołaniu, brak `run_*` i kod skryptu 1.
4. Przywrócono dokładne bajty źródła z początku kontroli i ponownie wykonano `release/pass` jako D16: kod skryptu 0, nowy EXE i `passed`. Kopia uszkodzonego źródła pozostała w dowodach D15; źródło rozwiązania nie było uszkadzane.
5. W odtworzeniu należy zachować tę kolejność, użyć osobnej kopii roboczej, zapisać kod procesu skryptu bezpośrednio po każdym wywołaniu i wykonać kontrolę `Path('_build/experiment.exe').is_file()` przed błędnym buildem i po nim. Samo `execution_attempted=false` nie zastępuje kontroli pliku.

### Poziom C — dwa rozszerzenia automatu

**C1 — powtórzenia.** Argument `--repeat` przyjmuje całkowite wartości 1–10, domyślnie 1. Automat kompiluje raz, następnie uruchamia program kolejno tyle razy, ile wskazano. D07 i D08 dokumentują:

```sh
python3 run_experiment.py --configuration release --case pass --repeat 3
python3 run_experiment.py --configuration release --case fail --repeat 3
```

Każda próba ma własne `run_01_*`, `run_02_*`, `run_03_*` i własny kod w podsumowaniu. D08 musi zachować także drugą i trzecią próbę mimo kodu 1 w pierwszej. Zakres 1–10 i odrzucenie wartości spoza niego potwierdza przegląd kodu; historyczna seria nie obejmuje wykonanych testów wartości granicznych.

**C2 — kontrolowane wejście.** Python i C++ obsługują `--size` w zakresie 1–10000. To zakres przyjęty w rozwiązaniu; PDF wymaga walidacji, lecz nie narzuca tych konkretnych granic. D09 i D10 dokumentują:

```sh
python3 run_experiment.py --configuration release --case pass --size 16
python3 run_experiment.py --configuration release --case pass --size 0
```

W D09 `summary.txt` musi zawierać `size=16`, komenda `--size 16`, a stdout `Input count: 16`. W D10 kompilacja może się zakończyć sukcesem, lecz nie wolno uruchomić programu. Python tworzy listę argumentów, np. `['_build/experiment.exe', '--size', '16']`; tekst `compile_command` lub `run_command` w podsumowaniu jest tylko czytelną reprezentacją. Do wykonania trafia lista z `shell=False`.

Trzeciego rozszerzenia C — rozmiarów plików i czasów modyfikacji — nie wybrano. Nie przypisuje się mu ukończenia na podstawie dodatkowych skrótów kontrolnych z nowej serii.

### Poziom D — konfiguracja YAML

Wymagane są PyYAML i trzy istniejące pliki konfiguracji. Instrukcja odtworzenia w lokalnym środowisku:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python run_experiment.py --config experiment.yaml
.venv/bin/python run_experiment.py --config fixtures/config_missing_field.yaml
.venv/bin/python run_experiment.py --config fixtures/config_bad_case.yaml
```

Powyższe trzy scenariusze odpowiadają zachowanym D11–D13; nie uruchamiano ich ponownie 15 października. Instalacja zależności służy odtworzeniu, nie jest sama dowodem poprawności testu.

Kontrakt konfiguracji wynika z `load_and_validate_config`:

- Wymagane: `configuration` jako `debug` albo `release` oraz `case` jako `pass` albo `fail`.
- Opcjonalne: całkowite `repeat` od 1 do 10 (domyślnie 1) oraz `size` jako `null` lub liczba całkowita 1–10000 (domyślnie `null`, czyli standardowe wejście ośmioelementowe).
- Wartości logiczne nie są przyjmowane jako liczby, a nieznane pola są odrzucane. Korzeń YAML musi być mapowaniem.
- Przy `--config` wartości biegu pochodzą z YAML; odpowiadające im wartości CLI nie są łączone z plikiem. Parser CLI nadal może odrzucić składniowo niepoprawne argumenty przed odczytem pliku.

Ścieżka jest rozwiązywana względem katalogu zadania; po `resolve()` musi pozostać pod nim i wskazywać plik. `yaml.safe_load` ogranicza odczyt do bezpiecznych typów danych, a walidacja sprawdza dopuszczalne pola i wartości. Samo `safe_load` nie zastępuje reguł konfiguracji. Ścieżki poprawnie odnalezionych konfiguracji są zapisywane względnie.

## Surowe wyniki

### Rejestr dowodów

Tabela 3 — pełne przyporządkowanie dowodów do przebiegów. Nazwy historycznych katalogów pozostawiono bez zmian.

| Dowód | Przypadek                                    | Źródło                                                                                  |
| ----- | -------------------------------------------- | --------------------------------------------------------------------------------------- |
| D00   | Metryczka obecna i deklaracja historyczna    | Sekcja środowiska; nowa [metryczka](logs/20261015_171412_190703_manual/environment.txt) |
| D01   | Ręczny Clang, 2026-10-15                     | [20261015_171412_190703_manual](logs/20261015_171412_190703_manual/)                    |
| D02   | A, pierwszy `release/pass`                   | [20261006_230805_304087](logs/20261006_230805_304087/)                                  |
| D03   | A, drugi `release/pass`                      | [20261006_230805_709909](logs/20261006_230805_709909/)                                  |
| D04   | B, `release/fail`                            | [20261006_231350_867382](logs/20261006_231350_867382/)                                  |
| D05   | B, błąd składni                              | [20261006_231351_627316](logs/20261006_231351_627316/)                                  |
| D06   | B, poprawny przebieg po naprawie             | [20261006_231351_947869](logs/20261006_231351_947869/)                                  |
| D07   | C1, `--repeat 3`, sukces                     | [20261006_232116_949515](logs/20261006_232116_949515/)                                  |
| D08   | C1, `--repeat 3`, niepowodzenie              | [20261006_232117_906847](logs/20261006_232117_906847/)                                  |
| D09   | C2, `--size 16`                              | [20261006_232121_612610](logs/20261006_232121_612610/)                                  |
| D10   | C2, `--size 0`                               | [20261006_232122_031292](logs/20261006_232122_031292/)                                  |
| D11   | D, poprawny YAML                             | [20261006_232657_077725](logs/20261006_232657_077725/)                                  |
| D12   | D, brak `configuration`                      | [20261006_232657_818191](logs/20261006_232657_818191/)                                  |
| D13   | D, niedozwolony `case`                       | [20261006_232657_871576](logs/20261006_232657_871576/)                                  |
| D14   | Nowa kontrola B, poprawny build przed błędem | [20261015_171413_158109](logs/20261015_171413_158109/)                                  |
| D15   | Nowa kontrola B, błąd i brak starego EXE     | [20261015_171413_703435](logs/20261015_171413_703435/)                                  |
| D16   | Nowa kontrola B, przywrócone źródło          | [20261015_171414_012492](logs/20261015_171414_012492/)                                  |

### Rola plików w katalogu dowodów

Tabela 4 — artefakty i sposób ich interpretacji.

| Plik                                     | Znaczenie                                                                                                    |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `compile_stdout.txt`                     | Zwykłe wyjście kompilatora, również gdy jest puste.                                                          |
| `compile_stderr.txt`                     | Ostrzeżenia i błędy kompilatora; nie należy ich usuwać z dowodów.                                            |
| `run_stdout.txt`, `run_stderr.txt`       | Strumienie jednej próby w historycznych A–B oraz ręcznym D01.                                                |
| `run_NN_stdout.txt`, `run_NN_stderr.txt` | Osobne strumienie kolejnych prób w C/D i obecnym automacie.                                                  |
| `summary.txt`                            | Polecenia, parametry, kody procesów potomnych, czasy i decyzja automatu; zakres zależy od wykonanych etapów. |
| `environment.txt`                        | Aktualne wersje i identyfikacja poprawnej wersji odniesienia, tylko nowe kontrole.                           |
| `verification.txt`                       | Zewnętrzna kontrola kodu skryptu, istnienia EXE i obecności plików wykonania, D14–D16.                       |
| `script_stdout.txt`, `script_stderr.txt` | Strumienie samego skryptu, odrębne od strumieni C++, D14–D16.                                                |
| `criteria.txt`, `executable_format.txt`  | Kryterium ręcznej próby i identyfikacja formatu wyniku, D01.                                                 |
| `main_invalid.cpp`                       | Dokładna kopia kontrolowanego błędu składni z D15; nie jest źródłem do budowania właściwego rozwiązania.     |

Przy błędzie kompilacji brak `run_*` oznacza prawidłowe zatrzymanie. Przy `config_error` nie ma również `compile_*`, ponieważ kompilacji nie podjęto. Pusty plik z faktycznie wykonanego etapu i brak pliku z etapu pominiętego niosą różne informacje.

### D01–D03 — przebieg poprawny

D01: [summary.txt](logs/20261015_171412_190703_manual/summary.txt) ma `compile_exit_code=0`, `fresh_executable_exists=true`, `run_exit_code=0`. Oba strumienie kompilatora i stderr programu są puste. Pełny [stdout ręcznej próby](logs/20261015_171412_190703_manual/run_stdout.txt):

```text
Case: normal
Input count: 8
Result correct: true
```

D02 i D03 mają ten sam wynik stdout. Istotne wartości w obu historycznych podsumowaniach:

```text
compile_exit_code=0
execution_attempted=true
run_exit_code=0
final_status=passed
compiler_backend=clang++
```

Są to odrębne katalogi, oba zachowane z pełnymi pięcioma plikami. Obecny kod sprawdza także istnienie programu; nie dopisano tej obserwacji wstecz do historycznych `summary.txt`.

### D04 — symulowana awaria programu

Zwykłe wyjście z [run_stdout.txt](logs/20261006_231350_867382/run_stdout.txt):

```text
Case: simulated failure
Input count: 8
Result correct: false
```

Diagnostyka z [run_stderr.txt](logs/20261006_231350_867382/run_stderr.txt):

```text
ERROR: result differs from the reference
```

[Podsumowanie D04](logs/20261006_231350_867382/summary.txt) pokazuje poprawną kompilację (`compile_exit_code=0`) i faktyczne wykonanie (`execution_attempted=true`), ale `run_exit_code=1` i `final_status=run_failed`. Jest to oczekiwane wykrycie kontrolowanego niepowodzenia.

### D05–D06 — błąd kompilacji i powrót do poprawnego przebiegu

Pełna diagnostyka historycznej kompilacji w [compile_stderr.txt](logs/20261006_231351_627316/compile_stderr.txt):

```text
main.cpp:44:42: error: expected ';' at end of declaration
   44 |   const bool correct = result == expected
      |                                          ^
      |                                          ;
1 error generated.
```

Istotne wartości [podsumowania D05](logs/20261006_231351_627316/summary.txt):

```text
compile_exit_code=1
execution_attempted=false
run_exit_code=not_started
final_status=compile_failed
```

D05 zawiera dwa strumienie kompilatora i podsumowanie, bez plików wykonania. Numer linii odnosi się do ówczesnej wersji źródła. D06 potwierdza `compile_exit_code=0`, `run_exit_code=0`, `passed` i ponownie `Result correct: true`. Sam brak starego EXE nie był zapisany w D05; tę lukę zamyka D15.

### D07–D08 — powtórzenia mimo niepowodzenia

Tabela 5 — kody i kompletność trzech prób, na podstawie podsumowań D07 i D08.

| Dowód | Próba 01 | Próba 02 | Próba 03 | Pary stdout/stderr | Status       |
| ----- | -------- | -------- | -------- | ------------------ | ------------ |
| D07   | 0        | 0        | 0        | 3                  | `passed`     |
| D08   | 1        | 1        | 1        | 3                  | `run_failed` |

W D07 każda próba ma `Result correct: true` i pusty stderr. W D08 każda ma `Result correct: false` oraz `ERROR: result differs from the reference`. Podsumowanie D08 zachowuje:

```text
repeat=3
run_01_exit_code=1
run_02_exit_code=1
run_03_exit_code=1
```

Obecność plików prób 02 i 03 potwierdza, że zapis nie zatrzymał się po pierwszej awarii. Nie opieramy tego wniosku wyłącznie na istnieniu pętli w kodzie.

### D09–D10 — przekazanie rozmiaru i walidacja

W D09 `summary.txt` zawiera `size=16` i `run_command=_build/experiment.exe --size 16`; stdout:

```text
Case: normal
Size argument: 16
Input count: 16
Result correct: true
```

W D10 kompilacja zakończyła się kodem 0, lecz nie powstały pliki wykonania. Istotne wartości podsumowania:

```text
size=0
compile_exit_code=0
execution_attempted=false
run_exit_code=not_started
final_status=validation_failed
validation_error=size out of range [1, 10000]
```

To odrzucenie parametru przez automat, nie błąd kompilatora ani wynik błędnego sortowania. Nie należy przypisywać programowi C++ kodu 2 w D10: program w ogóle nie został uruchomiony.

### D11–D13 — konfiguracja YAML i testy samego automatu

Poprawny [experiment.yaml](experiment.yaml):

```yaml
configuration: release
case: pass
repeat: 1
size: null
```

D11 zawiera `config_path=experiment.yaml`, `config_loaded=true`, kod kompilacji 0, kod próby 0 i `passed`. Stdout potwierdza standardowe wejście ośmioelementowe. Plik wskazuje parametry potrzebne do odtworzenia przypadku; nie gwarantuje identycznego czasu na innym komputerze.

D12 i D13 zawierają wyłącznie `summary.txt`. Oba zapisują `config_loaded=false`, `compile_exit_code=not_started`, `execution_attempted=false`, `run_exit_code=not_started` i `final_status=config_error`. Różnią się komunikatem:

```text
config_error=missing required field: configuration
```

```text
config_error=case must be 'pass' or 'fail'
```

D12 potwierdza odrzucenie brakującego pola, D13 niedozwolonej wartości. Pozostałe zabezpieczenia YAML opisano na podstawie przeglądu kodu; tych dwóch fixture'ów nie traktuje się jako testu wszystkich reguł.

### D14–D16 — bezpośrednia kontrola starego EXE

Tabela 6 — nowa sekwencja kontrolna, na podstawie `summary.txt` i niezależnych `verification.txt`.

| Dowód | Stan źródła      | EXE przed | Kod kompilacji | Kod skryptu | EXE po | Liczba plików `run_*` |
| ----- | ---------------- | --------- | -------------- | ----------- | ------ | --------------------- |
| D14   | poprawne         | brak      | 0              | 0           | obecny | 2                     |
| D15   | usunięty średnik | obecny    | 1              | 1           | brak   | 0                     |
| D16   | przywrócone      | brak      | 0              | 0           | obecny | 2                     |

Dokładne obserwacje [verification.txt D15](logs/20261015_171413_703435/verification.txt):

```text
script_exit_code=1
executable_before=true
executable_after=false
run_file_count=0
source_matches_original=false
```

[Podsumowanie D15](logs/20261015_171413_703435/summary.txt) potwierdza `execution_attempted=false` i `run_exit_code=not_started`. Diagnostyka wskazuje brak średnika w linii 84 aktualnej kopii. D16 ma `source_matches_original=true` i ten sam hash poprawnego źródła co D14. Zewnętrzna kontrola i strumienie skryptu są dodatkowymi artefaktami; nie dopisywano pól do surowego podsumowania automatu.

## Opracowanie wyników

Tabela 7 — zestawienie wyników automatyzacji. `not_started` oznacza etap pominięty, a nie kod procesu.

| Dowód   | Kompilacja    | Wykonanie     | `final_status`         | Podstawa oceny                               |
| ------- | ------------- | ------------- | ---------------------- | -------------------------------------------- |
| D01     | 0             | 0             | `passed` próby ręcznej | Nowy plik i zgodność wyniku.                 |
| D02–D03 | 0             | 0             | `passed`               | Dwa niezależne katalogi.                     |
| D04     | 0             | 1             | `run_failed`           | Rozdzielone strumienie kontrolowanej awarii. |
| D05     | 1             | `not_started` | `compile_failed`       | Diagnostyka, brak wykonania.                 |
| D06     | 0             | 0             | `passed`               | Wynik po historycznej naprawie.              |
| D07     | 0             | 0, 0, 0       | `passed`               | Komplet trzech prób.                         |
| D08     | 0             | 1, 1, 1       | `run_failed`           | Kontynuacja po pierwszym niepowodzeniu.      |
| D09     | 0             | 0             | `passed`               | Potwierdzone 16 elementów.                   |
| D10     | 0             | `not_started` | `validation_failed`    | Rozmiar odrzucony przed wykonaniem.          |
| D11     | 0             | 0             | `passed`               | Konfiguracja załadowana i wykonana.          |
| D12–D13 | `not_started` | `not_started` | `config_error`         | Walidacja zatrzymała procedurę.              |
| D14     | 0             | 0             | `passed`               | Utworzenie EXE przed testem błędu.           |
| D15     | 1             | `not_started` | `compile_failed`       | Bezpośrednio potwierdzony brak starego EXE.  |
| D16     | 0             | 0             | `passed`               | Przywrócone źródło i poprawny nowy build.    |

Nie wyznacza się zwycięzcy czasowego ani statystyk benchmarku. Czasy w podsumowaniach dokumentują przebieg procesów. Ta lekcja bada poprawność sterowania i wiarygodność dowodów; do porównywania kosztu sortowania potrzebny byłby osobny eksperyment.

## Interpretacja

### Poziom A — co potwierdza sukces

D01 potwierdza, że bieżący program można zbudować i uruchomić bez automatu. D02–D03 pokazują dwa zapisane wykonania tego samego wariantu i zachowanie oddzielnych dowodów. `passed` ma znaczenie dopiero razem z kontrolą kompilacji, nowego programu i kodu wykonania. D14 dodatkowo wykazuje zmianę stanu z braku pliku na obecność nowego EXE. Sam tekst `Result correct: true` nie zastąpi kodu zakończenia, ale jest dodatkowym sprawdzeniem, że uruchomiono oczekiwany przypadek.

### Poziom B — awaria badanego programu a awaria procedury

D04 kończy się `run_failed`, ponieważ program został uruchomiony i zwrócił 1. Ten negatywny wynik programu jest pozytywną kontrolą zdolności automatu do wykrywania niepowodzeń. D05/D15 kończą się wcześniej: błąd składni uniemożliwia powstanie programu. D15 potwierdza także brak pliku z wcześniejszego poprawnego buildu; eliminuje to konkretny fałszywy sukces polegający na uruchomieniu starego EXE.

`environment_error` oznacza w aktualnym kodzie brak obu obsługiwanych kompilatorów. To inny etap niż `compile_failed`, gdzie kompilację podjęto, lecz zwróciła błąd lub nie wytworzyła pliku. `run_failed` oznacza niezerowy kod podjętego wykonania. `environment_error` opisano na podstawie kodu, bez deklarowania wykonanego testu braku narzędzi. D06 i D16 dokumentują powrót do poprawnego przebiegu po usunięciu celowego błędu.

### Poziom C — kompletność prób i kontrola wejścia

D07–D08 pokazują działanie dwóch ścieżek `--repeat`: sukcesu i awarii programu. Ponieważ każdy wynik pozostaje zapisany, późniejsza próba nie usuwa informacji o poprzedniej. Zbiorczy status korzysta z wszystkich kodów, choć ogólne `run_exit_code` zawiera tylko ostatni. Sam ostatni kod nie jest wystarczającym podsumowaniem dowolnej mieszanej serii.

D09 potwierdza pełny przepływ wartości 16: argument skryptu → podsumowanie → lista argumentów C++ → 16 elementów i poprawne porównanie z wzorcem. D10 potwierdza zatrzymanie wartości 0 przed wykonaniem. Walidacja po kompilacji spełnia wymóg sprawdzenia przed uruchomieniem, lecz wykonuje niepotrzebny build dla niepoprawnego rozmiaru. To cecha obecnego rozwiązania, nie brak dowodów kompilacji.

### Poziom D — uzasadnienie projektu i granice potwierdzenia

YAML oddziela wybór przypadku od ręcznie przepisywanej komendy. Wymagane `configuration` i `case` chronią przed uruchomieniem przypadkowego scenariusza przy niepełnym pliku. Wyłączność parametrów YAML zapewnia jeden zestaw wartości biegu, lecz poprawnie sparsowane wartości CLI mogą zostać przy `--config` zignorowane — tę regułę trzeba znać podczas odtwarzania.

D11 dowodzi poprawnego odczytu i wykonania konkretnej konfiguracji. D12–D13 dowodzą dwóch odrzuceń przed build/run; brak strumieni z tych etapów jest oczekiwanym wynikiem. Przegląd kodu potwierdza też reguły ścieżki, typów i nieznanych pól, ale nie zastępuje testu każdej z nich. Nie wyciąga się wniosku, że cała obsługa YAML jest bezbłędna lub odporna na wszystkie możliwe pliki.

## Ograniczenia eksperymentu

1. Jedna maszyna macOS/arm64 i dwie daty kontroli. Nie wykonano procedury w Windows/MSVC ani Developer PowerShell; zgodność backendu `cl` nie została sprawdzona wykonaniem.
2. D02–D13 są historycznymi dowodami wcześniejszych wersji. Inne nazwy strumieni A–B i inne numery linii diagnostyki są zachowane zgodnie z pochodzeniem. Nie ma w nich hashy wiążących wszystkie ówczesne źródła z obecnym kodem.
3. Pierwotny raport nie zawierał dowodu D01 ani niezależnej kontroli braku EXE po błędzie. Uzupełnienie z 15 października potwierdza obecną wersję, nie rekonstruuje brakujących historycznych obserwacji.
4. Nowa sekwencja B była pojedynczą kontrolą w izolowanej kopii. Przypadki celowe badają określone ścieżki; nie wykazują pełnego pokrycia wszystkich awarii systemowych i wyjątków procesu.
5. Testy C obejmują `repeat=3` dla pass/fail i `size=16`/`size=0`. Nie wykonano pełnego przeglądu wartości granicznych `repeat` ani maksymalnego rozmiaru. Zakresy i dodatkowa walidacja C++ są potwierdzone przeglądem kodu.
6. D obejmuje trzy istniejące konfiguracje, a nie wszystkie reguły walidacji. Nie wykonano testów ucieczki ścieżki, specjalnych tagów YAML, nieznanych pól ani konfliktu YAML/CLI. `safe_load` i walidacja mają różne role.
7. `environment_error`, timeouty, brak artefaktu przy kodzie kompilacji 0 i nieznane kody zakończenia nie były wywoływane empirycznie. Kod 124 jest konwencją skryptu. Nie deklaruje się osobnych statusów D dla tych awarii.
8. `requirements.txt` dopuszcza PyYAML od 6.0, nie przypina konkretnej wersji. Informacja o 6.0.3 pochodzi z wcześniejszego raportu, nie z nowej kontroli zależności.
9. `perf_counter` w D01 deklaruje rozdzielczość około 41,67 ns i monotoniczność. Nie jest to dokładność pomiaru procesu. Zapis milisekund do trzech miejsc oraz narzut uruchomienia, przechwytywania i obciążenia systemu ograniczają interpretację czasów; nie służą one ocenie szybkości Bubble Sortu.
10. W sprawdzonych artefaktach ścieżki są względne. Nie oznacza to gwarancji anonimizacji dowolnej przyszłej diagnostyki; np. tekst błędu dla błędnej ścieżki może zawierać surowy argument użytkownika. Nowe dowody należy sprawdzać przed dołączeniem, zachowując oryginały bez cichej redakcji.
11. Nie wybrano manifestu C, CI ani odrębnego rozszerzenia D o SHA-256. Szkolne progi ocen zależą również od poprawności, obrony pracy i spełnienia warunków prowadzącego; zaznaczony zakres A–D nie jest obietnicą oceny.

## Wnioski

1. **A:** D01 dokumentuje ręczne zbudowanie bieżącego programu i zgodny wynik z kodem 0. D02–D03 zachowują dwa osobne automatyczne przebiegi poprawne; D14 potwierdza utworzenie pliku w bieżącej wersji.
2. **B:** D04 zachowuje rozdzielone stdout/stderr i kod programu 1 dla celowej awarii. D05 oraz D15 zatrzymują automat po błędzie kompilacji; nie jest to awaria wykonanego programu.
3. **B:** D15 potwierdza bezpośrednio, że stary EXE istniał przed próbą, a po niej nie istnieje i nie ma plików wykonania. D16 potwierdza przywrócenie poprawnych bajtów źródła i sukces kolejnego buildu.
4. **C1:** D07–D08 zachowują wszystkie trzy pary strumieni i kody prób, także po pierwszym niepowodzeniu. Wynik zbiorczy należy czytać razem z kodami każdej próby.
5. **C2:** D09 potwierdza przekazanie rozmiaru 16 i poprawny wynik; D10 odrzuca 0 przed uruchomieniem. Wybrany zakres i listy argumentów są jawne w kodzie.
6. **D:** D11–D13 wykazują działanie konfiguracji poprawnej oraz odrzucenie dwóch konkretnych błędów bez przechodzenia do kompilacji. Nie dowodzą pełnej poprawności wszystkich zabezpieczeń YAML.
7. Zapis strumieni, kodów i decyzji w osobnych katalogach pozwala prześledzić przyczynę sukcesu lub zatrzymania. Jest to lokalna podstawa linii CI, ale w tej pracy nie wykonano wybranego rozszerzenia CI ani benchmarku sortowania.

## Wykorzystanie AI i sposób weryfikacji

Codex pomógł zbudować programy A–D, zapisać stdout, oraz uporządkować raport na podstawie mocka.

Weryfikacja obejmuje: porównanie wszystkich istniejących logów z ich skrótami sprzed korekty; sprawdzenie stdout i kodów D02–D04; diagnostykę i brak wykonania D05; kod 0 i poprawny wynik D06; komplet trzech par oraz kody 0/0/0 i 1/1/1 w D07–D08; zgodność rozmiaru 16 w D09 oraz zatrzymanie D10; brak kompilacji i wykonania D12–D13; ręczny kod 0 D01; obserwacje EXE i kody skryptu 0/1/0 w D14–D16; przywrócenie dokładnych bajtów źródła; sprawdzenie względnych odnośników i anonimizacji nowych artefaktów.
