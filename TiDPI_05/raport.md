---
title: "TiDPI 05 - Automatyzacja kompilacji, uruchomienia i rejestracji wyniku"
author: "Kryptonim TiDPI: Regulus"
date: "2026-10-06"
lang: pl-PL
---

# Sprawozdanie TiDPI 05 — automatyzacja kompilacji, uruchomienia i rejestracji wyniku

## Kryptonim TiDPI i wykonany poziom

- Kryptonim: **Regulus**.
- Lekcja: TiDPI 05, automatyzacja kompilacji, uruchomienia i rejestracji wyniku.
- Data prób: 2026-10-06.
- Zakres ukończony i sprawdzony: **poziomy A–D**.
- Checklist zakresu:
  - [x] A
  - [x] B
  - [x] C
  - [x] D
- Odstępstwa: materiał zakłada Visual Studio 2022, `cl.exe` i Windows. Prace wykonano na macOS/arm64 z Apple Clang oraz `python3`. W [run_experiment.py](run_experiment.py) dodano wybór backendu: `cl` albo `clang++`. Zależność poziomu D: PyYAML (`requirements.txt`, lokalny `.venv`).
- Wersja programu: [main.cpp](main.cpp) — listing + `--size`. Automat: [run_experiment.py](run_experiment.py) z `--repeat`, `--size`, `--config`.
- Poziom C — wybrane **dwa z trzech**: `--repeat` oraz `--size` (bez manifestu).
- Poziom D — **konfiguracja YAML** z `yaml.safe_load`, walidacją pól i izolacją ścieżki.

### Oddane pliki (poziomy A–D)

```text
TiDPI_05/
├── raport.md
├── main.cpp
├── run_experiment.py
├── experiment.yaml
├── requirements.txt
├── README.md
├── .gitignore
├── fixtures/
│   ├── config_missing_field.yaml
│   └── config_bad_case.yaml
└── logs/
    ├── 20261006_230805_304087/          # A: release/pass (1)
    ├── 20261006_230805_709909/          # A: release/pass (2)
    ├── 20261006_231350_867382/          # B: release/fail
    ├── 20261006_231351_627316/          # B: compile_failed
    ├── 20261006_231351_947869/          # B: pass po naprawie
    ├── 20261006_232116_949515/          # C: --repeat 3 pass
    ├── 20261006_232117_906847/          # C: --repeat 3 fail
    ├── 20261006_232121_612610/          # C: --size 16 pass
    ├── 20261006_232122_031292/          # C: --size 0 validation_failed
    ├── 20261006_232657_077725/          # D: --config experiment.yaml
    ├── 20261006_232657_818191/          # D: config_error (brak pola)
    └── 20261006_232657_871576/          # D: config_error (zły case)
```

- Konfiguracja poprawna: [experiment.yaml](experiment.yaml).
- Fixtures awarii: [fixtures/config_missing_field.yaml](fixtures/config_missing_field.yaml), [fixtures/config_bad_case.yaml](fixtures/config_bad_case.yaml).
- D YAML pass: [logs/20261006_232657_077725/](logs/20261006_232657_077725/).
- D brak pola: [logs/20261006_232657_818191/](logs/20261006_232657_818191/).
- D zły case: [logs/20261006_232657_871576/](logs/20261006_232657_871576/).

## Cel i hipoteza

Cel poziomu A: łańcuch *kompilacja → uruchomienie → dowody w `logs/<run_id>/`* z decyzją po kodach wyjścia i artefaktach, nie po samym tekście konsoli.

Hipoteza A: ręczne Clang Release-equivalent → exit 0; dwa automatyczne `release`/`pass` → osobne katalogi z `final_status=passed`.

Cel poziomu B: ścieżki niepowodzenia (`fail`, błąd składni, pass po naprawie) oraz rozróżnienie `environment_error` / `compile_failed` / `run_failed`.

Hipoteza B: `fail` → kod 1 i `run_failed`; błąd składni → `compile_failed`, `execution_attempted=false`, brak EXE; po naprawie → `passed`.

Cel poziomu C: `--repeat` (osobne `run_NN_*`, bez przerywania po awarii) oraz `--size` (walidacja 1…10000, wartość w summary, argv bez `shell=True`).

Hipoteza C: `repeat 3` pass/fail zapisuje trzy pary i trzy kody; `size 16` → `passed`; `size 0` → `validation_failed` bez `run_*`.

Cel poziomu D: powtarzalna linia parametrów w pliku YAML pod kontrolą wersji, z bezpiecznym odczytem i walidacją — zły plik nie ma uruchamiać kompilacji ani programu z domyślnymi wartościami.

Hipoteza D: poprawny [experiment.yaml](experiment.yaml) da `config_loaded=true` i `passed`; brak wymaganego pola oraz niedozwolony `case` dadzą `config_error`, `compile_exit_code=not_started`, brak `compile_*`/`run_*`.

