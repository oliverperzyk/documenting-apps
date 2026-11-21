# Licznik słów

Regulus i Mars porównują czas wykonania tego samego algorytmu liczenia słów w Pythonie i C++. Programy czytają plik ASCII. Słowa oddzielają wyłącznie spacja, tabulator i znak nowej linii LF. `kot,pies` to jedno słowo, a pusty plik daje wynik `0`.

> [!IMPORTANT]
> Pomiary w raporcie wykonano na macOS na komputerze z Apple M4 Pro (14 cores). Czasy mogą się różnić zależnie od sprzętu, systemu i wersji narzędzi. Liczba słów dla tych samych danych powinna się zgadzać.

## 1. Przygotuj środowisko

| System                      | Powłoka      | Python                                | Kompilator C++17                                |
| --------------------------- | ------------ | ------------------------------------- | ----------------------------------------------- |
| Linux, np. Ubuntu 24.04 LTS | Bash         | 3.10+ do benchmarku, 3.11+ do analizy | GCC (`c++`, pakiet `build-essential` na Ubuntu) |
| macOS                       | Zsh lub Bash | 3.10+ do benchmarku, 3.11+ do analizy | Apple Clang (`c++`, Command Line Tools)         |
| Windows 11 x64              | PowerShell 7 | 3.11+ z poleceniem `py`               | MinGW-w64 (`g++`, np. MSYS2 UCRT64)             |

