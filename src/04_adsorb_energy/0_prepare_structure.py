from ase.io import read, write
from ase.visualize import view
from ase.geometry.geometry import wrap_positions
import os
from ase.data import colors, atomic_numbers

traj_path='../02_relax'
calculation_type='ab_energy_final'
sizes = ['222', '333', '444']
cells = []

centerNums = [100, 391, 952]

f = open('box_sizes.dat', 'w')
     # Write your code here
# Load init states
for i, size in enumerate(sizes):
    init_structure = read('{}/Cluster_{}/Water_cluster{}.xyz'.format(traj_path, size, size))[:centerNums[i]]
    MAPbI3_Water = read('{}/Cluster_{}/MAPbI3-pos-1.xyz'.format(traj_path, size))
    MAPbI3 = read('{}/Cluster_{}/MAPbI3-pos-1.xyz'.format(traj_path, size))[:centerNums[i]]
    Water = read('{}/Cluster_{}/MAPbI3-pos-1.xyz'.format(traj_path, size))[centerNums[i]:]

    #print(init_structure.cell)
    print('ABC {:.4f} {:.4f} {:.4f}'.format(init_structure.cell[0][0], init_structure.cell[1][1], init_structure.cell[2][2]))
    f.write('ABC {:.4f} {:.4f} {:.4f}\n'.format(init_structure.cell[0][0], init_structure.cell[1][1], init_structure.cell[2][2]))
    MAPbI3_Water.set_cell(init_structure.cell)
    MAPbI3.set_cell(init_structure.cell)
    Water.set_cell(init_structure.cell)

    view(MAPbI3_Water)
    view(MAPbI3)
    view(Water)

    os.system('mkdir -p {}/Cluster_{}'.format(calculation_type, size))
    write('{}/Cluster_{}/relaxed_MAPbI3_Water.xyz'.format(calculation_type, size), MAPbI3_Water)
    write('{}/Cluster_{}/relaxed_MAPbI3.xyz'.format(calculation_type, size), MAPbI3)
    write('{}/Cluster_{}/relaxed_Water.xyz'.format(calculation_type, size), Water)

f.close()
