# CHANGELOG
## [0.1.1]
### Added
- Introduce `compat_dispatch.c` for runtime CPU feature detection and automatic selection of the fastest popcount implementation.
- Additional unit tests

### Changed
- Refactor `compat.h` dispatch logic to clarify fallback paths and cleanup macros.  

## [0.1.0]
### Added
- C backend with SIMD popcount support
- Python sequence and numeric protocol support (`getitem`, `and`, `or`, etc.)
- Unit tests for all methods