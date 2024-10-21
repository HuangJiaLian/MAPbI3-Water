import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

spins = ['both']
kinds = ['I', 'Pb', 'C', 'N', 'H', 'O']
colors = {'I': '#984B98', 'Pb': '#F99005', 'O': '#0FA842', 'H': '#576ca8', 'C': 'grey', 'N': 'black'}
labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g']


calculation_type='PDOSsNaked'
band_gap_data = np.loadtxt('{}/band_a.dat'.format(calculation_type))
print('Band Gap File Found')


for type_i, vanclevel in enumerate(['0', '1', '2', '3', '4', '5', '6']):
    for spin in spins:
        sub_total = []
        fig, ax = plt.subplots(figsize=(5, 2.5))
        ax.set_yticks([])
        ax.tick_params(direction='in')
        ax.set_xlabel('E - E$_f$ [eV]', fontsize=12)
        ax.set_ylabel('PDOS', fontsize=12)
        for i, kind in enumerate(kinds):
            try:
                data = np.loadtxt('{}/level{}/smeared_{}_{}.dat'.format(calculation_type, vanclevel, spin, i+1))
                line, = ax.plot(data[:, 0], data[:, 1], linewidth=1.5,label='{}'.format(kind), color=colors[kind])        
                line_color = line.get_color()
                rgb_color = mcolors.hex2color(line_color)
                thin_color = tuple([c * 0.9 for c in rgb_color]) + (0.3,)
                ax.fill_between(data[:, 0], data[:, 1], color=thin_color)
                if type(band_gap_data) != False:
                    axins.axvline(x=band_gap_data[type_i][0], ls='-.', label='HOMO', color=colors['H'])
                    axins.axvline(x=band_gap_data[type_i][1], ls=':', label='LUMO', color=colors['H'])
                sub_total.append(data[:, 1])
            except:
                #print('File not found: smeared_{}_{}.dat'.format(spin, i+1))
                pass
        
        sub_total = np.array(sub_total)
        print(sub_total.shape)
        sub_total = np.sum(sub_total,axis=0)
        print(sub_total.shape)
        #plt.plot(data[:, 0], sub_total, linewidth=1.5, label='{}'.format('Total'))
        # plt.text(0.05, 0.95, 'Spin {}'.format(spin), transform=plt.gca().transAxes, color='black', va='top', ha='left')
        print(i)
        plt.text(0.03, 0.95, '{}'.format(labels[type_i]), transform=plt.gca().transAxes, color='black', va='top', ha='left', fontsize=20)
        #plt.text(0.1, 0.95, 'Vacancy level: {}'.format(vanclevel), transform=plt.gca().transAxes, color='black', va='top', ha='left')
        plt.xlim(-6,6)
        plt.ylim(bottom=0)
        plt.legend(frameon=False, loc='center left', handlelength=0.9, fontsize='large', handletextpad=0.5)
        plt.subplots_adjust(bottom=0.15)
        plt.subplots_adjust(left=0.05, right=0.95, bottom=0.17, top=0.98)

        axins = fig.add_axes([0.52, 0.5, 0.3, 0.43])
        x1, x2, y1, y2 = 0.0, 3.11, 0, 15
        axins.tick_params(direction='in')
        axins.set_xlim(x1, x2)
        axins.set_ylim(y1, y2)
        #axins.set_xticklabels([])
        axins.set_yticklabels([])
        for i, kind in enumerate(kinds):
            try:
                data = np.loadtxt('{}/level{}/smeared_{}_{}.dat'.format(calculation_type, vanclevel, spin, i+1))
                # line, = plt.plot(data[:, 0], data[:, 1], linewidth=1.5,label='{}'.format(kind), color=colors[kind])        
                # line_color = line.get_color()
                # rgb_color = mcolors.hex2color(line_color)
                # thin_color = tuple([c * 0.9 for c in rgb_color]) + (0.3,)
                # #print(line_color)
                # plt.fill_between(data[:, 0], data[:, 1], color=thin_color)
                # sub_total.append(data[:, 1])
                line,  = axins.plot(data[:, 0], data[:, 1], linewidth=1.5,label='{}'.format(kind), color=colors[kind])
                line_color = line.get_color()
                rgb_color = mcolors.hex2color(line_color)
                thin_color = tuple([c * 0.9 for c in rgb_color]) + (0.3,)
                axins.fill_between(data[:, 0], data[:, 1], color=thin_color)
                axins.axvline(x=band_gap_data[type_i][0], ls='-.', label='HOMO', color=colors['H'])
                axins.axvline(x=band_gap_data[type_i][1], ls=':', label='LUMO', color=colors['H'])
                y_position = axins.get_ylim()[1] * 2/3
                axins.annotate('', xy=(band_gap_data[type_i][0], y_position), xytext=(band_gap_data[type_i][1], y_position),
                            arrowprops=dict(arrowstyle='<->', lw=1, color=colors['H']))
                        # Change the text band gap to the real value of band gap, and place at 3/4 height
                band_gap_value = band_gap_data[type_i][1] - band_gap_data[type_i][0]
                y_position_3_4 = axins.get_ylim()[1] * 3/4
                axins.text((band_gap_data[type_i][0] + band_gap_data[type_i][1]) / 2, y_position_3_4, f'{band_gap_value:.2f}' + ' eV',
                        horizontalalignment='center', verticalalignment='bottom', color='black', fontsize=15)
            except:
                pass

        ax.indicate_inset_zoom(axins, edgecolor="black")
        #plt.savefig('{}/level{}/PDOS_{}_{}.pdf'.format(calculation_type, vanclevel, vanclevel, spin))
        plt.savefig('{}/PDOS_{}_{}.pdf'.format(calculation_type, vanclevel, spin))
        plt.savefig('{}/PDOS_{}_{}.png'.format(calculation_type, vanclevel, spin))
        plt.show()
