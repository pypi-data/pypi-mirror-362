import json
import tempfile
import unittest
import builtins
import aidge_core
import numpy as np
from pathlib import Path
from aidge_core.show_graphview import gview_to_json, str_aidge_graph_structure, str_aidge_seq_scheduling

def create_gview():
    # Create a LeNet-like model
    gview = aidge_core.sequential([aidge_core.PaddedConv2D(in_channels=1, out_channels=6, kernel_dims=[5,5], name='feature_feature_0_Conv', stride_dims=[1,1], padding_dims = [2,2,2,2]),
                               aidge_core.ReLU(name='feature_feature_1_Relu'),
                               aidge_core.MaxPooling2D(kernel_dims=[2,2], stride_dims=[2,2], ceil_mode=0, name='feature_feature_2_MaxPool'),
                               aidge_core.Conv2D(in_channels=6, out_channels=16, kernel_dims=[5,5], name='feature_feature_3_Conv', stride_dims=[1,1], dilation_dims = [1,1]),
                               aidge_core.ReLU(name='feature_feature_4_Relu'),
                               aidge_core.MaxPooling2D(kernel_dims=[2,2], stride_dims=[2,2], ceil_mode=0, name='feature_feature_5_MaxPool'),
                               aidge_core.FC(in_channels=400, out_channels=120, name='classifier_classifier_1_Gemm'),
                               aidge_core.ReLU(name='classifier_classifier_2_Relu'),
                               aidge_core.FC(in_channels=120, out_channels=84, name='classifier_classifier_3_Gemm'),
                               aidge_core.ReLU(name='classifier_classifier_4_Relu'),
                               aidge_core.FC(in_channels=84, out_channels=10, name='classifier_classifier_5_Gemm'),
                            ])

    # Fill Producers
    for node in gview.get_nodes():
        if node.type() == "Producer":
            prod_op = node.get_operator()
            value = prod_op.get_output(0)
            value.set_backend("cpu")
            tuple_out = node.output(0)[0]

            if (tuple_out[0].type() == "Conv2D" or tuple_out[0].type() == "PaddedConv2D") and tuple_out[1]==1:
                # Conv weight
                aidge_core.xavier_uniform_filler(value)
            elif tuple_out[0].type() == "Conv2D" and tuple_out[1]==2:
                # Conv bias
                aidge_core.constant_filler(value, 0.01)
            elif tuple_out[0].type() == "FC" and tuple_out[1]==1:
                # FC weight
                aidge_core.normal_filler(value)
            elif tuple_out[0].type() == "FC" and tuple_out[1]==2:
                # FC bias
                aidge_core.constant_filler(value, 0.01)
            else:
                pass

    # Compile model
    gview.forward_dims([[1, 1, 28, 28]])
    gview.set_datatype(aidge_core.dtype.float32)

    return gview

