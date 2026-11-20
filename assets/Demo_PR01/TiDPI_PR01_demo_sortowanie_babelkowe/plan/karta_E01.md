# Karta eksperymentu E01 — Bąbelkowy pojedynek

> Materiał dydaktyczny: wypełniony dokument fikcyjnego zespołu, należący do wzorca Projektu 01.

| Pole                                      | Wartość                                        |
| :---------------------------------------- | :--------------------------------------------- |
| Projekt i zespół                          | Projekt 01, temat 01, zespół `demo`            |
| Autor planu                               | `partner_A`                                    |
| Recenzent                                 | `partner_B`                                    |
| Wersja                                    | **1.0 — zamrożona przed właściwymi pomiarami** |
| Data zatwierdzenia                        | 7 listopada 2026                               |
| Identyfikator eksperymentu                | **E01**                                        |
| Identyfikator planowanej serii pomiarowej | **E01-DEMO**                                   |
| Hipoteza podlegająca ocenie               | **H1**                                         |

E01 oznacza eksperyment, czyli pytanie wraz z metodą jego sprawdzenia. E01-DEMO jest identyfikatorem konkretnej serii pomiarowej wykonanej według tego planu. H1 oznacza przewidywanie, które zostanie ocenione za pomocą wyników tej serii. Powtórzenie pomiarów w nowej sesji otrzyma osobny identyfikator i nie nadpisze E01-DEMO.

## 1. Pytanie badawcze i cel

Jak dla wskazanych rozmiarów i układów danych różnią się mediany czasu dwóch implementacji tego samego algorytmu bąbelkowego: C++ Release i CPythona?

Celem jest porównanie konkretnych rozwiązań na wspólnych wejściach i jednym stanowisku. Nie bada się, który język jest ogólnie „lepszy”. W obu wariantach zachowuje się kolejność porównań, sposób zamieniania sąsiadów i wcześniejsze zakończenie po przejściu bez zamian.

## 2. Hipoteza H1 i reguła decyzji

**H1: dla każdego z 12 zaplanowanych przypadków mediana czasu CPythona jest co najmniej dziesięciokrotnie większa niż mediana czasu C++ Release.**

Miara porównawcza ma jeden ustalony kierunek:

**R = mediana czasu CPython / mediana czasu C++ Release.**

Obie mediany odnoszą się do czasu jednego sortowania w tej samej grupie danych. R jest ilorazem bez jednostki. Próg 10 traktuje się jako własne, sprawdzalne przewidywanie zespołu; nie jest on standardem oceny wydajności ani wynikiem wcześniejszej serii.

| Sytuacja po zebraniu danych                                                         | Decyzja                                                                                                                |
| :---------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------- |
| Dla wszystkich 12 przypadków R ≥ 10, a dane są poprawne i porównywalne.             | Wyniki opisowo wspierają H1 w zdefiniowanym zakresie.                                                                  |
| Co najmniej jeden przypadek ma R < 10, przy poprawnych i porównywalnych danych.     | Wyniki nie wspierają H1 w całym zaplanowanym zakresie. Wskazuje się przypadki spełniające i niespełniające próg.       |
| Brakuje prób, walidacji, wspólnego wejścia lub informacji niezbędnej do porównania. | Nie rozstrzyga się H1 na podstawie niekompletnego materiału. Należy naprawić problem i udokumentować dalsze działanie. |

R = 10 spełnia warunek, a R = 9,9 go nie spełnia. Decyzję podejmuje się na podstawie niezaokrąglonych wyników. Nie zamienia się po pomiarach warunku „dla każdego przypadku” na „dla większości”. Niższa mediana C++ przy R mniejszym od 10 nie wystarczy do wsparcia tej H1.

Nie planuje się testu istotności statystycznej. Ocena jest opisowym sprawdzeniem przyjętego warunku, z uwzględnieniem kompletności danych i ograniczeń badania.

## 3. Zmienne i definicje operacyjne

