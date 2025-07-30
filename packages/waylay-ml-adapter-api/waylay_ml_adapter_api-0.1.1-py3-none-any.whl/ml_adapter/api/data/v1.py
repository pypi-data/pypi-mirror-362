"""V1 Dataplane protocol for ML services.

See
 * [KServe V1](https://kserve.github.io/website/master/modelserving/data_plane/v1_protocol/)
 * [Tensorflow V1](https://www.tensorflow.org/tfx/serving/api_rest#predict_api)
"""

from typing import Any, NotRequired, Required, TypedDict, Union

from . import common as C


class EncodedBinaryValue(TypedDict):
    """Encoded binary value."""

    b64: Required[str]


ScalarOrBinaryValue = C.Scalar | EncodedBinaryValue

Tensor = list[Union[ScalarOrBinaryValue, "Tensor"]]
ValueOrTensor = ScalarOrBinaryValue | Tensor
NamedValues = dict[str, ValueOrTensor]
RowData = ValueOrTensor | list[NamedValues]
ColumnData = ValueOrTensor | NamedValues


class V1Request(TypedDict):
    """V1 Inference Request."""

    # row format
    instances: NotRequired[RowData]
    # columnar format
    inputs: NotRequired[ColumnData]
    # signature selection
    signature_name: NotRequired[str]
    parameters: NotRequired[C.Parameters]


class V1PredictionResponse(TypedDict):
    """V1 Predictions Response."""

    predictions: NotRequired[RowData]
    outputs: NotRequired[ColumnData]
    parameters: NotRequired[C.Parameters]


class V1ErrorResponse(TypedDict):
    """V1 Error Response."""

    error: Required[str]


def is_binary(value: Any, datatype: C.DataType | None = None, **_kwargs):
    """Check whether a v1 value is a -(tensor of) b64 encoded binary values.

    The first element from the flattened list provides evidence.
    """
    if isinstance(value, list):
        return len(value) > 0 and is_binary(value[0], datatype=datatype)
    if isinstance(value, bytes):
        return True
    if isinstance(value, dict) and "b64" in value:
        return True
    return isinstance(value, str) and datatype == C.DataTypes.BYTES
