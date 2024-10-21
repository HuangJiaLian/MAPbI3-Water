#cp ../../7_Structure_evolution/3_structure_evolve.ipynb 7_structure_evolve.ipynb
#cp ../../6_Writing/structure_change/nofix/MAPbI3-pos-1-222.xyz MAPbI3-pos-1-222-water100p.xyz
cp ../../8_JPCLResponce/03_WaterRatioChange/VacancyLevels/level5/MAPbI3-pos-1.xyz MAPbI3-pos-1-222-water100p.xyz
#sed '/i =/ s/$/, Lattice="31.79 0.0 0.0 0.0 31.09 0.0 0.0 0.0 30.389999999999997" Properties=species:S:1:pos:R:3 pbc="F F F"/' calculation_out/222_moreSteps/MAPbI3-pos-1.xyz > calculation_out/222_moreSteps/MAPbI3-pos-1-cellAdded.xyz 
sed '/i =/ s/$/, Lattice="31.79 0.0 0.0 0.0 31.09 0.0 0.0 0.0 30.389999999999997" Properties=species:S:1:pos:R:3 pbc="F F F"/' calculation_out/222_moreSteps_1000/MAPbI3-pos-1.xyz > calculation_out/222_moreSteps_1000/MAPbI3-pos-1-cellAdded.xyz 
sed '/i =/ s/$/, Lattice="31.79 0.0 0.0 0.0 31.09 0.0 0.0 0.0 30.389999999999997" Properties=species:S:1:pos:R:3 pbc="F F F"/' MAPbI3-pos-1-222-water100p.xyz > MAPbI3-pos-1-222-water100p-cellAdded.xyz
