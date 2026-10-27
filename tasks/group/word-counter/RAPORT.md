# Licznik słów ASCII — porównanie czasu wykonania w C++ i Pythonie

**Projekt grupowy 14 · Zespół: Regulus i Mars "Czerwony Lew"**

## 1. Cel badania i hipoteza

Celem projektu było zaimplementowanie tego samego algorytmu liczenia słów w C++ i Pythonie oraz porównanie czasu jego wykonania dla tekstów ASCII o różnej długości i budowie. Badaliśmy wpływ liczby bajtów, długości słów i udziału separatorów na medianę oraz rozrzut czasu.

Postawiliśmy pytanie: **jak długość i budowa tekstu wiążą się z czasem działania obu implementacji?** Przyjęliśmy hipotezę, że dla ustalonego wariantu danych czas będzie rósł w przybliżeniu proporcjonalnie do liczby znaków, ponieważ algorytm przegląda każdy znak jeden raz. Nie przyjmowaliśmy przewagi żadnego języka jako założenia analizy. Hipotezę sformułowaliśmy podczas opracowania wyników, po wykonaniu pomiarów; nie była zarejestrowana przed eksperymentem.

Raport obejmuje jeden pełny przebieg: `20261026T184512Z_7d95f26993`, wykonany 26 października 2026 r., 18:45:12–18:45:28 UTC (19:45:12–19:45:28 czasu polskiego). Podstawą obliczeń jest [surowy CSV](results/20261026T184512Z_7d95f26993/measurements.csv), a opis warunków pochodzi z [metadanych](results/20261026T184512Z_7d95f26993/metadata.json). Nie łączyliśmy pomiarów z różnych przebiegów i nie wykonywaliśmy nowych pomiarów na potrzeby tego raportu.

## 2. Definicja słowa i algorytm

W zadaniu słowo oznacza niepusty ciąg znaków rozdzielany wyłącznie spacją (`0x20`), tabulatorem (`0x09`) lub LF (`0x0A`). Interpunkcja i CR (`0x0D`) należą do słowa. Dlatego `kot,pies` oraz `Ala\rma` zawierają po jednym słowie, a pusty tekst nie zawiera żadnego.

Obie implementacje wykorzystują licznik oraz zmienną logiczną `inWord`:

1. Przed pętlą ustawiamy licznik na `0`, a `inWord` na fałsz.
2. Separator ustawia `inWord` na fałsz, bez zwiększania licznika.
3. Znak niebędący separatorem rozpoczyna nowe słowo tylko wtedy, gdy `inWord` było fałszywe. Wówczas zwiększamy licznik i ustawiamy stan na prawdziwy.
4. Pozostałe znaki tego samego słowa nie zmieniają licznika. Po pętli zwracamy wynik bez dodatkowego doliczania ostatniego słowa.

Nie korzystamy z `split`, gotowego licznika słów ani ogólnego rozpoznawania białych znaków. Algorytm ma złożoność czasową O(n) i dodatkową pamięć O(1). Osobno wczytany tekst zajmuje O(n) pamięci.

Kod znajduje się w [wersji C++](source/cpp/main.cpp) i [wersji Python](source/python/main.py). W klasie `Solution` funkcja licząca jest oddzielona od odczytu pliku, pomiaru i wypisywania wyników. Pliki są odczytywane binarnie, a Python dekoduje ASCII przed pomiarem, dzięki czemu CR nie jest zamieniany na LF.

## 3. Dane i kontrola poprawności

### Przygotowanie danych

Wykorzystaliśmy 15 plików: po pięć dla 1000, 100000 i 1000000 bajtów. Dla ASCII jeden bajt odpowiada jednemu znakowi. Ziarna generatora dla tych rozmiarów wynoszą odpowiednio 14, 42 i 2026. Manifesty zawierają parametry danych, oczekiwane liczby słów i sumy SHA-256. Sprawdziliśmy zgodność wszystkich 15 zachowanych plików z metadanymi badanego przebiegu.

