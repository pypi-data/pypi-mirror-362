import copy
from acuitylib.layer.customlayer import CustomLayer
from acuitylib.layer.acuitylayer import IoMap
from acuitylib.core.shape import Shape
from acuitylib.core.dtype import DType
from acuitylib.pytorch_art import torch
from acuitylib.core.backend_pytorch_fx import register_op_adapter, OpAdapter, TorchDequantizeWrapper,\
    TorchQuantizeWrapper
from acuitylib.xtf import xtf as tf
from acuitylib.acuitylog import AcuityLog as al
from acuitylib.layer.layer_params import DefParam
from acuitylib.acuity_runtime import art_graph
import numpy as np


class ArgMax(CustomLayer):

    op = 'argmax'

    # label, description
    def_input  = [IoMap('in0', 'in', 'input port')]
    def_output = [IoMap('out0', 'out', 'output port')]

    def_param = [
        DefParam('output_type', DType.int64, False),
        DefParam('keepdims', False, False),
    ]

    def setup(self, inputs, outputs):
        in_shape = inputs[0].shape.dims
        out_shape = copy.deepcopy(in_shape)
        axis = self.params.axis
        if axis < 0:
            axis = len(in_shape) + axis
            setattr(self.params, 'axis', axis)
        if self.params.keepdims is False:
            out_shape.remove(in_shape[self.params.axis])
        else:
            out_shape[self.params.axis] = 1
        outputs[0].shape = Shape(out_shape)

    def load_params_from_caffe(self, cl):
        p = dict()
        p['axis'] = cl.argmax_param.axis
        self.set_params(p)

    def load_params_from_tf(self, ruler, layer_alias, op_alias_map, tensor_data_map, anet=None):
        p = dict()
        p['axis'] = int(tensor_data_map['C:out0'])
        self.set_params(p)

    def load_params_from_onnx(self, node):
        p = dict()
        p['axis'] = 0
        if 'axis' in node.params:
            p['axis'] = node.params['axis']
        if 'keepdims' in node.params and node.params['keepdims'] == 1:
            p['keepdims'] = True
        else:
            p['keepdims'] = False
        if 'select_last_index' in node.params and node.params['select_last_index'] == 1:
            al.w("Acuity don't support the select_last_index = ture")
        self.set_params(p)

    def compute_out_tensor(self, tensor, input_tensor):
        p = self.params
        output_type = DType.map_to_backend_dtype(p.output_type, 'tensorflow')
        out = tf.argmax(input_tensor[0], self.params.axis, output_type=output_type)
        if p.keepdims is True:
            out = tf.reshape(out, self.get_out_shape().dims)
        return [out]

    def compute_out_type(self):
        p = self.params
        self.get_output(0).type = p.output_type

    def compute_art_tensor(self, tensor, input_tensor):
        p = self.params
        out = art_graph.Argmax(input_tensor[0], p.axis, p.keepdims, name=self.lid)
        return [out]

    def compute_torch_tensor(self, tensor, input_tensor):
        p = self.params
        out = torch.argmax(input_tensor[0], self.params.axis, p.keepdims)
        return [out]

@register_op_adapter
class ArgMaxAdapter(OpAdapter):
    OP_NAME = ArgMax.op

    def __init__(self, layer: ArgMax) -> None:
        super().__init__(layer)
        params = layer.params
        self.axis = params.axis
        self.keepdims = params.keepdims

        self.input_dq = TorchDequantizeWrapper(layer.inputs[0].quant_param)
        self.output_q = TorchQuantizeWrapper(layer.outputs[0].quant_param)

    def compute_torch_tensor(self, tensor, input_tensor):
        out = torch.argmax(input_tensor[0], self.axis, self.keepdims)
        return [out]

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.input_dq(x)
        y = torch.argmax(x, self.axis, self.keepdims)
        y = self.output_q(y)
        return y