/**
 * @file python/binding.c
 * @brief Python C-API bindings for cbits.BitVector.
 *
 * Defines the Python-level BitVector type wrapping the C BitVector API,
 * including:
 * - PyBitVector type and lifecycle (tp_new, tp_init, tp_dealloc)
 * - Core BitVector methods (get, set, clear, flip, rank, copy)
 * - Sequence, numeric and richcompare protocols
 *
 * @see include/bitvector.h
 * @author lambdaphoenix
 * @version 0.1.1
 * @copyright Copyright (c) 2025 lambdaphoenix
 */
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "bitvector.h"

/**
 * @def CHECK_BV_OBJ(o)
 * @brief Verify that @a o is a PyBitVector instance or raise @c TypeError.
 */
#define CHECK_BV_OBJ(o)                                         \
    if (!PyObject_TypeCheck(o, PyBitVectorPtr)) {               \
        PyErr_SetString(PyExc_TypeError, "Expected BitVector"); \
        return NULL;                                            \
    }

/**
 * @def CHECK_BV_BOTH(a, b)
 * @brief Verify both @a a and @a b are PyBitVector, else return @c
 * NotImplemented.
 */
#define CHECK_BV_BOTH(a, b)                       \
    if (!PyObject_TypeCheck(a, PyBitVectorPtr) || \
        !PyObject_TypeCheck(b, PyBitVectorPtr)) { \
        Py_RETURN_NOTIMPLEMENTED;                 \
    }

/**
 * @struct PyBitVector
 * @brief Python object containing a pointer to a native BitVector.
 */
typedef struct {
    PyObject_HEAD BitVector *bv;
} PyBitVector;

/** Global pointer to the PyBitVector type object. */
PyTypeObject *PyBitVectorPtr = NULL;

/**
 * @brief Wrap a native BitVector in a new PyBitVector Python object.
 * @param bv_data Pointer to an allocated BitVector.
 * @return New reference to a PyBitVector, or NULL on allocation failure.
 */
static PyObject *
bv_wrap_new(BitVector *bv_data)
{
    PyBitVector *obj =
        (PyBitVector *) PyBitVectorPtr->tp_alloc(PyBitVectorPtr, 0);
    if (!obj) {
        bv_free(bv_data);
        return NULL;
    }
    obj->bv = bv_data;
    return (PyObject *) obj;
}
/* -------------------------------------------------------------------------
 * Deallocation and object lifecycle
 * ------------------------------------------------------------------------- */

/**
 * @brief Deallocate a PyBitVector object.
 * @param self Python object to deallocate.
 */
static void
py_bv_free(PyObject *self)
{
    PyBitVector *bvself = (PyBitVector *) self;
    if (bvself->bv) {
        bv_free(bvself->bv);
        bvself->bv = NULL;
    }
    Py_TYPE(self)->tp_free(self);
}

/**
 * @brief __new__ for BitVector: allocate the Python object.
 * @param type The Python type object.
 * @param args Positional args (unused).
 * @param kwds Keyword args (unused).
 * @return New, uninitialized PyBitVector or NULL on failure.
 */
static PyObject *
py_bv_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PyBitVector *bvself = (PyBitVector *) type->tp_alloc(type, 0);
    if (!bvself) {
        return NULL;
    }
    bvself->bv = NULL;
    return (PyObject *) bvself;
}

/**
 * @brief Python binding for BitVector.copy() → BitVector.
 * @param self Python PyBitVector instance.
 * @param UNUSED
 * @return New BitVector copy
 */
static PyObject *
py_bv_copy(PyObject *self, PyObject *ignored)
{
    BitVector *copy = bv_copy(((PyBitVector *) self)->bv);
    if (!copy) {
        PyErr_SetString(PyExc_MemoryError,
                        "Failed to allocate BitVector in copy()");
        return NULL;
    }
    return bv_wrap_new(copy);
}

/**
 * @brief Python binding for BitVector.__deepcopy__(memo) → BitVector.
 * @param self Python PyBitVector instance.
 * @param memo
 * @return New BitVector copy
 */
static PyObject *
py_bv_deepcopy(PyObject *self, PyObject *memo)
{
    PyObject *copy = py_bv_copy(self, NULL);
    if (!copy) {
        return NULL;
    }
    if (memo && PyDict_Check(memo)) {
        if (PyDict_SetItem(memo, self, copy) < 0) {
            Py_DECREF(copy);
            return NULL;
        }
    }
    return copy;
}

