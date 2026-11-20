# Dziennik decyzji — E01 i przebieg E01-DEMO

> Materiał dydaktyczny: wypełniony dokument fikcyjnego zespołu, należący do wzorca Projektu 01.

**Zespół:** `demo`. **Odpowiedzialni:** `partner_A` i `partner_B`. Wpisy rozróżniają decyzje przed właściwymi pomiarami od interpretacji wyników i poprawek redakcyjnych po pomiarach. Nie nadpisuje się poprzednich ustaleń.

## D-01 — Pytanie i kryterium H1

**Data:** 7.11.2026. **Stan wiedzy:** przed właściwą serią; czasy tej serii nie są jeszcze znane.

Ustalono pytanie o mediany czasu własnych implementacji sortowania bąbelkowego. H1 wymaga R = mediana Python / mediana C++ ≥ 10 dla każdego z 12 przypadków. Próg jest przewidywaniem, a nie warunkiem uzyskania dobrej oceny projektu. Wynik poniżej progu zostanie opisany bez zmiany hipotezy.

**Decyzja:** przyjąć H1 i regułę oceny z karty. **Zatwierdzenie:** partner_A i partner_B. **Dowód:** [karta E01](karta_E01.md), rozdział 2.

## D-02 — Pełny zestaw wejść i ta sama operacja

**Data:** 7.11.2026. **Stan wiedzy:** przed właściwą serią.

Przyjęto N = 100, 500 i 1000 oraz dane losowe, rosnące, malejące i z powtórzeniami. Oba warianty mają czytać wspólne pliki. Nie porównuje się własnego algorytmu z gotową funkcją biblioteczną. Dane rosnące pozostają w badaniu, ponieważ sprawdzają wcześniejsze zakończenie.

**Decyzja:** zachować wszystkie 12 przypadków i kontrolować pełne SHA-256. **Zatwierdzenie:** partner_A i partner_B. **Dowód:** karta, rozdziały 4–5; [recenzja R-03–R-05](recenzja_planu.md).

## D-03 — Zamrożenie wersji 1.0

**Data:** 7.11.2026. **Stan wiedzy:** po recenzji planu, przed właściwymi pomiarami.

Uwzględniono dziewięć uwag recenzenta: doprecyzowanie progu, mediany, kopii danych, tożsamości wejść, walidacji, reakcji na błąd, kolejności, przeliczania czasu i wartości odstających.

**Decyzja:** zatwierdzić kartę E01 1.0. Ewentualne zmiany metody wymagają nowego wpisu i zachowania poprzedniej wersji. **Zatwierdzenie:** partner_A i partner_B. **Dowód:** karta i recenzja z 7.11.

## D-04 — Gotowość techniczna i kalibracja

**Data:** 13.11.2026. **Stan wiedzy:** znane są wyniki testów i kalibracji; nie wykonano właściwej serii E01-DEMO.

Testy funkcjonalne, kontrolowana zmiana wyniku i próby uszkodzonego rekordu dały oczekiwane reakcje. Kalibracja potwierdziła liczby rund zapisane w karcie: 500/20/10 dla układów innych niż rosnący oraz 10 000/2000/1000 dla rosnącego. Nie trzeba było zmieniać planu. Czasów kalibracji nie włącza się do raportowej serii.

**Decyzja:** dopuścić właściwą serię przy niezmienionej karcie 1.0. **Odpowiedzialni:** partner_A — implementacje i rundy; partner_B — testy walidatora i parsera. **Ślad:** testy opisane w rozdziale 6 raportu; parametry w karcie.

## D-05 — Zakończenie serii E01-DEMO

**Data:** 14.11.2026, po sesji 10:00–11:00 CET. **Stan wiedzy:** dostępne są surowe wyniki właściwej serii.

Zebrano 480 poprawnych rekordów: 12 przypadków × 2 warianty × 20 prób. Zachowano 48 rozgrzewek poza analizą końcową. Jednostką tabel jest czas jednego sortowania, wyliczony przed statystykami przez podzielenie czasu próby przez liczbę rund i 1 000 000.

**Decyzja:** zakończyć serię i rozpocząć analizę; nie dopisywać prób tylko w grupach niekorzystnych dla H1. **Zatwierdzenie:** partner_A i partner_B. **Dowód:** `../results/raw/e01.csv` i podsumowania w `../results/summary/`.

## D-06 — Pozostawienie wysokiego poprawnego czasu

**Data:** 14.11.2026. **Stan wiedzy:** po analizie wyników.

Dla `random_1000` w CPythonie zaobserwowano 119,0 ms na sortowanie. Mediana grupy wynosi 70,0 ms, a średnia 72,1 ms. Nie ustalono przyczyny wysokiego czasu. Wynik funkcjonalny był poprawny, a plan nie dopuszczał usuwania obserwacji wyłącznie na podstawie wielkości czasu.

**Decyzja:** zachować rekord i pokazać rozrzut. Nie przypisywać zdarzenia konkretnemu procesowi bez dowodu. **Zatwierdzenie:** partner_A i partner_B. **Dowód:** CSV i tabela 5 raportu.

## D-07 — Odpowiedź na H1 bez przesuwania progu

**Data:** 14.11.2026. **Stan wiedzy:** znane są wartości 12 ilorazów median.

R wynosi 35,0 dla losowych, 8,0 dla rosnących, 36,0 dla malejących i 32,0 dla danych z powtórzeniami. Warunek R ≥ 10 spełnia 9 z 12 przypadków. Wszystkie trzy układy rosnące pozostają poniżej progu.

**Decyzja:** wyniki nie wspierają H1 w pełnym zakresie. Nie zmieniać progu 10 na 8 ani warunku „każdy” na „większość”. **Zatwierdzenie:** partner_A i partner_B. **Dowód:** [ocena H1](ocena_H1.md) i tabela 6 raportu.

## D-08 — Poprawki po audycie A-01 i A-02

**Data:** 14.11.2026. **Stan wiedzy:** po pomiarach i pierwszej wersji raportu.

Poprawiono zbyt szerokie zdanie w streszczeniu oraz tabelę używającą czasu całej próby zamiast jednej operacji. Odtworzono statystyki i wykres. Retest objął wszystkie liczby rund oraz kontrolę 2,00 ms, 72,10 ms i R = 8,0. Wynik był zgodny z CSV.

**Decyzja:** zamknąć A-01 i A-02. Są to poprawki analizy i opisu; nie zmieniają H1, algorytmu, planu ani surowych rekordów. **Zatwierdzenie:** partner_A i partner_B. **Dowód:** rozdział 11 raportu i `../results/summary/`.

## D-09 — Zamknięcie dokumentacji

**Data:** 14.11.2026. **Stan wiedzy:** po poprawkach i końcowej kontroli.

Sprawdzono zgodność karty, oceny H1, streszczenia i wniosków. Wersja karty pozostaje 1.0: do jej treści nie dopisano wyników po pomiarach. Końcową odpowiedź zapisano osobno.

**Decyzja:** zatwierdzić dokumentację do oddania i przygotować obronę. **Zatwierdzenie:** partner_A i partner_B. **Dowód:** [raport końcowy](../report/raport.md), [karta](karta_E01.md) i [ocena H1](ocena_H1.md).
