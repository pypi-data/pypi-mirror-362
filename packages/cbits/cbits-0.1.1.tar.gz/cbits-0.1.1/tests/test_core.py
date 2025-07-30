import unittest
import copy
from cbits import BitVector

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.n = 100
        self.bv = BitVector(self.n)

    def test_init_and_len(self):
        self.assertEqual(self.n, len(self.bv))
        self.assertEqual(self.n, self.bv.bits)
        with self.assertRaises(IndexError):
            _ = self.bv[self.n]

    def test_get_set_clear_flip(self):
        for i in (0, 10, 50, 99):
            self.assertFalse(self.bv.get(i))
        self.bv.set(0)
        self.bv.set(50)
        self.assertTrue(self.bv.get(0))
        self.assertTrue(self.bv.get(-self.n))
        self.assertTrue(self.bv.get(50))

        self.bv.clear(50)
        self.assertFalse(self.bv.get(50))

        self.bv.flip(50)
        self.assertTrue(self.bv.get(50))
        self.bv.flip(50)
        self.assertFalse(self.bv.get(50))

        with self.assertRaises(IndexError):
            self.bv.set(self.n)
        with self.assertRaises(IndexError):
            self.bv.flip(self.n + 1)

    def test_sequence_get_setitem(self):
        self.bv[5] = True
        self.assertTrue(self.bv[5])
        self.bv[5] = False
        self.assertFalse(self.bv[5])

        with self.assertRaises(IndexError):
            self.bv[self.n] = True
        with self.assertRaises(IndexError):
            _ = self.bv[self.n]

    def test_bool(self):
        self.assertFalse(bool(self.bv))
        self.bv.set(42)
        self.assertTrue(bool(self.bv))

    def test_repr_and_str(self):
        r = repr(self.bv)
        s = str(self.bv)
        self.assertIn("BitVector", r)
        self.assertIn("bits=", r)
        self.assertIn("BitVector", s)
        self.assertIn("bits", s)

    def test_rank(self):
        self.assertEqual(0, self.bv.rank(10))

        self.bv.set(0)
        self.bv.set(10)
        self.bv.set(20)

        self.assertEqual(1, self.bv.rank(0))
        self.assertEqual(1, self.bv.rank(9))
        self.assertEqual(2, self.bv.rank(10))
        self.assertEqual(3, self.bv.rank(20))
        self.assertEqual(3, self.bv.rank(self.n - 1))

        with self.assertRaises(IndexError):
            self.bv.rank(self.n)

    def test_bitwise_operators(self):
        a = BitVector(64)
        b = BitVector(64)

        for i in range(0, 64, 2):
            a.set(i)

        for i in range(1, 64, 2):
            b.set(i)

        anded = a & b
        ored = a | b
        xored = a ^ b
        not_a = ~a

        self.assertFalse(any(anded))
        self.assertTrue(all(ored[i] for i in range(64)))
        self.assertTrue(all(xored.get(i) for i in range(64)))
        self.assertTrue(not_a.get(1))
        self.assertFalse(not_a.get(0))

    def test_inplace_ops(self):
        a = BitVector(32)
        b = BitVector(32)
        for i in (0, 3, 31):
            a.set(i)
        for i in (1, 3, 30):
            b.set(i)
        a_copy = BitVector(32)
        for i in (0, 3, 31):
            a_copy.set(i)
        a_copy &= b
        self.assertFalse(a_copy.get(0))
        self.assertTrue(a_copy.get(3))
        self.assertFalse(a_copy.get(31))

        a |= b
        for i in (0, 1, 3, 30, 31):
            self.assertTrue(a.get(i))

        a ^= b
        self.assertTrue(a.get(0))
        self.assertFalse(a.get(1))
        self.assertFalse(a.get(3))
        self.assertFalse(a.get(30))
        self.assertTrue(a.get(31))

    def test_copy_and_equality(self):
        a = BitVector(16)
        b = BitVector(16)
        for i in (0, 5, 10):
            a.set(i)
            b.set(i)
        self.assertTrue(a == b)
        b.set(1)
        self.assertFalse(a == b)
        c = b.copy()
        self.assertEqual(b, c)

    def test_contains_subvector(self):
        a = BitVector(10)
        b = BitVector(3)
        a.set(0); a.set(2); a.set(4)
        b.set(0); b.set(2)
        self.assertIn(b, a)
        c = BitVector(3)
        c.set(1); c.set(2)
        self.assertNotIn(c, a)
        self.assertFalse(("foo" in a))

    def test_mismatched_bitwise_length(self):
        a = BitVector(8)
        b = BitVector(7)
        with self.assertRaises(ValueError):
            _ = a & b
        with self.assertRaises(ValueError):
            a &= b
        with self.assertRaises(ValueError):
            _ = a | b
        with self.assertRaises(ValueError):
            a |= b
        with self.assertRaises(ValueError):
            _ = a ^ b
        with self.assertRaises(ValueError):
            a ^= b

    def test_type_mismatch_bitwise(self):
        a = BitVector(8)
        with self.assertRaises(TypeError):
            _ = a & 123
        with self.assertRaises(TypeError):
            _ = a | "foo"

    def test_equality_with_other_types(self):
        a = BitVector(5)
        self.assertFalse(a == 42)
        self.assertTrue(a != 42)

    def test_negative_index_errors(self):
        bv = BitVector(5)
        bv.set(-1)
        self.assertTrue(bv.get(4))
        with self.assertRaises(IndexError):
            bv.get(-6)
        with self.assertRaises(IndexError):
            bv.set(-10)

    def test_copy_and_deepcopy_memo(self):
        a = BitVector(16)
        a.set(3)
        c1 = copy.copy(a)
        self.assertIsNot(c1, a)
        self.assertEqual(a, c1)
        memo = {}
        c2 = copy.deepcopy(a, memo)
        self.assertIn(a, memo)
        self.assertIs(memo[a], c2)
        self.assertEqual(a, c2)

    # def test_iterator(self):
    #     positions = [2, 5, 63, 64, 90]
    #     for p in positions:
    #         self.bv.set(p)
    #     result = list(iter(self.bv))
    #     self.assertEqual(result, positions)

    # def test_to_bytes(self):
    #     self.bv.set(0)
    #     self.bv.set(1)
    #     data = self.bv.to_bytes()
    #     self.assertIsInstance(data, bytes)
    #     self.assertEqual(data[0], 0b00000011)
    #
    #     from math import ceil
    #     self.assertEqual(len(data), ceil(self.n / 8))

    # def test_set_range_and_count(self):
    #     self.bv.set_range(10, 5)
    #     for i in range(10, 15):
    #         self.assertTrue(self.bv.get(i))
    #
    #     self.assertFalse(self.bv.get(9))
    #     self.assertFalse(self.bv.get(15))
    #
    #     cnt = self.bv.count_range(10, 15)
    #     self.assertEqual(cnt, 5)
    #     with self.assertRaises(ValueError):
    #         self.bv.count_range(20, 10)
    #     with self.assertRaises(IndexError):
    #         self.bv.count_range(-1, 5)
    #     with self.assertRaises(IndexError):
    #         self.bv.count_range(0, self.n + 1)


if __name__ == '__main__':
    unittest.main()