/**
 * @brief __init__ for BitVector(size): allocate the underlying C BitVector.
 * @param self Python PyBitVector instance.
 * @param args Positional args tuple.
 * @param kwds Keyword args dict.
 * @return 0 on success, -1 on error (with exception set).
 */
static int
py_bv_init(PyObject *self, PyObject *args, PyObject *kwds)
{
    Py_ssize_t n_bits;
    static char *kwlist[] = {"size", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "n", kwlist, &n_bits)) {
        return -1;
    }
    PyBitVector *bvself = (PyBitVector *) self;
    bvself->bv = bv_new((size_t) n_bits);
    if (!bvself->bv) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate BitVector");
        return -1;
    }
    return 0;
}

/* -------------------------------------------------------------------------
 * Core BitVector Methods
 * ------------------------------------------------------------------------- */

/**
 * @brief Parse and validate a single index argument.
 * @param self Python PyBitVector instance.
 * @param args Array of Python arguments.
 * @param n_args Number of arguments expected (should be 1).
 * @param p_index Output pointer to store the validated index.
 * @return 0 on success (p_index set), -1 on failure (exception set).
 */
static inline int
bv_parse_index(PyObject *self, PyObject *const *args, Py_ssize_t n_args,
               size_t *p_index)
{
    if (n_args != 1) {
        PyErr_SetString(PyExc_TypeError, "Method takes exactly one argument");
        return -1;
    }
    Py_ssize_t index = PyLong_AsSsize_t(args[0]);
    if (index == -1 && PyErr_Occurred()) {
        return -1;
    }
    PyBitVector *bvself = (PyBitVector *) self;
    size_t n_bits = bvself->bv->n_bits;
    if (index < 0) {
        index += (Py_ssize_t) n_bits;
    }
    if (index < 0 || index >= n_bits) {
        PyErr_SetString(PyExc_IndexError, "BitVector index out of range");
        return -1;
    }
    *p_index = (size_t) index;
    return 0;
}

/**
 * @brief Python binding for BitVector.get(index) → bool.
 * @param self Python PyBitVector instance.
 * @param args Array of Python arguments.
 * @param n_args Number of arguments expected (should be 1).
 * @return true is bit is set, false otherwise
 */
static PyObject *
py_bv_get(PyObject *self, PyObject *const *args, Py_ssize_t nargs)
{
    size_t index;
    if (bv_parse_index(self, args, nargs, &index) < 0) {
        return NULL;
    }

    int bit = bv_get(((PyBitVector *) self)->bv, index);
    return PyBool_FromLong(bit);
}

/**
 * @brief Python binding for BitVector.set(index).
 * @param self Python PyBitVector instance.
 * @param args Array of Python arguments.
 * @param n_args Number of arguments expected (should be 1).
 * @return None on success, NULL on error.
 */
static PyObject *
py_bv_set(PyObject *self, PyObject *const *args, Py_ssize_t nargs)
{
    size_t index;
    if (bv_parse_index(self, args, nargs, &index) < 0) {
        return NULL;
    }

    bv_set(((PyBitVector *) self)->bv, index);
    Py_RETURN_NONE;
}

/**
 * @brief Python binding for BitVector.clear(index).
 * @param self Python PyBitVector instance.
 * @param args Array of Python arguments.
 * @param n_args Number of arguments expected (should be 1).
 * @return None on success, NULL on error.
 */
static PyObject *
py_bv_clear(PyObject *self, PyObject *const *args, Py_ssize_t nargs)
{
    size_t index;
    if (bv_parse_index(self, args, nargs, &index) < 0) {
        return NULL;
    }

    bv_clear(((PyBitVector *) self)->bv, index);
    Py_RETURN_NONE;
}

/**
 * @brief Python binding for BitVector.flip(index).
 * @param self Python PyBitVector instance.
 * @param args Array of Python arguments.
 * @param n_args Number of arguments expected (should be 1).
 * @return None on success, NULL on error.
 */
static PyObject *
py_bv_flip(PyObject *self, PyObject *const *args, Py_ssize_t nargs)
{
    size_t index;
    if (bv_parse_index(self, args, nargs, &index) < 0) {
        return NULL;
    }

    bv_flip(((PyBitVector *) self)->bv, index);
    Py_RETURN_NONE;
}

