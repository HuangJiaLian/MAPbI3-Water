#!/usr/bin/env python

import MDAnalysis as mda
import numpy as np 
import matplotlib.pyplot as plt
from MDAnalysis.analysis import distances
import seaborn as sns


sizes = ['222', '333', '444']
labels = ['a', 'b', 'c']
mainColors = {'Pb': '#747b65', 'I':'#6a0045', 'C':'#a7ac9a',
              'N':'#576ca8', 'O':'#d61f1f', 'DGreen': '#034c3c'}
colors = ['#F99005', '#0FA842']
states = ['Start', 'Relaxed']
calculation_type='nofix'

plt.figure(figsize=(5.5,5))

for j, opt_idx in enumerate([0, -1]):
    bond_lengths_list = []
    for i, size in enumerate(sizes):
        u = mda.Universe('Cluster_{}/MAPbI3-pos-1.xyz'.format(size))
        # Point to the opt_idx frame
        u.trajectory[opt_idx]
        #  Select all the Pb atoms
        Pbs = u.select_atoms('name Pb') 
        idexes = Pbs.ix
        # print(idexes)
        
        bond_lengths = []
        for Pb in Pbs:
            # Select all the I atoms around the a Pb atom
            Is = u.select_atoms('name I').select_atoms('around 5 global index {}'.format(Pb.index))   
            lengths = distances.distance_array(Is, Pb.position)
            bond_lengths += lengths.flatten(order='C').tolist()
        plt.subplot(3, 1, i+1) 
        plt.ylabel('Density ')
        plt.xlabel('Pb-I distance [$\AA$]')
        plt.tick_params(direction="in", axis='both', top=True)
        plt.xlim(2.8, 4.75)
        plt.ylim(0, 11)
        color = mainColors['O'] if opt_idx ==  0 else mainColors['DGreen']
        plt.hist(bond_lengths, density=True, range=(2, 5), color = color, bins=100, alpha=0.7, label='{}'.format(states[j]))
        # sns.kdeplot(data=bond_lengths, fill=False, bw_adjust=0.6, color=color)
        plt.legend(frameon=False)
        plt.annotate('({})'.format(labels[i]), xy=(0.04, 0.8), xycoords="axes fraction")
        if i == 0 or i == 1: 
            plt.tick_params(labelbottom=False)
            plt.xlabel('')
        
plt.subplots_adjust(hspace=0.02, wspace=0.01, left=0.12, bottom=0.1, right=0.95, top=0.95)
plt.savefig('Figure2.pdf')
plt.show()
        
