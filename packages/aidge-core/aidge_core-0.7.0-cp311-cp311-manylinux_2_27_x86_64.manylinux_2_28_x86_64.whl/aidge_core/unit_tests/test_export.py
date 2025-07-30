"""
Copyright (c) 2023 CEA-List

This program and the accompanying materials are made available under the
terms of the Eclipse Public License 2.0 which is available at
http://www.eclipse.org/legal/epl-2.0.

SPDX-License-Identifier: EPL-2.0
"""

import unittest
import os
import pathlib
import shutil
import subprocess
import sys


import aidge_core
from aidge_core.utils import run_command
from aidge_core.testing.utils import tree_update_from_cache, tree_move, tree_remove

def initFiller(model):
    # Initialize parameters (weights and biases)
    for node in model.get_nodes():
        if node.type() == "Producer":
            prod_op = node.get_operator()
            value = prod_op.get_output(0)
            value.set_backend("cpu")
            tuple_out = node.output(0)[0]
            # Force seed before filler for reproducibility
            aidge_core.random.Generator.set_seed(0)
            # No conv in current network
            if tuple_out[0].type() == "Conv2D" and tuple_out[1] == 1:
                # Conv weight
                aidge_core.xavier_uniform_filler(value)
            elif tuple_out[0].type() == "Conv2D" and tuple_out[1] == 2:
                # Conv bias
                aidge_core.constant_filler(value, 0.01)
            elif tuple_out[0].type() == "FC" and tuple_out[1] == 1:
                # FC weight
                aidge_core.normal_filler(value)
            elif tuple_out[0].type() == "FC" and tuple_out[1] == 2:
                # FC bias
                aidge_core.constant_filler(value, 0.01)
            else:
                pass


class test_export(unittest.TestCase):
    """Test aidge export"""

    def setUp(self):
        self.EXPORT_PATH: pathlib.Path = pathlib.Path("dummy_export")
        self.BUILD_DIR: pathlib.Path = self.EXPORT_PATH / "build"
        self.INSTALL_DIR: pathlib.Path = (self.EXPORT_PATH / "install").absolute()
        self.TMP_BUILD_DIR: pathlib.Path = (
            self.EXPORT_PATH.parent /
            f"__tmp_{self.EXPORT_PATH.name}_build"
        )

    def tearDown(self):
        pass

    def test_generate_export(self):
        # Create model

        model = aidge_core.sequential(
            [
                aidge_core.FC(
                    in_channels=32 * 32 * 3, out_channels=64, name="InputNode"
                ),
                aidge_core.ReLU(name="Relu0"),
                aidge_core.FC(in_channels=64, out_channels=32, name="FC1"),
                aidge_core.ReLU(name="Relu1"),
                aidge_core.FC(in_channels=32, out_channels=16, name="FC2"),
                aidge_core.ReLU(name="Relu2"),
                aidge_core.FC(in_channels=16, out_channels=10, name="OutputNode"),
            ]
        )

        initFiller(model)
        model.forward_dims([[1, 32*32*3]])

        # Preserve previously generated build if present
        tree_move(self.BUILD_DIR, self.TMP_BUILD_DIR, ignore_missing=True, exist_ok=True)
        # Clean install dir
        tree_remove(self.INSTALL_DIR, ignore_missing=True)

        # Export model
        aidge_core.serialize_to_cpp(self.EXPORT_PATH, model)
        self.assertTrue(self.EXPORT_PATH.is_dir(), "Export folder has not been generated")
        # Add other source files
        shutil.copyfile(pathlib.Path(__file__).parent / "static/main.cpp", self.EXPORT_PATH / "main.cpp")

        # Use cache if any, put cache inside export dir
        # such that cleaning export dir also cleans the cache
        tree_update_from_cache(
            self.EXPORT_PATH,
            cache_path=self.EXPORT_PATH / "__cache_export"
        )

        # Move back preserved build dir if any and ensure build dir exists
        tree_move(self.TMP_BUILD_DIR, self.BUILD_DIR, ignore_missing=True)
        self.BUILD_DIR.mkdir(exist_ok=True)

        # Test compilation of export
        search_path = (
            os.path.join(sys.prefix, "lib", "libAidge")
            if "AIDGE_INSTALL" not in os.environ
            else os.environ["AIDGE_INSTALL"]
        )

        ##########################
        # CMAKE EXPORT
        try:
            for std_line in run_command(
                [
                    "cmake",
                    str(self.EXPORT_PATH.absolute()),
                    "-DPYBIND=ON",
                    f"-DCMAKE_PREFIX_PATH={search_path}", # search dependencies
                    f"-DCMAKE_INSTALL_PREFIX:PATH={self.INSTALL_DIR}", # local install
                ],
                cwd=str(self.BUILD_DIR),
            ):
                print(std_line, end="")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}\nFailed to configure export.")
            raise SystemExit(1)

        ##########################
        # BUILD EXPORT
        try:
            for std_line in run_command(
                ["cmake", "--build", "."],
                cwd=str(self.BUILD_DIR),
            ):
                print(std_line, end="")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}\nFailed to build export.")
            raise SystemExit(1)

        ##########################
        # INSTALL EXPORT
        try:
            for std_line in run_command(
                ["cmake", "--install", "."],
                cwd=str(self.BUILD_DIR),
            ):
                print(std_line, end="")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}\nFailed to install export.")
            raise SystemExit(1)


if __name__ == "__main__":
    unittest.main()