/**
 * @brief Python binding for BitVector.rank(index) → bool.
 * @param self Python PyBitVector instance.
 * @param args Array of Python arguments.
 * @param n_args Number of arguments expected (should be 1).
 * @return Number of bits set in range [0...pos]
 */
static PyObject *
py_bv_rank(PyObject *self, PyObject *const *args, Py_ssize_t nargs)
{
    size_t index;
    if (bv_parse_index(self, args, nargs, &index) < 0) {
        return NULL;
    }

    size_t rank = bv_rank(((PyBitVector *) self)->bv, index);
    return PyLong_FromSize_t(rank);
}

/**
 * @brief Method table for BitVector core methods.
 */
static PyMethodDef BitVector_methods[] = {
    {"get", (PyCFunction) py_bv_get, METH_FASTCALL, PyDoc_STR("Get bit")},
    {"set", (PyCFunction) py_bv_set, METH_FASTCALL, PyDoc_STR("Set bit")},
    {"clear", (PyCFunction) py_bv_clear, METH_FASTCALL,
     PyDoc_STR("Clear bit")},
    {"flip", (PyCFunction) py_bv_flip, METH_FASTCALL, PyDoc_STR("Flip bit")},
    {"rank", (PyCFunction) py_bv_rank, METH_FASTCALL, PyDoc_STR("Rank query")},
    {"copy", (PyCFunction) py_bv_copy, METH_NOARGS,
     PyDoc_STR("Return a copy of that BitVector")},
    {"__copy__", (PyCFunction) py_bv_copy, METH_NOARGS,
     PyDoc_STR("Return a copy of that BitVector")},
    {"__deepcopy__", (PyCFunction) py_bv_deepcopy, METH_O,
     PyDoc_STR("Return a copy of that BitVector")},
    {NULL, NULL, 0, NULL},
};

/* -------------------------------------------------------------------------
 * Magic Methods
 * ------------------------------------------------------------------------- */

/**
 * @brief __repr__ for BitVector.
 * @param self Python PyBitVector instance.
 * @return New Python string describing the object.
 */
static PyObject *
py_bv_repr(PyObject *self)
{
    PyBitVector *bvself = (PyBitVector *) self;
    return PyUnicode_FromFormat("<cbits.BitVector object at %p bits=%zu>",
                                self, bvself->bv->n_bits);
}

/**
 * @brief __str__ for BitVector.
 * @param self Python PyBitVector instance.
 * @return New Python string "BitVector with X bits".
 */
static PyObject *
py_bv_str(PyObject *self)
{
    PyBitVector *bvself = (PyBitVector *) self;
    return PyUnicode_FromFormat("BitVector with %zu bits", bvself->bv->n_bits);
}

/**
 * @brief Rich comparison (== and !=) for BitVector.
 * @param a First operant.
 * @param b Second operant.
 * @param op Comparison operation (Py_EQ or Py_NE).
 * @return Py_True or Py_False on success; Py_RETURN_NOTIMPLEMENTED if
 * unsupported.
 */
static PyObject *
py_bv_richcompare(PyObject *a, PyObject *b, int op)
{
    if (op != Py_EQ && op != Py_NE) {
        Py_RETURN_NOTIMPLEMENTED;
    }
    CHECK_BV_BOTH(a, b)
    BitVector *A = ((PyBitVector *) a)->bv;
    BitVector *B = ((PyBitVector *) b)->bv;

    bool eq = bv_equal(((PyBitVector *) a)->bv, ((PyBitVector *) b)->bv);
    if ((op == Py_EQ) == eq) {
        Py_RETURN_TRUE;
    }
    Py_RETURN_FALSE;
}

/**
 * @brief __hash__ for a BitVector object.
 *
 * Uses Python’s internal pointer-hashing helper to produce a hash
 * based solely on the object’s address.
 *
 * @param self Pointer to the PyBitVector instance to be hashed.
 * @return A Py_hash_t value computed from the object pointer.
 */
static Py_hash_t
py_bv_hash(PyObject *self)
{
    return _Py_HashPointer(self);
}

/* -------------------------------------------------------------------------
 * Sequence Protocol
 * ------------------------------------------------------------------------- */

/**
 * @brief __len__(BitVector) → number of bits.
 * @param self Python PyBitVector instance.
 * @return Number of bits as Py_ssize_t.
 */
