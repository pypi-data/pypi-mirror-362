"""
Copyright (c) 2023 CEA-List

This program and the accompanying materials are made available under the
terms of the Eclipse Public License 2.0 which is available at
http://www.eclipse.org/legal/epl-2.0.

SPDX-License-Identifier: EPL-2.0
"""

import unittest
import numpy as np

import aidge_core

class test_tensor_scalar(unittest.TestCase):
    """Test tensor binding for scalar (0-rank) tensors
    """
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def _scalar_np_array(self, dtype=None):
        return np.array(1, dtype=dtype)

    def _scalar_np(self, dtype=None):
        return np.int32(1).astype(dtype)

    def test_np_array_bool_to_tensor(self):
        np_array = self._scalar_np_array(dtype="bool")
        t = aidge_core.Tensor(np_array)
        self.assertEqual(t.dtype(), aidge_core.dtype.boolean)

    def test_np_array_int_to_tensor(self):
        np_array = self._scalar_np_array(dtype="int8")
        t = aidge_core.Tensor(np_array)
        self.assertEqual(t.dtype(), aidge_core.dtype.int8)

        np_array = self._scalar_np_array(dtype="int16")
        t = aidge_core.Tensor(np_array)
        self.assertEqual(t.dtype(), aidge_core.dtype.int16)

        np_array = self._scalar_np_array(dtype="int32")
        t = aidge_core.Tensor(np_array)
        self.assertEqual(t.dtype(), aidge_core.dtype.int32)

        np_array = self._scalar_np_array(dtype="int64")
        t = aidge_core.Tensor(np_array)
        self.assertEqual(t.dtype(), aidge_core.dtype.int64)

    def test_np_array_uint_to_tensor(self):
        np_array = self._scalar_np_array(dtype="uint8")
        t = aidge_core.Tensor(np_array)
        self.assertEqual(t.dtype(), aidge_core.dtype.uint8)

        np_array = self._scalar_np_array(dtype="uint16")
        t = aidge_core.Tensor(np_array)
        self.assertEqual(t.dtype(), aidge_core.dtype.uint16)

        np_array = self._scalar_np_array(dtype="uint32")
        t = aidge_core.Tensor(np_array)
        self.assertEqual(t.dtype(), aidge_core.dtype.uint32)

        np_array = self._scalar_np_array(dtype="uint64")
        t = aidge_core.Tensor(np_array)
        self.assertEqual(t.dtype(), aidge_core.dtype.uint64)

    def test_np_scalar_bool_to_tensor(self):
        np_array = self._scalar_np(dtype="bool")
        t = aidge_core.Tensor(np_array)
        self.assertEqual(t.dtype(), aidge_core.dtype.boolean)

    def test_np_scalar_int_to_tensor(self):
        np_array = self._scalar_np(dtype="int8")
        t = aidge_core.Tensor(np_array)
        self.assertEqual(t.dtype(), aidge_core.dtype.int8)

        np_array = self._scalar_np(dtype="int16")
        t = aidge_core.Tensor(np_array)
        self.assertEqual(t.dtype(), aidge_core.dtype.int16)

        np_array = self._scalar_np(dtype="int32")
        t = aidge_core.Tensor(np_array)
        self.assertEqual(t.dtype(), aidge_core.dtype.int32)

        np_array = self._scalar_np(dtype="int64")
        t = aidge_core.Tensor(np_array)
        self.assertEqual(t.dtype(), aidge_core.dtype.int64)

    def test_np_scalar_uint_to_tensor(self):
        np_array = self._scalar_np(dtype="uint8")
        t = aidge_core.Tensor(np_array)
        self.assertEqual(t.dtype(), aidge_core.dtype.uint8)

        np_array = self._scalar_np(dtype="uint16")
        t = aidge_core.Tensor(np_array)
        self.assertEqual(t.dtype(), aidge_core.dtype.uint16)

        np_array = self._scalar_np(dtype="uint32")
        t = aidge_core.Tensor(np_array)
        self.assertEqual(t.dtype(), aidge_core.dtype.uint32)

        np_array = self._scalar_np(dtype="uint64")
        t = aidge_core.Tensor(np_array)
        self.assertEqual(t.dtype(), aidge_core.dtype.uint64)
        
    def test_np_array_float_to_tensor(self):
        np_array = self._scalar_np_array(dtype="float32")
        t = aidge_core.Tensor(np_array)
        self.assertEqual(t.dtype(), aidge_core.dtype.float32)
        np_array = self._scalar_np_array(dtype="float64")
        t = aidge_core.Tensor(np_array)
        self.assertEqual(t.dtype(), aidge_core.dtype.float64)

    def test_np_scalar_float_to_tensor(self):
        np_array = self._scalar_np(dtype="float32")
        t = aidge_core.Tensor(np_array)
        self.assertEqual(t.dtype(), aidge_core.dtype.float32)
        np_array = self._scalar_np(dtype="float64")
        t = aidge_core.Tensor(np_array)
        self.assertEqual(t.dtype(), aidge_core.dtype.float64)

    def test_getcoord_getidx_scalar(self):
        np_array = self._scalar_np_array()
        t = aidge_core.Tensor(np_array)
        coord = t.get_coord(0)
        self.assertEqual(tuple(coord), ())
        idx = t.get_idx(coord)
        self.assertEqual(idx, 0)

    def test_indexing_scalar(self):
        np_array = self._scalar_np_array()
        t = aidge_core.Tensor(np_array)
        val = t[0]
        self.assertEqual(val, np_array[()])

    def test_coord_indexing_scalar(self):
        np_array = self._scalar_np_array()
        t = aidge_core.Tensor(np_array)
        val = t[()]
        self.assertEqual(val, np_array[()])


if __name__ == '__main__':
    unittest.main()
