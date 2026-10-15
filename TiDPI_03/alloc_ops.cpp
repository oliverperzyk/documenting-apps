#include "alloc_ops.hpp"

#include <cstdint>
#include <memory>

volatile std::uint32_t alloc_sink = 0;

#if defined(__clang__)
[[clang::optnone]]
#elif defined(__GNUC__)
__attribute__((optimize("O0")))
#endif
void alloc_and_free_once(std::size_t count, std::uint32_t tag) {
  // Stoper (w alloc_bench) mierzy wywołania tej funkcji.
  // Tutaj: std::make_unique<std::uint32_t[]>(count) oraz destruktor
  // unique_ptr (= delete[]) przy wyjściu z zakresu.
  // optnone: bez tego Clang -O2 eliduje new/delete (allocation elision).
  auto p = std::make_unique<std::uint32_t[]>(count);
  p[0] = tag;
  alloc_sink = p[0];
}
