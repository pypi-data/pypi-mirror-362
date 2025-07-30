
from importlib import resources
import json
import os
import copy
from pathlib import Path
import sys
from typing import Optional, Any

import numpy as np


def find_file_in_package(file_path: str) -> Optional[str]:
    """Try to locate the given config file either in current directory or in package data."""
    # Try loading from packaged resources
    try:
        config_file = resources.files("aidge_core.benchmark.operator_config").joinpath(file_path)
        if config_file.is_file():
            return config_file
    except ModuleNotFoundError:
        pass  # if resources can't find the package

    # Not found
    return None

def load_json(file_path: str, search_dir: str = '.') -> dict:
    """
    Loads and returns the JSON configuration from the given file.
    Searches in the given directory, current working directory, and package resources.
    """
    config_path = None

    file_path_obj = Path(file_path)
    search_dir_path = Path(os.path.expanduser(search_dir))

    # Check if file_path is directly usable
    if file_path_obj.is_file():
        config_path = file_path_obj
    # Check inside the search_dir
    elif (search_dir_path / file_path_obj).is_file():
        config_path = search_dir_path / file_path_obj
    # Fallback to package search
    elif find_file_in_package(file_path):
        config_path = find_file_in_package(file_path)

    if not config_path:
        print(file_path, search_dir, file_path_obj, search_dir_path)
        print("Cannot find JSON file.")
        sys.exit(1)

    with open(config_path, "r") as f:
        return json.load(f)

def validate_property(property: dict[str, Any]) -> None:
    required_keys = ["name", "dims", "values"]
    for key in required_keys:
        if key not in property:
            raise KeyError(f"Missing required key in configuration input properties: '{key}'.")

    # optional input not provided. So this could happen
    # if not property["dims"] and not property["values"]:
    #     raise ValueError("At least one of 'dims' or 'values' should be specified in each property")

    if property["values"] is not None:
        assert(isinstance(property["values"], np.ndarray))

    if property["dims"] is not None and property["values"] is not None:
        if property["dims"] != list(property["values"].shape):
            # uncompatible 'dims' and 'values' provided
            raise ValueError(f"Mismatch between 'dims' and 'values' shape")

def validate_config_structure(config: dict[str, Any]) -> None:
    """
    Validates that the configuration dictionary contains the required top-level keys.

    Required keys:
        - "attributes": A dictionary of attribute values.
        - "input_properties": A list of input property dictionaries.

    Raises:
        KeyError: If any required key is missing.
    """
    required_keys = ["attributes", "input_properties"]
    for key in required_keys:
        if key not in config:
            raise KeyError(f"Missing required key in configuration: '{key}'.")

    for prop in config["input_properties"]:
        validate_property(prop)

    # check each input name is unique
    name_set = set()
    for property in config["input_properties"]:
        if property["name"] in name_set:
            raise ValueError(f"'{property['name']}' input specified several times.")
        name_set.add(property["name"])

def convert_list_to_onnx_compatible_array(l: list[int | float | bool]) -> np.ndarray:
    """
    Converts a list of values into a NumPy array with ONNX-compatible data types.

    Supported conversions:
        - bool -> np.bool_
        - int -> np.int64
        - float -> np.float32

    Args:
        values: A list of bools, ints, or floats.

    Returns:
        A NumPy ndarray with the appropriate data type.

    Raises:
        TypeError: If the data type is unsupported.
    """
    array = np.array(l)
    if array.dtype == np.bool_:
        return array.astype(np.bool_)
    elif np.issubdtype(array.dtype, np.integer):
        return array.astype(np.int64)
    elif np.issubdtype(array.dtype, np.floating):
        return array.astype(np.float32)
    else:
        raise TypeError(f"Unsupported data type for list to be converted to ONNX compatible type.")

