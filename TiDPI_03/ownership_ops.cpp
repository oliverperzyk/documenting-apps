#include "ownership_ops.hpp"

#include <cstdint>
#include <memory>
#include <vector>

volatile std::uint32_t ownership_sink = 0;

#if defined(__clang__)
[[clang::optnone]]
#elif defined(__GNUC__)
__attribute__((optimize("O0")))
#endif
void alloc_free_raw(std::size_t count, std::uint32_t tag) {
  std::uint32_t *p = new std::uint32_t[count];
  p[0] = tag;
  ownership_sink = p[0];
  delete[] p;
}

#if defined(__clang__)
[[clang::optnone]]
#elif defined(__GNUC__)
__attribute__((optimize("O0")))
#endif
void alloc_free_unique(std::size_t count, std::uint32_t tag) {
  auto p = std::make_unique<std::uint32_t[]>(count);
  p[0] = tag;
  ownership_sink = p[0];
}

#if defined(__clang__)
[[clang::optnone]]
#elif defined(__GNUC__)
__attribute__((optimize("O0")))
#endif
void alloc_free_vector(std::size_t count, std::uint32_t tag) {
  // vector(n) value-inicjalizuje elementy (dla uint32_t: zera) — koszt w alokacji.
  std::vector<std::uint32_t> v(count);
  v[0] = tag;
  ownership_sink = v[0];
}
