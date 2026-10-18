---
title: "TiDPI 07 - Rzetelny benchmark C++ i Python"
author: "Kryptonim TiDPI: Regulus"
date: "2026-10-17"
lang: pl-PL
---

# Sprawozdanie TiDPI 07 - rzetelny benchmark C++ i Python

## 1. Kryptonim TiDPI i wykonany poziom

Kryptonim: **Regulus**. Wykonany zakres: **A–D w opisanej adaptacji danych i narzędzi**, aktualizacja 2026-10-17.
B obejmuje dwie nowe pełne poprawne serie i osobną kontrolę błędną.
C wykonano w dwóch kontrolowanych badaniach opisanych poniżej; D obejmuje badanie harmonogramu kolejności w dwóch seriach. Operacja ma status uzgodnionej z prowadzącym na podstawie
polecenia użytkownika: ręczna suma odległości od 500.

**Jawne uzgodnienie parametrów:** zastane A miało 20 020 liczb i 200 rund,
a nie 10 000 liczb i 100 rund. Użytkownik wybrał zachowanie pliku A i 100 rund
w B. Oczekiwanie B wynosi 501 000 000; historyczne A nadal ma 1 002 000 000.
Nie porównuje się czasów A i B jako identycznych obciążeń. Użytkownik potwierdził
pięć pól dokładnego nagłówka; wzmianka o sześciu polach była rozbieżnością.

Przeczytano cały szkolny PDF (10 stron), w tym A–D, artefakty, sprawozdanie
i kryteria oceny. PDF dla A–B wymaga automatyzacji, walidatora, błędnej próby, dwóch serii,
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

### Poziom C - zakres i rozstrzygnięcie danych

Wykonano dokładnie dwa rozszerzenia: **C1 Debug/Release** i **C2 rozmiar danych**.
W poleceniu przyjęto błędnie, że A miało plik 10 000 liczb. Sprawdzony plik ma
20 020 liczb; jego generator tasuje cały multizbiór. Zmiana liczności przed tasowaniem
zmienia prefiks mimo tego samego seedu. Użytkownik wybrał zachowanie generatora:
C1 używa pierwszych 10 000 wierszy A, C2 prefiksów nowego pliku 50 000.
**To jawne, zaakceptowane odstępstwo: plik 10 000 C2 nie jest identyczny z A ani
z jego prefiksem 10 000. Nie deklaruje się spełnienia pierwotnego warunku tożsamości.**

[Plan C](rozszerzenia/C/plan_C.md) rozróżnia wymagania PDF, dokładniejsze zasady użytkownika
i decyzje projektowe. Lokalny AGENTS.md pozostaje pusty i niezmieniony.
[Audyt A–B](rozszerzenia/C/kontrole/audit_AB.json) sprawdza rzeczywiste źródła, rekordy
i rozgrzewki; jest nową kontrolą dawnych dowodów, a nie historycznym uruchomieniem.
Raport B i eksport zachowano w [archiwum B](archiwum_B/integrity.json).
Migawki B, podobnie jak A, zachowują odsyłacze względem pierwotnego katalogu zadania.

Źródła C: [C++](rozszerzenia/C/benchmark.cpp), [Python](rozszerzenia/C/benchmark.py),
[przygotowanie danych](rozszerzenia/C/prepare_C.py), [automat](rozszerzenia/C/run_C.py),
[walidator](rozszerzenia/C/validate_C.py), [niezależna kontrola](rozszerzenia/C/verify_C.py).
Eksport C: [skrypt eksportu](rozszerzenia/C/export_C.sh); z katalogu TiDPI_07:
`sh rozszerzenia/C/export_C.sh`. Rozszerza reguły istniejącego eksportu B,
aby podpisy grup nie oddzielały się od logów; historyczny skrypt pozostaje zachowany.

### Poziom D - zakres i odstępstwo danych

W D wykonano kontrolowane badanie kolejności: dwa harmonogramy, dwie serie,
80 par i 160 świeżych procesów. Operacja i status uzgodnienia z prowadzącym
pochodzą wprost z aktualnego polecenia użytkownika: ręczna suma odległości od 500,
100 rund. Nie posiadamy odrębnej korespondencji z prowadzącym.

**Rozbieżność danych:** A ma 20 020 wartości. D używa jego dokładnego prefiksu
10 000 wierszy, identycznego z C1. To jawna decyzja interpretacyjna dla D,
nie dodatkowe uzgodnienie z prowadzącym ani twierdzenie, że historyczne A
miało 10 000 liczb. Nie deklaruje się literalnej zgodności z nieistniejącym
plikiem 10 000 z A. Wcześniejsze odstępstwo C2 pozostaje opisane powyżej.

Raport i eksport C zachowano w [archiwum C](archiwum_C/raport.md) oraz
[PDF C](archiwum_C/raport.pdf); odsyłacze tych migawek odnoszą się do pierwotnego
katalogu TiDPI_07. D25–D31 i TC-21–TC-27 są nowymi identyfikatorami.

Źródła D: [C++](rozszerzenia/D/benchmark.cpp), [Python](rozszerzenia/D/benchmark.py),
[przygotowanie](rozszerzenia/D/prepare_D.py), [automat](rozszerzenia/D/run_D.py),
[walidator](rozszerzenia/D/validate_D.py), [niezależna analiza](rozszerzenia/D/analyze_D.py).
Benchmarki są niezmienionymi kopiami wersji C. Plan wymaga nowych harmonogramów,
a nie kolejnych rozszerzeń C. AGENTS.md nadal jest pusty i nie był edytowany.

## 2. Cel i hipoteza

### Poziom A — zapis historyczny

Pytanie: jakie czasy osiągną dwie ręczne implementacje tej samej sumy odległości,
gdy dane, liczba rund i granice pomiaru są wspólne? Hipoteza zapisana w D01:
obie implementacje zwrócą dokładnie wynik wzorcowy; czasy mogą się różnić,
bez wybierania zwycięzcy przed pomiarem. Celem jest poprawny rdzeń benchmarku,
a nie ustalenie uniwersalnej szybkości języków.

Niezależnie oczekiwany wynik: **1 002 000 000** po **200 rundach**.
To wynik obliczeń; odcisk SHA-256 identyfikuje bajty pliku i ma inne znaczenie.

### Poziom B — zapis historyczny

Pytanie B: czy kierunek porównania minimum i mediany dwóch implementacji
powtórzy się w dwóch osobnych seriach przy wspólnym pliku i 100 rundach?
Hipotezę bez wyboru zwycięzcy zapisano w D10 przed nowymi pomiarami.
Obie implementacje mają uzyskać **501 000 000**. Plan B nie jest przedstawiany
jako plan sprzed historycznych pomiarów A.

### Poziom C - dwa pytania i hipotezy

C1: jak zestaw flag kompilacji zmienia czas przy identycznym źródle i danych?
Hipoteza: konfiguracja może zmienić czas, zachowując identyczny checksum.
C2: jak czas zmienia się przy 10 000, 30 000 i 50 000 elementów dla każdej
implementacji przy 100 rundach? Hipoteza: wzrost jest w przybliżeniu proporcjonalny
do liczby elementów. Nie zakładano zwycięzcy. Plan D17 zapisano przed pomiarami;
wynik niezależny i odciski danych ustalono w D18.

### Poziom D - pytanie i hipoteza

Czy przy wspólnych danych i poprawnym wyniku harmonogram zmienia rozkład czasów
oraz relację median Python/C++? Hipoteza D25: harmonogram **może** zmienić oba
opisy; nie zakładano istnienia ani kierunku efektu. Brak powtarzalnej różnicy
również jest wynikiem. Analiza jest opisowa, bez progu istotności i bez wyboru
zwycięzcy z góry. D jest jednym rozszerzeniem: kontrolowanym badaniem harmonogramu;
wykres i metryczki służą temu badaniu.

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

### Poziom B — zapis historyczny

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

### Poziom C - rzeczywiste środowisko

D19–D21: jedna maszyna **Apple M4 Pro**, arm64, 24 GiB RAM,
macOS 27.0.1 (build 26A434), Apple Clang 21.0.0
(clang-2100.3.34.2), CPython 3.14.4. Wersje i kody zapytań zapisano
osobno przy każdym przebiegu. Użyto macOS/Clang zamiast Windows/Visual Studio/MSVC;
nie wykonywano kroków specyficznych dla narzędzi Windows.