static Py_ssize_t
py_bv_len(PyObject *self)
{
    BitVector *bv = ((PyBitVector *) self)->bv;
    return (Py_ssize_t) (bv ? bv->n_bits : 0);
}

/**
 * @brief __getitem__(BitVector, index).
 * @param self Python PyBitVector instance.
 * @param i Index to access
 * @return Py_True or Py_False; NULL on IndexError.
 */
static PyObject *
py_bv_item(PyObject *self, Py_ssize_t i)
{
    BitVector *bv = ((PyBitVector *) self)->bv;
    if (!bv || bv->n_bits <= (size_t) i) {
        PyErr_SetString(PyExc_IndexError, "BitVector index out of range");
        return NULL;
    }
    return PyBool_FromLong(bv_get(bv, (size_t) i));
}

/**
 * @brief __setitem__(BitVector, index, value).
 * @param self Python PyBitVector instance.
 * @param i Index to access
 * @param value Boolean-like Python object
 * @return 0 on success; -1 on error (with exception set).
 */
static int
py_bv_ass_item(PyObject *self, Py_ssize_t i, PyObject *value)
{
    BitVector *bv = ((PyBitVector *) self)->bv;
    if (!bv || bv->n_bits <= (size_t) i) {
        PyErr_SetString(PyExc_IndexError,
                        "BitVector assignment index out of range");
        return -1;
    }
    int bit = PyObject_IsTrue(value);
    if (bit < 0) {
        return -1;
    }
    if (bit) {
        bv_set(bv, (size_t) i);
    }
    else {
        bv_clear(bv, (size_t) i);
    }
    return 0;
}

/**
 * @brief __contains__(BitVector, other) → boolean.
 * @param self Python PyBitVector instance (haystack).
 * @param value Python PyBitVector instance (needle).
 * @return 1 if contained, 0 otherwise
 */
static int
py_bv_contains(PyObject *self, PyObject *value)
{
    if (!PyObject_TypeCheck((PyObject *) value, PyBitVectorPtr)) {
        return false;
    }

    PyBitVector *A = (PyBitVector *) self;
    PyBitVector *B = (PyBitVector *) value;
    return bv_contains_subvector(A->bv, B->bv);
}

/* -------------------------------------------------------------------------
 * Number Protocol
 * ------------------------------------------------------------------------- */

/**
 * @brief __and__(BitVector, BitVector) → BitVector.
 * @param a Left operand.
 * @param b Right operand.
 * @return New BitVector representing bitwise AND; NULL on error.
 */
static PyObject *
py_bv_and(PyObject *a, PyObject *b)
{
    CHECK_BV_BOTH(a, b)

    PyBitVector *A = (PyBitVector *) a;
    PyBitVector *B = (PyBitVector *) b;

    size_t size = A->bv->n_bits;
    if (size != B->bv->n_bits) {
        PyErr_SetString(PyExc_ValueError, "length mismatch");
        return NULL;
    }
    BitVector *C = bv_new(size);
    if (!C) {
        PyErr_SetString(PyExc_MemoryError,
                        "BitVector allocation failed in __and__");
        return NULL;
    }

    for (size_t i = 0; i < A->bv->n_words; ++i) {
        C->data[i] = A->bv->data[i] & B->bv->data[i];
    }
    return bv_wrap_new(C);
}

/**
 * @brief __iand__(BitVector, BitVector) in-place AND.
 * @param a Left operand (modified in place).
 * @param b Right operand.
 * @return Self on success, NULL on error.
 */
static PyObject *
py_bv_iand(PyObject *self, PyObject *arg)
{
    CHECK_BV_OBJ(arg)

    PyBitVector *A = (PyBitVector *) self;
    PyBitVector *B = (PyBitVector *) arg;

    size_t size = A->bv->n_bits;
    if (size != B->bv->n_bits) {
        PyErr_SetString(PyExc_ValueError, "length mismatch");
        return NULL;
    }

    for (size_t i = 0; i < A->bv->n_words; ++i) {
        cbits_atomic_fetch_and(&A->bv->data[i], B->bv->data[i]);
    }
    A->bv->rank_dirty = true;
    Py_INCREF(self);
    return self;
}

/**
 * @brief __or__(BitVector, BitVector) → BitVector.
 * @param a Left operand.
 * @param b Right operand.
 * @return New BitVector representing bitwise OR; NULL on error.
 */
