# Automatyczny benchmark licznika słów

Wymagania: Python 3.10 lub nowszy i kompilator C++17. Automat korzysta wyłącznie z biblioteki standardowej Pythona. Polecenia poniżej wykonuje się z katalogu projektu, bez debuggera.

```sh
python3 -B -m unittest discover -s tests -v
python3 -B Benchmark.py --repetitions 2 --data-dir data/1000B_seed14
python3 -B Benchmark.py
```

Ostatnie polecenie wykonuje pełny przebieg: 15 plików × 2 języki × 30 prób = 900 pomiarów, bez rozgrzewek. Domyślne dane i katalog wynikowy są określane względem położenia skryptu, więc automat można uruchomić również z innego katalogu. Jawnie podane ścieżki względne odnoszą się do bieżącego katalogu użytkownika.

Opcje: `--repetitions N` (dodatnia liczba, domyślnie 30), `--data-dir PATH`, `--output-dir PATH` i `--compiler PROGRAM` (domyślnie `c++`, bez dodatkowych flag).

## Przygotowanie i kolejność

Przed kompilacją automat sprawdza manifesty, rozmiary, kodowanie ASCII i SHA-256. Oczekiwania pobiera z manifestów. Identyfikator danych to ścieżka względna wobec wybranego katalogu danych; wybór podkatalogu dla małego przebiegu daje odpowiednio krótsze identyfikatory.

Każdy przebieg otrzymuje nowy katalog `results/<czas-UTC>_<unikalny-sufiks>/`. Powstaje w nim świeży plik wykonywalny, kompilowany z flagami:

```text
-std=c++17 -O2 -Wall -Wextra -Wpedantic
```

Dokładne polecenie, wersja kompilatora i sumy kontrolne źródeł są w metadanych. Błąd kompilacji zatrzymuje przebieg; automat nie korzysta z `out/cpp` ani z wcześniejszego pliku wykonywalnego.

Pliki są uporządkowane według rozmiaru i identyfikatora. Dla każdego pliku próby nieparzyste mają kolejność C++ → Python, a parzyste Python → C++. Wszystkie procesy wykonują się sekwencyjnie. Każda próba to nowy proces i pojedyncze wywołanie algorytmu po wczytaniu danych. Limit uruchomienia to 30 sekund.

## Pomiar i zegary

Programy same mierzą wyłącznie algorytm i uzyskanie liczby słów. Start procesu, odczyt pliku, dekodowanie ASCII, tworzenie struktury wyniku pomiaru, drukowanie i walidacja nie wchodzą do mierzonego czasu. Odczyt binarny zachowuje różnicę między CR i LF.

C++ korzysta z monotonicznego `std::chrono::steady_clock`; tryb `--clock-info` zwraca JSON z nazwą, monotonicznością i okresem zegara jako ułamkiem sekund (`period_num / period_den`). Jest to okres nominalny typu zegara, a nie gwarancja rzeczywistej rozdzielczości ani dokładności.

Python używa `time.perf_counter_ns()`. `time.get_clock_info("perf_counter")` dostarcza nazwę implementacji, monotoniczność i deklarowaną rozdzielczość `resolution` w sekundach. Oba programy zapisują czas jako całkowitą liczbę nanosekund (`ns`); jednostka zapisu nie oznacza dokładności jednej nanosekundy. Informacje dla konkretnego przebiegu znajdują się w `metadata.json`.

Procesy nie współdzielą rozgrzanego interpretera. Brak rozgrzewek nie oznacza zimnego cache systemu: sprawdzanie danych i poprzednie próby mogą go rozgrzać. Krótkie pomiary są wrażliwe na koszt zegara, planistę systemu, obciążenie i stan CPU. Czasy równe zero i wartości skrajne pozostają zapisane.

## Pliki wynikowe i walidacja

- `measurements.csv` — jeden wiersz na wykonaną próbę, zapisywany i opróżniany z bufora na bieżąco.
- `metadata.json` — konfiguracja, kolejność danych, oczekiwania, SHA-256, wersje narzędzi, CPU, system, architektura, zegary i polecenie kompilacji.
- `summary.json` — liczby planowanych, wykonanych, poprawnych i odrzuconych prób dla każdej pary język–plik oraz status przebiegu.
- `compilation.log` — stdout i stderr kompilatora; pusty plik oznacza brak komunikatów.
- `errors.jsonl` — diagnostyka odrzuconych prób, tworzona tylko wtedy, gdy wystąpią.
- `word-counter` — plik wykonywalny użyty w danym przebiegu.