C1: Debug `-std=c++17 -O0 -g`, Release `-std=c++17 -O2 -DNDEBUG`.
C2: ten sam zestaw Release. W C1 oba pliki binarne skompilowano z dokładnie
tej samej kopii C++; różnią się wyłącznie flagami. Bez debuggera i dodatkowych
flag kompilacji. Polecenia, hashe źródeł i binariów są w D19–D21.

C++ deklaruje `steady_clock`, `is_steady=1`, okres `1/1000000000` s;
Python `mach_absolute_time()`, monotoniczność i rozdzielczość około **41,67 ns**.
To metadane zegarów; jednostka `time_ns` nie dowodzi dokładności 1 ns.
Efektywnej rozdzielczości ani narzutu odczytu zegara osobno nie zmierzono.

### Poziom D - środowisko obu serii

D27 i D28 zapisują rzeczywiste zapytania i wyniki: Apple M4 Pro, arm64,
24 GiB RAM, macOS 27.0.1 (26A434), Apple Clang 21.0.0
(clang-2100.3.34.2), **CPython 3.14.4**, zgodny z A–C. To adaptacja na
macOS/arm64/Clang; nie używano Windows, Visual Studio ani MSVC.

C++ zbudowano raz: `clang++ -std=c++17 -O2 -DNDEBUG`, bez debuggera.
Seria 2 otrzymała kopię tego samego pliku binarnego; hashe obu są identyczne.
W każdym przebiegu są rzeczywiste argv, kody kompilacji/kopiowania i hashe
źródeł oraz binariów. Nie zbierano prywatnej ścieżki instalacji Clanga:
z polecenia wersji od początku przechwytywano wyłącznie pierwsze dwa wiersze.

Zegary (stderr wszystkich procesów): C++ `steady_clock`, `is_steady=1`,
nominalny okres `1/1000000000` s; Python `mach_absolute_time()`, zgłoszona
rozdzielczość około **41,667 ns**. `time_ns` to jednostka zapisu; efektywnej
rozdzielczości C++ ani dokładności eksperymentu nie zmierzono.

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

### Poziom B — zapis historyczny

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

### Poziom C - dane i kontrolowane czynniki

Tabela 3. Dane C i niezależne checksumy po **100 rundach** (D18).
Skrót SHA-256 jest odciskiem bajtów, a checksum wynikiem badanej operacji.
Pełne odciski są w manifestach, nie są skracane w walidacji.

| Badanie | Elementy | Oczekiwany checksum | Początek SHA-256 |
| ------- | -------: | ------------------: | ---------------- |
| C1      |   10 000 |         251 042 700 | `9e19f79d6545`   |
| C2      |   10 000 |         250 039 700 | `71496284c499`   |
| C2      |   30 000 |         748 157 600 | `8fd5b5c6428f`   |
| C2      |   50 000 |       1 250 122 500 | `500b7f8b59c9`   |

C1: prefiks historycznego A, jedyna zmienna - flagi kompilacji.
C2: nadrzędny plik 50 000 utworzono przez `i % 1001` i tasowanie
`random.Random(20261017).shuffle`; mniejsze pliki są jego prefiksami bajtowymi.
Zakres wartości 0–1000, ASCII i LF. Przy 50 000 liczbach histogram nie ma
jednakowej liczności każdej wartości. To tasowanie multizbioru, nie niezależne
losowanie każdej liczby. W C2 jedynym badanym czynnikiem w obrębie implementacji
jest rozmiar. Oba programy dla danego rozmiaru czytają ten sam plik.
Stałe: 100 rund, kod operacji, maszyna, zegar danej implementacji i procedura prób.

Kontrola D18 potwierdziła zgodność prefiksów 10 000/30 000 z nowym plikiem
50 000 oraz **brak zgodności** 10 000 C2 z prefiksem A. Dlatego czasów C1
Release i C2 10 000 nie łączy się mimo jednakowej liczności.

### Poziom D - czynniki i dane

Zmieniany czynnik: naprzemienny albo losowany harmonogram 20 par.
Stałe: maszyna, wspólny prefiks i jego kolejność, źródła, binarny C++ Release,
Python 3.14.4, 100 rund, 2 rozgrzewki i 1 próba w każdym procesie.
Seria jest blokiem replikacji; odwrócono kolejność harmonogramów między seriami.
Pozycja 1/2 jest dodatkowym przekrojem analizy tego samego badania.

D26: dane ASCII/LF, 10 000 liczb, zakres 0…1000. Generator źródła A:
`[i % 1001 for i in range(20020)]`, następnie
`random.Random(20261017).shuffle(values)`; D bierze pierwszych 10 000 wierszy.
Pełny odcisk prefiksu (połączyć dwa wiersze bez spacji):

```text
9e19f79d6545d7af30356b633e33183c
7dedb859ad6f9b2f40391ff5a908eb07
```

Właściwy pełny SHA-256 zapisano też w manifeście D26, bez łamania wiersza.
Odcisk danych rozpoznaje plik; checksum obliczeń to **251 042 700**.
Oba procesy każdej pary czytają tę samą kopię pliku. Walidacja odtwarza dane
A i sprawdza tożsamość prefiksu oraz odciski przed i po badaniu.

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

### Poziom B — zapis historyczny

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

### Poziom C - kryteria i niezależny wzorzec

Wzorzec przed pomiarami: dla wartości poniżej 500 obliczono
`500 × liczność − suma`, a powyżej 500 `suma − 500 × liczność`;
sumę obu części pomnożono przez 100. Nie użyto funkcji benchmarków.
Po pomiarach D23 przeliczył oczekiwania drugim algorytmem, z histogramu:
`suma(liczność[x] × abs(x − 500)) × 100`.

Badane funkcje wykonują ręczną pętlę 100 rund: różnica od 500, warunkowa zmiana
znaku i dodanie do akumulatora. C++ używa `int64_t`, Python `int`.
Maksymalnie `50000 × 500 × 100 = 2500000000`, mniej niż granica `int64_t`;
różnica mieści się w −500…500, a sumy pośrednie także są bezpieczne.
Wzorzec, liczność i parametry są walidowane poza stoperem.

Walidator C wymaga całego harmonogramu, identyczności danych i hashy źródeł,
rzeczywistych poleceń i flag, sekwencyjnego wykonania, kodów 0, nagłówka,
typów, czasów ≥0, dokładnych numerów 1–10 i dwóch rozgrzewek na proces.
Każda rozgrzewka i próba musi mieć poprawny checksum oraz `true`.
Dopiero po akceptacji całego badania powstają CSV i statystyki. Kontekst badania,
konfiguracji, rozmiaru, rund, bloku i lokalizacji raw jest dodany w pochodnym CSV;
pięciopolowy format stdout nie został zmieniony.

TC-13: integralność A–B - zgodna (D17, D23).
TC-14: wzorce i prefiksy - zgodne z przyjętym rozstrzygnięciem; tożsamość z A
nie zachodzi (D18). TC-15: C1 - zaakceptowane (D19).
TC-16: rzeczywisty błąd - odrzucony bez CSV (D20).
TC-17: C2 po błędzie - zaakceptowane (D21).
TC-18: 10 fixture walidatora - 10 zgodnych decyzji (D22).
TC-19: niezależne rachunki - zgodne (D23).
TC-20: końcowy komplet, linki, anonimizacja i render - D24.

### Poziom D - wzorzec i walidacja

Przed pomiarami D26 wyznaczył niezależnie:
`100 × (500 × 4965 − 1239730 + 3781157 − 500 × 5027)`
= `100 × 2510427` = **251042700**. Osiem wartości równych 500 wnosi zero.
To sumy i liczności partycji, bez funkcji obliczeniowych benchmarków.
D30 później potwierdził wynik z pełnego histogramu innym algorytmem.

Obie implementacje wykonują ręczne pętle: `x − 500`, warunkowa zmiana znaku,
dodanie, 100 rund. Różnica mieści się w −500…500, składnik w 0…500,
a suma i wszystkie sumy pośrednie są nie większe niż
`10000 × 500 × 100 = 500000000 < 9223372036854775807`.
C++ używa `int64_t`; iloczyny kontroli parametrów typu `long long` są bezpieczne
także dla limitu wejścia programu 50 000. Python używa `int`.

