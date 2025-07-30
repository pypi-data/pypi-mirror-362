import os

from aidge_core.export_utils.code_generation import generate_file
from aidge_core.export_utils.data_conversion import aidge2c
from aidge_core import Tensor
from pathlib import Path

def tensor_to_c(tensor:Tensor)->str:
    """Given a :py:class:``aigd_core.Tensor``, return a C description of the tensor.
    For example:
    {
        {1, 2},
        {3, 4}
    }

    :param tensor: Tensor to transform to a string
    :type tensor: Tensor
    :return: String representation of a C array
    :rtype: str
    """
    return str(tensor)

def generate_input_file(export_folder:str,
                        array_name:str,
                        tensor:Tensor):

    # If directory doesn't exist, create it
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
    print(f"gen : {export_folder}/{array_name}.h")
    ROOT = Path(__file__).resolve().parents[0]

    if tensor.has_impl():
        fallback_tensor = Tensor()
        tensor_host = tensor.ref_from(fallback_tensor, "cpu")
        generate_file(
            file_path=f"{export_folder}/{array_name}.h",
            template_path=str(ROOT / "templates" / "c_data.jinja"),
            dims = tensor.dims(),
            data_t = aidge2c(tensor.dtype()),
            name = array_name,
            values = list(tensor_host)
        )
    else:
        generate_file(
            file_path=f"{export_folder}/{array_name}.h",
            template_path=str(ROOT / "templates" / "c_data.jinja"),
            dims = tensor.dims(),
            data_t = aidge2c(tensor.dtype()),
            name = array_name,
            values = []
        )
