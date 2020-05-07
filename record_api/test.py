import operator as op
import sys
import unittest
from unittest.mock import call, patch, ANY

import numpy as np

from . import Tracer


class TestMockNumPyMethod(unittest.TestCase):
    def setUp(self):
        self.a = np.arange(10)
        patcher = patch("record_api.core.log_call")
        self.mock = patcher.start()
        self.addCleanup(patcher.stop)
        self.tracer = Tracer("numpy")

    def assertCalls(self, *calls):
        self.assertListEqual(
            self.mock.mock_calls, [*calls],
        )

    def test_pos(self):
        with self.tracer:
            +self.a
        self.mock.assert_called_once_with(ANY, ANY, op.pos, self.a)

    def test_neg(self):
        with self.tracer:
            -self.a
        self.mock.assert_called_once_with(ANY, ANY, op.neg, self.a)

    def test_invert(self):
        with self.tracer:
            ~self.a
        self.mock.assert_called_once_with(ANY, ANY, op.invert, self.a)

    def test_add(self):
        with self.tracer:
            self.a + 10
        self.mock.assert_called_once_with(ANY, ANY, op.add, self.a, 10)

    def test_radd(self):
        with self.tracer:
            # verify regulaar add doesnt add
            10 + 10
            10 + self.a
        self.mock.assert_called_once_with(ANY, ANY, op.add, 10, self.a)

    def test_iadd(self):
        with self.tracer:
            self.a += 10
        self.mock.assert_called_once_with(ANY, ANY, op.iadd, self.a, 10)

    def test_getitem(self):
        l = [self.a]
        with self.tracer:
            self.a[0]
            # verify is value in np array doesn't count
            l[0]
        self.mock.assert_called_once_with(ANY, ANY, op.getitem, self.a, 0)

    def test_setitem(self):
        l = [0]
        with self.tracer:
            self.a[0] = 1
            # verify is value in np array doesn't count
            l[0] = self.a
        self.mock.assert_called_once_with(ANY, ANY, op.setitem, self.a, 0, 1)

    def test_setattr(self):
        with self.tracer:
            self.a.shape = (10, 1)
            # verify attr doesnt match
            o = lambda: None
            o.something = self.a  # type: ignore
        self.mock.assert_called_once_with(ANY, ANY, setattr, self.a, "shape", (10, 1))

    def test_tuple_unpack(self):
        with self.tracer:
            (*self.a, 10, *self.a)
        iter_ = call(ANY, ANY, iter, self.a)
        self.assertCalls(iter_, iter_)

    def test_tuple_unpack_with_call(self):
        def f(*args):
            pass

        with self.tracer:
            f(*self.a, 10, *self.a)
        iter_ = call(ANY, ANY, iter, self.a)
        self.assertCalls(iter_, iter_)

    def test_load_attr(self):
        o = lambda: None
        o.shape = (1,)  # type: ignore
        with self.tracer:
            self.a.shape
            # verify normal object doesn't trigger
            o.shape  # type: ignore
        self.mock.assert_called_once_with(ANY, ANY, getattr, self.a, "shape")

    def test_arange(self):
        with self.tracer:
            np.arange(10)
        self.mock.assert_called_once_with(ANY, ANY, np.arange, 10)

    def test_arange_in_fn(self):
        def fn():
            np.arange(10)

        with self.tracer:
            fn()
        self.mock.assert_called_once_with(ANY, ANY, np.arange, 10)

    def test_power(self):
        with self.tracer:
            np.power(100, 10)
        self.mock.assert_called_once_with(ANY, ANY, np.power, 100, 10)

    def test_sort(self):
        with self.tracer:
            self.a.sort(axis=0)
        self.assertCalls(
            call(ANY, ANY, getattr, self.a, "sort"),
            call(ANY, ANY, np.ndarray.sort, self.a, axis=0),
        )

    def test_eye(self):
        with self.tracer:
            np.eye(10, order="F")
        self.assertCalls(
            call(ANY, ANY, getattr, np, "eye"), call(ANY, ANY, np.eye, 10, order="F"),
        )

    def test_linspace(self):
        with self.tracer:
            np.linspace(3, 4, endpoint=False)
        self.assertCalls(
            call(ANY, ANY, getattr, np, "linspace"),
            call(ANY, ANY, np.linspace, 3, 4, endpoint=False),
        )

    def test_reshape(self):
        with self.tracer:
            self.a.reshape((5, 2))
        self.assertCalls(call(ANY, ANY, np.ndarray.reshape, self.a, (5, 2)),)

    def test_transpose(self):
        with self.tracer:
            self.a.T
        self.assertCalls(call(ANY, ANY, getattr, self.a, "T"))

    def test_concatenate(self):
        with self.tracer:
            np.concatenate((self.a, self.a), axis=0)
        self.assertCalls(
            call(ANY, ANY, getattr, np, "concatenate"),
            call(ANY, ANY, np.concatenate, (self.a, self.a), axis=0),
        )

    def test_ravel_list(self):
        """
        from numeric function to test array dispatch
        """
        with self.tracer:
            np.ravel([1, 2, 3])
        self.assertCalls(call(ANY, ANY, np.ravel, [1, 2, 3]))

    def test_ravel_array(self):
        """
        from numeric function to test array dispatch
        """
        with self.tracer:
            np.ravel(self.a)
        self.assertCalls(call(ANY, ANY, np.ravel, self.a))

    def test_std(self):
        with self.tracer:
            np.std(self.a)
        self.assertCalls(call(ANY, ANY, np.std, self.a))

    def test_builtin_types_no_call(self):
        with self.tracer:
            10 + 10
            10.2332 + 213
            12323.234 - 2342.40
        self.mock.assert_not_called()

if __name__ == "__main__":
    unittest.main()