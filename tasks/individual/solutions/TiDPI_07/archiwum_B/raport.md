---
title: "TiDPI 07 - Rzetelny benchmark C++ i Python"
author: "Kryptonim TiDPI: Regulus"
date: "2026-10-17"
lang: pl-PL
---

# Sprawozdanie TiDPI 07 - rzetelny benchmark C++ i Python

## 1. Kryptonim TiDPI i wykonany poziom

Kryptonim: **Regulus**. Wykonany zakres: **A–B**, aktualizacja 2026-10-17.
B obejmuje dwie nowe pełne poprawne serie i osobną kontrolę błędną.
C–D nie wykonywano. Operacja ma status uzgodnionej z prowadzącym na podstawie
polecenia użytkownika: ręczna suma odległości od 500.

**Jawne uzgodnienie parametrów:** zastane A miało 20 020 liczb i 200 rund,
a nie 10 000 liczb i 100 rund. Użytkownik wybrał zachowanie pliku A i 100 rund
w B. Oczekiwanie B wynosi 501 000 000; historyczne A nadal ma 1 002 000 000.
Nie porównuje się czasów A i B jako identycznych obciążeń. Użytkownik potwierdził
pięć pól dokładnego nagłówka; wzmianka o sześciu polach była rozbieżnością.

Przeczytano cały szkolny PDF (10 stron), w tym A–D, artefakty, sprawozdanie
i kryteria oceny. PDF wymaga automatyzacji, walidatora, błędnej próby, dwóch serii,
minimum i mediany. Dodatkowe wymagania użytkownika obejmują plan przed pomiarami,
niezależne oczekiwanie, max/rozstęp, histogram kontroli ujemnej, pełne dowody i render.
Lokalny AGENTS.md jest pusty; jego zastanej zmiany nie modyfikowano. Organizację
raportów TiDPI_03, TiDPI_05 i TiDPI_06 wykorzystano bez przenoszenia ich wyników.

Głównym sprawozdaniem jest ten dokument. Eksport: [raport PDF](raport.pdf).
[Archiwum raportu A](archiwum_A/raport.md) i [eksportu A](archiwum_A/raport.pdf)
są niezmienionymi migawkami; ich względne odsyłacze historyczne odnoszą się do
pierwotnego katalogu TiDPI_07. D01–D09 i TC-01–TC-05 zachowują historyczne znaczenie.

### Aktualne pliki rozwiązania

- [C++ B](benchmark.cpp), [Python B](benchmark.py), [generator](generate_data.py), [dane](dane/input.txt).
- [Plan B](plan_B.md), [automat](run_benchmark.py), [walidator](validate_results.py).
- [Testy kontraktu](test_validate_results.py), [niezależne przeliczenie](verify_B.py), [kontrola artefaktów](check_artifacts.py).
- [Eksport](export_report.sh): `sh export_report.sh`, Pandoc i XeLaTeX.

Szkolny PDF, pliki wykonywalne i pomocnicze pliki renderowania nie są częścią oddania.

## 2. Cel i hipoteza

### Poziom A — zapis historyczny

Pytanie: jakie czasy osiągną dwie ręczne implementacje tej samej sumy odległości,
gdy dane, liczba rund i granice pomiaru są wspólne? Hipoteza zapisana w D01:
obie implementacje zwrócą dokładnie wynik wzorcowy; czasy mogą się różnić,
bez wybierania zwycięzcy przed pomiarem. Celem jest poprawny rdzeń benchmarku,
a nie ustalenie uniwersalnej szybkości języków.

Niezależnie oczekiwany wynik: **1 002 000 000** po **200 rundach**.
To wynik obliczeń; odcisk SHA-256 identyfikuje bajty pliku i ma inne znaczenie.

### Poziom B

Pytanie B: czy kierunek porównania minimum i mediany dwóch implementacji
powtórzy się w dwóch osobnych seriach przy wspólnym pliku i 100 rundach?
Hipotezę bez wyboru zwycięzcy zapisano w D10 przed nowymi pomiarami.
Obie implementacje mają uzyskać **501 000 000**. Plan B nie jest przedstawiany
jako plan sprzed historycznych pomiarów A.

## 3. Środowisko oraz konfiguracja

### Poziom A — zapis historyczny

Metryczka D02 została zebrana 2026-10-17 o 10:22:26 czasu Europe/Warsaw.
Pomiary wykonano lokalnie, kolejno, bez debuggera.

| Element    | Faktycznie użyta wartość (D02)        |
| :--------- | :------------------------------------ |
| Sprzęt     | Apple M4 Pro, arm64, 24 GiB RAM       |
| System     | macOS 27.0.1, build 26A434            |
| Kompilator | Apple Clang 21.0.0, clang-2100.3.34.2 |
| Target     | arm64-apple-darwin27.0.0              |
| Python     | CPython 3.14.4                        |
| C++        | C++17, Release, `-O2 -DNDEBUG`        |

Rzeczywiste polecenie budowania (D04), z katalogu TiDPI_07:

```sh
clang++ -std=c++17 -O2 -DNDEBUG -Wall -Wextra -pedantic \
  benchmark.cpp -o _build/benchmark
```

`-O2` włącza optymalizację; `-DNDEBUG` definiuje makro konfiguracji Release;
standardowe `assert` nie są używane do kontroli badanego C++.
Kod kompilatora wyniósł 0; oba strumienie kompilacji są puste.
Nie używano Windows, Visual Studio ani MSVC. Jest to lokalna adaptacja
procedury szkolnej na macOS/arm64/Clang.

