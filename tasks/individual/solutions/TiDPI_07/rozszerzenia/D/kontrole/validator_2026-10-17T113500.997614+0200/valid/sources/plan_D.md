# Plan D - wpływ harmonogramu kolejności

Kryptonim: Regulus. Data: 2026-10-17. Plan zapisany przed NOWYMI pomiarami D;
nie dotyczy historycznych pomiarów A-C. Czas i odciski utrwali prepare_D.py.

## Pochodzenie wymagań i kryteria akceptacji

- PDF (całe 10 stron przeczytane): D to wartościowe rozszerzenie ponad A-C,
  z pytaniem, hipotezą, kontrolowanymi zmiennymi, walidacją i ograniczeniami.
  Zachować wcześniejsze dowody, wspólny raport i eksport, surowe dane i wykres
  z danymi źródłowymi w images. Podstawy A-C: wspólne dane, ręczna uzgodniona
  operacja, Release, rozgrzewki, powtórzenia, automat, walidacja, kontrola ujemna,
  dwie serie B, dokładnie dwa rozszerzenia C. Ocenę ustala prowadzący.
- Polecenie użytkownika: porównać konkretne harmonogramy w dwóch seriach,
  rounds=100, dokładnie 2 rozgrzewki + 1 próba w każdym świeżym procesie,
  pełne metadane każdej próby poza pięciopolowym stdout, checksumy każdej próby,
  kompletność i statystyki min/max/rozstęp/mediana oraz porównanie pozycji.
- Repozytorium: AGENTS.md jest pusty. Wzorce TiDPI_03/05/06 określają styl
  organizacji, nie przenoszą wyników ani historycznych metryczek.
- Decyzje projektowe: jeden binarny Release na obie serie, oddzielne katalogi serii,
  osobne strumienie każdego procesu, walidacja obu serii przed analizą, bez
  usuwania lub zastępowania pomiarów. Bez testu istotności: analiza opisowa.

## Pytanie i hipoteza

Czy harmonogram kolejności zmienia rozkład czasów obu badanych implementacji
oraz iloraz median Python/C++ przy identycznym zadaniu i poprawnym wyniku?
Hipoteza: może zmienić rozkład i relację median. Nie zakładamy efektu ani zwycięzcy;
brak wyraźnej, powtarzalnej różnicy również jest wynikiem.

## Operacja, dane, oczekiwanie

Ręczna suma odległości od 500: różnica x-500, warunkowa zmiana znaku,
dodanie do akumulatora, 100 rund. Status uzgodnienia z prowadzącym pochodzi
wprost z bieżącego polecenia użytkownika. Nie ma osobnej korespondencji.
Wzorzec niezależny: 100 * (500*n_low-sum_low + sum_high-500*n_high).
Przed pomiarami zapisać liczności i sumy partycji oraz wynik w data_manifest.json.
Po pomiarach sprawdzić histogramem i osobnym skryptem.

A ma 20 020 liczb, nie 10 000. D stosuje dokładnie pierwszych 10 000 wierszy A,
identycznych z C1, nie nowe dane C2. Jest to jawna interpretacja nieistniejącego
pliku 10 000 z A, nie twierdzenie o zgodności liczności historycznego A.
Oryginalny generator: [i % 1001 for i in range(20020)],
random.Random(20261017).shuffle(values), ASCII, LF; potem wybór prefiksu.
Zakres 0..1000. Dane i SHA-256 źródła oraz prefiksu zachować i sprawdzić.
Oczekiwany checksum prefiksu: 251042700 (nie odcisk SHA-256).
Różnica -500..500, wartość bezwzględna <=500;
10000*500*100=500000000 < 9223372036854775807, także wszystkie sumy pośrednie.
C++ int64_t, Python int. Iloczyny parametrów C++ long long są bezpieczne
w dopuszczonym zakresie count<=50000.

## Czynniki i granice

Zmieniany czynnik: sposób ułożenia 10 par C++/Python i 10 Python/C++.
Pozycja w parze jest dodatkowym przekrojem analizy, nie nowym rozszerzeniem C.
Stałe: maszyna, dane i ich kolejność, źródła, Clang Release -std=c++17 -O2 -DNDEBUG,
CPython 3.14.4 (wymagana zgodność z A-C), 100 rund, 2 rozgrzewki, 1 próba/proces.
Seria jest blokiem replikacji; kolejność harmonogramów odwrócona między seriami.
Nie uruchamiać pomiarów równolegle, bez debuggera, bez celowych przerw między parami.
Nie zmieniać liczby rund w celu poprawy czasów C++.

