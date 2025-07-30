import os
import json
import builtins
import aidge_core
import numpy as np
from pathlib import Path
from typing import Any, Dict, List, Optional

def _retrieve_operator_attrs(node : aidge_core.Node) -> Dict[str, Optional[Any]]:
    """
    Returns the dictionary containing the attributes of a given Node.

    :param graph: A Node in the list of ordered nodes.
    :type graph: aidge_core.Node

    :return: A dictionary with the Node's attributes.
    :rtype: Dict[str, Optional[Any]]
    """

    if node.get_operator().attr is not None:
        node_attr_dict =  node.get_operator().attr.dict()
        for key,value in node_attr_dict.items():
            if isinstance(value, aidge_core.aidge_core.Tensor):
                new_value = {
                    "dims": value.dims(),
                    "data_type": value.dtype(),
                    "tensor_data": np.array(value).tolist()
                }

                node_attr_dict[key] = new_value
    else:
        node_attr_dict = {}

    return node_attr_dict

def _create_dict(ordered_nodes : List[aidge_core.Node], write_trainable_params_embed : bool, write_trainable_params_ext : bool, path_trainable_params : Path, params_file_format : str) -> Dict[str, Optional[Any]]:
    """
    Creates a dictionary to store the information of a given ordered GraphView.

    :param ordered_nodes: A list with the GraphView's ordered nodes.
    :type graph: list
    :param write_trainable_params_embed: Whether or not to write the eventual trainable parameters of the Nodes in the same file as the dict (embed).
    :type write_trainable_params_embed: bool
    :param write_trainable_params_ext: Whether or not to write the eventual trainable parameters of the Nodes in an external file.
    :type write_trainable_params_ext: bool
    :param path_trainable_params: Path of the external file used to store the Nodes' trainable parameters.
    :type path_trainable_params: Path
    :param params_file_format: Format of the external file used to store the Nodes' trainable parameters. Options: ``npz`` or ``json``. Default : ``json``. Requires ``write_trainable_params_ext``.
    :type params_file_format: str

    :return: A dictionary with the GraphView description.
    :rtype: Dict[str, Optional[Any]]
    """

    graphview_dict = {'graph': []}

    for node in ordered_nodes:

        if node is not None:
            node_dict = {'name' : node.name(),
                         'optype' : node.get_operator().type(),
                         'nb_inputs' : node.get_operator().nb_inputs(),
                         'nb_outputs' : node.get_operator().nb_outputs()}

            inputs = []
            if node.get_operator().nb_inputs() > 0:
                for input_idx in range(node.get_operator().nb_inputs()):
                    if node.get_operator().get_input(input_idx) is not None:
                        input_dict = {'dims' : node.get_operator().get_input(input_idx).dims(),
                                    'data_type' : str(node.get_operator().get_input(input_idx).dtype()),
                                    'data_format' : str(node.get_operator().get_input(input_idx).dformat())}
                    
                    elif node.get_operator().get_input(input_idx) is None:
                        input_dict = {'dims' : None,
                                    'data_type' : None,
                                    'data_format' : None}

                    inputs.append(input_dict)

            node_dict['inputs'] = inputs

            outputs = []
            if node.get_operator().nb_outputs() > 0:
                for output_idx in range(node.get_operator().nb_outputs()):
                    if node.get_operator().get_output(output_idx) is not None:
                        output_dict = {'dims' : node.get_operator().get_output(output_idx).dims(),
                                    'data_type' : str(node.get_operator().get_output(output_idx).dtype()),
                                    'data_format' : str(node.get_operator().get_output(output_idx).dformat())}
                    
                    elif node.get_operator().get_output(output_idx) is None:
                        output_dict = {'dims' : None,
                                    'data_type' : None,
                                    'data_format' : None}

                    outputs.append(output_dict)

            node_dict['outputs'] = outputs

            parents = node.get_parents()
            if None in parents:
                if parents[0] is None: parents.append(parents.pop(0))
            else:
                pass

            parents_inputs = []
            input_idx = 0
            for parent in node.get_parents():
                if parent is not None:
                    for children in parent.outputs():
                        for child in children:
                            if child[0] == node and child[1] == input_idx:
                                parents_inputs.append((parent.name(), input_idx))

                elif parent is None:
                    if input_idx not in [item[1] for item in parents_inputs]:
                        parents_inputs.append((None, input_idx))

                input_idx += 1
            node_dict['parents'] = parents_inputs

            children_outputs = []
            output_idx = 0
            for children in node.get_ordered_children():
                for child in children:
                    if child is not None:
                        for parent in child.inputs():
                            if parent[0] == node and parent[1] == output_idx:
                                children_outputs.append((child.name(), output_idx))
                output_idx += 1
            node_dict['children'] = children_outputs

            # Check if Node is a metaop
            attributes_dict = {}
            if isinstance(node.get_operator(), aidge_core.MetaOperatorOp):
                attributes_dict['micro_graph'] = []
                for micro_node in node.get_operator().get_micro_graph().get_nodes():
                    micro_node_dict = {'name' : micro_node.name(),
                                        'optype' : micro_node.type()}

                    micro_node_attr_dict =  _retrieve_operator_attrs(micro_node)
                    micro_node_dict['attributes'] = micro_node_attr_dict
                    attributes_dict['micro_graph'].append(micro_node_dict)

            else:
                node_attr_dict = _retrieve_operator_attrs(node)
                attributes_dict.update(node_attr_dict)

            node_dict['attributes'] = attributes_dict

            if node.type() == 'Producer':
                if write_trainable_params_ext:

                    params_file_format.casefold()

                    if params_file_format=='npz':
                        np.savez_compressed(Path(path_trainable_params, node.name()), **{node.name() : node.get_operator().get_output(0)})
                        node_dict['tensor_data'] = str(Path(path_trainable_params, node.name() + '.npz'))

                    elif params_file_format=='json':
                        tensor = node.get_operator().get_output(0)
                        tensor_dict = {
                            node.name() :
                            {
                                'dims' : tensor.dims(),
                                'data_type' : tensor.dtype(),
                                'tensor_data' : np.array(tensor).tolist()
                            }
                        }

                        with open(Path(path_trainable_params, node.name() + '.json'), 'w') as fp:
                            json.dump(tensor_dict, fp, indent=4, default=str)

                        node_dict['tensor_data'] = str(Path(path_trainable_params, node.name() + '.json'))

                    else:
                        raise Exception("File format to write trainable parameters not recognized.")


                if write_trainable_params_embed:
                    node_dict['tensor_data'] = np.array(node.get_operator().get_output(0)).tolist()

                else:
                    pass

            graphview_dict['graph'].append(node_dict)

        else: # node is None
            pass

    return graphview_dict

