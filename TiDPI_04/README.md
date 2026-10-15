# TiDPI 04 — poziomy A–D

Kryptonim: **Regulus**.

## Oddanie

```text
TiDPI_04/
├── raport.md
├── main.cpp
├── wyniki/
│   ├── A_bazowy.txt
│   ├── A_zmieniony_seed.txt
│   ├── A_zmieniony_generator.txt
│   ├── A_powtorzony.txt
│   ├── Release_metadane.txt
│   └── debug/ (archiwum poprzedniej serii)
├── scripts/
│   ├── uruchom_release.py
│   └── opracuj_wyniki.py
├── images/
│   ├── B_porownania.png
│   └── D_std_sort_porownania.png
└── rozszerzenia/
    ├── C/
    │   ├── wiele_seedow/
    │   │   ├── main.cpp
    │   │   └── output.txt
    │   └── bez_early_exit/
    │       ├── main.cpp
    │       └── output.txt
    └── D/
        ├── main.cpp
        └── output.txt
```

- `raport.md` — sprawozdanie poziomów A–D (dowody D00–D08)
- `main.cpp` — program bazowy
- `wyniki/` — stdout poziomu A (B korzysta z `A_bazowy.txt`)
- `images/B_porownania.png` — wykres B
- `images/D_std_sort_porownania.png` — wykres D (Bubble vs `std::sort`)
- `rozszerzenia/C/` — wiele seedów + early-exit
- `rozszerzenia/D/` — porównania `std::sort` z komparatorem liczącym

Dodatkowo: `wyniki/A_powtorzony.txt` zawiera drugie uruchomienie bazowe, a `wyniki/Release_metadane.txt` — datę, środowisko, flagi, skróty źródeł oraz kody wyjścia. Stare outputy Debug z 2026-10-02 zachowano w `wyniki/debug/` (trzy warianty A oraz `C_wiele_seedow.txt`, `C_bez_early_exit.txt`, `D_std_sort.txt`). Raport i wykresy korzystają z Release z 2026-10-09.

Nie oddawaj szkolnego PDF-u ani katalogów `.build/`.

## Odtworzenie

Uruchamiaj programy z terminala bez debuggera. Pełną serię Release (trzy warianty A, oba C, D i powtórzenie bazowe) odtwarza skrypt:

```sh
python3 scripts/uruchom_release.py
python3 scripts/opracuj_wyniki.py
```

Drugi skrypt wymaga `matplotlib`; można użyć istniejącego interpretera `.build/venv/bin/python`, jeśli środowisko jest dostępne. Odtwarza tabele i wykresy z zapisanych outputów. Opcja `--check` tylko weryfikuje dane. Pierwszy skrypt zastępuje główne outputy, zachowując archiwum Debug; kopie źródeł obu wariantów A tworzy w `.build/release/`, bez edycji `main.cpp`. Ich nagłówki opisują faktyczne mapowanie generatora.

Po nowej serii należy także zaktualizować datę, metryczkę i interpretację tekstową raportu zgodnie z rzeczywistymi wynikami. Poniżej polecenia do uruchomienia pojedynczych badań.

### Poziom A (Release)

```sh
mkdir -p .build
clang++ -std=c++17 -O2 -DNDEBUG -Wall -Wextra -pedantic -o .build/main_release main.cpp
./.build/main_release
```

### Poziom B

Filtruj w `wyniki/A_bazowy.txt` wiersze `seed=20260401`. Wykres: `images/B_porownania.png`.

### Poziom C1 — wiele seedów

```sh
clang++ -std=c++17 -O2 -DNDEBUG -Wall -Wextra -pedantic \
  -o .build/c_wiele_seedow rozszerzenia/C/wiele_seedow/main.cpp
./.build/c_wiele_seedow > rozszerzenia/C/wiele_seedow/output.txt
```

### Poziom C2 — bez early-exit

```sh
clang++ -std=c++17 -O2 -DNDEBUG -Wall -Wextra -pedantic \
  -o .build/c_bez_early_exit rozszerzenia/C/bez_early_exit/main.cpp
./.build/c_bez_early_exit > rozszerzenia/C/bez_early_exit/output.txt
```

### Poziom D — porównania `std::sort`

```sh
clang++ -std=c++17 -O2 -DNDEBUG -Wall -Wextra -pedantic \
  -o .build/d_std_sort rozszerzenia/D/main.cpp
./.build/d_std_sort > rozszerzenia/D/output.txt
```

Parametry: seed `20260401`, algorytmy `bubble` i `std_sort` (komparator `CountingLess`), trzy układy, cztery rozmiary. Wykres: `images/D_std_sort_porownania.png`.