Walidator wymaga zgodności pełnego harmonogramu, równowagi pozycji,
niezmienności plików, flag, wersji, poleceń i kolejności zdarzeń bez nakładania
przedziałów monotonicznych. Wymaga kodów 0, dokładnego nagłówka,
jednego rekordu stdout z `trial=1`, całkowitych nieujemnych ns, niezależnego
checksumu i `true`. Sprawdza również obie rozgrzewki każdego procesu.
Metadane serii, harmonogramu, pary, pozycji i parametrów są w oddzielnym planie,
logu wykonania i pochodnym CSV. Kontrakt stdout nie został rozszerzony.

TC-21: nowy audyt źródeł i dowodów A–C oraz zachowanie zastanych plików — zgodne (D25, D30).
TC-22: plan i oba harmonogramy przed pomiarami, dokładne 10+10 kolejności — zgodne (D25).
TC-23: dane, wzorzec, zakres arytmetyki — zgodne (D26, D30).
TC-24: seria 1 i seria 2, każda 80 rekordów i 160 rozgrzewek — zaakceptowane (D27–D28).
TC-25: sześć kontroli walidatora — sześć zgodnych decyzji (D29).
TC-26: każdy wiersz raw/CSV, wszystkie statystyki i wybrane przeliczenia — zgodne (D30).
TC-27: komplet, linki, anonimizacja, render eksportu — wynik D31.

Kontrole D29 to oznaczone **kopie fixture**, nie dodatkowe benchmarki:
poprawna kopia oraz checksum mimo `true`, brak rekordu, zła kolejność planu,
błędna rozgrzewka i nakładające się zdarzenia. Odrzucono pięć wadliwych kopii,
bez `results.csv` ani `warmups.csv` w końcowej serii kontroli.
Pierwsza kontrola ujawniła pozostawanie odziedziczonego CSV rozgrzewek po odrzuceniu.
Poprawiono usuwanie obu plików pochodnych, zachowano stare źródło w dowodach
pierwszej kontroli i ponowiono sześć kontroli oraz walidację obu rzeczywistych serii.
Źródeł benchmarków i surowych pomiarów nie zmieniano; kopie historycznego walidatora
w przebiegach pozostają zachowane. D29 dokumentuje obie wersje i przeniesienie
starego pliku pochodnego do oznaczonego dowodu usterki.

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

### Poziom B — zapis historyczny

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

### Poziom C - wykonanie i harmonogram

1. Zarchiwizowano raport B, zapisano hashe zastanych plików. Plan i harmonogramy
   utrwalono o 11:03:47 dnia 2026-10-17 (Europe/Warsaw), przed pomiarami C.
2. Przygotowano dane i wzorce D18. D19: pięć bloków C1, w każdym proces Debug
   i Release, każdy z dwiema rozgrzewkami i dwiema próbami. Nieparzyste bloki
   zaczyna Debug, parzyste Release. Numery prób kolejno 1–2 aż do 9–10.
3. D20: uruchomiono pełny zaplanowany harmonogram C2 z osobną kopią Pythona,
   w której zmieniono `x-500` na `x-0`. Każdy wadliwy proces przerwał na pierwszej
   rozgrzewce. Zachowano także wszystkie wykonane pomiary C++, lecz całe badanie
   odrzucono i nie analizowano jego czasów.
4. D21: poprawny C2 po kontroli błędnej. Kolejności rozmiarów w blokach:
   10–30–50, 30–50–10, 50–10–30, 10–30–50, 30–50–10 (tysięcy).
   W każdym rozmiarze bloki nieparzyste zaczyna C++, parzyste Python.
   Każdy proces wykonuje dwie rozgrzewki i dwie próby. Rotacja dotyczy bloków.
5. D22–D23: fixture i niezależne przeliczenie. D24: aktualizacja raportu,
   eksport, kontrola powiązań i przegląd wyrenderowanych stron.

W poprawnym C1 wykonano **10 procesów, 20 rozgrzewek i 20 prób**; w poprawnym C2
**30 procesów, 60 rozgrzewek i 60 prób**. Na każdą grupę przypada 10 właściwych
prób i 10 rozgrzewek. To jedna zaakceptowana seria każdego badania, oddzielna
od historycznych dwóch serii B. Niczego nie uruchamiano równolegle w harmonogramie.
Nie usuwano niewygodnych czasów ani nie zastępowano ich nowymi próbami.

Pomiar: start zegara → wywołanie funkcji → stop zegara. Obejmuje inicjalizację
akumulatora i obie pętle; wyklucza uruchomienie procesu, odczyt, przygotowanie,
walidację, porównanie wyniku i wypisywanie. Obserwowalny checksum nie wyklucza
wszystkich transformacji optymalizatora; nie badano asemblera.

Pierwsza próba C1 ([niepełny przebieg](rozszerzenia/C/C1/przebiegi/20261017_110356_248419_good/runner_result.json))
zatrzymała się na odmowie `sysctl` przez piaskownicę: bez kompilacji i pomiarów.
Późniejsza kontrola odrzuciła niekompletny zbiór. Po dopuszczeniu wykonania poza
piaskownicą powstał nowy D19. Niepełnych strumieni nie poprawiano.

Odtworzenie, z katalogu `rozszerzenia/C`, po przygotowaniu danych:

```sh
python3 run_C.py C1
python3 run_C.py C2 --fault
python3 run_C.py C2
python3 test_C.py C2/przebiegi/ID_POPRAWNEGO_PRZEBIEGU
python3 verify_C.py
```

`ID_POPRAWNEGO_PRZEBIEGU` zastępuje się nazwą wypisaną przez automat.
`prepare_C.py` odtwarza dane w świeżym zestawie i chroni istniejące dowody przed
nadpisaniem. `verify_C.py` jest kontrolą tego zestawu: oczekuje po jednym
zaakceptowanym przebiegu każdego badania; kolejne powtórzenia analizuje się osobno.

### Poziom D - wykonana procedura

1. Zbadano podstawy A–C, zapisano ich manifest i migawkę raportu C.
   Zapisano plan D25, dane D26, oba harmonogramy i pełne metadane 160 procesów.
   `prepared_at=2026-10-17T11:27:57.547968+02:00`; nie jest to deklaracja
   o powstaniu planów przed dawnymi pomiarami A–C.
2. Pierwsze przygotowanie `rozszerzenia/D/przebiegi/20261017_112757_745453`
   zatrzymało się na zablokowanym `sysctl`, **przed kompilacją i pomiarami**.
   Zachowano strumienie i kod. Po zgodzie wykonano nowy pełny przebieg poza piaskownicą.
3. Seria 1: naprzemienny, potem losowany. Seria 2: losowany, potem naprzemienny.
   Każdy harmonogram ma 20 par. Naprzemienny zaczyna C++/Python; następna para
   Python/C++. Losowany jest tasowaniem listy dziesięciu par każdego rodzaju
   przez `random.Random(20260402).shuffle()`. W obu seriach użyto tego samego
   utrwalonego losowania. Rotacja dotyczy par, odwrócenie harmonogramów — serii.
4. Para oznacza dwa osobne procesy uruchomione kolejno. Każdy czyta plik,
   wykonuje 2 rozgrzewki i 1 próbę; start nowego procesu dla następnej implementacji.
   Nie stosowano celowych przerw, odrzucania skrajnych czasów ani powtórzeń zastępujących.
5. Stoper obejmuje wywołanie `calculate(values)` i jego pętle. Odczyt, importy,
   przygotowanie, walidacja, wypisywanie oraz start/koniec procesu są poza pomiarem.
   Wynik jest obserwowalny i sprawdzany, co nie wyklucza przekształceń optymalizatora.
6. Najpierw zwalidowano obie kompletne serie. Potem D30 osobno odczytał raw,
   przeliczył histogram i statystyki, przygotował CSV wykresu i wykres PGFPlots.
   Wykonano kontrole D29, poprawkę publikacji i ponowną walidację bez nowych pomiarów.
   Uzupełniono wspólny raport i eksport oraz sprawdzono render (D31).

