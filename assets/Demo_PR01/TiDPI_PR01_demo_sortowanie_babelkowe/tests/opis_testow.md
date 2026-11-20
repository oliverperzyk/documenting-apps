# Zestaw testów funkcjonalnych i kontraktu

`cases.json` zawiera sześć poprawnych wejść oraz oczekiwane wyniki. T07 i T08 opisują odpowiednio celowe uszkodzenie wyniku i brak wejścia. Pełny zapis reakcji zawiera `logs/functional_runs.jsonl`, a zbiorczą kontrolę kodów `logs/functional_tests.csv`.

W testach P02–P08 pojedynczo zmienia się poprawną serię: usuwa próbę, powiela klucz, wpisuje ujemny czas, błędny skrót, niepoprawny wynik, nieznany przypadek albo nienumeryczny czas. Oczekiwane rozstrzygnięcia zawiera `logs/parser_tests.csv`. Własny walidator powinien dać się sprawdzić tymi samymi sytuacjami, a nie tylko poprawnym CSV.

Zgodnie z zakresem demonstracji nie dołączono implementacji testów. Źródła i automatyzacja są miejscami na kod; dane testowe i przykładowe rezultaty są wypełnione.
