"""
Copyright (c) 2023 CEA-List

This program and the accompanying materials are made available under the
terms of the Eclipse Public License 2.0 which is available at
http://www.eclipse.org/legal/epl-2.0.

SPDX-License-Identifier: EPL-2.0
"""

import unittest
import aidge_core

class test_topological_order(unittest.TestCase):
    """Test python binding for nodes ordering"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_generic_loop_order_0(self):
        # Defines a Generic recurring loop header operator with
        # inputs: (init, back) and outputs (loop, last)
        # Note that one must specify the back edge as otherwise the
        # generated order may not schedule the loop header before the add
        loop0 = aidge_core.GenericOperator("Loop", 2, 0, 2, "Loop#0")
        loop0.get_operator().set_back_edges({1})
        assert not loop0.get_operator().is_back_edge(0)
        assert loop0.get_operator().is_back_edge(1)
        add0 = aidge_core.Add("add0")

        loop0.add_child(add0, 0, 1)
        add0.add_child(loop0, 0, 1)
        graph = aidge_core.GraphView()
        graph.add(loop0)
        graph.add(add0)

        nodes = graph.get_ordered_nodes()
        assert len(nodes) == 2
        assert nodes == [loop0, add0]

    def test_generic_loop_order_1(self):
        # Defines a Generic recurring loop header operator with
        # inputs: (back, init) and outputs (loop, last)
        # Note that one must specify the back edge as otherwise the
        # generated order may not schedule the loop header before the add
        loop0 = aidge_core.GenericOperator("Loop", 2, 0, 2, "Loop#0")
        loop0.get_operator().set_back_edges({0})
        assert not loop0.get_operator().is_back_edge(1)
        assert loop0.get_operator().is_back_edge(0)
        add0 = aidge_core.Add("add0")

        loop0.add_child(add0, 0, 1)
        add0.add_child(loop0, 0, 0)
        graph = aidge_core.GraphView()
        graph.add(loop0)
        graph.add(add0)

        nodes = graph.get_ordered_nodes()
        assert len(nodes) == 2
        assert nodes == [loop0, add0]


if __name__ == '__main__':
    unittest.main()