Stoper bezpośrednio przed calculate(values), stop bezpośrednio po niej:
steady_clock i duration_cast<nanoseconds>, perf_counter_ns(). Poza pomiarem:
start i koniec procesu, importy, odczyt i przygotowanie, walidacja, wypisywanie.
Checksum obserwowalny i sprawdzany; nie wyklucza wszystkich optymalizacji.
Zapisać nominalny okres C++ i zgłoszoną rozdzielczość Pythona oddzielnie od ns.
Nie deklarować zmierzonej efektywnej rozdzielczości C++ ani dokładności 1 ns.

## Dokładne harmonogramy i liczebności

Naprzemienny: 20 par, nieparzysta para C++/Python, parzysta Python/C++.
Losowany: lista 10 [cpp,python] i 10 [python,cpp], przetasowana
random.Random(20260402).shuffle(). Ten sam zapisany układ w obu seriach.
Zapis pełnych harmonogramów przed pierwszym pomiarem: schedules.json,
planned_trials.json i prepared.json z czasem i hashami.
Seria 1: naprzemienny, losowany. Seria 2: losowany, naprzemienny.
Rotacja na poziomie PAR, a odwrócenie kolejności harmonogramów na poziomie SERII.
Każda para to dwa odrębne kolejno uruchomione procesy; każdy 2+1.
Łącznie 80 par, 160 procesów, 160 właściwych pomiarów, 320 rozgrzewek.
W każdym stdout lokalny trial=1; numer pary i pozycja są tylko w metadanych.

## Walidacja, odrzucenie, analiza

Sprawdzić źródła A-C i dowody, zachować ich hashe i raport C. Braki podstaw
uzupełniać tylko jeśli potrzebne D, nie wykonywać nowych rozszerzeń C.
Sprawdzić plan przed pomiarami, dokładny harmonogram i jego równowagę,
zgodność rzeczywistej kolejności/timestampów/poleceń z planem, brak nakładania,
kody 0, wersje, flagi, niezmienność danych/źródeł/binariów.
Każdy stdout: dokładny nagłówek language;trial;time_ns;checksum;correct,
dokładnie 1 rekord, właściwy język, całkowity trial=1 i time_ns>=0,
checksum niezależny, correct=true. Stderr: zegar i 2 osobne poprawne rozgrzewki.
Błąd dowolnego elementu odrzuca CAŁY zbiór danej serii: bez results.csv i statystyk.
Nie powtarzać niewygodnych pomiarów; zachować wszystkie strumienie i diagnostykę.
Testy walidatora na oznaczonych kopiach: checksum mimo true, brak rekordu,
zła kolejność, zła rozgrzewka; bez przedstawiania ich jako pomiarów.

Dopiero po walidacji obu serii: osobno seria/harmonogram/implementacja,
min/max/rozstęp/mediana z 20 pomiarów; dodatkowo pozycje 1/2 (po 10).
Mediana to średnia dwóch środkowych po sortowaniu. Minimum opisuje dolny kres
zaobserwowanych czasów, mediana środek próby, nie gwarantowany czas.
Iloraz median Python/C++ i relacja median pozycji 2/1 obliczane w obrębie grup.
Wykres rozkładu wszystkich 160 właściwych punktów, osobne skale implementacji,
serie i harmonogramy oznaczone, pozycje oznaczone kolorami. Zachować CSV wykresu.
Niezależnie przeliczyć checksum, wszystkie statystyki i surowe wiersze par 1/20.

## Ograniczenia i końcowe artefakty

Jedna maszyna, tylko 2 serie, brak niezależnych dni i wielu randomizacji.
Odwrócenie kolejności ogranicza pomieszanie z czasem, ale nie usuwa trendu i tła.
Świeże procesy mają własny stan, rozgrzewki są wewnątrz procesu i nie gwarantują
stabilności systemu. Start procesu nie jest mierzony, lecz może wpływać na stan.
Nie przypisywać efektu temperaturze, cache, częstotliwości lub interpreterowi
bez ich pomiaru. Brak efektu nie dowodzi jego nieistnienia w innych warunkach.
Aktualizować jeden raport w 12 sekcjach, D25+ i TC-21+, PDF render i anonimizacja.
Bez commitu, pushu, wysyłki i bez dołączania szkolnego PDF do zestawu oddania.