Dane powstały na podstawie lokalnego słownika 250 angielskich słów: 125 krótkich (1–5 liter) i 125 długich (7–8 liter). Według [metadanych źródła słownika](data/1000B_seed14/manifest.json) wykorzystano zasób `first20hours/google-10000-english`, wybierając słowa ASCII z listy bez wulgaryzmów w kolejności źródłowej. [Kopia słownika](assets/english_words.json) i generator są dołączone do projektu. Oczekiwana liczba słów jest wyznaczana podczas dodawania pełnych słów, niezależnie od porównywanych liczników. Pozostałe bajty są wypełniane separatorami.

Dla każdej długości przygotowano cztery wspólne warianty:

- `short_sparse_mixed` — krótkie słowa i pojedyncze separatory w cyklu spacja/tabulator/LF;
- `short_dense_mixed` — krótkie słowa i grupy ośmiu separatorów;
- `long_sparse_mixed` — długie słowa i pojedyncze separatory;
- `long_dense_mixed` — długie słowa i grupy ośmiu separatorów.

Piąty wariant to `short_spaces` dla 1000 B, `short_tabs` dla 100000 B oraz `short_lf` dla 1000000 B. Jest to niepełna macierz długość–wariant. Tych trzech dodatkowych wariantów nie traktujemy jako jednej serii do badania wpływu długości ani jako izolowanego porównania rodzajów separatorów.

Oczekiwane wyniki dla danych benchmarkowych:

| Długość [B] | Wariant              | Oczekiwane słowa |
| ----------: | -------------------- | ---------------: |
|        1000 | `long_dense_mixed`   |               65 |
|        1000 | `long_sparse_mixed`  |              119 |
|        1000 | `short_dense_mixed`  |               88 |
|        1000 | `short_spaces`       |              219 |
|        1000 | `short_sparse_mixed` |              225 |
|      100000 | `long_dense_mixed`   |             6498 |
|      100000 | `long_sparse_mixed`  |            11904 |
|      100000 | `short_dense_mixed`  |             8747 |
|      100000 | `short_sparse_mixed` |            22452 |
|      100000 | `short_tabs`         |            22511 |
|     1000000 | `long_dense_mixed`   |            64966 |
|     1000000 | `long_sparse_mixed`  |           119166 |
|     1000000 | `short_dense_mixed`  |            87327 |
|     1000000 | `short_lf`           |           224800 |
|     1000000 | `short_sparse_mixed` |           224791 |

### Przypadki kontrolne

Ręcznie ustalone oczekiwania są zapisane w `WordGenerator.FIXTURES`. Przed przygotowaniem wersji końcowej uruchomiliśmy wszystkie osiem przypadków na obu rzeczywistych programach i uzyskaliśmy oczekiwane wyniki.

| Wejście (zapis znaków specjalnych) | Oczekiwana liczba słów |
| ---------------------------------- | ---------------------: |
| Pusty tekst                        |                      0 |
| ` \t\n  \n\t`                      |                      0 |
| `word` bez separatora na końcu     |                      1 |
| `Ala  ma`                          |                      2 |
| `Ala\tma\nkota`                    |                      3 |
| `\t\ncat  dog\n\t`                 |                      2 |
| `kot,pies`                         |                      1 |
| `Ala\rma`                          |                      1 |

Zapis `\t`, `\n` i `\r` w tabeli oznacza odpowiednio tabulator, LF i CR. Testy obejmują pusty tekst, same separatory, wielokrotne i mieszane separatory, separatory na brzegach, interpunkcję i brak separatora na końcu. Nie ograniczamy kontroli do zgodności obu języków: każdy wynik porównujemy z niezależnym oczekiwaniem.

Uruchomiliśmy również wszystkie 18 dostępnych testów automatycznych: 11 testów automatu benchmarkowego i 7 testów analizy. Sprawdzają one m.in. błędne wyniki, niepoprawne wyjście, timeout, błąd kompilacji, brakujące i powielone próby, mediany parzyste i nieparzyste oraz zachowanie zer i wartości skrajnych. Wszystkie testy zakończyły się powodzeniem.

## 4. Środowisko i metoda pomiaru

### Warunki eksperymentu

Parametry zapisane dla analizowanego przebiegu:

