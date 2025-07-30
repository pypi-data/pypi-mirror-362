"""V2 Dataplane protocol for ML services.

See
 * [Open Inference Protocol](
    https://github.com/kserve/open-inference-protocol/tree/main
   )

"""

from typing import NotRequired, Required, TypedDict, Union

from .common import DataType, Parameters, Scalar

Tensor = list[Union[Scalar, "Tensor"]]


class TensorData(TypedDict):
    """Named tensor data."""

    name: Required[str]
    shape: Required[list[int]]
    datatype: Required[DataType]
    parameters: NotRequired[Parameters]
    data: Required[Tensor]


class TensorRef(TypedDict):
    """Reference to a named tensor argument."""

    name: str
    parameters: NotRequired[Parameters]


class V2Request(TypedDict):
    """A V2 inference request."""

    id: NotRequired[str]
    parameters: NotRequired[Parameters]
    inputs: Required[list[TensorData]]
    outputs: NotRequired[list[TensorRef]]


class V2Response(TypedDict):
    """A V2 inference data response."""

    id: NotRequired[str]
    model_name: Required[str]
    model_version: NotRequired[str]
    parameters: NotRequired[Parameters]
    outputs: Required[list[TensorData]]


class V2ErrorResponse(TypedDict):
    """A V2 inference error response."""

    error: Required[str]
