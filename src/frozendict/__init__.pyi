from __future__ import annotations

from typing import Optional, TypeVar, Union, overload

try:
    from typing import Iterable, Iterator, Mapping, Tuple, Type
except ImportError:
    from collections.abc import Iterable, Iterator, Mapping

    Tuple = tuple
    Type = type

K = TypeVar("K")
V = TypeVar("V", covariant=True)
K2 = TypeVar("K2")
V2 = TypeVar("V2")
SelfT = TypeVar("SelfT")

class frozendict(Mapping[K, V]):
    @overload
    def __new__(cls: Type[SelfT]) -> SelfT: ...
    @overload
    def __new__(cls, **kwargs: V) -> frozendict[str, V]: ...
    @overload
    def __new__(cls: Type[SelfT], mapping: Mapping[K, V]) -> SelfT: ...
    @overload
    def __new__(cls: Type[SelfT], iterable: Iterable[Tuple[K, V]]) -> SelfT: ...
    def __getitem__(self, key: K) -> V: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[K]: ...
    def __hash__(self) -> int: ...
    def __reversed__(self) -> Iterator[K]: ...
    def copy(self: SelfT) -> SelfT: ...
    def __copy__(self: SelfT) -> SelfT: ...
    def __deepcopy__(self: SelfT) -> SelfT: ...
    def delete(self: SelfT, key: K) -> SelfT: ...
    def key(self, index: int) -> K: ...
    def value(self, index: int) -> V: ...
    def item(self, index: int) -> Tuple[K, V]: ...
    def __or__(
        self, other: Mapping[K2, V2]
    ) -> frozendict[Union[K, K2], Union[V, V2]]: ...
    def set(self, key: K2, value: V2) -> frozendict[Union[K, K2], Union[V, V2]]: ...
    def setdefault(
        self, key: K2, default: V2
    ) -> frozendict[Union[K, K2], Union[V, V2]]: ...
    @classmethod
    def fromkeys(
        cls: Type[SelfT], 
        seq: Iterable[K], 
        value: Optional[V] = None
    ) -> SelfT: ...

FrozenOrderedDict = frozendict
