# Podstawy raportów TiDPI 01–07

Ten plik zawiera wspólny szkielet i dodatki do każdego z siedmiu sprawozdań. Jest szablonem, nie dowodem wykonania zadań. Skopiuj szkielet do pliku `raport.md` odpowiedniej lekcji i uzupełnij go wymaganiami z jej dodatku. Raporty pozostają po polsku. Pola w nawiasach kwadratowych są podpowiedziami, nie wynikami.

Lekcje 00a–00c dostarczają zasad pracy i testowania; obowiązkowy cykl indywidualnych raportów obejmuje 01–07. Każda lekcja ma jeden raport obejmujący także rozszerzenia. Raporty poziomów w repozytorium są dokumentacją pomocniczą do raportu głównego. TiDPI 01 ma etapy i R1–R5, pozostałe zadania poziomy A–D.

Podstawa: lekcja 00a, s. 4–10; 01, s. 9–19; 02, s. 13–15; 03, s. 13–15; 04, s. 10–12; 05, s. 12–14; 06, s. 14–16; 07, s. 6–8. Numery odnoszą się do stron lokalnych PDF-ów. Szkolnych materiałów nie dołączaj do repozytorium ani paczki rozwiązania.

## Jak korzystać z szablonów

- Zachowaj dwanaście sekcji wspólnego szkieletu w podanej kolejności. Dodaj podsekcje wskazane dla konkretnego zadania; załączniki umieść na końcu sekcji 12.
- W sekcji niedotyczącej zadania wyjaśnij dlaczego. W 01 nie ma własnego pomiaru, a w 05–06 czasy pomocnicze nie są benchmarkiem. Nie dopisuj fikcyjnych statystyk.
- Dla 02–07 wyższy poziom obejmuje wcześniejsze. A pozwala uzyskać najwyżej 3, A–B najwyżej 4, A–C najwyżej 5, A–C z wartościowym D najwyżej 6; częściowe A może pozwolić na 2. Zakres nie gwarantuje oceny.
- Używaj wyłącznie przydzielonego kryptonimu. `students_name` oznacza kryptonim, nie imię. Sprawdź także nazwy plików, YAML, właściwości eksportu, logi i zrzuty. W raporcie wskazuj dowody i nazwy plików bez ścieżek katalogów.
- Logi zachowuj bez zmian, włącznie z kropkami, odstępami i błędami. W opisach i opracowaniu stosuj przecinek dziesiętny. Unikaj prywatnych ścieżek podczas zbierania dowodów; konieczną anonimizowaną kopię oznacz, a oryginał zachowaj prywatnie.
- Każda liczba pochodzi z logu zadania albo jest jawnie oznaczona jako fikcyjne dane ćwiczeniowe. Parametry wymagane przez polecenie opisują plan, nie wykonanie.
- Tabele i rysunki wymagają podpisu i przywołania w tekście. Wykres opisuje tę serię na tej maszynie: podaj osie, jednostki, legendę i tabelę źródłową.
- Zapisuj faktyczny toolchain. Zamiennik Visual Studio, debuggera, Excela lub platformy nie dowodzi wykonania kroku wymagającego konkretnego narzędzia. Braki i odstępstwa nazwij wprost.

## Wspólny szkielet do skopiowania

Pole `date` oznacza datę dokumentu; datę eksperymentu podaj osobno. Przy eksporcie z `--number-sections` nie dodawaj ręcznej numeracji nagłówków. Wszystkie podpowiedzi usuń lub zastąp własną treścią przed oddaniem.

Środowisko poniżej uzupełniono na podstawie odczytów z 2026-09-28, zachowanych w `environment.log`. To stan zainstalowanych narzędzi, nie potwierdzenie wykonania eksperymentu lub eksportu. Przed próbami ponownie sprawdź wersje i pozostaw w raporcie narzędzia faktycznie wykorzystane. Kopię logu dołącz jako D00. W TiDPI 01 ten opis dotyczy przygotowania dokumentu; środowisko fikcyjnego testu opisz oddzielnie według pakietu.

````markdown
---
title: "TiDPI [NN] - [temat zadania]"
author: "Kryptonim TiDPI: {{ students_name }}"
date: "YYYY-MM-DD"
lang: pl-PL
---

# Sprawozdanie TiDPI [NN] - [temat zadania]

## Kryptonim TiDPI i wykonany poziom

- Kryptonim: [przydzielony kryptonim].
- Numer i temat lekcji: [NN, temat].
- Data wykonania: [data prób; dla 01 oznacz datę fikcyjnego pakietu].
- Zakres ukończony i sprawdzony: [poziomy albo etapy i R1–R5].
- Elementy nieukończone: [lista i przyczyny albo brak].
- Wersja badanego programu: [wersja lub identyfikator źródła].

## Cel i hipoteza

[Cel, pytanie badawcze i podstawa testu, z której wynika oczekiwany rezultat.]
[Hipoteza zapisana przed serią. Dla 05–06: kryteria powodzenia/odrzucenia. Dla 01: podstawa oceny dostarczonego pakietu, bez udawania planowania historycznych prób.]

