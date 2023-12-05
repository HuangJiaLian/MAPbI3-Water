import os, sys
import numpy as np 
from ase.io import read, write
from ase.visualize import view
import matplotlib.pyplot as plt

def cosine_similarity(a, b):
    dot_product = np.dot(a, b)
    magnitude_a = np.linalg.norm(a)
    magnitude_b = np.linalg.norm(b)
    similarity = dot_product / (magnitude_a * magnitude_b)
    return similarity
basePath  = 'VacancyLevels'
similarities = []
for l in range(7):
    out_file = os.path.join(basePath, 'level{}/MAPbI3-pos-1.xyz'.format(l))
    frames = read(out_file, ':')
    v_0 = frames[0][:100].positions.flatten()
    v_t = frames[-1][:100].positions.flatten()
    similarity = cosine_similarity(v_0, v_t)
    similarities.append(similarity)
    print(similarity)

plt.plot(range(7), similarities, marker='o')
plt.xlabel('Vacancy Level')
plt.ylabel('Similarity')
plt.title('Similarity between initial and final positions')
plt.show()

