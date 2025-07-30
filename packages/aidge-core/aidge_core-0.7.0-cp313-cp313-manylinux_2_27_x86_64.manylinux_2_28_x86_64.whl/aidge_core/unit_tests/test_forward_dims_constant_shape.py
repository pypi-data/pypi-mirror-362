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

class DivImpl(aidge_core.OperatorImpl):
    """Div operator implementation to avoid dependency to backend_cpu"""

    def __init__(self, op: aidge_core.Operator):
        aidge_core.OperatorImpl.__init__(self, op, "div")
        self.op = op
        print("Creating divImpl")
    def forward(self):
        data_input_0 = np.array(self.op.get_input(0))
        data_input_1 = np.array(self.op.get_input(1))
        output =  (data_input_0 / data_input_1)
        self.op.set_output(0, aidge_core.Tensor(output)) # setting operator output

# Note: In this test, except Div, every operator are backend independent
aidge_core.register_DivOp("cpu", DivImpl)

class test_forward_dims_constant_shape(unittest.TestCase):
    """Test forwardDims with shapeAsConstant=True
    """
    def setUp(self):
        # Declaring constant values
        prod_two_a = aidge_core.Producer(aidge_core.Tensor(np.array(2, dtype=np.int64)), "two_a", constant=True)
        prod_two_b = aidge_core.Producer(aidge_core.Tensor(np.array(2, dtype=np.int64)), "two_b", constant=True)

        # Declaring operators
        shape_op_1     = aidge_core.Shape(name="shape_op_1")
        shape_op_2     = aidge_core.Shape(name="shape_op_2")
        shape_op_3     = aidge_core.Shape(name="shape_op_3")
        shape_op_4     = aidge_core.Shape(name="shape_op_4")
        gather_op_1    = aidge_core.Gather(axis = 0, indices = [0], name="gather_op_1")
        gather_op_2    = aidge_core.Gather(axis = 0, indices = [1], name="gather_op_2")
        gather_op_3    = aidge_core.Gather(axis = 0, indices = [2], name="gather_op_3")
        gather_op_4    = aidge_core.Gather(axis = 0, indices = [3], name="gather_op_4")
        div_op         = aidge_core.Div(name="div_op")


        u_op_1         = aidge_core.Unsqueeze(axes = [0], name="unsqueeze_op_1")
        u_op_2         = aidge_core.Unsqueeze(axes = [0], name="unsqueeze_op_2")
        u_op_3         = aidge_core.Unsqueeze(axes = [0], name="unsqueeze_op_3")
        u_op_4         = aidge_core.Unsqueeze(axes = [0], name="unsqueeze_op_4")
        u_op_5         = aidge_core.Unsqueeze(axes = [0], name="unsqueeze_op_5")
        u_op_6         = aidge_core.Unsqueeze(axes = [0], name="unsqueeze_op_6")
        u_op_7         = aidge_core.Unsqueeze(axes = [0], name="unsqueeze_op_7")
        u_op_8         = aidge_core.Unsqueeze(axes = [0], name="unsqueeze_op_8")
        u_op_9         = aidge_core.Unsqueeze(axes = [0], name="unsqueeze_op_9")
        concat_op_1    = aidge_core.Concat(5, name="concat_op_1")
        concat_op_2    = aidge_core.Concat(4, name="concat_op_2")
        reshape_op_1   = aidge_core.Reshape(name="reshape_op_1")
        reshape_op_2   = aidge_core.Reshape(name="reshape_op_2")
        transpose_op_1 = aidge_core.Transpose([0, 2, 1, 3, 4], name="transpose_op_1")

        # Declaring Connectors
        x = aidge_core.Connector(aidge_core.Identity(f"Input"))
        a = aidge_core.Connector(prod_two_a)
        b = aidge_core.Connector(prod_two_b)

        # Graph creation using functional declaration
        x1 = shape_op_1(x)
        x2 = shape_op_2(x)
        x3 = shape_op_3(x)
        x4 = shape_op_4(x)
        n = gather_op_1(x1)
        c = gather_op_2(x2)
        h = gather_op_3(x3)
        w = gather_op_4(x4)

        shape_1 = concat_op_1(u_op_1(n), u_op_2(a), u_op_3(div_op(c, b)), u_op_4(h), u_op_5(w))
        shape_2 = concat_op_2(u_op_6(n), u_op_7(c), u_op_8(h), u_op_9(w))

        y = reshape_op_2(transpose_op_1(reshape_op_1(x, shape_1)), shape_2)

        self.graph = aidge_core.generate_graph([y])


    def tearDown(self):
        pass

    def test_constant_shape_folding(self):
        # Note: Except Div every operator are backend independent
        self.graph.set_backend("cpu")
        self.graph.set_datatype(aidge_core.dtype.float32)

        aidge_core.constant_shape_folding(self.graph, [[5, 12, 24, 24]])
        self.assertEqual(len(self.graph.get_nodes()), 6, "After forward dims with constant folding we don't have the expected number of nodes.")


if __name__ == '__main__':
    unittest.main()
