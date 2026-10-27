# Instrukcja pracy z projektem — Darwin i Windows

Instrukcja dotyczy grupowego projektu licznika słów. Opiera się na [treści zadania](assets/TASK.md), [roadmapie](ROADMAP.md) i [raporcie końcowym](RAPORT.md). Szczegóły pomiarów i formatu CSV opisuje [BENCHMARK.md](BENCHMARK.md).

Wszystkie polecenia wykonuj z katalogu `word-counter`. Bloki **Darwin** są przeznaczone dla macOS, dla powłoki zsh lub bash. Bloki **Windows** wymagają PowerShell 7 i natywnego kompilatora MinGW-w64. Nie są to polecenia dla `cmd.exe` ani WSL.

## 1. Narzędzia i środowisko analizy

**Po co:** sprawdzić dostępność narzędzi oraz zainstalować biblioteki wykresów w osobnym środowisku, bez zmieniania globalnego Pythona.

Wymagane są:

- Python 3.11 lub nowszy; na Windows także launcher `py`;
- kompilator C++17: Apple Clang z Command Line Tools na Darwin, MinGW-w64 z `g++` na Windows;
- do analizy: pakiety z `requirements-analysis.txt` (Matplotlib 3.11.2 i jego zależności);
- do eksportu: Pandoc i XeLaTeX z TeX Live, polskie wsparcie językowe, pakiety `fvextra`, `xurl`, `seqsplit`, `etoolbox`, `float` oraz fonty TeX Gyre Pagella, TeX Gyre Heros i Latin Modern Mono;
- opcjonalnie Poppler (`pdfinfo`, `pdftotext`, `pdftoppm`) do kontroli PDF.

Narzędzia systemowe należy wcześniej zainstalować i udostępnić w `PATH`. Poniższe polecenia instalują tylko zależności Pythona. Nie ma potrzeby aktywowania środowiska wirtualnego — dalsze kroki wskazują jego interpreter bezpośrednio.

**Darwin:**

```sh
python3 --version
c++ --version
pandoc --version
xelatex --version
python3 -m venv .venv-analysis
.venv-analysis/bin/python -m pip install -r requirements-analysis.txt
```

**Windows (PowerShell 7):**

```powershell
$env:PYTHONUTF8 = "1"
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
py -3 --version
g++ --version
pandoc --version
xelatex --version
py -3 -m venv .venv-analysis
& .\.venv-analysis\Scripts\python.exe -m pip install -r requirements-analysis.txt
```

Ustawienia UTF-8 obowiązują w bieżącej sesji PowerShell. Pozwalają przekazywać polskie znaki między Pythonem, Pandokiem i konsolą. Katalog `.venv-analysis/` zawiera lokalne środowisko; nie jest materiałem do oddania. W poleceniach `py -3` wybiera zainstalowanego Pythona 3 — sprawdź, że ma co najmniej wersję 3.11.

## 2. Kompilacja i uruchomienie licznika

**Po co:** policzyć słowa w tym samym pliku w obu językach i sprawdzić podstawowe uruchomienie. Przykładowe wejście powinno dać **65 słów**. Czas jest zależny od komputera; powinien być nieujemny i podany w `ns`.

**Darwin:**

```sh
mkdir -p out
c++ -std=c++17 -O2 -Wall -Wextra -Wpedantic source/cpp/main.cpp -o out/cpp &&
  ./out/cpp data/1000B_seed14/long_dense_mixed_1000.txt
python3 -B source/python/main.py data/1000B_seed14/long_dense_mixed_1000.txt
```

**Windows (PowerShell 7):**

```powershell
New-Item -ItemType Directory -Force -Path .\out | Out-Null
g++ -std=c++17 -O2 -Wall -Wextra -Wpedantic .\source\cpp\main.cpp -o .\out\cpp.exe
if ($LASTEXITCODE -ne 0) { throw "Kompilacja C++ nie powiodła się." }
& .\out\cpp.exe .\data\1000B_seed14\long_dense_mixed_1000.txt
py -3 -B .\source\python\main.py .\data\1000B_seed14\long_dense_mixed_1000.txt
```