- **CPU:** Apple M4 Pro, arm64, 14 logicznych CPU.
- **System:** `macOS-27.0.1-arm64-arm-64bit-Mach-O`.
- **Python:** 3.14.4, kompilacja `main, Apr 7 2026, 13:13:20`, Clang 21.0.0 (`clang-2100.0.123.102`).
- **Kompilator C++:** Apple clang 21.0.0 (`clang-2100.3.34.2`), target `arm64-apple-darwin27.0.0`.
- **Flagi:** `-std=c++17 -O2 -Wall -Wextra -Wpedantic`; uruchomienie bez debuggera.

Nie zapisano ilości RAM, temperatury, zasilania ani obciążenia komputera podczas pomiarów. Nie wykorzystujemy tych nieznanych parametrów do wyjaśniania wyników.

### Zakres i kolejność pomiarów

Dla każdej pary język–plik wykonano 30 prób, bez rozgrzewek: **15 × 2 × 30 = 900 pomiarów**. Każda próba uruchamia osobny proces i wykonuje pojedyncze liczenie. Programy działają sekwencyjnie: w próbach nieparzystych C++ przed Pythonem, w parzystych odwrotnie.

Mierzony odcinek obejmuje wyłącznie algorytm i uzyskanie liczby słów. Nie obejmuje startu procesu, odczytu, dekodowania ASCII, drukowania, walidacji ani tworzenia struktury przechowującej czas i wynik. Dane są wczytywane przed uruchomieniem zegara, a sprawdzenie liczby słów następuje po pomiarze.

C++ używa monotonicznego `std::chrono::steady_clock` z nominalnym okresem 1/1000000000 s. Python używa `time.perf_counter_ns()`; zapisana implementacja to `mach_absolute_time()`, a deklarowana rozdzielczość wynosi około 41,67 ns. Oba programy zapisują całkowite nanosekundy. Jednostka zapisu nie oznacza dokładności 1 ns, a nominalny okres zegara C++ nie jest pomiarem jego rzeczywistej rozdzielczości.

Automat sprawdza wejścia względem manifestów, kompiluje świeży program i nie uruchamia starej wersji po błędzie kompilacji. Poza pomiarem porównuje każdą otrzymaną liczbę słów z oczekiwaniem. Błędne próby pozostają w CSV ze statusem i przyczyną, lecz nie wchodzą do statystyk. Limit procesu wynosi 30 s.

### Kompletność i obliczenia

Kontrola [kompletności](analysis/completeness.csv) i [podsumowania przebiegu](results/20261026T184512Z_7d95f26993/summary.json) potwierdza 900 wierszy, 30 grup język–plik i po 30 unikalnych prób w każdej grupie. Wszystkie próby mają status `valid`, a liczby słów odpowiadają oczekiwaniom. Nie ma braków, duplikatów, odrzuceń ani zerowych czasów. [Rejestr odstępstw](analysis/issues.csv) zawiera tylko nagłówek.

Dla każdej grupy obliczamy medianę, minimum, maksimum i rozstęp. Przy 30 próbach mediana jest średnią pozycji 15 i 16 po sortowaniu; rozstęp to różnica maksimum i minimum. Zachowujemy wszystkie poprawne pomiary, również skrajne. Wartości zerowe także pozostałyby w zbiorze, gdyby wystąpiły. Nie odejmujemy kosztu odczytu zegara. Brak danych nie jest traktowany jako zero.

## 5. Wyniki

Poniższe tabele obejmują wszystkie 30 grup, po 30 poprawnych prób każda. Czasy podano w nanosekundach, bez zaokrąglania median połówkowych. Źródłem jest [CSV pomiarów](results/20261026T184512Z_7d95f26993/measurements.csv); pełne zestawienie maszynowe zawiera [statistics.csv](analysis/statistics.csv).

### Tekst 1000 B

| Język  | Wariant            |   n | Mediana [ns] | Minimum [ns] | Maksimum [ns] | Rozstęp [ns] |
| ------ | ------------------ | --: | -----------: | -----------: | ------------: | -----------: |
| C++    | long_dense_mixed   |  30 |        500.0 |          458 |           708 |          250 |
| Python | long_dense_mixed   |  30 |      16854.0 |        16125 |         23542 |         7417 |
| C++    | long_sparse_mixed  |  30 |        500.0 |          458 |           667 |          209 |
| Python | long_sparse_mixed  |  30 |      18604.5 |        17959 |         25250 |         7291 |
| C++    | short_dense_mixed  |  30 |        500.0 |          458 |           584 |          126 |
| Python | short_dense_mixed  |  30 |      15792.0 |        15292 |         22083 |         6791 |
| C++    | short_spaces       |  30 |        541.5 |          458 |           750 |          292 |
| Python | short_spaces       |  30 |      18167.0 |        17500 |         25292 |         7792 |
| C++    | short_sparse_mixed |  30 |        500.0 |          458 |           625 |          167 |
| Python | short_sparse_mixed |  30 |      19083.5 |        18542 |         22584 |         4042 |