| Rola                              | Definicja                                                                       |
| :-------------------------------- | :------------------------------------------------------------------------------ |
| Zmienna niezależna: implementacja | `bubble_cpp_release` oraz `bubble_cpython`.                                     |
| Czynniki opisujące przypadek      | Liczba elementów N i rodzaj uporządkowania wejścia.                             |
| Zmienna zależna                   | Czas jednego sortowania w milisekundach, wyliczony z czasu próby i liczby rund. |
| Główna statystyka                 | Mediana 20 czasów jednego sortowania w grupie.                                  |
| Miara porównawcza                 | R = mediana Python / mediana C++.                                               |
| „Szybciej”                        | Niższa mediana czasu w tej samej grupie.                                        |
| „Poprawnie”                       | Cały wynik równy wzorcowi, z zachowaniem długości i wszystkich powtórzeń.       |
| „Te same dane”                    | Ten sam plik o zgodnym pełnym SHA-256, odczytany przez oba warianty.            |

Kontroluje się algorytm, dane, liczbę rund w parze, granicę pomiaru, stanowisko, konfigurację, liczbę rozgrzewek i prób oraz jednostkę czasu. Procesy w tle, temperatura, zmiany taktowania, kolejność i zachowanie środowisk wykonania mogą zakłócać wynik. Zauważone zdarzenia zapisuje się w logu, zamiast dopisywać ich przyczynę po fakcie.

## 4. Dane wejściowe i zakres przypadków

Bada się trzy rozmiary: **100, 500 i 1000 elementów**, oraz cztery układy: losowy, rosnący, malejący i z powtórzeniami. Razem daje to **12 przypadków**, analizowanych osobno.

|    N |  Seed | Rundy: losowe | Rundy: rosnące | Rundy: malejące | Rundy: powtórzenia |
| ---: | ----: | ------------: | -------------: | --------------: | -----------------: |
|  100 | 42100 |           500 |         10 000 |             500 |                500 |
|  500 | 42500 |            20 |           2000 |              20 |                 20 |
| 1000 | 43000 |            10 |           1000 |              10 |                 10 |

Losowe liczby całkowite pochodzą z zakresu od -10 000 do 10 000. Układy rosnący i malejący przygotowuje się z tego samego zestawu losowego dla danego N. W układzie z powtórzeniami dopuszcza się wyłącznie -1, 0 i 1. Dane generuje się raz; oba programy czytają te same pliki, a nie osobno odtwarzają generator z podanego seeda.

Identyfikator przypadku ma postać `random_100`, `ascending_500`, `descending_1000` lub `duplicates_100`, odpowiednio do układu i rozmiaru. Pliki w `data/input/` zawierają jeden wiersz liczb oddzielonych przecinkami, bez nagłówka, w kodowaniu ASCII, zakończony znakiem LF. Manifest zapisuje rozmiar, seed, zakres wartości, ścieżkę, SHA-256 wejścia oraz SHA-256 wzorca uporządkowania.

Liczby rund ustala się przed właściwą serią. Kalibracja ma potwierdzić, że próby nie są zbyt krótkie i że przygotowane kopie mieszczą się w pamięci. Jeżeli wymusi zmianę parametrów, aktualizuje się plan przed pomiarami, zachowuje się poprzednią wersję i zapisuje się, jakie wyniki były już znane. Danych kalibracyjnych nie włącza się do statystyk E01-DEMO.

## 5. Implementacje i granica pomiaru

W C++ stosuje się `std::vector<int>`, a w Pythonie listę liczb całkowitych. Oba warianty implementują sortowanie bąbelkowe samodzielnie. Równe wartości nie są zamieniane. Po każdym przejściu skraca się sprawdzany fragment, a po przejściu bez zamian kończy się pracę. Dla pustego i jednoelementowego wejścia kończy się od razu.

