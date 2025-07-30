def parse_node_input(node_inputs: list) -> list:
    """Parse node intputs in order to adapt the list for Jinja.

    :param node_inputs: return of node.inputs()
    :type node_inputs: list of tuple of aidge_core.Node, output idx.
    :return: list of tuple of node name, output idx.
    :rtype: list
    """
    return [None if parent_node is None else (parent_node.name(), outId) for parent_node, outId in node_inputs]
