import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

spins = ['both']
kinds = ['I', 'Pb', 'C', 'N', 'H', 'O']
colors = {'I': '#984B98', 'Pb': '#F99005', 'O': '#0FA842', 'H': '#576ca8', 'C': 'grey', 'N': 'black'}
labels = ['a', 'b', 'c']
calculate_type = 'PDOS234'

for type_i, size in enumerate(['222', '333', '444']):
    for spin in spins:
        sub_total = []
        fig, ax = plt.subplots(figsize=(6, 2.5))
        ax.set_yticks([])
        ax.tick_params(direction='in')
        ax.set_xlabel('E - E$_\mathrm{f}$ [eV]')
        ax.set_ylabel('PDOS')
        for i, kind in enumerate(kinds):
            data = np.loadtxt('{}/Cluster_{}/smeared_{}_{}.dat'.format(calculate_type, size, spin, i+1))
            line, = ax.plot(data[:, 0], data[:, 1], linewidth=1.5,label='{}'.format(kind), color=colors[kind])        
            line_color = line.get_color()
            rgb_color = mcolors.hex2color(line_color)
            thin_color = tuple([c * 0.9 for c in rgb_color]) + (0.3,)
            #print(line_color)
            ax.fill_between(data[:, 0], data[:, 1], color=thin_color)
            sub_total.append(data[:, 1])

            # axins.plot(data[:, 0], data[:, 1], linewidth=1.5,label='{}'.format(kind), color=colors[kind])

        sub_total = np.array(sub_total)
        print(sub_total.shape)
        sub_total = np.sum(sub_total,axis=0)
        print(sub_total.shape)
        #plt.plot(data[:, 0], sub_total, linewidth=1.5, label='{}'.format('Total'))
        # plt.text(0.05, 0.95, 'Spin {}'.format(spin), transform=plt.gca().transAxes, color='black', va='top', ha='left')
        print(i)
        plt.text(0.03, 0.95, '({})'.format(labels[type_i]), transform=plt.gca().transAxes, color='black', va='top', ha='left')
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
        #axins.set_xticklabels([])
        axins.set_yticklabels([])
        for i, kind in enumerate(kinds):
            data = np.loadtxt('{}/Cluster_{}/smeared_{}_{}.dat'.format(calculate_type, size, spin, i+1))
            line,  = axins.plot(data[:, 0], data[:, 1], linewidth=1.5,label='{}'.format(kind), color=colors[kind])
            line_color = line.get_color()
            rgb_color = mcolors.hex2color(line_color)
            thin_color = tuple([c * 0.9 for c in rgb_color]) + (0.3,)
            axins.fill_between(data[:, 0], data[:, 1], color=thin_color)
        ax.indicate_inset_zoom(axins, edgecolor="black")
        plt.savefig('Figure5_{}.pdf'.format(size))
        plt.show()