Przed próbą tworzy się tyle świeżych kopii nieposortowanego wejścia, ile będzie rund. **Kopiowanie pozostaje poza pomiarem.** Włącza się zegar, wykonuje się pętlę sortującą każdą kopię dokładnie raz i zatrzymuje się zegar. Narzut tej pętli pozostaje w pomiarze; nie odejmuje się go osobno. Wynik powstaje w modyfikowanych kopiach.

Poza pomiarem pozostają również start procesu, odczyt i parsowanie, przygotowanie wzorca, walidacja, obliczanie skrótów i zapis rekordów. Używa się `std::chrono::steady_clock` w C++ oraz `time.perf_counter_ns()` w Pythonie. Do wspólnego rekordu zapisuje się całkowity czas próby w nanosekundach.

## 6. Środowisko i konfiguracja

Planowane stanowisko: Intel Core i5-10400, 12 procesorów logicznych, 16 GB RAM, Windows 11 23H2 x64, zasilanie sieciowe. C++: MSVC 19.40, C++17, optymalizacja `/O2`, x64, bez debuggera. Python: CPython 3.12.7 x64, osobny proces, bez dodatkowych bibliotek w benchmarku.

Przed serią zapisuje się rzeczywiste wersje i pełne polecenie kompilacji. Trybu zasilania nie uznaje się za potwierdzony, jeżeli nie uda się go wiarygodnie odczytać; brak tej informacji należy opisać jako ograniczenie. Nie zapisuje się prywatnej nazwy użytkownika ani ścieżek profilu.

## 7. Rozgrzewka, próby i kolejność

Dla każdego przypadku i wariantu wykonuje się dwie rozgrzewki, a potem 20 właściwych prób. Daje to **48 rozgrzewek i 480 prób właściwych**. Wyniki rozgrzewek pozostają w logach, lecz nie w analizie końcowej.

W nieparzystej rundzie prób najpierw uruchamia się C++, a potem Python; w parzystej odwrotnie. `trial` przyjmuje wartości od 1 do 20 dla każdego wariantu i przypadku, a `order` oznacza pierwszą lub drugą pozycję w parze. Nie uruchamia się wariantów równocześnie. Wewnątrz porównywanej pary obowiązuje taka sama liczba rund sortowania.

Nie zwiększa się liczby prób tylko dla przypadku, którego wynik nie pasuje do H1. Nowa niezależna sesja otrzymuje inny identyfikator i osobny zapis danych.

## 8. Walidacja i warunki publikacji

Każdy wynik każdej rundy porównuje się w całości ze wspólnym wzorcem poza pomiarem. Testy wstępne obejmują `[]`, `[7]`, `[5, 3, 2]`, `[-1, 0, -1, 1]`, dane rosnące i malejące. Wprowadza się kontrolowany błąd, zmieniając `[1, 2, 3]` na `[1, 2, 4]`, aby sprawdzić, czy walidator go wykrywa.

Kod 0 oznacza poprawne wykonanie, kod 1 niezgodność wyniku, a kod 2 błąd środowiska lub kontraktu. Po błędzie nie publikuje się częściowej serii jako kompletnej. Zachowuje się jej logi i wyjaśnia się decyzję. Naprawiony przebieg identyfikuje się osobno.

Parser sprawdza identyfikatory, typy pól, zgodność implementacji z językiem, dodatni czas, rozmiar, liczbę rund, poprawność wyniku, brak duplikatów i komplet 20 prób na grupę. Sprawdza też zgodność skrótu wyniku ze wzorcem. Sama flaga `correct=true` nie zastępuje kontroli funkcjonalnej.

## 9. Kontrakt rekordu i analiza

Minimalny rekord ma pola:

```text
protocol_version;run_id;task;language;implementation;case_id;size;
rounds;warmup;trial;order;time_ns;result_checksum;correct
```

Powyższe dwa wiersze przedstawiają jeden nagłówek. Jednostki nie występują w komórkach. Przebieg właściwy ma `run_id=E01-DEMO`, a analizowane rekordy `warmup=false`. Kluczem próby jest połączenie przebiegu, przypadku, implementacji i numeru próby. `result_checksum` opisuje pełny uporządkowany wynik zapisany w ustalonym formacie.