Flaga `-std=c++17` jest wymagana m.in. przez `std::filesystem`; `-O2` włącza optymalizację. Pozostałe flagi włączają ostrzeżenia. Wyniki kompilacji to `out/cpp` lub `out/cpp.exe`. Warunek po kompilacji zapobiega uruchomieniu starego programu, jeśli nowa kompilacja się nie udała.

Przykładowy format wyjścia: `Ilość znalezionych słów: 65; (czas: 1234 ns)`. Separatory to wyłącznie spacja, tabulator i LF; CR oraz interpunkcja pozostają częściami słów.

## 3. Testy automatyczne

**Po co:** sprawdzić odrzucanie błędnych wyników, obsługę awarii i timeoutów oraz poprawność analizy median, duplikatów i brakujących prób. Testy analizy można uruchomić osobno, bez kompilacji C++ i generowania wykresów.

**Darwin:**

```sh
python3 -B -m unittest discover -s tests -v
python3 -B -m unittest discover -s tests -p 'test_analysis.py' -v
```

**Windows (PowerShell 7):**

```powershell
py -3 -B -m unittest discover -s tests -v
py -3 -B -m unittest discover -s tests -p "test_analysis.py" -v
```

Pierwsze polecenie uruchamia cały dostępny zestaw, drugie wyłącznie analizę — nie trzeba wykonywać obu, jeśli wystarcza pełny zestaw. Wynik jest wypisywany w konsoli; `OK` i kod `0` oznaczają powodzenie. Testy korzystają z katalogów tymczasowych.

**Ograniczenie Windows:** testy integracyjne automatu wskazują kompilator `c++` i używają nazwy programu bez `.exe`. Samo zainstalowanie `g++` nie gwarantuje ich powodzenia. Pełny zestaw na Windows należy traktować jako kontrolę diagnostyczną; nie deklarujemy jego pełnej zgodności natywnej. Osobny zestaw `test_analysis.py` nie wymaga kompilatora.

Osiem przypadków kontrolnych oraz ręcznie ustalone liczby słów zapisano w `WordGenerator.FIXTURES`, m.in. pusty tekst → 0, `Ala  ma` → 2, `Ala\tma\nkota` → 3, `kot,pies` → 1 i `Ala\rma` → 1. Przypadki te są odrębne od testów infrastruktury w `tests/`; raport opisuje ich sprawdzenie na obu programach.

## 4. Generowanie danych — znane ograniczenie

**Po co:** udokumentować odtworzenie parametrów danych: 1000 B z ziarnem 14, 100000 B z ziarnem 42 i 1000000 B z ziarnem 2026. Zapis zawsze kierujemy do nowego, osobnego katalogu.

**Obecny generator nie kończy się sukcesem:** zapisuje teksty, ale zgłasza `KeyError: 'source'` przed utworzeniem manifestu, ponieważ w `assets/english_words.json` brakuje metadanych `source`. Poniższe polecenia pokazują interfejs i parametry; wymagają naprawy generatora, zanim będzie można uznać je za pełną procedurę odtworzenia. Do pracy z zachowanym eksperymentem używaj istniejącego `data/` i jego manifestów.

**Darwin:**

```sh
generated_dir="regenerated/$(uuidgen)"
mkdir -p "$generated_dir"
python3 -B WordGenerator.py --output-dir "$generated_dir/1000B_seed14" --sizes 1000 --seed 14
python3 -B WordGenerator.py --output-dir "$generated_dir/100000B_seed42" --sizes 100000 --seed 42
python3 -B WordGenerator.py --output-dir "$generated_dir/1000000B_seed2026" --sizes 1000000 --seed 2026
```

**Windows (PowerShell 7):**

```powershell
$generatedDir = Join-Path "regenerated" ([guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $generatedDir | Out-Null
py -3 -B .\WordGenerator.py --output-dir "$generatedDir/1000B_seed14" --sizes 1000 --seed 14
py -3 -B .\WordGenerator.py --output-dir "$generatedDir/100000B_seed42" --sizes 100000 --seed 42
py -3 -B .\WordGenerator.py --output-dir "$generatedDir/1000000B_seed2026" --sizes 1000000 --seed 2026
```

