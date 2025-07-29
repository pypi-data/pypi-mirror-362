import os
import re
import pathlib
import subprocess
from typing import Any

from flamapy.core.models import VariabilityModel
from flamapy.core.exceptions import FlamaException


class BDDModel(VariabilityModel):
    """A Binary Decision Diagram (BDD) representation of the feature model.

    It relies on the bdd4va library (https://github.com/rheradio/bdd4va).
    """

    LD_LIBRARY_PATH = 'LD_LIBRARY_PATH'

    @staticmethod
    def get_extension() -> str:
        return 'bdd'

    def __init__(self) -> None:
        """Initialize the BDD with the dddmp file.

        The BDD relies on a dddmp file that stores a feature model's BDD encoding (dddmp is the
        format that the BDD library CUDD uses; check https://github.com/vscosta/cudd)
        """
        self.bdd_file: str | None = None
        self.var_file: str | None = None
        self.exp_file: str | None = None
        self.sifting_file: str | None = None  # Variable ordering file (not used yet)
        self._mapping_names: dict[str, str] = {}  # Maps to maintain original features' names
        self._mapping_names_inv: dict[str, str] = {}
        self._bddbin_dir: str | None = None
        self._env: dict[str, str] = {}
        self._set_global_constants()

    @property
    def mapping_names(self) -> dict[str, str]:
        return self._mapping_names
    
    @mapping_names.setter
    def mapping_names(self, mapping: dict[str, str]) -> None:
        """Set the mapping names of the BDD model."""
        self._mapping_names = mapping
        self._mapping_names_inv = {v: k for k, v in mapping.items()}

    @property
    def mapping_names_inv(self) -> dict[str, str]:
        return self._mapping_names_inv

    def _set_global_constants(self) -> None:
        """Private auxiliary function that configures the following global constants.

            + BDDBIN_DIR, which stores the path of the module bdd4va, 
            which is needed to locate the binaries.
            + ENV, which stores the environment variables of the CUDD library.
        """
        caller_dir = os.getcwd()  # get BDDBIN_DIR
        os.chdir(pathlib.Path(__file__).parent)
        shell = subprocess.Popen(['pwd'], 
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, 
                                 text=True, 
                                 shell=True)
        stdout, _ = shell.communicate()
        self._bddbin_dir = stdout.strip()
        os.chdir(caller_dir)
        self._env = os.environ.copy()
        self._env[BDDModel.LD_LIBRARY_PATH] = self._bddbin_dir + '/bin:' + \
                                              self._env.get(BDDModel.LD_LIBRARY_PATH, '')

    def __del__(self) -> None:
        self.delete_files()

    def delete_files(self) -> None:
        """Delete the files created by the BDD library."""
        if self.var_file is not None:
            path = pathlib.Path(self.var_file)
            base = path.parent
            filename = path.stem
            os.remove(self.var_file)
            self.var_file = None
        if self.exp_file is not None:
            os.remove(self.exp_file)
            self.exp_file = None
        if self.sifting_file is not None:
            os.remove(self.sifting_file)
            self.sifting_file = None
        if self.bdd_file is not None:
            os.remove(self.bdd_file)
            self.bdd_file = None
        # Remove auxiliary generated files
        AUXILIARY_FILES = ['.dddmp.data', '.dddmp.reorder', '.tree', '.dddmp.applied']
        for aux_file in AUXILIARY_FILES: 
            path = pathlib.Path(base / (filename + aux_file))
            if path.exists():
                os.remove(path)

    def run(self, binary: str, *args: Any) -> tuple[str, str]:
        """Auxiliary function to run binary files. Returns the stdout and stderr of the command."""
        assert self._bddbin_dir is not None
        bin_dir = self._bddbin_dir + '/bin'
        bin_file = bin_dir + '/' + binary
        command = [bin_file] + list(args)
        process = subprocess.Popen(command,
                                   env=self._env, 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE,
                                   text=True)
        stdout, stderr = process.communicate()
        return stdout, stderr

    @staticmethod
    def expand_assignment(bdd_file: str, feature_assignment: list[str]) -> list[str]:
        '''
        Changes the format of a list of features' assignments.
        e.g., ['MP3', 'not Basic'] => ['MP3=true', 'Basic=false']
        First, it checks if the features in feature_assignment are valid features of bdd_file.
        :param bdd_file: file containing the BDD encoding of the model
        :param feature_assignment: the list of features' assignments
        :return: reformatted feature assignment
        '''

        # Get all feature names
        with open(bdd_file, 'r', encoding='utf8') as file:
            bdd_code = file.read()
            varnames_match = re.search(r'varnames\s+(.*)', bdd_code)
            if not varnames_match:
                raise FlamaException('No varnames found in the BDD file.')
            varnames = varnames_match.group(1).split()

        expanded_assignment = []
        for feature in feature_assignment:
            feat = None
            if re.match(r'not\s+', feature):
                feat_match = re.search(r'not\s+(.*)', feature)
                if feat_match:
                    feat = feat_match.group(1)
                    if varnames.count(feat) == 0:
                        raise FlamaException(f'{feat} is not a valid feature of {bdd_file}.')
                    feat += "=false"
            else:
                if varnames.count(feature) == 0:
                    raise FlamaException(f'{feature} is not a valid feature of {bdd_file}.')
                feat = feature + "=true"
            if feat:
                expanded_assignment.append(feat)
        return expanded_assignment

    def __str__(self) -> str:
        res = f'BDD file: {self.bdd_file}\r\n'
        res += f'  Var file: {self.var_file}\r\n'
        res += f'  Exp file: {self.exp_file}\r\n'
        res += f'  Sifting file: {self.sifting_file}\r\n'
        return res