CSV jest zapisany w UTF-8, ma nagłówek i separator przecinkowy. Pola:

- `language`, `data_id`, `sha256`, `size_bytes`, `variant` — język i identyfikacja wejścia.
- `trial`, `position` — numer próby od 1 i pozycja języka w parze (1 lub 2).
- `elapsed`, `unit` — surowy czas i jednostka `ns`; brak odczytanego czasu oznacza puste pole, nie zero.
- `expected_words`, `actual_words` — wynik oczekiwany i otrzymany; brak odczytanego wyniku oznacza puste pole.
- `status`, `reason` — status i opis odrzucenia.

Statusy prób: `valid`, `wrong_result`, `invalid_output`, `runtime_error`, `timeout`. Parser wymaga dokładnego formatu dotychczasowego wyjścia programów, nieujemnych liczb całkowitych i pustego stderr przy sukcesie. Porównanie z oczekiwaniem następuje poza pomiarem. Błędna liczba słów zachowuje czas; odrzucone próby nie wchodzą do liczby poprawnych prób ani do późniejszych statystyk. Nie ma automatycznego ponawiania błędnej próby.

Kod zakończenia automatu wynosi `0` wyłącznie dla kompletnego przebiegu, w którym wszystkie próby są poprawne. Pozostałe błędy dają `1`, a Ctrl+C — `130`. Dotychczasowe wyniki pozostają w katalogu przebiegu. Statusy to `complete`, `completed_with_rejections`, `failed` i `interrupted`; tylko `complete` jest poprawnym, kompletnym przebiegiem. Przy błędzie przygotowania część plików wynikowych może jeszcze nie istnieć.

## Testy

Testy `unittest` sprawdzają ścisły parser, zachowanie czasu zerowego, celowo błędną liczbę słów, odrzucenie niepoprawnego wyjścia, błąd uruchomienia i timeout. Sprawdzają również brak użycia starego programu po błędzie kompilacji oraz zachowanie podsumowania po przerwaniu.

Test integracyjny tworzy wejście `Ala\rma`, ale celowo zapisuje oczekiwanie `2` zamiast `1`. Uruchamia oba rzeczywiste programy: wszystkie cztery próby trafiają do CSV jako `wrong_result`, podsumowanie ma zero poprawnych prób, a automat zwraca kod `1`. Tymczasowe dane testowe nie zmieniają manifestów projektu.

Analiza jest dostępna w [RAPORT.md](RAPORT.md). Skrypt `Analyze.py` sprawdza plan i kompletność względem metadanych oraz `summary.json`, a do statystyk dopuszcza poprawne, jednoznaczne próby bez usuwania zer ani obserwacji skrajnych. Instrukcja instalacji zależności i uruchomienia znajduje się w raporcie.

## Zweryfikowane przebiegi

Mały przebieg (5 plików, 2 języki, 2 próby) zakończył się wynikiem 20/20 w `results/20261026T184237Z_ec1201df18/`.

Pełny przebieg: [surowe pomiary](results/20261026T184323Z_8894299b2b/measurements.csv), [metadane](results/20261026T184323Z_8894299b2b/metadata.json) i [podsumowanie](results/20261026T184323Z_8894299b2b/summary.json). Uzyskano 900/900 poprawnych prób bez odrzuceń. Pierwotna dokumentacja odnotowała weryfikację prób, kolejności i zgodności źródeł. Obecna kontrola wykazuje jednak, że C++ i `Benchmark.py` mają inne SHA-256 niż w historycznych metadanych; nie należy utożsamiać historycznych pomiarów z aktualnym kodem. Testy obecnego automatu przechodzą, ale nie potwierdzają zgodności historycznej wersji.

Raport korzysta z nowszego pełnego przebiegu: [CSV](results/20261026T184512Z_7d95f26993/measurements.csv), [metadane](results/20261026T184512Z_7d95f26993/metadata.json), [podsumowanie](results/20261026T184512Z_7d95f26993/summary.json). Ma on 900/900 poprawnych prób, dokładny model CPU Apple M4 Pro i brak odrzuceń. Nie łączono go z wcześniejszymi seriami. Obecny Python jest zgodny z historycznym SHA-256; niezgodność C++ i automatu opisuje [kontrola pochodzenia](analysis/provenance.json). Łącznie przechodzi 18 testów automatu i analizy.

Opis zgodności źródeł i sumy `current_sha256` są migawką kontroli sprzed późniejszego commitu formatującego. Formatowanie nie aktualizuje historycznych wyników ani zachowanego pliku kontroli pochodzenia.
