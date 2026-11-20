# Recenzja planu eksperymentu E01

> Materiał dydaktyczny: wypełniony dokument fikcyjnego zespołu, należący do wzorca Projektu 01.

**Data:** 7.11.2026. **Recenzent:** `partner_B`. **Autor planu:** `partner_A`. **Przedmiot recenzji:** karta E01 przed zamrożeniem wersji 1.0. **Planowany przebieg:** E01-DEMO.

## 1. Cel przeglądu

Sprawdzono, czy plan pozwala ocenić H1 bez zmiany zasad po poznaniu wyników. Recenzja dotyczy kompletności metody. Nie potwierdza jeszcze poprawności nieukończonego kodu, działania walidatora ani wyników przyszłej serii.

H1 wymaga ilorazu median CPython / C++ Release co najmniej 10 **dla każdego z 12 przypadków**. To silniejszy warunek niż sama niższa mediana C++. Plan musi przewidywać możliwość niespełnienia tego progu.

## 2. Uwagi i ich rozstrzygnięcie

| ID   | Uwaga do wersji roboczej                                                                            | Uzgodnione uzupełnienie wersji 1.0                                                                                              |
| :--- | :-------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------ |
| R-01 | „Python ma być dziesięć razy wolniejszy” nie określa miary ani zakresu.                             | Zapisano iloraz median czasu jednej operacji i warunek R ≥ 10 w każdym z 12 przypadków.                                         |
| R-02 | Trzecia linia danych nie musi być medianą; prób będzie 20.                                          | Zapisano porządkowanie czasów i średnią dwóch środkowych wartości.                                                              |
| R-03 | Kolejne sortowania tej samej tablicy zmieniłyby zadanie na sortowanie danych rosnących.             | Każda runda otrzyma świeżą kopię wejścia przygotowaną przed zegarem.                                                            |
| R-04 | Ten sam seed w osobnych generatorach nie gwarantuje wspólnego wejścia.                              | Oba programy będą czytać te same pliki, weryfikowane pełnym SHA-256.                                                            |
| R-05 | Sama suma lub skrót bez kontroli pełnego wyniku może ukryć pomyłkę.                                 | Wynik każdej rundy będzie porównywany w całości ze wspólnym wzorcem.                                                            |
| R-06 | Nie zapisano reakcji na pojedynczą błędną próbę.                                                    | Błąd wstrzyma publikację serii; log zostanie zachowany, a naprawiony przebieg otrzyma osobny identyfikator.                     |
| R-07 | Wariant wykonywany zawsze jako drugi mógłby korzystać z innych warunków.                            | Przyjęto kolejność C++–Python w nieparzystych rundach prób i Python–C++ w parzystych.                                           |
| R-08 | Liczba rund może różnić się między przypadkami, więc czasu całej próby nie można porównywać wprost. | Najpierw przelicza się `time_ns / rounds / 1 000 000`, potem wyznacza się statystyki. W parze liczba rund pozostaje identyczna. |
| R-09 | Usunięcie wolnego wyniku po pomiarze mogłoby zmienić odpowiedź na H1.                               | Poprawnych czasów nie usuwa się na podstawie ich wielkości. Przedstawiono rozrzut.                                              |

## 3. Kontrola gotowości planu

| Pytanie kontrolne                       | Ocena po poprawkach                                                                                            |
| :-------------------------------------- | :------------------------------------------------------------------------------------------------------------- |
| Czy wiadomo, jaki wynik nie wesprze H1? | Tak. Wystarczy R < 10 w co najmniej jednym poprawnie zbadanym przypadku.                                       |
| Czy zadanie i algorytm są takie same?   | Tak. Własne sortowanie bąbelkowe z identyczną regułą wcześniejszego zakończenia.                               |
| Czy wskazano wszystkie przypadki?       | Tak. Trzy rozmiary i cztery układy, bez wybierania przypadków po wyniku.                                       |
| Czy liczba prób jest ustalona?          | Tak. Dwie rozgrzewki i 20 prób na wariant oraz przypadek.                                                      |
| Czy granica pomiaru jest wspólna?       | Tak. Sortowanie i pętla wywołań; przygotowanie kopii, wejścia i walidacja poza zegarem.                        |
| Czy przewidziano kontrolowany błąd?     | Tak. Zmiana elementu wyniku ma wywołać kod 1 i zablokować publikację.                                          |
| Czy opisano statystyki i jednostki?     | Tak. Czas jednej operacji w ms, komplet wymaganych statystyk i kierunek R.                                     |
| Czy zapisano ograniczenia?              | Tak. Jedna sesja i stanowisko, pojedyncze wejście na przypadek, brak rozdzielenia wpływu środowiska od języka. |

## 4. Warunki rozpoczęcia właściwej serii

Przed uruchomieniem E01-DEMO trzeba jeszcze wykonać kalibrację, testy obu implementacji i testy parsera. Kalibracja ma potwierdzić przyjęte liczby rund; nie służy do sprawdzania, czy H1 „już wychodzi”. Jeżeli potrzebna będzie zmiana planu, należy zapisać ją przed właściwą serią.

Metryczka środowiska ma zawierać odczytane wersje i pełne polecenie kompilacji. Nie wpisuje się przypuszczalnego trybu zasilania jako faktu. Bez poprawnego wyniku kontrolowanego błędu nie rozpoczyna się pomiarów właściwych.

## 5. Decyzja recenzenta

**Plan zaakceptowany po uwzględnieniu R-01–R-09.** Uwagi przeniesiono do [karty E01 1.0](karta_E01.md), którą zatwierdzono wspólnie 7.11.2026. Akceptacja dotyczy planu; spełnienie warunków technicznych będzie sprawdzone przed serią. Historię dalszych ustaleń prowadzi się w [dzienniku decyzji](dziennik_decyzji.md).
