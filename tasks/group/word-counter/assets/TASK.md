# Projekt 14: Licznik słów

**Języki:** C++ / Python

## Zadanie

Policzcie słowa w tekście ASCII z pliku. W tym zadaniu słowo jest niepustym ciągiem znaków rozdzielanym wyłącznie spacją, tabulatorem lub znakiem nowej linii LF. Interpunkcja nie jest separatorem, więc `kot,pies` liczy się jako jedno słowo.

### Jak działa algorytm

1. Ustawcie licznik słów na `0` i zmienną logiczną `inWord` na fałsz. Ta zmienna odpowiada na pytanie: czy czytacie właśnie wnętrze słowa?
2. Przeglądajcie tekst znak po znaku. Jeżeli znak jest separatorem, ustawcie `inWord` na fałsz. Nie zwiększajcie licznika.
3. Jeśli znak nie jest separatorem, a `inWord` jest fałszem, znaleźliście początek nowego słowa: zwiększcie licznik i ustawcie `inWord` na prawdę.
4. Jeśli znak nie jest separatorem, ale `inWord` jest już prawdą, jesteście wewnątrz tego samego słowa. Niczego nie zmieniajcie.
5. Po ostatnim znaku zwróćcie licznik. Nie trzeba osobno doliczać ostatniego słowa — policzyliście je przy pierwszym znaku. Pusty tekst daje `0`. Nie używajcie `split`.

### Przykład krok po kroku

Dla `Ala  ma`:

1. `A` rozpoczyna słowo: licznik `1`, `inWord = prawda`.
2. `l` i `a` są kontynuacją; licznik nadal `1`.
3. Pierwsza spacja ustawia `inWord = fałsz`. Druga niczego nie dolicza — dwa odstępy nie tworzą pustego słowa.
4. `m` rozpoczyna nowe słowo: licznik `2`. Kolejne `a` go nie zmienia.
5. Koniec tekstu: zwracacie `2`.

## Dane i przypadki testowe

Krótkie i długie słowa, mało i dużo separatorów. Sprawdźcie pusty tekst, same separatory i brak separatora na końcu.

## Benchmark

- Zaimplementujcie opisany algorytm w obu językach, bez zastępowania go gotową funkcją biblioteczną. Porównajcie czas dla co najmniej trzech różnych długości tekstu i wymienionych wariantów, używając tych samych danych.
- Skrypt ma automatycznie uruchamiać wielokrotne próby i zapisywać czasy do CSV. Mierzcie sam algorytm wraz z utworzeniem wyniku, bez wczytywania danych i zapisu plików. Sprawdzajcie wynik poza pomiarem; odrzucajcie błędne próby.
- Porównajcie mediany i rozrzut czasów; podajcie jednostki oraz liczbę powtórzeń.

## Definition of Done — co dostarczacie

- [ ] Kod obu implementacji i automatycznego benchmarku oraz krótką instrukcję uruchomienia.
- [ ] Dane lub generator pozwalający je odtworzyć, testy z oczekiwanymi wynikami i surowe czasy w CSV.
- [ ] Raport MD: metoda pomiaru, sprzęt i wersje narzędzi, wyniki, wykresy i wnioski. Obrazy w podkatalogu, połączone ścieżkami względnymi.
- [ ] Zgodny z MD, profesjonalnie złożony PDF przez Pandoc, bez uciętej treści i artefaktów wydruku z przeglądarki, wraz z poleceniem eksportu. **Jakość PDF jest jednym z kryteriów dobrej oceny.**
