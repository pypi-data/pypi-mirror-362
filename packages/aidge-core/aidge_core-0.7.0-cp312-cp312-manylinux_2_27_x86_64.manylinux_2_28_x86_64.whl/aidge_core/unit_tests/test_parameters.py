"""
Copyright (c) 2023 CEA-List

This program and the accompanying materials are made available under the
terms of the Eclipse Public License 2.0 which is available at
http://www.eclipse.org/legal/epl-2.0.

SPDX-License-Identifier: EPL-2.0
"""

import unittest
import aidge_core

class test_attributes(unittest.TestCase):
    """Very basic test to make sure the python APi is not broken.
    Can be remove in later stage of the developpement.
    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_conv(self):
        # TODO : test StrideDims & DilationDims when supported in ctor
        in_channels = 4
        out_channels = 8
        k_dims = [2, 2]
        conv_op = aidge_core.Conv2D(in_channels , out_channels, k_dims).get_operator()
        self.assertEqual(conv_op.in_channels(), in_channels)
        self.assertEqual(conv_op.out_channels(), out_channels)
        self.assertEqual(conv_op.attr.get_attr("kernel_dims"), k_dims)

    def test_fc(self):
        in_channels = 4
        out_channels = 8
        fc_op = aidge_core.FC(in_channels, out_channels).get_operator()
        self.assertEqual(fc_op.out_channels(), out_channels)

    def test_producer_1D(self):
        dims = [5]
        producer_op = aidge_core.Producer(dims).get_operator()
        self.assertEqual(producer_op.dims(), dims)

    def test_producer_2D(self):
        dims = [10,5]
        producer_op = aidge_core.Producer(dims).get_operator()
        self.assertEqual(producer_op.dims(), dims)

    def test_producer_3D(self):
        dims = [1,10,5]
        producer_op = aidge_core.Producer(dims).get_operator()
        self.assertEqual(producer_op.dims(), dims)

    def test_producer_4D(self):
        dims = [12,1,10,5]
        producer_op = aidge_core.Producer(dims).get_operator()
        self.assertEqual(producer_op.dims(), dims)

    def test_producer_5D(self):
        dims = [2,12,1,10,5]
        producer_op = aidge_core.Producer(dims).get_operator()
        self.assertEqual(producer_op.dims(), dims)

    def test_leaky_relu(self):
        negative_slope = 0.25
        leakyrelu_op = aidge_core.LeakyReLU(negative_slope).get_operator()
        self.assertEqual(leakyrelu_op.attr.get_attr("negative_slope"), negative_slope)

if __name__ == '__main__':
    unittest.main()
