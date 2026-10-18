# Plan poziomu A - Regulus

Zapisany 2026-10-17 przed pierwszą kompilacją i pomiarami. Brak wcześniejszych wyników TiDPI_07.

Pytanie: jakie czasy osiągają dwie ręczne implementacje sumy odległości od 500
w tych samych warunkach? Hipoteza: obie zwrócą dokładnie wynik wzorcowy;
czasy mogą się różnić, bez ustalania zwycięzcy przed pomiarem.

Dane: count=20020, wartości 0..1000, każda dokładnie 20 razy; seed=20261017.
Generator Python random.Random(seed).shuffle tasuje gotowy multizbiór.
Format ASCII: jedna liczba i LF na wiersz. Zapis SHA-256 bajtów po wygenerowaniu.
Niezależne oczekiwanie: suma 0..500 wynosi 125250. Po obu stronach 500
suma odległości wynosi 2*125250=250500; 20 kopii daje 5010000.
rounds=200, wynik=1002000000. Górne oszacowanie count*500*rounds=2002000000
mieści się w int64_t (9223372036854775807); Python int bez przepełnienia.

Operacja: wynik=0; dla każdej z 200 rund i każdej wartości oblicz d=x-500,
jeżeli d<0, ustaw d=-d; dodaj d do wyniku. Bez sum/abs w badanej pętli.
C++ int64_t, Python int; brak mnożenia w pętli. Kolejność danych identyczna.

Zmieniany czynnik: implementacja C++/Python. Stałe: dane, rundy, algorytm,
maszyna, zegary monotoniczne, konfiguracja C++ Release -O2 -DNDEBUG -std=c++17.
Pomiar: start zegara, wywołanie funkcji (inicjalizacja akumulatora i obie pętle), stop.
Poza pomiarem: start procesu, odczyt, alokacja, walidacja danych, kontrola wyniku,
formatowanie, stdout/stderr. Zapis jednostki ns nie oznacza rozdzielczości 1 ns.

Kolejność sekwencyjna: blok 1 C++ potem Python; blok 2 Python potem C++.
Rotacja dotyczy bloków, nie pojedynczych prób. Każdy proces: dwie rozgrzewki
na osobnym stderr i pięć właściwych prób. Łącznie na implementację cztery
rozgrzewki oraz dziesięć prób (numery 1..5 i 6..10). Jedna seria, dwa bloki.
Nie powtarzać ani nie usuwać niewygodnych czasów. Bez debuggera.

Akceptacja: wspólny hash i histogram wejścia, poprawny build i wszystkie kody 0;
rekordy language;trial;time_ns;checksum;correct, poprawne typy, dodatnie czasy,
dokładny komplet numerów, checksum=1002000000 i correct=true także w rozgrzewkach.
Przy błędzie odrzucić porównanie i zachować dowody; nowe wykonanie w nowym katalogu.
Statystyki dopiero po walidacji całości: min, max, rozstęp, mediana (średnia pozycji 5 i 6).
Kontrole TC-01 dane/wzorzec; TC-02 Release; TC-03 rekordy i rozgrzewki;
TC-04 niezależne przeliczenie wybranych wierszy i statystyk; TC-05 eksport/linki/anonimizacja.

PDF s. 6: wymagania A; s. 8-10: struktura, anonimowość, dowody, interpretacja.
Automat, przypadek błędny i druga pełna seria należą do B, nie są tu realizowane.
Ogólna lista artefaktów PDF obejmuje wszystkie poziomy; zakres A określa lista s. 6.
Dodatkowe zasady polecenia: plan przed pomiarami, niezależny wzorzec, rotacja,
pełne metadane i TC/D. AGENTS.md lokalnie pusty. Wybór multizbioru i dwóch bloków
to decyzje projektowe, nie dosłowne wymagania PDF.
