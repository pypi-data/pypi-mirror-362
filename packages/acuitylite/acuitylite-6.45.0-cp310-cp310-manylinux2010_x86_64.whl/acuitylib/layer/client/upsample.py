from acuitylib.layer.customlayer import CustomLayer
from acuitylib.layer.acuitylayer import IoMap
from acuitylib.core.shape import Shape
from acuitylib.xtf import xtf as tf
from acuitylib.acuitylog import AcuityLog as al

class Upsample(CustomLayer):

    op = 'upsample'

    # label, description

    def_output = [IoMap('out0', 'out', 'output port')]

    def_input = []

    def _norm_upsample_param(self, height, width):
        p = self.params
        if p.upsample_inputs_num == 2:
            if p.scale != 0:
                scale_h = p.scale
                scale_w = p.scale
            else:
                scale_h = getattr(p, 'scale_h', 0)
                scale_w = getattr(p, 'scale_w', 0)
            pad_h = int(getattr(p, 'pad_h', 0))
            pad_w = int(getattr(p, 'pad_w', 0))
            if p.upsample_h == 0:
                upsample_h = height * scale_h - pad_h
                setattr(p, 'upsample_h', upsample_h)
            if p.upsample_w == 0:
                upsample_w = width * scale_w - pad_w
                setattr(p, 'upsample_w', upsample_w)

    def setup(self, inputs, outputs):
        p = self.params
        if p.upsample_inputs_num == 2:
            in_shape = inputs[0].shape.dims
            if self.net.get_platform_mode() == 'nchw':
                self._norm_upsample_param(in_shape[2], in_shape[3])
                out_shape = [in_shape[0], in_shape[1], p.upsample_h, p.upsample_w]
            else:
                self._norm_upsample_param(in_shape[1], in_shape[2])
                out_shape = [in_shape[0], p.upsample_h, p.upsample_w, in_shape[-1]]
        if p.upsample_inputs_num == 1:
            in_shape = inputs[0].shape.dims
            if self.net.get_platform_mode() == 'nchw':
                in_weight = in_shape[3]
                in_height = in_shape[2]
                out_shape = [in_shape[0], in_shape[1], in_height*p.scale, in_weight*p.scale]
            else:
                in_weight = in_shape[2]
                in_height = in_shape[1]
                out_shape = [in_shape[0], in_height*p.scale, in_weight*p.scale, in_shape[-1]]

        outputs[0].shape = Shape(out_shape)

    def load_params_from_caffe(self, cl):
        if len(cl.bottom) == 1:
            p = dict()
            p['upsample_inputs_num'] = 1
            p['scale'] = cl.upsample_param.scale
            self.set_params(p)
        elif len(cl.bottom) == 2:
            p = dict()
            p['upsample_inputs_num'] = 2
            p['scale'] = cl.upsample_param.scale
            p['upsample_h'] = cl.upsample_param.upsample_h
            p['upsample_w'] = cl.upsample_param.upsample_w
            # DEPRECATED in caffe
            p['pad_h'] = getattr(cl.upsample_param, 'pad_out_h', False)
            p['pad_w'] = getattr(cl.upsample_param, 'pad_out_w', False)
            p['scale_h'] = getattr(cl.upsample_param, 'scale_h', 0)
            p['scale_w'] = getattr(cl.upsample_param, 'scale_w', 0)
            self.set_params(p)
        else :
            al.e('upsample only support 1 or 2 input .')


    def compute_out_tensor(self, tensor, input_tensor):
        p = self.params
        if p.upsample_inputs_num == 2:
            data = input_tensor[0]
            idx = input_tensor[1]

            out_shape = self.get_out_shape().dims
            out_shape[0] = data.get_shape().as_list()[0]
            sz = out_shape[0] * out_shape[1] * out_shape[2] * out_shape[3]

            data = tf.reshape(data, [-1])
            idx = tf.reshape(idx, [-1, 1])
            out = tf.scatter_nd(tf.cast(idx, tf.int64), data, [sz])
            real_out = tf.reshape(out, out_shape)

        if p.upsample_inputs_num == 1:
            scale = p.scale
            if (scale > 1):
                permute_shape_nchw_to_nhwc = [0, 2, 3, 1]
                permute_shape_nhwc_to_nchw = [0, 3, 1, 2]
                if self.net.get_platform_mode() == "nhwc":
                    compute_tensor = input_tensor[0]
                    out = tf.tile(compute_tensor, [1, 1, 1, scale * scale])
                    out = tf.compat.v1.depth_to_space(out, block_size=scale)
                    real_out = out
                elif self.net.get_platform_mode() == "nchw":
                    compute_tensor = tf.transpose(input_tensor[0], permute_shape_nchw_to_nhwc)
                    out = tf.tile(compute_tensor, [1, 1, 1, scale * scale])
                    out = tf.compat.v1.depth_to_space(out, block_size=scale)
                    real_out = tf.transpose(out, permute_shape_nhwc_to_nchw)
            else:
                real_out = input_tensor[0]

        return [real_out]