## Środowisko oraz konfiguracja

Stan środowiska sprawdzono 2026-09-28. Poniższe wersje opisują dostępne narzędzia; ich użycie w danym zadaniu wymaga potwierdzenia w logach wykonania. Dla TiDPI 01 są to narzędzia autora dokumentu, a nie środowisko fikcyjnego wykonawcy.

Tabela 1 - sprzęt i narzędzia dostępne podczas kontroli środowiska.

| Element                              | Wartość                                                                                   | Dowód                                    |
| ------------------------------------ | ----------------------------------------------------------------------------------------- | ---------------------------------------- |
| System                               | macOS 27.0, kompilacja 26A428                                                             | D00                                      |
| Architektura                         | arm64 (Apple Silicon); sprawdzony proces Python: 64-bitowy, wskaźnik 8 bajtów             | D00                                      |
| Procesor                             | Apple M4 Pro, 14 rdzeni fizycznych i 14 logicznych                                        | D00                                      |
| Pamięć RAM                           | 25 769 803 776 bajtów = 24 GiB                                                            | D00                                      |
| Kompilator C++                       | Apple Clang 21.0.0 (clang-2100.3.34.2), target arm64-apple-darwin27.0.0                   | D00                                      |
| Domyślny interpreter                 | CPython 3.14.4, uruchamiany poleceniem python3                                            | D00                                      |
| Pozostałe interpretery               | Osobny Python 3.13.5 i systemowy Python 3.9.6; [wskaż, jeśli użyto zamiast domyślnego]    | D00, [log próby]                         |
| Debugger                             | LLDB 2103.0.34.103; [uzupełnij dowód użycia w zadaniu]                                    | D00, [Dxx]                               |
| Edytory                              | Visual Studio Code 1.139.1, Cursor 3.21.16, PyCharm 2026.2.1; [pozostaw użyty]            | D00                                      |
| Narzędzia deweloperskie              | Aktywne Command Line Tools; zainstalowany Xcode 26.6                                      | D00, [potwierdzenie wyboru przy próbach] |
| Konwerter dokumentów                 | Pandoc 3.11                                                                               | D00                                      |
| Silnik PDF                           | XeLaTeX: XeTeX 3.141592653-2.6-0.999998, TeX Live 2026, kpathsea 6.4.2                    | D00                                      |
| Dostępne aplikacje dokumentów        | Pages 14.2, Numbers 14.2; [opisz rzeczywiście wykonane kontrole/import]                   | D00, [Dxx]                               |
| Przeglądarka                         | Google Chrome 149.0.7827.201; [jeśli wykorzystano]                                        | D00                                      |
| Automatyzacja                        | PowerShell 7.5.4, CMake 4.1.0; [pozostaw użyte]                                           | D00                                      |
| Narzędzia repozytorium               | Git 2.54.0 (Apple Git-157), Node.js 24.11.1, Bun 1.4.0; [pozostaw istotne]                | D00                                      |
| Standard C++ i ustawienia kompilacji | [Dokładne flagi faktycznej kompilacji; instalacja nie ustala standardu ani Debug/Release] | [Dxx]                                    |
| Warunki podczas eksperymentu         | [Zasilanie, obciążenie, liczba serii i inne faktyczne warunki prób]                       | [Dxx]                                    |

Polecenie g++ w sprawdzonym środowisku wskazuje Apple Clang, nie GNU GCC. Natywne arm64 nie jest platformą x64. Dostępny PowerShell dla macOS nie oznacza środowiska Developer PowerShell z MSVC.

W sprawdzonym terminalu nie znaleziono cl/cl.exe ani gdb, ninja, pdftotext, pdftoppm, pdfinfo i tectonic. W sprawdzonym Pythonie domyślnym i osobnym 3.13.5 nie znaleziono pypandoc ani pypandoc-binary. Zainstalowany Pandoc działa jako osobny program; brak interfejsu Pythona nie oznacza jego braku.

W sprawdzonych katalogach aplikacji macOS nie znaleziono Microsoft Word, Microsoft Excel, LibreOffice ani Visual Studio. Nie sprawdzano środowisk Windows w maszynach wirtualnych. Pages/Numbers i LLDB są dostępnymi narzędziami lokalnymi; opisz odstępstwa od polecenia, a wymaganego użycia Worda/Excela/Visual Studio nie oznaczaj jako wykonanego na podstawie samej ich alternatywy. Wersja XeLaTeX potwierdza dostępność silnika, nie poprawność jeszcze niewykonanego eksportu.

## Zmienne i warunki eksperymentu

[Badane warianty, zmieniany czynnik, warunki stałe.]
[Dane: rozmiar, typ, zakres, układ, generator, seed i przepis odtworzenia, jeśli dotyczą.]
[Liczba prób, rund i rozgrzewek, rotacja kolejności.]
[Zegar, jednostka, rozdzielczość, dokładny zakres stopera i operacje wyłączone. Jeśli nie ma badania czasowego, wyjaśnij to.]

