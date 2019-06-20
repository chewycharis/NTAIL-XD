#!/bin/bash 
# ChuHui'19 
# This script makes remd.mdp and nvt-remd.mdp for REMD 
# if you see a bunch of temp files from sed don't get scared. they will go away on their own. 
cd $HOME/mdp
#Paccept = 0.15 
temp=(300.00 302.43 304.88 307.34 309.82 312.31 314.81 317.34 319.87 322.43 325.00 327.58 330.18 332.80 335.43 338.08 340.74 343.42 346.12 348.84 351.57 354.32 357.08 359.88 362.68 365.49 368.32 371.17 374.04 376.93) 
#make 6-nvt-remd-x.mdp
#mkdir 6-nvt-remd
nvt_temp=$(grep ref-t 6-nvt-remd.mdp)
gen_temp=$(grep gen-temp 6-nvt-remd.mdp)
for x in ${!temp[@]}; do             # {!array[@]} returns list of index
	cp 6-nvt-remd.mdp 6-nvt-remd-$x.mdp
	sed -i -e "s/$nvt_temp/ref-t=${temp[$x]} ${temp[$x]} /g" 6-nvt-remd-$x.mdp
	sed -i -e "s/$gen_temp/gen-temp=${temp[$x]}/g" 6-nvt-remd-$x.mdp
	mv 6-nvt-remd-$x.mdp 6-nvt-remd/
done 



#make 7-remd-x.mdp
mkdir 7-remd
md_temp=$(grep ref-t 7-remd.mdp)
for x in ${!temp[@]}; do             
	cp 7-remd.mdp 7-remd-$x.mdp
	sed -i -e "s/$md_temp/ref-t=${temp[$x]} ${temp[$x]}/g" 7-remd-$x.mdp
	mv 7-remd-$x.mdp 7-remd/
done 


	 