def _write_dict_json(graphview_dict : Dict[str, Optional[Any]], json_path : str) -> None:
    """
    Writes dictionary containing GraphView description to a JSON file.

    :param graphview_dict: A dictionary with the GraphView description.
    :type graphview_dict: dict[str, int, float, bool, None]
    :param json_path: Path to write JSON file.
    :type json_path: str
    """

    with open(json_path, 'w') as fp:
        json.dump(graphview_dict, fp, indent=4, default=str)

    return None

def gview_to_json(gview : aidge_core.GraphView, json_path : Path, write_trainable_params_embed : bool = False, write_trainable_params_ext : bool = False, params_file_format : str = 'json') -> None:
    """
    Generates the description for a GraphView in the JSON format.

    :param graph: A GraphView of Aidge.
    :type graph: aidge_core.GraphView
    :param json_path: Path to write JSON file.
    :type json_path: Path
    :param write_trainable_params_embed: Whether or not to write the eventual trainable parameters of the Nodes in the same file as the dict (embed).
    :type write_trainable_params_embed: bool, optional
    :param write_trainable_params_ext: Whether or not to write the eventual trainable parameters of the Nodes in an external file.
    :type write_trainable_params_ext: bool, optional
    :param params_file_format: Format of the external file used to store the Nodes' trainable parameters. Options: ``npz`` or ``json``. Default : ``json``. Requires ``write_trainable_params_ext``.
    :type params_file_format: str, optional
    """

    json_path = Path(json_path)

    if not json_path.suffix:
        if not json_path.is_dir():
            json_path.mkdir(parents=True, exist_ok=True)
        json_path = json_path.joinpath('model.json')

    else:
        if json_path.suffix != '.json':
            raise Exception('If ``json_path`` contains a filename, it must be of JSON format.')
        if not json_path.parent.is_dir():
            json_path.parent.mkdir(parents=True, exist_ok=True)

    if write_trainable_params_ext:
        path_trainable_params = (json_path.parent).joinpath(json_path.stem +  '_trainable_params/')
        path_trainable_params.mkdir(parents=True, exist_ok=True)

    else:
        path_trainable_params = Path()

    if isinstance(gview, aidge_core.GraphView):
        # Sort GraphView in topological order
        ordered_nodes = gview.get_ordered_nodes()

        # Create dict from GraphView
        graphview_dict = _create_dict(ordered_nodes, write_trainable_params_embed, write_trainable_params_ext, path_trainable_params, params_file_format)

        # Write dict to JSON
        _write_dict_json(graphview_dict, json_path)

    else:
        raise Exception("Graph must be an instance of aidge_core.GraphView.")

    return None