Dla sprawdzonego CPython 3.14.4 perf_counter korzysta z mach_absolute_time(), jest monotoniczny i nie podlega korektom czasu systemowego. Zgłoszona rozdzielczość wynosi około 41,67 ns (D00). To informacja interpretera, nie zmierzona dokładność eksperymentu ani rozdzielczość zegara C++; tę ostatnią ustal oddzielnie, jeśli dotyczy zadania.

## Kontrola poprawności

[Niezależnie ustalony wynik oczekiwany, pełna kontrola wyniku, kompletność danych i identyfikatory dowodów.]
[Wymagany przypadek błędny: oczekiwana i rzeczywista reakcja, kod zakończenia, przywrócenie poprawnej wersji.]
[Niepoprawne lub niekompletne przebiegi zachowaj jako dowody; nie potwierdzają przewagi wydajnościowej.]

## Procedura

1. [Zachowanie bazy i ustalenie kryteriów.]
2. [Przygotowanie danych i konfiguracji; dokładne polecenia bez prywatnych ścieżek.]
3. [Kontrola poprawności i zaplanowana rozgrzewka.]
4. [Próby w zapisanej kolejności; identyfikatory przebiegów.]
5. [Zapis stdout, stderr, kodów i wszystkich wyników.]
6. [Weryfikacja danych, obliczenia i ręczna kontrola wybranych wierszy.]
7. [Przywrócenie stałych i kodu po celowych zmianach.]
8. [Eksport oraz wykonana kontrola dokumentów, jeśli wymagane.]

## Surowe wyniki

### Rejestr dowodów

- D00 - environment.log, odczyty wersji i metadanych środowiska z 2026-09-28; bez pomiarów zadania i bez potwierdzenia eksportu.
- D01 - [nazwa pliku, przypadek/przebieg, co potwierdza].
- D02 - [nazwa pliku, przypadek/przebieg, co potwierdza].

Tabela 2 - przypadki i kontrola zgodności; dostosuj kolumny do zadania, np. dodaj kody i decyzje parsera.

| Przypadek/próba | Dane i wariant | Wynik oczekiwany | Wynik rzeczywisty | Status      | Dowód          |
| --------------- | -------------- | ---------------- | ----------------- | ----------- | -------------- |
| [ID]            | [uzupełnij]    | [z reguły]       | [z logu]          | [PASS/FAIL] | [Dxx, wiersze] |

### Dowód D01 - [podpis]

[Opis dowodu; jeśli cytujesz fragment, oznacz go i podaj wiersze oryginału. Pełne pliki zachowaj jako załączniki.]

```text
[Wklej niezmieniony log; dane ćwiczeniowe wyraźnie oznacz.]
```

[Dodaj wszystkie wymagane przypadki, awarie i kody. Nie zastępuj braków zerami.]

## Opracowanie wyników

[Pogrupuj wyniki według czynników definiujących przypadek i serię. Podaj liczbę poprawnych prób i wiersze źródłowe.]
[Dla pomiarów: minimum, maksimum, rozstęp = maksimum - minimum, mediana. Posortuj wartości; przy parzystej liczbie prób mediana jest średnią dwóch środkowych. Pokaż ręcznie sprawdzone obliczenie.]
[Jednostki w nagłówkach tabel. W 01, 05–06 opracuj przypadki/statusy zamiast statystyk benchmarkowych. Dodaj liczniki, współczynniki, porównania formatów i wykresy wymagane przez zadanie.]

Tabela 3 - opracowanie serii czasowej; stosuj wyłącznie przy odpowiednim badaniu, a [jednostka] zastąp µs albo ns.

| Seria i wariant | Rozmiar/układ/seed | Poprawne próby | Minimum [jednostka] | Maksimum [jednostka] | Rozstęp [jednostka] | Mediana [jednostka] | Dowód          |
| --------------- | ------------------ | -------------: | ------------------: | -------------------: | ------------------: | ------------------: | -------------- |
| [uzupełnij]     | [uzupełnij]        |       [z logu] |            [z logu] |             [z logu] |            [oblicz] |            [oblicz] | [Dxx, wiersze] |

[Rysunek 1 - tytuł, osie, jednostki, legenda, tabela źródłowa.]

## Interpretacja

[Obserwacja i dowody, potem znaczenie. Nie zmieniaj przypuszczenia o przyczynie w stwierdzony fakt.]
[Powtarzalność, wahania, porównanie zakresów. Nakładające się zakresy nie uzasadniają stabilnego zwycięzcy.]

## Ograniczenia eksperymentu

[Dla pomiarów: jedna maszyna, jedna seria i jej warunki; przy powtórzeniu podaj faktyczną liczbę serii i ograniczenia każdej. Rozdzielczość zegara, zakłócenia, wyłączenia stopera, niewykonane konfiguracje.]
[Czas 0 w jednostce zapisu oznacza wynik poniżej tej rozdzielczości, nie zerowy koszt.]
[Dla zadania bez własnych pomiarów wyjaśnij, dlaczego ograniczenia stopera nie dotyczą pracy. Opisz ograniczenia danych, automatu lub parsera i następny test.]

