# Plan poziomu C - Regulus

Dokument przygotowany przed uruchomieniami C. Rzeczywisty czas przygotowania,
hash tego planu i harmonogramów zapisuje prepare_C.py w prepared.json.
Nie dotyczy historycznych pomiarów A-B i nie zmienia ich projektu.

## Wymagania i ustalenia

PDF (pełne 10 stron przeczytane podczas planowania): C wymaga dokładnie dwóch
wybranych rozszerzeń, kontroli jednego czynnika i dowodów jak w B; strony 6-10
opisują poziomy, artefakty, raport i kryteria oceny. Użytkownik określił C1/C2,
flagi, rozmiary, rounds=100, pięć bloków, po dwie próby i dwie rozgrzewki
na proces. AGENTS.md jest pusty; nie ma aktualnego nakazu raportów pomocniczych.
Oddzielne źródła C, nazwy katalogów i schemat CSV z kontekstem są decyzjami projektu.

Operacja ma status uzgodnionej z prowadzącym na podstawie polecenia użytkownika:
ręczna suma odległości wartości od 500, bez sum/abs w badanej pętli.
Historia: A ma 20020 elementów i 200 rund, B ma te same dane i 100 rund.
Użytkownik zaakceptował zachowanie generatora i jawne odstępstwo: C1 bierze
pierwsze 10000 elementów A; C2 bierze prefiksy nowego pliku 50000. Prefiksy
10000 nie są identyczne. Nie wolno przedstawiać nowego pliku jako danych A
ani zmieniać po cichu starego generatora. Zachować test porównania prefiksów.

## Pytania i hipotezy

C1: jak konfiguracja C++ wpływa na czas dla tych samych danych i źródła?
Hipoteza: czas może się zmienić, checksum pozostanie identyczny. Bez wskazania
zwycięzcy przed pomiarem.
C2: jak czas zmienia się z liczbą elementów przy stałych 100 rundach?
Hipoteza: dla każdej implementacji czas rośnie w przybliżeniu proporcjonalnie
do liczności. Analiza opisowa stosunków median i czasu na element; bez arbitralnego
progu akceptacji liniowości, bez testu statystycznego i bez założenia zwycięzcy.

## Dane, wzorzec i pomiar

C1: bajtowy prefiks 10000 wierszy dane/input.txt historycznego A.
Oczekiwany checksum 251042700; potwierdzić niezależnym wzorcem przed pomiarami.
C2: values=[i % 1001 for i in range(50000)], random.Random(20261017).shuffle(values).
ASCII, jedna liczba na wiersz, LF; pliki 10000/30000 są prefiksami pliku 50000.
Zakres 0..1000. Manifest przed pomiarami zawiera count, SHA-256 i wzorzec
każdego pliku. Wzorzec: dla x<500 suma 500*count-sum, dla x>500 suma
sum-500*count; po dodaniu pomnożyć przez 100. Nie importować calculate.
Odcisk bajtów nie jest checksumem obliczeń. Obie implementacje w C2 czytają
dokładnie ten sam plik. Kopie wejść i źródeł utrwalić dla każdego przebiegu.

Arytmetyka: int64_t/int; d=x-500 w -500..500, odległość 0..500;
50000*500*100=2500000000 < 9223372036854775807; także sumy pośrednie bezpieczne.
Wynik zaczyna od zera, zewnętrzna pętla 100 rund, wewnętrzna po wszystkich
wartościach, zmiana znaku przy d<0, dodanie do akumulatora.
Start zegara bezpośrednio przed wywołaniem calculate, stop bezpośrednio po nim;
inicjalizacja akumulatora i pętle wewnątrz pomiaru. Odczyt, alokacja, walidacja,
start procesu, kompilacja, sprawdzenie checksumu i wypisywanie poza pomiarem.
C++ steady_clock + duration_cast<nanoseconds>, Python perf_counter_ns.
Zachować nominalny okres C++ i deklarowaną rozdzielczość Python osobno od ns.
Nie twierdzić, że poznano efektywną dokładność zegara lub wykluczono optymalizacje.

## Zmienne i harmonogram

C1 zmienia tylko konfigurację kompilacji identycznego benchmark.cpp:
Debug -std=c++17 -O0 -g; Release -std=c++17 -O2 -DNDEBUG.
Pozostałe warunki stałe: dane 10000, 100 rund, maszyna, źródło, metoda zegara,
liczba prób i rozgrzewek. Bez debuggera, sekwencyjnie.
Pięć bloków; w każdym po procesie każdej konfiguracji, 2 rozgrzewki i 2 próby.
Bloki nieparzyste: Debug, Release; parzyste: Release, Debug.
Numery prób: 1-2,3-4,5-6,7-8,9-10; 10 właściwych i 10 rozgrzewek na konfigurację.

