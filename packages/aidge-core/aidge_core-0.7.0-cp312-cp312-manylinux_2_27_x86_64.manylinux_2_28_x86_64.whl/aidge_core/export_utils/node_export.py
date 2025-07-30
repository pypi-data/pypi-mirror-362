import aidge_core
from pathlib import Path

from aidge_core.export_utils import data_conversion, code_generation
from abc import ABC, abstractmethod
from typing import List, Dict



def get_chan(tensor: aidge_core.Tensor) -> int:
    dformat = tensor.dformat()
    dims = tensor.dims()
    if dformat == aidge_core.dformat.default or dformat == aidge_core.dformat.nchw:
        if len(dims) == 4:  # Suppose NCHW
            return dims[1]
        elif len(dims) == 3:  # Suppose NCW
            return dims[1]
        elif len(dims) == 2:  # Suppose NC
            return dims[1]
        elif len(dims) == 1:  # Suppose C (for bias)
            return dims[0]
    elif dformat == aidge_core.dformat.nhwc:
        if len(dims) == 4:  # NHWC
            return dims[3]
        elif len(dims) == 3:  # NWC
            return dims[2]
        elif len(dims) == 2:  # NC
            return 1
        elif len(dims) == 1:  # C for bias
            return 1
    elif dformat == aidge_core.dformat.chwn:
        assert len(dims) == 4
        return dims[0]
    elif dformat == aidge_core.dformat.ncdhw:
        assert len(dims) == 4
        return dims[1]
    elif dformat == aidge_core.dformat.ndhwc:
        assert len(dims) == 4
        return dims[4]
    elif dformat == aidge_core.dformat.cdhwn:
        assert len(dims) == 4
        return dims[0]
    elif dformat == aidge_core.dformat.chw:
        assert len(dims) == 3
        return dims[0]
    elif dformat == aidge_core.dformat.hwc:
        assert len(dims) == 3
        return dims[2]
    elif dformat == aidge_core.dformat.nwc:
        assert len(dims) == 3
        return dims[2]
    elif dformat == aidge_core.dformat.ncw:
        assert len(dims) == 3
        return dims[1]
    else:
        raise RuntimeError(f"Unknown dataformat: {dformat}")


def get_height(tensor: aidge_core.Tensor) -> int:
    dformat = tensor.dformat()
    dims = tensor.dims()
    if dformat == aidge_core.dformat.default or dformat == aidge_core.dformat.nchw:
        if len(dims) == 4:  # Suppose NCHW
            return dims[2]
        elif len(dims) == 3:  # Suppose NCW
            return 1
        elif len(dims) == 2:  # Suppose NC
            return 1
        elif len(dims) == 1:  # Suppose C for bias
            return 1
    elif dformat == aidge_core.dformat.nhwc:
        if len(dims) == 4:  # NHWC
            return dims[1]
        elif len(dims) == 3:  # NWC
            return 1
        elif len(dims) == 2:  # NC
            return 1
        elif len(dims) == 1:  # C for bias
            return 1
    elif dformat == aidge_core.dformat.chwn:
        assert len(dims) == 4
        return dims[1]
    elif dformat == aidge_core.dformat.ncdhw:
        assert len(dims) == 4
        return dims[3]
    elif dformat == aidge_core.dformat.ndhwc:
        assert len(dims) == 4
        return dims[2]
    elif dformat == aidge_core.dformat.cdhwn:
        assert len(dims) == 4
        return dims[2]
    elif dformat == aidge_core.dformat.chw:
        assert len(dims) == 3
        return dims[1]
    elif dformat == aidge_core.dformat.hwc:
        assert len(dims) == 3
        return dims[0]
    elif dformat == aidge_core.dformat.nwc:
        assert len(dims) == 3
        return 1
    elif dformat == aidge_core.dformat.ncw:
        assert len(dims) == 3
        return 1
    else:
        raise RuntimeError(f"Unknown dataformat: {dformat}")