Dla każdego rekordu najpierw wylicza się **t [ms] = time_ns / rounds / 1 000 000**. Następnie dla każdej z 24 grup oblicza się minimum, maksimum, medianę, średnią, odchylenie standardowe próbki z dzieleniem przez n - 1 i liczbę poprawnych prób. Przy 20 wartościach mediana jest średnią dwóch środkowych po uporządkowaniu. Dopiero z median porównywanych wariantów oblicza się 12 ilorazów R.

Nie usuwa się poprawnych prób wyłącznie z powodu wysokiego czasu. Należy przedstawić rozrzut i zapisać zauważone zakłócenia. Prób niepoprawnych nie włącza się do statystyk wydajności, ale zachowuje się ich ślad i wstrzymuje się publikację pełnej serii do wyjaśnienia problemu. Reguł filtrowania nie zmienia się po zobaczeniu wyniku.

W raporcie czasy zostaną przedstawione z dokładnością zapisu pozwalającą odczytać małe wartości, a R z jednym miejscem po przecinku. Zaokrąglanie następuje po obliczeniach i nie wpływa na decyzję o H1.

## 10. Automatyzacja i dowody

Główny skrypt sprawdzi środowisko i dane, skompiluje C++, przeprowadzi serię, zapisze stdout, stderr oraz kody zakończenia, zwaliduje rekordy i wygeneruje podsumowania. Czasy nie będą przepisywane ręcznie z terminala.

| Deklaracja do sprawdzenia          | Zaplanowany dowód                                           |
| :--------------------------------- | :---------------------------------------------------------- |
| Plan powstał przed właściwą serią. | Ta karta w wersji 1.0, recenzja i dziennik decyzji.         |
| Warianty otrzymały te same dane.   | Manifest, pełne skróty plików i logi odczytu.               |
| Wyniki są poprawne.                | Wzorzec, logi walidacji i kontrolowanego błędu.             |
| Zebrano komplet prób.              | Surowe rekordy i kontrola kluczy oraz liczebności grup.     |
| Liczby z raportu można odtworzyć.  | `results/raw/e01.csv`, skrypt analizy i `results/summary/`. |
| Wniosek odpowiada H1.              | Tabela 12 ilorazów i osobny dokument oceny H1 po pomiarach. |

## 11. Ograniczenia przewidziane przed badaniem

Badanie obejmuje jeden komputer, jedną sesję, trzy rozmiary i jeden zestaw liczb dla każdej kombinacji układu oraz N. Nie rozdziela wpływu języka od reprezentacji danych, kompilatora, interpretera i narzutu pętli. Naprzemienność nie wyklucza zmiany warunków w czasie. Powtarzane rundy mogą inaczej wykorzystywać pamięć niż pojedyncze uruchomienie.

Te ograniczenia wyznaczają zakres wniosku. Różne wejścia lub błędne wyniki nie są zwykłym ograniczeniem: podważają porównanie i wymagają naprawy.

## 12. Zatwierdzenie i wersjonowanie

Kartę przygotowano w ramach zadań `partner_A`, a jej założenia zrecenzowano w ramach zadań `partner_B`. Po uwzględnieniu uwag wersję 1.0 zatwierdzono wspólnie dnia 7.11.2026. Przed właściwą serią wymagane jest zakończenie kalibracji oraz testów poprawności i parsera. Samo zatwierdzenie planu nie jest potwierdzeniem wykonania testów.

Zmiany zapisuje się w [dzienniku decyzji](dziennik_decyzji.md). [Recenzja planu](recenzja_planu.md) dokumentuje kontrolę przed pomiarami. [Ocena H1](ocena_H1.md) powstaje dopiero po analizie E01-DEMO i nie jest częścią zamrożonej karty.