static PyObject *
py_bv_or(PyObject *a, PyObject *b)
{
    CHECK_BV_BOTH(a, b)

    PyBitVector *A = (PyBitVector *) a;
    PyBitVector *B = (PyBitVector *) b;

    size_t size = A->bv->n_bits;
    if (size != B->bv->n_bits) {
        PyErr_SetString(PyExc_ValueError, "length mismatch");
        return NULL;
    }
    BitVector *C = bv_new(size);
    if (!C) {
        PyErr_SetString(PyExc_MemoryError,
                        "BitVector allocation failed in __or__");
        return NULL;
    }

    for (size_t i = 0; i < A->bv->n_words; ++i) {
        C->data[i] = A->bv->data[i] | B->bv->data[i];
    }
    return bv_wrap_new(C);
}

/**
 * @brief __ior__(BitVector, BitVector) in-place OR.
 * @param a Left operand (modified in place).
 * @param b Right operand.
 * @return Self on success, NULL on error.
 */
static PyObject *
py_bv_ior(PyObject *self, PyObject *arg)
{
    CHECK_BV_OBJ(arg)

    PyBitVector *A = (PyBitVector *) self;
    PyBitVector *B = (PyBitVector *) arg;

    size_t size = A->bv->n_bits;
    if (size != B->bv->n_bits) {
        PyErr_SetString(PyExc_ValueError, "length mismatch");
        return NULL;
    }

    for (size_t i = 0; i < A->bv->n_words; ++i) {
        cbits_atomic_fetch_or(&A->bv->data[i], B->bv->data[i]);
    }
    A->bv->rank_dirty = true;
    Py_INCREF(self);
    return self;
}

/**
 * @brief __xor__(BitVector, BitVector) → BitVector.
 * @param a Left operand.
 * @param b Right operand.
 * @return New BitVector representing bitwise XOR; NULL on error.
 */
static PyObject *
py_bv_xor(PyObject *a, PyObject *b)
{
    CHECK_BV_BOTH(a, b)

    PyBitVector *A = (PyBitVector *) a;
    PyBitVector *B = (PyBitVector *) b;

    size_t size = A->bv->n_bits;
    if (size != B->bv->n_bits) {
        PyErr_SetString(PyExc_ValueError, "length mismatch");
        return NULL;
    }
    BitVector *C = bv_new(size);
    if (!C) {
        PyErr_SetString(PyExc_MemoryError,
                        "BitVector allocation failed in __xor__");
        return NULL;
    }

    for (size_t i = 0; i < A->bv->n_words; ++i) {
        C->data[i] = A->bv->data[i] ^ B->bv->data[i];
    }
    return bv_wrap_new(C);
}

/**
 * @brief __ixor__(BitVector, BitVector) in-place XOR.
 * @param a Left operand (modified in place).
 * @param b Right operand.
 * @return Self on success, NULL on error.
 */
static PyObject *
py_bv_ixor(PyObject *self, PyObject *arg)
{
    CHECK_BV_OBJ(arg)

    PyBitVector *A = (PyBitVector *) self;
    PyBitVector *B = (PyBitVector *) arg;

    size_t size = A->bv->n_bits;
    if (size != B->bv->n_bits) {
        PyErr_SetString(PyExc_ValueError, "length mismatch");
        return NULL;
    }

    for (size_t i = 0; i < A->bv->n_words; ++i) {
        cbits_atomic_fetch_xor(&A->bv->data[i], B->bv->data[i]);
    }
    A->bv->rank_dirty = true;
    Py_INCREF(self);
    return self;
}

/**
 * @brief __invert__(BitVector) → BitVector.
 * @param self Python PyBitVector instance.
 * @return New BitVector instance with all bits toggled, NULL on error;
 */
static PyObject *
py_bv_invert(PyObject *self)
{
    PyBitVector *A = (PyBitVector *) self;
    BitVector *C = bv_new(A->bv->n_bits);
    if (!C) {
        PyErr_SetString(PyExc_MemoryError,
                        "BitVector allocation failed in __not__");
        return NULL;
    }
    for (size_t i = 0; i < A->bv->n_words; ++i) {
        C->data[i] = ~A->bv->data[i];
    }
    return bv_wrap_new(C);
}

/**
 * @brief __bool__(BitVector) → boolean.
 * @param self Python PyBitVector instance.
 * @return 1 if any bit is set, 0 otherwise
 */
