# Roadmap — licznik słów

Checklista realizacji [zadania grupowego](assets/TASK.md). Etapy wykonujemy w podanej kolejności: najpierw poprawność, potem pomiary i opracowanie wyników. Punkt oznaczamy jako ukończony dopiero po sprawdzeniu jego rezultatu.

## 1. Ustalenie zasad i podział pracy

- [x] Zapisać definicję słowa: niepusty ciąg znaków rozdzielany wyłącznie spacją, tabulatorem lub LF. Interpunkcja pozostaje częścią słowa.
- [x] Ustalić przed pomiarami co najmniej trzy długości tekstu, warianty danych, liczbę powtórzeń, jednostkę czasu i kolejność uruchamiania implementacji.
- [ ] Zapisać pytanie badawcze oraz hipotezę bez zakładania z góry, która implementacja będzie szybsza.

## 2. Dane i oczekiwane wyniki

- [x] Przygotować pliki ASCII lub deterministyczny generator z zapisaną konfiguracją, ziarnem losowania, jeśli jest używane, i instrukcją odtworzenia danych.
- [x] Przygotować warianty obejmujące krótkie i długie słowa oraz mały i duży udział separatorów dla każdej wybranej długości tekstu.
- [x] Przygotować wspólny zestaw danych wejściowych; zapisać rozmiar w bajtach i identyfikator lub sumę kontrolną każdego pliku.
- [x] Podłączyć wspólny zestaw danych do obu implementacji, zapewniając im dokładnie te same dane wejściowe.
- [x] Wyznaczyć oczekiwane liczby słów niezależnie od porównania wyników obu programów.
- [x] Przygotować testy: pusty tekst → `0`, same spacje/tabulatory/LF → `0`, jedno słowo bez separatora na końcu → `1`.
- [x] Przygotować testy: `Ala  ma` → `2`, `Ala\tma\nkota` → `3`, `kot,pies` → `1`.
- [x] Sprawdzić separatory na początku i końcu tekstu, wielokrotne separatory oraz ich mieszanki.
- [x] Sprawdzić, że inne znaki ASCII, np. CR (`\r`), nie są traktowane jako separatory: `Ala\rma` → `1`.

Przygotowano `WordGenerator.py`, słownik 250 angielskich słów w `assets/english_words.json` oraz 15 plików benchmarkowych w `data/`: po pięć dla 1000, 100000 i 1000000 bajtów, z ziarnami odpowiednio 14, 42 i 2026. Manifesty zawierają konfigurację, oczekiwane liczby słów i SHA-256. Zweryfikowano rozmiary, ASCII, oczekiwane liczby słów, sumy kontrolne oraz powtarzalność generowania. Przypadki kontrolne są zdefiniowane w `WordGenerator.FIXTURES`; uruchomienie ich na implementacjach C++ i Python pozostaje do wykonania.

## 3. Implementacje i kontrola poprawności

- [x] Napisać w C++ pętlę przeglądającą tekst znak po znaku, z licznikiem ustawionym na `0` i stanem `inWord` ustawionym na fałsz.
- [x] Napisać w Pythonie ten sam algorytm i te same przejścia stanu.
- [x] Zwiększać licznik wyłącznie przy wejściu w nowe słowo; nie doliczać osobno słowa po końcu tekstu.
- [x] Nie używać `split`, gotowego licznika słów ani ogólnego rozpoznawania białych znaków rozszerzającego listę separatorów.
- [x] Oddzielić funkcję liczącą od wczytywania plików, pomiaru, walidacji i wypisywania wyników; przy odczycie zachować rozróżnienie LF i CR.
- [x] Uruchomić wszystkie testy w obu językach i porównać wyniki z oczekiwaniami.
- [x] Sprawdzić poprawność także na wszystkich plikach przeznaczonych do benchmarku.

## 4. Automatyczny benchmark

