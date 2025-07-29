from typing import TYPE_CHECKING
from ascender.core.di.injector import AscenderInjector

if TYPE_CHECKING:
    from spectests.decorators.testcase import TestingCase


class AscSpecificationInterface:
    _injector: AscenderInjector | None

    __asc_module__: "TestingCase"

    @property
    def injector(self) -> AscenderInjector:
        assert self._injector
        return self._injector