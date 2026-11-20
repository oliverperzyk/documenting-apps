# Tok prezentacji Projektu 01 — Bąbelkowy pojedynek

Prezentację przygotowano do przeprowadzenia z użyciem `report/raport.pdf`. Osobny PPTX nie jest potrzebny. Kolejność poniżej prowadzi od pytania przez metodę i wynik do decyzji; nie jest odczytaniem całego raportu.

## 1. Pytanie i przewidywanie — PDF, strony 1–2

Porównano własne implementacje sortowania bąbelkowego w C++ Release i CPythonie. H1 przewidywała R ≥ 10 dla każdego z 12 przypadków. Warunek zapisano przed właściwą serią, a nie po obejrzeniu wyników.

## 2. Uczciwe warunki — PDF, strony 3–5

Wykorzystano te same pliki o zgodnych SHA-256, 3 rozmiary i 4 układy. Zastosowano świeżą kopię na rundę, jednakową granicę pomiaru, 2 rozgrzewki i po 20 prób. Kolejność wariantów zmieniano naprzemiennie. Poprawność sprawdzano pełnym wzorcem poza zegarem.

## 3. Najważniejszy wynik — PDF, strona 8

Wykres ilorazów median pokazuje R = 35 dla losowych, 8 dla rosnących, 36 dla malejących i 32 dla danych z powtórzeniami. Rozrzut i liczebności znajdują się na stronach 6–7; sam wykres ilorazów ich nie zastępuje.

## 4. Odpowiedź na H1 — PDF, strona 8

Próg spełniło 9 z 12 przypadków. Trzy wejścia rosnące nie osiągnęły 10. Wyniki nie wspierają H1 w pełnym zakresie. Nie zmieniono warunku na „większość” i nie usunięto niewygodnych danych.

## 5. Granice odpowiedzi — PDF, strona 9

Wniosek odnosi się do opisanych implementacji, jednego stanowiska, jednej sesji i wskazanych wejść. Nie oznacza, że każdy program w C++ osiągnie takie przyspieszenie. Wysoki poprawny czas 119 ms zachowano; przyczyny nie ustalono.

## 6. Gdzie szukać dowodu? — PDF, strona 10

Od liczby należy przejść do CSV i reguły obliczenia. Źródłem 2,00 ms jest mediana C++ dla random_1000. Dla R = 8,0 należy podzielić 0,064 przez 0,008. Rejestr w `audit/rejestr_dowodow.md` wskazuje pozostałe deklaracje.

## Pytania do obrony i rdzeń odpowiedzi

| Pytanie                                        | Rdzeń odpowiedzi / dowód                                                    |
| :--------------------------------------------- | :-------------------------------------------------------------------------- |
| Dlaczego nie porównano czasów całej próby?     | Liczby rund zależą od przypadku; najpierw przeliczono czas jednej operacji. |
| Skąd mediana przy 20 próbach?                  | Średnia dwóch środkowych wartości po uporządkowaniu.                        |
| Czy samo `correct=true` wystarczy?             | Nie. Potrzebna jest kontrola pełnego wyniku oraz test walidatora.           |
| Co wykazał kontrolowany błąd?                  | Zmieniony element został odrzucony, kod 1, bez publikacji błędnej serii.    |
| Dlaczego 119 ms nie usunięto?                  | Próba poprawna, brak wcześniej przyjętej reguły odrzucenia.                 |
| Czy niższa mediana C++ potwierdza H1?          | Nie sama w sobie; H1 wymagała również progu 10 w każdym przypadku.          |
| Czy na innym procesorze wynik będzie taki sam? | Tego nie zbadano; potrzebna nowa sesja na opisanym środowisku.              |
| Jak sprawdzono sugestie AI?                    | Zapis decyzji i weryfikacji w `teamwork/wykorzystanie_AI.md`.               |

Każdy partner powinien umieć wskazać te same dowody. Przy braku pamięci dokładnej liczby należy otworzyć źródło zamiast zgadywać.
