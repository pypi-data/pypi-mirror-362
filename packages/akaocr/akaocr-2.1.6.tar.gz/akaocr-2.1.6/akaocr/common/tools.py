# Writer: LauNT - 07/2025 - akaOCR Team

import onnxruntime as ort
import copy

from .det_postprocess import DetPostProcess
from .rec_postprocess import CTCLabelDecode
from .rot_postprocess import ClsPostProcess


def build_post_process(config, global_config=None):
    # Post-processing for recognition model
    
    support_dict = [
        'CTCLabelDecode', 'DetPostProcess', 'ClsPostProcess'
    ]
    config = copy.deepcopy(config)
    module_name = config.pop('name')

    if global_config is not None:
        config.update(global_config)
    assert module_name in support_dict, Exception(
        'Post process only support {}'.format(support_dict))
    module_class = eval(module_name)(**config)

    return module_class


def prepare_inference_session(device='cpu'):
    # Create session options

    so = ort.SessionOptions()
    so.add_session_config_entry('session.dynamic_block_base', '4')
    so.enable_cpu_mem_arena = True
    so.inter_op_num_threads = 1
    so.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL

    if device == 'gpu':
        # configure GPU settings
        providers=[
        ("CUDAExecutionProvider", {"cudnn_conv_algo_search": "DEFAULT"}),
        "CPUExecutionProvider"
    ]
    else:
        # configure CPU settings
        providers = ['CPUExecutionProvider']

    return so, providers


def create_predictor(model_path, device='cpu'):
    # Create a predictor for ONNX model inference.

    so, providers = prepare_inference_session(device)

    # create the ONNX Runtime inference session
    sess = ort.InferenceSession(
        model_path, sess_options=so, providers=providers)

    return sess, sess.get_inputs()[0], None