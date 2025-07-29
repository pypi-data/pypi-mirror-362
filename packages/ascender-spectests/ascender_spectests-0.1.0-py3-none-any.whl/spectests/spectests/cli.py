from typing import Annotated
from ascender.core.cli import GenericCLI
from ascender.core import Inject
from ascender.core.cli.main import console_command, OptionCMD, ContextApplication
from unittest import TestSuite, TextTestRunner

from spectests.utils.spec_iter import flatten_specifications


class SpecTestsCLI(GenericCLI):
    app_name = "tests"
    
    def __init__(
        self, 
        specifications: Annotated[list[list[TestSuite]] | list[TestSuite], Inject("ASC_SPEC_TESTS")]
    ) -> None:
        self.specifications = flatten_specifications(specifications)
    
    @console_command(name="start", help="Run the ascender specification tests. Defined by provider")
    def start(
        self, 
        ctx: ContextApplication,
        specific: str | None = OptionCMD(default=None, required=False),
        descriptions: bool = OptionCMD(default=True, required=False),
        verbosity: int = OptionCMD(default=1, ctype=int, required=False),
        failfast: bool = OptionCMD(default=False, required=False)
    ) -> None:
        ctx.console_print("[cyan]Starting the ascender specification tests...[/cyan]")
        runner = TextTestRunner(descriptions=descriptions, verbosity=verbosity, failfast=failfast)

        for suite in self.specifications:
            ctx.console_print(f"[cyan]Loading suite: {suite.__class__.__name__}[/cyan]")
            if specific is not None and specific != suite.name:
                continue

            ctx.console_print(f"[cyan]Running suite: {suite.__class__.__name__}[/cyan]")
            runner.run(suite)