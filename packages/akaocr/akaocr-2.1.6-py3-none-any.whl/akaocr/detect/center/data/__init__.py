# Writer: LauNT - 07/2025 - akaOCR Team

from .data import ToCHWImage
from .data import KeepKeys
from .data import NormalizeImage
from .data import DetResize


def transform(data, ops=None):
    # Data transformation

    if ops is None:
        ops = []
    for op in ops:
        data = op(data)
        if data is None:
            return None
    return data


def create_operators(op_param_list, global_config=None):
    # Create operators based on the config

    assert isinstance(op_param_list, list), (
        f"TypeError: {type(op_param_list)} != list."
    )
    ops = []

    # create operators
    for operator in op_param_list:
        assert isinstance(operator, dict) and len(operator) == 1, (
            f"ConfigError: {operator} is wrong."
        )
        op_name = list(operator)[0]
        param = {} if operator[op_name] is None else operator[op_name]

        if global_config is not None:
            param.update(global_config)
        
        op = eval(op_name)(**param)
        ops.append(op)

    return ops
