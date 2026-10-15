#pragma once

#include <cstddef>
#include <cstdint>

// Osobna jednostka translacji: kompilator Release nie widzi ciała przy
// optymalizacji pętli pomiarowej i nie może usunąć make_unique.
void alloc_and_free_once(std::size_t count, std::uint32_t tag);

extern volatile std::uint32_t alloc_sink;
