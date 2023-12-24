import numpy as np
from ase.io import read, write
from ase.visualize import view
from tqdm import tqdm 
from ase.cell import Cell
from ase.io.trajectory import TrajectoryWriter
from ase.data import colors, atomic_numbers
import os

# Obtian the trajectory for center cluster

sizes = ['222']
# md_types = ['cluster', 'bulk']
md_types = ['cluster']
boxes = [(31.7900009155, 31.0900001526, 30.3899993896), (27.03067872876426, 26.29503608786156, 27.44481142700276)]
# size = sizes[0]
# md_type = md_types[0]
mainColors = {'Pb': '#747b65', 'I':'#6a0045', 'C':'#a7ac9a', 'N':'#2e4ea8', 'O':'#d61f1f'}
centerNums = [100, 391, 916]

def hex2rgb(color, fraction=True):
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:], 16)
    return (r/255., g/255., b/255.) if fraction else (r, g, b)

for e in ['Pb', 'I', 'C', 'N', 'O']:
    color = hex2rgb(mainColors[e])
    e_an = atomic_numbers[e]
    colors.jmol_colors[e_an] = color
    colors.cpk_colors[e_an] = color
    
rot = '0x,0y,0z'

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
    'celllinewidth': 0.1,  # Radius of the cylinders representing the cell
}


size = sizes[0]

for j, md_type in enumerate(md_types):
    trajs = read('{}/nvt-pos-1-222.xyz'.format(md_type), index='::1')
    indices=[atom.index for atom in trajs[0] if atom.index < 100]
    MAPbI3_traj = TrajectoryWriter('MAPbI3_{}.traj'.format(md_type), 'w')
    for i, atoms in enumerate(tqdm(trajs)):
        MAPbI3 = atoms[indices]
        MAPbI3.set_cell(Cell(np.eye(3)*np.array(boxes[j])))
        if i % 1000 == 0:
            # write('{}/MAPbI3_{}_{}.png'.format(md_type, md_type, i), MAPbI3)
            # write('{}/MAPbI3_{}_{}.cif'.format(md_type, md_type, i), MAPbI3)
            povray_settings['textures'] = ['intermediate' for a in MAPbI3]
            renderer = write('center_{}_{}_ps.pov'.format(size, i//1000), \
                            MAPbI3, **generic_projection_settings, povray_settings=povray_settings)
            renderer.render()
        MAPbI3_traj.write(MAPbI3)
    cmd = 'mv center_* {}/'.format(md_type)