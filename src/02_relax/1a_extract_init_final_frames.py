#!/usr/bin/env python

from ase.io import read, write
from ase.visualize import view
from ase.geometry.geometry import wrap_positions
from ase.data import colors, atomic_numbers
import os

# 000 111 are for creating legends for naked cluster and cluster+water respectively. 
sizes = ['000', '111', '222', '333', '444']
cells = []

mainColors = {'Pb': '#747b65', 'I':'#6a0045', 'C':'#a7ac9a', 'N':'#2e4ea8', 'O':'#d61f1f'}

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


# View used to start ag, and find desired viewing angle
# view(atoms)
# rot = '5x,-10y,0z'  # found using ag: 'view -> rotate'
rot = '0x,0y,0z'  # found using ag: 'view -> rotate'

# Common kwargs for eps, png, pov
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




# Load init states
for size in sizes:
    init_structure = read('cluster_{}/Water_cluster{}.xyz'.format(size, size))
    write('cluster_{}/Init_{}.cif'.format(size, size), init_structure)
    # Write the .pov (and .ini) file.
    povray_settings['textures'] = ['intermediate' for a in init_structure]
    renderer = write('init_{}.pov'.format(size), \
        init_structure, **generic_projection_settings, povray_settings=povray_settings)
    renderer.render()
    
    final_structure = read('cluster_{}/MAPbI3-pos-1.xyz'.format(size))
    final_structure.set_cell(init_structure.cell)
    write('cluster_{}/Relaxed_{}.cif'.format(size, size), final_structure)
    # view(final_structure)
    
    # Write the .pov (and .ini) file.
    renderer = write('final_{}.pov'.format(size), \
        final_structure, **generic_projection_settings, povray_settings=povray_settings)
    renderer.render()
cmd = 'rm *.pov *.ini'
os.system(cmd)


