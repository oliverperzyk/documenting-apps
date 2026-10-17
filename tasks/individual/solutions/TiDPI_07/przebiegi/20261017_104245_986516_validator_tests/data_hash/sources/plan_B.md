# Plan B — Regulus

Zapis przed nowymi pomiarami B, 2026-10-17. Historyczny plan A pozostaje bez zmian.
Pytanie: jakie minimum i medianę osiągną te dwie ręczne implementacje dla
wspólnego pliku i 100 rund; czy kierunek porównania powtórzy się w dwóch seriach?
Hipoteza: obie implementacje dadzą niezależny wynik wzorcowy, a różnice czasów
mogą powtórzyć się między seriami; nie wskazujemy zwycięzcy przed pomiarem.

Operacja uzgodniona z prowadzącym według polecenia użytkownika: ręczna suma
odległości od 500. Dane A pozostają bez zmian: 20020 elementów, 0..1000,
każda wartość 20 razy, seed=20261017, random.Random(seed).shuffle multizbioru.
SHA-256: 1e1422a8679f65bb7ec778bdbd821b74a4596431774711e89671acaa9ddca3d8.
Użytkownik potwierdził zachowanie tego pliku (nie nowego pliku 10000 liczb)
i zmianę rounds z historycznych 200 na 100. Oczekiwanie B=501000000:
20 _2_ (500*501/2) * 100. Walidator sprawdzi histogram i niezależnie
obliczy sumy partycji poniżej/powyżej 500. Nie importuje calculate benchmarków.
Kontrola ujemna: dla środka 0 wzorzec=20*(1000*1001/2)*100=1001000000.
Potwierdzić różnicę na rzeczywistym histogramie przed uruchomieniem błędu.

Czynnik porównywany: implementacja. Stałe: maszyna, plik, ręczna operacja,
rounds=100, C++17 Release -O2 -DNDEBUG -Wall -Wextra -pedantic; bez debuggera.
C++ int64_t: d=-500..500, wynik <=20020*500*100=1001000000 < 2^63-1;
Python int. Pomiar: start zegara, funkcja z inicjalizacją i pętlami, stop;
poza stoperem odczyt, przygotowanie, walidacja, stdout/stderr, start procesu.
C++ steady_clock i duration_cast<nanoseconds>, Python perf_counter_ns.
Jednostka ns jest osobna od rozdzielczości; zanotować informacje obu zegarów.

Każda seria: blok 1 C++ -> Python, blok 2 Python -> C++, sekwencyjnie.
Każdy proces: 2 rozgrzewki na stderr, 5 prób na stdout; numery 1..5 / 6..10.
Łącznie 4 rozgrzewki i dokładnie 10 prób na implementację. Rotacja bloków,
nie pojedynczych prób. Zachować wszystkie czasy, bez zastępowania obserwacji.
Kolejność serii: poprawna 1, kopia Python z x-0, poprawna 2.
Poprawna 2 potwierdza działanie oryginału po błędzie; oryginał nie jest psuty.

Akceptacja: hash i histogram danych, kopie i hashe źródeł, kompilacja i procesy
z kodem 0, zgodny harmonogram, dokładny nagłówek i PIĘĆ pól
language;trial;time_ns;checksum;correct (rozbieżność sześciu pól rozstrzygnięta
przez użytkownika). Dozwolone cpp/python, trial int i dokładny komplet,
time_ns int >=0, checksum int zgodny ze wzorcem, correct=true.
Rozgrzewki walidować oddzielnie, także kompletność, numery i checksum.
Błąd w dowolnej części odrzuca całość: brak results.csv i brak statystyk.
Błędny program może przerwać już rozgrzewkę; zachować to jako rzeczywisty błąd.
Dla zaakceptowanych: min/max/rozstęp/mediana osobno dla serii i implementacji.
Przy 10 czasach mediana=(pozycja 5+6)/2, dokładnie, bez utraty 0,5 ns.
Niezależnie przeliczyć wiersze 1 i 10 oraz statystyki z surowych strumieni.

PDF: automat, walidacja, kontrola ujemna, dwie serie, minimum/mediana i eksport.
Użytkownik: plan przed pomiarami, niezależny wzorzec, pełne metadane,
max/rozstęp, histogram błędu, TC/D i wizualna kontrola eksportu.
AGENTS.md jest pusty. Decyzje projektowe: dwa bloki jak w A, osobny walidator,
kody 0 akceptacja / 1 odrzucenie / 2 błąd obsługi; świeży build per seria,
timeout 60 s na proces benchmarku, 120 s na kompilację.
