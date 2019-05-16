#!/bin/bash
protein=(cabs_7 cabs_8 parallel_3 yrotate_6 ztranslate_2 ztranslate_5   sonia_1 xrotate_3)  
klist=(39 14 9 9 7 6 15 2) #number of cluster -1  
cd ~/Desktop/rms
for c in $(seq 0 7);
	do 
	k=${klist[$c]}        
	pdbID=${protein[$c]} 
	for x in $(seq 0 $k);
		do
		echo  $pdbID'_'$x'_rms.xvg'
		gracebat $pdbID'_'$x'_rms.xvg' -batch ~/Desktop/grace_rmsd -nosafe
	done 
done 
