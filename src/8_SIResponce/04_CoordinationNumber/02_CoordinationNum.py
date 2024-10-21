import MDAnalysis as mda
import numpy as np 
import matplotlib.pyplot as plt
from tqdm import tqdm
import matplotlib.pyplot as plt 

def distance(p1, p2, box):
    '''
    calculate the distance between point p1 and p2.
    box: the size of poriodic box. eg. np.array([5, 5, 5])
    '''
    delta = np.abs(p1 - p2)
    delta_x, delta_y, delta_z = delta[:, 0], delta[:, 1], delta[:, 2]
    delta[:, 0] = np.where(delta_x > 0.5*box[0], delta_x - box[0] , delta_x)
    delta[:, 1] = np.where(delta_y > 0.5*box[1], delta_y - box[1] , delta_y)
    delta[:, 2] = np.where(delta_z > 0.5*box[2], delta_z - box[2] , delta_z)
    dis =  np.sqrt((delta ** 2).sum(axis=-1))
    return dis

def rdf(universe, elementA, elementB, startFrame, rangeA = None):
    '''
    Calculate pair correlation function g_AB(r)
    
    Input:
    universe: MDAnalysis universe object
    elementA: center atom element
    elementB: atom around the center

    Output:
    r: distances between A and B
    gr: pair correlation function 
    '''
    if rangeA != -1:
        atomA = universe.select_atoms('name {} and index {}:{}'.\
                        format(elementA, rangeA[0], rangeA[1]))
    else:
        atomA = universe.select_atoms('name {}'.format(elementA))
    atomB = universe.select_atoms('name {}'.format(elementB))
    box = universe.dimensions[0:3]
    numA = atomA._ix.size
    numB = atomB._ix.size

    AB_all_distances = np.array([])

    # Change to startFrame
    universe.trajectory[startFrame]
    atomA_positions = atomA.positions
    atomB_positions = atomB.positions
    for center_A in atomA_positions:
        AB_distances = distance(center_A, atomB_positions, box)
        AB_all_distances = np.concatenate((AB_all_distances, AB_distances))
    
    bins = np.linspace(1, box[0]/2, 200)
    gr=np.histogram(AB_all_distances, bins=bins)
    r = gr[1][0:-1]
    dr=gr[1][1]-gr[1][0]
    box_volume = box.prod()
    rho = numB/box_volume
    gr = (gr[0]/(4*np.pi*gr[1][0:-1]**2*dr * rho)) / numA
    return r, gr, rho



def coordination_number(r_values, rdf, cutoff_distance, density):
    """
    Calculate the coordination number based on the radial distribution function (RDF).

    Parameters:
    rdf (numpy.ndarray): Radial distribution function values.
    r_values (numpy.ndarray): Corresponding distance values for RDF.
    cutoff_distance (float): The distance up to which the coordination number is calculated.
    density (float): Number density of the system.

    Returns:
    float: Coordination number up to the specified cutoff distance.
    """
    # Find the indices of r_values that are less than or equal to the cutoff_distance
    indices = np.where(r_values <= cutoff_distance)

    # Calculate the coordination number as the integral of RDF up to cutoff_distance
    coord_number = np.trapz(rdf[indices] * 4 * np.pi * density * r_values[indices]**2, r_values[indices])
    return coord_number


traj = 'AIMD_Traj/nvt-pos-1.xyz'
dimension = np.array([31.79, 31.09, 30.389999999999997, 90, 90, 90])

u = mda.Universe(traj, dt=0.001)
u.dimensions = dimension
u.transfer_to_memory(start=0, step=1, verbose=True)

frames = len(u.trajectory)
print('Total frames: {}'.format(frames))
print('Universe dimension: ', u.dimensions)


times = np.linspace(0, 8, 1000)
CN_PbIs = []
CN_NIs = []
CN_NOs = []
CN_PbNs = []

for t in range(len(times)):
    frameNum = int(times[t]*1000)
    print('Time: {} ps'.format(times[t]))

    r, gr, rho = rdf(u, 'N', 'O', frameNum, [0, 100])
    CN_NO = coordination_number(r, gr,  3.5, rho)
    CN_NOs.append(CN_NO)
    print('CN_NO: ', CN_NO)


    r, gr, rho = rdf(u, 'N', 'I', frameNum, [0, 100])
    CN_NI = coordination_number(r, gr,  4.7, rho)
    CN_NIs.append(CN_NI)
    print('CN_NI: ', CN_NI)

    r, gr, rho = rdf(u, 'Pb', 'N', frameNum, [0, 100])
    CN_PbN = coordination_number(r, gr,  7, rho)
    CN_PbNs.append(CN_PbN)
    print('CN_NI: ', CN_PbN)

    r, gr, rho = rdf(u, 'Pb', 'I', frameNum, [0, 100])
    CN_PbI = coordination_number(r, gr,  3.7, rho)
    CN_PbIs.append(CN_PbI)
    print('CN_PbI: ', CN_PbI)


plt.figure(figsize=(9,3))
plt.tick_params(direction='in')
plt.plot(times, CN_NOs, label='N-O')
plt.plot(times, CN_NIs, label='N-I')
plt.plot(times, CN_PbNs, label='Pb-N')
plt.plot(times, CN_PbIs, label='Pb-I')

plt.xlabel('Time (ps)')
plt.ylabel('Coordination Number')
plt.xlim([0, 8])
plt.ylim([0.5, 6.5])
plt.legend(loc='upper right', frameon=False, ncol=4)
plt.tight_layout()
plt.savefig('CNum.pdf')
plt.savefig('CNum.png', dpi=300)
plt.show()


