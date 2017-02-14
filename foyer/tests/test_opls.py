import glob
import os

import parmed as pmd
from pkg_resources import resource_filename
import pytest

from foyer import Forcefield
from foyer.tests.utils import atomtype

OPLSAA = Forcefield(name='oplsaa')

OPLS_TESTFILES_DIR = resource_filename('foyer', '../opls_validation')

class TestOPLS(object):

    @pytest.fixture(autouse=True)
    def initdir(self, tmpdir):
        tmpdir.chdir()

    top_files = set(glob.glob(os.path.join(OPLS_TESTFILES_DIR, '*/*.top')))

    # Please update this file if you implement atom typing for a test case.
    # You can automatically update the files by running the below function
    # `find_correctly_implemented`.
    implemented_tests_path = os.path.join(os.path.dirname(__file__),
                                          'implemented_opls_tests.txt')
    with open(implemented_tests_path) as f:
        correctly_implemented = [line.strip() for line in f]

    def find_correctly_implemented(self):
        with open(self.implemented_tests_path, 'a') as fh:
            for top_path in self.top_files:
                _, top_file = os.path.split(top_path)
                mol_name = top_file[:-4]
                try:
                    self.test_atomtyping(mol_name)
                except Exception as e:
                    print(e)
                    continue
                else:
                    if mol_name not in self.correctly_implemented:
                        fh.write('{}\n'.format(mol_name))

    @pytest.mark.parametrize('mol_name', correctly_implemented)
    def test_atomtyping(self, mol_name, testfiles_dir=OPLS_TESTFILES_DIR):
        top_filename = '{}.top'.format(mol_name)
        gro_filename = '{}.gro'.format(mol_name)
        top_path = os.path.join(testfiles_dir, mol_name, top_filename)
        gro_path = os.path.join(testfiles_dir, mol_name, gro_filename)

        structure = pmd.gromacs.GromacsTopologyFile(top_path, xyz=gro_path, parametrize=False)
        atomtype(structure, OPLSAA)

    def test_full_parametrization(self):
        top = os.path.join(OPLS_TESTFILES_DIR, 'benzene/benzene.top')
        gro = os.path.join(OPLS_TESTFILES_DIR, 'benzene/benzene.gro')
        structure = pmd.load_file(top, xyz=gro)
        parametrized = OPLSAA.apply(structure)

        assert sum((1 for at in parametrized.atoms if at.type == 'opls_145')) == 6
        assert sum((1 for at in parametrized.atoms if at.type == 'opls_146')) == 6
        assert len(parametrized.bonds) == 12
        assert all(x.type for x in parametrized.bonds)
        assert len(parametrized.angles) == 18
        assert all(x.type for x in parametrized.angles)
        assert len(parametrized.rb_torsions) == 24
        assert all(x.type for x in parametrized.dihedrals)



if __name__ == '__main__':
    TestOPLS().find_correctly_implemented()