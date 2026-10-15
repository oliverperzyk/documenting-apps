#include <array>
#include <cstdint>
#include <iostream>

// Kopia eksperymentalna: lokalna tablica o stałym rozmiarze.
// Największy uruchomiony wariant w tej serii: 2'000'000 elementów (8 MiB).
// Pierwszy nieudany w serii rosnącej: 2'250'000 (potem także 2'100'000).
// Nie uruchamiać absurdalnych wartości na oryginalnym main.cpp.
constexpr std::size_t element_count = 2'000'000;

using FixedArray = std::array<std::uint32_t, element_count>;

int main() {
  FixedArray local_values{};
  local_values.front() = 1;
  local_values.back() = 2;

  const std::size_t bytes = element_count * sizeof(std::uint32_t);
  std::cout << "element_count=" << element_count << '\n'
            << "bytes=" << bytes << '\n'
            << "front=" << local_values.front() << '\n'
            << "back=" << local_values.back() << '\n'
            << "ok=true\n";
  return 0;
}
