"""Common data API definitions."""

from typing import Literal, Union

Scalar = str | bool | float | int
Tensor = list[Union[Scalar, "Tensor"]]

Parameters = dict[str, Scalar]
DataType = Literal[
    "BOOL",
    "UINT8",
    "UINT16",
    "UINT32",
    "UINT64",
    "INT8",
    "INT16",
    "INT32",
    "INT64",
    "FP16",
    "FP32",
    "FP64",
    "BYTES",
]


class DataTypes:
    """DataType constants."""

    DEFAULT = "FP64"
    FP32 = "FP32"
    BYTES = "BYTES"


ScalarOrBytes = Scalar | bytes
Tensor = list[Union[ScalarOrBytes, "Tensor"]]
ScalarOrTensor = ScalarOrBytes | Tensor
NamedScalarOrTensors = dict[str, ScalarOrTensor]
NamedTensors = dict[str, Tensor]

ScalarTensorOrNamed = ScalarOrBytes | NamedScalarOrTensors

BytesTensor = list[Union[bytes, "BytesTensor"]]
BytesOrBytesTensor = bytes | BytesTensor

InferenceProtocol = Literal["KServe-1.0"] | Literal["OIP-2.0"] | Literal["N/A"]

V1_PROTOCOL: InferenceProtocol = "KServe-1.0"
V2_PROTOCOL: InferenceProtocol = "OIP-2.0"
NO_PROTOCOL: InferenceProtocol = "N/A"
