import os
import importlib
''' !!!IMPORTANT!! The old torch include a onnx shared lib,
    it will cause segment fault if global onnx version doesn't match
    the torch onnx version, so acuity have to import onnx before torch.
    https://github.com/onnx/onnx/issues/2394
'''
onnx = importlib.import_module('onnx')
''' !!!IMPORTANT!! The torch import maybe hanged after tensorflow import,
    so acuity should firstly import torch
'''
try:
    torch = importlib.import_module('torch')
except ImportError:
    pass
from acuitylib.optimize.optimizer import Optimizer
from acuitylib.netwalker import NetWalker
from acuitylib.acuitylog import AcuityLog as Log
from acuitylib.acuitynet import AcuityNet as Net
from acuitylib.acuitynet import AcuityNet as AcuityModel
from acuitylib.acuitynetbuilder import AcuityNetBuilder as Builder
from acuitylib.client import Client as Client
from acuitylib.train.train import Train
import acuitylib.train as train
from acuitylib.xtf import xtf, xrnn
''' Export postprocess
'''
from acuitylib.app.medusa.postprocess.postprocess import PostProcess

def get_version():
    from acuitylib.utils import get_acuity_path, is_binary_package
    if is_binary_package():
        Log.w("Acuity binary version will reach end-of-life by Q4 2023, please use wheel version alternatively!")
        acuity_version_path = os.path.join(get_acuity_path(), 'VERSION')
    else:
        acuity_version_path = os.path.join(get_acuity_path(), 'acuitylib', 'VERSION')
    try:
        with open(acuity_version_path, 'r') as f:
            version = f.readlines()[0].strip('\n')
        return version
    except:
        return None

__version__ = get_version()
