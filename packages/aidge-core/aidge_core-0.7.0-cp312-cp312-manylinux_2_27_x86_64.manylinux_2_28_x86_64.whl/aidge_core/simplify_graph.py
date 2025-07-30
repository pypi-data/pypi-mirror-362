import numpy as np
import aidge_core

def simplify_graph(graph: aidge_core.GraphView):
    """
    Simplify a graph loaded from ONNX.

    :param graph: The GraphView to simplify.
    :type graph: aidge_core.GraphView
    """

    def check_constant_producer(value):
        def _check_constant_producer(node):
            out = node.get_operator().get_output(0)
            return (len(out) == 1 and np.isclose(out[0], value))
        return _check_constant_producer

    gm = aidge_core.SinglePassGraphMatching(graph)
    gm.add_node_lambda("Constant_sqrt2", check_constant_producer(np.sqrt(2)))
    gm.add_node_lambda("Constant_1", check_constant_producer(1))
    gm.add_node_lambda("Constant_0_5", check_constant_producer(0.5))

    # Linear [from PyTorch ONNX]
    aidge_core.fuse_to_metaops(gm, "MatMul-*>Add", "Linear")

    # LayerNorm [from PyTorch ONNX]
    aidge_core.fuse_to_metaops(gm, "ReduceMean-*>Sub#1~>(Pow#1->ReduceMean-*>Add#1->Sqrt)-*>Div#1-*>Mul#1-*>Add#2;"
                                   "Sub#1~*>Div#1;"
                                   "Pow#1<1~Producer;"
                                   "Add#1<*~Producer;"
                                   "Mul#1<*~Producer;"
                                   "Add#2<*~Producer;"
                                   "Sub#1~>$", "LayerNorm")

    # ScaledDotProductAttention [from PyTorch ONNX]
    aidge_core.fuse_to_metaops(gm, "MatMul->Div#1->Softmax-*>MatMul;"
                                   "Div#1<1~Producer", "ScaledDotProductAttention")

    # MultiHeadAttention [from PyTorch ONNX]
    aidge_core.fuse_to_metaops(gm, "ScaledDotProductAttention#1->Transpose->Reshape#1->Linear;"
                                   "Reshape#1<1~Producer;"
                                   "ScaledDotProductAttention#1<0-(Transpose<-Reshape#2<-Add#1);"
                                   "ScaledDotProductAttention#1<1-(Transpose<-Reshape#3<-Add#2);"
                                   "ScaledDotProductAttention#1<2-(Transpose<-Reshape#4<-Add#3);"
                                   "Reshape#2<1~Producer;"
                                   "Add#1<*-0-Split#1;"
                                   "Add#2<*-1-Split#1;"
                                   "Add#3<*-2-Split#1;"
                                   "Split#1<-MatMul;"
                                   "Split#1<1~Producer", "MultiHeadAttention")

    # GeLU [from PyTorch ONNX]
    aidge_core.fuse_to_metaops(gm, "Div#1->Erf->Add#1-*>Mul->Mul#2;"
                                   "Div#1<1~Producer[Constant_sqrt2];"
                                   "Add#1<*~Producer[Constant_1];"
                                   "Mul#2<*~Producer[Constant_0_5]", "GeLU")
