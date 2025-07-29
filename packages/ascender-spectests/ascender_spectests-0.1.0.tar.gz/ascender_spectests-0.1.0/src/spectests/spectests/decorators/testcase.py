from ascender.core.struct.module_ref import AscModuleRef
from ascender.core.struct.controller_ref import ControllerRef
from ascender.core.struct.module import AscModule
from ascender.core import Provider


class TestingCase(AscModule):
    
    def __init__(
        self,
        imports: list[type[AscModuleRef] | type[ControllerRef]] = [],
        providers: list[Provider] = []
    ):
        super().__init__(imports=imports, declarations=[], providers=providers, exports=[])