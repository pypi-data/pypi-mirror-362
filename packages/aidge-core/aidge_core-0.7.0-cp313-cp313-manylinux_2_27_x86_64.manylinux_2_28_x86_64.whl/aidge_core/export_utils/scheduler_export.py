import aidge_core
import os
import shutil
from pathlib import Path
from aidge_core.export_utils import ExportLib, generate_file, copy_file, copy_folder
from typing import List, Dict, Tuple


def scheduler_export(scheduler, export_folder_path: str, export_lib: ExportLib = None, memory_manager=None, memory_manager_args=None, dev_mode=False) -> None:
    """Exports an aidge_core.Scheduler to C++ code.

    This function generates files for a given computation graph, including forward-pass functions,
    configuration headers, and the main API entry point for the exported model.
    It requires a memory manager to allocate resources, and optionally an `ExportLib` instance to handle backend configurations for node operators.


    1. **Export Preparation**:
        - Initializes export and DNN folders, checking that required memory management functions are defined.
        - Retrieves peak memory usage and memory details for each node using the `memory_manager`.

    2. **Configuration Generation**:
        - Iterates over nodes scheduled by `scheduler`, configuring backends if `export_lib` is specified.
        - Exports configuration headers and forward-pass actions for each node by invoking `op.export()` and `op.forward()`, appending these to `list_configs` and `list_actions`, respectively.
        - Collects information on input and output nodes, including their names, data types, and sizes.

    3. **Code Generation**:
        - Defines the forward-pass function, `model_forward`, with inputs and outputs based on node attributes.
        - Generates the following files:

            - **forward.cpp**: Implements the model forward pass using templates, applying configurations and actions for each node.

            - **forward.hpp**: Exports the forward API, defining inputs and outputs.

            - **main.cpp**: Main entry file, serving as the model's forward-pass interface.

    4. **Static File Export (Optional)**:
        - If `export_lib` is specified, static files are copied to the export folder based on `export_lib` specifications.


    :param scheduler: Scheduler instance managing the computation graph. Uses `graph_view` and `get_sequential_static_scheduling` methods to retrieve the computation graph layout and ordered nodes.
    :type scheduler: aidge_core.Scheduler
    :param export_folder_path: Path to the folder where the generated export files will be saved. Creates this folder, along with subdirectories for model and source files.
    :type export_folder_path: str
    :param export_lib: Library providing the backend implementation for node operators. Defaults to None. If provided, each node's backend is set to the library's name.
    :type export_lib: ExportLib, optional
    :param memory_manager: Required function for managing memory allocation. It should take `scheduler` and optional `memory_manager_args` as parameters, returning `peak_mem` (peak memory usage) and `mem_info` (memory details for each node).
    :type memory_manager: callable
    :param memory_manager_args: Additional arguments passed to `memory_manager`. Defaults to an empty dictionary.
    :type memory_manager_args: dict, optional
    :param dev_mode: Wether or not the developer mode is enabled. If enabled, the export files
                     will be symlinks from the aidge export module. Therefore, modifying
                     a file within the export will change the module as well.
                     The dev_mode flag is also passed to the forward jinja templates to allow export
                     customization (ie. Adding a debug mode for instance).
    :type dev_mode: bool, optional
    """
    export_folder = Path().absolute() / export_folder_path

    os.makedirs(str(export_folder), exist_ok=True)

    dnn_folder = export_folder / "dnn"
    os.makedirs(str(dnn_folder), exist_ok=True)

    if memory_manager_args is None:
        memory_manager_args = {}

    if memory_manager is None:
        raise ValueError("A memory manager is required (no default value yet).")
    peak_mem, mem_info = memory_manager(
        scheduler, **memory_manager_args)

    # List of function call for forward.cpp
    list_actions: List[str] = []
    # List of headers for forward.cpp
    list_configs: List[str] = []
    # List of headers for forward.hpp
    list_libraries: List[str] = []

    # List of aidge_core.Node ordered by scheduler
    list_forward_nodes: List[aidge_core.Node] = scheduler.get_sequential_static_scheduling()
    export_nodes: Dict[aidge_core.Node, aidge_core.ExportNode] = {}

    # If exportLib define use it
    # else parse component in platform
    # if export_lib is None:
    #     raise ValueError("Export need an ExportLib.")
    for node in list_forward_nodes:
        if export_lib is not None:
            aidge_core.Log.debug(f"Setting backend {export_lib._name} to {node.name()}[{node.type()}].")
            node.get_operator().set_backend(export_lib._name)

        op_impl = node.get_operator().get_impl()
        if op_impl is None:
            raise RuntimeError(f"Operator {node.name()}[{node.type()}] doesn't have an implementation.")
        if not isinstance(op_impl, ExportLib):
            raise RuntimeError(f"Operator {node.name()}[{node.type()}] doesn't have an exportable backend ({op_impl}): {op_impl.backend()}.")

        # Get operator current specs
        required_specs = op_impl.get_required_spec()
        # Get specs of the implementation that match current specs
        specs = op_impl.get_best_match(required_specs)
        # Retrieve said implementation
        export_node = op_impl.get_export_node(specs)

        if export_node is None:
            raise RuntimeError(f"Could not find export node for {node.name()}[{node.type()}] with specs {required_specs}.\n\nAvailable specs are: {op_impl.get_available_impl_specs()}")
        # Instanciate ExportNode
        op = export_node(node, mem_info[node])
        export_nodes[node] = op

        # For configuration files
        list_configs += op.export(dnn_folder)
        # For forward file
        list_actions += op.forward()

    gv_inputs: list[tuple[aidge_core.Node, int]] = scheduler.graph_view().get_ordered_inputs()
    gv_outputs: list[tuple[aidge_core.Node, int]] = scheduler.graph_view().get_ordered_outputs()

    inputs_name: List[str] = []
    inputs_dtype: List[str] = []
    outputs_name: List[str] = []
    outputs_dtype: List[str] = []

    cstdint_types = [
        aidge_core.dtype.int64,
        aidge_core.dtype.int32,
        aidge_core.dtype.int16,
        aidge_core.dtype.int8,
        aidge_core.dtype.uint64,
        aidge_core.dtype.uint32,
        aidge_core.dtype.uint16,
        aidge_core.dtype.uint8
    ]

    for in_node, in_idx in gv_inputs:
        if in_node.get_operator().get_input(in_idx) is not None:
            op = export_nodes[in_node]
            inputs_name.append(op.attributes["in_name"][in_idx])
            inputs_dtype.append(op.attributes["in_cdtype"][in_idx])
            if op.attributes["in_dtype"][in_idx] in cstdint_types:
                list_configs += ["<stdint.h>"]
                list_libraries += ["<stdint.h>"]

    for out_node, out_idx in gv_outputs:
        op = export_nodes[out_node]
        outputs_name.append(op.attributes["out_name"][out_idx])
        outputs_dtype.append(op.attributes["out_cdtype"][out_idx])
        if op.attributes["out_dtype"][out_idx] in cstdint_types:
                list_configs += ["<stdint.h>"]
                list_libraries += ["<stdint.h>"]

    func_name = "model_forward"
    ROOT = Path(__file__).resolve().parents[0]

    forward_template = str(ROOT / "templates" / "forward.jinja")
    if export_lib.forward_template != None:
        forward_template = export_lib.forward_template

    list_node_names = []
    for node in list_forward_nodes:
        if node.type() != "Producer":
            list_node_names.append(node.name())

    # Convert Path to str
    header_set = set([str(header) for header in list_configs])

    generate_file(
        str(dnn_folder / "src" / "forward.cpp"),
        forward_template,
        func_name=func_name,
        headers=header_set,
        actions=list_actions,
        mem_section=export_lib.mem_section,
        peak_mem=peak_mem,
        inputs_name=inputs_name,
        inputs_dtype=inputs_dtype,
        outputs_name=outputs_name,
        outputs_dtype=outputs_dtype,
        dev_mode=dev_mode,
        list_node_names=list_node_names
    )

    forward_header_template = str(ROOT / "templates" / "forward_header.jinja")
    if export_lib.forward_header_template is not None:
        forward_header_template = export_lib.forward_header_template

    # Generate dnn API
    generate_file(
        str(dnn_folder / "include" / "forward.hpp"),
        forward_header_template,
        libraries=set(list_libraries),
        func_name=func_name,
        inputs_name=inputs_name,
        inputs_dtype=inputs_dtype,
        outputs_name=outputs_name,
        outputs_dtype=outputs_dtype,
        dev_mode=dev_mode
    )

    if export_lib is not None:
        # Copy all static files in the export
        for source, destination in export_lib.static_files.items():
            copy_file(source, str(export_folder / destination), dev_mode)

        # Copy all static folders in the export
        for source, destination in export_lib.static_folders.items():
            copy_folder(source, str(export_folder / destination), dev_mode)