C2 zmienia rozmiar, analizowany oddzielnie w C++ Release i Pythonie.
Stałe: metoda generatora, wspólne prefiksy, 100 rund, maszyna, implementacja,
Release -std=c++17 -O2 -DNDEBUG, zegar, liczba rozgrzewek i prób.
Kolejność rozmiarów w blokach:
1:10000,30000,50000; 2:30000,50000,10000; 3:50000,10000,30000;
4:10000,30000,50000; 5:30000,50000,10000.
W obrębie każdego rozmiaru bloki nieparzyste: C++,Python; parzyste: Python,C++.
Każdy proces: 2 rozgrzewki i 2 próby. 10 prób i 10 rozgrzewek na każdą
z sześciu jednorodnych grup. Rotacja dotyczy bloków, nie pojedynczych prób.
Harmonogramy JSON zapisane przed uruchomieniami, wykonanie musi im odpowiadać.
Jedna seria C1 i jedna seria C2; dwóch historycznych pełnych serii B nie powtarzać
jako nowych dowodów historycznych. Bez poziomu D.

Przed poprawną serią C2 wykonać osobny rzeczywisty przebieg ujemny: kopia
Pythona ze środkiem 0 zamiast 500. Wzorzec bez zmiany; zachować źródło, strumienie,
kody i odrzucenie. Oryginału nie psuć; po nim poprawna C2 potwierdzi przywrócenie.

## Akceptacja i odrzucenie

Dokładny nagłówek language;trial;time_ns;checksum;correct. Oddzielne strumienie
każdego procesu; poprawne języki, typy całkowite, ns>=0, komplet numerów 1..10
w grupie bez duplikatów, dwie rozgrzewki 1/2 i dwie próby na proces, każdy
checksum równy niezależnemu wzorcowi i correct=true; kody 0 i komplet plików.
Sprawdzić źródła, dane, flagi, harmonogram oraz kolejność i brak nakładania procesów.
Błąd dowolnej grupy odrzuca całe badanie; zachować raw i diagnostykę, nie tworzyć
results.csv ani statystyk. Bez odrzucania niewygodnych czasów lub zastępowania prób.
Nowy przebieg zawsze w nowym katalogu. Timeout 60 s/proces i 120 s/kompilacja;
124 oznacza timeout, 127 błąd uruchomienia. Kod walidacji 0 akceptacja, 1 odrzucenie.

Po akceptacji min/max/rozstęp i mediana (średnia pozycji 5 i 6 po sortowaniu)
osobno dla badania, konfiguracji, liczności, implementacji i przebiegu.
Niezależnie przeliczyć wzorzec histogramem, wszystkie statystyki i wiersze 1/10;
wskazać autora kontroli jako asystenta, nie przypisywać jej uczniowi.
Testy walidatora: komplet, checksum przy true, brak/duplikat próby, rozmiar,
konfiguracja, rozgrzewka; fixture nie są pomiarami wydajności.

## Dowody i raport

D17: plan i audyt A-B; D18: dane i prefiksy; D19: C1; D20: kontrola błędna;
D21: poprawna C2; D22: testy walidatora; D23: niezależne rachunki;
D24: końcowy komplet, anonimowość i obejrzany render PDF.
TC-13: zachowanie A-B; TC-14: dane/wzorce/prefiksy; TC-15: C1;
TC-16: rzeczywiste odrzucenie; TC-17: C2 po błędzie; TC-18: fixture walidatora;
TC-19: niezależne rachunki; TC-20: raport/eksport/linki/anonimizacja.
Raport główny rozszerzyć do A-C, zachować dawne identyfikatory i wyniki.
Oddzielić obserwacje od przypuszczeń; opisać jedną maszynę, zakłócenia,
macOS/arm64/Clang zamiast Windows, brak pomiaru temperatury/cache/obciążenia.
Eksport Pandoc/XeLaTeX, render Poppler i przegląd wszystkich stron.
Anonimizacja od chwili pozyskania; nie zbierać prywatnej ścieżki toolchainu.
Bez commit/push/wysyłania zewnętrznego; szkolny PDF wyłączony z paczki.
