# Ocena hipotezy H1 — wyniki przebiegu E01-DEMO

> Materiał dydaktyczny: wypełniony dokument fikcyjnego zespołu, należący do wzorca Projektu 01.

**Data:** 14.11.2026. **Autorzy:** partner_A i partner_B. **Podstawa:** karta eksperymentu E01 w wersji 1.0 z 7.11.2026. Dokument sporządzono po analizie wyników; nie zastępuje ani nie zmienia zamrożonego planu.

## 1. Oceniana hipoteza

**H1: dla każdego z 12 zaplanowanych przypadków mediana czasu CPythona jest co najmniej dziesięciokrotnie większa niż mediana czasu C++ Release.**

Weryfikuje się warunek **R = mediana Python / mediana C++ ≥ 10** dla każdego przypadku osobno. Jedna niespełniająca grupa wystarcza, by nie uznać H1 za wspartą w pełnym zakresie. Regułę i próg przyjęto przed właściwą serią.

## 2. Dane i procedura oceny

Analiza obejmuje E01-DEMO, 12 przypadków i po 20 poprawnych prób obu implementacji. Razem jest to 480 rekordów i 24 grupy pomiarowe. Właściwe rekordy mają `warmup=false`. Rozgrzewki nie należą do tej analizy. Nie usuwano wartości odstających.

Najpierw dla każdego rekordu obliczono czas jednego sortowania: `time_ns / rounds / 1 000 000`. Dla każdej grupy wyznaczono medianę 20 czasów, a następnie iloraz median wariantów. Decyzje oparto na niezaokrąglonych wartościach; tabela przedstawia czytelny zapis tych wyników.

## 3. Wyniki dla wszystkich zaplanowanych przypadków

| Przypadek             | Mediana C++ [ms] | Mediana CPython [ms] |    R | Warunek R ≥ 10 |
| :-------------------- | ---------------: | -------------------: | ---: | :------------- |
| losowe, N = 100       |          0,02000 |              0,70000 | 35,0 | spełniony      |
| losowe, N = 500       |          0,50000 |             17,50000 | 35,0 | spełniony      |
| losowe, N = 1000      |          2,00000 |             70,00000 | 35,0 | spełniony      |
| rosnące, N = 100      |          0,00080 |              0,00640 |  8,0 | niespełniony   |
| rosnące, N = 500      |          0,00400 |              0,03200 |  8,0 | niespełniony   |
| rosnące, N = 1000     |          0,00800 |              0,06400 |  8,0 | niespełniony   |
| malejące, N = 100     |          0,02500 |              0,90000 | 36,0 | spełniony      |
| malejące, N = 500     |          0,62500 |             22,50000 | 36,0 | spełniony      |
| malejące, N = 1000    |          2,50000 |             90,00000 | 36,0 | spełniony      |
| powtórzenia, N = 100  |          0,01500 |              0,48000 | 32,0 | spełniony      |
| powtórzenia, N = 500  |          0,37500 |             12,00000 | 32,0 | spełniony      |
| powtórzenia, N = 1000 |          1,50000 |             48,00000 | 32,0 | spełniony      |

Przykładowo dla losowych 1000 elementów R = 70,0 / 2,0 = 35,0. Dla rosnących 1000 elementów R = 0,064 / 0,008 = 8,0. Druga grupa ma niższą medianę C++, ale nie osiąga wymaganego progu 10.

## 4. Decyzja i jej uzasadnienie

**Wyniki E01-DEMO nie wspierają H1 w pełnym zaplanowanym zakresie.** Warunek spełnia 9 z 12 przypadków. Trzy przypadki rosnące mają R = 8,0, a H1 wymagała R ≥ 10 dla każdego z nich.

Węższe stwierdzenie „mediana C++ była niższa we wszystkich badanych przypadkach” jest zgodne z danymi. Nie jest jednak równoważne H1. Zastąpienie nim pierwotnej hipotezy po pomiarach ukryłoby niespełnione przewidywanie. Nie usuwa się przypadków rosnących i nie zmienia się progu na 8.

Nie podaje się wartości p ani nie deklaruje się istotności statystycznej. Oceniono opisowe kryterium zapisane w karcie. Nie wyprowadza się uniwersalnego twierdzenia o językach programowania.

## 5. Zakres odpowiedzi

Wniosek dotyczy własnych implementacji sortowania bąbelkowego, opisanych 12 wejść, jednego stanowiska i jednej sesji. Dla danych rosnących działa wcześniejsze zakończenie, zmieniające liczbę wykonywanych operacji. Badanie nie rozdziela wpływu reprezentacji liczb, kompilatora, interpretera i narzutu pętli.

Przebadanie innych zestawów, rozmiarów i niezależnych sesji wymaga osobnego planu. Obecne wyniki nie pozwalają powiedzieć, jakie przyspieszenie uzyska dowolny program po przepisaniu do C++.

## 6. Powiązanie z dowodami

- [Karta E01 1.0](karta_E01.md) — pierwotne brzmienie H1, próg i reguła decyzji.
- [Dziennik decyzji](dziennik_decyzji.md), D-01, D-03 i D-07 — przyjęcie kryterium i jego zachowanie po pomiarach.
- [Surowy CSV](../results/raw/e01.csv) — rekordy użyte w analizie.
- [Skrypt analizy](../src/automation/analyze_results.py) — odtworzenie statystyk i ilorazów.
- [Podsumowanie JSON](../results/summary/summary.json) i [tabela statystyk](../results/summary/statistics.csv) — wyniki obliczeń.
- [Raport końcowy](../report/raport.md), rozdziały 8–11 — rozrzut, wykres, interpretacja i poprawki po audycie.

**Zatwierdzenie:** W ramach kontroli partner_A sprawdzono przejście od rekordów do median, a w ramach kontroli partner_B porównano wszystkie ilorazy z progiem i brzmieniem H1. Powyższą odpowiedź zatwierdzono wspólnie 14.11.2026.
