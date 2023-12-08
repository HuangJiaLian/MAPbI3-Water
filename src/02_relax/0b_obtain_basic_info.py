#!/usr/bin/env python

from ase.io import read, write
from ase.visualize import view
from ase.geometry.geometry import wrap_positions
import os
from ase.data import colors, atomic_numbers

sizes = ['222', '333', '444']
cells = []


centerNums = [100, 391, 952]

# Load init states
for i, size in enumerate(sizes):
    cluster = read('cluster_{}/Water_cluster{}.xyz'.format(size, size))[:centerNums[i]]
    formula = cluster.get_chemical_formula()
    print("Cluster {} formula: {}".format(size, formula))

    positions = cluster.get_positions()
    max_pos = positions.max(axis=0)
    min_pos = positions.min(axis=0)
    size_xyz = max_pos - min_pos
    cluster_size = size_xyz.mean()
    cluster_size_nm = cluster_size / 10
    print("Cluster {} size in nm: {:.2f}".format(size, cluster_size_nm))

    waters = read('cluster_{}/Water_cluster{}.xyz'.format(size, size))[centerNums[i]:]
    num_atoms_waters = len(waters)
    print('H2O number:', num_atoms_waters/3)

    cell_volume_nm3 = cluster.get_volume() / 1000
    print("Box volume in nm^3: {:.2f}".format(cell_volume_nm3))



