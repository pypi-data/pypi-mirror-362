import aidge_core
from pathlib import Path
from aidge_core.export_utils import generate_file, data_conversion, generate_input_file

def generate_main_cpp(export_folder: str, graph_view: aidge_core.GraphView, inputs_tensor=None, labels=None) -> None:
    """
    Generate a C++ file to manage the forward pass of a model using the given graph structure.

    This function extracts details from the :py:class:`aidge_core.graph_view` object, including input and output node names, data types,
    and tensor sizes. It uses this data to populate a C++ file template (`main.jinja`), creating a file (`main.cpp`)
    that call the `model_forward` function, which handles data flow and processing for the exported model.

    This function also generate files containing input tensor if they have been set.

    :param export_folder: Path to the folder where the generated C++ file (`main.cpp`) will be saved.
    :type export_folder: str
    :param graph_view: An instance of :py:class:`aidge_core.graph_view`, providing access to nodes and
                       ordered input/output data within the computational graph.
    :type graph_view: aidge_core.graph_view
    :param inputs_tensor: argument to provide external tensor to use in the main function
                          By default, the input of the given graph will be exported.
    :type inputs_tensor: aidge_core.Tensor
    :param labels: Argument to provide labels tensor to generate and use in the main function.
    :type labels: aidge_core.Tensor
    :raises RuntimeError: If there is an inconsistency in the output arguments (names, data types, sizes),
                          indicating an internal bug in the graph representation.
    """
    outputs_name: list[str] = []
    outputs_dtype: list[str] = []
    outputs_size: list[int] = []
    inputs_name: list[str] = []
    gv_inputs: list[tuple[aidge_core.Node, int]] = graph_view.get_ordered_inputs()
    gv_outputs: list[tuple[aidge_core.Node, int]] = graph_view.get_ordered_outputs()

    # Generate input file(s)
    for in_node, in_idx in gv_inputs:
        in_node_input, in_node_input_idx = in_node.input(in_idx)
        in_name = f"{in_node.name()}_input_{in_idx}" if in_node_input is None else f"{in_node_input.name()}_output_{in_node_input_idx}"

        if inputs_tensor is None:
            inputs_tensor = in_node.get_operator().get_input(in_idx)

        # Ignore optional inputs
        if inputs_tensor is None or inputs_tensor.undefined():
            if (int(in_node.get_operator().input_category(in_idx)) & int(aidge_core.InputCategory.Optional)):
                aidge_core.Log.notice(f"Ignoring missing optional input {in_name}.")
            else:
                inputs_name.append(in_name)
                if inputs_tensor is not None:
                    aidge_core.Log.notice("No support for inputs_tensor argument yet.")
                aidge_core.Log.warn(f"No input tensor set for {in_name}, main generated will not be functionnal after code generation.")
        else:
            inputs_name.append(in_name)
            generate_input_file(
                export_folder=str(Path(export_folder) / "data"),
                array_name=in_name,
                tensor=inputs_tensor)

    # Generate labels file
    if labels is not None:
        generate_input_file(
            export_folder=str(Path(export_folder) / "data"),
            array_name="labels",
            tensor=labels
        )

    for out_node, out_id in gv_outputs:
        outputs_name.append(f"{out_node.name()}_output_{out_id}")
        out_tensor = out_node.get_operator().get_output(out_id)
        outputs_dtype.append(data_conversion.aidge2c(out_tensor.dtype()))
        outputs_size.append(out_tensor.size())

    if len(outputs_name) != len(outputs_dtype) or len(outputs_name) != len(outputs_size):
            raise RuntimeError("FATAL: Output args list does not have the same length this is an internal bug.")

    ROOT = Path(__file__).resolve().parents[0]
    generate_file(
        str(Path(export_folder) / "main.cpp"),
        str(ROOT / "templates" / "main.jinja"),
        func_name="model_forward",
        inputs_name=inputs_name,
        outputs_name=outputs_name,
        outputs_dtype=outputs_dtype,
        outputs_size=outputs_size,
        labels=(labels is not None)
    )


