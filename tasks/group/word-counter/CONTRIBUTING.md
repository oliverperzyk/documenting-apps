# Uruchomienie i przygotowanie materiałów

Polecenia wykonuj z katalogu `word-counter`. Wymagane: Python 3.11+, kompilator C++17 i zależności z `requirements-analysis.txt` do wykresów. Do PDF potrzebne są Pandoc, XeLaTeX (TeX Live z polskim wsparciem językowym, `fvextra`, `xurl`, `seqsplit`, `etoolbox`) oraz fonty TeX Gyre Pagella, TeX Gyre Heros i Latin Modern Mono. Na potrzeby sprawdzenia PDF użyto również Popplera (`pdfinfo`, `pdftotext`, `pdftoppm`). Polecenia powłoki poniżej dotyczą macOS/Linux.

## Kompilacja i uruchomienie

```sh
mkdir -p out
c++ -std=c++17 -O2 -Wall -Wextra -Wpedantic source/cpp/main.cpp -o out/cpp
./out/cpp data/1000B_seed14/long_dense_mixed_1000.txt
python3 -B source/python/main.py data/1000B_seed14/long_dense_mixed_1000.txt
```

Oba programy powinny wypisać 65 słów oraz nieujemny czas w nanosekundach. Nie zastępuj plików wykonywalnych w historycznych katalogach `results/`.

## Testy i analiza

```sh
python3 -B -m unittest discover -s tests -v
python3 -m venv .venv-analysis
.venv-analysis/bin/python -m pip install -r requirements-analysis.txt
.venv-analysis/bin/python -B Analyze.py --output-dir analysis-reproduced
```

Przypadki kontrolne i ręcznie ustalone oczekiwania zapisano w `WordGenerator.FIXTURES`. Testy automatu i analizy obejmują m.in. odrzucanie błędnych prób, duplikaty i brakujące pomiary. Odtworzona analiza korzysta z historycznego przebiegu wskazanego w `Analyze.py`; nie zastępuje materiałów w `analysis/`. Bieżące sumy źródeł w odtworzonej kontroli pochodzenia mogą różnić się od zachowanej migawki sprzed formatowania.

## Generowanie danych

Zachowany zestaw `data/` zawiera pliki i manifesty z oczekiwaniami oraz SHA-256. Do istniejącego benchmarku używaj właśnie tego zestawu. Interfejs generatora:

```sh
python3 -B WordGenerator.py --output-dir regenerated/1000B_seed14 --sizes 1000 --seed 14
python3 -B WordGenerator.py --output-dir regenerated/100000B_seed42 --sizes 100000 --seed 42
python3 -B WordGenerator.py --output-dir regenerated/1000000B_seed2026 --sizes 1000000 --seed 2026
```

**Znane ograniczenie:** obecny generator zapisuje pliki tekstowe, ale kończy się błędem `KeyError: 'source'` przed zapisaniem manifestu. W słowniku brakuje metadanych `source`. Te polecenia dokumentują parametry danych i obecnie nie stanowią działającej procedury pełnego odtworzenia. Nie uruchamiaj ich nad `data/`. Naprawa generatora i potwierdzenie pochodzenia słownika są osobnym zadaniem. Generator tworzy siedem wariantów na rozmiar; historyczny benchmark wykorzystał pięć wskazanych w swoich metadanych.

## Benchmark

```sh
python3 -B Benchmark.py --repetitions 2 --data-dir data/1000B_seed14
python3 -B Benchmark.py
```

Pierwsze polecenie wykonuje 20 prób kontrolnych, drugie 900 prób (30 na każdą parę język–plik), bez rozgrzewek. Każde tworzy nowy katalog w `results/`. Nie oczekuj identycznych czasów jak w raporcie. Metoda, format CSV i statusy są opisane w [BENCHMARK.md](BENCHMARK.md).

## Eksport PDF przez Pandoc

```sh
mkdir -p output/pdf
pandoc RAPORT.md --from=markdown --pdf-engine=xelatex \
  --resource-path=. --filter=./PdfLinks.py \
  --include-in-header=assets/pdf-header.tex \
  -V lang=pl-PL -V papersize=a4 -V fontsize=10pt \
  -V geometry:margin=18mm -V mainfont=texgyrepagella-regular.otf \
  -V mainfontoptions='BoldFont=texgyrepagella-bold.otf,ItalicFont=texgyrepagella-italic.otf,BoldItalicFont=texgyrepagella-bolditalic.otf' \
  -V sansfont=texgyreheros-regular.otf -V monofont=lmmono10-regular.otf \
  -o output/pdf/RAPORT.pdf
```

`PdfLinks.py` jest filtrem JSON Pandoca napisanym w Pythonie, bez dodatkowych bibliotek. Klasa `PdfLinks` i jej metoda `init` odczytują dokument ze standardowego wejścia i zwracają przekształcony dokument na standardowe wyjście. Filtr zachowuje tekst odnośników i dostosowuje ich lokalne cele do położenia PDF; umożliwia też łamanie długich nazw i skład wykładnika matematycznego. Nagłówek TeX ustawia łamanie kodu i mniejszy krój tabel. Przenieś PDF wraz z projektem, aby zachować lokalne odnośniki do CSV i dokumentów. Sam PDF zawiera treść raportu i oba wykresy.

Nie zapisuj danych osobowych ani prywatnych ścieżek w raporcie. Przed oddaniem potwierdźcie rzeczywisty podział pracy i umiejętność wyjaśnienia własnej części. Stan odbioru opisuje [ODBIOR.md](ODBIOR.md).
