# Rejestr dowodów — E01-DEMO

**Wersja końcowa:** 14.11.2026. Ścieżki poniżej odnoszą się do katalogu głównego projektu. Rejestr wskazuje konkretny materiał do sprawdzenia, nie zastępuje jego treści. Dokument należy do zestawu opisanego w README.

| ID  | Deklaracja                                 | Artefakt                                                                       | Sposób kontroli                                                                      |
| :-- | :----------------------------------------- | :----------------------------------------------------------------------------- | :----------------------------------------------------------------------------------- |
| D01 | Oba warianty otrzymały identyczne wejście. | `data/manifest.csv`, `data/input/`, `logs/runs/*.jsonl`                        | Porównanie pełnych SHA-256 plików i `input_sha256` zapisanych przy wywołaniach.      |
| D02 | Do analizy przyjęto 480 poprawnych prób.   | `results/raw/e01.csv`, `results/validated/e01.csv`, `validation_summary.json`  | Liczba kluczy, komplet trial 1–20, 24 grupy, zgodne skróty wyników i `correct=true`. |
| D03 | Testy sprawdzają pełny wynik.              | `tests/cases.json`, `data/reference/`, `logs/functional_tests.csv`             | Porównanie wyniku z pełnym wzorcem; T07 ma wykryć zmianę wartości.                   |
| D04 | Nieprawidłowa seria nie jest publikowana.  | `logs/parser_tests.csv`, `audit/kontrolowany_blad.md`                          | Oczekiwane REJECT dla braku, duplikatu, złego czasu, przypadku i skrótu.             |
| D05 | C++ zbudowano w Release x64.               | `logs/compile_summary.txt`, `compile_stdout.txt`, `compile_stderr.txt`         | Pełne polecenie, `/O2`, konfiguracja i kod zakończenia 0.                            |
| D06 | Środowisko zostało opisane.                | `logs/environment.txt`                                                         | System, CPU, RAM, wersje i nieustalony tryb zasilania.                               |
| D07 | Zachowano kolejność i rozgrzewki.          | `logs/runs/index.csv`, 12 plików JSONL, `logs/run_summary.json`                | 528 wywołań, w tym 48 rozgrzewek; naprzemienne pozycje wariantów.                    |
| D08 | Czasy tabel dotyczą jednego sortowania.    | `results/raw/e01.csv`, `results/summary/statistics.csv`                        | Podział time_ns przez rounds i 1 000 000 przed statystykami.                         |
| D09 | Statystyki i wykres są zgodne.             | `results/summary/summary.json`, `report/images/ilorazy.png`, raport            | Kontrola median, rozrzutu i 12 ilorazów.                                             |
| D10 | H1 zachowała pierwotne kryterium.          | `plan/karta_E01.md`, `recenzja_planu.md`, `dziennik_decyzji.md`, `ocena_H1.md` | Daty, próg 10, zakres wszystkich 12 przypadków, odpowiedź 9/12.                      |
| D11 | Wysoki poprawny czas pozostawiono.         | CSV, tabela 5 raportu                                                          | 119 ms dla CPythona w random_1000; średnia 72,1 ms, mediana 70 ms.                   |
| D12 | Poprawki sprawdzono ponownie.              | `audit/protokol_audytu.md`, `retesty.md`                                       | Zamknięcie A-01 i A-02 na podstawie zapisanej kontroli.                              |
| D13 | Sprawdzono instrukcję odtworzenia.         | `audit/protokol_czystej_kopii.md`, logi smoke                                  | Osobny identyfikator E01-SMOKE, 2 rekordy, kod 0.                                    |
| D14 | Udokumentowano wkład i użycie AI.          | `teamwork/dziennik_pracy.md`, `wykorzystanie_AI.md`                            | Zadanie, rezultat, dowód; przyjęcie lub odrzucenie sugestii i weryfikacja.           |
| D15 | Przygotowano obronę całości.               | `presentation/prezentacja_i_obrona.md`, `proba_obrony.md`                      | Tok wypowiedzi oraz pytania do obu partnerów z drogą do dowodów.                     |

Pliki w `src/` wskazują miejsca dostarczenia kodu. Zgodnie z zakresem demonstracji zawierają komentarze zamiast implementacji; rejestr nie stanowi potwierdzenia ich uruchamialności.
