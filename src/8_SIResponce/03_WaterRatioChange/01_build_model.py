from ase.io import read, write
from ase.visualize import view
from ase import Atoms
import numpy as np


def placeWater(x, y, z):
    dx = 0.7
    return Atoms('HOH', positions=np.array([[x-dx, y+dx, z], [x, y, z], [x+dx, y+dx, z]]))

def distance(p1, p2):
    return np.sqrt(np.sum(np.square(p1 - p2), axis=-1))

def canBePlaced(p, positions, dis_cut = 3.0):
    dis = distance(p, positions)        
    return True if (dis > dis_cut).all() else False

def inside(x, y, z, X, Y, Z, D):
    if y < x + (Y -D) and y > -x + D and y < -x + (Y+X-D) and y > x - (X-D) and\
       z < y + (Z -D) and z > -y + D and z < -y + (Z+Y-D) and z > y - (Y-D) and\
       x < z + (X -D) and x > -z + D and x < -z + (X+Z-D) and x > z - (Z-D):
        return True
    else:
        return False


# https://stackoverflow.com/a/51715491/13467324
# https://excalidraw.com/#json=bIHrisNujypTi1kLw9jaR,2OWjY35j49faq6IFD5JY3g
def checkerboard(shape):
    """
    Create checkerboard in numpy 
    """
    return np.indices(shape).sum(axis=0) % 2 

# Based on checkerboard
# I created the occupancyMask
def occupancyMask(shape, vacancyLevel):
    """
    Create occupancy mask in numpy 
    """
    if vacancyLevel == 0:
        mask = np.ones(shape, int)
    elif vacancyLevel == 1:
        temp = np.indices(shape).sum(axis=0) % 4
        mask = np.where(temp > 0, 1, 0)
    elif vacancyLevel == 2:
        temp = np.indices(shape).sum(axis=0) % 3
        mask = np.where(temp > 0, 1, 0)
    elif vacancyLevel == 3:
        mask = np.indices(shape).sum(axis=0) % 2 
    elif vacancyLevel == 4:
        temp = np.indices(shape).sum(axis=0) % 3
        mask = np.where(temp > 0, 0, 1)
    elif vacancyLevel == 5:
        temp = np.indices(shape).sum(axis=0) % 4
        mask = np.where(temp > 0, 0, 1)
    elif vacancyLevel == 6:
        mask = np.zeros(shape, int)
    else:
        print('Vacancy level is integer defined from 0 to 6.')
    return mask



initio_vacuum = 4 # Important: Change to see the difference. 

clusters = ['222']
for vacancyLevel in range(7):
    for cluster in clusters:
        MAPbI3_cluster = read('POSCAR_{}_0.5.vasp'.format(cluster))
        # Set cube cell
        MAPbI3_cluster.set_cell([10, 10, 10, 90, 90, 90])
        MAPbI3_cluster.set_pbc(False)
        MAPbI3_cluster.center(vacuum=initio_vacuum)

        cluster_positions = MAPbI3_cluster.positions
        # print(cluster_positions)

        print(MAPbI3_cluster.cell)
        
        # print(MAPbI3_cluster.get_cell())
        X = MAPbI3_cluster.cell.array[0,0]
        Y = MAPbI3_cluster.cell.array[1,1]
        Z = MAPbI3_cluster.cell.array[2,2]


        Roo = 2.77
        xs = np.array([i*Roo for i in range(0, int(X/Roo))])
        ys = np.array([i*Roo for i in range(0, int(Y/Roo))])
        zs = np.array([i*Roo for i in range(0, int(Z/Roo))])

        n_water = 0
        off_set = np.array([(X-xs[-1])/2, (Y-ys[-1])/2, (Z-zs[-1])/2])
        D = 7
        counter = 0
        print('Size')
        print(len(xs), len(ys), len(zs))
        # mask = np.zeros((len(xs), len(ys), len(zs)), int)


        
        
        # Get the shape, vacancyLevel
        maskShape = (len(xs), len(ys), len(zs))
        mask = occupancyMask(shape=maskShape, vacancyLevel=vacancyLevel)
        print('Mask:')
        print(mask)
        for i, x in enumerate(xs):
            for j, y in enumerate(ys):
                for k, z in enumerate(zs):
                        Ox, Oy, Oz = x + off_set[0], y + off_set[1], z + off_set[2]
                        if inside(Ox, Oy, Oz, X, Y, Z, D):
                            if canBePlaced(p=np.array([Ox, Oy, Oz]), positions=cluster_positions, dis_cut = 2.5):
                                if mask[i, j, k] == 1:
                                    HOH = placeWater(Ox, Oy, Oz)
                                    MAPbI3_cluster += HOH
                                    n_water += 1

        num_density = n_water / (X*Y*Z)
        mol_mass_water = 18.015
        NA = 6.02214076*1E23
        mass_density = mol_mass_water * 1E-3 * num_density / (NA*1E-30)

        print('-------------------------------------')
        print('Vacancy level: {}'.format(vacancyLevel))
        print('Box: {} {} {}'.format(X, Y, Z))
        print('Number of H2O molecules: {}'.format(n_water))
        #print('Number density: {}'.format(num_density))
        #print('Mass density: {}'.format(mass_density))

        MAPbI3_cluster.center(vacuum=5.5)
        MAPbI3_cluster.write('Water_cluster{}_VacancyLevel{}.xyz'.format(cluster, vacancyLevel))
        view(MAPbI3_cluster)
        input('Press Enter')


