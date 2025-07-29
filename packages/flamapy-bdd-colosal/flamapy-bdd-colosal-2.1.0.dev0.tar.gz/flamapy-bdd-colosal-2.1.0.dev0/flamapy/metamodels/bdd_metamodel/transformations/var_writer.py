from flamapy.core.transformations import ModelToText
from flamapy.metamodels.fm_metamodel.models import FeatureModel


class VarWriter(ModelToText):
    """Variable writer for feature models."""

    @staticmethod
    def get_destination_extension() -> str:
        return 'var'

    def __init__(self, path: str, source_model: FeatureModel):
        self.path: str = path
        self.source_model: FeatureModel = source_model

    def transform(self) -> str:
        with open(self.path, 'w', encoding='utf8') as file:
            str_vars = ' '.join(feature.name for feature in self.source_model.get_features())
            file.write(str_vars)
        return str_vars