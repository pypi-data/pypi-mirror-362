"""
Copyright (c) 2023 CEA-List

This program and the accompanying materials are made available under the
terms of the Eclipse Public License 2.0 which is available at
http://www.eclipse.org/legal/epl-2.0.

SPDX-License-Identifier: EPL-2.0
"""

import unittest
import aidge_core

class test_recipes(unittest.TestCase):
    """
    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_remove_dropout(self):
        graph_view = aidge_core.sequential([
            aidge_core.GenericOperator("Conv", 1, 0, 1, "Conv0"),
            aidge_core.GenericOperator("Dropout", 1, 0, 1, name="Dropout0")
        ])
        old_nodes = graph_view.get_nodes()
        aidge_core.remove_dropout(graph_view)
        self.assertTrue(len(graph_view.get_nodes()) == len(old_nodes) - 1)
        self.assertTrue("Dropout0" not in [i.name for i in graph_view.get_nodes()])

        self.assertTrue(all([i in old_nodes for i in graph_view.get_nodes()]))

    def test_remove_flatten(self):
        graph_view = aidge_core.sequential([
            aidge_core.GenericOperator("Flatten", 1, 0, 1, name="Flatten0"),
            aidge_core.FC(10, 50, name='0')
        ])
        old_nodes = graph_view.get_nodes()
        aidge_core.remove_flatten(graph_view)
        self.assertTrue(len(graph_view.get_nodes()) == len(old_nodes) - 1)
        self.assertTrue("Flatten0" not in [i.name for i in graph_view.get_nodes()])

        self.assertTrue(all([i in old_nodes for i in graph_view.get_nodes()]))

    def test_fuse_matmul_add(self):
        matmul0 = aidge_core.MatMul(name="MatMul0")
        add0 = aidge_core.Add(name="Add0")
        matmul1 = aidge_core.MatMul(name="MatMul1")
        add1 = aidge_core.Add(name="Add1")
        w0 = aidge_core.Producer([1, 1], name="W0")
        w0.add_child(matmul0, 0, 0)
        b0 = aidge_core.Producer([1], name="B0")
        b0.add_child(add0, 0, 1)
        w1 = aidge_core.Producer([1, 1], name="W1")
        w1.add_child(matmul1, 0, 0)
        b1 = aidge_core.Producer([1], name="B1")
        b1.add_child(add1, 0, 1)

        graph_view = aidge_core.sequential([matmul0, add0, matmul1, add1])
        graph_view.add(w0)
        graph_view.add(b0)
        graph_view.add(w1)
        graph_view.add(b1)

        old_nodes = graph_view.get_nodes()
        aidge_core.matmul_to_fc(graph_view)

        self.assertTrue(len(graph_view.get_nodes()) == len(old_nodes) - 2)
        self.assertTrue("MatMul0" not in [i.name() for i in graph_view.get_nodes()])
        self.assertTrue("Add0" not in [i.name() for i in graph_view.get_nodes()])
        self.assertTrue("MatMul1" not in [i.name() for i in graph_view.get_nodes()])
        self.assertTrue("Add1" not in [i.name() for i in graph_view.get_nodes()])

        self.assertTrue("W0" in [i.name() for i in graph_view.get_nodes()])
        self.assertTrue("B0" in [i.name() for i in graph_view.get_nodes()])
        self.assertTrue("W1" in [i.name() for i in graph_view.get_nodes()])
        self.assertTrue("B1" in [i.name() for i in graph_view.get_nodes()])
        # TODO : Vérifier que FC bien crée

if __name__ == '__main__':
    unittest.main()



