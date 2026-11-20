# Poprawki i ponowne sprawdzenie

**Data:** 14.11.2026. **Przebieg źródłowy:** E01-DEMO. Retest oznacza sprawdzenie po poprawce; nie musi oznaczać powtarzania pomiarów, jeżeli nie zmieniono mierzonego programu, wejścia ani granicy zegara.

## RT-01 — zakres wniosku po A-01

Porównano wszystkie 12 ilorazów z progiem zapisanym w karcie 1.0. Dane losowe dały 35,0, rosnące 8,0, malejące 36,0 i z powtórzeniami 32,0 w każdym z trzech rozmiarów. Policzone 9 przypadków spełniających próg i 3 niespełniające zgadza się z tabelą 6.

Sprawdzono streszczenie, rozdział 10, `plan/ocena_H1.md` i tok wypowiedzi do obrony. We wszystkich miejscach podano niewsparcie H1 w całym zakresie. Nie zastąpiono słowa „każdy” słowem „większość”. **Wynik: PASS; A-01 zamknięte.**

## RT-02 — jednostka i rundy po A-02

Sprawdzono przeliczenie `time_ns / rounds / 1 000 000` dla grup o 10, 20, 500, 1000, 2000 i 10 000 rund. Dla 20 prób medianę wyznaczono jako średnią dwóch środkowych czasów jednej operacji. Statystyki odtworzono z wartości niezaokrąglonych, a nie z komórek poprzedniej tabeli.

| Kontrola                     | Oczekiwany rezultat                | Rezultat |
| :--------------------------- | :--------------------------------- | :------- |
| Mediana C++, random_1000     | (1,98 + 2,02) / 2 = 2,00 ms        | Zgodny.  |
| Średnia CPython, random_1000 | 72,10 ms przy pozostawieniu 119 ms | Zgodny.  |
| R, ascending_1000            | 0,064 / 0,008 = 8,0                | Zgodny.  |
| Wykres                       | 12 ilorazów zgodnych z tabelą 6    | Zgodny.  |

**Wynik: PASS; A-02 zamknięte.** Dane surowe i identyfikator E01-DEMO pozostały bez zmian. Kontrolę wykonano w ramach zadań partner_A, a spójność opisów zweryfikowano w ramach zadań partner_B.