## Wnioski

1. [Odpowiedź na cel z odwołaniem do konkretnych wyników/dowodów.]
2. [Co wykazała ta seria lub zestaw testów i czego nie można uogólnić.]

## Wykorzystanie AI i sposób weryfikacji

- Narzędzie i inne źródła: [zgodnie z prawdą].
- Zakres pomocy: [kod, testy, obliczenia, struktura, redakcja].
- Weryfikacja kodu: [wykonane kontrole i poprawione błędy].
- Weryfikacja danych: [Dxx, numery wierszy, wartości i ręcznie sprawdzone obliczenia].
- Weryfikacja wniosków: [porównanie z wymaganiem, źródłami i logami].
- Pozostałe niewiadome: [co wymaga dalszego sprawdzenia].

### Załączniki i kontrola oddawanej wersji

[Nazwy pełnych źródeł, danych, logów, skryptów i eksportów.]
[Rzeczywiście wykonana kontrola odczytu plików, zasobów i anonimizacji właściwości dokumentów.]
````

## TiDPI 01 - fikcyjny test i publikacja dokumentu

Podstawa: lekcja 01, s. 9–19. Do wspólnego szkieletu dodaj poniższe elementy.

### Sekcje 1–4: zakres, podstawa testu, środowiska i dane

- Wskaż etapy 1–3 i wykonane R1–R5. Dodaj cytat lub uwagę: dane są fikcyjnym materiałem dydaktycznym, nie własnym pomiarem.
- Reguła kosztu: 2 zł za kilometr, minimum 0 zł, maksimum 10 zł. To podstawa wyników oczekiwanych.
- Oddziel środowisko pakietu od narzędzi autora raportu. Fikcyjny pakiet podaje Windows 11 24H2, x86_64, Python 3.13.5, aplikację 0.3.0, datę 2026-08-10 10:15:00. Nie przedstawiaj tego jako własnej konfiguracji.
- Opisz pochodzenie danych oraz ujawnioną po testach implementację, nie udawaj własnego wykonania historycznych prób.

### Sekcje 5–7: przypadki, kontrola, publikacja i dowody

- Przelicz oczekiwania według reguły. Tabela: ID, odległość [km], oczekiwane [zł], rzeczywiste [zł], status. Wypełnij wszystkie TC-01–TC-06 z s. 9; zachowaj pełny, niezmieniony log jako D01. Sprawdź podsumowanie: 1 PASS, 5 FAIL, 6 przypadków.
- Oddzielnie przywołaj kod `min(distance_km + 2, 10)`. Tabela i log to dowód, interpretacja reguły to kolejny krok.
- Etap 1: jeden główny nagłówek, co najmniej cztery sekcje drugiego poziomu, akapit celu, lista środowiska, tabela co najmniej dwóch przypadków, blok `text`, link do dokumentacji Pandoca, cytat o fikcyjności.
- Etapy 2–3: komplet sześciu przypadków, środowisko w tabeli, podgląd Markdown; zapisany wynik `pandoc --version`, dokładne polecenia eksportu, DOCX ze spisem treści i numeracją, PDF.
- Otwórz DOCX/PDF i sprawdź polskie znaki, nagłówki, tabele, log/kod, linki i podział stron. Przy braku silnika PDF zachowaj diagnostykę, wygeneruj standalone HTML, wydrukuj do PDF i opisz tę drogę.
- Odnotuj dwuminutowy przegląd przez inną osobę, jeśli rzeczywiście się odbył; inaczej wskaż niewykonany krok.

### Sekcje 8–12: opracowanie, rozszerzenia i oddanie

- Co najmniej dwie różnice prezentacji MD/DOCX/PDF; statystyki czasu nie dotyczą tego zadania.
- Co najmniej dwa wnioski odwołujące się do TC-xx, trzy ograniczenia oraz następny test, np. dane nienumeryczne, duże liczby, zaokrąglanie, integracja z wyznaczaniem odległości.
- R1: modyfikacja stylów Title, Heading 1, Heading 2, Normal i Source Code; opis co najmniej czterech świadomych zmian; referencyjny i stylowany DOCX.
- R2: `export_reports.ps1`, kontrola źródła, wersja Pandoca, DOCX/HTML/próba PDF, komunikaty każdego eksportu i kontrola dokumentów.
- R3: skrypt `pypandoc`, DOCX, konsola; zależność od binarnego Pandoca, różnica `convert_text()`/`convert_file()`.
- R4: `check_report.py`, reguły struktury; poprawny dokument i uszkodzona kopia z kodami 0/nonzero.
- R5: fixture z tabelą, listą zadań, przekreśleniem, przypisem i YAML; porównanie VS Code, GFM jeśli dostępny, Pandoc HTML.
- Podstawa do oddania: `raport.md`, `raport.docx`, `raport.pdf`; również `raport.html` przy wariancie awaryjnym i artefakty wykonanych rozszerzeń. Wskaż ponownie sprawdzone wiersze pakietu i pomoc AI.

