import numpy as np

from aidge_core.aidge_export_aidge.registry import ExportSerialize
from aidge_core.aidge_export_aidge import ROOT_EXPORT
from aidge_core.export_utils import ExportNodeCpp
from aidge_core import ImplSpec, IOSpec, dtype

@ExportSerialize.register("Producer", ImplSpec(IOSpec(dtype.any)))
class Producer(ExportNodeCpp):
    """
    If there is a standardization of the export operators
    then this class should be just a inheritance of ProducerCPP
    """
    def __init__(self, node, mem_info):
        super().__init__(node, mem_info)
        child, in_idx = self.node.output(0)[0]

        self.values = np.array(self.operator.get_output(0))

        self.config_template = str(
            ROOT_EXPORT / "templates/parameter.jinja")
        self.forward_template = str(
            ROOT_EXPORT / "templates/graph_ctor/producer.jinja")
        self.attributes["tensor_name"] = f"{child.name()}_{in_idx}"
        self.attributes["values"] = str(self.operator.get_output(0)).translate(str.maketrans('[]', '{}'))
        self.include_list = ["aidge/operator/Producer.hpp"]
        self.kernels_to_copy = []
        self.config_path = "include/attributes"
        self.config_extension = "hpp"

