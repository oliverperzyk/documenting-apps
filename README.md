# 📝 `@oliverperzyk/documenting-apps`

Repozytorium zawiera indywidualne jak i grupowe rozwiązania zadań oraz materiałów na przedmiot **Testowanie i Dokumentowanie Projektów Informatycznych**. Zawiera również narzędzia do automatycznego formatowania plików (Prettier, clang-format i Ruff) oraz lintowania plików JSON, Markdown i Python.

## 🛠️ Narzędzia deweloperskie

Wymagane są [Bun](https://bun.sh/) oraz [uv](https://docs.astral.sh/uv/getting-started/installation/) (z poleceniem `uvx`) dostępne w `PATH`. Po sklonowaniu repozytorium uruchom `bun install`, aby zainstalować zależności i hooki Lefthook. Przy pierwszym uruchomieniu polecenia dla Pythona `uvx` pobierze przypiętą wersję Ruff `0.17.1` do izolowanego środowiska; wymaga to dostępu do sieci. Nie trzeba instalować Ruff w środowiskach poszczególnych zadań.

- `bun run lint` — sprawdza pliki JSON, Markdown i Python.
- `bun run lint:fix` — stosuje poprawki ESLint i bezpieczne poprawki Ruff, w tym sortowanie importów.
- `bun run format` — formatuje pliki za pomocą Prettier, clang-format i Ruff.
- `bun run format:check` — sprawdza formatowanie bez zapisywania zmian.
- `bun run lint-python` i `bun run lint-python:fix` — sprawdzają lub poprawiają wyłącznie pliki `.py`.
- `bun run format-python` i `bun run format-python:check` — formatują pliki `.py` lub sprawdzają ich formatowanie.

Polecenia dla Pythona domyślnie obejmują całe repozytorium. Można podać konkretne pliki lub katalogi, np. `bun run lint-python "tasks/individual/solutions/TiDPI_06/main.py"`. Konfiguracja `.ruff.toml` ustala zgodność z Pythonem 3.10, limit 120 kolumn, wcięcia po cztery spacje, podwójne cudzysłowy i zakończenia linii LF. Linter wykrywa podstawowe błędy, nieużywany kod i nieuporządkowane importy; nie stosuje niebezpiecznych poprawek.

Ruff pomija zależności, środowiska wirtualne, katalogi IDE oraz wygenerowane pliki i dowody eksperymentów, m.in. `build`, `_build`, `.build`, `.bundle`, `logs`, `wyniki`, `bundles`, `pdfs` i `submissions`. Dodatkowo chroni archiwalne przebiegi, kopie źródeł i dane kontrolne w katalogach `przebiegi`, `kontrole` oraz `archiwum_*`. Wykluczenia obowiązują także przy podaniu konkretnej ścieżki. Katalog `.ruff_cache` jest ignorowany przez Git, Prettier i ESLint.

Przed commitem Lefthook uruchamia lint-staged: dla zmienionych plików `.py` najpierw wykonuje bezpieczne poprawki Ruff, a następnie formatowanie. Przed pushem uruchamia `lint:fix`, a potem `format:check`. Istniejące naruszenia reguł Pythona mogą zablokować push; samo dodanie konfiguracji nie zmienia dotychczasowych rozwiązań.

## 🏅 Rozwiązania indywidualne

Rozwiązania zadań z materiałów indywidualnych (od TiDPI_03 do TiDPI_12) znajduje się w folderze `tasks/individual`, z kolei, ten folder dzieli się na dwa katalogi:

- [`📦 tasks/individual/bundles`](./tasks/individual/bundles/README.md) - Zawiera pliki `.zip` gotowe do pobrania przez prowadzącego przedmiot, które zawierają tylko i wyłącznie pliki wymagane do dołączenia do raportu. Dzięki temu, nie trzeba pobierać wszystkich (w tym zbędnych) plików.
- [`📚 tasks/individual/solutions`](./tasks/individual/solutions/) - Zawiera wszystkie pliki, które były wykorzystywane podczas rozwiązywania zadań.

## 🏡 Rozwiązania grupowe

> [!NOTE]
> Informacja o rozwiązaniach grupowych zostanie dodana wraz z implementacją pierwszych rozwiązań.