C++ używa `steady_clock`, `is_steady=1`, nominalny okres typu zegara 1/1 000 000 000 s.
To okres reprezentacji, nie zmierzona efektywna rozdzielczość. Tej ostatniej
nie wyznaczono. Python używa `perf_counter_ns()`; `get_clock_info` zgłosił
`mach_absolute_time()`, monotoniczność i rozdzielczość około **41,667 ns**.
Oba programy zapisują `time_ns`; jednostka zapisu nie określa dokładności pomiaru.
Informacje o zegarach zachowano na stderr (D05-D06).

### Poziom B

D12 i D14 zawierają osobne aktualne metryczki. Obie serie: Apple M4 Pro,
arm64, 24 GiB RAM, macOS 27.0.1 (26A434), Apple Clang 21.0.0,
CPython 3.14.4. To pomiary macOS/Clang zamiast szkolnych Windows/Visual Studio/MSVC.
Każdy przebieg budowano osobno, bez debuggera, z optymalizacją `-O2`, makrem `-DNDEBUG` i standardem C++17.
Pełne flagi, polecenia i kody kompilacji zachowano w D12–D14.

Zegary i jednostka nie zmieniły się: C++ `steady_clock`, nominalny okres 1 ns;
Python `mach_absolute_time()`, zgłoszona rozdzielczość około **41,667 ns**.
Informacje są w stderr każdego procesu. Efektywnej rozdzielczości C++
i dokładności całego eksperymentu nie mierzono; jednostka `time_ns` nie dowodzi
dokładności 1 ns. Wersję kompilatora zapisano bez prywatnej ścieżki instalacji.

## 4. Zmienne i warunki eksperymentu

### Poziom A — zapis historyczny

Czynnik porównywany: konkretna implementacja C++ lub Python.
Stałe: maszyna, wspólny plik, kolejność liczb, 200 rund, ręczne pętle,
2 rozgrzewki na proces i 5 prób na blok. Łącznie każda implementacja wykonała
**4 rozgrzewki i 10 prób właściwych**. Parametry ustalono przed pomiarami (D01).
Rotowana jest kolejność całych bloków, nie pojedynczych prób.

Generator tworzy **20 020** liczb całkowitych z zakresu **0-1000**:
każda wartość występuje dokładnie 20 razy. `random.Random(20261017).shuffle`
tasuje gotowy multizbiór; **seed = 20261017**. Nie jest to niezależne losowanie
każdego elementu. Plik ASCII ma jedną liczbę na wiersz i zakończenia LF.
Dane zapisano raz; oba programy odczytują `dane/input.txt`.

Pełny SHA-256 w D03 i D07; poniższe dwa wiersze należy połączyć bez spacji:

```text
1e1422a8679f65bb7ec778bdbd821b74a459
6431774711e89671acaa9ddca3d8
```

Weryfikator sprawdził hash bajtów i cały histogram. Hash po serii zgadzał się
z hashem generatora przed kompilacją. Polecenia D04 wskazują ten sam plik;
kod benchmarków tylko go odczytuje. Odrębnych danych dla języków nie generowano.

### Poziom B

B zachowuje dokładnie bajty pliku A, histogram, seed i zakres opisane powyżej.
Hash przed i po każdej serii jest zgodny; kopia pliku jest w każdym katalogu
przebiegu. Oba procesy odczytują wspólny `dane/input.txt`.
Zmieniono rounds z historycznych 200 na uzgodnione **100**, jednakowo dla obu
implementacji. B bada jedną konfigurację; zmiany tej nie przedstawia się jako C.

Rotacja, rozgrzewki i próby są jak w A: blok 1 C++ → Python, blok 2 Python → C++;
po 2 rozgrzewki i 5 prób na proces, czyli **4 rozgrzewki i 10 prób na implementację**.
Harmonogram zapisano przed uruchomieniami. Start procesu, odczyt, alokacja,
walidacja i wypisywanie są poza stoperem. Nie usuwano ani nie zastępowano czasów.
Kontrola ujemna zmienia tylko środek w osobnej kopii Pythona.

## 5. Kontrola poprawności

### Poziom A — zapis historyczny

### Wzorzec niezależny od benchmarków

Dla wartości 0-1000 odległości po obu stronach 500 tworzą dwa ciągi 1-500:

```text
1 + ... + 500 = 500 * 501 / 2 = 125250
jedna kopia 0..1000: 2 * 125250 = 250500
20 kopii: 20 * 250500 = 5010000
200 rund: 200 * 5010000 = 1002000000
```

Formułę zapisano przed pomiarami (D01). Po pomiarach D07 dodatkowo policzył
wynik innym algorytmem: dla liczb poniżej 500 użył różnicy `500 * count - sum`,
a powyżej 500 różnicy `sum - 500 * count`. Użycie bibliotecznej sumy w tej
niezależnej kontroli nie zmienia ręcznego algorytmu badanego.

### Implementacje i arytmetyka

W obu funkcjach wynik zaczyna od zera. Zewnętrzna pętla wykonuje 200 rund,
wewnętrzna przechodzi po wspólnych danych. Oblicza `d = x - 500`, zmienia znak
gdy `d < 0`, następnie dodaje `d` do akumulatora. Nie używa `sum()` ani `abs()`
w mierzonej operacji. C++ przechowuje liczby i wynik w `int64_t`, Python w `int`.

Po walidacji wejścia `d` mieści się w zakresie od -500 do 500, a odległość
od 0 do 500. Największy możliwy wynik wynosi
`20020 * 500 * 200 = 2002000000`, znacznie mniej niż
`9223372036854775807` dla `int64_t`. Iloczyny występują w uzasadnieniu,
nie w badanej pętli. Akumulator rośnie monotonnie i również pośrednie wyniki
mieszczą się w typie. Python ma arytmetykę całkowitą o dowolnej precyzji.

