from typing import Iterable, Literal, Type
from typing_extensions import TypedDict

from spectests.interfaces.specification import AscSpecificationInterface


class SpecSuite(TypedDict):
    type: Literal["specsuite"]
    spec: Type[AscSpecificationInterface]
    methods: Iterable[str]


class AutoSpec(TypedDict):
    type: Literal["autospec"]
    spec: Type[AscSpecificationInterface]