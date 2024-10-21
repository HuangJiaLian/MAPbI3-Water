Dear developers,

I'd like to express my gratitude for your ongoing efforts in developing and updating CP2K.

I recently tried out the latest version, CP2K v2023.2, and noticed the addition of a new pseudopotential file 'GTH_SOC_POTENTIALS' in the `data` folder.

I'd like to perform PDOS calculations with spin-orbit coupling (SOC). And I modified my input file by using 'POTENTIAL_FILE_NAME GTH_SOC_POTENTIALS' instead of 'POTENTIAL_FILE_NAME GTH_POTENTIALS'. The calculations were executed without errors. However, I am not sure this is the correct procedure to use this feature. Could you please provide some guidance?

Your response would be greatly appreciated.

Best regards, 

Jie Huang


Dear Jie Huang
 
Note, that SOC is only available for the calculation of some (very few) properties during a post-SCF calculation. The preceding wavefunction optimization is not performed with SOC.
 
Best
 
Matthias



Dear Matthias:

I appreciate your quick response and the clarification regarding the limitation. It helps me better understand the situation. 

Kind regards, 

Jie