Poza stoperem każdy wynik jest porównywany ze stałą wzorcową, wypisywany
lub zapisywany w diagnostyce rozgrzewki. Błędny checksum przerywa proces kodem 1;
błąd wejścia/parametrów kodem 2. Samo sprawdzanie i wypisanie wyniku zapewnia
obserwowalność, lecz nie wyklucza wszystkich transformacji kompilatora.
Nie użyto `volatile` ani wyłączenia optymalizacji; nie badano asemblera.

### Rejestr dowodów i testów

- **D01** - [Plan](plan_A.md) sprzed pierwszego pomiaru; kopia w źródłach D02
- **D02** - [Środowisko](wyniki/20261017_102226_905860_A/environment.json), [SHA źródeł](wyniki/20261017_102226_905860_A/source_sha256.json), [kopia C++](wyniki/20261017_102226_905860_A/sources/benchmark.cpp)
- **D03** - [Metadane generatora](wyniki/20261017_102226_905860_A/generator_stdout.txt), [dane](dane/input.txt)
- **D04** - [Polecenia](wyniki/20261017_102226_905860_A/commands.txt), [kody](wyniki/20261017_102226_905860_A/exit_codes.json), [stdout kompilatora](wyniki/20261017_102226_905860_A/compile_stdout.txt), [stderr](wyniki/20261017_102226_905860_A/compile_stderr.txt)
- **D05** - C++: [blok 1 stdout](wyniki/20261017_102226_905860_A/block1_cpp_stdout.txt), [stderr](wyniki/20261017_102226_905860_A/block1_cpp_stderr.txt), [blok 2 stdout](wyniki/20261017_102226_905860_A/block2_cpp_stdout.txt), [stderr](wyniki/20261017_102226_905860_A/block2_cpp_stderr.txt)
- **D06** - Python: [blok 1 stdout](wyniki/20261017_102226_905860_A/block1_python_stdout.txt), [stderr](wyniki/20261017_102226_905860_A/block1_python_stderr.txt), [blok 2 stdout](wyniki/20261017_102226_905860_A/block2_python_stdout.txt), [stderr](wyniki/20261017_102226_905860_A/block2_python_stderr.txt)
- **D07** - [Weryfikacja i statystyki](wyniki/20261017_102226_905860_A/verification.json), [stdout](wyniki/20261017_102226_905860_A/verify_stdout.txt), [stderr](wyniki/20261017_102226_905860_A/verify_stderr.txt), [kod](wyniki/20261017_102226_905860_A/verify_exit_code.txt)
- **D08** - [Niezależne przeliczenie](wyniki/20261017_102226_905860_A/independent_check.txt)
- **D09** - [Kontrola końcowych artefaktów](wyniki/20261017_102226_905860_A/final_check.json)

TC-01: pełny histogram, count, seed, hash i wzorzec - **zgodne** (D03, D07).
TC-02: rzeczywiste flagi Release, źródła, kod kompilatora 0 - **zgodne** (D02, D04).
TC-03: nagłówek, typy, dodatnie czasy, numery 1-10, 20 rekordów i 8 rozgrzewek,
checksum oraz `true`, wszystkie kody procesów 0 - **zgodne** (D05-D07).
TC-04: osobne przeliczenie wzorca, median, rozstępów i wierszy 1 oraz 10
obu implementacji - **zgodne** (D08).
TC-05: komplet plików, linki, anonimizacja oraz przegląd renderu eksportu - D09.

### Poziom B

W B wynik jednej rundy nadal wynosi 5 010 000, po 100 rundach **501 000 000**.
Walidator liczy go z liczności i sum partycji poniżej/powyżej 500, bez importowania
badanej funkcji. Sprawdza też pełny histogram i stały hash danych.
C++: różnica mieści się w −500…500, odległość w 0…500, a największa możliwa
suma `20020 × 500 × 100 = 1001000000` mieści się w `int64_t`, także pośrednio.

Kontrakt: dokładnie `language;trial;time_ns;checksum;correct`, pięć pól;
`cpp/python` zgodnie z producentem, całkowite próby i checksumy, całkowity czas
≥0, numery dokładnie 1–10 bez powtórzeń, pięć prób na blok, `correct=true`
i niezależny checksum w każdym rekordzie. Oddzielnie sprawdzane są cztery
rozgrzewki każdej implementacji, ich numery, czasy i checksumy. Walidator sprawdza
również harmonogram, kody, konfigurację Release, informacje o zegarach i kopie źródeł.

Walidacja całości poprzedza statystyki i publikację CSV. Kody walidatora i automatu:
0 — akceptacja; 1 — odrzucenie eksperymentu; 2 — błąd obsługi/konfiguracji.
Timeout ma umowny kod 124, błąd uruchomienia 127; nie wystąpiły w trzech seriach.

TC-06: integralność historycznego A — **zgodna** (D10, D15).
TC-07: 18 fixture walidatora — **18 zgodnych, 0 niezgodnych** (D11).
TC-08: pierwszy pełny poprawny przebieg — **zaakceptowany** (D12).
TC-09: kontrola ujemna — **odrzucona, bez CSV** (D13).
TC-10: drugi pełny przebieg po błędzie — **zaakceptowany** (D14).
TC-11: niezależne przeliczenie i powtarzalność wniosku — **zgodne** (D15).
TC-12: komplet, linki, anonimizacja i wizualny przegląd aktualnego PDF — D16.

D11 obejmuje poprawne dane, czas 0, zły nagłówek/jednostkę, brak/nadmiar pola,
obcą i niezgodną implementację, zły typ, ujemny czas, duplikat, brak/nadmiar próby,
`false`, błędny checksum mimo `true`, błędną rozgrzewkę, kod procesu, harmonogram
i hash danych. Każde z 16 odrzuceń usuwa wcześniej istniejący poprawny CSV fixture.
Są to sztuczne dane kontraktu, nie pomiary. Kod używa jawnych warunków;
walidacja produkcyjna nie zależy od aktywności `assert`.

