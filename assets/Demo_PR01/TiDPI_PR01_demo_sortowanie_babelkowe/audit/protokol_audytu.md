# Protokół audytu końcowego — E01-DEMO

**Data:** 14.11.2026. **Zakres:** plan, dane, statystyki, raport, wykres i instrukcja odtworzenia. **Podział kontroli:** partner_A — od danych do tabel; partner_B — od wniosków do dowodów. Następnie wykonano przegląd wzajemny.

## Ustalenia

| ID   | Klasa i lokalizacja                    | Dowód problemu i skutek                                                                                               | Decyzja                                                                                       | Stan                     |
| :--- | :------------------------------------- | :-------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------- | :----------------------- |
| A-01 | Poważne; pierwsza wersja streszczenia. | Zdanie „we wszystkich przypadkach co najmniej dziesięciokrotnie” nie zgadzało się z R = 8 dla trzech wejść rosnących. | Podać 9 z 12 i niewsparcie H1 w pełnym zakresie; nie zmieniać progu ani usuwać przypadków.    | Zamknięte po RT-01.      |
| A-02 | Poważne; pierwsza tabela czasów.       | Użyto czasu całej próby, chociaż liczba rund zależała od przypadku.                                                   | Przeliczać każdy rekord na jedno sortowanie przed statystykami i odtworzyć zależne materiały. | Zamknięte po RT-02.      |
| A-03 | Obserwacja; metryczka zasilania.       | Brak wiarygodnego odczytu trybu zasilania.                                                                            | Zachować brak informacji i opisać ograniczenie.                                               | Uwzględnione w raporcie. |

## Kontrola końcowa

Sprawdzono zgodność 12 wejść z manifestem, liczebność 24 grup po 20 i jawny kierunek ilorazu median. Wyniki kontrolne 2,00 ms, 72,10 ms oraz R = 8,0 odtworzono z danych. Porównano raport MD i PDF, podpis wykresu oraz osobny dokument oceny H1.

Wysoki poprawny czas 119 ms pozostawiono. Nie ustalono jego przyczyny i nie przypisano go konkretnemu procesowi bez dowodu. Nie stwierdzono potrzeby zmiany planu ani ponownego pomiaru z powodu poprawek A-01/A-02: dotyczyły analizy i opisu. Surowe rekordy zachowano.

**Decyzja końcowa:** zamknięto ustalenia poważne po retestach; ograniczenie A-03 pozostaje jawne. Zatwierdzenie: partner_A i partner_B. Powiązania: [retesty](retesty.md), [rejestr dowodów](rejestr_dowodow.md), [raport](../report/raport.md).
