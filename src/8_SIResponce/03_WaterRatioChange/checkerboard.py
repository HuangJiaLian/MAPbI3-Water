import numpy as np 


def occupancyMask(shape, vacancyLevel):
    """
    Create occupancy mask in numpy 
    """

    if vacancyLevel == 0:
        mask = np.ones(shape, int)
    elif vacancyLevel == 1:
        temp = np.indices(shape).sum(axis=0) % 3
        mask = np.where(temp > 0, 1, 0)
    elif vacancyLevel == 2:
        mask = np.indices(shape).sum(axis=0) % 2 
    elif vacancyLevel == 3:
        temp = np.indices(shape).sum(axis=0) % 3
        mask = np.where(temp > 0, 0, 1)
    elif vacancyLevel == 4:
        mask = np.zeros(shape, int)
    else:
        print('Vacancy level is integer defined from 0 to 4.')

    return mask


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


for level in range(7):
    mask = occupancyMask(shape=(8, 8), vacancyLevel=level)
    print('Mask for vacancy level {}:\n {}'.format(level, mask))