## Środowisko oraz konfiguracja

Tabela 1 — narzędzia faktycznie użyte (D00).

| Element          | Wartość                    | Dowód                |
| ---------------- | -------------------------- | -------------------- |
| System           | macOS 27.0.1, build 26A434 | D00                  |
| Architektura     | arm64 (Apple Silicon)      | D00                  |
| Python           | 3.14.4 + lokalny `.venv`   | D00 / D              |
| PyYAML           | 6.0.3                      | D / requirements.txt |
| Kompilator       | Apple Clang 21.0.0, C++17  | D00                  |
| MSVC `cl.exe`    | niedostępny                | D00                  |
| Konfiguracja     | Release: `-O2 -DNDEBUG`    | D01–D13              |
| Backend automatu | `clang++`                  | D02–D13              |

### D00 — wersje narzędzi

```text
host=macOS 27.0.1 build 26A434
arch=arm64
Python 3.14.4
Apple clang version 21.0.0 (clang-2100.3.34.2)
Target: arm64-apple-darwin27.0.0
cl: not found
actual_toolchain: Apple Clang + python3 on macOS arm64 (odstępstwo od MSVC)
```

## Zmienne i warunki eksperymentu

- Źródło: [main.cpp](main.cpp); automat: [run_experiment.py](run_experiment.py); dowody: `logs/<run_id>/`.
- Przed kompilacją: `unlink` starego `_build/experiment.exe`.
- C: `--repeat` → `run_NN_*`; `passed` tylko gdy wszystkie kody = 0; `--size` walidowane przed run.
- D: `--config PATH` — parametry biegu **wyłącznie** z YAML (bez mieszania z CLI). Ścieżka musi leżeć pod katalogiem projektu. Odczyt: `yaml.safe_load`. Required: `configuration`, `case`.

## Procedura

### Poziom A

1. Narzędzia (D00); ręczna kompilacja Clang.
2. Dwa przebiegi `release`/`pass` → D02, D03.

### Poziom B

1. `release`/`fail` → D04.
2. Błąd składni → D05; przywrócenie kodu → D06.

### Poziom C

1. `--repeat 3` pass/fail → D07, D08.
2. `--size 16` / `--size 0` → D09, D10.

### Poziom D

1. `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`
2. `.venv/bin/python run_experiment.py --config experiment.yaml` → D11.
3. `--config fixtures/config_missing_field.yaml` → D12.
4. `--config fixtures/config_bad_case.yaml` → D13.

## Surowe wyniki

### Rejestr dowodów

- **D00–D01:** środowisko i ręczny Clang.
- **D02–D03:** A pass — [logs/20261006_230805_304087/](logs/20261006_230805_304087/), [logs/20261006_230805_709909/](logs/20261006_230805_709909/).
- **D04–D06:** B — [logs/20261006_231350_867382/](logs/20261006_231350_867382/), [logs/20261006_231351_627316/](logs/20261006_231351_627316/), [logs/20261006_231351_947869/](logs/20261006_231351_947869/).
- **D07–D10:** C — [logs/20261006_232116_949515/](logs/20261006_232116_949515/), [logs/20261006_232117_906847/](logs/20261006_232117_906847/), [logs/20261006_232121_612610/](logs/20261006_232121_612610/), [logs/20261006_232122_031292/](logs/20261006_232122_031292/).
- **D11:** D YAML OK — [logs/20261006_232657_077725/](logs/20261006_232657_077725/).
- **D12:** D brak `configuration` — [logs/20261006_232657_818191/](logs/20261006_232657_818191/).
- **D13:** D zły `case` — [logs/20261006_232657_871576/](logs/20261006_232657_871576/).

### Rola plików w katalogu dowodów

| Plik                                | Rola                                             |
| ----------------------------------- | ------------------------------------------------ |
| `compile_*.txt`                     | Zrzuty kompilatora (gdy kompilacja wystartowała) |
| `run_stdout.txt` / `run_stderr.txt` | A–B (historyczne nazwy)                          |
| `run_NN_*.txt`                      | C/D — osobna para na próbę                       |
| `summary.txt`                       | Status, kody, `config_path` / `config_error` (D) |

Przy `compile_failed`, `validation_failed` i `config_error` plików `run_*` nie ma. Przy `config_error` nie ma też `compile_*`.

### D02–D10 (skrót A–C)

Jak w poprzednich iteracjach: dwa pass A; fail/compile_failed/pass B; repeat i size C — statusy w tabeli 2 poniżej; pełne pliki w `logs/`.

### D11 — poprawny YAML

Pełne dowody: [logs/20261006_232657_077725/](logs/20261006_232657_077725/).

