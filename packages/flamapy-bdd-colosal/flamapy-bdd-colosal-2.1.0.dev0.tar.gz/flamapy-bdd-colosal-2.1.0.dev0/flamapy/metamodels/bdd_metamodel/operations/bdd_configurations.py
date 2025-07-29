import re
from typing import Any, cast

from flamapy.core.models import VariabilityModel
from flamapy.core.operations import Configurations
from flamapy.core.exceptions import FlamaException
from flamapy.metamodels.configuration_metamodel.models import Configuration
from flamapy.metamodels.bdd_metamodel.models import BDDModel


GEN_PRODUCTS_BIN = 'genProducts'


class BDDConfigurations(Configurations):

    def __init__(self) -> None:
        self.result: list[Any] = []

    def execute(self, model: VariabilityModel) -> 'BDDConfigurations':
        bdd_model = cast(BDDModel, model)
        self.result = configurations(bdd_model)
        return self

    def get_result(self) -> list[Any]:
        return self.result

    def get_configurations(self) -> list[Any]:
        return self.get_result()


def configurations(bdd_model: BDDModel) -> list[Any]:
    stdout, stderr = bdd_model.run(GEN_PRODUCTS_BIN, bdd_model.bdd_file)
    if not stdout:
        raise FlamaException(f"Couldn't generate products: {stderr}")
    line_iterator = iter(stdout.splitlines())
    configurations = []
    for line in line_iterator:
        parsed_line = re.compile(r'\s+').split(line)
        configuration = {}
        negation = False
        for element in parsed_line:
            if element != "":
                if element == "not":
                    negation = True
                else:
                    configuration[bdd_model.mapping_names_inv.get(element)] = not negation
                    negation = False
        configurations.append(Configuration(configuration))
    return configurations
