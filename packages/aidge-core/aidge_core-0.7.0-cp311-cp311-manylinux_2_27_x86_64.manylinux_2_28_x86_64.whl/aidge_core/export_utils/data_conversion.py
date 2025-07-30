import numpy as np
import aidge_core

from typing import Dict

datatype_converter_aidge2c = {
    aidge_core.dtype.float64 : "double",
    aidge_core.dtype.float32 : "float",
    aidge_core.dtype.float16 : "half_float::half",
    aidge_core.dtype.int8    : "int8_t",
    aidge_core.dtype.int16   : "int16_t",
    aidge_core.dtype.int32   : "int32_t",
    aidge_core.dtype.int64   : "int64_t",
    aidge_core.dtype.uint8   : "uint8_t",
    aidge_core.dtype.uint16  : "uint16_t",
    aidge_core.dtype.uint32  : "uint32_t",
    aidge_core.dtype.uint64  : "uint64_t"
}

def aidge2c(datatype):
    """Convert a aidge datatype to C type

    If the type is not convertible to a C type (e.g. int4), return None and raise a warning.

    :param datatype: Aidge datatype to convert
    :type datatype: :py:object:`aidge_core.DataType`
    :return: A string representing the C type
    :rtype: string
    """
    if datatype in datatype_converter_aidge2c:
        return datatype_converter_aidge2c[datatype]
    else:
        raise ValueError(f"Unsupported {datatype} aidge datatype")

def aidge2export_type(datatype: aidge_core.dtype, conversion_map: Dict[aidge_core.dtype, str] = datatype_converter_aidge2c) -> str:
    """Convert a aidge datatype to the export type specified by the map passed in argument

    If the aidge type is not convertible, that is to say, is not specified in the map, a value Error is raised.

    :param datatype: Aidge datatype to convert
    :type datatype: :py:object:`aidge_core.DataType`
    :param conversion_map: Map that specify the conversion
    :type conversion_map: Dict[:py:object:`aidge_core.DataType`, str]
    :return: A string representing the export type
    :rtype: string
    """
    if datatype in conversion_map:
        return conversion_map[datatype]
    else:
        raise ValueError(f"Unsupported type conversion {datatype} aidge datatype for export")