Odtworzenie nowego przebiegu z katalogu `rozszerzenia/D`: `python3 run_D.py`.
Istniejący plan jest niezmienny; `prepare_D.py` odmawia jego nadpisania.
Po nowym przebiegu: `python3 analyze_D.py`, `python3 test_D.py`.
Eksport raportu z katalogu TiDPI_07: `sh rozszerzenia/D/export_D.sh`.
Pełny automat zapisuje osobne katalogi; nie należy nakładać uruchomień benchmarków.

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

### Poziom B — zapis historyczny

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

### Poziom C - rejestr dowodów

- **D17** - Plan i zachowanie podstaw: [plan](rozszerzenia/C/plan_C.md), [czas i hashe planu](rozszerzenia/C/prepared.json), [audyt A–B](rozszerzenia/C/kontrole/audit_AB.json), [manifest zastanych plików](rozszerzenia/C/preexisting_sha256.json).
- **D18** - Dane i niezależne oczekiwania: [manifest C1](rozszerzenia/C/C1/data_manifest.json), [manifest C2](rozszerzenia/C/C2/data_manifest.json), [porównanie prefiksów](rozszerzenia/C/prefix_check.json).
- **D19** - Poprawny C1: [metryczka](rozszerzenia/C/C1/przebiegi/20261017_110944_353315_good/environment.json), [harmonogram](rozszerzenia/C/C1/przebiegi/20261017_110944_353315_good/schedule.json), [polecenia](rozszerzenia/C/C1/przebiegi/20261017_110944_353315_good/commands.txt), [kody](rozszerzenia/C/C1/przebiegi/20261017_110944_353315_good/exit_codes.txt), [walidacja](rozszerzenia/C/C1/przebiegi/20261017_110944_353315_good/validation.json), [CSV](rozszerzenia/C/C1/przebiegi/20261017_110944_353315_good/results.csv).
- **D20** - Rzeczywista kontrola błędna: [zmieniony Python](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/sources/benchmark.py), [metryczka](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/environment.json), [harmonogram](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/schedule.json), [polecenia](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/commands.txt), [kody](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/exit_codes.txt), [odrzucenie](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/validation.json).
- **D21** - Poprawny C2 po błędzie: [metryczka](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/environment.json), [harmonogram](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/schedule.json), [polecenia](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/commands.txt), [kody](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/exit_codes.txt), [walidacja](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/validation.json), [CSV](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/results.csv).
- **D22** - Testy walidatora: [10 przypadków](rozszerzenia/C/kontrole/validator_2026-10-17T111130.812999_0200/summary.json), [źródło testów](rozszerzenia/C/test_C.py).
- **D23** - Niezależna kontrola: [rachunki](rozszerzenia/C/kontrole/independent_check.json), [źródło](rozszerzenia/C/verify_C.py).
- **D24** - Kontrola końcowa: [wynik](rozszerzenia/C/kontrole/final_check.json), [weryfikator](rozszerzenia/C/check_C.py).

W każdym przebiegu pliki `bB_N_W_stdout.txt` i `bB_N_W_stderr.txt` są pełnymi,
niezmienionymi strumieniami procesu: B to blok, N to liczność, W to wariant.
`execution.json` zapisuje kolejność i czasy, `sources` zawiera dokładne wersje
źródeł, `source_sha256.json` ich hashe, `data` kopie wspólnych wejść.

Poniżej bezpośrednie odsyłacze do wszystkich strumieni benchmarków; każdy wpis
obejmuje stdout i stderr, także w odrzuconym D20.

- D19 `b1_10000_Debug`: [stdout](rozszerzenia/C/C1/przebiegi/20261017_110944_353315_good/b1_10000_Debug_stdout.txt), [stderr](rozszerzenia/C/C1/przebiegi/20261017_110944_353315_good/b1_10000_Debug_stderr.txt).
- D19 `b1_10000_Release`: [stdout](rozszerzenia/C/C1/przebiegi/20261017_110944_353315_good/b1_10000_Release_stdout.txt), [stderr](rozszerzenia/C/C1/przebiegi/20261017_110944_353315_good/b1_10000_Release_stderr.txt).
- D19 `b2_10000_Release`: [stdout](rozszerzenia/C/C1/przebiegi/20261017_110944_353315_good/b2_10000_Release_stdout.txt), [stderr](rozszerzenia/C/C1/przebiegi/20261017_110944_353315_good/b2_10000_Release_stderr.txt).
- D19 `b2_10000_Debug`: [stdout](rozszerzenia/C/C1/przebiegi/20261017_110944_353315_good/b2_10000_Debug_stdout.txt), [stderr](rozszerzenia/C/C1/przebiegi/20261017_110944_353315_good/b2_10000_Debug_stderr.txt).
- D19 `b3_10000_Debug`: [stdout](rozszerzenia/C/C1/przebiegi/20261017_110944_353315_good/b3_10000_Debug_stdout.txt), [stderr](rozszerzenia/C/C1/przebiegi/20261017_110944_353315_good/b3_10000_Debug_stderr.txt).
- D19 `b3_10000_Release`: [stdout](rozszerzenia/C/C1/przebiegi/20261017_110944_353315_good/b3_10000_Release_stdout.txt), [stderr](rozszerzenia/C/C1/przebiegi/20261017_110944_353315_good/b3_10000_Release_stderr.txt).
- D19 `b4_10000_Release`: [stdout](rozszerzenia/C/C1/przebiegi/20261017_110944_353315_good/b4_10000_Release_stdout.txt), [stderr](rozszerzenia/C/C1/przebiegi/20261017_110944_353315_good/b4_10000_Release_stderr.txt).
- D19 `b4_10000_Debug`: [stdout](rozszerzenia/C/C1/przebiegi/20261017_110944_353315_good/b4_10000_Debug_stdout.txt), [stderr](rozszerzenia/C/C1/przebiegi/20261017_110944_353315_good/b4_10000_Debug_stderr.txt).
- D19 `b5_10000_Debug`: [stdout](rozszerzenia/C/C1/przebiegi/20261017_110944_353315_good/b5_10000_Debug_stdout.txt), [stderr](rozszerzenia/C/C1/przebiegi/20261017_110944_353315_good/b5_10000_Debug_stderr.txt).
- D19 `b5_10000_Release`: [stdout](rozszerzenia/C/C1/przebiegi/20261017_110944_353315_good/b5_10000_Release_stdout.txt), [stderr](rozszerzenia/C/C1/przebiegi/20261017_110944_353315_good/b5_10000_Release_stderr.txt).
- D20 `b1_10000_cpp`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b1_10000_cpp_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b1_10000_cpp_stderr.txt).
- D20 `b1_10000_python`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b1_10000_python_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b1_10000_python_stderr.txt).
- D20 `b1_30000_cpp`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b1_30000_cpp_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b1_30000_cpp_stderr.txt).
- D20 `b1_30000_python`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b1_30000_python_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b1_30000_python_stderr.txt).
- D20 `b1_50000_cpp`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b1_50000_cpp_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b1_50000_cpp_stderr.txt).
- D20 `b1_50000_python`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b1_50000_python_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b1_50000_python_stderr.txt).
- D20 `b2_30000_python`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b2_30000_python_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b2_30000_python_stderr.txt).
- D20 `b2_30000_cpp`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b2_30000_cpp_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b2_30000_cpp_stderr.txt).
- D20 `b2_50000_python`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b2_50000_python_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b2_50000_python_stderr.txt).
- D20 `b2_50000_cpp`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b2_50000_cpp_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b2_50000_cpp_stderr.txt).
- D20 `b2_10000_python`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b2_10000_python_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b2_10000_python_stderr.txt).
- D20 `b2_10000_cpp`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b2_10000_cpp_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b2_10000_cpp_stderr.txt).
- D20 `b3_50000_cpp`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b3_50000_cpp_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b3_50000_cpp_stderr.txt).
- D20 `b3_50000_python`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b3_50000_python_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b3_50000_python_stderr.txt).
- D20 `b3_10000_cpp`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b3_10000_cpp_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b3_10000_cpp_stderr.txt).
- D20 `b3_10000_python`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b3_10000_python_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b3_10000_python_stderr.txt).
- D20 `b3_30000_cpp`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b3_30000_cpp_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b3_30000_cpp_stderr.txt).
- D20 `b3_30000_python`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b3_30000_python_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b3_30000_python_stderr.txt).
- D20 `b4_10000_python`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b4_10000_python_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b4_10000_python_stderr.txt).
- D20 `b4_10000_cpp`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b4_10000_cpp_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b4_10000_cpp_stderr.txt).
- D20 `b4_30000_python`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b4_30000_python_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b4_30000_python_stderr.txt).
- D20 `b4_30000_cpp`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b4_30000_cpp_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b4_30000_cpp_stderr.txt).
- D20 `b4_50000_python`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b4_50000_python_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b4_50000_python_stderr.txt).
- D20 `b4_50000_cpp`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b4_50000_cpp_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b4_50000_cpp_stderr.txt).
- D20 `b5_30000_cpp`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b5_30000_cpp_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b5_30000_cpp_stderr.txt).
- D20 `b5_30000_python`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b5_30000_python_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b5_30000_python_stderr.txt).
- D20 `b5_50000_cpp`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b5_50000_cpp_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b5_50000_cpp_stderr.txt).
- D20 `b5_50000_python`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b5_50000_python_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b5_50000_python_stderr.txt).
- D20 `b5_10000_cpp`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b5_10000_cpp_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b5_10000_cpp_stderr.txt).
- D20 `b5_10000_python`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b5_10000_python_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111029_701722_fault/b5_10000_python_stderr.txt).
- D21 `b1_10000_cpp`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b1_10000_cpp_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b1_10000_cpp_stderr.txt).
- D21 `b1_10000_python`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b1_10000_python_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b1_10000_python_stderr.txt).
- D21 `b1_30000_cpp`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b1_30000_cpp_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b1_30000_cpp_stderr.txt).
- D21 `b1_30000_python`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b1_30000_python_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b1_30000_python_stderr.txt).
- D21 `b1_50000_cpp`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b1_50000_cpp_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b1_50000_cpp_stderr.txt).
- D21 `b1_50000_python`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b1_50000_python_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b1_50000_python_stderr.txt).
- D21 `b2_30000_python`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b2_30000_python_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b2_30000_python_stderr.txt).
- D21 `b2_30000_cpp`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b2_30000_cpp_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b2_30000_cpp_stderr.txt).
- D21 `b2_50000_python`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b2_50000_python_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b2_50000_python_stderr.txt).
- D21 `b2_50000_cpp`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b2_50000_cpp_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b2_50000_cpp_stderr.txt).
- D21 `b2_10000_python`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b2_10000_python_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b2_10000_python_stderr.txt).
- D21 `b2_10000_cpp`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b2_10000_cpp_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b2_10000_cpp_stderr.txt).
- D21 `b3_50000_cpp`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b3_50000_cpp_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b3_50000_cpp_stderr.txt).
- D21 `b3_50000_python`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b3_50000_python_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b3_50000_python_stderr.txt).
- D21 `b3_10000_cpp`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b3_10000_cpp_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b3_10000_cpp_stderr.txt).
- D21 `b3_10000_python`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b3_10000_python_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b3_10000_python_stderr.txt).
- D21 `b3_30000_cpp`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b3_30000_cpp_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b3_30000_cpp_stderr.txt).
- D21 `b3_30000_python`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b3_30000_python_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b3_30000_python_stderr.txt).
- D21 `b4_10000_python`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b4_10000_python_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b4_10000_python_stderr.txt).
- D21 `b4_10000_cpp`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b4_10000_cpp_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b4_10000_cpp_stderr.txt).
- D21 `b4_30000_python`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b4_30000_python_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b4_30000_python_stderr.txt).
- D21 `b4_30000_cpp`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b4_30000_cpp_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b4_30000_cpp_stderr.txt).
- D21 `b4_50000_python`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b4_50000_python_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b4_50000_python_stderr.txt).
- D21 `b4_50000_cpp`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b4_50000_cpp_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b4_50000_cpp_stderr.txt).
- D21 `b5_30000_cpp`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b5_30000_cpp_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b5_30000_cpp_stderr.txt).
- D21 `b5_30000_python`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b5_30000_python_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b5_30000_python_stderr.txt).
- D21 `b5_50000_cpp`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b5_50000_cpp_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b5_50000_cpp_stderr.txt).
- D21 `b5_50000_python`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b5_50000_python_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b5_50000_python_stderr.txt).
- D21 `b5_10000_cpp`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b5_10000_cpp_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b5_10000_cpp_stderr.txt).
- D21 `b5_10000_python`: [stdout](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b5_10000_python_stdout.txt), [stderr](rozszerzenia/C/C2/przebiegi/20261017_111039_385982_good/b5_10000_python_stderr.txt).

