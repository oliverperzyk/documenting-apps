# Źródło i eksport raportu

Raport źródłowy znajduje się w `report/raport.md`, wykres w `report/images/ilorazy.png`, a styl w `dokumentacja_eksportu/styl.css`. Gotowy PDF dołączono w `report/raport.pdf`. Wszystkie odnośniki mają postać względną.

Przykład etapu Pandoc, wykonywanego z katalogu głównego:

```powershell
pandoc report/raport.md --from=markdown --to=html5 --standalone --embed-resources --resource-path=report --css=dokumentacja_eksportu/styl.css --output=raport.html
```

Następnie przygotowany HTML jest składany do PDF w Chromium z uwzględnieniem stylu wydruku. Automatyczne nagłówki z adresem i datą wydruku powinny być wyłączone. Pliki pośrednie należy utrzymywać w katalogu roboczym. W tej demonstracji skrypt eksportu jest placeholderem, a do korzystania z gotowego PDF nie jest potrzebne żadne z narzędzi eksportu.
