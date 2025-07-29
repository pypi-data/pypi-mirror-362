from typing import cast
from unittest import TestSuite, TestCase, TestLoader
from spectests.interfaces.specification import AscSpecificationInterface
from ascender.core import Provider
from ascender.core.di.injector import Injector
from ascender.core.utils.module import load_module

from spectests.interfaces.spectypes import AutoSpec, SpecSuite


def provideSpecTests(*tests: SpecSuite | AutoSpec) -> Provider:
    def provider_factory(injector: Injector):
        suites: list[TestSuite] = []
        
        for test in tests:
            if not isinstance(test, dict):
                raise TypeError("Test must be a Mapping containing the specification test information")
            
            if test.get("type") == "specsuite":
                try:
                    specification_case = cast(type[TestCase], load_module(test["spec"]))
                except RuntimeError:
                    specification_case = cast(type[TestCase], test["spec"])
                
                suites.append(TestSuite([specification_case(testMethod) for testMethod in test["methods"]]))
            
            elif test.get("type") == "autospec":
                try:
                    specification_interface = cast(type[AscSpecificationInterface], load_module(test["spec"]))
                except RuntimeError:
                    specification_interface = cast(type[AscSpecificationInterface], test["spec"])
                suites.append(TestLoader().loadTestsFromTestCase(specification_interface))
        
        return suites
    
    return {
        "provide": "ASC_SPEC_TESTS",
        "use_factory": lambda i: provider_factory(i),
        "deps": [Injector],
        "multi": True
    }