### Poziom C - komplet właściwych rekordów zaakceptowanych serii

Poniższe bloki to agregacje pełnych rekordów stdout, rozdzielone według badania,
konfiguracji i rozmiaru; pierwotne strumienie z własnymi nagłówkami są w D19/D21.
Rozgrzewki pozostają oddzielnie w stderr.

**C1, Debug, 10000 elementów, cpp, 100 rund:**

```text
language;trial;time_ns;checksum;correct
cpp;1;10899417;251042700;true
cpp;2;9806583;251042700;true
cpp;3;9198291;251042700;true
cpp;4;9106500;251042700;true
cpp;5;7857916;251042700;true
cpp;6;8072333;251042700;true
cpp;7;8182375;251042700;true
cpp;8;7706292;251042700;true
cpp;9;7253959;251042700;true
cpp;10;7628917;251042700;true
```

**C1, Release, 10000 elementów, cpp, 100 rund:**

```text
language;trial;time_ns;checksum;correct
cpp;1;365083;251042700;true
cpp;2;356792;251042700;true
cpp;3;291958;251042700;true
cpp;4;279625;251042700;true
cpp;5;167750;251042700;true
cpp;6;167542;251042700;true
cpp;7;149000;251042700;true
cpp;8;150041;251042700;true
cpp;9;169417;251042700;true
cpp;10;184042;251042700;true
```

**C2, CPython, 10000 elementów, python, 100 rund:**

```text
language;trial;time_ns;checksum;correct
python;1;27792917;250039700;true
python;2;27906459;250039700;true
python;3;35362166;250039700;true
python;4;34936333;250039700;true
python;5;28126125;250039700;true
python;6;27582875;250039700;true
python;7;34426083;250039700;true
python;8;34716416;250039700;true
python;9;29058042;250039700;true
python;10;39755250;250039700;true
```

**C2, CPython, 30000 elementów, python, 100 rund:**

```text
language;trial;time_ns;checksum;correct
python;1;105892250;748157600;true
python;2;106783875;748157600;true
python;3;83214167;748157600;true
python;4;83409458;748157600;true
python;5;83147375;748157600;true
python;6;98458542;748157600;true
python;7;111272375;748157600;true
python;8;95245333;748157600;true
python;9;84061458;748157600;true
python;10;85746541;748157600;true
```

**C2, CPython, 50000 elementów, python, 100 rund:**

```text
language;trial;time_ns;checksum;correct
python;1;145687417;1250122500;true
python;2;146225375;1250122500;true
python;3;142522958;1250122500;true
python;4;142815458;1250122500;true
python;5;148166834;1250122500;true
python;6;144019583;1250122500;true
python;7;141958000;1250122500;true
python;8;143600042;1250122500;true
python;9;185816708;1250122500;true
python;10;178493208;1250122500;true
```

**C2, Release, 10000 elementów, cpp, 100 rund:**

```text
language;trial;time_ns;checksum;correct
cpp;1;148916;250039700;true
cpp;2;148917;250039700;true
cpp;3;170709;250039700;true
cpp;4;170792;250039700;true
cpp;5;149042;250039700;true
cpp;6;151750;250039700;true
cpp;7;161625;250039700;true
cpp;8;149042;250039700;true
cpp;9;202334;250039700;true
cpp;10;474084;250039700;true
```

**C2, Release, 30000 elementów, cpp, 100 rund:**

```text
language;trial;time_ns;checksum;correct
cpp;1;509708;748157600;true
cpp;2;532709;748157600;true
cpp;3;446792;748157600;true
cpp;4;446750;748157600;true
cpp;5;475542;748157600;true
cpp;6;446792;748157600;true
cpp;7;512875;748157600;true
cpp;8;512834;748157600;true
cpp;9;500666;748157600;true
cpp;10;489917;748157600;true
```

**C2, Release, 50000 elementów, cpp, 100 rund:**