Przed błędem D13 potwierdził na rzeczywistym histogramie różne oczekiwania:
`20 × 2 × 125250 × 100 = 501000000` dla środka 500,
`20 × 500500 × 100 = 1001000000` dla środka 0. Nie zmieniono danych ani
oczekiwania. Osobna kopia zmienia jedną linię `d = x - 500` na `d = x - 0`.
Python kończy oba bloki kodem 1 już po pierwszej rozgrzewce, z `correct=false`;
walidator rozpoznaje także błędny checksum i brak kompletu. Nie powstał CSV.
Nie ma więc właściwych czasów Pythona z tej próby do porównania.

## 6. Procedura

### Poziom A — zapis historyczny

1. Przeczytano materiał i wzorce raportów, sprawdzono Git. Istniejącą zmianę
   pustego `AGENTS.md` pozostawiono bez modyfikacji. W TiDPI_07 nie było źródeł
   ani pomiarów; jedynym plikiem był szkolny PDF.
2. Zapisano D01 przed kompilacją i pomiarami; przygotowano obie implementacje.
3. Pierwsze przygotowanie metryczki przerwał sandbox przy `sysctl` (kod 1).
   Generator, kompilacja i pomiary jeszcze nie ruszyły. Zachowano
   [notatkę przygotowania](wyniki/20261017_102013_529727_A/preflight.txt).
   Po autoryzacji wykonano serię w nowym katalogu. Notatka jest opisem zdarzenia,
   nie pełnym logiem ani zanonimizowaną kopią surowych czasów.
4. Zebrano D02, kopie i hashe źródeł; wygenerowano wspólny plik, zapisano D03.
5. Skompilowano C++ w Release (D04). Blok 1: C++, potem Python;
   blok 2: Python, potem C++. Każdy proces wykonał 2 rozgrzewki, potem 5 prób.
   Procesy nie działały równocześnie. Zachowano wszystkie czasy.
6. Stoper obejmuje wywołanie funkcji, inicjalizację wyniku, pętle i powrót.
   C++: `steady_clock::now()` i `duration_cast<nanoseconds>`;
   Python: `time.perf_counter_ns()`. Odczyt, alokacja i przygotowanie,
   walidacja wejścia, kontrola wyniku i wypisywanie pozostają poza pomiarem.
   Zapis czasu zawiera także nieunikniony narzut wywołania zegara.
7. Najpierw sprawdzono wszystkie rekordy i rozgrzewki. Dopiero po akceptacji
   wyliczono statystyki i złożono pliki `A_*_raw.txt` (D07). D08 sprawdza wybrane
   rachunki ponownie. Nie wykonano celowego uszkodzenia danych wymaganego w B.

Historyczne polecenia użyte dla A (bieżące źródła są już wersją B):

```sh
python3 collect_A.py
python3 verify_A.py wyniki/IDENTYFIKATOR_NOWEJ_SERII
```

Identyfikator wypisuje pierwszy skrypt; trzeba zastąpić nim drugą ścieżkę.
Historyczny kolektor tworzył nowy katalog wyników. Nie należy go uruchamiać z bieżącymi źródłami B; odtworzenie A wymaga wersji źródeł z D02. Generator odtwarza wejście
z tym samym seedem; wzorcowy hash umożliwia kontrolę zgodności bajtów.
Użycie tej samej wersji CPython 3.14.4 usuwa niepewność co do zmiany procedury
`shuffle` między wersjami. Można też użyć dołączonego gotowego pliku danych.
Weryfikator uruchamiać zwykłym `python3`, bez `-O` (korzysta z `assert`).

### Poziom B

1. Sprawdzono Git, zarchiwizowano raport i PDF A oraz zweryfikowano hashe
   historycznych kopii. Zapisano plan B przed nowymi pomiarami (D10).
2. Zmieniono obie implementacje do 100 rund i wykonano testy walidatora (D11).
3. Pierwsze przygotowanie B przerwał odczyt metryczki w sandboxie;
   [katalog niepełnego przygotowania](przebiegi/20261017_104254_574971_good1/runner_result.json)
   nie zawiera kompilacji ani pomiarów. Po zezwoleniu wykonano nową serię D12.
4. Automat zapisał harmonogram, kopie źródeł i dane, metryczkę, skompilował świeży
   plik w katalogu przebiegu i uruchomił cztery procesy kolejno. Każdy strumień
   i kod zapisano oddzielnie, również przy błędzie. Limit procesu wynosi 60 s,
   kompilacji 120 s. Po nieudanej kompilacji nie uruchamia się programu.
5. Zapisano histogram D13, utworzono uszkodzoną kopię i wykonano rzeczywiste odrzucenie.
   Automat zachował także poprawne procesy C++, bez analizowania ich jako zaakceptowanej serii.
6. Uruchomiono ponownie poprawne źródła w D14. Oryginał Pythona pozostał
   niezmieniony przez kontrolę ujemną; jego hash odpowiada poprawnemu D14.
7. Niezależnie przeliczono wyniki (D15), uzupełniono raport i wykonano eksport (D16).

Odtworzenie B z katalogu zadania (każda komenda tworzy nowy katalog):

```sh
python3 test_validate_results.py
python3 run_benchmark.py --label good1
python3 run_benchmark.py --label fault \
  --python-source kontrola_bledna/benchmark.py
python3 run_benchmark.py --label good2
python3 validate_results.py przebiegi/IDENTYFIKATOR
```

Przebieg `fault` ma oczekiwany kod 1. Wymagane są lokalne Clang, Python,
`sw_vers` i `sysctl`. Nie uruchamiać serii równolegle. Plan i kontrola histogramu
są zachowane w załącznikach; `verify_B.py` przelicza wskazane serie historyczne.

