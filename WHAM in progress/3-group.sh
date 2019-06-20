#!/bin/bash

a=(0 30 60 90 120 150 180)
protein=NIV-NTAIL-XD-parallel
declare -a a


for i in ${a[@]};
	do 
	for j in ${a[@]};
		do 
#		echo 'NIV-NTAIL-XD-parallel_'${i}'-'${j} | bash ~/script/2-md_and_remd_STAMPEDE2/3-gromacs_preparation.sh
		
		## include dihedral restraint ##
		cd ${HOME}/Desktop/${protein}_ALA66/${protein}_${i}-${j}
                awk "/${protein}_${i}-${j}_topol_Protein_chain_B.itp/"'{print; print "#include \"dihrestraint.itp\" "; next}1' ${protein}_${i}'-'${j}_topol.top > ${protein}-${i}-${j}-umbrella.top

               (echo a CA CB SD CE \& r MSCN; echo q;) | gmx make_ndx -f ${protein}_${i}-${j}_solv_ions.gro -o ${protein}-${i}-${j}-dihedral1.ndx
               (echo a N CA CB SD \& r MSCN; echo q;) | gmx make_ndx -f ${protein}_${i}-${j}_solv_ions.gro -o ${protein}-${i}-${j}-dihedral2.ndx
               dihndx1=$(tail -n 1 ${protein}-${i}-${j}-dihedral1.ndx)
               dihndx2=$(tail -n 1 ${protein}-${i}-${j}-dihedral2.ndx)
		(echo [ dihedral_restraints ]; echo \; ai  aj  ak  al  type  phi  dphi  kfac; echo \;CA-CB-SD-CE; echo $dihndx1 1 $i 0 30; echo \;N-CA-CB-SD; echo $dihndx2 1 $j 0 30;) > dihrestraint.itp
		
		done
	done 
 

