from ase.io import read, write
from ase.visualize import view
import numpy as np 

H2O_numbers = np.array([156, 370, 891], int)
Atom_numbers = np.array([568, 1501, 3625], int)
cluster_atom_numbers = Atom_numbers - H2O_numbers*3
for cnum, type in zip(cluster_atom_numbers, ['222', '333', '444']):
    cluster_and_water = '{}/Water_cluster{}.xyz'.format(type, type)

    # Read the xyz file
    atoms = read(cluster_and_water)

    naked_cluster = atoms[:cnum]
    # View the first cnum atoms
    view(naked_cluster)

    # Save naked_cluster as xyz file in corresponding folder
    write('{}/naked_cluster{}.xyz'.format(type, type), naked_cluster)
