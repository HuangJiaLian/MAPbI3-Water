import numpy as np
import matplotlib.pyplot as plt


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
calculate_type = 'PDOSsNaked'

# read and plot
spins = ['alpha', 'beta']
kinds = ['I', 'Pb', 'C', 'N', 'H', 'O']
colors = {'I': '#984B98', 'Pb': '#F99005', 'O': '#0FA842', 'H': '#8E3700', 'C': 'grey', 'N': 'black'}

f = open('{}/band.dat'.format(calculate_type), 'w')

for vacancyLevel in ['0', '1', '2', '3', '4', '5', '6']:
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
        numType = 5 if calculate_type == 'cp2k-bare' else 6
        for k in range(numType):
            # if calculate_type == 'cp2k-bare':
            pdosFile = '{}/level{}/MAPbI3_DOS-{}_k1-1.pdos'.format(calculate_type, vacancyLevel, spin)
            # if calculate_type == 'cp2k-full':
            #     pdosFile = '{}/cp2k_dos_{}/MAPbI3_DOS-{}_k1-1.pdos'.format(calculate_type, size, spin)
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
            plt.plot(ener_diff, data[:, 3] + offset, label='{}-{}-{}'.format(vacancyLevel, spin, kinds[k]), color=colors[kinds[k]])

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
    plt.savefig('{}/bandgap_{}.pdf'.format(calculate_type, vacancyLevel))
    plt.show()
f.close()