def get_width(tensor: aidge_core.Tensor) -> int:
    dformat = tensor.dformat()
    dims = tensor.dims()
    if dformat == aidge_core.dformat.default or dformat == aidge_core.dformat.nchw:
        if len(dims) == 4:  # Suppose NCHW
            return dims[3]
        elif len(dims) == 3:  # Suppose NCW
            return dims[2]
        elif len(dims) == 2:  # Suppose NC
            return 1
        elif len(dims) == 1:  # Suppose C for bias
            return 1
    elif dformat == aidge_core.dformat.nhwc:
        if len(dims) == 4:  # NHWC
            return dims[2]
        elif len(dims) == 3:  # NWC
            return dims[1]
        elif len(dims) == 2:  # NC
            return 1
        elif len(dims) == 1:  # C for bias
            return 1
    elif dformat == aidge_core.dformat.chwn:
        assert len(dims) == 4
        return dims[2]
    elif dformat == aidge_core.dformat.ncdhw:
        assert len(dims) == 4
        return dims[4]
    elif dformat == aidge_core.dformat.ndhwc:
        assert len(dims) == 4
        return dims[3]
    elif dformat == aidge_core.dformat.cdhwn:
        assert len(dims) == 4
        return dims[3]
    elif dformat == aidge_core.dformat.chw:
        assert len(dims) == 3
        return dims[2]
    elif dformat == aidge_core.dformat.hwc:
        assert len(dims) == 3
        return dims[1]
    elif dformat == aidge_core.dformat.nwc:
        assert len(dims) == 3
        return dims[1]
    elif dformat == aidge_core.dformat.ncw:
        assert len(dims) == 3
        return dims[2]
    else:
        raise RuntimeError(f"Unknown dataformat: {dformat}")

def get_batch(tensor: aidge_core.Tensor) -> int:
    dformat = tensor.dformat()
    dims = tensor.dims()
    if dformat == aidge_core.dformat.default or dformat == aidge_core.dformat.nchw:
        if len(dims) == 4:  # Suppose NCHW
            return dims[0]
        elif len(dims) == 3:  # Suppose NCW
            return dims[0]
        elif len(dims) == 2:  # Suppose NC
            return dims[0]
        elif len(dims) == 1:  # Suppose C for bias
            return 1
    elif dformat == aidge_core.dformat.nhwc:
        if len(dims) == 4:  # NHWC
            return dims[0]
        elif len(dims) == 3:  # NWC
            return dims[0]
        elif len(dims) == 2:  # NC
            return dims[0]
        elif len(dims) == 1:  # C for bias
            return 1
    elif dformat == aidge_core.dformat.chwn:
        assert len(dims) == 4
        return dims[3]
    elif dformat == aidge_core.dformat.ncdhw:
        assert len(dims) == 4
        return dims[0]
    elif dformat == aidge_core.dformat.ndhwc:
        assert len(dims) == 4
        return dims[0]
    elif dformat == aidge_core.dformat.cdhwn:
        assert len(dims) == 4
        return dims[4]
    elif dformat == aidge_core.dformat.chw:
        assert len(dims) == 3
        return 1
    elif dformat == aidge_core.dformat.hwc:
        assert len(dims) == 3
        return 1
    elif dformat == aidge_core.dformat.nwc:
        assert len(dims) == 3
        return dims[0]
    elif dformat == aidge_core.dformat.ncw:
        assert len(dims) == 3
        return dims[0]
    else:
        raise RuntimeError(f"Unknown dataformat: {dformat}")


