"""
Copyright (c) 2023 CEA-List

This program and the accompanying materials are made available under the
terms of the Eclipse Public License 2.0 which is available at
http://www.eclipse.org/legal/epl-2.0.

SPDX-License-Identifier: EPL-2.0
"""

import unittest
import aidge_core
from functools import reduce

import numpy as np

GLOBAL_CPT = 0

class testImpl(aidge_core.OperatorImpl):
    def __init__(self, op: aidge_core.Operator):
        aidge_core.OperatorImpl.__init__(self, op, 'cpu') # Required to avoid type error !

    def forward(self):
        global GLOBAL_CPT
        GLOBAL_CPT += 1

class test_OperatorImpl(unittest.TestCase):
    """Test Op
    """
    def setUp(self):
        global GLOBAL_CPT
        GLOBAL_CPT = 0
    def tearDown(self):
        pass

    def test_setImplementation(self):
        """Test setting an implementation manually
        """
        global GLOBAL_CPT
        matmul = aidge_core.GenericOperator("MatMul", 1, 0, 1, name="MatMul0")
        generic_matmul_op = matmul.get_operator()
        generic_matmul_op.set_forward_dims(lambda x: x)
        generic_matmul_op.set_impl(testImpl(generic_matmul_op))
        generic_matmul_op.set_input(0, aidge_core.Tensor(np.arange(18).reshape(1,2,3,3)))
        generic_matmul_op.forward()
        self.assertEqual(GLOBAL_CPT, 1)

    def test_Registrar_setOp(self):
        """Test registering an implementation
        """
        global GLOBAL_CPT
        aidge_core.register_Conv2DOp("cpu", testImpl)
        self.assertTrue("cpu" in aidge_core.get_keys_Conv2DOp())
        conv = aidge_core.Conv2D(2,2,[1,1], name="Conv0")
        conv.get_operator().set_backend("cpu")
        conv.get_operator().set_input(0, aidge_core.Tensor(np.arange(18).reshape(1,2,3,3)))
        conv.get_operator().forward()
        self.assertEqual(GLOBAL_CPT, 1)

    def test_Registrar_setGraphView(self):
        """Test registering an implementation
        """
        global GLOBAL_CPT
        aidge_core.register_Conv2DOp("cpu", testImpl)
        aidge_core.register_ProducerOp("cpu", testImpl)
        self.assertTrue("cpu" in aidge_core.get_keys_Conv2DOp())
        conv = aidge_core.Conv2D(2,2,[1,1], name="Conv0")
        model = aidge_core.sequential([conv])
        model.set_backend("cpu")
        conv.get_operator().set_input(0, aidge_core.Tensor(np.arange(18).reshape(1,2,3,3)))
        conv.get_operator().forward()
        self.assertEqual(GLOBAL_CPT, 1)

if __name__ == '__main__':
    unittest.main()
