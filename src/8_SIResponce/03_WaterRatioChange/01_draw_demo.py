import matplotlib.pyplot as plt
import numpy as np

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



maskShape = (8,8,8)
waterNums = [156, 117, 104, 78, 52, 39, 0]
for vacancyLevel in range(7):
    mask = occupancyMask(shape=maskShape, vacancyLevel=vacancyLevel)[0]
    print('Level: ', vacancyLevel)
    plt.figure(figsize=(5, 5))
    plt.xlim(-2, 9)
    plt.ylim(-2, 9)
    plt.xticks([])
    plt.yticks([])
    for i in range(8):
        for j in range(8):
            if (i == 0 and j == 0) or (i == 1 and j == 0) or (i == 0 and j == 1) or (i == 7 and j == 7) or (i == 7 and j == 6) or (i == 6 and j == 7) or (i == 7 and j == 0) or (i == 6 and j == 0) or (i == 7 and j == 1) or (i == 0 and j == 7) or (i == 0 and j == 6) or (i == 1 and j == 7): 
                # plt.scatter(j, i, s=100, color='lightgrey', facecolors='none', edgecolors='grey', linestyle='--')
                pass
            else:
                if mask[i][j] == 1:
                    plt.scatter(j, i, s=150, color='red')
                else:
                    plt.scatter(j, i, s=150, color='lightgrey')
        #plt.text(-1.5, 8, f'Vacancy level: {vacancyLevel}', fontsize=18, color='black')
        #plt.text(-1.5, 7, f'Water: {waterNums[vacancyLevel]}', fontsize=18, color='black')
    plt.tight_layout()
    plt.savefig('Demo_level_{}.png'.format(vacancyLevel))
    # plt.show()
