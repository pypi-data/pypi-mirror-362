from aidge_core.aidge_export_aidge.registry import ExportSerialize
from aidge_core.aidge_export_aidge import ROOT_EXPORT
from aidge_core.export_utils import ExportNodeCpp
from aidge_core import ImplSpec, IOSpec, dtype

@ExportSerialize.register("ReLU", ImplSpec(IOSpec(dtype.any)))
class ReLU(ExportNodeCpp):
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
        self.config_template = ""
        self.forward_template = str(
            ROOT_EXPORT / "templates/graph_ctor/relu.jinja")
        self.include_list = ["aidge/operator/ReLU.hpp"]
        self.kernels_to_copy = []