class ExportNode(ABC):
    """Abstract class to interface node with export generation.

    This class exposes a dictionary, ``attributes``, which contains all the information
    required to generate an export for a given node, including input/output names,
    dimensions, types, and optional memory information.

    - All the attributes of the Aidge Operator are automatically fetch, the key to get an attribute is the attribute name in python format, example ``no_bias``

    - **node** (aidge_core.Node): The Aidge Node instance associated with this ExportNode.

    - **name** (str): Name of the node, typically set via the Aidge node.

    - **nb_in** (int): Number of input connections for the node.

    - **nb_out** (int): Number of output connections for the node.

    - **in_name** (list[str]): Unique name for each input connection.

      Format:
        - If no input node: ``{node_name}_input_{in_id}``
        - If there is a parent node: ``{parent_name}_output_{out_id}``

    - **in_dims** (list[list[int]]): Dimensions of each input.

    - **in_node** (list[aidge_core.Node]): List of associated input nodes.

    - **in_size** (list[int]): Size of each input.

    - **in_chan** (list[int]): Channels in each input, based on data format.

    - **in_height** (list[int]): Height of each input, based on data format.

    - **in_width** (list[int]): Width of each input, based on data format.

    - **in_batch** (list[int]): Batch of each input, based on data format.

    - **in_dtype** (list[:py:class:`aidge_core.dtype`]): Data type for each input (Aidge format).

    - **in_cdtype** (list[str]): Data type for each input (C/C++ format).

    - **out_name** (list[str]): Unique name for each output, formatted as ``{name}_output_{out_id}``.

    - **out_node** (list[list[aidge_core.Node]]): Associated output nodes for each output.

    - **out_dims** (list[list[int]]): Dimensions of each output.

    - **out_size** (list[int]): Size of each output.

    - **out_chan** (list[int]): Channels in each output, based on data format.

    - **out_height** (list[int]): Height of each output, based on data format.

    - **out_width** (list[int]): Width of each output, based on data format.

    - **out_batch** (list[int]): Batch of eact output, based on data format.

    - **out_dtype** (list[:py:class:`aidge_core.dtype`]): Data type for each output (Aidge format).

    - **out_cdtype** (list[str]): Data type for each output (C/C++ format).

    - **mem_info** (bool): True if `mem_info` is available for this node.

    - **mem_info_size** (list[int]): Memory size for each output, if applicable.

    - **mem_info_offset** (list[int]): Offset to access each output, if applicable.

    - **mem_info_stride** (list[int]): Stride for accessing each output.

    - **mem_info_length** (list[int]): Length of each output.

    - **mem_info_cont_size** (list[int]): Continuous size for each output.

    - **mem_info_cont_offset** (list[int]): Continuous offset for each output.

    - **mem_info_wrap_offset** (list[int]): Wrap offset for each output.

    - **mem_info_wrap_size** (list[int]): Wrap size for each output.

    """

    @abstractmethod
    def __init__(self, aidge_node: aidge_core.Node,
                 mem_info: List[dict]=None,
                 conversion_map: Dict[aidge_core.dtype, str] = data_conversion.datatype_converter_aidge2c) -> None:
        """Create ExportNode and retrieve attributes from ``aidge_node``:
        """

        super().__init__()
        self.node = aidge_node
        self.operator = aidge_node.get_operator()
        # Attributes are auto fetched from aidge operators
        self.attributes = {}  if isinstance(self.operator, aidge_core.MetaOperatorOp) or self.operator.attr is None else self.operator.attr.dict()
        self.attributes["node"] = self.node
        self.attributes["name"] = self.node.name()
        self.attributes["nb_in"] = self.node.get_nb_inputs()
        self.attributes["nb_out"] = self.node.get_nb_outputs()

        if not self.node.name():
            raise RuntimeError(f"Empty node name is not allowed for export (for node {self.node})")

        # List of input nodes
        self.inputs = []
        # List of output nodes
        self.outputs = []

        self.attributes["in_name"] = [None] * self.attributes["nb_in"]
        self.attributes["in_node"] = [None] * self.attributes["nb_in"]
        self.attributes["in_dims"] = [None] * self.attributes["nb_in"]
        self.attributes["in_size"] = [None] * self.attributes["nb_in"]
        self.attributes["in_dformat"] = [None] * self.attributes["nb_in"]
        self.attributes["in_format"] = [None] * self.attributes["nb_in"]
        self.attributes["in_dtype"] = [None] * self.attributes["nb_in"]
        self.attributes["in_cdtype"] = [None] * self.attributes["nb_in"]
        self.attributes["in_sizeof"] = [None] * self.attributes["nb_in"]
        self.attributes["in_chan"] = [None] * self.attributes["nb_in"]
        self.attributes["in_height"] = [None] * self.attributes["nb_in"]
        self.attributes["in_width"] = [None] * self.attributes["nb_in"]
        self.attributes["in_batch"] = [None] * self.attributes["nb_in"]

        self.attributes["out_name"] = [None] * self.attributes["nb_out"]
        self.attributes["out_nodes"] = [None] * self.attributes["nb_out"]
        self.attributes["out_dims"] = [None] * self.attributes["nb_out"]
        self.attributes["out_size"] = [None] * self.attributes["nb_out"]
        self.attributes["out_dformat"] = [None] * self.attributes["nb_out"]
        self.attributes["out_format"] = [None] * self.attributes["nb_out"]
        self.attributes["out_dtype"] = [None] * self.attributes["nb_out"]
        self.attributes["out_cdtype"] = [None] * self.attributes["nb_out"]
        self.attributes["out_chan"] = [None] * self.attributes["nb_out"]
        self.attributes["out_height"] = [None] * self.attributes["nb_out"]
        self.attributes["out_width"] = [None] * self.attributes["nb_out"]
        self.attributes["out_batch"] = [None] * self.attributes["nb_out"]

        # TODO: document this attribute
        # true if node have mem_info else false
        self.attributes["mem_info"] = mem_info is not None and len(mem_info) > 0
        if self.attributes["mem_info"]:
            self.attributes["mem_info_size"] = [None] * self.attributes["nb_out"]
            self.attributes["mem_info_offset"] = [None] * self.attributes["nb_out"]
            self.attributes["mem_info_stride"] = [None] * self.attributes["nb_out"]
            self.attributes["mem_info_length"] = [None] * self.attributes["nb_out"]
            self.attributes["mem_info_cont_size"] = [None] * self.attributes["nb_out"]
            self.attributes["mem_info_cont_offset"] = [None] * self.attributes["nb_out"]
            self.attributes["mem_info_wrap_offset"] = [None] * self.attributes["nb_out"]
            self.attributes["mem_info_wrap_size"] = [None] * self.attributes["nb_out"]

        for idx, parent_node_in_id in enumerate(self.node.inputs()):
            parent_node, out_id = parent_node_in_id
            self.inputs.append(parent_node)
            if self.operator.get_input(idx) is not None:
                tensor = self.operator.get_input(idx)
                self.attributes["in_name"][idx] = f"{self.attributes['name']}_input_{idx}" if parent_node is None else f"{parent_node.name()}_output_{out_id}"
                self.attributes["in_node"][idx] = parent_node
                self.attributes["in_dims"][idx] = tensor.dims()
                self.attributes["in_size"][idx] = tensor.size()
                self.attributes["in_dformat"][idx] = tensor.dformat()
                self.attributes["in_format"][idx] = aidge_core.format_as(tensor.dformat())
                self.attributes["in_dtype"][idx] = tensor.dtype()
                # self.attributes["in_cdtype"][idx] = data_conversion.aidge2c(tensor.dtype())
                self.attributes["in_cdtype"][idx] = data_conversion.aidge2export_type(tensor.dtype(), conversion_map)
                self.attributes["in_sizeof"][idx] = (aidge_core.dtype_bit_width(tensor.dtype()) + 8 - 1) // 8
                self.attributes["in_chan"][idx] = get_chan(tensor)
                self.attributes["in_height"][idx] = get_height(tensor)
                self.attributes["in_width"][idx] = get_width(tensor)
                self.attributes["in_batch"][idx] = get_batch(tensor)
            elif self.operator.input_category(idx) == aidge_core.InputCategory.OptionalParam or \
                self.operator.input_category(idx) == aidge_core.InputCategory.OptionalData:
                pass
            else:
                raise RuntimeError(f"No input for {self.node.name()} at input {idx}, did you forget to forward dims?")
        for idx, list_child_node_in_id in enumerate(self.node.outputs()):
            out_nodes = [node_in_id[0]
                             for node_in_id in list_child_node_in_id]
            self.outputs += out_nodes
            if self.operator.get_output(idx) is not None:
                tensor = self.operator.get_output(idx)
                self.attributes["out_name"][idx] = f"{self.attributes['name']}_output_{idx}"
                self.attributes["out_nodes"][idx] = out_nodes
                self.attributes["out_dims"][idx] = tensor.dims()
                self.attributes["out_size"][idx] = tensor.size()
                self.attributes["out_dformat"][idx] = tensor.dformat()
                self.attributes["out_format"][idx] = aidge_core.format_as(tensor.dformat())
                self.attributes["out_dtype"][idx] = tensor.dtype()
                # self.attributes["out_cdtype"][idx] = data_conversion.aidge2c(tensor.dtype())
                self.attributes["out_cdtype"][idx] = data_conversion.aidge2export_type(tensor.dtype(), conversion_map)
                self.attributes["out_chan"][idx] = get_chan(tensor)
                self.attributes["out_height"][idx] = get_height(tensor)
                self.attributes["out_width"][idx] = get_width(tensor)
                self.attributes["out_batch"][idx] = get_batch(tensor)
                # Output mem_info
                # TODO: add to docstring
                if self.attributes["mem_info"]:
                    if "size" in mem_info[idx]:
                        self.attributes["mem_info_size"][idx] = mem_info[idx]["size"]
                    else:
                        raise RuntimeError("Size is mandatory")
                    if "offset" in mem_info[idx]:
                        self.attributes["mem_info_offset"][idx] = mem_info[idx]["offset"]
                    else:
                        raise RuntimeError("Offset is mandatory")
                    if "stride" in mem_info[idx]:
                        self.attributes["mem_info_stride"][idx] = mem_info[idx]["stride"]
                    else:
                        self.attributes["mem_info_stride"][idx] = mem_info[idx]["size"]
                    if "length" in mem_info[idx]:
                        self.attributes["mem_info_length"][idx] = mem_info[idx]["length"]
                    else:
                        self.attributes["mem_info_length"][idx] = tensor.size()
                    if "cont_size" in mem_info[idx]:
                        self.attributes["mem_info_cont_size"][idx] = mem_info[idx]["cont_size"]
                    else:
                        self.attributes["mem_info_cont_size"][idx] = mem_info[idx]["size"]
                    if "cont_offset" in mem_info[idx]:
                        self.attributes["mem_info_cont_offset"][idx] = mem_info[idx]["cont_offset"]
                    else:
                        self.attributes["mem_info_cont_offset"][idx] = mem_info[idx]["offset"]
                    if "cont_offset" in mem_info[idx]:
                        self.attributes["mem_info_wrap_offset"][idx] = mem_info[idx]["wrap_offset"]
                    else:
                        self.attributes["mem_info_wrap_offset"][idx] = 0
                    if "wrap_size" in mem_info[idx]:
                        self.attributes["mem_info_wrap_size"][idx] = mem_info[idx]["wrap_size"]
                    else:
                        self.attributes["mem_info_wrap_size"][idx] = 0
            else:
                raise RuntimeError(f"No output for {self.node.name()}")

    # **Class Attributes:**

    # - **config_template** (str): Path to the template defining how to export the node definition.
    #   This template is required for exporting; if undefined, raises an error, if no config
    #   template is required set this to an empty string.

    # - **forward_template** (str): Path to the template for generating code to perform a forward pass
    #   of the node. Required for exporting the forward pass; raises an error if undefined.

    # - **include_list** (list[str]): List of include paths (e.g., "include/toto.hpp") to be added to
    #   the generated export files. Must be defined before export; raises an error if undefined.

    # - **kernels_to_copy** (list[str]): List of paths to kernel files that should be copied during
    #   export. The kernels are copied to ``kernels_path``, and are automatically
    #   added to the include list.

    # - **kernels_path** (str): Path where all kernels are stored in the export, prefixed by the
    #   `export_root`. Defaults to "include/kernels".

    # - **config_path** (str): Path of the configuration folder where node definitions are exported.
    #   Defaults to "include/layers".

    # - **config_extension** (str): File extension for the configuration files, typically for header
    #   files. Defaults to "h".

