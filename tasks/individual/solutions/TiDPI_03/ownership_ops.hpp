#pragma once

#include <cstddef>
#include <cstdint>

// Osobna jednostka translacji + optnone: zapobiega elizji new/delete przy -O2.
void alloc_free_raw(std::size_t count, std::uint32_t tag);
void alloc_free_unique(std::size_t count, std::uint32_t tag);
void alloc_free_vector(std::size_t count, std::uint32_t tag);

extern volatile std::uint32_t ownership_sink;