Po naprawie generatora wynikiem powinny być teksty oraz `manifest.json` z konfiguracją, oczekiwaniami i SHA-256. Generator tworzy siedem wariantów dla każdego rozmiaru oraz przypadki kontrolne; historyczny benchmark używał pięciu wariantów na rozmiar. Nie kieruj tych poleceń do `data/` i nie zakładaj, że nowy zestaw wszystkich wariantów odpowiada dokładnie historycznemu eksperymentowi.

## 5. Mały i pełny benchmark

**Po co:** najpierw sprawdzić automat na małym zestawie, następnie zebrać wielokrotne pomiary obu języków. Automat sam kompiluje C++, sprawdza manifesty, rozmiary, ASCII i SHA-256, a wynik każdej próby porównuje z oczekiwaniem poza pomiarem.

**Darwin:**

```sh
python3 -B Benchmark.py --repetitions 2 --data-dir data/1000B_seed14
python3 -B Benchmark.py
```

**Windows (PowerShell 7) — wywołania wymagające weryfikacji ograniczenia opisanego poniżej:**

```powershell
py -3 -B .\Benchmark.py --compiler g++ --repetitions 2 --data-dir .\data\1000B_seed14
py -3 -B .\Benchmark.py --compiler g++
```

**Ograniczenie Windows:** automat oczekuje pliku `word-counter`, a natywne narzędzia Windows mogą utworzyć `word-counter.exe`. Kontrola istnienia pliku może wtedy zatrzymać przebieg mimo udanej kompilacji. Powyższe polecenia są prawidłowymi wywołaniami CLI, ale nie są potwierdzoną procedurą wykonania natywnego benchmarku na Windows. Nie poprawiamy tego zachowania w ramach instrukcji. Zestaw narzędzi musi także obsługiwać flagi GCC/Clang; `cl.exe` nie jest zamiennikiem argumentu `--compiler g++`.

Mały przebieg obejmuje 5 plików × 2 języki × 2 próby = **20 pomiarów**. Pełny obejmuje 15 plików × 2 języki × 30 prób = **900 pomiarów**, bez rozgrzewek. Programy działają sekwencyjnie: w próbach nieparzystych C++ przed Pythonem, w parzystych odwrotnie.

Czas algorytmu pochodzi z programów i jest zapisywany w nanosekundach. Nie obejmuje uruchomienia procesu, wczytywania, drukowania ani walidacji. Każdy przebieg tworzy osobny katalog `results/<czas-UTC>_<unikalny-sufiks>/` z `measurements.csv`, `metadata.json`, `summary.json`, logiem kompilacji oraz programem użytym w pomiarze. W razie odrzuceń pojawia się `errors.jsonl`. Nie ma potrzeby ręcznie czyścić wcześniejszych wyników.

Kod `0` oznacza kompletny przebieg bez odrzuceń; `1` — niepowodzenie lub odrzucenia, a `130` — przerwanie przez Ctrl+C. Odrzucone próby pozostają zapisane i nie są dopuszczane do statystyk. Nowe czasy nie muszą być identyczne z raportem i dotyczą bieżącego kodu.

## 6. Odtworzenie statystyk i wykresów

**Po co:** ponownie obliczyć wyniki konkretnego, zachowanego eksperymentu, bez uruchamiania nowego benchmarku. Korzystamy z przebiegu analizowanego w raporcie: `20261026T184512Z_7d95f26993`.

**Darwin:**

```sh
.venv-analysis/bin/python -B Analyze.py \
  --run-dir results/20261026T184512Z_7d95f26993 \
  --output-dir analysis-reproduced
```

**Windows (PowerShell 7):**

```powershell
& .\.venv-analysis\Scripts\python.exe -B .\Analyze.py `
  --run-dir .\results\20261026T184512Z_7d95f26993 `
  --output-dir .\analysis-reproduced
```

W `analysis-reproduced/` powstają `statistics.csv`, `completeness.csv`, `issues.csv`, `provenance.json` i dwa wykresy PNG w `images/`. Ponowne użycie tej samej ścieżki zastępuje pliki odtworzonej analizy — wybierz inną nazwę, jeśli chcesz je zachować. Nie nadpisuj dołączonego `analysis/` ani żadnego katalogu `results/`.

