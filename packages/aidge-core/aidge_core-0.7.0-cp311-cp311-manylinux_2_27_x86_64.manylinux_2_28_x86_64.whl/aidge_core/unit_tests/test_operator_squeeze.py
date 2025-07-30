"""
Copyright (c) 2023 CEA-List

This program and the accompanying materials are made available under the
terms of the Eclipse Public License 2.0 which is available at
http://www.eclipse.org/legal/epl-2.0.

SPDX-License-Identifier: EPL-2.0
"""

import unittest
import aidge_core
from aidge_core import Log
import numpy as np
from numpy import testing as npt


class TestSqueeze(unittest.TestCase):
    """
    Test squeeze operator
    """

    def setUp(self):
        ############DEFINING INPUT AND OUTPUTS FOR TESTS
        axes_to_squeeze_0 = [0]
        axes_to_squeeze_many = [0, 1, 4]
        axes_to_squeeze_all = []
        axes_to_squeeze_error = [1, 2, 4, 5, 10, 3, 42, 127, 12, 3, 4, 1, 4, 50]

        squeeze_dim_0 = aidge_core.Squeeze(axes_to_squeeze_0, name="squeeze_dim_0")
        squeeze_many = aidge_core.Squeeze(axes_to_squeeze_many, name="squeeze_many")
        squeeze_all = aidge_core.Squeeze(axes_to_squeeze_all, name="squeeze_all")
        squeeze_error = aidge_core.Squeeze(axes_to_squeeze_error, name="squeeze_error")

        input_1_data_shape = np.array([1, 2, 3])
        input_2_data_hape = np.array([1, 1, 3, 3, 1, 9])
        input_3_data_shape = np.array([1])
        input_4_data_shape = np.array([1, 1, 4])

        input_axes_0 = axes_to_squeeze_0
        input_axes_many = axes_to_squeeze_many
        input_axes_all = axes_to_squeeze_all
        # input_axes_error = aidge_core.Tensor(axes_to_squeeze_error)

        ####################### DEFINING TEST RUNS
        self.tests_axes_defined_by_attribute = [
            (input_1_data_shape, squeeze_dim_0, np.array([2, 3])),
            (input_1_data_shape, squeeze_all, np.array([2, 3])),
            (input_2_data_hape, squeeze_dim_0, np.array([1, 3, 3, 1, 9])),
            (input_2_data_hape, squeeze_many, np.array([3, 3, 9])),
            (input_2_data_hape, squeeze_all, np.array([3, 3, 9])),
            (input_3_data_shape, squeeze_dim_0, np.array([])),
            (input_3_data_shape, squeeze_all, np.array([])),
            (input_4_data_shape, squeeze_dim_0, np.array([1, 4])),
            (input_4_data_shape, squeeze_all, np.array([4])),
        ]

        # operators are puprposefully chosen with different predefined attribute than the input_axes tensor
        self.tests_axes_defined_by_input = [
            (input_1_data_shape, input_axes_0, squeeze_error, np.array([2, 3])),
            (input_1_data_shape, input_axes_all, squeeze_error, np.array([2, 3])),
            (input_2_data_hape, input_axes_0, squeeze_error, np.array([1, 3, 3, 1, 9])),
            (input_2_data_hape, input_axes_many, squeeze_error, np.array([3, 3, 9])),
            (input_2_data_hape, input_axes_all, squeeze_error, np.array([3, 3, 9])),
            (input_3_data_shape, input_axes_0, squeeze_error, np.array([])),
            (input_3_data_shape, input_axes_all, squeeze_error, np.array([])),
            (input_4_data_shape, input_axes_0, squeeze_error, np.array([1, 4])),
            (input_4_data_shape, input_axes_all, squeeze_error, np.array([4])),
        ]
        self.test_error = [
            (input_1_data_shape, squeeze_error),
            (input_1_data_shape, squeeze_many),
            (input_3_data_shape, squeeze_many),
            (input_4_data_shape, squeeze_many),
        ]
        return

    def tearDown(self):
        pass

    def test_axes_defined_via_tensor_input(self):
        Log.notice("\ntest_axes_defined_via_tensor_input")
        for index, (
            input_shape,
            input_axes_to_squeeze,
            squeeze_node_template,
            output_shape,
        ) in enumerate(self.tests_axes_defined_by_input):
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

    def test_axes_defined_via_attribute(self):
        Log.notice("\ntest_axes_defined_via_attribute")
        for index, (input_shape, squeeze_node_template, output_shape) in enumerate(
            self.tests_axes_defined_by_attribute
        ):
            test_squeeze_node = squeeze_node_template
            test_squeeze_op = test_squeeze_node.get_operator()

            print(f"\nTest {index}")
            print(f"input size : {input_shape.shape}")
            print(f"operator : {test_squeeze_node}")
            print(f"expected output_shape : {output_shape}")

            test_squeeze_node.get_operator().set_backend("cpu")

            input_values = np.ones(shape=input_shape, dtype=np.float32)
            output_values = np.ones(shape=output_shape, dtype=np.float32)
            input_data = aidge_core.Tensor(input_values)
            input_data.set_datatype(aidge_core.dtype.float32)
            input_data.set_backend("cpu")
            test_squeeze_op.set_input(0, input_data)

            test_squeeze_op.forward_dims()
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
        return

    def test_error(self):
        for input_shape, squeeze_node_template in self.test_error:
            test_squeeze_node = squeeze_node_template
            test_squeeze_op = test_squeeze_node.get_operator()

            input_values = np.ones(shape=input_shape)
            input_data = aidge_core.Tensor(input_values)
            input_data.set_datatype(aidge_core.dtype.float32)
            input_data.set_backend("cpu")
            test_squeeze_op.set_input(0, input_data)

            self.assertFalse(test_squeeze_op.forward_dims())
        return


if __name__ == "__main__":
    unittest.main()
