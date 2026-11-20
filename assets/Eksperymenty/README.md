# Eksperymenty demonstracyjne TiDPI

Katalog zawiera jedną solucję Visual Studio oraz osobny projekt dla każdej lekcji wymagającej demonstracji działającego eksperymentu.

```text
TiDPI_Eksperymenty.sln
├── L02_Sortowanie_babelkowe
├── L03_Tablice_statyczne_i_dynamiczne
├── L04_Dane_deterministyczne
├── L05_Automatyzacja
├── L06_Ustrukturyzowany_output
├── L07_Rzetelny_benchmark
├── L08_Planowanie_eksperymentu
├── L09_Analiza_wynikow
└── L10_Odtwarzalne_srodowisko
```

Projekty zawierają kod demonstracyjny powiązany z poszczególnymi lekcjami. Prowadzący może wykorzystać go podczas pokazu albo udostępnić uczniom w całości lub we wskazanym zakresie. Kod demonstracyjny nie zastępuje samodzielnej pracy uczniów ani kodu przygotowywanego przez nich w Projekcie 01. Przed demonstracją należy wybrać właściwy projekt jako startowy oraz konfigurację odpowiednią do celu: Debug do obserwacji programu w debuggerze, Release bez debuggera do pomiarów wydajnościowych.

Projekt `L05_Automatyzacja` zawiera dodatkowo skrypt `run_experiment.py`. Należy uruchamiać go z Developer PowerShell for VS 2022; skrypt kompiluje własną kopię programu do lokalnego katalogu `_build/` i zapisuje dowody w `logs/`.

Projekt `L06_Ustrukturyzowany_output` zawiera skrypt `parse_results.py`, który waliduje wersjonowany output programu C++ i tworzy CSV wyłącznie dla kompletnego, poprawnego strukturalnie wejścia.

Katalog `L09_Analiza_wynikow` jest demonstracją w Pythonie niewymagającą projektu C++. Skrypt `analyze_results.py` waliduje przykładowe CSV, opisuje serie oraz oznacza potencjalne wartości odstające regułą 1,5×IQR bez usuwania rekordów. Plik `profile_demo.py` służy do pokazania profilera `cProfile` dostępnego w standardowej bibliotece Pythona.

Katalog `L10_Odtwarzalne_srodowisko` jest demonstracją w Pythonie niewymagającą projektu C++ ani pakietów zewnętrznych. Skrypt `environment_check.py` waliduje wersjonowaną konfigurację, oblicza skróty plików, zapisuje manifest środowiska i wykrywa różnice względem zarejestrowanego stanu.

## Dodawanie kolejnej lekcji

1. Utworzyć podkatalog `LNN_Krotka_nazwa`.
2. Dodać projekt konsolowy C++ do `TiDPI_Eksperymenty.sln`.
3. Zachować konfiguracje Debug/Release oraz x86/x64, jeśli temat wymaga porównania architektur.
4. Umieścić kompletny eksperyment w projekcie i zachować zgodność z listingiem omawianym w lekcji.
5. Zbudować co najmniej `Debug|x64` i `Release|x64`, a następnie uruchomić program i sprawdzić jego kontrole poprawności.
