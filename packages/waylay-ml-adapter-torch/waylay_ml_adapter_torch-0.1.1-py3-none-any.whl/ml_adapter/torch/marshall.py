"""Pytorch ML Marshaller."""

import numpy.typing as npt

import ml_adapter.base.marshall.v1.base as V1B
import torch
from ml_adapter.api.data import common as C
from ml_adapter.api.data import v1 as V1
from ml_adapter.numpy.marshall import V1NumpyEncoding

TorchTensor = torch.Tensor
NamedArrays = dict[str, TorchTensor]
ArraysOrNamedArrays = TorchTensor | NamedArrays

TORCH_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

TORCH_DATA_TYPES: dict[C.DataType, torch.dtype] = {
    "BOOL": torch.bool,
    "INT8": torch.int8,
    "INT16": torch.int16,
    "INT32": torch.int32,
    "INT64": torch.int64,
    "UINT8": torch.uint8,
    "UINT16": torch.uint16,
    "UINT32": torch.uint32,
    "UINT64": torch.uint64,
    "FP16": torch.float16,
    "FP32": torch.float32,
    "FP64": torch.float64,
}

TORCH_DATA_TYPES_BY_NP: dict[str, torch.dtype] = {
    "bool": torch.bool,
    "int8": torch.int8,
    "int16": torch.int16,
    "int32": torch.int32,
    "int64": torch.int64,
    "uint8": torch.uint8,
    "uint16": torch.uint16,
    "uint32": torch.uint32,
    "uint64": torch.uint64,
    "float16": torch.float16,
    "float32": torch.float32,
    "float64": torch.float64,
    "complex32": torch.complex32,
    "complex64": torch.complex64,
    "complex128": torch.complex128,
}


def _as_torch_dtype(dtype: npt.DTypeLike | torch.dtype):
    dtype_name: str = ""
    if isinstance(dtype, torch.dtype):
        return dtype
    if isinstance(dtype, str):
        dtype_name = dtype
    elif hasattr(dtype, "name"):
        dtype_name = dtype.name
    elif hasattr(dtype, "__name__"):
        dtype_name = dtype.__name__
    try:
        return TORCH_DATA_TYPES_BY_NP[dtype_name]
    except KeyError as exc:
        raise ValueError(f"dtype not supported on torch: {dtype}") from exc


class V1TorchNativeEncoding(
    V1B.WithScalarEncoding, V1B.WithV1TensorEncoding[TorchTensor]
):
    """Encoding and decoding of v1 tensors to pytorch arrays."""

    def get_scalar_dtype(
        self,
        dtype: npt.DTypeLike | torch.dtype | None = None,
        datatype: C.DataType | None = None,
        **_kwargs,
    ) -> torch.dtype | None:
        """Get the scalar type for tensors."""
        if dtype is not None:
            return _as_torch_dtype(dtype)
        datatype = datatype or self.scalar_data_type
        if datatype is None:
            return None
        try:
            return TORCH_DATA_TYPES[datatype]
        except KeyError as exc:
            raise ValueError(f"Invalid datatype: {datatype}") from exc

    def decode(
        self,
        value: V1.ValueOrTensor,
        dtype: npt.DTypeLike | None = None,
        datatype: C.DataType | None = None,
        **kwargs,
    ) -> TorchTensor:
        """Map a value tensor."""
        if V1.is_binary(value, datatype):
            raise ValueError("Torch models do not support binary data.")
        torch_dtype = self.get_scalar_dtype(dtype, datatype)
        if isinstance(value, torch.Tensor):
            if torch_dtype is None or value.dtype == torch_dtype:
                return value
            return value.type(torch_dtype).to(TORCH_DEVICE)
        return torch.tensor(value, dtype=torch_dtype).to(TORCH_DEVICE)

    def encode(self, data: TorchTensor, **kwargs) -> V1.ValueOrTensor:
        """Encode a pytorch array to a value or tensor."""
        return data.tolist()


class V1TorchNumpyEncoding(
    V1B.WithScalarEncoding, V1B.WithV1TensorEncoding[TorchTensor]
):
    """Encoding and decoding of v1 tensors to pytorch arrays via numpy."""

    # default scalar type, similar for default of torch.tensor(a_float_array)
    # note that numpy.array(a_float_array) default is FP64 ...
    # scalar_data_type = C.DataTypes.FP32

    _numpy: V1NumpyEncoding

    def __init__(self, *args, **kwargs):
        """Initialize."""
        self._numpy = V1NumpyEncoding()
        self.set_scalar_type(self.scalar_data_type)

    # @override
    def set_scalar_type(self, datatype: C.DataType | None):
        """Set default scalar type for tensors."""
        super().set_scalar_type(datatype)
        self._numpy.set_scalar_type(datatype)

    def decode(
        self,
        value: V1.ValueOrTensor,
        dtype: npt.DTypeLike | None = None,
        datatype: str | None = None,
        **kwargs,
    ) -> TorchTensor:
        """Map a value tensor, decoding binary data."""
        return torch.from_numpy(self._numpy.decode(value, dtype, datatype)).to(
            TORCH_DEVICE
        )

    def encode(self, data: TorchTensor, **kwargs) -> V1.ValueOrTensor:
        """Encode a pytorch array to a value or tensor."""
        force = kwargs.pop("force", False)
        return self._numpy.encode(data.detach().numpy(force=force), **kwargs)


class V1TorchMarshaller(
    V1B.V1ValueOrDictRequestMarshallerBase[TorchTensor],
    V1B.V1ValueOrDictResponseMarshallerBase[TorchTensor],
    V1TorchNativeEncoding,
):
    """Convert v1 payload from and to torch tensors."""
