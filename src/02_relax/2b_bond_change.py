#!/usr/bin/env python

import MDAnalysis as mda
import numpy as np 
import matplotlib.pyplot as plt
from MDAnalysis.analysis import distances
import seaborn as sns


colors = {'Pb': '#747b65', 'I':'#6a0045', 'C':'#a7ac9a',
              'N':'#576ca8', 'O':'#d61f1f', 'DGreen': '#034c3c'}
sizes = ['222', '333', '444']
calculation_type='nofix'
boxes = [np.array([31.79, 31.09, 30.39]), np.array([37.33, 36.63, 35.93]), np.array([45.64, 44.94, 44.24])]
DotSize = 12
numsWater = [156, 370, 891]
labels = ['a', 'b', 'c']

# Create a figure with a 4:1 width ratio
fig = plt.figure(figsize=(5.5,5))
gs = fig.add_gridspec(3, 2, width_ratios=[4, 1])
ymin, ymax = -0.7, 3.7

for i, size in enumerate(sizes):
    ###################
    # 1. Load structure
    ###################
    u = mda.Universe('cluster_{}/MAPbI3-pos-1.xyz'.format(size))
    
    # Point to the opt_idx frame
    u.trajectory[0]
    
    # Find the center of mass
    nAtoms = len(u.atoms)
    nCluster = nAtoms - 3*numsWater[i]
    nanoCluster = u.select_atoms('index 0:{}'.format(nCluster-1))
    center = nanoCluster.center_of_mass()
    
    #  Select all the Pb atoms
    Pbs = u.select_atoms('name Pb')
    idexes = Pbs.ix
    # print(idexes)
    IPbs = []
    for Pb in Pbs:
        Is = u.select_atoms('name I').select_atoms('around 5 global index {}'.format(Pb.index))   
        #print(Is.n_atoms)
        #print(Is.ix)
        IPb = [[i, Pb.ix]for i in Is.ix]
        IPbs = IPbs + IPb
    ##################################
    # 2. Find the I-Pb bond relation
    ##################################
    IPbs = np.array(IPbs)
    
    # 3. Record I-Pb bond length
    IPbLens = []
    for IPb in IPbs:
        disIPb = mda.analysis.distances.dist(u.select_atoms('index {}'.format(IPb[0])), u.select_atoms('index {}'.format(IPb[1])))[-1][0]
        IPbLens.append(disIPb)
    IPbLens = np.array(IPbLens)
    
    #########################################
    # 3. Distances of I to the center of mass
    #########################################
    # Is = u.select_atoms('index {}'.format(' '.join(IPbs[:, 0].astype(int).astype(str))))
    Is = u.atoms[[k.astype(int) for k in IPbs[:, 0]]]
    Distances_I_center = np.sqrt(np.sum((Is.positions - center)**2, axis=-1))


    
    # Point to the opt_idx frame
    u.trajectory[-1]
    ###############################
    # 5. Record I-Pb bond length
    ###############################
    IPbLens_relaxed = []
    for IPb in IPbs:
        disIPb = mda.analysis.distances.dist(u.select_atoms('index {}'.format(IPb[0])), u.select_atoms('index {}'.format(IPb[1])))[-1][0]
        IPbLens_relaxed.append(disIPb)
    IPbLens_relaxed = np.array(IPbLens_relaxed)

    
    # 6. I-Pb bond length change
    IPbLens_Change = IPbLens_relaxed - IPbLens

    # Create scatter plot in first subplot
    ax1 = fig.add_subplot(gs[i, 0])
    ax1.scatter(Distances_I_center, IPbLens_Change, s=DotSize, color=colors['DGreen'], alpha=0.5)
    ax1.axhline(y=np.mean(IPbLens_Change), color=colors['Pb'], linestyle='--', lw=1, label='Mean')
    ax1.set_xlabel('Center-I distance [$\AA$]')
    ax1.set_ylabel('$\Delta$ Pb-I distance [$\AA$]')
    ax1.set_xlim(2.5, 19.9)
    ax1.set_ylim(ymin, ymax)
    ax1.tick_params(axis='both', direction='in', right=True)
    ax1.set_yticks(range(int(ymin), int(ymax)+1, 1))
    if i == 0 or i == 1:
        ax1.tick_params(axis='both', direction='in', right=True, labelbottom=False)
        ax1.set_xlabel('')
    ax1.annotate('({})'.format(labels[i]), xy=(0.04, 0.8), xycoords="axes fraction")
    # Add legend
    ax1.legend(frameon=False, loc='upper right', handlelength=1.5, handletextpad=0.4)
    # Create histogram of y values in second subplot
    ax2 = fig.add_subplot(gs[i, 1])
    ax2.axhline(y=np.mean(IPbLens_Change), color=colors['Pb'], linestyle='--', lw=1, label='Mean')
    ax2.hist(IPbLens_Change, orientation='horizontal', range=(-0.9, 1.9), bins=30,  density=True, color=colors['DGreen'], alpha=1)
    sns.kdeplot(y=IPbLens_Change, fill=True, bw_adjust=0.5,
                ax=ax2, color=colors['Pb'])
    ax2.set_xlabel('')
    ax2.set_ylim(ymin, ymax)
    ax2.tick_params(axis='both', direction='in', labelleft=False)
    if i == 0 or i == 1:
        ax2.set_xlabel('')

    ax2.spines['top'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.set_xticks([])
    ax2.set_yticks([])
fig.subplots_adjust(hspace=0.05, wspace=0.01, left=0.1, bottom=0.1, right=0.99, top=0.95)
plt.savefig('Figure3.pdf')
plt.show()
    
    
        
        