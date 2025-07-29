import re
from typing import Any, Optional, cast

from flamapy.core.models import VariabilityModel
from flamapy.core.exceptions import FlamaException
from flamapy.metamodels.configuration_metamodel.models import Configuration
from flamapy.metamodels.bdd_metamodel.models import BDDModel
from flamapy.metamodels.bdd_metamodel.operations.interfaces import FeatureInclusionProbability


FEATURE_PROBABILITIES_BIN = 'feature_probabilities'


class BDDFeatureInclusionProbability(FeatureInclusionProbability):
    """Computes the probability each model feature has to be included in a valid product.

    That is, for every feature it returns the number of valid products with the feature activated
    divided by the total number of valid products 
    (a product is valid if it satisfies all model constraints).

    For detailed information, see the paper: 
    Heradio, R., Fernandez-Amoros, D., Mayr-Dorn, C., Egyed, A.:
    Supporting the statistical analysis of variability models. 
    In: 41st International Conference on Software Engineering (ICSE), pp. 843-853. 
    Montreal, Canada (2019).

    The operation also support a feature_assignment: a list with a partial or a complete features' 
    assignment (e.g., ["f1", "not f3", "f5"]).

    Return a dictionary with the format 
    {feature_1: feature_1_probability, feature_2: feature_2_probability, ...}
    """

    def __init__(self) -> None:
        self.result: dict[Any, float] = {}
        self.partial_configuration: Optional[Configuration] = None
        self.precision = 4

    def set_partial_configuration(self, partial_configuration: Configuration) -> None:
        self.partial_configuration = partial_configuration

    def set_precision(self, precision: int) -> None:
        self.precision = precision

    def get_result(self) -> dict[Any, float]:
        return self.result

    def feature_inclusion_probability(self) -> dict[Any, float]:
        return self.get_result()

    def execute(self, model: VariabilityModel) -> 'BDDFeatureInclusionProbability':
        bdd_model = cast(BDDModel, model)
        self.result = feature_inclusion_probabilities(bdd_model, self.precision,
                                                      self.partial_configuration)
        return self


def feature_inclusion_probabilities(bdd_model: BDDModel, 
                                    precision: int,
                                    partial_configuration: Optional[Configuration] = None
                                    ) -> dict[Any, float]:
    """
    Computes the featue inclusion probabilities.
        :param feature_assignment: a list with a partial or a complete features' assignment
               (e.g., ["f1", "not f3", "f5"])
        :return: The feature inclusion probabilities.
    """
    if partial_configuration is not None:
        partial_configuration = secure_feature_names(bdd_model, partial_configuration)
        result = feature_inclusion_probability(bdd_model, precision,
                                               [str(f) if selected else f'not {f}' 
                                                for f, selected in 
                                                partial_configuration.elements.items()])
    else:
        result = feature_inclusion_probability(bdd_model, precision)
    return result


def feature_inclusion_probability(bdd_model: BDDModel,
                                  precision: int,
                                  feature_assignment: Optional[list[str]] = None
                                  ) -> dict[Any, float]:
    assert bdd_model.bdd_file is not None
    
    if feature_assignment is None:
        stdout, stderr = bdd_model.run(FEATURE_PROBABILITIES_BIN, bdd_model.bdd_file)
    else:
        expanded_assignment = BDDModel.expand_assignment(bdd_model.bdd_file, feature_assignment)
        stdout, stderr = bdd_model.run(FEATURE_PROBABILITIES_BIN,
                                       *expanded_assignment, 
                                       bdd_model.bdd_file)
    if not stdout:
        raise FlamaException(f"Couldn't calculate the feature inclusion probabilities: {stderr}")
    line_iterator = iter(stdout.splitlines())
    probabilities = {}
    for line in line_iterator:
        parsed_line = re.compile(r'\s+').split(line.strip())
        original_feature_name = bdd_model.mapping_names_inv.get(parsed_line[0])
        probabilities[original_feature_name] = round(float(parsed_line[1]), precision)
    return probabilities


def secure_feature_names(bdd_model: BDDModel, configuration: Configuration) -> Configuration:
    elements = {}
    for elem, selected in configuration.elements.items():
        elements[bdd_model.mapping_names[elem]] = selected 
    return Configuration(elements)