```text
language;trial;time_ns;checksum;correct
cpp;1;778250;1250122500;true
cpp;2;777416;1250122500;true
cpp;3;842708;1250122500;true
cpp;4;825500;1250122500;true
cpp;5;856292;1250122500;true
cpp;6;852834;1250122500;true
cpp;7;792292;1250122500;true
cpp;8;746375;1250122500;true
cpp;9;776250;1250122500;true
cpp;10;803500;1250122500;true
```

### Poziom C - kontrola ujemna i fixture

D20: rzeczywisty fragment stderr pierwszego wadliwego procesu Pythona:

```text
warmup=1;time_ns=35027208;checksum=503213100;correct=false
```

Dla 10 000 C2 oczekiwano 250039700, więc kod procesu wynosi 1, a walidator
odrzucił cały zbiór bez CSV i statystyk. Oryginalny Python pozostał poprawny;
D21 potwierdza zgodność jego hashy i działanie po błędzie. D23 sprawdza także,
że uszkodzony wariant różni się właśnie środkiem obliczenia.

D22 obejmuje komplet poprawny oraz odrzucenia: checksum przy `true`, brak próby,
duplikat próby, zła liczność w manifeście, złe flagi, brak rozgrzewki, jednostka
`time_us`, zmieniony harmonogram i niezerowy kod procesu. Wynik: **10 zgodnych,
0 niezgodnych decyzji**. Dziewięć odrzuconych fixture miało wcześniej poprawny
CSV; po odrzuceniu plik nie istnieje. Są to oznaczone kopie testowe, a nie
kolejne pomiary wydajności.

### Poziom D - rejestr dowodów i pełne strumienie

- **D25** — [plan D](rozszerzenia/D/plan_D.md), [czas i hashe przygotowania](rozszerzenia/D/prepared.json), [oba harmonogramy](rozszerzenia/D/schedules.json), [metadane wszystkich zaplanowanych procesów](rozszerzenia/D/planned_trials.json), [manifest zastanych plików](rozszerzenia/D/preexisting_sha256.json), [przerwane przygotowanie](rozszerzenia/D/przebiegi/20261017_112757_745453/seria_1/exit_codes.txt).
- **D26** — [dane 10 000](rozszerzenia/D/data/input_10000.txt), [generator, pochodzenie, SHA-256 i wzorzec](rozszerzenia/D/data_manifest.json).
- **D27** — seria 1: [metryczka](rozszerzenia/D/przebiegi/20261017_113308_338673/seria_1/environment.json), [kolejność](rozszerzenia/D/przebiegi/20261017_113308_338673/seria_1/schedule.json), [polecenia](rozszerzenia/D/przebiegi/20261017_113308_338673/seria_1/commands.json), [czasy wykonania procesów](rozszerzenia/D/przebiegi/20261017_113308_338673/seria_1/execution.json), [kody](rozszerzenia/D/przebiegi/20261017_113308_338673/seria_1/exit_codes.txt), [walidacja](rozszerzenia/D/przebiegi/20261017_113308_338673/seria_1/validation.json), [zaakceptowane pomiary](rozszerzenia/D/przebiegi/20261017_113308_338673/seria_1/results.csv), [rozgrzewki osobno](rozszerzenia/D/przebiegi/20261017_113308_338673/seria_1/warmups.csv).
- **D28** — seria 2: [metryczka](rozszerzenia/D/przebiegi/20261017_113308_338673/seria_2/environment.json), [kolejność](rozszerzenia/D/przebiegi/20261017_113308_338673/seria_2/schedule.json), [polecenia](rozszerzenia/D/przebiegi/20261017_113308_338673/seria_2/commands.json), [czasy wykonania procesów](rozszerzenia/D/przebiegi/20261017_113308_338673/seria_2/execution.json), [kody](rozszerzenia/D/przebiegi/20261017_113308_338673/seria_2/exit_codes.txt), [walidacja](rozszerzenia/D/przebiegi/20261017_113308_338673/seria_2/validation.json), [zaakceptowane pomiary](rozszerzenia/D/przebiegi/20261017_113308_338673/seria_2/results.csv), [rozgrzewki osobno](rozszerzenia/D/przebiegi/20261017_113308_338673/seria_2/warmups.csv).
- **D29** — [końcowe 6 kontroli walidatora](rozszerzenia/D/kontrole/validator_2026-10-17T113500.997614+0200/summary.json), [źródło kontroli](rozszerzenia/D/test_D.py), [rejestr poprawki sprzątania CSV](rozszerzenia/D/kontrole/cleanup_fix.json).
- **D30** — [niezależny audyt i rachunki](rozszerzenia/D/analysis/independent_check.json), [statystyki wszystkich przekrojów](rozszerzenia/D/analysis/stats.json), [160 źródłowych punktów wykresu](rozszerzenia/D/analysis/plot_data.csv), [źródło PGFPlots](rozszerzenia/D/analysis/distribution.tex), [skrypt analizy](rozszerzenia/D/analyze_D.py).
- **D31** — [kontrola końcowa](rozszerzenia/D/kontrole/final_check.json), [weryfikator artefaktów](rozszerzenia/D/check_D.py), [manifest plików do oddania](rozszerzenia/D/submission_files.txt).

Pełne, niezmienione stdout i stderr są zachowane osobno dla każdego procesu,
np. pierwszy stdout C++ serii 1:

```text
naprzemienny_p01_1_cpp_stdout.txt
```

i odpowiadający `stderr.txt`.
Jest 160 par takich plików w D27–D28; puste strumienie narzędzi również zachowano.
Nazwa zawiera harmonogram, parę, pozycję i implementację. `commands.json` i
`execution.json` stanowią pełny indeks. CSV wskazuje dokładny plik i numer wiersza.
Wszystkie właściwe rekordy mają lokalny `trial=1`; tożsamość pomiaru wyznaczają
łącznie seria, harmonogram, para, pozycja i implementacja, nie samo `trial`.
Rozgrzewki pozostają w stderr i osobnym pochodnym `warmups.csv`.

W raporcie nie powiela się 160 pełnych wierszy; komplet znajduje się w linkowanych
strumieniach i CSV. Poniżej wyłącznie **fragment**, pierwsza para D27:

```text
language;trial;time_ns;checksum;correct
cpp;1;877917;251042700;true
language;trial;time_ns;checksum;correct
python;1;141995750;251042700;true
```

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

### Poziom B — zapis historyczny

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

### Poziom C - statystyki osobnych grup

Tabela 4. Jednostka **ms**, po 10 właściwych prób w każdej grupie; D19/D21,
niezależne przeliczenie D23. Nie łączono badań ani rozmiarów.

| Badanie | Konfiguracja | Elementy |   Minimum |   Maksimum |   Rozstęp |    Mediana |
| ------- | ------------ | -------: | --------: | ---------: | --------: | ---------: |
| C1      | Debug        |    10000 |  7,253959 |  10,899417 |  3,645458 |   8,127354 |
| C1      | Release      |    10000 |     0,149 |   0,365083 |  0,216083 |  0,1767295 |
| C2      | CPython      |    10000 | 27,582875 |   39,75525 | 12,172375 | 31,7420625 |
| C2      | CPython      |    30000 | 83,147375 | 111,272375 |    28,125 |  90,495937 |
| C2      | CPython      |    50000 |   141,958 | 185,816708 | 43,858708 |   144,8535 |
| C2      | Release      |    10000 |  0,148916 |   0,474084 |  0,325168 |  0,1566875 |
| C2      | Release      |    30000 |   0,44675 |   0,532709 |  0,085959 |  0,4952915 |
| C2      | Release      |    50000 |  0,746375 |   0,856292 |  0,109917 |   0,797896 |

C1: iloraz median Debug/Release = **45,99** (D19, D23).

Tabela 5. C2: stosunek median do 10 000 oraz mediana podzielona przez
liczbę elementów, w ns/element dla całej próby obejmującej 100 rund (D21, D23).

| Implementacja | Elementy | Mediana / mediana 10 000 | ns/element |
| ------------- | -------: | -----------------------: | ---------: |
| cpp           |    10000 |                        1 |     15,669 |
| cpp           |    30000 |                    3,161 |      16,51 |
| cpp           |    50000 |                    5,092 |     15,958 |
| python        |    10000 |                        1 |   3174,206 |
| python        |    30000 |                    2,851 |   3016,531 |
| python        |    50000 |                    4,563 |    2897,07 |