## TiDPI 02 - sortowanie indeksowe i wskaźnikowe

Podstawa: lekcja 02, s. 4–7 i 13–15.

### Sekcje 1–4: pytanie, algorytm i warunki

- Wykonane A–D; hipoteza o wpływie dostępu indeksowego/wskaźnikowego bez wybierania zwycięzcy.
- Faktyczny kompilator, C++17 lub nowszy; Debug dla obserwacji, flagi Release i brak debuggera dla pomiarów.
- Ten sam Bubble Sort, skracanie końca, `swapped`, osobne identyczne kopie wejścia. W obrębie przypadku zmienia się sposób dostępu.
- `steady_clock`, mikrosekundy, tylko sortowanie; generowanie, kopie, `std::sort`, kontrola i output poza pomiarem.

### Sekcje 5–7: poprawność, debugger, próby i rozszerzenia

- A: ręcznie zapisz każdy pełny przebieg `{5, 2, 4, 1}`. Debugger: `i`, `end`, pary wartości, `swapped`; `current`, `next`, dereferencje, `next - current`. Wyjaśnij indeksowanie i przesunięcie wskaźnika.
- Każdy pełny wynik obu funkcji porównaj z `std::sort`; samo uporządkowanie nie dowodzi zachowania wartości.
- B: 1000, 2000, 4000 elementów × pięć prób × dwie implementacje; naprzemienna kolejność i pełne kontrole.
- C: losowe, posortowane, odwrotne × co najmniej trzy rozmiary × pięć prób × obie implementacje; zmiana kolejności.
- D: hipoteza, czynnik zmieniany i warunki stałe oraz surowe dowody np. kodu maszynowego, optymalizacji, wcześniejszego zakończenia lub kolejności.

### Sekcje 8–12: tabele, wykres, wnioski i pliki

- Tabela surowa: rozmiar, rodzaj danych gdy dotyczy, próba, kolejność, `indexed_us`, `pointers_us`, obie poprawności, Dxx.
- Opracowanie osobno dla wariantu/rozmiaru/rodzaju: liczba prób, minimum, maksimum, rozstęp, mediana [µs], wiersze logu.
- B: zmiana czasu po podwojeniu n i powtarzalność przewagi. C: wymagany wykres, najwcześniejsze `!swapped`, wpływ danych na przebiegi i podobieństwo obu implementacji.
- O(n²) nie gwarantuje dokładnie czterokrotnego czasu. Nie przypisuj różnicy cache/aliasingowi bez badania.
- Załącz źródła, pełne logi, debugger, wykres C i dowody D, jeśli wykonano; wskaż kontrole obliczeń i kodu AI.

## TiDPI 03 - trzy sposoby przechowywania tablic

Podstawa: lekcja 03, s. 5–11 i 13–15.

### Sekcje 1–4: warianty, parametry, pamięć

- Hipoteza dotyczy przetwarzania przygotowanych danych. Rozróżnij stały rozmiar, zakres nazwy, czas życia i typowe miejsce pamięci.
- Lokalny/globalny `std::array` oraz dynamiczny `std::unique_ptr<std::uint32_t[]>`; wspólna funkcja, typ, rozmiar i wejście.
- Podaj `element_count`, `rounds`, bajty i KiB. Dane początkowe `i % 1000`; operacja +1 w każdej rundzie.
- Tylko `process_data` wewnątrz stopera; alokacja, inicjalizacja, kontrola, checksum i zwalnianie poza nim.

### Sekcje 5–7: kontrola, adresy, rotacja, awarie

- A: ręczne bajty i KiB (bajty/1024), porównanie z logiem; trzy adresy z debuggera; wyjaśnienie lokalnej, globalnej, lokalnej `static`, dynamicznej tablicy i RAII.
- Sprawdź każdy początkowy element, każdy wynik `i % 1000 + rounds`, pełną równość tablic i dodatkowe checksumy.
- Zachowaj celowo błędne oczekiwanie, wykrycie błędu i przywrócenie kodu.
- B: co najmniej trzy rozmiary, po sześć prób trzech wariantów; przykładowo 5000, 20000, 50000. Stałe `rounds` w serii (bazowo 100); rotacja trzech wariantów i ponowne przygotowanie również globalnej tablicy.
- Zapisz ponowną kompilację po zmianie stałej i przywrócenie po sweepie.
- C: dwa z trzech: oddzielna alokacja ze zwolnieniem; stopniowa granica lokalnej tablicy na kopii projektu; Release x86/x64 z `sizeof(void*)`.
- Granica: bajty, największy uruchomiony i pierwszy nieudany wariant, rzeczywista diagnostyka. Bez awarii nie deklaruj znalezienia granicy.
- D: hipoteza i dowody np. porównania właścicieli pamięci, RAII przy wyjątku, wycieku lub rozmiaru elementu.

