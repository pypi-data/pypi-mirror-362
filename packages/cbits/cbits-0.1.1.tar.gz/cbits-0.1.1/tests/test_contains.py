import unittest
from cbits import BitVector


def from_bits(bitstr: str) -> BitVector:
    bv = BitVector(len(bitstr))
    for i, ch in enumerate(bitstr):
        if ch == '1':
            bv.set(i)
    return bv

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.a_str = "00110101"
        self.a = from_bits(self.a_str)

    def test_subvector_found(self):
        patterns = ["0", "1", "0011", "0110", "1101", "01", "101", "0101", ""]
        for pat in patterns:
            with self.subTest(pat=pat):
                b = from_bits(pat)
                self.assertTrue(
                    b in self.a,
                    msg=f"Pattern {pat!r} should be found in {self.a_str!r}"
                )

    def test_subvector_not_found(self):
        patterns = ["111", "1011", "1000", "0010", "1001"]
        for pat in patterns:
            with self.subTest(pat=pat):
                b = from_bits(pat)
                self.assertFalse(
                    b in self.a,
                    msg=f"Pattern {pat!r} should NOT be found in {self.a_str!r}"
                )

    def test_equal_full_match(self):
        b = from_bits(self.a_str)
        self.assertTrue(b in self.a)

    def test_longer_than_A(self):
        longer = self.a_str + "0"
        b = from_bits(longer)
        self.assertFalse(b in self.a)

    def test_multiple_word_boundary(self):
        bits = "".join(str((i // 3) % 2) for i in range(130))
        a = from_bits(bits)
        slice_str = bits[70:95]
        b = from_bits(slice_str)
        self.assertTrue(
            b in a,
            msg="Sub-vector across 64-bit boundary not found"
        )

if __name__ == '__main__':
    unittest.main()