Ilorazy w Tabeli 5 i ns/element zaokrąglono do trzech miejsc; Tabela 4 zachowuje
wartości wynikające z ns, w tym połówki ns median.
D23 ponownie odczytał wszystkie surowe wiersze i porównał je z CSV, przeliczył
wszystkie minima, maksima, rozstępy i mediany. Osobno zapisał wiersze **1 i 10**
każdej z ośmiu grup wraz z przeliczeniem ns→ms oraz pary pozycji 5/6.
Przykład C1 Debug: `(8072333 + 8182375) / 2 = 8127354 ns`;
Release: `(169417 + 184042) / 2 = 176729,5 ns`.
Minimum opisuje najkrótszą zaobserwowaną próbę, mediana środkowy poziom serii;
żadna z tych miar nie jest gwarancją czasu bez zakłóceń.

### Poziom D - rozkłady i rachunki

Nie połączono serii, harmonogramów ani implementacji w jedną statystykę.
N = naprzemienny, L = losowany; S1/S2 = seria; Py = Python. Tabele 6–8 i wykres D30
pochodzą wyłącznie ze 160 zaakceptowanych prób właściwych, bez rozgrzewek.

Tabela 6. D: **ms**, 20 pomiarów w każdej grupie; źródła D27–D28, kontrola D30.

| Seria | Układ | Program |    Minimum |   Maksimum |   Rozstęp |     Mediana |
| ----- | ----- | ------- | ---------: | ---------: | --------: | ----------: |
| 1     | N     | C++     |    0,34025 |      1,093 |   0,75275 |   0,7380835 |
| 1     | N     | Py      | 136,733334 |  232,41625 | 95,682916 | 159,1611455 |
| 1     | L     | C++     |   0,363083 |   1,095167 |  0,732084 |       0,863 |
| 1     | L     | Py      | 132,766667 | 207,682667 |    74,916 | 177,4218335 |
| 2     | N     | C++     |   0,340542 |   2,162875 |  1,822333 |    0,896125 |
| 2     | N     | Py      | 137,319459 | 223,725042 | 86,405583 | 176,8170415 |
| 2     | L     | C++     |   0,338875 |      1,233 |  0,894125 |    0,903375 |
| 2     | L     | Py      |    153,106 | 190,496458 | 37,390458 | 179,5984995 |

Tabela 7. D: pozycje w parze, **ms**, po 10 pomiarów; D30.

| Grupa   | Poz. |    Minimum |   Maksimum |   Rozstęp |     Mediana |
| ------- | ---- | ---------: | ---------: | --------: | ----------: |
| 1/N/C++ | 1    |    0,34025 |   1,003459 |  0,663209 |   0,5911875 |
| 1/N/C++ | 2    |   0,340375 |      1,093 |  0,752625 |   0,8577505 |
| 1/N/Py  | 1    | 136,733334 | 191,256792 | 54,523458 | 155,3951245 |
| 1/N/Py  | 2    |  141,99575 |  232,41625 |   90,4205 |  168,302667 |
| 1/L/C++ | 1    |   0,363083 |   1,034625 |  0,671542 |    0,659125 |
| 1/L/C++ | 2    |   0,444334 |   1,095167 |  0,650833 |    0,906729 |
| 1/L/Py  | 1    | 157,909167 | 207,682667 |   49,7735 |  176,410646 |
| 1/L/Py  | 2    | 132,766667 | 200,448416 | 67,681749 |  178,603625 |
| 2/N/C++ | 1    |   0,353167 |   2,162875 |  1,809708 |    0,900354 |
| 2/N/C++ | 2    |   0,340542 |   1,715292 |   1,37475 |   0,7722085 |
| 2/N/Py  | 1    | 137,319459 | 188,358375 | 51,038916 |  174,324604 |
| 2/N/Py  | 2    | 155,200792 | 223,725042 |  68,52425 |  181,033708 |
| 2/L/C++ | 1    |   0,389458 |      1,233 |  0,843542 |    0,924604 |
| 2/L/C++ | 2    |   0,338875 |   1,152834 |  0,813959 |    0,902625 |
| 2/L/Py  | 1    | 154,427333 | 190,496458 | 36,069125 | 177,5390625 |
| 2/L/Py  | 2    |    153,106 |   187,1345 |   34,0285 | 180,3641455 |

Tabela 8. D: iloraz median **Python/C++** i mediany pozycji **2/1**, bez jednostki; D30.

| Seria / układ | Python/C++ | C++ poz. 2/1 | Python poz. 2/1 |
| ------------- | ---------: | -----------: | --------------: |
| 1 / N         |    215,641 |        1,451 |           1,083 |
| 1 / L         |    205,587 |        1,376 |           1,012 |
| 2 / L         |    198,808 |        0,976 |           1,016 |
| 2 / N         |    197,313 |        0,858 |           1,038 |

Mediana dla 20 prób jest średnią 10. i 11. czasu po sortowaniu,
a dla 10 prób — 5. i 6. Na przykład D27/N/C++:
`(631333 + 844834) / 2 = 738083,5 ns`
= 0,7380835 ms; rozstęp
`1093000 − 340250 = 752750 ns`.
Minimum to najlepszy zaobserwowany czas, podatny na korzystny przypadek;
mediana opisuje środek tej próby i nie wskazuje jej mechanizmu ani gwarantowanego czasu.

D30 przeliczył niezależnie wszystkie 8 grup i 16 przekrojów pozycji,
porównał każdy surowy rekord z CSV i checksumem histogramowym.
Dodatkowo zapisał dokładne surowe wiersze par **1 i 20**, obu harmonogramów,
obu serii i obu implementacji, oraz ich przeliczenia ns na ms (16 wierszy).
Nie przypisuje się tej kontroli ręcznej pracy użytkownika.

![D30: wszystkie 160 właściwych pomiarów. N - naprzemienny, L - losowany; S1/S2 - serie. Kolor i kształt oznaczają pozycję w parze; czarna kreska to mediana 20 pomiarów. Rozsunięcie poziome według numeru pary służy widoczności punktów. Skale pionowe paneli są różne.](images/D_distribution.png){width=100%}

Dane wykresu: [CSV z każdym punktem](rozszerzenia/D/analysis/plot_data.csv).
Oś pozioma zachowuje faktyczną kolejność bloków, a wszystkie punkty mają
osobne współrzędne poziome. Nie usuwano obserwacji skrajnych.

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

### Poziom B — zapis historyczny

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

### Poziom C - obserwacje i granice interpretacji

**C1, obserwacja:** przy wspólnym prefiksie A, 100 rundach i identycznym źródle
Release miał niższą medianę niż Debug; iloraz median wyniósł 45,99.
Wszystkie wyniki obliczeń pozostały identyczne. Jest to wynik dwóch zestawów
flag w tym eksperymencie; nie rozdziela wpływu poszczególnych flag ani mechanizmów
optymalizatora. Nie badano asemblera, cache ani temperatury.

**C2, obserwacja:** mediany rosną dla obu implementacji wraz z licznością.
Dla trzykrotnego i pięciokrotnego rozmiaru stosunki wyniosły odpowiednio
3,161 i 5,092 dla C++ oraz
2,851 i 4,563 dla Pythona.
To jest zgodne z przybliżonym wzrostem proporcjonalnym w tych trzech punktach,
lecz nie dowodzi dokładnej liniowości. Nie wyznaczano przedziałów ufności ani
progu testu hipotezy. Wahania czasu na element i rozstępy pozostają widoczne;
nie usuwano skrajnych czasów. Przyczyn odchyleń nie zidentyfikowano.

Wnioski dotyczą konkretnych implementacji, danych, kompilatora i interpretera
na tej maszynie. Nie są twierdzeniem o uniwersalnej szybkości języków.

### Poziom D - obserwacje bez przypisywania przyczyn

**Obserwacja:** w serii 1 losowany układ ma medianę większą od naprzemiennego
o 16,92% dla C++ i 11,47% dla Pythona. W serii 2 różnice wynoszą
odpowiednio 0,81% i 1,57%. Kierunek dla Pythona odwrócił się, a skala
różnic obu implementacji między harmonogramami zmalała. Wykres pokazuje
szerokie nakładanie się zakresów i rozrzut, szczególnie w C++.

