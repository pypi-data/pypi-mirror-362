from aidge_core.aidge_export_aidge.registry import ExportSerialize
from aidge_core.aidge_export_aidge import ROOT_EXPORT
from aidge_core.export_utils import ExportNodeCpp
from aidge_core import ImplSpec, IOSpec, dtype

@ExportSerialize.register(["ConvDepthWise1D", "ConvDepthWise2D"], ImplSpec(IOSpec(dtype.any)))
class ConvDepthWise(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
        self.config_template = str(
            ROOT_EXPORT / "templates/attributes/conv_depth_wise.jinja")
        self.forward_template = str(
            ROOT_EXPORT /"templates/graph_ctor/conv_depth_wise.jinja")
        self.include_list = ["aidge/operator/ConvDepthWise.hpp"]
        self.kernels_to_copy = []
        self.config_path = "include/attributes"
        self.config_extension = "hpp"