def generate_main_compare_cpp(export_folder: str, graph_view: aidge_core.GraphView, inputs_tensor=None) -> None:
    """
    Generate a C++ file to manage the forward pass and compare the output of a model.

    This function extracts details from the :py:class:`aidge_core.graph_view` object, including input and output node names, data types,
    and tensor sizes. It uses this data to populate a C++ file template (`main.jinja`), creating a file (`main.cpp`)
    that call the `model_forward` function, which handles data flow and processing for the exported model.

    This function also generate files containing input tensor if they have been set.

    :param export_folder: Path to the folder where the generated C++ file (`main.cpp`) will be saved.
    :type export_folder: str
    :param graph_view: An instance of :py:class:`aidge_core.graph_view`, providing access to nodes and
                       ordered input/output data within the computational graph.
    :type graph_view: aidge_core.graph_view
    :param inputs_tensor: **For future**argument to provide tensor to use in the main function, not implemented yet!
    :type inputs_tensor: None
    :raises RuntimeError: If there is an inconsistency in the output arguments (names, data types, sizes),
                          indicating an internal bug in the graph representation.
    """
    outputs_name: list[str] = []
    outputs_dtype: list[str] = []
    outputs_size: list[int] = []
    inputs_name: list[str] = []
    gv_inputs: list[tuple[aidge_core.Node, int]] = graph_view.get_ordered_inputs()
    gv_outputs: list[tuple[aidge_core.Node, int]] = graph_view.get_ordered_outputs()

    for in_node, in_idx in gv_inputs:
        in_node_input, in_node_input_idx = in_node.input(in_idx)
        in_name = f"{in_node.name()}_input_{in_idx}" if in_node_input is None else f"{in_node_input.name()}_output_{in_node_input_idx}"
        input_tensor = in_node.get_operator().get_input(in_idx)
        if input_tensor is None or input_tensor.undefined():
            if (int(in_node.get_operator().input_category(in_idx)) & int(aidge_core.InputCategory.Optional)):
                aidge_core.Log.notice(f"Ignoring missing optional input {in_name}.")
            else:
                inputs_name.append(in_name)
                if inputs_tensor is not None:
                    aidge_core.Log.notice("No support for inputs_tensor argument yet.")
                aidge_core.Log.warn(f"No input tensor set for {in_name}, main generated will not be functionnal after code generation.")
        else:
            inputs_name.append(in_name)
            generate_input_file(str(Path(export_folder) / "data"), array_name=in_name, tensor=input_tensor)

    for out_node, out_id in gv_outputs:
        out_name = f"{out_node.name()}_output_{out_id}"
        outputs_name.append(out_name)
        out_tensor = out_node.get_operator().get_output(out_id)
        outputs_dtype.append(data_conversion.aidge2c(out_tensor.dtype()))
        outputs_size.append(out_tensor.size())
        if out_tensor is None or out_tensor.undefined():
            aidge_core.Log.notice(f"No input tensor set for {out_name}, main generated will not be functionnal after code generation.")
        else:
            generate_input_file(str(Path(export_folder) / "data"), array_name=out_name+"_expected", tensor=out_tensor)

    if len(outputs_name) != len(outputs_dtype) or len(outputs_name) != len(outputs_size):
            raise RuntimeError("FATAL: Output args list does not have the same length this is an internal bug.")

    ROOT = Path(__file__).resolve().parents[0]
    generate_file(
        str(Path(export_folder) / "main.cpp"),
        str(ROOT / "templates" / "main_compare.jinja"),
        func_name="model_forward",
        inputs_name=inputs_name,
        outputs_name=outputs_name,
        outputs_dtype=outputs_dtype,
        outputs_size=outputs_size
    )

def generate_main_inference_time_cpp(export_folder: str, graph_view: aidge_core.GraphView, nb_iterations, nb_warmup, inputs_tensor=None) -> None:
    """
    Generate a C++ file to manage the forward pass of a model using the given graph structure.

    This function extracts details from the :py:class:`aidge_core.graph_view` object, including input and output node names, data types,
    and tensor sizes. It uses this data to populate a C++ file template (`main.jinja`), creating a file (`main.cpp`)
    that call the `model_forward` function, which handles data flow and processing for the exported model.

    This function also generate files containing input tensor if they have been set.

    :param export_folder: Path to the folder where the generated C++ file (`main.cpp`) will be saved.
    :type export_folder: str
    :param graph_view: An instance of :py:class:`aidge_core.graph_view`, providing access to nodes and
                       ordered input/output data within the computational graph.
    :type graph_view: aidge_core.graph_view
    :param inputs_tensor: **For future** argument to provide tensor to use in the main function, not implemented yet!
    :type inputs_tensor: None
    :raises RuntimeError: If there is an inconsistency in the output arguments (names, data types, sizes),
                          indicating an internal bug in the graph representation.
    """
    outputs_name: list[str] = []
    outputs_dtype: list[str] = []
    outputs_size: list[int] = []
    inputs_name: list[str] = []
    gv_inputs: list[tuple[aidge_core.Node, int]] = graph_view.get_ordered_inputs()
    gv_outputs: list[tuple[aidge_core.Node, int]] = graph_view.get_ordered_outputs()
    print("bonjour")
    for in_node, in_idx in gv_inputs:
        in_node_input, in_node_input_idx = in_node.input(in_idx)
        in_name = f"{in_node.name()}_input_{in_idx}" if in_node_input is None else f"{in_node_input.name()}_output_{in_node_input_idx}"
        input_tensor = in_node.get_operator().get_input(in_idx)
        if input_tensor is None or input_tensor.undefined():
            if (int(in_node.get_operator().input_category(in_idx)) & int(aidge_core.InputCategory.Optional)):
                aidge_core.Log.notice(f"Ignoring missing optional input {in_name}.")
            else:
                inputs_name.append(in_name)
                if inputs_tensor is not None:
                    aidge_core.Log.notice("No support for inputs_tensor argument yet.")
                aidge_core.Log.warn(f"No input tensor set for {in_name}, main generated will not be functionnal after code generation.")
        else:
            inputs_name.append(in_name)
            aidge_core.export_utils.generate_input_file(str(Path(export_folder) / "data"), array_name=in_name, tensor=input_tensor)

    for out_node, out_id in gv_outputs:
        outputs_name.append(f"{out_node.name()}_output_{out_id}")
        out_tensor = out_node.get_operator().get_output(out_id)
        outputs_dtype.append(data_conversion.aidge2c(out_tensor.dtype()))
        outputs_size.append(out_tensor.size())

    if len(outputs_name) != len(outputs_dtype) or len(outputs_name) != len(outputs_size):
            raise RuntimeError("FATAL: Output args list does not have the same length this is an internal bug.")

    ROOT = Path(__file__).resolve().parents[0]
    generate_file(
        str(Path(export_folder) / "main.cpp"),
        str(ROOT / "templates" / "main_benchmark_inference_time.jinja"),
        func_name="model_forward",
        inputs_name=inputs_name,
        outputs_name=outputs_name,
        outputs_dtype=outputs_dtype,
        outputs_size=outputs_size,
        nb_iterations=nb_iterations,
        nb_warmup=nb_warmup
    )