| Klucz                    | Wartość                                |
| ------------------------ | -------------------------------------- |
| `config_path`            | `experiment.yaml`                      |
| `config_loaded`          | `true`                                 |
| `configuration` / `case` | `release` / `pass`                     |
| `final_status`           | `passed`                               |
| pliki                    | `compile_*`, `run_01_*`, `summary.txt` |

### D12 — brak wymaganego pola

Pełne dowody: [logs/20261006_232657_818191/](logs/20261006_232657_818191/) — tylko `summary.txt`.

| Klucz                 | Wartość                                 |
| --------------------- | --------------------------------------- |
| `final_status`        | `config_error`                          |
| `config_error`        | `missing required field: configuration` |
| `compile_exit_code`   | `not_started`                           |
| `execution_attempted` | `false`                                 |

### D13 — niedozwolony `case`

Pełne dowody: [logs/20261006_232657_871576/](logs/20261006_232657_871576/) — tylko `summary.txt`.

| Klucz               | Wartość                         |
| ------------------- | ------------------------------- |
| `final_status`      | `config_error`                  |
| `config_error`      | `case must be 'pass' or 'fail'` |
| `compile_exit_code` | `not_started`                   |

## Zestawienie statusów

Tabela 2 — obserwacje D02–D13.

| Dowód   | Przypadek        | `final_status`    | Uwagi                |
| ------- | ---------------- | ----------------- | -------------------- |
| D02–D03 | release/pass     | passed            | A                    |
| D04     | release/fail     | run_failed        | kod 1                |
| D05     | błąd składni     | compile_failed    | brak EXE             |
| D06     | pass po naprawie | passed            |                      |
| D07     | repeat 3 pass    | passed            | trzy kody 0          |
| D08     | repeat 3 fail    | run_failed        | trzy kody 1          |
| D09     | size 16          | passed            |                      |
| D10     | size 0           | validation_failed | brak run_\*          |
| D11     | YAML OK          | passed            | `config_loaded=true` |
| D12     | brak pola        | config_error      | bez compile          |
| D13     | zły case         | config_error      | bez compile          |

### Różnica statusów końcowych

| Status              | Znaczenie                                            |
| ------------------- | ---------------------------------------------------- |
| `environment_error` | Brak kompilatora                                     |
| `config_error`      | Plik YAML / ścieżka / walidacja pól — bez kompilacji |
| `compile_failed`    | Kompilacja nie dała kodu 0 / EXE                     |
| `validation_failed` | Argument CLI poza zakresem po kompilacji             |
| `run_failed`        | Program wystartował, próba z kodem ≠ 0               |
| `passed`            | Kompilacja OK, wszystkie próby kod 0                 |

## Interpretacja

### Poziomy A–C

Jak wcześniej: łańcuch pass/fail/compile_failed; `--repeat` nie ucina zapisu; `--size` walidowane przed run.

### Poziom D — konfiguracja YAML

**Problem:** CLI jest wygodne do jednorazowych prób, ale powtarzalna linia testowa wymaga parametrów w pliku pod kontrolą wersji. Zły plik nie może „po cichu” odpalić domyślnego `release`/`pass`.

**Bezpieczeństwo:** wyłącznie `yaml.safe_load` (bez wykonywania tagów); ścieżka po `resolve()` musi leżeć pod katalogiem projektu; root = mapping; wymagane `configuration` i `case`; nieznane pola odrzucane.

**Precedencja:** przy `--config` parametry biegu pochodzą tylko z YAML — jednoznaczna obrona przed mieszaniem z CLI.

**Dowody testów automatu:** D11 sukces; D12/D13 awarie walidacji z `config_error` i zatrzymaniem przed kompilacją.

## Ograniczenia eksperymentu

1. Manifest C i rozszerzenia D inne niż YAML (SHA-256, CI) nie wykonano.
2. Zależność od PyYAML / lokalnego venv (PEP 668 na Homebrew Python).
3. Nie użyto MSVC.
4. `environment_error` nie był wywoływany empirycznie.
5. W `summary` ścieżki config są względne (anonimizacja).

## Wnioski

1. A–C: automat rozróżnia sukces, awarię programu, kompilacji i walidacji argumentów.
2. D: YAML daje powtarzalną konfigurację; `safe_load` + walidacja + izolacja ścieżki blokują złe pliki przed build/run.
3. Status `config_error` jest osobną klasą awarii automatu — testowaną fixture’ami D12/D13.

## Wykorzystanie AI i sposób weryfikacji

Asystent pomógł rozbudować automat o `--config`, pliki YAML/fixtures, przebiegi D11–D13 oraz ten raport. Statusy pochodzą z `logs/`.

Sprawdzono ręcznie: D11 `config_loaded=true` i `passed`; D12/D13 tylko `summary.txt`, `compile_exit_code=not_started`, komunikaty o brakującym polu / złym `case`; katalogi A–C nietknięte.