static int
py_bv_bool(PyObject *self)
{
    PyBitVector *bvself = (PyBitVector *) self;
    return bv_rank(bvself->bv, bvself->bv->n_bits - 1) > 0;
}

/* -------------------------------------------------------------------------
 * Properties
 * ------------------------------------------------------------------------- */

/**
 * @brief Getter for the read-only "bits" property.
 * @param self Python PyBitVector instance.
 * @param closure Unused.
 * @return Python integer of the bit-length
 */
static PyObject *
py_bv_get_size(PyObject *self, void *closure)
{
    PyBitVector *bvself = (PyBitVector *) self;
    return PyLong_FromSize_t(bvself->bv->n_bits);
}

/**
 * @brief Setter for the read-only "bits" property, always raises.
 * @param self Python PyBitVector instance.
 * @param closure Unused.
 * @return -1 and sets AttributeError
 */
static int
py_bv_set_size(PyObject *self, void *closure)
{
    PyErr_SetString(PyExc_AttributeError, "size is read-only");
    return -1;
}

/**
 * @brief Property definitions for the BitVector type.
 *
 * This table lists all read-only and writable properties exposed
 * on the Python BitVector object.
 *
 * @see PyGetSetDef
 */
static PyGetSetDef PyBitVector_getset[] = {
    {"bits", (getter) py_bv_get_size, (setter) py_bv_set_size,
     PyDoc_STR("The number of bits"), NULL},
    {NULL},
};

/* -------------------------------------------------------------------------
 * Type Object Definition
 * ------------------------------------------------------------------------- */

/**
 * @brief Slot table for the PyBitVector type.
 *
 * Maps Python’s type callbacks (new, init, dealloc, repr, etc.)
 * and protocol slots (sequence, number, richcompare) to our C functions.
 *
 * @see PyType_Slot
 */
static PyType_Slot PyBitVector_slots[] = {
    {Py_tp_new, py_bv_new},
    {Py_tp_init, py_bv_init},
    {Py_tp_dealloc, py_bv_free},
    {Py_tp_methods, BitVector_methods},
    {Py_tp_repr, py_bv_repr},
    {Py_tp_str, py_bv_str},
    {Py_tp_doc, PyDoc_STR("BitVector")},
    {Py_tp_getset, PyBitVector_getset},
    {Py_tp_richcompare, py_bv_richcompare},
    {Py_tp_hash, py_bv_hash},

    {Py_sq_length, py_bv_len},
    {Py_sq_item, py_bv_item},
    {Py_sq_ass_item, py_bv_ass_item},
    {Py_sq_contains, py_bv_contains},

    {Py_nb_and, py_bv_and},
    {Py_nb_inplace_and, py_bv_iand},
    {Py_nb_or, py_bv_or},
    {Py_nb_inplace_or, py_bv_ior},
    {Py_nb_xor, py_bv_xor},
    {Py_nb_inplace_xor, py_bv_ixor},
    {Py_nb_invert, py_bv_invert},
    {Py_nb_bool, py_bv_bool},

    {0, 0},
};

/**
 * @brief Type specification for cbits.BitVector.
 *
 * This structure describes the Python type name, size,
 * inheritance flags, and slot table used to create the type.
 *
 * @see PyType_Spec
 */
PyType_Spec PyBitVector_spec = {
    .name = "cbits.BitVector",
    .basicsize = sizeof(PyBitVector),
    .itemsize = 0,
    .flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .slots = PyBitVector_slots,
};

/* -------------------------------------------------------------------------
 * Module Init
 * ------------------------------------------------------------------------- */

#if PY_VERSION_HEX >= 0x030C0000
    /**
     * @def ADD_OBJECT(module, name, object)
     * @brief Add a PyObject to a module, handling reference counts portably.
     *
     * On Python ≥ 3.12, PyModule_AddObjectRef() is available and automatically
     * steals a reference. On older versions, we fall back to
     * PyModule_AddObject() and manually increment the reference on success.
     *
     * @param module The Python module to which the object is added.
     * @param name The attribute name under which the object is registered.
     * @param object The PyObject pointer to add.
     * @return 0 on success, -1 on failure (exception set by
     * PyModule_AddObject*).
     */
    #define ADD_OBJECT(module, name, object) \
        (PyModule_AddObjectRef(module, name, object))