Iloraz median Python/C++ wynosi w S1: N **215,641**, L **205,587**;
w S2: L **198,808**, N **197,313**. Sposób ułożenia pomiarów współwystępuje
więc z innymi wartościami statystyk, lecz różnica relacji nie zachowuje kierunku
po odwróceniu bloków. Nie wykazano stałej wielkości efektu harmonogramu.

**Pozycja:** C++ ma ilorazy median 2/1: **1,451** i **1,376** w S1,
ale **0,976** i **0,858** w S2 (kolejność bloków jak w Tabeli 8).
Nie ma stabilnej przewagi pierwszej lub drugiej pozycji C++.
Python ma mediany pozycji 2 większe o około **1,24–8,31%** w czterech grupach,
lecz przy tylko 10 obserwacjach na pozycję i nakładających się rozkładach
nie jest to dowód mechanizmu ani uniwersalnego efektu.

**Wniosek opisowy:** wyniki są zgodne z możliwością zmiany obserwowanych rozkładów,
jednak dwie serie nie rozdzielają przekonująco wpływu harmonogramu od trendu
w czasie i zakłóceń. Nie ma podstaw do kategorycznego potwierdzenia przyczynowej
hipotezy ani do stwierdzenia, że kolejność nigdy nie ma znaczenia.
Nie mierzono cache, temperatury, taktowania i procesów tła; nie przypisuje się
im różnic. Wnioski dotyczą tych implementacji, pliku i warunków.

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

### Poziom B — zapis historyczny

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

### Poziom C - ograniczenia i odstępstwa

- Jedna maszyna, jedna zaakceptowana seria C1 i jedna C2, po pięć bloków;
  dodatkowo rzeczywista kontrola ujemna i niepełne przygotowanie C1.
  Rotacja ogranicza powiązanie wariantu z kolejnością, lecz nie usuwa zakłóceń.
- Nie mierzono temperatury, częstotliwości, obciążenia systemu, cache ani trybu
  zasilania. Procesy tła mogły wpływać na wyniki; brak danych do wskazania przyczyn.
- C1 stosuje 10 000-elementowy prefiks A, gdyż historyczne A nie miało 10 000
  liczb. C2 zachowuje metodę i seed generatora A, lecz jego prefiks różni się od A.
  To odstępstwo zaakceptowane przez użytkownika; pierwotna tożsamość nie zachodzi.
- Prefixy kontrolują zagnieżdżenie danych, ale wraz z rozmiarem zmienia się skład
  próbki. Nie jest to badanie wielu niezależnych losowań danych.
- Mierzone są funkcja i pętle, bez I/O i startu procesu. Jednostka ns i metadane
  zegara nie są pomiarem dokładności. Krótkie próby C++ są podatne na narzut i szum.
- Brak pomiarów Windows/MSVC, innych maszyn i replikacji pełnych serii C.
  Dodatkowe fixture sprawdzają wybrane reguły, nie dowodzą braku wszystkich błędów.

### Poziom D - ograniczenia projektu

- Jedna maszyna i **dwie serie** z jedną ustaloną permutacją losowaną.
  Po 20 par nie oznacza 20 niezależnych serii. Brak wielu dni, maszyn,
  niezależnych losowań i przedziałów ufności ogranicza siłę wniosku.
- Odwrócenie bloków ogranicza stałe powiązanie harmonogramu z początkiem badania,
  ale dwa bloki w każdej serii nie izolują całego trendu w czasie. Numer pary,
  pozycja, czas i stan systemu nadal mogą współzmieniać wyniki.
- Świeży proces ogranicza przenoszenie stanu samego programu z poprzednich prób,
  ale nie resetuje systemu ani sprzętu. Dwie rozgrzewki są **wewnątrz każdego
  procesu**; nie dowodzą stabilności całego komputera ani usunięcia wszystkich
  efektów uruchomienia. Inicjalizacja i start procesu są poza stoperem,
  mogą jednak zmienić stan przed mierzoną pętlą.
- Stałe 100 rund zachowano zgodnie z poleceniem; krótkie próby C++ mają duży
  względny rozrzut. Jednostka ns i nominalny okres zegara nie oznaczają dokładności 1 ns.
- Nie monitorowano temperatury, cache, zasilania, częstotliwości i obciążenia tła.
  Nie da się przypisać im przyczyn różnic. Zestaw zawiera też pełne koszty
  wywołania mierzonej funkcji, lecz wyklucza odczyt, walidację i wypisywanie.
- Dane to prefiks 20 020-elementowego A, nie historyczny osobny plik 10 000.
  Nie zmieniano historycznego A; odstępstwo oraz wcześniejsze C2 są jawne.
- Fixture walidatora to wybrane mutacje, nie dowód wykrycia wszystkich awarii.
  Pierwsze przygotowanie i usterkę pliku pochodnego zachowano oddzielnie od
  pełnych zaakceptowanych serii; nie zastępowały żadnego niewygodnego pomiaru.

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

### Poziom B — zapis historyczny

Poziom B jest potwierdzony przez D10–D16: automat, 18 kontroli walidatora,
dwa pełne zaakceptowane przebiegi z CSV, rzeczywiste odrzucenie kopii ze środkiem 0,
zachowane źródło błędu i ponowny poprawny przebieg. A zachowuje wyniki i identyfikatory.
Na etapie B nie wykonano C–D; nie deklaruje się oceny.

Najważniejsze decyzje do obrony: hash rozpoznaje dane, checksum sprawdza wynik;
wzorzec jest niezależny od pętli; rozgrzewki są osobną częścią walidacji;
CSV powstaje dopiero po akceptacji całości; rotacja dotyczy bloków;
minimum i mediana opisują inne cechy serii; parametrów A i B nie wolno mieszać.
Zachowanie 20 020 liczb i zmiana do 100 rund oraz pięć pól są jawnie uzgodnione.

### Poziom C - wnioski

D17–D24 dokumentują dwa wybrane badania, harmonogramy przed pomiarami,
niezależne wzorce, pełne strumienie, poprawne serie i rzeczywiste odrzucenie.
C1 potwierdziło zmianę czasu przy zachowaniu wyniku po zmianie flag kompilacji.
C2 pokazało wzrost median z licznością w przybliżeniu proporcjonalny w badanym
zakresie. Obserwacje i ograniczenia przedstawiono oddzielnie.

**Poziom C wykonano według zaakceptowanej korekty planu. Nie deklaruje się
pełnej zgodności z pierwotnym warunkiem identyczności pliku 10 000 z A.**
Materiały historyczne A–B zachowano; na etapie C nie wykonywano D. Kompletność dowodów
oraz przegląd aktualnego eksportu potwierdza D24, z osobnym wskazaniem zakresu.

### Poziom D - wynik i decyzje do obrony

D25–D31 potwierdzają wykonanie rozszerzenia D w opisanej adaptacji danych:
harmonogramy utrwalone przed pomiarami, dwa odwrócone układy bloków,
80 par / 160 właściwych prób i 320 rozgrzewek, walidacja całych zbiorów,
statystyki i wykres wszystkich punktów. Literalnego warunku istnienia osobnego
pliku 10 000 z A nie można potwierdzić; zastosowano jego dokładny prefiks.
Nie obiecuje się oceny ani nie ukrywa odstępstw A–C.

Różnice statystyk wystąpiły, lecz kierunek i skala nie były stabilne między
seriami. Nie wykazano trwałego przyczynowego efektu harmonogramu.

Do wyjaśnienia: **równowaga 10+10** zapobiega trwałemu przypisaniu implementacji
do jednej pozycji; **odwrócenie bloków** ogranicza powiązanie harmonogramu z czasem;
**świeże procesy i 2+1** ustalają ten sam cykl przygotowania każdej obserwacji;
**osobne metadane** zachowują kontrakt i pozwalają wskazać raw;
**niezależny wzorzec** sprawdza poprawność, a SHA-256 tożsamość pliku;
**wszystkie punkty** pokazują rozrzut ukryty przez pojedynczą medianę.

## 12. Wykorzystanie AI i sposób weryfikacji

Codex został wykorzystany do zautomatyzowania uruchamianych runów w zadaniach, zbudowania raportu na podstawie mocka oraz końcowej iteracji przez wszystkie zadania, by upewnić się, że żaden krok nie został pominięty.
