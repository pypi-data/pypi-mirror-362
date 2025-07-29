from acuitylib.layer.customlayer import CustomLayer
from acuitylib.layer.acuitylayer import IoMap
from acuitylib.core.shape import Shape
from acuitylib.xtf import xtf as tf
from acuitylib.acuitylog import AcuityLog as al
class Upsample2(CustomLayer):

    op = 'upsample2'

    # label, description

    def_output = [IoMap('out0', 'out', 'output port')]

    def_input = []

    def setup(self, inputs, outputs):
        p = self.params
        if p.upsampleinputsnum == 2:
            in_shape = self.get_input(0).shape.dims
            if self.net.get_platform_mode() == 'nchw':
                out_shape = [in_shape[0], in_shape[1], inputs[1].shape.dims[2], inputs[1].shape.dims[3]]
                setattr(p, 'realoutheight', inputs[1].shape.dims[2])
                setattr(p, 'realoutwidth', inputs[1].shape.dims[3])
            else:
                ##nhwc
                out_shape = [in_shape[0], inputs[1].shape.dims[2], inputs[1].shape.dims[3], in_shape[1]]
                setattr(p, 'realoutheight', inputs[1].shape.dims[2])
                setattr(p, 'realoutwidth', inputs[1].shape.dims[3])
        if p.upsampleinputsnum == 1:
            in_shape = inputs[0].shape.dims
            if self.net.get_platform_mode() == 'nchw':
                if hasattr(p, 'outh') and hasattr(p, 'outw'):
                    upsampleinputsnum = getattr(p,'outh')
                    out_width = getattr(p,'outw')
                    out_shape = [in_shape[0], in_shape[1], upsampleinputsnum, out_width]
                elif hasattr(p, 'heightscale') and hasattr(p, 'widthscale'):
                    upsampleinputsnum = getattr(p,'heightscale')*in_shape[2]
                    out_width = getattr(p,'widthscale') * in_shape[3]
                    out_shape = [in_shape[0], in_shape[1], upsampleinputsnum, out_width]
            else:
                ##nhwc
                if hasattr(p, 'outh') and hasattr(p, 'outw'):
                    upsampleinputsnum = getattr(p,'outh')
                    out_width = getattr(p,'outw')
                    out_shape = [in_shape[0],upsampleinputsnum, out_width, in_shape[3] ]
                if hasattr(p, 'heightscale') and hasattr(p, 'widthscale'):
                    upsampleinputsnum = getattr(p, 'heightscale') * in_shape[2]
                    out_width = getattr(p, 'widthscale') * in_shape[3]
                    out_shape = [in_shape[0],upsampleinputsnum, out_width, in_shape[1] ]
            setattr(p, 'realoutheight', upsampleinputsnum)
            setattr(p, 'realoutwidth', out_width)

        outputs[0].shape = Shape(out_shape)

    def load_params_from_caffe(self, cl):
        p = dict()
        p['realoutheight'] = 0
        p['realoutwidth'] = 0
        if len(cl.bottom) == 1:
            p['upsampleinputsnum'] = 1
            caffe_param = cl.upsample2_param
            p['mode'] = "BILINEAR"
            if hasattr(caffe_param, 'height') and hasattr(caffe_param, 'width') and \
                    (( caffe_param.height != 32 ) or ( caffe_param.width != 32 )) :
                p['outh'] = caffe_param.height
                p['outw'] = caffe_param.width
            elif  (( caffe_param.height == 32 ) and ( caffe_param.width == 32 )) and \
                    (caffe_param.height_scale ==2) and ( caffe_param.width_scale == 2 ) :
                p['outh'] = caffe_param.height
                p['outw'] = caffe_param.width
            elif hasattr(caffe_param, 'height_scale') and hasattr(caffe_param, 'width_scale')  and\
                    ( caffe_param.height == 32 ) and ( caffe_param.width == 32 )  :
                p['heightscale'] = caffe_param.height_scale
                p['widthscale'] = caffe_param.width_scale
            if ( caffe_param.mode == "NEAREST" ) or ( caffe_param.mode == 0 ) :
                p['mode'] = "NEAREST"
            self.set_params(p)
        elif len(cl.bottom) == 2:
            p['upsampleinputsnum'] = 2
            p['mode'] = "BILINEAR"
            caffe_param = cl.upsample2_param
            if ( caffe_param.mode == "NEAREST" ) or ( caffe_param.mode == 0):
                p['mode'] = "NEAREST"
            self.set_params(p)
        else :
            al.e('Upsample2 support two bottom or use (height and width)or (height_scale and width_scale)! .')
    def compute_out_tensor(self, tensor, input_tensor):
        ##nchw input,compute use nhwc
        p = self.params
        in_shape = self.get_input(0).shape.dims
        permute_shape_nchw_to_nhwc = [0, 2, 3, 1]
        permute_shape_nhwc_to_nchw = [0, 3, 1, 2]
        compute_tensor = tf.transpose(input_tensor[0], permute_shape_nchw_to_nhwc)
        if getattr(p,'upsampleinputsnum') == 2:
            in_shape1=self.get_input(1).shape.dims
            out_height = in_shape1[2]
            out_width = in_shape1[3]
            if getattr(p,'mode') == "BILINEAR":
                out = tf.compat.v1.image.resize_bilinear(compute_tensor, [out_height, out_width], False)
            if getattr(p,'mode') == "NEAREST":
                out = tf.compat.v1.image.resize_nearest_neighbor(compute_tensor, [out_height, out_width], False)
            out = tf.transpose(out, permute_shape_nhwc_to_nchw)

        if getattr(p,'upsampleinputsnum') == 1:
            if hasattr(p, 'outh') and hasattr(p, 'outw'):
                out_height = getattr(p,'outh')
                out_width = getattr(p,'outw')
            elif hasattr(p, 'heightscale') and hasattr(p, 'widthscale'):
                out_height = getattr(p,'heightscale')*in_shape[2]
                out_width = getattr(p,'widthscale') * in_shape[3]
            if getattr(p,'mode') == "BILINEAR":
                out = tf.compat.v1.image.resize_bilinear(compute_tensor, [out_height, out_width], False)
            if getattr(p,'mode') == "NEAREST":
                out = tf.compat.v1.image.resize_nearest_neighbor(compute_tensor, [out_height, out_width], False)
            out = tf.transpose(out, permute_shape_nhwc_to_nchw)
        return [out]
