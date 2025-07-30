/**
 * @file src/compat_dispatch.c
 * @brief Runtime dispatch for fastest popcount block implementation.
 *
 * Contains fallback, AVX2, and AVX-512 versions of block-level popcount,
 * plus runtime CPU feature detection to select the best implementation.
 *
 * @see include/compat.h
 * @author lambdaphoenix
 * @version 0.1.1
 * @copyright Copyright (c) 2025 lambdaphoenix
 */
#include "compat.h"

uint64_t
cbits_popcount_block_fallback(const uint64_t *ptr)
{
    uint64_t sum = 0;
    for (size_t i = 0; i < 8; ++i) {
        sum += cbits_popcount64(ptr[i]);
    }
    return sum;
}

uint64_t (*cbits_popcount_block_ptr)(const uint64_t *ptr) =
    cbits_popcount_block_fallback;

#if defined(__x86_64__) || defined(_M_X64)

    #if defined(__GNUC__)
__attribute__((target("avx2")))
    #endif
uint64_t
cbits_popcount_block_avx2(const uint64_t *ptr)
{
    __m256i v0 = _mm256_loadu_si256((const __m256i *) ptr);
    __m256i v1 = _mm256_loadu_si256((const __m256i *) (ptr + 4));
    uint64_t tmp[8];
    _mm256_storeu_si256((__m256i *) tmp, v0);
    _mm256_storeu_si256((__m256i *) (tmp + 4), v1);
    return cbits_popcount64(tmp[0]) + cbits_popcount64(tmp[1]) +
           cbits_popcount64(tmp[2]) + cbits_popcount64(tmp[3]) +
           cbits_popcount64(tmp[4]) + cbits_popcount64(tmp[5]) +
           cbits_popcount64(tmp[6]) + cbits_popcount64(tmp[7]);
}

    #if defined(__GNUC__)
__attribute__((target("avx512vpopcntdq")))
    #endif
uint64_t
cbits_popcount_block_avx512(const uint64_t *ptr)
{
    __m512i v = _mm512_load_si512((const void *) ptr);
    __m512i c = _mm512_popcnt_epi64(v);
    return _mm512_reduce_add_epi64(c);
}

    #if defined(__GNUC__)
__attribute__((target("avx2"))) __attribute__((target("avx512vpopcntdq")))
__attribute__((constructor)) void
init_cpu_dispatch_gcc(void)
{
    if (__builtin_cpu_supports("avx512vpopcntdq")) {
        cbits_popcount_block_ptr = cbits_popcount_block_avx512;
        return;
    }
    if (__builtin_cpu_supports("avx2")) {
        cbits_popcount_block_ptr = cbits_popcount_block_avx2;
    }
}
    #elif defined(_MSC_VER)
        #include <intrin.h>
void __cdecl init_cpu_dispatch(void);
        #pragma section(".CRT$XCU", read)
__declspec(allocate(".CRT$XCU")) void(__cdecl *_ict_ptr)(void) =
    init_cpu_dispatch;

void __cdecl init_cpu_dispatch(void)
{
    int info[4] = {0};
    __cpuidex(info, 7, 0);
    if (info[1] & (1ULL << 57)) {
        cbits_popcount_block_ptr = cbits_popcount_block_avx512;
        return;
    }
    __cpuidex(info, 1, 0);
    if (info[2] & (1U << 5)) {
        cbits_popcount_block_ptr = cbits_popcount_block_avx2;
        return;
    }
}
    #endif
#endif
#if !defined(__x86_64__) && !defined(_M_X64)
void
init_cpu_dispatch(void)
{
}
#endif