def make_property_valid(property: dict) -> None:
    if "name" not in property:
        raise KeyError(f"Missing required 'name' key in provided property.")
    property.setdefault("values", None)
    property.setdefault("dims", None)
    if property["values"] is not None:
        property["values"] = convert_list_to_onnx_compatible_array(property['values'])
        if property["dims"]:
            if property["dims"] != list(property["values"].shape):
                # uncompatible 'dims' and 'values' provided
                raise ValueError(f"Mismatch between 'dims' and 'values' shape")
        else:
            property["dims"] = list(property["values"].shape)
    return

def normalize_configuration_format(config: dict[str, Any]) -> None:
    """
    Ensures configuration dictionary format is standardized and all properties are valid.

    This function ensures:
        - 'attributes' and 'input_properties' keys are present.
        - Each input property is validated and ONNX-compatible.

    Raises:
        KeyError, TypeError, ValueError: For malformed configurations.
    """
    # if no config provided, use the default values
    config.setdefault("attributes", {})
    config.setdefault("input_properties", [])

    try:
        for i, prop in enumerate(config["input_properties"]):
            make_property_valid(prop)
        validate_config_structure(config)
    except (TypeError, KeyError, ValueError) as e:
        raise ValueError(f"Invalid property at index {i}: {e}") from e


def clean_benchmark_configuration(benchmark_config: dict[str, Any]) -> None:
    """
    Validates and normalizes a benchmark configuration.

    The configuration must include:
        - 'base_configuration': A valid base configuration.
        - 'test_configurations': A dictionary of test cases, each containing configurations.

    Raises:
        KeyError, TypeError, ValueError: If any configuration is invalid.
    """


    try:
        normalize_configuration_format(benchmark_config["base_configuration"])
    except (TypeError, KeyError, ValueError) as e:
        raise ValueError(f"Invalid 'base_configuration': {e}") from e

    if "test_configurations" not in benchmark_config:
        raise ValueError("Invalid benchmark configuration, no test case found.")

    for param, value in benchmark_config["test_configurations"].items():
        for value_str, config in value.items():
            try:
                normalize_configuration_format(config)
            except (TypeError, KeyError, ValueError) as e:
                raise ValueError(f"Invalid 'test' configuration '{param}: {value_str}': {e}") from e

