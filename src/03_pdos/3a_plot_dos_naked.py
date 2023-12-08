#!/usr/bin/env python

import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


# Find GAP at first
def getEFermi(pdosFile):
    start = 'E(Fermi) ='
    end = ' a.u.'
    with open(pdosFile, 'r') as f:
        for line in f:
            if 'E(Fermi)' in line:
                fermi_energy = float(line.split(start)[1].split(end)[0])
                break
    return fermi_energy 

H2eV = 27.211032441
calculate_type = 'PDOSNaked234'

# read and plot
spins = ['alpha', 'beta']
kinds = ['I', 'Pb', 'C', 'N', 'H', 'O']
colors = {'I': '#984B98', 'Pb': '#F99005', 'O': '#0FA842', 'H': '#8E3700', 'C': 'grey', 'N': 'black'}

f = open('{}/band.dat'.format(calculate_type), 'w')

for size in ['222', '333', '444']:
    offset = 0
    deltaY = 0.01
    HOMOs = []
    LUMOs = []
    plt.figure(figsize=(6, 3))
    # plt.grid()
    plt.xlim(-4, 6)
    plt.ylim(0, 0.15)
    plt.tick_params(direction='in')
    #plt.axvline(x=0, ls='--')
    refEnergy = 1
    for spin in spins:
        numType = 5
        for k in range(numType):
            pdosFile = '{}/Cluster_{}/MAPbI3_DOS-{}_k1-1.pdos'.format(calculate_type, size, spin)
            data =  np.loadtxt(pdosFile, skiprows=2)
            eF = getEFermi(pdosFile) 
            #print(eF)
            ener_diff = (data[:, 1] - eF) * H2eV
            HOMO = np.max(ener_diff[ener_diff<refEnergy])
            LUMO = np.min(ener_diff[ener_diff>refEnergy])
            HOMOs.append(HOMO)
            LUMOs.append(LUMO)

            # plt.scatter(ener_diff, data[:, 3], s=30, alpha=1.0, label='{}-{}-{}'.format(size, spin, kinds[k]))
            plt.scatter(ener_diff, data[:, 3], s=30, alpha=1.0)
            offset += deltaY
            plt.plot(ener_diff, data[:, 3] + offset, label='{}-{}-{}'.format(size, spin, kinds[k]), color=colors[kinds[k]])

    HOMO = np.max(np.array(HOMOs))
    LUMO = np.min(np.array(LUMOs))
    print("HOMO, LUMO = {}, {}".format(HOMO, LUMO))
    bandGap = LUMO - HOMO
    print('Band gap:{} eV'.format(bandGap))
    f.write('{} {} {}\n'.format(HOMO, LUMO, bandGap))
    # plt.axvline(HOMO, ls='-')
    # plt.axvline(LUMO, ls='-.')
    plt.xlabel('Eigenvalue [eV]')
    plt.legend(frameon=False, loc='upper left', ncol=2)
    plt.tight_layout()
    #plt.savefig('{}/bandgap_{}.pdf'.format(calculate_type, size))
    plt.show()
f.close()





print('Ploting ... ')
#spins = ['alpha', 'beta', 'both']
spins = ['both']
#kinds = ['H', 'I', 'O', 'Pb', 'C', 'N']
kinds = ['I', 'Pb', 'C', 'N', 'H']
#colors = {'I': '#984B98', 'Pb': '#F99005', 'O': '#0FA842', 'H': '#8E3700', 'C': 'grey', 'N': 'black'}
colors = {'I': '#984B98', 'Pb': '#F99005', 'H': '#576ca8', 'C': 'grey', 'N': 'black'}
labels = ['a', 'b', 'c']


band_gap_data = np.loadtxt('{}/band.dat'.format(calculate_type))
for r, size in enumerate(['222', '333', '444']):
    for spin in spins:
        sub_total = []
        fig, ax = plt.subplots(figsize=(6, 2.5))
        ax.set_yticks([])
        ax.tick_params(direction='in')
        ax.set_xlabel('E - E$_\mathrm{f}$ [eV]')
        ax.set_ylabel('PDOS')
        for i, kind in enumerate(kinds):
            data = np.loadtxt('{}/Cluster_{}/smeared_{}_{}.dat'.format(calculate_type,size, spin, i+1))
            line, = ax.plot(data[:, 0], data[:, 1], linewidth=1.5,label='{}'.format(kind), color=colors[kind])        
            line_color = line.get_color()
            rgb_color = mcolors.hex2color(line_color)
            thin_color = tuple([c * 0.9 for c in rgb_color]) + (0.3,)
            #print(line_color)
            ax.fill_between(data[:, 0], data[:, 1], color=thin_color)
            sub_total.append(data[:, 1])


        sub_total = np.array(sub_total)
        #print(sub_total.shape)
        sub_total = np.sum(sub_total,axis=0)
        #print(sub_total.shape)
        plt.text(0.03, 0.95, '({})'.format(labels[r]), transform=plt.gca().transAxes, color='black', va='top', ha='left')
        plt.xlim(-6,6)
        plt.ylim(bottom=0)
        plt.legend(frameon=False)
        plt.subplots_adjust(bottom=0.15)
        plt.subplots_adjust(left=0.05, right=0.95, bottom=0.17, top=0.98)
        
        
        axins = fig.add_axes([0.52, 0.5, 0.3, 0.43])
        x1, x2, y1, y2 = -0.1, 3.2, 0, 15
        axins.tick_params(direction='in')
        axins.set_xlim(x1, x2)
        axins.set_ylim(y1, y2)
        axins.set_yticklabels([])
        for i, kind in enumerate(kinds):
            data = np.loadtxt('{}/Cluster_{}/smeared_{}_{}.dat'.format(calculate_type,size, spin, i+1))
            line,  = axins.plot(data[:, 0], data[:, 1], linewidth=1.5,label='{}'.format(kind), color=colors[kind])
            line_color = line.get_color()
            rgb_color = mcolors.hex2color(line_color)
            thin_color = tuple([c * 0.9 for c in rgb_color]) + (0.3,)
            axins.fill_between(data[:, 0], data[:, 1], color=thin_color)
            if type(band_gap_data) != False:
                axins.axvline(x=band_gap_data[r][0], ls='-.', label='HOMO', color=colors['H'])
                axins.axvline(x=band_gap_data[r][1], ls=':', label='LUMO', color=colors['H'])
            y_position = axins.get_ylim()[1] * 2/3
            axins.annotate('', xy=(band_gap_data[r][0], y_position), xytext=(band_gap_data[r][1], y_position),
                        arrowprops=dict(arrowstyle='<->', lw=1, color=colors['H']))
                    # Change the text band gap to the real value of band gap, and place at 3/4 height
            band_gap_value = band_gap_data[r][1] - band_gap_data[r][0]
            y_position_3_4 = axins.get_ylim()[1] * 3/4
            axins.text((band_gap_data[r][0] + band_gap_data[r][1]) / 2, y_position_3_4, f'{band_gap_value:.2f}' + ' eV',
                    horizontalalignment='center', verticalalignment='bottom', color='black')
        ax.indicate_inset_zoom(axins, edgecolor="black")   
        plt.savefig('Figure4_{}.pdf'.format(size))
        plt.show()
