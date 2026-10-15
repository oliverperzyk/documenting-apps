# TiDPI 05 — poziomy A–D

Kryptonim: **Regulus**.

## Oddanie

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
└── logs/          # dowody A–D (nazwy nadane przez automat)
```

- Poziom C: `--repeat` + `--size` (bez manifestu).
- Poziom D: konfiguracja YAML (`--config`, `yaml.safe_load`, status `config_error`).

Nie oddawaj szkolnego PDF-u, katalogu `_build/` ani `.venv/`.

## Środowisko Python (poziom D)

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Dalej używaj `.venv/bin/python` (Homebrew Python blokuje systemowy `pip` — PEP 668).

## Odtworzenie

### Ręcznie (Clang)

```sh
mkdir -p _build
clang++ -std=c++17 -Wall -Wextra -pedantic -O2 -DNDEBUG -o _build/experiment.exe main.cpp
./_build/experiment.exe
```

### Automat — CLI (A–C)

```sh
python3 run_experiment.py --configuration release --case pass
python3 run_experiment.py --configuration release --case fail
python3 run_experiment.py --configuration release --case pass --repeat 3
python3 run_experiment.py --configuration release --case pass --size 16
```

### Automat — YAML (D)

```sh
.venv/bin/python run_experiment.py --config experiment.yaml
.venv/bin/python run_experiment.py --config fixtures/config_missing_field.yaml
.venv/bin/python run_experiment.py --config fixtures/config_bad_case.yaml
```

Przy `--config` parametry biegu pochodzą wyłącznie z pliku YAML. Błąd walidacji → `final_status=config_error`, bez kompilacji i bez `run_*`.
