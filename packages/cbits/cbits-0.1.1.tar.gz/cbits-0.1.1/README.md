[![Doxygen](https://img.shields.io/badge/docs-doxygen-2c4aa8?logo=doxygen)](https://lambdaphoenix.github.io/cbits/)
[![GitHub License](https://img.shields.io/github/license/lambdaphoenix/cbits)](https://github.com/lambdaphoenix/cbits/blob/main/LICENSE)
[![Changelog](https://img.shields.io/badge/CHANGELOG-md-blue.svg)](https://github.com/lambdaphoenix/cbits/blob/main/CHANGELOG.md)

# cbits

> High-performance BitVector for Python.

---

## Installation

```bash
pip install cbits
```

##
Quick Start
```python
from cbits import BitVector

# Create a 64-bit vector
bv = BitVector(64)

# Set bits, clear, flip, query
bv.set(3)
bv.clear(3)
bv.flip(0)
print(bv.get(0))      # → True or False
print(len(bv), bv.bits)

# Negative indexing
bv.set(-1)
print(bv.get(63))

# Boolean test & rank
print(bool(bv))
print(bv.rank(32))    # count of set bits up to index 32

# Copy & deepcopy
import copy
bv2 = bv.copy()
bv3 = copy.deepcopy(bv)

# Bitwise operations
a = BitVector(8); b = BitVector(8)
a.set(0); a.set(2)
b.set(1); b.set(2)
print((a & b)[0], (a | b)[0], (a ^ b)[0], (~a)[0])

# Sequence & iteration
bv[5] = True
print(bv[5])
print([i for i, bit in enumerate(bv) if bit])

# Contains
a = BitVector(8); b = BitVector(4)
a.set(0); a.set(2); a.set(5)  # 10100100
b.set(0); b.set(3)  # 1001
print(b in a)
```

## API Reference
### Class: BitVector
```python
class BitVector:
    def __init__(self, size: int)
    @property
    def bits(self) -> int

    def get(self, index: int) -> bool
    def set(self, index: int) -> None
    def clear(self, index: int) -> None
    def flip(self, index: int) -> None
    def rank(self, index: int) -> int

    def copy(self) -> BitVector
    def __copy__(self) -> BitVector
    def __deepcopy__(self, memo) -> BitVector

    # Sequence protocol
    def __len__(self) -> int
    def __getitem__(self, index: int) -> bool
    def __setitem__(self, index: int, value: bool)
    def __contains__(self, other: BitVector) -> bool

    # Numeric & bitwise protocol
    def __and__(self, other: BitVector) -> BitVector
    def __iand__(self, other: BitVector) -> BitVector
    def __or__(self, other: BitVector) -> BitVector
    def __ior__(self, other: BitVector) -> BitVector
    def __xor__(self, other: BitVector) -> BitVector
    def __ixor__(self, other: BitVector) -> BitVector
    def __invert__(self) -> BitVector
    def __bool__(self) -> bool

    def __repr__(self) -> str
    def __str__(self) -> str
```

## License
Apache License 2.0 See [LICENSE](https://github.com/lambdaphoenix/cbits/blob/main/LICENSE) for details.

## Project Links
- [📖 Documentation & Source](https://github.com/lambdaphoenix/cbits)
- [🐛 Issues](https://github.com/lambdaphoenix/cbits/issues)
- [📋 Changelog](https://github.com/lambdaphoenix/cbits/blob/main/CHANGELOG.md)