Kod `0` oznacza brak odstępstw kontroli CSV i podsumowania, `1` — wykryte odstępstwa, `2` — błąd wejścia, zależności lub zapisu. Kod `0` nie potwierdza identyczności aktualnych źródeł z historycznym kodem: ten aspekt opisuje osobno `provenance.json`. Zachowana kontrola w `analysis/` jest migawką sprzed późniejszego formatowania źródeł.

## 7. Eksport raportu przez Pandoc

**Po co:** otrzymać PDF zgodny z `RAPORT.md`, z polskimi znakami, tabelami i osadzonymi wykresami. Przed eksportem muszą istnieć oba PNG w `analysis/images/` i narzędzia wymienione w punkcie 1.

**Darwin:**

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

**Windows (PowerShell 7):**

```powershell
New-Item -ItemType Directory -Force -Path .\output\pdf | Out-Null
$pdfArgs = @(
  "--from=json", "--pdf-engine=xelatex", "--resource-path=.",
  "--include-in-header=assets/pdf-header.tex",
  "-V", "lang=pl-PL", "-V", "papersize=a4", "-V", "fontsize=10pt",
  "-V", "geometry:margin=18mm", "-V", "mainfont=texgyrepagella-regular.otf",
  "-V", "mainfontoptions=BoldFont=texgyrepagella-bold.otf,ItalicFont=texgyrepagella-italic.otf,BoldItalicFont=texgyrepagella-bolditalic.otf",
  "-V", "sansfont=texgyreheros-regular.otf", "-V", "monofont=lmmono10-regular.otf",
  "-o", "output/pdf/RAPORT.pdf"
)
pandoc .\RAPORT.md --from=markdown --to=json |
  py -3 -B .\PdfLinks.py |
  pandoc @pdfArgs
if ($LASTEXITCODE -ne 0) { throw "Eksport PDF nie powiódł się." }
```

Wariant Windows jawnie przekazuje dokument JSON przez klasę `PdfLinks`, więc nie wymaga obsługi shebanga ani skojarzenia plików `.py`. Wariant Darwin korzysta z tego samego filtra przez opcję `--filter`. Nagłówek TeX ustawia m.in. łamanie kodu i wygląd tabel.

Wynik to `output/pdf/RAPORT.pdf`; ponowny eksport zastępuje ten plik. Aby zachować starszą wersję, zmień argument `-o` na inną nazwę **w tym samym katalogu**. Filtr ustawia względne linki dla położenia `output/pdf/`, dlatego nie przenoś samego PDF w inne miejsce, jeśli chcesz korzystać z odnośników do plików projektu.

## 8. Podgląd i kontrola materiałów

**Po co:** sprawdzić każdą stronę, a nie tylko poprawny kod zakończenia eksportu. Skontroluj polskie znaki, tabele, wartości, wykresy, podpisy, kod, linki, numerację i brak uciętej treści. Porównaj liczby z CSV oraz treść z Markdownem.

**Darwin — otwarcie PDF:**

```sh
open output/pdf/RAPORT.pdf
```

**Windows (PowerShell 7) — otwarcie PDF:**

```powershell
Start-Process .\output\pdf\RAPORT.pdf
```

**Opcjonalna kontrola Popplerem na Darwin:**

```sh
mkdir -p output/pdf/review
pdfinfo output/pdf/RAPORT.pdf
pdftotext -layout output/pdf/RAPORT.pdf output/pdf/review/RAPORT.txt
pdftoppm -r 120 -png output/pdf/RAPORT.pdf output/pdf/review/page
```

**Opcjonalna kontrola Popplerem na Windows (PowerShell 7):**

```powershell
New-Item -ItemType Directory -Force -Path .\output\pdf\review | Out-Null
pdfinfo .\output\pdf\RAPORT.pdf
pdftotext -layout .\output\pdf\RAPORT.pdf .\output\pdf\review\RAPORT.txt
pdftoppm -r 120 -png .\output\pdf\RAPORT.pdf .\output\pdf\review\page
```
