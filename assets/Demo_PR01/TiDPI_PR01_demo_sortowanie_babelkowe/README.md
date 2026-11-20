# Projekt 01 — Bąbelkowy pojedynek

**Zespół:** `demo`. **Eksperyment:** E01. **Seria wynikowa:** E01-DEMO.

> Zestaw jest kompletnie wypełnionym przykładem dydaktycznym z danymi i dokumentami demonstracyjnymi. Zgodnie z przeznaczeniem zestawu wszystkie pliki źródłowe zawierają wyłącznie komentarze-placeholdery. Opisane niżej uruchomienia przedstawiają docelową instrukcję pracy uczniowskiej, a nie działający benchmark w tej kopii. Materiały oznaczają strukturę i oczekiwany rezultat; we własnym projekcie należy dostarczyć działający kod i rzeczywiste dowody.

## Cel i pytanie badawcze

Porównanie własnych implementacji sortowania bąbelkowego w C++ Release i CPythonie na identycznych danych. H1 wymaga ilorazu median Python / C++ co najmniej 10 w każdym z 12 przypadków. Plan zawiera 3 rozmiary, 4 układy, 2 rozgrzewki i 20 prób na wariant oraz przypadek.

## Od czego zacząć przegląd zestawu?

1. [Karta E01](plan/karta_E01.md) — pytanie, H1 i plan przed pomiarami.
2. [Raport PDF](report/raport.pdf) lub [Markdown](report/raport.md) — sposób opisania wykonanej pracy.
3. [Ocena H1](plan/ocena_H1.md) — wszystkie 12 porównań i odpowiedź na hipotezę.
4. [Rejestr dowodów](audit/rejestr_dowodow.md) — przejście od deklaracji do konkretnego pliku.
5. [Lista kompletności](audit/lista_kontrolna.md) — sprawdzenie paczki.
6. [Tok prezentacji i obrona](presentation/prezentacja_i_obrona.md) — wypowiedź z użyciem stron raportu PDF.

## Wymagania docelowego projektu

Windows x64, narzędzia C++ Visual Studio z MSVC, Python 3.10 lub nowszy. W przykładowej serii opisano MSVC 19.40 i CPython 3.12.7. Do otwarcia raportu nie jest potrzebna instalacja Pandoca. Źródłem dokumentu jest Markdown; przykład eksportu przewiduje Pandoc, HTML5 i skład do PDF w Chromium.

## Jedno główne polecenie — pełna seria

W katalogu głównym projektu, z przygotowanej konsoli narzędzi C++ x64:

```powershell
python src/automation/run_benchmark.py --config plan/config_E01.json
```

Docelowo polecenie sprawdza środowisko i dane, kompiluje C++ w Release, uruchamia warianty, zachowuje wyjścia i kody, waliduje wyniki i wyznacza statystyki. W razie błędu nie publikuje częściowej serii. W demonstracji należy przeglądać dostarczone wyniki; wykonanie pliku-placeholdera nie wykona powyższych czynności.

## Krótki przebieg kontrolny

```powershell
python src/automation/run_benchmark.py --smoke --run-id E01-SMOKE
```

Oczekiwany rezultat: kod 0, `VALIDATION: PASS`, dwa rekordy w `results/raw/e01_smoke.csv`. Przykładowy zapis znajduje się w `logs/smoke_stdout.txt`. Przebieg dymny nie zastępuje właściwej serii i nie należy do jej statystyk.

## Odtworzenie analizy i raportu

```powershell
python src/automation/analyze_results.py
python dokumentacja_eksportu/eksportuj_pdf.py
```

Docelowe wyniki to `results/summary/statistics.csv`, `summary.json` i `report/raport.pdf`. Oba wskazane pliki Python również są placeholderami. Wartości można prześledzić ręcznie: `time_ns / rounds / 1 000 000`, grupowanie po przypadku i implementacji, mediana 20 wartości, a następnie iloraz median Python / C++.

## Katalogi i kontrakt

- `plan/`: karta 1.0, recenzja, dziennik decyzji, konfiguracja i ocena H1.
- `src/`: miejsca na oba benchmarki i cztery skrypty automatyzacji.
- `data/`: wspólne wejścia, wzorce i manifest z pełnymi SHA-256.
- `results/raw/`: komplet 480 rekordów E01-DEMO i osobny przebieg dymny.
- `results/validated/`: dane przyjęte do analizy oraz wynik kontroli.
- `results/summary/`: statystyki, ilorazy i podstawa wniosku.
- `logs/`: środowisko, kompilacja, kalibracja, testy i wszystkie 528 wywołań (48 rozgrzewek + 480 właściwych prób).
- `report/`: raport MD i PDF oraz wykres.
- `audit/`: rejestr dowodów, ustalenia, retesty i kontrola czystej kopii.
- `teamwork/`: dziennik pracy i weryfikacja użycia AI.
- `tests/`: małe wejścia i oczekiwane wyniki, w tym kontrolowany błąd.
- `presentation/`: tok prezentacji na podstawie raportu PDF i próba obrony.

Każdy plik JSONL w `logs/runs/` zawiera 44 wywołania danego przypadku. Każdy wpis zachowuje polecenie, stdout, stderr, kod zakończenia i identyfikację wejścia. Indeks ma 528 wierszy. Puste pliki stderr oznaczają brak komunikatów błędu, nie brak dokumentu.

## Kody zakończenia i poprawność

Kod 0: sukces. Kod 1: niezgodność wyniku. Kod 2: błąd środowiska lub kontraktu. Próby T07/T08 i testy parsera mają sprawdzać również poprawne odrzucanie danych. Status PASS w takim teście oznacza zgodność z oczekiwaną reakcją, a nie przyjęcie błędnego wyniku.

## Wynik i ograniczenia

H1 nie jest wsparta w pełnym zakresie: próg spełnia 9 z 12 przypadków. Trzy przypadki rosnące mają R = 8. Pozostałe rodzaje dają R = 35, 36 i 32. Nie usunięto wysokiego poprawnego czasu 119 ms. Wniosek ograniczono do opisanych implementacji, wejść, jednej sesji i stanowiska.

## Przygotowanie paczki do oddania

Docelowo należy wykonać kontrolę według `audit/protokol_czystej_kopii.md`, a następnie wyłączyć z kopii do oddania EXE, pliki pośrednie, katalogi budowania, projekty Visual Studio, środowiska wirtualne, cache, prywatne ścieżki i sekrety. Zachowuje się kod, dane i logi. W tej paczce nie ma artefaktów budowania. ZIP zawiera jeden katalog główny nazwany dokładnie jak archiwum.