Na Ubuntu 24.04 domyślny Python 3.12 wystarcza do analizy. Zainstaluj Git, kompilator i obsługę środowisk wirtualnych. [Informacje o Ubuntu 24.04](https://documentation.ubuntu.com/release-notes/24.04/)

```bash
sudo apt update
sudo apt install git build-essential python3 python3-venv
```

Na macOS, jeśli brakuje `c++`, uruchom `xcode-select --install`. Zainstaluj Pythona, jeśli `python3 --version` pokazuje wersję starszą od wymaganej. [Instalatory Pythona](https://www.python.org/downloads/)

Na Windows zainstaluj Git, PowerShell 7 i Pythona z poleceniem `py`. W terminalu MSYS2 UCRT64 zainstaluj kompilator poleceniem `pacman -S mingw-w64-ucrt-x86_64-gcc`. W PowerShell dodaj katalog `ucrt64\bin` z instalacji MSYS2 do `PATH` bieżącej sesji. Poniższy przykład używa domyślnego katalogu instalacji. [Środowiska MSYS2](https://www.msys2.org/docs/environments/) · [Pakiet GCC](https://packages.msys2.org/packages/mingw-w64-ucrt-x86_64-gcc)

```powershell
$env:Path = "C:\msys64\ucrt64\bin;$env:Path"
$env:PYTHONUTF8 = "1"
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
py -3 --version
g++ --version
```

Pobierz repozytorium i przejdź do katalogu projektu. Jeśli masz już lokalną kopię, otwórz w niej `tasks/group/word-counter`. Wszystkie dalsze polecenia wykonuj z tego katalogu.

```sh
git clone https://github.com/oliverperzyk/documenting-apps.git
cd documenting-apps/tasks/group/word-counter
```

## 2. Uruchom oba liczniki

Na **macOS i Linuxie** sprawdź wersje, skompiluj C++ i uruchom oba programy na tym samym pliku.

```sh
python3 --version
c++ --version
mkdir -p out
c++ -std=c++17 -O2 -Wall -Wextra -Wpedantic source/cpp/main.cpp -o out/word-counter &&
  ./out/word-counter data/1000B_seed14/long_dense_mixed_1000.txt
python3 -B source/python/main.py data/1000B_seed14/long_dense_mixed_1000.txt
```

Na **Windows** wykonaj te kroki w PowerShell.

```powershell
New-Item -ItemType Directory -Force out | Out-Null
g++ -std=c++17 -O2 -Wall -Wextra -Wpedantic .\source\cpp\main.cpp -o .\out\word-counter.exe
if ($LASTEXITCODE -ne 0) { throw "Kompilacja C++ nie powiodła się." }
& .\out\word-counter.exe .\data\1000B_seed14\long_dense_mixed_1000.txt
py -3 -B .\source\python\main.py .\data\1000B_seed14\long_dense_mixed_1000.txt
```

Oba programy powinny zwrócić **65 słów** oraz nieujemny czas w `ns`. Oczekiwaną liczbę słów znajdziesz w [manifeście zestawu 1000 B](data/1000B_seed14/manifest.json).

## 3. Wykonaj benchmark

Na **macOS i Linuxie** uruchom testy i krótki benchmark. Skrypt sam kompiluje C++ i sprawdza rozmiary danych, kodowanie ASCII i sumy SHA-256 według manifestów. Do uruchomienia licznika, testów i benchmarku wystarcza standardowa biblioteka Pythona.

```sh
python3 -B -m unittest discover -s tests -v
python3 -B Benchmark.py --repetitions 2 --data-dir data/1000B_seed14
```

Oczekuj `OK` po 18 testach i statusu `complete` z **20/20 poprawnych prób** po benchmarku. Następnie uruchom pełny pomiar.

```sh
python3 -B Benchmark.py
```

Pełny przebieg obejmuje **900 prób** (15 plików o rozmiarach 1000, 100000 i 1000000 B × 2 języki × 30 powtórzeń). Mierzony czas obejmuje liczenie słów i uzyskanie wyniku. Odczyt pliku, start procesu, wypisywanie i sprawdzanie wyniku odbywają się poza pomiarem.

Na **Windows** pomiar pojedynczego pliku uzyskasz z wyjścia obu liczników. Pełny natywny benchmark ma ograniczenie. Skrypt szuka programu `word-counter`, a MinGW-w64 może zapisać `word-counter.exe`, co zatrzymuje przebieg na kontroli pliku po kompilacji. W PowerShell możesz uruchomić testy analizy poleceniem `py -3 -B -m unittest discover -s tests -p test_analysis.py -v` i sprawdzić zapisane wyniki według następnej sekcji. [Ograniczenia natywnego Windows](CONTRIBUTING.md)

Do pomiarów użyj dołączonego `data/`. W bieżącej wersji `WordGenerator.py` kończy się błędem `KeyError: 'source'` przed zapisaniem manifestu. [Opis danych i generatora](CONTRIBUTING.md#4-generowanie-danych--znane-ograniczenie)

## 4. Sprawdź pomiary i odtwórz analizę

Benchmark wypisuje ścieżkę do nowego podkatalogu `results/`. W `summary.json` sprawdź, czy `status` to `complete`, pola `planned`, `executed` i `valid` mają wartość 20 lub 900 zgodnie z zakresem, a `rejected` wynosi `0`. W `measurements.csv` każda poprawna próba ma `status=valid`, zgodne `actual_words` i `expected_words` oraz `unit=ns`. Jeśli przebieg się nie powiedzie, zajrzyj do `compilation.log` lub do `errors.jsonl`, jeśli powstał. [Format plików i kody zakończenia](BENCHMARK.md)

Do statystyk i wykresów zainstaluj Matplotlib 3.11.2 z pliku zależności. Na **macOS i Linuxie** utwórz środowisko wirtualne.

```sh
python3 -m venv .venv-analysis
.venv-analysis/bin/python -m pip install -r requirements-analysis.txt
```

Aby przeanalizować własny pełny pomiar, zastąp `IDENTYFIKATOR` nazwą katalogu wypisaną przez `Benchmark.py`.

```sh
.venv-analysis/bin/python -B Analyze.py --run-dir 'results/IDENTYFIKATOR' --output-dir analysis-local
```

Aby odtworzyć analizę przebiegu z raportu na **macOS lub Linuxie**, wskaż zapisany katalog.

```sh
.venv-analysis/bin/python -B Analyze.py --run-dir results/20261026T184512Z_7d95f26993 --output-dir analysis-reproduced
```

Na **Windows** ten sam przebieg przeanalizujesz w PowerShell.

```powershell
py -3 -m venv .venv-analysis
& .\.venv-analysis\Scripts\python.exe -m pip install -r requirements-analysis.txt
$env:MPLCONFIGDIR = Join-Path $env:TEMP "word-counter-matplotlib"
& .\.venv-analysis\Scripts\python.exe -B .\Analyze.py --run-dir .\results\20261026T184512Z_7d95f26993 --output-dir .\analysis-reproduced
```

Po analizie pełnego przebiegu oczekuj **30 grup** i **0 odstępstw**. Sprawdź pliki w wybranym katalogu wyjściowym.

- `completeness.csv` pokazuje kompletność prób dla każdej pary język–plik. W pełnym przebiegu każda para powinna mieć 30 poprawnych prób. `issues.csv` powinien zawierać sam nagłówek.
- `statistics.csv` zawiera liczbę poprawnych prób, medianę, minimum, maksimum i rozstęp (`maksimum − minimum`) w nanosekundach. Przy odtwarzaniu raportu porównaj wartości z [zapisanymi statystykami](analysis/statistics.csv). Wykresy w `images/` pokazują czasy w mikrosekundach.
- `provenance.json` porównuje sumy SHA-256 źródeł i danych z metadanymi przebiegu. Dla historycznego przebiegu dane są zgodne, a bieżące sumy `source/cpp/main.cpp`, `source/python/main.py` i `Benchmark.py` różnią się od zapisanych. Odtworzone statystyki dotyczą tamtego przebiegu. Pomiary bieżącego kodu uzyskasz przez nowy benchmark.

## Dokumentacja

- [Raport z eksperymentu](RAPORT.md)
- [Metodyka benchmarku](BENCHMARK.md)
- [Eksport raportu do PDF](CONTRIBUTING.md#7-eksport-raportu-przez-pandoc)