def generate_main_display_output_cpp(export_folder: str, graph_view: aidge_core.GraphView, inputs_tensor=None) -> None:
    """
    Generate a C++ file to manage the forward pass of a model using the given graph structure.

    This function extracts details from the :py:class:`aidge_core.graph_view` object, including input and output node names, data types,
    and tensor sizes. It uses this data to populate a C++ file template (`main.jinja`), creating a file (`main.cpp`)
    that call the `model_forward` function, which handles data flow and processing for the exported model.

    This function also generate files containing input tensor if they have been set.

    :param export_folder: Path to the folder where the generated C++ file (`main.cpp`) will be saved.
    :type export_folder: str
    :param graph_view: An instance of :py:class:`aidge_core.graph_view`, providing access to nodes and
                       ordered input/output data within the computational graph.
    :type graph_view: aidge_core.graph_view
    :param inputs_tensor: **For future** argument to provide tensor to use in the main function, not implemented yet!
    :type inputs_tensor: None
    :raises RuntimeError: If there is an inconsistency in the output arguments (names, data types, sizes),
                          indicating an internal bug in the graph representation.
    """
    outputs_name: list[str] = []
    outputs_dtype: list[str] = []
    outputs_size: list[int] = []
    inputs_name: list[str] = []
    gv_inputs: list[tuple[aidge_core.Node, int]] = graph_view.get_ordered_inputs()
    gv_outputs: list[tuple[aidge_core.Node, int]] = graph_view.get_ordered_outputs()

    for in_node, in_idx in gv_inputs:
        in_node_input, in_node_input_idx = in_node.input(in_idx)
        in_name = f"{in_node.name()}_input_{in_idx}" if in_node_input is None else f"{in_node_input.name()}_output_{in_node_input_idx}"
        input_tensor = in_node.get_operator().get_input(in_idx)
        if input_tensor is None or input_tensor.undefined():
            if (int(in_node.get_operator().input_category(in_idx)) & int(aidge_core.InputCategory.Optional)):
                aidge_core.Log.notice(f"Ignoring missing optional input {in_name}.")
            else:
                inputs_name.append(in_name)
                if inputs_tensor is not None:
                    aidge_core.Log.notice("No support for inputs_tensor argument yet.")
                aidge_core.Log.warn(f"No input tensor set for {in_name}, main generated will not be functionnal after code generation.")
        else:
            inputs_name.append(in_name)
            aidge_core.export_utils.generate_input_file(str(Path(export_folder) / "data"), array_name=in_name, tensor=input_tensor)

    for out_node, out_id in gv_outputs:
        outputs_name.append(f"{out_node.name()}_output_{out_id}")
        out_tensor = out_node.get_operator().get_output(out_id)
        outputs_dtype.append(data_conversion.aidge2c(out_tensor.dtype()))
        outputs_size.append(out_tensor.size())

    if len(outputs_name) != len(outputs_dtype) or len(outputs_name) != len(outputs_size):
            raise RuntimeError("FATAL: Output args list does not have the same length this is an internal bug.")

    ROOT = Path(__file__).resolve().parents[0]
    generate_file(
        str(Path(export_folder) / "main.cpp"),
        str(ROOT / "templates" / "main_benchmark_display_output.jinja"),
        func_name="model_forward",
        inputs_name=inputs_name,
        outputs_name=outputs_name,
        outputs_dtype=outputs_dtype,
        outputs_size=outputs_size
    )