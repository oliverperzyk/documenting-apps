# Mapa kompletności demonstracji

## Co wykorzystano z wcześniejszej demonstracji?

Zachowano raport w stylu bezosobowym (MD/PDF), wykres, cztery dokumenty planu, manifest, 12 wejść i 480 rekordów pełnej serii. Pomiary pięciopróbkowe z małego przykładu lekcji 12 pominięto, ponieważ nie odpowiadają minimalnemu zakresowi Projektu 01. Nie kopiowano starych wersji i archiwów roboczych.

## Co uzupełniono?

| Wymaganie projektu                           | Element wzorca                                                                           |
| :------------------------------------------- | :--------------------------------------------------------------------------------------- |
| Kod C++ i Python                             | Pliki `src/cpp/main.cpp` i `src/python/benchmark.py` — placeholdery.                     |
| Generator, walidacja, analiza, automatyzacja | Cztery placeholdery w `src/automation/`.                                                 |
| Wzorce sortowania i małe testy               | `data/reference/`, `tests/cases.json`.                                                   |
| Surowe i zwalidowane wyniki                  | `results/raw/`, `results/validated/`.                                                    |
| Wszystkie wymagane statystyki                | `results/summary/statistics.csv` i `summary.json`.                                       |
| Środowisko i kompilacja                      | `logs/environment.txt`, `compile_*`.                                                     |
| Wyjścia, błędy, kody, kolejność, rozgrzewki  | `logs/runs/index.csv` i 12 plików JSONL obejmujących 528 wywołań.                        |
| Kalibracja                                   | `logs/calibration.csv` — osobno od końcowych statystyk.                                  |
| Kontrolowany błąd i parser                   | Testy T01–T08 obu wariantów i P01–P08; oczekiwane oraz uzyskane reakcje.                 |
| README i przebieg dymny                      | Główna instrukcja, oddzielne E01-SMOKE, przykładowe wyjścia i protokół czystej kopii.    |
| Audyt i poprawki                             | `audit/rejestr_dowodow.md`, `protokol_audytu.md`, `retesty.md`.                          |
| Współpraca i AI                              | `teamwork/dziennik_pracy.md`, `wykorzystanie_AI.md`.                                     |
| Prezentacja i obrona                         | Tok wypowiedzi z wykorzystaniem PDF oraz protokół próby obrony w `presentation/`.        |
| Kompletność i czystość paczki                | Lista kontrolna, brak programów skompilowanych i cache, ZIP z jednym katalogiem głównym. |

Raport obejmuje pytanie, H1, zmienne, dane, implementacje, granicę pomiaru, rozgrzewki, środowisko, walidację, automatyzację, wszystkie statystyki, wykres, ograniczenia, odpowiedź na H1, rozszerzenia, wkład, AI i rejestr dowodów. Źródła pozostają jedynym celowo niewypełnionym elementem, zgodnie z zakresem zamówionego wzorca.