def merge_test_with_base_configuration(test_config: dict[str, Any], base_config: dict[str, Any]) -> dict[str, Any]:
    """
    Overrides a base configuration with test configuration elements.

    - Preserves the input order from `base_config`.
    - Uses values from `test_config` when present.
    - Falls back to `base_config` for missing input properties or attributes.
    - Ensures the merged input order is uniquely determined, otherwise raises ValueError.

    Args:
        test_config (dict): The test-specific config (may be partial).
        base_config (dict): The base config (may be partial), may be empty.

    Returns:
        dict: Merged configuration with full attributes and input_properties.
    Raises:
        ValueError: If `input_properties` from test and base cannot be merged due to ambiguous ordering.
    """
    def override_attributes(test_attr: dict[str, Any], base_attr: dict[str, Any]) -> dict[str, Any]:
        """Overrides attributes from the base config with those from the test config."""
        updated_attributes = copy.deepcopy(base_attr)
        for k in test_attr:
            updated_attributes[k] = test_attr[k]
        return updated_attributes

    def override_inputs(test_inputs: list[dict[str, Any]], base_inputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Merges the `input_properties` lists from test and base configs while preserving order.

        The resulting list respects the base config's order, but allows test config values to override.
        If the order cannot be uniquely determined, raises a ValueError.
        """
        i: int = 0
        j: int = 0
        B_names = [b["name"] for b in base_inputs]
        T_names = [t["name"] for t in test_inputs]
        I = len(base_inputs)
        J = len(test_inputs)

        updated_inputs: list[dict[str, Any]] = []

        while i < I and j < J:
            k = j
            while k < J:
                if B_names[i] == T_names[k]:
                    break
                k += 1
            if k == J:
                k = i
                while k < I:
                    if T_names[j] == B_names[k]:
                        break
                    k += 1
                if k == I:
                    raise ValueError("Updated input list order cannot be deduced: not a single element in common between the base and test input configuration list.")
                else:
                    # B_names = [a, b, c, ...], T_names = [c, _, ...]
                    # updated += [a, b] from B
                    # udated += [c] from T that overrides
                    updated_inputs += base_inputs[i:k]
                    updated_inputs.append(test_inputs[j])
                    j += 1
                    i += k+1
            else:
                # B_names = [a, _, _, ...], T_names = [x, y, a, _, ...]
                # updated += [x, y, a]
                updated_inputs += test_inputs[j:k+1]
                j = k+1
                i += 1

        if i < I and j == J:
            updated_inputs += base_inputs[i:]
        elif i == I and j < J:
            updated_input += test_inputs[j:]
        elif i < I and j < J:
            raise ValueError("Ill-formed updated input")

        return updated_inputs

    validate_config_structure(test_config)
    validate_config_structure(base_config)

    updated_config = { "attributes": {}, "input_properties": []}


    if len(base_config["input_properties"]) == 0:
        updated_config["input_properties"] = test_config["input_properties"]
    elif len(test_config["input_properties"]) == 0:
        updated_config["input_properties"] = base_config["input_properties"]
    else :
        updated_config["input_properties"] = override_inputs(test_config["input_properties"], base_config["input_properties"])
    updated_config["attributes"] = override_attributes(test_config["attributes"], base_config["attributes"])
    return updated_config


################################################################################

def convert_bytes_to_str(obj):
    """
    Recursively converts bytes in a nested data structure to UTF-8 strings.

    Args:
        obj: A dictionary, list, or value possibly containing bytes.

    Returns:
        A structure with bytes converted to strings.
    """
    if isinstance(obj, dict):
        return {k: convert_bytes_to_str(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_bytes_to_str(item) for item in obj]
    elif isinstance(obj, bytes):
        return obj.decode('utf-8')
    else:
        return obj

def build_template_configuration_for_onnx_op(operator_name: str, opset_version: int, initializer_rank: int) -> dict[str, Any]:
    config: dict = {
        "operator": operator_name,
        "opset_version": opset_version,
        "initializer_rank": initializer_rank,
        "test_meta_data": {
            "multiple_batchs": True
        }
    }

    def build_base_configuration_from_onnx_schema(operator_name: str, opset_version: int) -> dict[str, Any]:
        """
        Builds a base configuration dictionary from the ONNX schema of a given operator.

        The configuration includes:
            - 'attributes': default attribute values (if specified in schema).
            - 'input_properties': input names with placeholder values and dims.

        Args:
            operator_name: Name of the ONNX operator (e.g., "Add", "Relu").

        Returns:
            A base configuration dictionary suitable for test configuration merging.

        Raises:
            RuntimeError: If the operator schema cannot be retrieved.
        """
        from onnx.helper import get_attribute_value
        from onnx.defs import get_schema

        try:
            schema = get_schema(operator_name, opset_version)
        except Exception as e:
            raise RuntimeError(f"Failed to get schema for operator '{operator_name}': {e}")

        base_config = {
            "attributes": {},
            "input_properties": []
        }

        # Handle attributes with default values
        for attr_name, attr_proto in schema.attributes.items():
            if attr_proto.default_value is not None:
                base_config["attributes"][attr_name] = get_attribute_value(attr_proto.default_value)

        # Handle inputs
        for input_param in schema.inputs:
            # No value for 'dims' or 'values' specified
            # This will cause an error if required inputs are not set
            # Optional inputs will not be linked if not set
            base_config["input_properties"].append({
                "name": input_param.name,
                "dims": None,
                "values": None
            })

        return base_config
    config["base_configuration"] = build_base_configuration_from_onnx_schema(operator_name, opset_version)
    config["test_configurations"] = {}
    return convert_bytes_to_str(config)