#!/bin/bash
source /Users/mac/.jackprogram/anaconda3/bin/activate py2


# Get get-smearing-pdos.py and pdos.py
srcPath=/Users/mac/Github/MAPBI3_Water/6_Writing/dos
cp $srcPath/get-smearing-pdos.py . 
cp $srcPath/pdos.py . 

# calculation_type=PDOSs
calculation_type=PDOSsNaked

# Out loop 
for vaclevel in 0 1 2 3 4 5 6
do 
echo Level ${vaclevel}
cp get-smearing-pdos.py $calculation_type/level$vaclevel/
cp pdos.py $calculation_type/level$vaclevel/
cd $calculation_type/level$vaclevel/

# Inner loop 
for i in 1 2 3 4 5 6

do  
    # This check is especially for level 6 that doesn't have k6
    if [ -f MAPbI3_DOS-ALPHA_k$i-1.pdos ]; then
        echo MAPbI3_DOS-ALPHA_k$i-1.pdos
        python get-smearing-pdos.py MAPbI3_DOS-ALPHA_k$i-1.pdos
        mv smeared.dat smeared_alpha_$i.dat

        python get-smearing-pdos.py MAPbI3_DOS-BETA_k$i-1.pdos
        mv smeared.dat smeared_beta_$i.dat

        python get-smearing-pdos.py MAPbI3_DOS-ALPHA_k$i-1.pdos MAPbI3_DOS-BETA_k$i-1.pdos
        mv smeared.dat smeared_both_$i.dat    
    fi
done
cd ../../
done

source /Users/mac/.jackprogram/anaconda3/bin/activate base