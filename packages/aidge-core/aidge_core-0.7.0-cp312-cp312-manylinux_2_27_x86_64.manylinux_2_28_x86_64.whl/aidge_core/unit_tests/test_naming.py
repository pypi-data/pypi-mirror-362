"""
Copyright (c) 2023 CEA-List

This program and the accompanying materials are made available under the
terms of the Eclipse Public License 2.0 which is available at
http://www.eclipse.org/legal/epl-2.0.

SPDX-License-Identifier: EPL-2.0
"""

import unittest
import aidge_core
import inspect
import re

def is_snake_case(s: str) -> bool:
    return bool(re.fullmatch(r'^[a-z]+(_[a-z]+)*$', s))

class test_naming(unittest.TestCase):
    """Test tensor binding
    """
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_attributes_name(self):

        for obj in inspect.getmembers(aidge_core):
            if (inspect.isclass(obj[1]) and issubclass(obj[1], aidge_core.Operator) and obj[1] is not aidge_core.Operator) and hasattr(obj[1], "attributes_name"):
                print(obj[0])
                print(obj[1].attributes_name())
                for attr_name in obj[1].attributes_name():
                    self.assertTrue(is_snake_case(attr_name), f"Operator {obj[0]} has an attribute {attr_name} that is not in snake_case.")



if __name__ == '__main__':
    unittest.main()
