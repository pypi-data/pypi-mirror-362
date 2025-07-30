"""
Copyright (c) 2023 CEA-List

This program and the accompanying materials are made available under the
terms of the Eclipse Public License 2.0 which is available at
http://www.eclipse.org/legal/epl-2.0.

SPDX-License-Identifier: EPL-2.0
"""

import pytest
import aidge_core
import numpy as np
import itertools

def test_getavailable_backends():
    assert "cpu" in aidge_core.Tensor.get_available_backends()


@pytest.mark.parametrize("dtype, expected_dtype", [
    (np.bool, aidge_core.dtype.boolean),
    (np.int8, aidge_core.dtype.int8),
    (np.int16, aidge_core.dtype.int16),
    (np.int32, aidge_core.dtype.int32),
    (np.int64, aidge_core.dtype.int64),
    (np.uint8, aidge_core.dtype.uint8),
    (np.uint16, aidge_core.dtype.uint16),
    (np.uint32, aidge_core.dtype.uint32),
    (np.uint64, aidge_core.dtype.uint64),
    (np.float16, aidge_core.dtype.float16),
    (np.float32, aidge_core.dtype.float32),
    (np.float64, aidge_core.dtype.float64),
])
def test_numpy_dtype_conversion(dtype, expected_dtype):
    original_array = np.arange(9).reshape(1, 1, 3, 3).astype(dtype)

    # NumPy -> Tensor
    tensor = aidge_core.Tensor(original_array)
    assert tensor.dtype() == expected_dtype
    if np.issubdtype(dtype, np.floating):
        assert all(
            np.isclose(tensor_value, numpy_value, rtol=1e-3, atol=1e-5)
            for tensor_value, numpy_value in zip(tensor, original_array.flatten())
        )
    else:
        assert all(tensor_value == numpy_value for tensor_value, numpy_value in zip(tensor, original_array.flatten()))

    assert tuple(tensor.dims()) == original_array.shape

    # Tensor -> NumPy
    converted_array = np.array(tensor)

    # Validate shape
    assert converted_array.shape == original_array.shape

    # Validate data
    if np.issubdtype(dtype, np.floating):
        np.testing.assert_allclose(converted_array, original_array, rtol=1e-3, atol=1e-5)
    else:
        np.testing.assert_array_equal(converted_array, original_array)

def test_tensor_get_set():
    dims = [2, 2, 2]
    original_array = np.arange(np.prod(dims)).reshape(dims).astype(np.int32)
    tensor = aidge_core.Tensor(original_array)

    # Verify initial values match original array
    assert all(tensor_value == numpy_value for tensor_value, numpy_value in zip(tensor, original_array.flatten()))

    # Set all elements to a new value
    new_value = 42
    for i in range(len(tensor)):
        tensor[i] = new_value

    # Check that all elements have been updated
    assert all(tensor_value == new_value for tensor_value in tensor)

def test_tensor_get_coord_get_idx():
    dims = [2, 2, 2]
    tensor = aidge_core.Tensor(dims=dims)
    # Test that get_idx(get_coord(i)) == i for all flat indices
    for flat_idx in range(len(tensor)):
        coord = tensor.get_coord(flat_idx)
        idx = tensor.get_idx(coord)
        assert idx == flat_idx, f"Mismatch: idx={idx} vs flat_idx={flat_idx}, coord={coord}"

    # Additionally test that get_coord(get_idx(coord)) == coord for all possible coordinates
    all_coords = list(itertools.product(*[range(d) for d in dims]))
    for coord in all_coords:
        idx = tensor.get_idx(coord)
        recovered_coord = tensor.get_coord(idx)
        assert tuple(recovered_coord) == coord, f"Mismatch: recovered_coord={recovered_coord} vs coord={coord}, idx={idx}"

if __name__ == '__main__':
    print("Please run this with pytest")
