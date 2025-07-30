"""
Copyright (c) 2023 CEA-List

This program and the accompanying materials are made available under the
terms of the Eclipse Public License 2.0 which is available at
http://www.eclipse.org/legal/epl-2.0.

SPDX-License-Identifier: EPL-2.0
"""

import unittest
import aidge_core
import numpy as np
from numpy import testing as npt


class TestUnsqueeze(unittest.TestCase):
    """
    Test unsqueeze operator
    """

    def setUp(self):
        axis_to_unsqueeze_dim_0 = [0]
        axis_to_unsqueeze_many = [1, 4, 5]
        axis_to_unsqueeze_error_identical_index = [0, 0, 0]
        axis_to_unsqueeze_error_too_high_index = [50]
        axis_to_unsqueeze_onnx_test = [0, 4]
        unsqueeze_dim_0 = aidge_core.Unsqueeze(
            axis_to_unsqueeze_dim_0, name="unsqueeze_dim_0"
        )
        unsqueeze_many = aidge_core.Unsqueeze(
            axis_to_unsqueeze_many, name="unsqueeze_many"
        )
        unsqueeze_error_identical_index = aidge_core.Unsqueeze(
            axis_to_unsqueeze_error_identical_index,
            name="unsqueeze_error_identical_index",
        )
        unsqueeze_error_node = aidge_core.Unsqueeze(
            axis_to_unsqueeze_error_too_high_index,
            name="unsqueeze_error_index_too_high",
        )
        unsqueeze_onnx_test = aidge_core.Unsqueeze(
            axis_to_unsqueeze_onnx_test, name="unsqueeze taken from onnx documentation"
        )

        input_1_data_shape = np.array([1, 2, 3])
        input_2_data_shape = np.array([2, 1, 3, 3])
        input_3_data_shape = np.array([1, 1, 4])
        input_onnx_data_shape = np.array([3, 4, 5])

        input_axes_dim_0 = axis_to_unsqueeze_dim_0
        input_axes_many = axis_to_unsqueeze_many
        input_axes_onnx_test = axis_to_unsqueeze_onnx_test

        self.tests_axes_defined_by_attribute = [
            (input_1_data_shape, unsqueeze_dim_0, np.array([1, 1, 2, 3])),
            (input_2_data_shape, unsqueeze_dim_0, np.array([1, 2, 1, 3, 3])),
            (input_2_data_shape, unsqueeze_many, np.array([2, 1, 1, 3, 1, 1, 3])),
            (input_3_data_shape, unsqueeze_dim_0, np.array([1, 1, 1, 4])),
            (input_3_data_shape, unsqueeze_many, np.array([1, 1, 1, 4, 1, 1])),
            (input_onnx_data_shape, unsqueeze_onnx_test, np.array([1, 3, 4, 5, 1])),
        ]

        self.tests_axes_defined_by_tensor = [
            (
                input_1_data_shape,
                input_axes_dim_0,
                unsqueeze_error_node,
                np.array([1, 1, 2, 3]),
            ),
            (
                input_2_data_shape,
                input_axes_dim_0,
                unsqueeze_error_node,
                np.array([1, 2, 1, 3, 3]),
            ),
            (
                input_2_data_shape,
                input_axes_many,
                unsqueeze_error_node,
                np.array([2, 1, 1, 3, 1, 1, 3]),
            ),
            (
                input_3_data_shape,
                input_axes_dim_0,
                unsqueeze_error_node,
                np.array([1, 1, 1, 4]),
            ),
            (
                input_3_data_shape,
                input_axes_many,
                unsqueeze_error_node,
                np.array([1, 1, 1, 4, 1, 1]),
            ),
            (
                input_onnx_data_shape,
                input_axes_onnx_test,
                unsqueeze_error_node,
                np.array([1, 3, 4, 5, 1]),
            ),
        ]

        self.test_error = [
            (input_1_data_shape, unsqueeze_error_identical_index),
            (input_1_data_shape, unsqueeze_error_node),
            (input_1_data_shape, unsqueeze_many),  # dims too high
        ]
        return

    def tearDown(self):
        pass

    def test_axes_defined_by_attribute(self):
        for index, (
            input_shape,
            unsqueeze_template,
            expected_output_shape,
        ) in enumerate(self.tests_axes_defined_by_attribute):
            test_unsqueeze = unsqueeze_template
            test_unsqueeze_op = test_unsqueeze.get_operator()

            print(f"\nTest {index}")
            print(f"input size : {input_shape}")
            print(f"operator : {test_unsqueeze}")
            print(f"expected output_shape : {expected_output_shape}")

            test_unsqueeze_op.set_backend("cpu")

            input_values = np.ones(shape=input_shape, dtype=np.float32)
            expected_output_values = np.ones(
                shape=expected_output_shape, dtype=np.float32
            )
            input_tensor = aidge_core.Tensor(input_values)
            test_unsqueeze_op.set_input(0, input_tensor)

            test_unsqueeze_op.forward_dims()
            test_unsqueeze_op.forward()

            unsqueeze_output = test_unsqueeze_op.get_output(0)

            npt.assert_array_equal(
                unsqueeze_output.dims(),
                expected_output_shape,
                err_msg=f"UNSQUEEZE FAILURE : expected result dimensions differs from output's\n\toperator : {test_unsqueeze}\n\tinput.shape : {input_shape.shape}",
            )
            npt.assert_array_almost_equal(
                np.array(unsqueeze_output),
                expected_output_values,
                7,
                err_msg=f"UNSQUEEZE FAILURE : output tensor values differs from expected values\n\toperator : {test_unsqueeze}\n\tinput.shape : {input_shape.shape}",
            )
        return

    def test_axes_defined_via_tensor_input(self):
        for index, (
            input_shape,
            input_axes_to_squeeze,
            squeeze_node_template,
            output_shape,
        ) in enumerate(self.tests_axes_defined_by_tensor):
            test_squeeze_node = squeeze_node_template
            test_squeeze_op = test_squeeze_node.get_operator()

            print(f"\nTest {index}")
            print(f"input shape : {input_shape}")
            print(f"input axes: {np.array(input_axes_to_squeeze)}")
            print(f"operator : {test_squeeze_node}")
            print(f"expected output_shape : {output_shape}")

            test_squeeze_op.set_backend("cpu")
            test_squeeze_op.set_datatype(aidge_core.dtype.float32)

            input_values = np.ones(shape=input_shape, dtype=np.float32)
            output_values = np.ones(shape=output_shape, dtype=np.float32)

            input_data = aidge_core.Tensor(input_values)
            input_data.set_datatype(aidge_core.dtype.float32)
            input_data.set_backend("cpu")

            input_axes = aidge_core.Tensor(
                np.array(input_axes_to_squeeze, dtype=np.float32)
            )
            input_axes.set_datatype(aidge_core.dtype.int8)
            input_axes.set_backend("cpu")

            test_squeeze_op.set_input(0, input_data)
            test_squeeze_op.set_input(1, input_axes)

            self.assertEqual(test_squeeze_op.forward_dims(True), True)
            test_squeeze_op.forward()

            squeeze_output = test_squeeze_op.get_output(0)

            npt.assert_array_equal(
                squeeze_output.dims(),
                output_shape,
                err_msg=f"SQUEEZE FAILURE : expected result differs from output size\n\toperator : {test_squeeze_node}\n\tinput.shape : {input_shape.shape}",
            )
            npt.assert_array_almost_equal(
                np.array(squeeze_output, dtype=np.float32),
                output_values,
                7,
                err_msg=f"SQUEEZE FAILURE : output tensor values differs from expected values\n\toperator : {test_squeeze_node}\n\tinput.shape : {input_shape.shape}",
            )
            # self.assertEqual(test_squeeze_op.dims_forwarded(), True, "SQUEEZE_FAILURE : dims_forwarded failed.")
        return


if __name__ == "__main__":
    unittest.main()

