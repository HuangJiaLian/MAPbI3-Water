# 222
rsync  -Pr huangj4@triton.aalto.fi:/scratch/phys/project/sin/Jie/Github/cp2kTest/PreviousOpt_Morestep/cluster_222/MAPbI3-pos-1.xyz cluster_222/
rsync  -Pr huangj4@triton.aalto.fi:/scratch/phys/project/sin/Jie/Github/cp2kTest/PreviousOpt_Morestep/cluster_222/output.log cluster_222/

# 333
rsync  -Pr huangj4@triton.aalto.fi:/scratch/phys/project/sin/Jie/Github/cp2kTest/PreviousOpt_Morestep/cluster_333_2000Step/MAPbI3-pos-1.xyz cluster_333/
rsync  -Pr huangj4@triton.aalto.fi:/scratch/phys/project/sin/Jie/Github/cp2kTest/PreviousOpt_Morestep/cluster_333_2000Step/output.log cluster_333/

# 444 (LBFGS)
scp huangj4@triton.aalto.fi:/scratch/phys/project/sin/Jie/Github/cp2kTest/PreviousOpt_Morestep/cluster_444_3000_scratch_L_1208/MAPbI3-pos-1-combined.xyz cluster_444/MAPbI3-pos-1.xyz
rsync  -Pr huangj4@triton.aalto.fi:/scratch/phys/project/sin/Jie/Github/cp2kTest/PreviousOpt_Morestep/cluster_444_3000_scratch_L_1208/output.log cluster_444/

