from typing import Optional, cast

from flamapy.core.models import VariabilityModel
from flamapy.core.operations import ConfigurationsNumber
from flamapy.core.exceptions import FlamaException
from flamapy.metamodels.configuration_metamodel.models import Configuration
from flamapy.metamodels.bdd_metamodel.models.bdd_model import BDDModel


COUNTER_BIN = 'counter'


class BDDConfigurationsNumber(ConfigurationsNumber):
    """It computes the number of solutions of the BDD model.

    It also supports counting the solutions from a given partial configuration.
    """

    def __init__(self) -> None:
        self.result: int = 0
        self.partial_configuration: Optional[Configuration] = None

    def set_partial_configuration(self, partial_configuration: Configuration) -> None:
        self.partial_configuration = partial_configuration

    def execute(self, model: VariabilityModel) -> 'BDDConfigurationsNumber':
        bdd_model = cast(BDDModel, model)
        self.result = configurations_number(bdd_model, self.partial_configuration)
        return self

    def get_result(self) -> int:
        return self.result

    def get_configurations_number(self) -> int:
        return self.get_result()


def configurations_number(bdd_model: BDDModel, 
                          partial_configuration: Optional[Configuration] = None) -> int:
    """
    Computes the number of valid configurations.
        :param feature_assignment: a list with a partial or a complete features' assignment
               (e.g., ["f1", "not f3", "f5"])
        :return: The number of valid configurations
    """
    if partial_configuration is not None:
        partial_configuration = secure_feature_names(bdd_model, partial_configuration)
        result = count(bdd_model, [str(f) if selected else f'not {f}' for f, selected in 
                                   partial_configuration.elements.items()])
    else:
        result = count(bdd_model)
    return result


def count(bdd_model: BDDModel, feature_assignment: Optional[list[str]] = None) -> int:
    """
    Computes the number of valid configurations.
        :param feature_assignment: a list with a partial or a complete features' assignment
                (e.g., ["f1", "not f3", "f5"])
        :return: The number of valid configurations
    """
    assert bdd_model.bdd_file is not None
    
    if feature_assignment is None:
        stdout, stderr = bdd_model.run(COUNTER_BIN, bdd_model.bdd_file)
    else:
        expanded_assignment = BDDModel.expand_assignment(bdd_model.bdd_file, feature_assignment)
        stdout, stderr = bdd_model.run(COUNTER_BIN, *expanded_assignment, bdd_model.bdd_file)
    if not stdout:
        raise FlamaException(f"Couldn't calculate the number of configurations: {stderr}")
    return int(stdout)


def secure_feature_names(bdd_model: BDDModel, configuration: Configuration) -> Configuration:
    elements = {}
    for elem, selected in configuration.elements.items():
        elements[bdd_model.mapping_names[elem]] = selected 
    return Configuration(elements)