#else

    /**
     * @def ADD_OBJECT(module, name, object)
     * @brief Add a PyObject to a module, handling reference counts portably.
     *
     * On Python ≥ 3.12, PyModule_AddObjectRef() is available and automatically
     * steals a reference. On older versions, we fall back to
     * PyModule_AddObject() and manually increment the reference on success.
     *
     * @param module The Python module to which the object is added.
     * @param name The attribute name under which the object is registered.
     * @param object The PyObject pointer to add.
     * @return 0 on success, -1 on failure (exception set by
     * PyModule_AddObject*).
     */
    #define ADD_OBJECT(module, name, object)           \
        (PyModule_AddObject(module, name, object) == 0 \
             ? (Py_XINCREF(object), 0)                 \
             : -1)
#endif
#ifdef PYPY_VERSION
    #undef ADD_OBJECT
static inline int
cbits_add_object(PyObject *module, const char *name, PyObject *obj)
{
    int err = PyModule_AddObject(module, name, obj);
    if (err < 0) {
        return err;
    }
    Py_XINCREF(obj);
    return 0;
}

    /**
     * @def ADD_OBJECT(module, name, object)
     * @brief Add a PyObject to a module, handling reference counts portably.
     *
     * On Python ≥ 3.12, PyModule_AddObjectRef() is available and automatically
     * steals a reference. On older versions, we fall back to
     * PyModule_AddObject() and manually increment the reference on success.
     *
     * @param module The Python module to which the object is added.
     * @param name The attribute name under which the object is registered.
     * @param object The PyObject pointer to add.
     * @return 0 on success, -1 on failure (exception set by
     * PyModule_AddObject*).
     */
    #define ADD_OBJECT(module, name, object) \
        cbits_add_object(module, name, object)
#endif

/**
 * @brief Module exec callback: register BitVector type and metadata.
 * @param module New module instance.
 * @return 0 on success; -1 on failure (exception set).
 */
static int
cbits_module_exec(PyObject *module)
{
/* Register BitVector */
#if defined(_MSC_VER)
    init_cpu_dispatch();
#endif
#if PY_VERSION_HEX >= 0x030B0000
    PyBitVectorPtr = (PyTypeObject *) PyType_FromModuleAndSpec(
        module, &PyBitVector_spec, NULL);
#else
    PyBitVectorPtr = (PyTypeObject *) PyType_FromSpec(&PyBitVector_spec);
    if (!PyBitVectorPtr || PyType_Ready(PyBitVectorPtr) < 0) {
        PyErr_SetString(PyExc_RuntimeError,
                        "Failed to initialize BitVector type");
        return -1;
    }
#endif
    if (!PyBitVectorPtr) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to create BitVector type");
        return -1;
    }

    if (ADD_OBJECT(module, "BitVector", (PyObject *) PyBitVectorPtr) < 0) {
        return -1;
    }

    /* Metadata */
    if (PyModule_AddStringConstant(module, "__author__", "lambdaphoenix") <
        0) {
        return -1;
    }
    if (PyModule_AddStringConstant(module, "__version__", "0.1.0") < 0) {
        return -1;
    }
    if (PyModule_AddStringConstant(module, "__license__", "Apache-2.0") < 0) {
        return -1;
    }
    if (PyModule_AddStringConstant(
            module, "__license_url__",
            "https://github.com/lambdaphoenix/cbits/blob/main/LICENSE") < 0) {
        return -1;
    }
    return 0;
}

/**
 * @brief Module initialization slots.
 *
 * Lists callbacks invoked when the module is loaded; here,
 * we use Py_mod_exec to register types and module constants.
 *
 * @see PyModuleDef_Slot
 */
static PyModuleDef_Slot cbits_module_slots[] = {
    {Py_mod_exec, cbits_module_exec},
    {0, NULL},
};

/**
 * @brief Definition of the _cbits extension module.
 *
 * Describes the module’s name, docstring, memory footprint,
 * and its initialization slot table.
 *
 * @see PyModuleDef
 */
static PyModuleDef cbits_module = {
    .m_base = PyModuleDef_HEAD_INIT,
    .m_name = "_cbits",
    .m_doc = PyDoc_STR("cbits"),
    .m_size = 0,
    .m_slots = cbits_module_slots,
};

/**
 * @brief Python entrypoint for _cbits extension module.
 * @param void
 * @return New module object (borrowed reference).
 */
PyMODINIT_FUNC
PyInit__cbits(void)
{
    return PyModuleDef_Init(&cbits_module);
}