class test_show_gview(unittest.TestCase):
    """Test aidge functionality to show GraphView.
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_gview_to_json(self):

        gview = create_gview()

        # Create temporary file to store JSON model description
        model_description_file = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
        model_description_file.close() # Ensure the file is closed

        # Pass the file path to gview_to_json
        gview_to_json(gview, Path(model_description_file.name))

        # Load JSON
        with open(model_description_file.name, 'r') as fp:
                model_json = json.load(fp)

        # Get list of nodes of Aidge graphview
        gview_ordered_nodes = gview.get_ordered_nodes()

        # Iterate over the list of ordered nodes and the corresponding JSON
        self.assertEqual(len(gview_ordered_nodes), len(model_json['graph']))

        for node_gview, node_json in zip(gview_ordered_nodes, model_json['graph']):

            self.assertEqual(node_gview.get_operator().type(), node_json['optype'])
            self.assertEqual(node_gview.get_operator().nb_inputs(), node_json['nb_inputs'])
            self.assertEqual(node_gview.get_operator().nb_outputs(), node_json['nb_outputs'])

            self.assertEqual(node_gview.get_operator().nb_inputs(), len(node_json['inputs']))
            for input_idx in range(node_gview.get_operator().nb_inputs()):
                self.assertEqual(node_gview.get_operator().get_input(input_idx).dims(), node_json['inputs'][input_idx]['dims'])
                self.assertEqual(str(node_gview.get_operator().get_input(input_idx).dtype()), node_json['inputs'][input_idx]['data_type'])
                self.assertEqual(str(node_gview.get_operator().get_input(input_idx).dformat()), node_json['inputs'][input_idx]['data_format'])

            self.assertEqual(node_gview.get_operator().nb_outputs(), len(node_json['outputs']))
            for output_idx in range(node_gview.get_operator().nb_outputs()):
                self.assertEqual(node_gview.get_operator().get_output(output_idx).dims(), node_json['outputs'][output_idx]['dims'])
                self.assertEqual(str(node_gview.get_operator().get_output(output_idx).dtype()), node_json['outputs'][output_idx]['data_type'])
                self.assertEqual(str(node_gview.get_operator().get_output(output_idx).dformat()), node_json['outputs'][output_idx]['data_format'])

            self.assertEqual(len(node_gview.get_parents()), len(node_json['parents']))
            self.assertEqual(len(node_gview.get_children()), len(node_json['children']))

            if not hasattr(node_gview.get_operator(), 'get_micro_graph'):
                try:
                    self.assertEqual(len(node_gview.get_operator().attr.dict()), len(node_json['attributes']))

                    temp_node_dict = node_gview.get_operator().attr.dict()

                    for key, value in node_gview.get_operator().attr.dict().items():
                        
                        if isinstance(value, aidge_core.aidge_core.Tensor):
                            new_value = {
                                "dims": value.dims(),
                                "data_type": value.dtype(),
                                "tensor_data": np.array(value).tolist()
                            }
                            temp_node_dict.update({key : new_value})
                        
                        elif not type(value).__name__ in dir(builtins):
                            temp_node_dict.update({key : str(value)})

                        else:
                            pass

                    self.assertDictEqual(temp_node_dict, node_json['attributes'])

                except AttributeError:
                    self.assertIsNone(node_gview.get_operator().attr) and self.assertFalse(node_json['attributes'])

            elif hasattr(node_gview.get_operator(), 'get_micro_graph'):

                self.assertEqual(len(node_gview.get_operator().get_micro_graph().get_nodes()), len(node_json['attributes']['micro_graph']))

                for micro_node_gview in node_gview.get_operator().get_micro_graph().get_nodes():
                    for micro_node_json in node_json['attributes']['micro_graph']:
                        if micro_node_gview.get_operator().type() == micro_node_json['optype']:
                            temp_mnode_dict = micro_node_gview.get_operator().attr.dict() # So the dict can be updated if needed
                            for key, value in micro_node_gview.get_operator().attr.dict().items():                           
                                if isinstance(value, aidge_core.aidge_core.Tensor):
                                    new_value = {
                                        "dims": value.dims(),
                                        "data_type": str(value.dtype()),
                                        "tensor_data": np.array(value).tolist()
                                    }
                                    temp_mnode_dict.update({key : new_value})
                                
                                elif not type(value).__name__ in dir(builtins):
                                    # Use str(value) to stay consistent with how json.dumps(..., default=str) handles custom objects
                                    temp_mnode_dict.update({key : str(value)})
                                
                                else:
                                    pass

                            self.assertDictEqual(temp_mnode_dict, micro_node_json['attributes'])



class test_string_presentation(unittest.TestCase):
    """Test aidge functionality to show GraphView as string.
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_gview_to_string(self):

        gview = create_gview()

        print(str_aidge_graph_structure(gview))

    def test_paral_gview_to_string(self):
        gview = aidge_core.sequential([aidge_core.ReLU("A"), aidge_core.parallel([aidge_core.ReLU("B"), aidge_core.ReLU("C")]), aidge_core.Concat(2, name = "D")])
        print(str_aidge_graph_structure(gview))

    def test_mul_input_gview_to_string(self):
        gview = aidge_core.sequential([aidge_core.Concat(2, name = "A")])
        print(str_aidge_graph_structure(gview))


    def test_scheduler_to_string(self):
        schedule = [aidge_core.ReLU(f"A_{i}") for i in range(100)]
        print(str_aidge_seq_scheduling(schedule))


if __name__ == '__main__':
    unittest.main()

