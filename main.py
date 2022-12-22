import numpy as np

import biotite.structure.io.pdb
import biotite.structure

from graph import Plot
from assemble import AssembleTC

'''
Fold protein based on partial charges of atoms
'''


class Atom:
    def __init__(self, position: np.array, charge: float, symbol: str, *args, **kwargs):
        self.position: np.array = position
        self.partial_charge: float = charge
        self.symbol: str = symbol

    def __str__(self):
        return f'{self.symbol}, {self.position}, {self.partial_charge}'


class Protein:
    def __init__(self, file_name='', *args, **kwargs):
        if len(file_name):
            try:
                pdbfile = biotite.structure.io.pdb.PDBFile.read(
                    file_name)
                self.molecule: biotite.structure.AtomArray = biotite.structure.io.pdb.get_structure(
                    pdbfile, model=True)  # only kept for displaying the molecule
            except FileNotFoundError as ex:
                print(f"Could not load file: {file_name}. Loading from biotite info.")
                self.molecule = AssembleTC.assemble()
        else:
            self.molecule = AssembleTC.assemble()

        self.molecule.bonds = biotite.structure.connect_via_residue_names(
            self.molecule)
        self.charges = biotite.structure.partial_charges(self.molecule)

        self.aa_start_index = [
            j for i, j, _ in self.molecule.bonds.as_array()
            if self.molecule.res_id[i] != self.molecule.res_id[j]
        ]

        self.atoms: np.array = np.array([Atom(pos, q, s) for pos, q, s in zip(
            self.molecule.coord, self.charges, self.molecule.element)], dtype=Atom)

        # self.show_graph()

        self.calculate_net_torque_on_seg(self.aa_start_index[10])

    def calculate_torque_on_seg(self, index):
        torque = 0.0
        for atom1 in self.atoms[:index]:
            for atom2 in self.atoms[index:]:
                dpos = atom1.position - atom2.position
                print(np.linalg.norm(dpos))


    def rotate_segment(self, index, theta, origin):
        pass

    def show_graph(self):
        self.molecule._coord = np.array([atom.position for atom in self.atoms])
        Plot.plot(self.molecule, self.charges)


def main():

    trp_cage = Protein()

    return


if __name__ == '__main__':
    main()