##################################################################################################

#PRINT AIDGE GRAPH TO TEXT (from model outputs)
def str_aidge_graph_structure(model:aidge_core.GraphView) -> str :
    """
    Generates a string describing the GraphView starting from the output nodes, then their parents, up to inputs or producers.

    :param node: A GraphView of Aidge.
    :type graph: aidge_core.GraphView

    :return: A string with the GraphView description.
    :rtype: str
    """

    def _str_aidge_node_parents(node:aidge_core.Node, index:int=0, nb_brothers:int=0, str_indent:str=''):

        str_result = ""
        if node is not None:  #the node is present
            s = ' ' if len(str_indent)==0 else '├' if index<nb_brothers else '└'
            str_result += f'{str_indent}{s} {node.name()} ({node.type()})\n'
            parents = node.get_parents()
            nb_parents = len(parents)
            s = '|' if index<nb_brothers else ' '
            for i, parent in enumerate(parents):
                str_result += _str_aidge_node_parents(parent, i, nb_parents-1, f'{str_indent}{s} ')
        else:  #when the node is lacking it means that it is an input...
            s = '├' if index<nb_brothers else '└'
            str_result += f'{str_indent}{s} <input>\n'
        return str_result

    #starting from each node (layer) containing final outputs
    output_nodes = model.get_output_nodes()
    nb_output_nodes = len(output_nodes)
    #generates a string describing the connections, from each output node, then its parents, up to inputs or producers.
    str_result = ""
    for i, node in enumerate(output_nodes):
        str_result += _str_aidge_node_parents(node, i, nb_output_nodes-1)
    return str_result

##################################################################################################

#PRINT AIDGE STATIC SEQUENTIAL SCHEDULING TO TEXT (from scheduler)
def str_aidge_seq_scheduling(static_scheduling:list[aidge_core.Node]) -> str :
    """
    Generates a string describing a given Sequential Scheduling.

    :param static_scheduling: A list of nodes representing the sequential scheduling.
    :type graph: list of aidge_core.GraphNode

    :return: A string with the scheduling description.
    :rtype: str
    """

    str_result = ""
    max_len_id = len(str(len(static_scheduling)))
    for i, node in enumerate(static_scheduling):
        str_result += f"- {i+1:>{max_len_id}} : {node.name()} ({node.type()})\n"
    return str_result

##################################################################################################