class ExportNodeCpp(ExportNode):
    """Class for exporting Aidge nodes with C++ code generation.

    This subclass of :class:`ExportNode` defines specific templates,
    configuration paths, and other attributes required to generate
    C++ code for Aidge nodes, including header and source files
    for node definitions and forward passes.

    :var config_template: Path to the template defining how to export the node definition.
        This template is required for exporting; if undefined, raises an error, if no config
        template is required set this to an empty string.
    :vartype config_template: str
    :var forward_template: Path to the template for generating code to perform a forward pass
        of the node. Required for exporting the forward pass; raises an error if undefined.
    :vartype forward_template: str
    :var include_list: List of include paths (e.g., "include/toto.hpp") to be added to
        the generated export files. Must be defined before export; raises an error if undefined.
    :vartype include_list: list[str]
    :var kernels_to_copy: A list of dict holding src and dst kernels paths to copy in the export.
        export. The kernels are copied in dst_path (default : self.kernels_path).
        They are automatically added to the include list unless the fwd_include option is set to False.
    :vartype kernels_to_copy: list[dict]
    :var kernels_path: Path where all kernels are stored in the export, prefixed by the
        `export_root`. Defaults to "include/kernels".
    :vartype kernels_path: str
    :var config_path: Path of the configuration folder where node definitions are exported.
        Defaults to "include/layers".
    :vartype config_path: str
    :var config_extension: File extension for the configuration files, typically for header
        files. Defaults to "h".
    :vartype config_extension: str
    :var dev_mode: Wether or not the developer mode is enabled. If enabled, the export files
        will be symlinks from the aidge export module. Therefore, modifying
        a file within the export will change the module as well. 
        The dev_mode flag is also passed to the forward jinja templates to allow export
        customization (ie. Adding a debug mode for instance).
    :vartype dev_mode: bool
    """

    # Path to the template defining how to export the node definition
    config_template: str = None
    # Path to the template defining how to export the node definition
    forward_template: str = None
    # List of includes to add example "include/toto.hpp"
    include_list: list = None
    # A list of dict holding src and dst kernels paths to copy in the export.
    # kernels are copied in dst_path (default : self.kernels_path)
    # They are automatically added to the include list unless the fwd_include option is set to False.
    kernels_to_copy = None
    # Path where all the kernels are stored in the export (prefixed by export_root)
    kernels_path: str = "include/kernels"
    # Path of config folders
    config_path: str = "include/layers"
    # Config_folder_extension
    config_extension: str = "h"
    # Dev mode - Symlink copy
    dev_mode: bool = False


    def add_kernel_to_copy(self, kernel_src_path: str, kernel_dst_path: str = kernels_path, fwd_include: bool = True):
        """ Add a kernel to the kernels_to_copy list of dict.
        
        :param kernel_src_path: File path for the kernel to copy within the export module.
        :type kernel_src_path: str
        :param kernel_dst_path: File path for the kernel to copy within the generated export. 
        :type kernel_dst_path: str
        :param fwd_include: Wether the kernel is included in the generated forward file or not.
        :type fwd_include: bool
        """

        if self.kernels_to_copy is None:
            self.kernels_to_copy = []

        kernel_to_copy: dict = {
            "src_path": kernel_src_path,
            "dst_path": kernel_dst_path,
            "fwd_include": fwd_include
        }
        self.kernels_to_copy.append(kernel_to_copy)


    def reformat_kernels_to_copy(self):
        """ Adapt the `kernels_to_copy` format to fit the new approach

        Deprecation function which convert the old way to define the 
        kernels_to_copy variable (List of kernels source paths) to
        the new one (List of dictionnaries holding source and destination
        paths as well as a boolean indicated wether the file needs to be
        included into the generated forward file). 
        """

        deprecated_kernel_to_copy = self.kernels_to_copy
        self.kernels_to_copy = None

        for src_path in deprecated_kernel_to_copy:
            self.add_kernel_to_copy(src_path)


    def export(self, export_folder: str):
        """Defines how to export the node definition.

        This method checks that `config_template`, `include_list`, and
        `kernels_to_copy` are defined, then copies each kernel to the export folder,
        appends their paths to the include list, and generates the configuration file
        based on the `config_template`.

        :param export_folder: Folder path where the files are exported.
        :type export_folder: str
        :return: List of include paths with the paths for kernels and configuration files.
        :rtype: list[str]
        """
        if self.config_template is None:
            raise ValueError("config_template have not been defined")
        if self.include_list is None:
            raise ValueError("include_list have not been defined")
        if self.kernels_to_copy is None:
            raise ValueError("kernels_to_copy have not been defined")
        
        # Check for deprecated usage of kernels_to_copy
        if len(self.kernels_to_copy) > 0 and isinstance(self.kernels_to_copy[0], str):
            aidge_core.Log.warn("This way of using kernels_to_copy is deprecated. " \
                                "Please consider using the add_kernel_to_copy() function instead.")
            self.reformat_kernels_to_copy()


        kernel_include_list = []
        for kernel in self.kernels_to_copy:

            # Copy the kernel file
            kernel_src_path = Path(kernel["src_path"])
            kernel_dst_path = Path(kernel["dst_path"])
            code_generation.copy_file(
                kernel_src_path,
                str(export_folder / kernel_dst_path),
                self.dev_mode
            )

            # Include the kernel file within the fwd
            if kernel["fwd_include"]:
                kernel_include_list.append(
                    kernel_dst_path / (kernel_src_path.stem + kernel_src_path.suffix))

        if self.config_template != "":
            path_to_definition = f"{self.config_path}/{self.attributes['name']}.{self.config_extension}"

            try:
                code_generation.generate_file(
                    str(export_folder / path_to_definition),
                    self.config_template,
                    **self.attributes
                )
            except Exception as e:
                raise RuntimeError(f"Error when creating config file for {self.node.name()}[{self.node.type()}].") from e
            kernel_include_list.append(path_to_definition)

        return self.include_list + kernel_include_list

    def forward(self):
        """Generates code for a forward pass using the `forward_template`.
        """
        if self.forward_template is None:
            raise ValueError("forward_template have not been defined")
        forward_call: str = code_generation.generate_str(
            self.forward_template,
            **self.attributes
        )
        return [forward_call]
