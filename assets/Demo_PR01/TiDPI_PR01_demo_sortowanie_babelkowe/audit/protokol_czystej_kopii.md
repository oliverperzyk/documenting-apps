# Protokół odtworzenia z czystej kopii

**Data:** 14.11.2026. **Rola odtwarzająca:** partner_B. **Podstawa:** README bez ustnych wskazówek autora. **Identyfikator kontroli:** E01-SMOKE, odrębny od serii raportowej.

| Krok                         | Oczekiwany rezultat                                 | Zapis rezultatu                                |
| :--------------------------- | :-------------------------------------------------- | :--------------------------------------------- |
| Kopia bez kompilatów i cache | Zachowane źródła, dane i konfiguracja.              | Kontrola struktury — zgodna.                   |
| Sprawdzenie narzędzi         | MSVC i Python dostępne w przygotowanej konsoli.     | Wersje zgodne z metryczką.                     |
| Budowanie Release x64        | Kod 0.                                              | `logs/compile_summary.txt`.                    |
| Przebieg dymny               | Kod 0, VALIDATION: PASS.                            | `logs/smoke_stdout.txt`, `smoke_summary.json`. |
| Kontrola wyniku              | 2 rekordy, właściwy schemat, brak błędnych wyników. | `results/raw/e01_smoke.csv`.                   |
| Otwarcie dokumentów          | Raport MD i PDF, poprawne obrazy.                   | Kontrola zakończona zgodnością.                |
| Ochrona serii źródłowej      | E01-DEMO nie zostaje nadpisane.                     | Wyniki kontroli mają osobny identyfikator.     |
| Ponowne oczyszczenie kopii   | Brak EXE, obiektów, build i cache.                  | Kontrola końcowa zgodna.                       |

Przebieg dymny służy sprawdzeniu podstawowej ścieżki. Nie potwierdza powtórzenia wszystkich 480 czasów i nie zastępuje pełnego benchmarku. Różnica czasów przy niezależnym uruchomieniu nie jest sama w sobie błędem odtworzenia.

Dokument przedstawia wzorcowy zapis kontroli w oddawanym projekcie. W udostępnionej demonstracji źródła zastąpiono komentarzami, zgodnie z README; tego protokołu nie należy traktować jako potwierdzenia uruchomienia plików-placeholderów.