### Tekst 100000 B

| Język  | Wariant            |   n | Mediana [ns] | Minimum [ns] | Maksimum [ns] | Rozstęp [ns] |
| ------ | ------------------ | --: | -----------: | -----------: | ------------: | -----------: |
| C++    | long_dense_mixed   |  30 |      48104.0 |        46541 |         98666 |        52125 |
| Python | long_dense_mixed   |  30 |    1664354.0 |      1517625 |       1774958 |       257333 |
| C++    | long_sparse_mixed  |  30 |      48250.0 |        46375 |         68667 |        22292 |
| Python | long_sparse_mixed  |  30 |    1909438.0 |      1797375 |       2038334 |       240959 |
| C++    | short_dense_mixed  |  30 |      48167.0 |        46666 |         60417 |        13751 |
| Python | short_dense_mixed  |  30 |    1573875.0 |      1431292 |       1688291 |       256999 |
| C++    | short_sparse_mixed |  30 |      47750.0 |        46250 |         63000 |        16750 |
| Python | short_sparse_mixed |  30 |    2020042.0 |      1917500 |       2207916 |       290416 |
| C++    | short_tabs         |  30 |      47896.0 |        46584 |         61917 |        15333 |
| Python | short_tabs         |  30 |    2020479.0 |      1841875 |       2409167 |       567292 |

### Tekst 1000000 B

| Język  | Wariant            |   n | Mediana [ns] | Minimum [ns] | Maksimum [ns] | Rozstęp [ns] |
| ------ | ------------------ | --: | -----------: | -----------: | ------------: | -----------: |
| C++    | long_dense_mixed   |  30 |     503541.5 |       469834 |        648750 |       178916 |
| Python | long_dense_mixed   |  30 |   16429583.5 |     15767708 |      17169208 |      1401500 |
| C++    | long_sparse_mixed  |  30 |     507792.0 |       469708 |        635500 |       165792 |
| Python | long_sparse_mixed  |  30 |   18996687.0 |     18418667 |      22482667 |      4064000 |
| C++    | short_dense_mixed  |  30 |     502041.5 |       462125 |        558417 |        96292 |
| Python | short_dense_mixed  |  30 |   15717312.5 |     15106792 |      16245209 |      1138417 |
| C++    | short_lf           |  30 |     504020.5 |       469833 |        617333 |       147500 |
| Python | short_lf           |  30 |   21284062.5 |     20324625 |      22123375 |      1798750 |
| C++    | short_sparse_mixed |  30 |     489667.0 |       464584 |        551333 |        86749 |
| Python | short_sparse_mixed |  30 |   20014896.0 |     19455250 |      21085000 |      1629750 |

Przykłady niezależnej kontroli arytmetycznej: dla C++ `short_spaces`, 1 000 B, dwie środkowe wartości wynoszą 541 i 542 ns, więc mediana to `(541 + 542) / 2 = 541,5 ns`, a rozstęp `750 − 458 = 292 ns`. Dla Pythona `long_sparse_mixed`, 1 000 000 B, wartości środkowe 18 995 708 i 18 997 666 ns dają medianę 18 996 687 ns, a rozstęp `22 482 667 − 18 418 667 = 4 064 000 ns`.

### Wizualizacja median i rozrzutu

Na wykresach te same czasy są podzielone przez 1000 i przedstawione w mikrosekundach. Osobne skale języków i paneli poprawiają czytelność; należy uwzględniać je przy porównywaniu wysokości punktów i długości odcinków.

![Mediany czasu czterech wspólnych wariantów według długości tekstu [µs]](analysis/images/mediany_dlugosc.png)