## 7. Surowe wyniki

### Poziom A — zapis historyczny

D05 i D06 to pełne, niezmienione strumienie procesów. Rozgrzewki są osobnymi
rekordami na stderr i nie należą do tabeli prób. Poniżej pełna zawartość
pochodnych plików `A_cpp_raw.txt` i `A_python_raw.txt`: połączono po dwa bloki,
zachowując wszystkie pola i jeden nagłówek. Nie przedstawia się ich jako
stdout pojedynczego procesu. Oryginalne bloki pozostają do kontroli.

C++ (D05, agregacja D07):

```text
language;trial;time_ns;checksum;correct
cpp;1;808500;1002000000;true
cpp;2;795375;1002000000;true
cpp;3;773084;1002000000;true
cpp;4;840916;1002000000;true
cpp;5;779375;1002000000;true
cpp;6;668208;1002000000;true
cpp;7;730208;1002000000;true
cpp;8;731834;1002000000;true
cpp;9;676125;1002000000;true
cpp;10;659875;1002000000;true
```

Python (D06, agregacja D07):

```text
language;trial;time_ns;checksum;correct
python;1;107626500;1002000000;true
python;2;106623500;1002000000;true
python;3;107586333;1002000000;true
python;4;106552750;1002000000;true
python;5;106012416;1002000000;true
python;6;133934750;1002000000;true
python;7;139381458;1002000000;true
python;8;132183500;1002000000;true
python;9;135451250;1002000000;true
python;10;135279125;1002000000;true
```

### Poziom B

### Rejestr nowych dowodów B

- **D10** — [plan B](plan_B.md), [integralność i archiwizacja A](archiwum_A/integrity.json).
- **D11** — [18 testów walidatora](przebiegi/20261017_104245_986516_validator_tests/summary.json), [źródło testów](test_validate_results.py).
- **D12** — przebieg 1: [metryczka](przebiegi/20261017_104449_232316_good1/environment.json), [harmonogram](przebiegi/20261017_104449_232316_good1/schedule.json), [polecenia](przebiegi/20261017_104449_232316_good1/commands.txt), [kody](przebiegi/20261017_104449_232316_good1/exit_codes.txt), [walidacja](przebiegi/20261017_104449_232316_good1/validation.json), [zaakceptowany CSV](przebiegi/20261017_104449_232316_good1/results.csv).
- **D13** — kontrola błędna: [histogram i oczekiwania](kontrola_bledna/histogram_check.json), [uszkodzone źródło](kontrola_bledna/benchmark.py), [diff](kontrola_bledna/change.diff), [metryczka](przebiegi/20261017_104540_940321_fault/environment.json), [harmonogram](przebiegi/20261017_104540_940321_fault/schedule.json), [polecenia](przebiegi/20261017_104540_940321_fault/commands.txt), [kody](przebiegi/20261017_104540_940321_fault/exit_codes.txt), [odrzucenie](przebiegi/20261017_104540_940321_fault/validation.json).
- **D14** — przebieg 2: [metryczka](przebiegi/20261017_104916_993218_good2/environment.json), [harmonogram](przebiegi/20261017_104916_993218_good2/schedule.json), [polecenia](przebiegi/20261017_104916_993218_good2/commands.txt), [kody](przebiegi/20261017_104916_993218_good2/exit_codes.txt), [walidacja](przebiegi/20261017_104916_993218_good2/validation.json), [zaakceptowany CSV](przebiegi/20261017_104916_993218_good2/results.csv).
- **D15** — [niezależne rachunki](kontrole_B/independent_check.json), [skrypt kontroli](verify_B.py).
- **D16** — [końcowa kontrola artefaktów](kontrole_B/final_check.json).

W każdym D12–D14 `block1_*` i `block2_*` są niezmienionymi strumieniami
poszczególnych procesów, nie agregacją. `exit_codes.txt` zawiera także kod walidatora;
`exit_codes.json` zawiera kody kompilacji i benchmarków. `execution.json` zapisuje
rzeczywisty czas i status wywołań. `sources/` i `source_sha256.json` identyfikują kod.
`input.txt` jest kopią wspólnego wejścia. `validate_stdout.txt` i `validate_stderr.txt`
są strumieniami walidatora. Nie redagowano surowych dowodów.

**D12 — komplet strumieni:**

- Blok 1: [cpp stdout](przebiegi/20261017_104449_232316_good1/block1_cpp_stdout.txt), [cpp stderr](przebiegi/20261017_104449_232316_good1/block1_cpp_stderr.txt), [python stdout](przebiegi/20261017_104449_232316_good1/block1_python_stdout.txt), [python stderr](przebiegi/20261017_104449_232316_good1/block1_python_stderr.txt).
- Blok 2: [cpp stdout](przebiegi/20261017_104449_232316_good1/block2_cpp_stdout.txt), [cpp stderr](przebiegi/20261017_104449_232316_good1/block2_cpp_stderr.txt), [python stdout](przebiegi/20261017_104449_232316_good1/block2_python_stdout.txt), [python stderr](przebiegi/20261017_104449_232316_good1/block2_python_stderr.txt).
- [kompilacja stdout](przebiegi/20261017_104449_232316_good1/compile_stdout.txt), [kompilacja stderr](przebiegi/20261017_104449_232316_good1/compile_stderr.txt), [stdout walidatora](przebiegi/20261017_104449_232316_good1/validate_stdout.txt), [stderr walidatora](przebiegi/20261017_104449_232316_good1/validate_stderr.txt), [hashe źródeł](przebiegi/20261017_104449_232316_good1/source_sha256.json).

**D13 — komplet strumieni:**

