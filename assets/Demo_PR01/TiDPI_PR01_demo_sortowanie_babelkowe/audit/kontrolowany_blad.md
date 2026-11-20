# Protokół kontrolowanego błędu i testów parsera

**Data testów:** 13.11.2026. Celem jest wykazanie, że błędny wynik i niepoprawna seria zostają odrzucone. Status PASS oznacza uzyskanie oczekiwanej reakcji, także gdy tą reakcją jest błąd.

## Test funkcjonalny T07

Wejście `[3, 2, 1]` ma wzorzec `[1, 2, 3]`. Po zakończeniu sortowania kontrolnie zmieniono ostatni element na 4. Porównanie całego wyniku wykryło niezgodność. Dla obu wariantów zapisano kod 1; nie opublikowano wyników takiego przebiegu.

T08 dotyczył nieistniejącego wejścia. Otrzymano kod 2. Próby T01–T06 obejmowały wejście puste, pojedynczy element, małą tablicę, ujemne wartości i powtórzenia oraz porządek rosnący i malejący. Oczekiwane wyniki zawiera `tests/cases.json`, a reakcje obu wariantów `logs/functional_tests.csv`.

## Testy parsera P01–P08

Poprawną serię przyjęto. Odrzucono oddzielne warianty: brak próby, powtórzony klucz, ujemny czas, błędny skrót wyniku, wynik oznaczony jako niepoprawny, niewłaściwy przypadek i nienumeryczne pole czasu. Zapis oczekiwanego i uzyskanego rozstrzygnięcia znajduje się w `logs/parser_tests.csv`.

Próby z kontrolowanym błędem nie należą do 480 poprawnych rekordów E01-DEMO. Nie należy dodawać ich do statystyk czasu ani przedstawiać ich odrzucenia jako usunięcia wartości odstającej. Zatwierdzenie: partner_A i partner_B.