- [x] Przygotować kompilację C++ z optymalizacją i zapisać dokładne flagi; pomiary wykonywać bez debuggera.
- [x] Wczytywać dane przed rozpoczęciem pomiaru. Mierzyć wyłącznie algorytm wraz z utworzeniem wyniku, bez odczytu, zapisu, drukowania i kontroli poprawności.
- [x] Użyć zegarów monotonicznych i opisać ich jednostkę oraz rozdzielczość.
- [x] Przygotować skrypt uruchamiający wielokrotne próby dla obu języków, wszystkich długości i wariantów danych.
- [x] Uruchamiać porównywane programy sekwencyjnie i zmieniać kolejność języków między próbami. Jeśli stosowane są rozgrzewki, ustalić ich liczbę wcześniej i oddzielić je od właściwych pomiarów.
- [x] Poza pomiarem porównywać wynik każdej próby z oczekiwaną liczbą słów; błędne próby wykluczać ze statystyk, zachowując informację o odrzuceniu i jego przyczynie.
- [x] Obsłużyć błędy kompilacji i uruchomienia; nie uruchamiać starego pliku wykonywalnego po nieudanej kompilacji.
- [x] Zapisywać surowe czasy do CSV wraz z językiem, identyfikatorem danych, długością tekstu, wariantem, numerem próby, jednostką i statusem poprawności.
- [x] Sprawdzić automat na małym zestawie i celowo błędnym wyniku, aby potwierdzić odrzucanie niepoprawnych prób.
- [x] Wykonać pełny benchmark i zachować wszystkie pomiary w osobnym katalogu przebiegu, bez nadpisywania wcześniejszych wyników.

Automat: `Benchmark.py`; metoda i instrukcja: [BENCHMARK.md](BENCHMARK.md). Przeszło 11 testów automatu, w tym celowo błędny wynik. Mały przebieg: 20/20 poprawnych prób w `results/20261026T184237Z_ec1201df18/`. Pełny przebieg: 900/900 poprawnych prób, bez odrzuceń, w `results/20261026T184323Z_8894299b2b/` (30 prób na każdą parę język–plik, bez rozgrzewek). Zweryfikowano kompletność CSV, naprzemienną kolejność i zgodność sum kontrolnych źródeł. Do późniejszych statystyk dopuszczamy wyłącznie wiersze `status == valid`.

## 5. Analiza i raport Markdown

- [ ] Sprawdzić kompletność CSV: dla każdej kombinacji języka, długości i wariantu musi być zaplanowana liczba poprawnych prób; braki opisać i wyjaśnić.
- [ ] Obliczyć medianę, minimum, maksimum i rozstęp osobno dla każdej kombinacji. Dla parzystej liczby prób medianę liczyć jako średnią dwóch środkowych wartości po sortowaniu.
- [ ] Zachować czasy równe `0` i obserwacje skrajne; wyjaśnić ograniczenia rozdzielczości zegara zamiast usuwać niewygodne pomiary.
- [ ] Przygotować wykresy porównujące mediany i rozrzut czasów dla długości i wariantów danych; dodać tytuły, jednostki, legendy i odwołania do źródłowego CSV.
- [ ] Umieścić obrazy w podkatalogu i podłączyć je w raporcie ścieżkami względnymi.
- [ ] Napisać `raport.md`: cel i hipoteza, definicja słowa, algorytm, dane, oczekiwane wyniki testów, metoda pomiaru oraz liczba powtórzeń.
- [ ] Opisać faktyczny sprzęt, system, wersje kompilatora i Pythona, flagi kompilacji, zegary oraz polecenia uruchomienia.
- [ ] Dodać wyniki, wykresy, omówienie odrzuconych prób, ograniczenia i wnioski odnoszące się do zebranych danych. Oddzielić obserwacje od przypuszczeń o ich przyczynach.
- [ ] Udokumentować podział pracy oraz wykorzystanie AI i sposób weryfikacji jej wyników. Sprawdzić, czy materiały nie ujawniają danych osobowych ani prywatnych ścieżek.

## 6. Eksport PDF i odbiór końcowy

- [ ] Przygotować krótką instrukcję kompilacji, uruchomienia testów, wygenerowania danych i wykonania benchmarku.
- [ ] Wyeksportować profesjonalnie złożony PDF przez Pandoc i zapisać dokładne polecenie eksportu oraz wymagane narzędzia.
- [ ] Otworzyć PDF i sprawdzić każdą stronę: polskie znaki, tabele, wykresy, podpisy, kod, odnośniki, podział stron oraz brak uciętej treści i artefaktów wydruku z przeglądarki.
- [ ] Porównać PDF z Markdownem i potwierdzić zgodność treści, liczb i wykresów.
- [ ] Ręcznie przeliczyć wybrane wyniki z CSV i porównać je z tabelami oraz wykresami.
- [ ] Sprawdzić komplet oddawanych materiałów: oba programy, automat benchmarku, instrukcja, dane lub generator, testy z oczekiwaniami, surowy CSV, raport MD, obrazy i PDF.
- [ ] Przejść instrukcję na czystym zestawie plików i potwierdzić, że wyniki można odtworzyć, a każdy członek zespołu potrafi wyjaśnić swoją część.