### Sekcje 8–12: statystyki, wykres, interpretacja

- Dla rozmiaru i wariantu: wszystkie czasy, minimum, maksimum, rozstęp, mediana [µs]. Przy sześciu próbach średnia trzeciej/czwartej wartości po sortowaniu.
- B wymaga wykresu czasu względem liczby elementów. C opracuj oddzielnie, nie łącz alokacji z przetwarzaniem.
- Nie uogólniaj na „sterta zawsze wolniejsza” ani „x64 zawsze szybsze”; adresy jednej próby nie są uniwersalną mapą pamięci.
- Załącz źródła, pełne logi funkcjonalne/czasowe, debugger, wykres, awarie i wykonane rozszerzenia; rejestr sprawdzonych obliczeń.

## TiDPI 04 - odtwarzanie danych i liczba operacji

Podstawa: lekcja 04, s. 2–5 i 9–12.

### Sekcje 1–4: cel, metryczka, przepis wejścia

- Oddziel odtworzenie danych, wyniku funkcjonalnego i czasu.
- Wersja kodu/generatora, środowisko, konfiguracja, rozmiary, próby i kolejność.
- Świeży `std::mt19937(seed)`, mapowanie `% 10000U`, typ/zakres, sorted/reversed/pseudorandom, algorytm odcisku.
- Tylko instrumentowany Bubble Sort mierzony; comparisons, swaps i passes wewnątrz operacji. Generowanie, odcisk, kopie, wzorzec i kontrola poza nią.

### Sekcje 5–7: odciski, zmiany i serie

- A: n=500, jeden seed, trzy układy, po pięć odcisków i liczników; wykaż stałość wejścia/pracy i wahania czasu.
- Zmień seed: pokaż zmianę pseudolosowych danych i brak wpływu na sorted/reversed; krótko zmień instrukcję generatora, zachowaj efekt i przywróć bazę.
- Kontrola pełnego sortowania względem `std::sort`, każdego `correct` i stałości odcisków/liczników wewnątrz grup.
- B: seed 20260401, n=500, 1000, 2000, 4000, trzy układy, pięć prób, rotacja, Release bez debuggera.
- Zachowaj także bazowy output seeda 20260402, ale nie mieszaj go z grupami analizy B.
- C: dwa z trzech: co najmniej trzy nowe seedy; wersja bez `!swapped` na identycznych danych; prawie posortowane dane z liczbą/metodą zaburzeń.
- D: osobna hipoteza i dowody np. komparatora `std::sort`, odtwarzania pliku, zgodności między środowiskami lub skali logarytmicznej.

### Sekcje 8–12: wzrost, wykres i ograniczenia

- Zachowaj `size;seed;order;trial;time_us;comparisons;swaps;passes;fingerprint;correct` i metadane.
- Czasy/statystyki opracuj według rozmiaru–seeda–układu, a liczniki traktuj jako główny dowód wzrostu.
- Porównaj sorted z `n - 1`, reversed z `n * (n - 1) / 2`; teoria i log w oddzielnych kolumnach.
- Oblicz comparisons(2n)/comparisons(n) dla kolejnych rozmiarów. Przy zerowym mianowniku wzrostu zamian oznacz brak zdefiniowanego ilorazu.
- B: wykres liczby porównań względem n, osobne serie układów, tabela źródłowa.
- Ograniczenia: modulo bias, kolizje odcisku, narzut instrumentacji i wybrane seedy. O(1) pamięci pomocniczej nie oznacza O(1) całego wejścia.
- Załącz pełne źródła/logi, odciski, opracowanie i wykres; wskaż ręcznie sprawdzone wzory i logi oraz pomoc AI.

## TiDPI 05 - automat build → run → evidence

Podstawa: lekcja 05, s. 2–4 i 9–14.

### Sekcje 1–4: kryteria sukcesu, środowisko i schemat

- Kryteria: świeży program, zachowane dowody, poprawne rozpoznanie niepowodzeń.
- Faktyczny kompilator/Python; wyjaśnienie wykonanej komendy i flag. Dla MSVC: standard, wyjątki, ostrzeżenia, zgodność, UTF-8, wyjście; Release `/O2 /MD`, Debug `/Od /MDd`.
- Schemat źródło → usunięcie starego wygenerowanego EXE → build → kod i nowy EXE → run albo zatrzymanie → evidence.
- Strumienie, kody, timeouts, lista argumentów, `shell=False`, osobne przebiegi. Czasy procesów to metadane, nie benchmark algorytmu.

### Sekcje 5–7: sukces, awaria wykonania i kompilacji

