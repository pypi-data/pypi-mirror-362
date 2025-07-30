"""
Functions to convert CoreMessages.AnyArray to and from numpy arrays
"""

import numpy as np

from .CoreMessages_pb2 import AnyArray

__all__ = [
    "any_array_to_numpy",
    "numpy_to_any_array",
]

ANY_ARRAY_TYPE_TO_NUMPY_TYPE = {
    AnyArray.S8: np.int8,
    AnyArray.U8: np.uint8,
    AnyArray.S16: np.int16,
    AnyArray.U16: np.uint16,
    AnyArray.S32: np.int32,
    AnyArray.U32: np.uint32,
    AnyArray.S64: np.int64,
    AnyArray.U64: np.uint64,
    AnyArray.FLOAT: np.float32,
    AnyArray.DOUBLE: np.float64,
    AnyArray.BOOL: np.bool_,
    AnyArray.NONE: np.void,
}

DTYPE_TO_ANYARRAY_TYPE = {v: k for k, v in ANY_ARRAY_TYPE_TO_NUMPY_TYPE.items()}


def any_array_to_numpy(any_array):
    """Convert protobuf AnyArray to numpy array"""
    if any_array.type == AnyArray.NONE:
        if any_array.data:
            raise ValueError("any_array has no type", any_array)
        else:
            return np.array([], dtype=np.void)

    return np.frombuffer(any_array.data, ANY_ARRAY_TYPE_TO_NUMPY_TYPE[any_array.type])


def numpy_to_any_array(array):
    """Convert numpy array to AnyArray"""
    try:
        type_ = DTYPE_TO_ANYARRAY_TYPE[array.dtype.type]
    except KeyError:
        raise TypeError(f"Unsupported dtype for anyarray: {array.dtype}")
    data = np.ascontiguousarray(array).tobytes()
    return AnyArray(type=type_, data=data)
