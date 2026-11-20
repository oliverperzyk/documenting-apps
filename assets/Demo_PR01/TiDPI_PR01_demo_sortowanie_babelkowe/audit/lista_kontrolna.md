# Lista kompletności materiału do oddania

Niniejszy zestaw pokazuje wszystkie kategorie wymaganych materiałów. Wyjątek uzgodniony dla demonstracji: kod ma postać komentarzy-placeholderów. W rzeczywistej pracy uczniowskiej takie pliki nie spełniają wymagania działającej implementacji.

| Wymaganie                                           | Miejsce w zestawie                                        | Status materiału                         |
| :-------------------------------------------------- | :-------------------------------------------------------- | :--------------------------------------- |
| Jeden katalog o poprawnej nazwie                    | `TiDPI_PR01_demo_sortowanie_babelkowe`                    | Dostarczono.                             |
| Karta E01, hipoteza, recenzja i decyzje             | `plan/`                                                   | Wypełniono.                              |
| Oba benchmarki                                      | `src/cpp/main.cpp`, `src/python/benchmark.py`             | Placeholdery zgodnie z poleceniem.       |
| Generator, walidator, analiza, główna automatyzacja | `src/automation/`                                         | Placeholdery zgodnie z poleceniem.       |
| Wspólne wejścia i pełne skróty                      | `data/input/`, `manifest.csv`                             | 12 plików.                               |
| Wzorce i małe testy                                 | `data/reference/`, `tests/cases.json`                     | 12 wzorców i testy T01–T08.              |
| Surowe czasy i walidacja                            | `results/raw/`, `results/validated/`                      | 480 rekordów pełnej serii, osobny smoke. |
| Statystyki i ilorazy                                | `results/summary/`                                        | 24 grupy, 12 ilorazów.                   |
| Środowisko, kompilacja, wyjścia i kody              | `logs/`                                                   | Komplet zapisów demonstracyjnych.        |
| Rozgrzewki i kolejność                              | `logs/runs/`                                              | 528 wywołań, w tym 48 rozgrzewek.        |
| Kontrolowany błąd i parser                          | `logs/functional_tests.csv`, `parser_tests.csv`, protokół | Zapis oczekiwanych i uzyskanych reakcji. |
| Raport MD/PDF i obrazy                              | `report/`                                                 | Dostarczono.                             |
| Rejestr dowodów, audyt i retesty                    | `audit/`                                                  | Wypełniono.                              |
| Czysta kopia i przebieg dymny                       | Protokół oraz `logs/smoke_*`                              | Wypełniono.                              |
| Wkład zespołu i AI                                  | `teamwork/`                                               | Wypełniono.                              |
| Prezentacja i obrona                                | `presentation/` oraz raport PDF                           | Tok prezentacji, pytania i próba obrony. |
| Brak plików zakazanych i danych osobowych           | Cała paczka                                               | Do kontroli przed utworzeniem ZIP.       |

Przed oddaniem własnego projektu należy zastąpić treści demonstracyjne własną pracą, wykonać rzeczywiste testy i uzupełnić ślad wykonania. Archiwum ZIP powinno zawierać jeden katalog główny; gotowy EXE, build, cache i środowisko wirtualne nie należą do paczki.