- A: dostępność narzędzi, ręczny build/run, komendy i kod; dwa release/pass z różnymi katalogami i dowodem braku nadpisania.
- Powiąż `passed` z kodem kompilacji, świeżym artefaktem, wynikiem funkcjonalnym i kodem programu.
- B: release/fail; stdout, diagnostyka stderr, kod programu 1 i skryptu 1. Oznacz symulację jako test automatu.
- Błąd składni: diagnostyka, niezerowy kod kompilacji, `execution_attempted=false`, brak starego EXE; brak logów run jest oczekiwany.
- Przywróć źródło i pokaż następny sukces. Wyjaśnij `environment_error`, `compile_failed`, `run_failed`.
- Rejestr dowodów: osobne `compile_stdout.txt`, `compile_stderr.txt`, `run_stdout.txt`, `run_stderr.txt`, `summary.txt` i ich role.
- C: dwa z trzech: `--repeat` 1–10, pliki/kody każdej próby nawet po awarii; walidowany/zapisany `--size`; manifest rozmiaru/mtime źródła i EXE. Testy sukcesu i błędów.
- D: własny problem i sprawdzone rozwiązanie np. SHA-256, osobnych statusów, konfiguracji lub CI.

### Sekcje 8–12: tabela przebiegów i granice automatu

- Tabela: ID, konfiguracja/przypadek, oczekiwany status, kod build, podjęcie run, kod programu, kod skryptu, rzeczywisty status, dowody.
- Niepodjęty etap oznacz „nie uruchomiono”, nie kodem 0. Sprawdź tabelę z summary i strumieniami.
- Wyjaśnij blokadę starego EXE i umowę kodów. Sam napis OK, timestamp lub nazwa pliku nie dowodzi poprawności treści.
- Ograniczenia środowiska, timeoutów, kodowania i sprawdzonych ścieżek. Nie obliczaj statystyk sortowania z czasów całych procesów.
- Załącz `main.cpp`, `run_experiment.py`, pełne artefakty sukcesów/awarii i rozszerzenia; w AI opisz kontrolę gałęzi decydujących o uruchomieniu.

## TiDPI 06 - kontrakt, parser i CSV

Podstawa: lekcja 06, s. 2–4 i 13–16.

### Sekcje 1–4: kryteria akceptacji i schemat

- Cel: rozdzielenie parsowania, walidacji i rezultatu testu; wersje producenta/parsera.
- Protokół `TIDPI_RESULTS;1`; nagłówek `case;size;trial;time_us;comparisons;correct`, separator `;`.
- case: sorted/reversed/random; size całkowite ≥ 2; trial całkowite ≥ 1; czas/licznik całkowite ≥ 0; correct dokładnie true/false.
- Kodowanie UTF-8 z obsługą BOM, `csv`, `DictWriter`, `newline=''`, jednostka w nagłówku, unikalność trójki case/size/trial, co najmniej jeden rekord.
- Publikacja po walidacji całego zestawu. `correct=false` jest poprawnym opisem nieudanego testu.

### Sekcje 5–7: dane poprawne, odrzucone i nieudany test

- A: producent Release, raw output, stdout/stderr/kod parsera; dokładnie 18 rekordów: trzy układy × rozmiary 16/32 × trzy próby.
- CSV sprawdź w edytorze, przez import UTF-8/`;` w Excelu i ponowny odczyt `csv` z liczbą rekordów. Wyjaśnij parsowanie/walidację na przykładzie.
- B: invalid-number, missing-field, duplicate-row, wrong-version → oczekiwany kod parsera 2, reguła/numer wiersza na stderr, brak CSV. Zapisz rzeczywiste decyzje.
- Przed jednym błędem pozostaw poprawny stary CSV; wykaż usunięcie i brak nowego. Surowe wejście musi pozostać osobnym plikiem.
- failed-test → poprawna struktura, CSV zachowuje false, kod parsera 1. Poprawne dane i same true → CSV i kod 0.
- Kody producenta i parsera zapisz oddzielnie; wadliwy kontrakt może być celowo wyemitowany z kodem producenta 0.
- Dxx łączy wejście, diagnostykę, kod i publikację. Twórz oddzielne oznaczone fixture, nie poprawiaj oryginałów.
- C: dwa z trzech: v2 z seed i odrzucenie przez v1; kompletność wykrywająca brak/nadmiar; note ze średnikiem/cudzysłowem i poprawne CSV escaping.
- D: co najmniej dziesięć różnych fixture, granice/kombinacje, automat, uzasadniony model zagrożeń danych i dowody akceptacji/odrzucenia.

### Sekcje 8–12: macierz decyzji i ograniczenia

- Tabela: fixture/tryb, reguła, wiersz, oczekiwany i rzeczywisty kod, oczekiwany i rzeczywisty CSV/brak, status testu parsera, dowód.
- Rozróżnij błąd odczytu, struktury, wartości oraz poprawne dane nieudanego testu.
- Pokaż liczbowe time_us/comparisons bez jednostek w komórkach; małych czasów nie traktuj jako benchmarku.
- Ograniczenia: wybrane reguły/fixture, brak domyślnej kontroli kompletności w bazie, ustawienia importu. Plik istniejący w Excelu nie zastępuje walidacji.
- Załącz producenta, parser, wszystkie wejścia, strumienie/kody, poprawne CSV, rozszerzenia; wskaż sprawdzenie odrzucania i all-or-nothing.

