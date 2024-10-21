from ase.io import read, write
from ase.visualize import view
from tqdm import tqdm
import nglview as nv
from ase.cell import Cell
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from ase import Atoms
import pydot
from networkx.drawing.nx_pydot import graphviz_layout
from ase.data import colors, atomic_numbers
from ase.cell import Cell
import os


def renderStructure(aseAtoms, outFile='output.pov'):

    # View used to start ag, and find desired viewing angle using view(atoms)
    rot = '0x,0y,0z'  # found using ag: 'view -> rotate'

    generic_projection_settings = {
        'rotation': rot,  # text string with rotation (default='' )
        'radii': .85,  # float, or a list with one float per atom
        'colors': None,  # List: one (r, g, b) tuple per atom
        'show_unit_cell': 2,   # 0, 1, or 2 to not show, show, and show all of cell
    }

    # Extra kwargs only available for povray (All units in angstrom)
    povray_settings = {
        'display': False,  # Display while rendering
        'pause': True,  # Pause when done rendering (only if display)
        'transparent': True,  # Transparent background
        'canvas_width': 2500,  # Width of canvas in pixels
        'canvas_height': None,  # Height of canvas in pixels
        'camera_dist': 50.,  # Distance from camera to front atom
        'image_plane': None,  # Distance from front atom to image plane
        #'camera_type': 'perspective',  # perspective, ultra_wide_angle
        'point_lights': [],             # [[loc1, color1], [loc2, color2],...]
        'area_light': [(2., 3., 40.),  # location
                       'White',       # color
                       .7, .7, 3, 3],  # width, height, Nlamps_x, Nlamps_y
        'background': 'White',        # color
        'textures': None,  # Length of atoms list of texture names
        'celllinewidth': 0.00000001,  # Radius of the cylinders representing the cell
    }


    povray_settings['textures'] = ['intermediate' for a in aseAtoms]
    renderer = write('{}'.format(outFile),\
               aseAtoms, **generic_projection_settings, povray_settings=povray_settings)
    renderer.render()
    print('Rendered.')





traj_cluster = read('{}/{}/MAPbI3-pos-1-cellAdded.xyz'.format('calculation_out', '222_moreSteps_1000'), index='::1')


idxs = np.linspace(1, len(traj_cluster), 5, int)
print(idxs+1)
for i in idxs:
    # G, distances, angles = structure_analysis(traj_cluster[i])
    # traj_cluster[i].set_cell(Cell(np.eye(3)*box))
    # write('cluster/dgraph/R_{}.png'.format(i), traj_cluster[i][0:100])
    i = int(i-1)
    renderStructure(traj_cluster[i][0:100], outFile='frame_{}.pov'.format(i+1))


traj_cluster = read('MAPbI3-pos-1-222-water100p-cellAdded.xyz', index='::1')
idxs = np.linspace(1, len(traj_cluster), 5, int)
print(idxs+1)
for i in idxs:
    print(i)
    # G, distances, angles = structure_analysis(traj_cluster[i])
    # traj_cluster[i].set_cell(Cell(np.eye(3)*box))
    # write('cluster/dgraph/R_{}.png'.format(i), traj_cluster[i][0:100])
    i = int(i-1)
    renderStructure(traj_cluster[i][0:100], outFile='frame_water100p{}.pov'.format(i+1))