Pierwszy wykres obejmuje tylko warianty występujące przy wszystkich trzech długościach. Osie są liniowe. Odcinki łączą mediany, ale nie przedstawiają dopasowanego modelu. Bliskość punktów dla 1000 i 100000 B wynika ze skali osi długości. Źródło: [CSV przebiegu](results/20261026T184512Z_7d95f26993/measurements.csv).

![Mediany i zakresy minimum–maksimum wszystkich wariantów [µs]](analysis/images/rozrzut_warianty.png)

Drugi wykres pokazuje medianę jako punkt, a minimum i maksimum jako końce odcinka. Każdy zakres obejmuje wszystkie 30 poprawnych prób i nie jest przedziałem ufności. Panele rozdzielają długości tekstu i języki. Źródło: [CSV przebiegu](results/20261026T184512Z_7d95f26993/measurements.csv).

## 6. Interpretacja i ograniczenia

### Obserwacje wynikające z danych

Dla wszystkich 15 plików mediana czasu C++ jest niższa od mediany Pythona. Iloraz median Python/C++ wynosi od około **31,31** (`short_dense_mixed`, 1000000 B) do **42,30** (`short_sparse_mixed`, 100000 B). Są to ilorazy median w tym eksperymencie, a nie uniwersalne współczynniki szybkości języków.

W czterech wspólnych wariantach mediany rosną wraz z długością. Przykładowo dla `short_sparse_mixed` C++ uzyskuje 500, 47750 i 489667 ns, a Python 19083,5, 2020042 i 20014896 ns. Przy wzroście długości 100× mediana rośnie odpowiednio około 95,5× i 105,85×; przy kolejnym wzroście długości 10× — około 10,25× i 9,91×. Jest to zgodne z przybliżonym skalowaniem liniowym w badanym zakresie, bez dowodu ścisłej proporcjonalności.

Wpływ budowy danych nie jest identyczny w obu językach. W Pythonie `short_dense_mixed` ma niższą medianę niż `short_sparse_mixed` przy każdej długości. W C++ dla 1000 B obie mediany wynoszą 500 ns, natomiast dla 1000000 B wariant gęsty ma medianę wyższą: 502041,5 wobec 489667 ns. Nie ma podstaw do wniosku, że większy udział separatorów zawsze przyspiesza obie implementacje.

Rozrzut pokazuje ograniczenia pojedynczego pomiaru. Dla C++ `long_dense_mixed`, 100000 B, maksimum 98666 ns jest ponad dwukrotnie większe od mediany 48104 ns. Dla Pythona `long_sparse_mixed`, 1000000 B, rozstęp wynosi 4064000 ns. Zachowaliśmy te poprawne obserwacje, zamiast usuwać je jako niewygodne.

### Możliwe przyczyny i granice interpretacji

Różnice mogą wiązać się z kosztem interpretowanej pętli Pythona i optymalizacją kodu maszynowego C++. Budowa tekstu może zmieniać częstość porównań, gałęzi i zwiększania licznika. Na obserwacje skrajne mogą wpływać planista systemu i stan CPU. Nie rejestrowaliśmy jednak liczników sprzętowych, temperatury ani obciążenia, więc nie potwierdzamy tych przypuszczeń jako przyczyn.

Badanie obejmuje jedną maszynę, jeden system, jeden zestaw optymalizacji i jeden pełny przebieg. Nie przeprowadzaliśmy testów istotności ani estymacji przedziałów ufności. Brak rozgrzewek nie oznacza zimnej pamięci podręcznej: kontrola danych i wcześniejsze procesy mogły rozgrzać cache. Naprzemienna kolejność ogranicza efekt pozycji, ale nie eliminuje zakłóceń. Wyniki około 500 ns są szczególnie wrażliwe na rozdzielczość zegara i koszt jego odczytu.

### Pochodzenie kodu i odtwarzalność

[Kontrola pochodzenia](analysis/provenance.json) jest zachowaną migawką sprzed późniejszego formatowania. W tej kontroli Python był zgodny z sumą z pomiaru, natomiast C++ i `Benchmark.py` miały inne SHA-256. Samo formatowanie może zmieniać sumy bez zmiany działania, ale brak zgodności bajtowej nie pozwala przypisać historycznych czasów bieżącym źródłom. Wyniki dotyczą zapisanego przebiegu; testy obecnego kodu nie zastępują potwierdzenia tożsamości jego historycznej wersji.