- Blok 1: [cpp stdout](przebiegi/20261017_104540_940321_fault/block1_cpp_stdout.txt), [cpp stderr](przebiegi/20261017_104540_940321_fault/block1_cpp_stderr.txt), [python stdout](przebiegi/20261017_104540_940321_fault/block1_python_stdout.txt), [python stderr](przebiegi/20261017_104540_940321_fault/block1_python_stderr.txt).
- Blok 2: [cpp stdout](przebiegi/20261017_104540_940321_fault/block2_cpp_stdout.txt), [cpp stderr](przebiegi/20261017_104540_940321_fault/block2_cpp_stderr.txt), [python stdout](przebiegi/20261017_104540_940321_fault/block2_python_stdout.txt), [python stderr](przebiegi/20261017_104540_940321_fault/block2_python_stderr.txt).
- [kompilacja stdout](przebiegi/20261017_104540_940321_fault/compile_stdout.txt), [kompilacja stderr](przebiegi/20261017_104540_940321_fault/compile_stderr.txt), [stdout walidatora](przebiegi/20261017_104540_940321_fault/validate_stdout.txt), [stderr walidatora](przebiegi/20261017_104540_940321_fault/validate_stderr.txt), [hashe źródeł](przebiegi/20261017_104540_940321_fault/source_sha256.json).

**D14 — komplet strumieni:**

- Blok 1: [cpp stdout](przebiegi/20261017_104916_993218_good2/block1_cpp_stdout.txt), [cpp stderr](przebiegi/20261017_104916_993218_good2/block1_cpp_stderr.txt), [python stdout](przebiegi/20261017_104916_993218_good2/block1_python_stdout.txt), [python stderr](przebiegi/20261017_104916_993218_good2/block1_python_stderr.txt).
- Blok 2: [cpp stdout](przebiegi/20261017_104916_993218_good2/block2_cpp_stdout.txt), [cpp stderr](przebiegi/20261017_104916_993218_good2/block2_cpp_stderr.txt), [python stdout](przebiegi/20261017_104916_993218_good2/block2_python_stdout.txt), [python stderr](przebiegi/20261017_104916_993218_good2/block2_python_stderr.txt).
- [kompilacja stdout](przebiegi/20261017_104916_993218_good2/compile_stdout.txt), [kompilacja stderr](przebiegi/20261017_104916_993218_good2/compile_stderr.txt), [stdout walidatora](przebiegi/20261017_104916_993218_good2/validate_stdout.txt), [stderr walidatora](przebiegi/20261017_104916_993218_good2/validate_stderr.txt), [hashe źródeł](przebiegi/20261017_104916_993218_good2/source_sha256.json).

Poniżej pełne rekordy właściwych prób B jako pochodna prezentacja bloków; oryginalne stdout są wskazane powyżej.

### D12 — przebieg 1

cpp:

```text
language;trial;time_ns;checksum;correct
cpp;1;552000;501000000;true
cpp;2;464959;501000000;true
cpp;3;467875;501000000;true
cpp;4;463000;501000000;true
cpp;5;459292;501000000;true
cpp;6;335875;501000000;true
cpp;7;339458;501000000;true
cpp;8;341750;501000000;true
cpp;9;335541;501000000;true
cpp;10;303792;501000000;true
```

python:

```text
language;trial;time_ns;checksum;correct
python;1;54592709;501000000;true
python;2;55922333;501000000;true
python;3;55462792;501000000;true
python;4;55978709;501000000;true
python;5;54561709;501000000;true
python;6;54863041;501000000;true
python;7;55469000;501000000;true
python;8;57055084;501000000;true
python;9;55348208;501000000;true
python;10;55618583;501000000;true
```

### D14 — przebieg 2

cpp:

```text
language;trial;time_ns;checksum;correct
cpp;1;352333;501000000;true
cpp;2;353416;501000000;true
cpp;3;353292;501000000;true
cpp;4;376042;501000000;true
cpp;5;373375;501000000;true
cpp;6;306958;501000000;true
cpp;7;306125;501000000;true
cpp;8;323375;501000000;true
cpp;9;340042;501000000;true
cpp;10;319292;501000000;true
```

python:

```text
language;trial;time_ns;checksum;correct
python;1;57780875;501000000;true
python;2;57082500;501000000;true
python;3;57581083;501000000;true
python;4;56790667;501000000;true
python;5;57419042;501000000;true
python;6;57217875;501000000;true
python;7;57593208;501000000;true
python;8;57442667;501000000;true
python;9;58419209;501000000;true
python;10;56792625;501000000;true
```

### D13 — fragment błędnego stderr Pythona

```text
warmup=1;time_ns=37196334;checksum=1001000000;correct=false
```

To fragment pierwszego procesu, nie pełny stderr. Walidator ma kod 1,
`accepted=false`, `csv_created=false`, `published_records=0`.

## 8. Opracowanie wyników

### Poziom A — zapis historyczny

Tabela 1. Jedna seria A, ta sama konfiguracja, 10 prób na implementację;
jednostka **ms**, przeliczenie `time_ns / 1000000`. Źródło: D05-D08.

| Miara    | C++ Release |     Python |
| :------- | ----------: | ---------: |
| Minimum  |    0,659875 | 106,012416 |
| Maksimum |    0,840916 | 139,381458 |
| Rozstęp  |    0,181041 |  33,369042 |
| Mediana  |    0,752459 | 119,905000 |

Mediana przy 10 próbach to średnia piątej i szóstej wartości po sortowaniu.
Dla C++: `(731834 + 773084) / 2 = 752459 ns`.
Dla Python: `(107626500 + 132183500) / 2 = 119905000 ns`.
Rozstęp to maksimum minus minimum. Nie zaokrąglano danych przed obliczeniem.
Minimum pokazuje najszybszą zaobserwowaną próbę, mediana środek rozkładu
zachowanych czasów. Żadna z nich nie jest gwarantowanym czasem programu.

