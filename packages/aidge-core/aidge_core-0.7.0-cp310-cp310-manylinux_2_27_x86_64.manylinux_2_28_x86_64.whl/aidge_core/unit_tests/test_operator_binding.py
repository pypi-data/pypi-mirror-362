"""
Copyright (c) 2023 CEA-List

This program and the accompanying materials are made available under the
terms of the Eclipse Public License 2.0 which is available at
http://www.eclipse.org/legal/epl-2.0.

SPDX-License-Identifier: EPL-2.0
"""

import unittest
import aidge_core

class test_operator_binding(unittest.TestCase):
    """Very basic test to make sure the python APi is not broken.
    Can be remove in later stage of the developpement.
    """
    def setUp(self):
        self.generic_operator = aidge_core.GenericOperator("FakeConv", 1, 0, 1).get_operator()

    def tearDown(self):
        pass

    def test_default_name(self):
        op_type = "Conv"
        gop = aidge_core.GenericOperator(op_type, 1, 0, 1, "FictiveName")
        # check node name is not operator type
        self.assertNotEqual(gop.name(), "Conv")
        # check node name is not default
        self.assertNotEqual(gop.name(), "")

    def test_param_bool(self):
        self.generic_operator.attr.add_attr("bool", True)
        self.assertEqual(self.generic_operator.attr.has_attr("bool"), True)
        self.assertEqual(self.generic_operator.attr.get_attr("bool"), True)
        self.generic_operator.attr.del_attr("bool")
        self.assertEqual(self.generic_operator.attr.has_attr("bool"), False)

    def test_param_int(self):
        self.generic_operator.attr.add_attr("int", 1)
        self.assertEqual(self.generic_operator.attr.get_attr("int"), 1)

    def test_param_float(self):
        self.generic_operator.attr.add_attr("float", 2.0)
        self.assertEqual(self.generic_operator.attr.get_attr("float"), 2.0)

    def test_param_str(self):
        self.generic_operator.attr.add_attr("str", "value")
        self.assertEqual(self.generic_operator.attr.get_attr("str"), "value")

    def test_param_l_int(self):
        self.generic_operator.attr.add_attr("l_int", [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
        self.assertEqual(self.generic_operator.attr.get_attr("l_int"), [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])

    def test_param_l_bool(self):
        self.generic_operator.attr.add_attr("l_bool", [True, False, False, True])
        self.assertEqual(self.generic_operator.attr.get_attr("l_bool"), [True, False, False, True])

    def test_param_l_float(self):
        self.generic_operator.attr.add_attr("l_float", [2.0, 1.0])
        self.assertEqual(self.generic_operator.attr.get_attr("l_float"), [2.0, 1.0])

    def test_param_l_str(self):
        self.generic_operator.attr.add_attr("l_str", ["ok"])
        self.assertEqual(self.generic_operator.attr.get_attr("l_str"), ["ok"])

    def test_dynamicattribute_binding(self):
        # Check original C++ attributes are binded
        attrs = aidge_core.test_DynamicAttributes_binding()
        self.assertEqual(attrs.has_attr("a"), True)
        self.assertEqual(attrs.get_attr("a"), 42)
        self.assertEqual(attrs.has_attr("b"), True)
        self.assertEqual(attrs.get_attr("b"), "test")
        self.assertEqual(attrs.has_attr("c"), True)
        self.assertEqual(attrs.get_attr("c"), [True, False, True])
        self.assertEqual(attrs.dict().keys(), {"a", "b", "c", "mem", "impl"})
        self.assertEqual(attrs.has_attr("d"), False)
        self.assertEqual(attrs.has_attr("mem.a"), True)
        self.assertEqual(attrs.get_attr("mem.a"), 1)
        self.assertEqual(attrs.has_attr("mem.data.b"), True)
        self.assertEqual(attrs.get_attr("mem.data.b"), 1.0)
        self.assertEqual(attrs.get_attr("mem").get_attr("data").get_attr("b"), 1.0)
        self.assertEqual(attrs.has_attr("impl.c"), True)
        self.assertEqual(attrs.get_attr("impl.c"), "test")

        # Add Python attributes
        attrs.add_attr("d", 18.56)
        self.assertEqual(attrs.get_attr("d"), 18.56)
        self.assertEqual(attrs.has_attr("d"), True)
        self.assertEqual(attrs.dict().keys(), {"a", "b", "c", "d", "mem", "impl"})
        self.assertEqual(attrs.has_attr("e"), False)
        attrs.add_attr("mem.data.c", 19.36)
        self.assertEqual(attrs.get_attr("mem.data.c"), 19.36)
        self.assertEqual(attrs.has_attr("mem.data.c"), True)
        self.assertEqual(attrs.dict().keys(), {"a", "b", "c", "d", "mem", "impl"})

        # Check that added Python attribute is accessible in C++
        # Return the value of an attribute named "d" of type float64 (double in C++)
        self.assertEqual(aidge_core.test_DynamicAttributes_binding_check(attrs), 18.56)
        attrs.d = 23.89
        self.assertEqual(aidge_core.test_DynamicAttributes_binding_check(attrs), 23.89)

        op = aidge_core.GenericOperatorOp("any_type", 1,0,1)
        with self.assertRaises(IndexError):
            op.attr.something

        op.attr.something = aidge_core.DynamicAttributes()
        try:
            self.assertEqual(str(op.attr), "AttrDict({'something': AttrDict({})})")
        except Exception:
            self.fail("op.attr.something raised Exception unexpectedly!")

        op.attr.something.arg1 = 4
        self.assertEqual(op.attr.something.arg1, 4)

        # auto create the namespace another_thing (not enabled)
        #op.attr.another_thing.arg = 44
        #self.assertEqual(op.attr.another_thing.arg, 44)

    def test_forward_dims(self):
        in_dims=[25, 25]
        input = aidge_core.Producer(in_dims, name="In")
        genOp = aidge_core.GenericOperator("genOp", 1, 0, 1, name="genOp")
        _ = aidge_core.sequential([input, genOp])
        self.assertListEqual(genOp.get_operator().get_output(0).dims(), [])
        genOp.get_operator().set_forward_dims(lambda x:x)
        genOp.get_operator().forward_dims()
        self.assertListEqual(genOp.get_operator().get_output(0).dims(), in_dims)

    def test_set_impl(self):

        class PythonCustomImpl(aidge_core.OperatorImpl):
            """Dummy implementation to test that C++ call python code
            """
            def __init__(self, op: aidge_core.Operator):
                aidge_core.OperatorImpl.__init__(self, op, 'test_impl') # Recquired to avoid type error !
                self.idx = 0

            def forward(self):
                """Increment idx attribute on forward.
                """
                self.idx += 1

        generic_node = aidge_core.GenericOperator("Relu", 1, 0, 1, name="myReLu")
        generic_op = generic_node.get_operator()
        customImpl = PythonCustomImpl(generic_op)

        #generic_op.forward() # Throw an error, no implementation set
        generic_op.set_impl(customImpl)
        generic_op.forward() # Increment idx
        self.assertEqual(customImpl.idx, 1)

    def test_magic_meth(self):
        myVar = 2
        myBool = True
        # Test dynamic attribute set
        gop = aidge_core.GenericOperator("test", 1, 0, 1, "FictiveName", my_var=myVar).get_operator()
        gop.attr.my_bool = myBool
        # Test variable set by kwargs
        self.assertEqual(gop.attr.my_var, myVar)
        # Test set attr
        self.assertEqual(gop.attr.my_bool, myBool)

        # Test static attribute set !
        prod = aidge_core.Producer([1]).get_operator()
        self.assertEqual(prod.attr.constant, False)
        prod.attr.constant = True # By default Constant is False
        self.assertEqual(prod.attr.constant, True)



if __name__ == '__main__':
    unittest.main()
