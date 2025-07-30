"""Types related to model loading."""

import io
from abc import abstractmethod
from pathlib import Path
from typing import Generic, Protocol, Self, TypeVar

from .data.common import Parameters

AssetLocation = Path
AssetLocationLike = Path | str
AssetSource = AssetLocationLike | io.IOBase


def as_location(location: AssetLocationLike | None) -> AssetLocation:
    """Parse a location specification as location path."""
    return Path(location or ".")


#: Model Instance Type Variable
MI = TypeVar("MI")
#: Native Model Inference Request
MREQ = TypeVar("MREQ", contravariant=True)
#: Native Model Inference Response
MRES = TypeVar("MRES", covariant=True)
#: Marshalled Model Inference Request
RREQ = TypeVar("RREQ")
#: Marshalled Model Inference Response
RRES = TypeVar("RRES")

#: Native Model Scalar or Tensor representation
V = TypeVar("V")
#: Dicts of Scalar or Tensor
VDict = dict[str, V]
#: Scalar or Tensor or Dicts of it.
VorDict = V | VDict


class AsyncModelInvoker(Protocol, Generic[MREQ, MRES]):
    """Protocol for model invocation."""

    @abstractmethod
    async def __call__(self, req: MREQ, *args: MREQ, **kwargs) -> MRES:
        """Signature for model invocation."""


class AsyncModelInvokerWithParams(Protocol, Generic[MREQ, MRES]):
    """Protocol for a model invocation with output parameters."""

    @abstractmethod
    async def __call__(
        self, req: MREQ, *args: MREQ, **kwargs
    ) -> tuple[MRES, Parameters]:
        """Signature for a model invocation with output parameters."""


class SyncModelInvoker(Protocol, Generic[MREQ, MRES]):
    """Protocol for model invocation."""

    @abstractmethod
    def __call__(self, req: MREQ, *args: MREQ, **kwargs) -> MRES:
        """Signature for model invocation."""


class SyncModelInvokerWithParams(Protocol, Generic[MREQ, MRES]):
    """Protocol for a model invocation with output parameters."""

    @abstractmethod
    def __call__(self, req: MREQ, *args: MREQ, **kwargs) -> tuple[MRES, Parameters]:
        """Signature for a model invocation with output parameters."""


class AsyncSerializableModel(Protocol):
    """Protocol for a model that provides its own serialization."""

    @abstractmethod
    async def save(self: Self, location: AssetLocation, **kwargs):
        """Signature for save the model instance."""

    @classmethod
    @abstractmethod
    async def load(cls: type[Self], location: AssetLocation, **kwargs) -> Self:
        """Signature to load the model instance."""


class SyncSerializableModel(Protocol):
    """Protocol for a model that provides its own serialization."""

    @abstractmethod
    def save(self: Self, location: AssetLocation, **kwargs):
        """Signature for save the model instance."""

    @classmethod
    @abstractmethod
    def load(cls: type[Self], location: AssetLocation, **kwargs) -> Self:
        """Signature to load the model instance."""


SerializableModel = AsyncSerializableModel | SyncSerializableModel


ModelInvoker = (
    AsyncModelInvoker[MREQ, MRES]
    | AsyncModelInvokerWithParams[MREQ, MRES]
    | SyncModelInvoker[MREQ, MRES]
    | SyncModelInvokerWithParams[MREQ, MRES]
)