Zachowane dane wejściowe i manifesty są dostępne i zgodne z metadanymi eksperymentu. Generator ma jednak znany błąd: przed zapisaniem manifestu odwołuje się do brakującego pola `source` słownika i kończy się `KeyError: 'source'`. Nie przedstawiamy zatem generowania od nowa jako w pełni sprawnej procedury. Ograniczenie nie zmienia analizy zachowanego CSV; naprawa generatora i nowy pomiar bieżącego kodu pozostają odrębnymi zadaniami.

## 7. Podział pracy i wykorzystanie AI

Projekt realizowaliśmy i weryfikowaliśmy wspólnie, z następującym podziałem odpowiedzialności:

- **Regulus** odpowiadał za planowanie, projektowanie algorytmu i końcowy przegląd rozwiązania.
- **Mars** odpowiadał za implementację algorytmu oraz przygotowanie materiałów do oddania.

Podział pracy był zgodny z zalecanym podziałem pracy wedle naszych predyspozycji oraz cech otrzymanych przez maila na podstawie wyników testu na archityp dewelopera.

Wykorzystaliśmy AI jako wsparcie pracy nad projektem. Pomoc obejmowała:

- przeportowanie implementacji licznika z C++ do Pythona z zachowaniem tego samego algorytmu i przejść stanu;
- przygotowanie dodatkowych testów w Pythonie;
- opracowanie końcowego raportu na podstawie `MOCK_RAPORT.md`;
- wyszukanie zasobów potrzebnych do przygotowania zestawów danych, w tym źródła słownika angielskich słów.

Rezultatów AI nie przyjmowaliśmy bez sprawdzenia. Kontrola obejmowała porównanie implementacji z definicją słowa, uruchomienie przypadków kontrolnych i testów automatycznych, weryfikację wejść przez SHA-256 oraz niezależne przeliczenie statystyk wszystkich 30 grup z surowego CSV, bez używania funkcji statystycznej analizatora. Porównaliśmy też liczby w raporcie i jednostki wykresów. Za przyjęte rozwiązanie, interpretację wyników i ostateczną treść raportu odpowiada zespół.

## 8. Odtworzenie analizy i wnioski

Instrukcja kompilacji, testów, generowania danych, uruchomienia nowego benchmarku i dokładne polecenie eksportu przez Pandoc znajdują się w [CONTRIBUTING.md](CONTRIBUTING.md). Szczegóły automatu i formatu wyników opisano w [BENCHMARK.md](BENCHMARK.md). Do odtworzenia statystyk zachowanego przebiegu służy:

```sh
python3 -m venv .venv-analysis
.venv-analysis/bin/python -m pip install -r requirements-analysis.txt
.venv-analysis/bin/python -B Analyze.py --run-dir results/20261026T184512Z_7d95f26993 --output-dir analysis-reproduced
python3 -B -m unittest discover -s tests -v
```

Polecenia dotyczą macOS/Linux. W Windows ścieżka interpretera środowiska to `.venv-analysis\Scripts\python.exe`; przenośność całości na tym systemie nie była sprawdzana. Nowa analiza jest zapisywana osobno, bez zastępowania zachowanych materiałów. Nowy benchmark również tworzy osobny katalog i nie powinien nadpisywać historycznych wyników.

W badanym przebiegu implementacja C++ miała niższą medianę dla każdego pliku. W obu językach wzrost czasu w czterech wspólnych wariantach był zgodny z oczekiwanym, przybliżonym skalowaniem liniowym. Budowa tekstu wiązała się z różnicami czasów, ale nie uzyskaliśmy jednej reguły wpływu separatorów wspólnej dla obu implementacji.

Hipoteza skalowania jest zgodna z obserwacjami w badanym zakresie. Rozrzut poprawnych pomiarów potwierdza potrzebę powtórzeń i analizy mediany wraz z zakresem, zamiast oceniania programu na podstawie jednej próby. Wnioski ograniczamy do zapisanych danych i warunków eksperymentu, z uwzględnieniem opisanych ograniczeń pochodzenia źródeł i odtwarzalności generatora.
