import aidge_core

def remove_optional_inputs(graph_view: aidge_core.GraphView):
    """ Remove optional inputs from the ordered_list of the model

    :param graph_view: An instance of :py:class:`aidge_core.graph_view`, providing access to nodes and
                       ordered input/output data within the computational graph.
    :type graph_view: aidge_core.graph_view
    """

    inputNodes = []
    for n in graph_view.get_ordered_inputs():
        if not (int(n[0].get_operator().input_category(n[1])) & int(aidge_core.InputCategory.Optional)):
            inputNodes.append(n)
    graph_view.set_ordered_inputs(inputNodes)

def get_node_from_metaop(node: aidge_core.Node, node_type: str):
    """
    Given a node, this function will check if the type correspond to the given type, 
    if not and the operator is a MetaOperator, then we call recursively this function
    on the GraphView held by the MetaOperator. 
    This function will return a list of matching nodes. 

    :param node: Node to browse
    :type node: aidge_core.Node
    :param node_type: Node type
    :type node_type: str
    """

    if node.type() == node_type:
        return [node]
    res = []
    if isinstance(node.get_operator(), aidge_core.MetaOperatorOp):
        for n in node.get_operator().get_micro_graph().get_nodes():
            res += get_node_from_metaop(n, node_type)    
    return res