D08 ponownie sprawdza te rachunki z użyciem `Decimal`, a także surowe wiersze
1 i 10 obu języków: checksum zgodny z formułą i przeliczenie ns na ms.
Przykładowo pierwsza próba C++: `808500 ns = 0,808500 ms`;
pierwsza Python: `107626500 ns = 107,626500 ms`.

### Poziom B

Tabela 2. Poprawne serie B, 100 rund, po 10 prób na implementację; **ms**. Źródła: D12, D14, niezależna kontrola D15.

| Seria | Implementacja |   Minimum |  Maksimum |  Rozstęp |    Mediana |
| :---- | :------------ | --------: | --------: | -------: | ---------: |
| 1     | cpp           |  0,303792 |     0,552 | 0,248208 |   0,400521 |
| 1     | python        | 54,561709 | 57,055084 | 2,493375 |  55,465896 |
| 2     | cpp           |  0,306125 |  0,376042 | 0,069917 |  0,3461875 |
| 2     | python        | 56,790667 | 58,419209 | 1,628542 | 57,4308545 |

Mediana jest średnią pozycji 5 i 6 po sortowaniu. W serii 1:
C++ `(341750 + 459292) / 2 = 400521 ns`,
Python `(55462792 + 55469000) / 2 = 55465896 ns`.
W serii 2: C++ `(340042 + 352333) / 2 = 346187,5 ns`,
Python `(57419042 + 57442667) / 2 = 57430854,5 ns`.
Zachowano połówki ns wynikające z rachunku; nie oznaczają większej dokładności zegara.
Rozstępy to różnice skrajnych wartości, bez wstępnego zaokrąglania.

D15 innym odczytem CSV i rachunkiem `Decimal` porównał wszystkie rekordy CSV
z oryginalnymi blokami oraz ponownie obliczył min/max/rozstęp/medianę dla czterech grup.
Osobno sprawdził checksum i przeliczenie ns→ms w próbach 1 i 10 obu implementacji
w obu seriach: osiem wierszy. Weryfikację wykonał asystent.

Minimum odpowiada na pytanie o najlepszy zaobserwowany czas w tej serii.
Mediana opisuje środek uporządkowanych czasów i słabiej reaguje na pojedyncze
skrajne obserwacje. Minimum nie jest gwarantowanym osiągalnym czasem, a mediana
nie dowodzi stabilności wszystkich prób. Przy dwóch grupach czasów może leżeć
między nimi, co widać także w historycznym A. Błędnej serii nie podsumowano statystycznie.

## 9. Interpretacja

### Poziom A — zapis historyczny

**Obserwacja:** w tej serii C++ Release miał niższe minimum i medianę niż
ręczna implementacja Python. Obie zwróciły poprawne wyniki we wszystkich próbach
oraz rozgrzewkach. Dotyczy to wskazanego pliku, 200 rund i użytych programów.

**Obserwacja o kolejności (D08):** wszystkie czasy C++ z bloku 2
(0,659875-0,731834 ms) były niższe niż z bloku 1 (0,773084-0,840916 ms).
W Pythonie blok 2 (132,183500-139,381458 ms) był wolniejszy niż blok 1
(106,012416-107,626500 ms). Zachowano oba bloki. Zbiorcza mediana Pythona
leży pomiędzy grupami, dlatego nie opisuje czasu pojedynczego typowego bloku.

Przyczyny różnic między blokami nie ustalono. Nie mierzono temperatury,
częstotliwości, cache ani obciążenia tła. Rotacja kolejności ogranicza stałe
uprzywilejowanie miejsca w harmonogramie, ale nie zapewnia identycznych warunków.
Sama obserwacja nie pozwala przypisać różnic konkretnemu mechanizmowi sprzętu
ani kosztowi interpretera.

### Poziom B

**Obserwacja B:** w obu poprawnych seriach minimum i mediana C++ Release
są niższe niż Pythona. Kierunek wniosku powtórzył się, chociaż wartości i rozstępy
nie są identyczne: mediana C++ wyniosła 0,400521 i 0,3461875 ms, Pythona
55,465896 i 57,4308545 ms. W obu seriach również maksimum C++ jest poniżej
minimum Pythona. To obserwacja tych programów, pliku i konfiguracji.

**Obserwacja kontroli ujemnej:** sam szybki wynik nie wystarcza.
Uszkodzona kopia rzeczywiście wykonała inną operację, została odrzucona
niezależnie od czasu, a późniejsza poprawna seria została zaakceptowana.
Zgodność samych dwóch producentów nie zastępuje wzorca.

Nie ustalono przyczyn zmian czasów między seriami. Nie mierzono cache,
temperatury, taktowania ani obciążenia. Nie wyprowadza się uniwersalnego
współczynnika szybkości języków ani przyczyn związanych z interpreterem.

## 10. Ograniczenia eksperymentu

### Poziom A — zapis historyczny

- Jedna maszyna, jedna seria z dwoma blokami, jeden rozmiar i 200 rund.
  Nie wykonano drugiej pełnej serii B ani badań konfiguracji C-D.
- C++ i Python używają różnych reprezentacji liczb i środowisk wykonania;
  wspólne jest zadanie i ręczny algorytm, nie instrukcje maszynowe.
- Czas C++ jest krótszy niż 1 ms; narzut i zakłócenia mogą mieć względnie
  duże znaczenie. Nie kalibrowano rund w osobnym eksperymencie.
- Brak kontroli temperatury, częstotliwości, trybu zasilania i procesów tła.
  Rozgrzewka nie dowodzi osiągnięcia stabilnego stanu komputera.
- Znana jest zgłoszona rozdzielczość Pythona i nominalny okres C++;
  nie oszacowano rzeczywistej dokładności ani efektywnej rozdzielczości C++.
