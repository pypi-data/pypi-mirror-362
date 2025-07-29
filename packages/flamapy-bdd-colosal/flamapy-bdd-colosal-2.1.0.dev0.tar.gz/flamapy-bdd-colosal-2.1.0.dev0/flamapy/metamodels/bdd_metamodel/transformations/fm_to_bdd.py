import os
import copy
import pathlib
import tempfile

from flamapy.core.transformations import ModelToModel
from flamapy.core.exceptions import FlamaException
from flamapy.metamodels.fm_metamodel.models import FeatureModel
from flamapy.metamodels.fm_metamodel.transformations import (
    FMSecureFeaturesNames,
    FlatFM
)
from flamapy.metamodels.fm_metamodel.transformations.refactorings import (
    FeatureCardinalityRefactoring
)
from flamapy.metamodels.bdd_metamodel.models import BDDModel
from flamapy.metamodels.bdd_metamodel.transformations.pl_writer import PLWriter
from flamapy.metamodels.bdd_metamodel.transformations.var_writer import VarWriter


tempfile.tempdir = '/tmp'
LOGIC2BDD_BIN = 'logic2bdd'
MIN_NODES = 100000
LINE_LENGTH = 50
CONSTRAINT_REORDER = 'minspan'


class FmToBDD(ModelToModel):

    @staticmethod
    def get_source_extension() -> str:
        return 'fm'

    @staticmethod
    def get_destination_extension() -> str:
        return 'bdd'

    def __init__(self, source_model: FeatureModel) -> None:
        self.source_model = source_model
        self.bdd_model = BDDModel()

    def transform(self) -> BDDModel:
        # FlatFM if the feature model contains imports
        feature_model = self.source_model
        if feature_model.imports:
            feature_model = FlatFM(feature_model).transform()
        # Apply the feature cardinality refactoring to the source model
        if FeatureCardinalityRefactoring(feature_model).is_applicable():
            feature_model = copy.deepcopy(feature_model)
            feature_model = FeatureCardinalityRefactoring(feature_model).transform()

        # Secure the features names and create a mapping with the original names
        fmsfn = FMSecureFeaturesNames(feature_model)
        secure_fm = fmsfn.transform()
        mapping_names = fmsfn.mapping_names
        self.bdd_model.mapping_names = mapping_names

        # Create the var file
        self.bdd_model.var_file = create_var_file(secure_fm)

        # Create the exp file
        self.bdd_model.exp_file = create_exp_file(secure_fm)

        # Build the BDD
        self.bdd_model.bdd_file = build_bdd(self.bdd_model,
                                            self.bdd_model.var_file,
                                            self.bdd_model.exp_file)
        return self.bdd_model


def create_var_file(source_model: FeatureModel) -> str:
    """Create the var file from the source model."""
    fd, path = tempfile.mkstemp(suffix='.' + VarWriter.get_destination_extension())
    os.close(fd) 
    VarWriter(path=path, source_model=source_model).transform()
    return path
    

def create_exp_file(source_model: FeatureModel) -> str:
    """Create the exp file from the source model."""
    fd, path = tempfile.mkstemp(suffix='.' + PLWriter.get_destination_extension())
    os.close(fd) 
    PLWriter(path=path, source_model=source_model).transform()
    return path


def build_bdd(bdd_model: BDDModel, 
              varfile: str, 
              expfile: str) -> str:
    """Build the BDD using the given variables, expressions and order files."""
    path = pathlib.Path(varfile)
    filename = path.stem
    output_file = f'{tempfile.tempdir}/{filename}.dddmp'
    _, stderr = bdd_model.run(LOGIC2BDD_BIN, 
                              '-line-length', str(LINE_LENGTH),
                              '-min-nodes', str(MIN_NODES), 
                              '-constraint-reorder', CONSTRAINT_REORDER,
                              '-out', output_file,
                              varfile, 
                              expfile)
    if not pathlib.Path(output_file).exists():
        raise FlamaException(f'Error in FM2BDD transformation building the BDD: {stderr}')
    return output_file