## TiDPI 07 - benchmark C++ i Python

Podstawa: lekcja 07, s. 2–8.

### Sekcje 1–4: pytanie, wspólny wynik i warunki

- Hipoteza o konkretnych implementacjach i wspólny oczekiwany wynik przed pomiarem. Ręczna operacja uzgodniona z prowadzącym; suma kwadratów to przykład z demonstracji.
- Sprzęt/system, kompilator i rzeczywisty C++ Release, Python, wersje źródeł.
- A: wspólny plik co najmniej 10000 liczb; liczba, seed, generator, zakres, odcisk/checksum. Osobne generowanie z tym samym seedem nie dowodzi wspólnego wejścia.
- Ta sama ręczna pętla i rounds; sprawdzenie zakresu typu C++ i oczekiwania niezależnego od porównywanych programów.
- Co najmniej dwie ustalone rozgrzewki i dziesięć właściwych prób na implementację; kolejność zmieniana, programy uruchamiane kolejno. Rozgrzewki oddzielone od analizy.
- `steady_clock` w ns i `perf_counter_ns()`; tylko obliczenia, bez I/O, przygotowania, outputu i walidacji.

### Sekcje 5–7: walidator, błąd i powtórzenie

- Checksum każdego programu zgodny z niezależnym oczekiwaniem; dowód wspólnego pliku i wykorzystania wyniku.
- Format `language;trial;time_ns;checksum;correct`; pełne rekordy, stdout/stderr/kody.
- B: automat i walidacja nagłówka, typów, liczby prób, jednostek, checksumów; zachowany zwalidowany CSV.
- Celowo zmień implementację lub dane i wykaż odrzucenie porównania; zachowaj diagnozę i przywrócenie poprawnej wersji.
- Powtórz cały eksperyment w osobnym przebiegu; oznacz serie i porównaj główny wniosek, bez anonimowego łączenia wyników.
- C: dwa z pięciu: osobne Debug/Release; co najmniej trzy rozmiary; brak/ustalona rozgrzewka; ręczna pętla/biblioteka jako różne implementacje; uzasadnione rounds. Jeden czynnik na badanie.
- D: własna hipoteza, kontrola i dowody np. kalibracji, losowania kolejności, pełnej metryczki, rozkładu lub funkcji spoza interpretera.

### Sekcje 8–12: statystyki, druga seria i paczka

- Osobno dla implementacji, serii i konfiguracji: wszystkie czasy, liczba poprawnych prób, minimum, maksimum, rozstęp, mediana [ns].
- Przy dziesięciu próbach mediana to średnia piątej/szóstej wartości po sortowaniu. Minimum to najkrótsza obserwacja; mediana opisuje środek serii. Wyjaśnij różnicę tych pytań.
- Porównaj wnioski obu serii. Ilorazy/procenty wskazują liczby źródłowe; nie dziel przez zero.
- Ograniczenia: jedna maszyna, faktyczna liczba serii, zakłócenia, rozdzielczość odrębna od jednostki ns, wyłączenia i optymalizacja.
- Wniosek dotyczy tego kodu, danych, rounds i konfiguracji, nie uniwersalnej szybkości języków.
- Paczka: MD i wygenerowany DOCX albo PDF, źródła obu języków, generator, wspólny plik albo jednoznaczne odtworzenie, automat, raw obu implementacji, zwalidowany CSV, logi/kody, dowody; kontrola eksportu i anonimizacji.

## Kontrola każdego raportu przed oddaniem

- [ ] Dwanaście sekcji i właściwe wymagania zadania są obecne.
- [ ] Zakres ukończony zgadza się z dowodami; braki i odstępstwa nazwano.
- [ ] Oczekiwania pochodzą z reguły; wyniki i wszystkie próby z właściwych logów.
- [ ] Awarii, niepełnych przebiegów i kodów nie ukryto; dowody mają identyfikatory.
- [ ] Arytmetykę sprawdzono ręcznie i wskazano źródłowe wiersze.
- [ ] Wykresy mają podpisy, jednostki, osie, legendę i tabelę źródłową.
- [ ] Interpretacja odróżnia obserwację od przypuszczenia i uwzględnia ograniczenia.
- [ ] Pełne źródła/załączniki dają się odczytać po przeniesieniu paczki.
- [ ] Wymagane eksporty otwarto i obejrzano, a nie tylko utworzono.
- [ ] Finalny raport nie zawiera podpowiedzi ani danych osobowych.
- [ ] Pomoc AI ujawniono i można wyjaśnić kod, obliczenia oraz wnioski.

Do pakowania użyj `bun run bundle TiDPI_NN` według [instrukcji manifestu i zatwierdzania](../../scripts/BUNDLE.md). Lista `artifacts` musi obejmować wszystkie pliki wymagane przez ukończony zakres. Dopiero po powyższej ręcznej kontroli wpisz wskazany `reviewedContentSha256` do `submission.json`; kontrola struktury przez skrypt nie dowodzi poprawności eksperymentu ani zgodności eksportu z raportem.
