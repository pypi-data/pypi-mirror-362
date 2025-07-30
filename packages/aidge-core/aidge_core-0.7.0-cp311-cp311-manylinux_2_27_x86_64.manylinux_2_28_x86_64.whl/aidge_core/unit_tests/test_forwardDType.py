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

# List of all dtype defined by Aidge
ALL_AIDGE_DTYPE = [i for i in aidge_core.dtype.__members__.values() if i != aidge_core.dtype.any]

oh_no =[]

class test_forwardDType(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    ### HELPER FUNCTIONS ###
    def verify_node_out_dtype(self, node, out_dtype):
        """Helper function to verify output data type of a node
        """
        operator = node.get_operator()
        self.assertEqual(operator.nb_outputs(), len(out_dtype), "Error in test design, the number of outputs provided does not correspond to the number of outputs of the operator.")
        for out_idx in range(operator.nb_outputs()):
            tensor_dtype = operator.get_output(out_idx).dtype()
            self.assertEqual(tensor_dtype, out_dtype[out_idx], f"Node {node.name()}({node.type()}) output#{out_idx} is {tensor_dtype}, expected {out_dtype[out_idx]}")

    def run_node_test(self, node, in_dtype, out_dtype):
        """Run forwardDType unit test on the graph

        :param graph: GraphView to call forwardDtype on
        :type graph: aidge_core.GraphView
        :param in_dtype: List of input type to forward
        :type in_dtype: List[aidge_core.dtype]
        :param out_dtype: List of expected output type
        :type out_dtype: List[aidge_core.dtype]
        """
        op = node.get_operator()

        for in_idx in range(len(in_dtype)):
            in_tensor = aidge_core.Tensor()
            in_tensor.set_datatype(in_dtype[in_idx])
            op.set_input(in_idx, in_tensor)

        self.assertTrue(op.forward_dtype(), "Forward data type failed")
        self.verify_node_out_dtype(node, out_dtype)

    def run_graph_test(self, graph, in_dtype, out_dtype):
        """Run forwardDType unit test on the graph

        :param graph: GraphView to call forwardDtype on
        :type graph: aidge_core.GraphView
        :param in_dtype: List of input type to forward
        :type in_dtype: List[aidge_core.dtype]
        :param out_dtype: Dictionary of node name and expected output type
        :type out_dtype: Dict[str: List[aidge_core.dtype]]
        """
        # Loop to create an empty tensor for each operator outputs
        # This replace a forwardDims!
        # for node in graph.get_nodes():
        #     op = node.get_operator()
        #     if op.type() == aidge_core.ProducerOp.Type and op.attr.constant:
        #         # Cannot set_output for constant Producer
        #         continue
        #     for out_idx in range(op.nb_outputs()):
        #         out_tensor = aidge_core.Tensor()
        #         oh_no.append(out_tensor)
        #         op.set_output(out_idx, out_tensor)

        self.assertTrue(graph.forward_dtype(in_dtype), "Forward data type failed")
        for node in graph.get_nodes():
            if node.name() not in out_dtype:
                print(f"Warning: {node.name()}({node.type()}) if not tested!")
            else:
                self.verify_node_out_dtype(node, out_dtype[node.name()])

    ### TESTING_OPERATORS ###
    # Please ensure test cases are written in alphabetic order!

    def test_Abs_forward_dtype(self):
        pass

    def test_Add_forward_dtype(self):
        for in_dtype in ALL_AIDGE_DTYPE:
            with self.subTest(dtype=f"Add forward_dtype: {in_dtype}"):
                node = aidge_core.Div(name="add")
                self.run_node_test(node, [in_dtype, in_dtype], [in_dtype])

    def test_And_forward_dtype(self):
        pass

    def test_ArgMax_forward_dtype(self):
        for in_dtype in ALL_AIDGE_DTYPE:
            with self.subTest(dtype=f"ArgMax forward_dtype: {in_dtype}"):
                node = aidge_core.ArgMax(name="ArgMax")
                self.run_node_test(node, [in_dtype], [aidge_core.dtype.int64])

    def test_Atan_forward_dtype(self):
        pass

    def test_AvgPooling_forward_dtype(self):
        pass

    def test_BatchNorm_forward_dtype(self):
        pass

    def test_BitShift_forward_dtype(self):
        pass

    def test_Cast_forward_dtype(self):
        for cast_dtype in ALL_AIDGE_DTYPE:
            for in_dtype in ALL_AIDGE_DTYPE:
                with self.subTest(dtype=f"Cast[{in_dtype}] forward_dtype:  {cast_dtype}"):
                    cast = aidge_core.Cast(cast_dtype, name="Cast")
                    # Whatever input type, expected out type is cast_dtype
                    self.run_node_test(cast, [in_dtype], [cast_dtype])

    def test_Clip_forward_dtype(self):
        pass

    def test_Concat_forward_dtype(self):
        pass

    def test_ConstantOfShape_forward_dtype(self):
        for in_dtype in ALL_AIDGE_DTYPE:
            with self.subTest(dtype=f"ConstantOfShape forward_dtype: {in_dtype}"):
                node = aidge_core.ConstantOfShape(name="ConstantOfShape")
                value_tensor = aidge_core.Tensor()
                value_tensor.set_datatype(in_dtype)
                node.get_operator().attr.set_attr("value", value_tensor)
                self.run_node_test(node, [aidge_core.dtype.int64], [in_dtype])

    def test_Conv_forward_dtype(self):
        test_cases = [
            ("float32", [aidge_core.dtype.float32] * 3, [aidge_core.dtype.float32]),
            ("int8", [aidge_core.dtype.int8, aidge_core.dtype.int8, aidge_core.dtype.int32], [aidge_core.dtype.int32]),
        ]

        for name, in_dtype, out_dtype in test_cases:
            with self.subTest(dtype=name):
                node = aidge_core.Conv2D(1, 1, [2,2], name="Conv2D")
                self.run_node_test(node, in_dtype, out_dtype)

    def test_Conv_nobias_forward_dtype(self):
        test_cases = [
            ("float32", [aidge_core.dtype.float32] * 2, [aidge_core.dtype.float32]),
            ("float16", [aidge_core.dtype.float16] * 2, [aidge_core.dtype.float16]),
            ("int8", [aidge_core.dtype.int8, aidge_core.dtype.int8], [aidge_core.dtype.int32]),
            ("int4", [aidge_core.dtype.int4, aidge_core.dtype.int4], [aidge_core.dtype.int32]),
        ]

        for name, in_dtype, out_dtype in test_cases:
            with self.subTest(dtype=name):
                node = aidge_core.Conv2D(1, 1, [2,2], no_bias=True, name="Conv2D")
                self.run_node_test(node, in_dtype, out_dtype)

    def test_ConvDepthWise_forward_dtype(self):
        test_cases = [
            ("float32", [aidge_core.dtype.float32] * 3, [aidge_core.dtype.float32]),
            ("int8", [aidge_core.dtype.int8, aidge_core.dtype.int8, aidge_core.dtype.int32], [aidge_core.dtype.int32]),
        ]

        for name, in_dtype, out_dtype in test_cases:
            with self.subTest(dtype=name):
                node = aidge_core.ConvDepthWise2D(1, [2,2], name="ConvDepthWise2D")
                self.run_node_test(node, in_dtype, out_dtype)

    def test_ConvDepthWise_nobias_forward_dtype(self):
        test_cases = [
            ("float32", [aidge_core.dtype.float32] * 2, [aidge_core.dtype.float32]),
            ("float16", [aidge_core.dtype.float16] * 2, [aidge_core.dtype.float16]),
            ("int8", [aidge_core.dtype.int8, aidge_core.dtype.int8], [aidge_core.dtype.int32]),
            ("int4", [aidge_core.dtype.int4, aidge_core.dtype.int4], [aidge_core.dtype.int32]),
        ]

        for name, in_dtype, out_dtype in test_cases:
            with self.subTest(dtype=name):
                node = aidge_core.ConvDepthWise2D(1, [2,2], no_bias=True, name="ConvDepthWise2D")
                self.run_node_test(node, in_dtype, out_dtype)

    def test_ConvTranspose_forward_dtype(self):
        test_cases = [
            ("float32", [aidge_core.dtype.float32] * 3, [aidge_core.dtype.float32]),
            ("int8", [aidge_core.dtype.int8, aidge_core.dtype.int8, aidge_core.dtype.int32], [aidge_core.dtype.int32]),
        ]

        for name, in_dtype, out_dtype in test_cases:
            with self.subTest(dtype=name):
                node = aidge_core.ConvTranspose2D(1, 1, [2,2], name="ConvTranspose2D")
                self.run_node_test(node, in_dtype, out_dtype)

    def test_ConvTranspose_nobias_forward_dtype(self):
        test_cases = [
            ("float32", [aidge_core.dtype.float32] * 2, [aidge_core.dtype.float32]),
            ("float16", [aidge_core.dtype.float16] * 2, [aidge_core.dtype.float16]),
            ("int8", [aidge_core.dtype.int8, aidge_core.dtype.int8], [aidge_core.dtype.int32]),
            ("int4", [aidge_core.dtype.int4, aidge_core.dtype.int4], [aidge_core.dtype.int32]),
        ]

        for name, in_dtype, out_dtype in test_cases:
            with self.subTest(dtype=name):
                node = aidge_core.ConvTranspose2D(1, 1, [2,2], no_bias=True, name="ConvTranspose2D")
                self.run_node_test(node, in_dtype, out_dtype)

    def test_CryptoHash_forward_dtype(self):
        pass

    def test_DepthToSpace_forward_dtype(self):
        pass

    def test_Div_forward_dtype(self):
        for in_dtype in ALL_AIDGE_DTYPE:
            with self.subTest(dtype=f"Div forward_dtype: {in_dtype}"):
                node = aidge_core.Div(name="Div")
                self.run_node_test(node, [in_dtype, in_dtype], [in_dtype])

    def test_Equal_forward_dtype(self):
        pass

    def test_Erf_forward_dtype(self):
        pass

    def test_Expand_forward_dtype(self):
        for in_dtype in ALL_AIDGE_DTYPE:
            with self.subTest(dtype=f"Expand forward_dtype: {in_dtype}"):
                node = aidge_core.Expand(name="Expand")
                self.run_node_test(node, [in_dtype, aidge_core.dtype.int64], [in_dtype])

    def test_FC_forward_dtype(self):
        test_cases = [
            ("float32", [aidge_core.dtype.float32] * 3, [aidge_core.dtype.float32]),
            ("int8", [aidge_core.dtype.int8, aidge_core.dtype.int8, aidge_core.dtype.int32], [aidge_core.dtype.int32]),
        ]

        for name, in_dtype, out_dtype in test_cases:
            with self.subTest(dtype=name):
                node = aidge_core.FC(1, 1, name="FC")
                self.run_node_test(node, in_dtype, out_dtype)

    def test_FC_nobias_forward_dtype(self):
        test_cases = [
            ("float32", [aidge_core.dtype.float32] * 2, [aidge_core.dtype.float32]),
            ("float16", [aidge_core.dtype.float16] * 2, [aidge_core.dtype.float16]),
            ("int8", [aidge_core.dtype.int8, aidge_core.dtype.int8], [aidge_core.dtype.int32]),
            ("int4", [aidge_core.dtype.int4, aidge_core.dtype.int4], [aidge_core.dtype.int32]),
        ]

        for name, in_dtype, out_dtype in test_cases:
            with self.subTest(dtype=name):
                node = aidge_core.FC(1, 1, True, name="FC")
                self.run_node_test(node, in_dtype, out_dtype)

    def test_FC_nobias_not_created(self):
        # forwardDType should not set bias in the case of nobias!
        fc = aidge_core.FC(1, 1, True)
        g = aidge_core.sequential([fc])
        # Trying to set bias when nobias!
        g.forward_dtype([aidge_core.dtype.float32, aidge_core.dtype.float32])
        # Check bias is not created!
        assert (fc.get_operator().get_input(2) is None)

    def test_Flatten_forward_dtype(self):
        pass

    def test_Fold_forward_dtype(self):
        pass

    def test_Gather_forward_dtype(self):
        for in_dtype in ALL_AIDGE_DTYPE:
            with self.subTest(dtype=f"Gather forward_dtype: {in_dtype}"):
                node = aidge_core.Gather(name="Gather")
                self.run_node_test(node, [in_dtype], [in_dtype])

    def test_GenericOperator_forward_dtype(self):
        pass

    def test_GlobalAveragePooling_forward_dtype(self):
        pass

    def test_GridSample_forward_dtype(self):
        pass

    def test_Hardmax_forward_dtype(self):
        for in_dtype in ALL_AIDGE_DTYPE:
            with self.subTest(dtype=f"HardMax forward_dtype: {in_dtype}"):
                # no need to check for different axis dtype is perpendicular to axis param
                node = aidge_core.Hardmax(axis=0, name=f"HardMax axis")
                self.run_node_test(node, [in_dtype], [in_dtype])


    def test_Heaviside_forward_dtype(self):
        pass

    def test_ILayerNorm_forward_dtype(self):
        pass

    def test_Identity_forward_dtype(self):
        pass

    def test_LRN_forward_dtype(self):
        pass

    def test_LeakyReLU_forward_dtype(self):
        pass

    def test_Ln_forward_dtype(self):
        pass

    def test_MatMul_forward_dtype(self):
        pass

    def test_MaxPooling_forward_dtype(self):
        for in_dtype in ALL_AIDGE_DTYPE:
            with self.subTest(dtype=f"MaxPooling forward_dtype: {in_dtype}"):
                node = aidge_core.MaxPooling2D([2,2], name="MaxPooling")
                self.run_node_test(node, [in_dtype], [in_dtype, aidge_core.dtype.int64])

    def test_Memorize_forward_dtype(self):
        pass

    def test_MetaOperator_forward_dtype(self):
        pass

    def test_MetaOperatorDefs_forward_dtype(self):
        pass

    def test_Mod_forward_dtype(self):
        pass

    def test_Move_forward_dtype(self):
        pass

    def test_Mul_forward_dtype(self):
        for in_dtype in ALL_AIDGE_DTYPE:
            with self.subTest(dtype=f"Mul forward_dtype: {in_dtype}"):
                node = aidge_core.Mul(name="Mul")
                self.run_node_test(node, [in_dtype, in_dtype], [in_dtype])

    def test_Pad_forward_dtype(self):
        pass

    def test_Pop_forward_dtype(self):
        pass

    def test_Pow_forward_dtype(self):
        pass

    def test_ReLU_forward_dtype(self):
        for in_dtype in ALL_AIDGE_DTYPE:
            with self.subTest(dtype=f"ReLU forward_dtype: {in_dtype}"):
                node = aidge_core.ReLU(name="Relu")
                self.run_node_test(node, [in_dtype], [in_dtype])

    def test_ReduceMean_forward_dtype(self):
        pass

    def test_ReduceSum_forward_dtype(self):
        pass

    def test_Reshape_forward_dtype(self):
        pass

    def test_Resize_forward_dtype(self):
        scale_type = [
            aidge_core.dtype.float16,
            aidge_core.dtype.float32,
            aidge_core.dtype.float64,
        ]
        for in_dtype in ALL_AIDGE_DTYPE:
            for scale_dtype in scale_type:
                with self.subTest(dtype=f"Resize forward_dtype: {in_dtype}, {scale_dtype}"):
                    node = aidge_core.Resize(name="Resize")
                    self.run_node_test(node, [in_dtype, scale_dtype, aidge_core.dtype.int64], [in_dtype])

    def test_Round_forward_dtype(self):
        pass

    def test_Scaling_forward_dtype(self):
        pass

    def test_Select_forward_dtype(self):
        pass

    def test_Shape_forward_dtype(self):
        pass

    def test_ShiftGELU_forward_dtype(self):
        pass

    def test_ShiftMax_forward_dtype(self):
        pass

    def test_Sigmoid_forward_dtype(self):
        pass

    def test_Slice_forward_dtype(self):
        for in_dtype in ALL_AIDGE_DTYPE:
            with self.subTest(dtype=f"Slice forward_dtype: {in_dtype}"):
                node = aidge_core.Slice(name="Slice")
                self.run_node_test(node, [
                    in_dtype,
                    aidge_core.dtype.int64,
                    aidge_core.dtype.int64,
                    aidge_core.dtype.int64,
                    aidge_core.dtype.int64],
                    [in_dtype])

    def test_Softmax_forward_dtype(self):
        pass

    def test_Split_forward_dtype(self):
        for in_dtype in ALL_AIDGE_DTYPE:
            with self.subTest(dtype=f"Split forward_dtype: {in_dtype}"):
                node = aidge_core.Split(1, name="Split")
                self.run_node_test(node, [
                    in_dtype,
                    aidge_core.dtype.int64],
                    [in_dtype])

    def test_Sqrt_forward_dtype(self):
        pass

    def test_Squeeze_forward_dtype(self):
        for in_dtype in ALL_AIDGE_DTYPE:
            with self.subTest(dtype=f"Squeeze forward_dtype: {in_dtype}"):
                node = aidge_core.Squeeze(name="Squeeze")
                self.run_node_test(node, [
                    in_dtype,
                    aidge_core.dtype.int64],
                    [in_dtype])

    def test_Stack_forward_dtype(self):
        pass

    def test_Sub_forward_dtype(self):
        for in_dtype in ALL_AIDGE_DTYPE:
            with self.subTest(dtype=f"Add forward_dtype: {in_dtype}"):
                node = aidge_core.Sub(name="sub")
                self.run_node_test(node, [in_dtype, in_dtype], [in_dtype])

    def test_Tanh_forward_dtype(self):
        pass

    def test_TopK_forward_dtype(self):
        for in_dtype in ALL_AIDGE_DTYPE:
            with self.subTest(dtype=f"Add forward_dtype: {in_dtype}"):
                node = aidge_core.TopK(name="TopK")
                self.run_node_test(node, [in_dtype, aidge_core.dtype.int64], [in_dtype, aidge_core.dtype.int64])

    def test_Transpose_forward_dtype(self):
        pass

    def test_Unfold_forward_dtype(self):
        pass

    def test_Unsqueeze_forward_dtype(self):
        for in_dtype in ALL_AIDGE_DTYPE:
            with self.subTest(dtype=f"Unsqueeze forward_dtype: {in_dtype}"):
                node = aidge_core.Unsqueeze(name="Unsqueeze")
                self.run_node_test(node, [
                    in_dtype,
                    aidge_core.dtype.int64],
                    [in_dtype])

    def test_WeightInterleaving_forward_dtype(self):
        pass


    ### TESTING GRAPH ###

    def test_shuffle_net(self):
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
        reshape_op_1   = aidge_core.Reshape(name=  "reshape_op_1")
        reshape_op_2   = aidge_core.Reshape(name=  "reshape_op_2")
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

        shuffle_net_graph = aidge_core.generate_graph([y])
        for in_dtype in ALL_AIDGE_DTYPE:
            with self.subTest(dtype=f"ShuffleNet {in_dtype}"):
                output_dtype = {
                    "shape_op_1":     [aidge_core.dtype.int64],
                    "shape_op_2":     [aidge_core.dtype.int64],
                    "shape_op_3":     [aidge_core.dtype.int64],
                    "shape_op_4":     [aidge_core.dtype.int64],
                    "gather_op_1":    [aidge_core.dtype.int64],
                    "gather_op_3":    [aidge_core.dtype.int64],
                    "gather_op_2":    [aidge_core.dtype.int64],
                    "gather_op_4":    [aidge_core.dtype.int64],
                    "div_op":         [aidge_core.dtype.int64],
                    "unsqueeze_op_1": [aidge_core.dtype.int64],
                    "unsqueeze_op_2": [aidge_core.dtype.int64],
                    "unsqueeze_op_3": [aidge_core.dtype.int64],
                    "unsqueeze_op_4": [aidge_core.dtype.int64],
                    "unsqueeze_op_5": [aidge_core.dtype.int64],
                    "unsqueeze_op_6": [aidge_core.dtype.int64],
                    "unsqueeze_op_7": [aidge_core.dtype.int64],
                    "unsqueeze_op_8": [aidge_core.dtype.int64],
                    "unsqueeze_op_9": [aidge_core.dtype.int64],
                    "concat_op_1":    [aidge_core.dtype.int64],
                    "concat_op_2":    [aidge_core.dtype.int64],
                    "two_a":          [aidge_core.dtype.int64],
                    "two_b":          [aidge_core.dtype.int64],
                    "reshape_op_1":   [in_dtype],
                    "reshape_op_2":   [in_dtype],
                    "transpose_op_1": [in_dtype],
                    "Input":          [in_dtype]
                }
                self.run_graph_test(shuffle_net_graph, [in_dtype], output_dtype)

if __name__ == '__main__':
    unittest.main()