- Kompilator może wektoryzować lub inaczej przekształcać pętle. Zgodność
  checksumu nie dowodzi wykonania każdej instrukcji źródłowej dosłownie.
- Dane są równomiernym multizbiorem po przetasowaniu. Nie reprezentują
  wszystkich rozkładów ani zastosowań; seed nie jest dowodem jakości losowości.
- Wyniki nie obejmują odczytu, walidacji, wypisywania i startu procesu.
  macOS/Clang zastępuje szkolny zestaw Windows/MSVC.

### Poziom B

- B: jedna maszyna, dwie poprawne serie, jedna konfiguracja 100 rund i kontrola ujemna.
  Historyczne A ma 200 rund; nie łączy się tych wyników.
- Pojedyncze czasy C++ są krótsze niż 1 ms. Nie zwiększano rund ani nie kalibrowano
  czasu, ponieważ zachowano uzgodnione 100 rund; zakłócenia i narzut mają znaczenie.
- Brak pomiaru temperatury, częstotliwości, procesów tła i efektywnej rozdzielczości C++.
  Nie potwierdzono identycznych warunków zasilania wszystkich serii.
- Test błędny kończy Python w rozgrzewce, więc nie daje kompletu właściwych czasów;
  jest to dowód odrzucenia, nie dodatkowy eksperyment wydajnościowy.
- 18 fixture sprawdza wybrane reguły, nie wszystkie możliwe uszkodzenia i awarie.
  Timeouty i błędy uruchomienia mają obsługę w kodzie, ale nie wymuszano ich w tej serii.
- Atomowa publikacja dotyczy pojedynczego CSV; nie badano przerwania procesu
  między publikacją CSV a zapisem JSON ani równoczesnej walidacji tego samego katalogu.
- Pominięto ścieżkę instalacji kompilatora, aby metryczka pozostała anonimowa.
  Nie stanowi to zapisu całego środowiska systemowego.

## 11. Wnioski

### Poziom A — zapis historyczny

Poziom A został wykonany w opisanej adaptacji: wspólny plik ma ponad 10 000
liczb, dwie implementacje wykonują uzgodnioną operację, a wszystkie 20 prób
i 8 rozgrzewek zgadzają się z niezależnym wzorcem. Release, granice stopera,
źródła i pełne strumienie mają dowody D01-D08. Eksport i kontrola końcowa są w D09.

W tej serii mediany wyniosły 0,752459 ms i 119,905000 ms. Wniosek dotyczy tych
implementacji i warunków. Różnice między blokami przemawiają za zachowaniem
wszystkich prób i ostrożnością w uogólnianiu. Nie deklaruje się wyników B-D
ani przewidywanej oceny.

Najważniejsze decyzje do obrony: jeden plik eliminuje różnice generatorów;
multizbiór pozwala sprawdzić wynik prostym wzorem; stoper obejmuje tylko
pracę obliczeniową; Release pozwala mierzyć zoptymalizowany C++; rozgrzewki
są ustalone z góry; checksum kontroluje poprawność, a SHA-256 tożsamość danych.

### Poziom B

Poziom B jest potwierdzony przez D10–D16: automat, 18 kontroli walidatora,
dwa pełne zaakceptowane przebiegi z CSV, rzeczywiste odrzucenie kopii ze środkiem 0,
zachowane źródło błędu i ponowny poprawny przebieg. A zachowuje wyniki i identyfikatory.
Nie wykonano C–D ani nie deklaruje się oceny.

Najważniejsze decyzje do obrony: hash rozpoznaje dane, checksum sprawdza wynik;
wzorzec jest niezależny od pętli; rozgrzewki są osobną częścią walidacji;
CSV powstaje dopiero po akceptacji całości; rotacja dotyczy bloków;
minimum i mediana opisują inne cechy serii; parametrów A i B nie wolno mieszać.
Zachowanie 20 020 liczb i zmiana do 100 rund oraz pięć pól są jawnie uzgodnione.

## 12. Wykorzystanie AI i sposób weryfikacji

### Poziom A — zapis historyczny

Asystent Codex przeczytał materiał, przygotował plan, kod, zapis dowodów,
weryfikator i raport oraz wykonał rzeczywiste uruchomienia. Weryfikacja obejmuje
pełny histogram, hash, wzorzec z innej metody, wszystkie rekordy i kody,
ponowne rachunki wybranych wierszy oraz przegląd renderu PDF (D07-D09).
Nie przypisuje się tych czynności użytkownikowi ani nie deklaruje jego
samodzielnej obrony kodu. Przed oddaniem powinien umieć wyjaśnić powyższe decyzje.

Metryczkę zebrano bez nazwy konta i prywatnych ścieżek. Wersja kompilatora
zawiera wyłącznie pierwsze dwa wiersze `clang++ --version`, zgodnie z opisem
w D02; ścieżki instalacji nie zbierano. Surowych strumieni D03-D06 nie
redagowano. Nie commitowano, nie pushowano ani nie wysyłano plików zewnętrznie.

### Poziom B

W B asystent przygotował plan, automat, walidator, fixture, uszkodzoną kopię,
niezależną kontrolę oraz aktualizację raportu; wykonał kompilacje i rzeczywiste
uruchomienia. D15 dokładnie wskazuje przeliczone wiersze i statystyki.
Nie przypisuje się użytkownikowi tych kontroli ani samodzielnego napisania kodu.

D16 dotyczy aktualnego eksportu B; historyczny D09 pozostaje kontrolą eksportu A.
Sprawdzenie obejmuje linki i artefakty, hashe kopii źródeł, dane, zgodność wyników,
anonimizację oraz render każdej strony. Nie redagowano strumieni raw.
Nie commitowano, nie pushowano i nie wysyłano materiałów zewnętrznie.
