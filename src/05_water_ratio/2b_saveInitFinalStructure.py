from ase.io import read, write
relaxPath = 'VacancyLevels'


for l in range(7):
    print('level{}'.format(l))
    trajFile = '{}/level{}/MAPbI3-pos-1.xyz'.format(relaxPath, l)
    initial_frame = read(trajFile, index=0, format='xyz')
    final_frame = read(trajFile, index=-1, format='xyz')
    naked_final_frame = final_frame[:100]
    initial_frame.set_cell([(31.79, 0.0, 0.0), (0.0, 31.09, 0.0), (0.0, 0.0, 30.389999999999997)], scale_atoms=False)
    final_frame.set_cell([(31.79, 0.0, 0.0), (0.0, 31.09, 0.0), (0.0, 0.0, 30.389999999999997)], scale_atoms=False)
    naked_final_frame.set_cell([(31.79, 0.0, 0.0), (0.0, 31.09, 0.0), (0.0, 0.0, 30.389999999999997)], scale_atoms=False)
    write('initial_frame_level{}.png'.format(l), initial_frame)
    write('final_frame_level{}.png'.format(l), final_frame)
    write('naked_final_frame_level{}.png'.format(l), naked_final_frame)
    
