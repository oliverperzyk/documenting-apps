# TiDPI 03 — poziomy A–D

Kryptonim: **Regulus**.

## Oddanie

- `raport.md` — sprawozdanie ze wszystkimi surowymi dowodami D00–D09
- `main.cpp` — program bazowy (`element_count = 50'000`)
- `alloc_bench.cpp`, `alloc_ops.cpp`, `alloc_ops.hpp` — pomiar alokacji (C1)
- `stack_probe/` — kopia do badania granicy lokalnej tablicy (C2)
- `ownership_bench.cpp`, `ownership_ops.cpp`, `ownership_ops.hpp` — raw / unique_ptr / vector (D)

Nie oddawaj szkolnego PDF-u ani katalogów `.build/`.

## Odtworzenie

### Poziom A (Debug)

```sh
mkdir -p .build
clang++ -std=c++17 -O0 -g -D_DEBUG -Wall -Wextra -pedantic -o .build/main_debug main.cpp
./.build/main_debug
```

### Poziom B (Release)

Dla każdego `element_count` ∈ {`5'000`, `20'000`, `50'000`} zmień stałą w `main.cpp`, przebuduj i uruchom (bez debuggera). `rounds` pozostaje `100`.

```sh
clang++ -std=c++17 -O2 -DNDEBUG -Wall -Wextra -pedantic -o .build/main_release main.cpp
./.build/main_release
```

### Poziom C1 — koszt alokacji (Release)

```sh
clang++ -std=c++17 -O2 -DNDEBUG -Wall -Wextra -pedantic -c -o .build/alloc_ops.o alloc_ops.cpp
clang++ -std=c++17 -O2 -DNDEBUG -Wall -Wextra -pedantic -c -o .build/alloc_bench.o alloc_bench.cpp
clang++ -O2 -o .build/alloc_bench .build/alloc_ops.o .build/alloc_bench.o
./.build/alloc_bench
```

### Poziom C2 — granica lokalnej tablicy

Pracuj tylko w `stack_probe/`. Zmieniaj `element_count` stopniowo; nie ustawiaj od razu absurdalnej wartości na oryginalnym `main.cpp`.

```sh
cd stack_probe
mkdir -p .build
clang++ -std=c++17 -O0 -Wall -Wextra -pedantic -o .build/stack_probe main.cpp
./.build/stack_probe
```

### Poziom D — raw / unique_ptr / vector (Release)

```sh
clang++ -std=c++17 -O2 -DNDEBUG -Wall -Wextra -pedantic -c -o .build/ownership_ops.o ownership_ops.cpp
clang++ -std=c++17 -O2 -DNDEBUG -Wall -Wextra -pedantic -c -o .build/ownership_bench.o ownership_bench.cpp
clang++ -O2 -o .build/ownership_bench .build/ownership_ops.o .build/ownership_bench.o
./.build/ownership_bench
```
