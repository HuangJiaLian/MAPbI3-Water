
for dir in 222 333 444
do
  cd $dir
  # Perform operations here
  scp huangj4@triton.aalto.fi:/scratch/phys/project/sin/Jie/Github/cp2kTest/nakedRelax/submit.sh . 
  cd ..
done

zip -r archive.zip 222 333 444

scp archive.zip huangj4@triton.aalto.fi:/scratch/phys/project/sin/Jie/Github/cp2kTest/nakedRelax/
