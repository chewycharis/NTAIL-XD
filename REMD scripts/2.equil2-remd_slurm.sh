#!/bin/bash

#SBATCH -J CABS_Model_8_equil2_remd                   # Job name
#SBATCH -o /work/05752/chuhuifu/stampede2/output_files/CABS_Model_8_equil2_remd.o%j               # Name of stdout output file
#SBATCH -e /work/05752/chuhuifu/stampede2/output_files/CABS_Model_8_equil2_remd.e%j       # Name of stderr error file
#SBATCH -p normal                           # Queue (partition) name
#SBATCH -N 3                                # Total # of nodes
#SBATCH -n 180                                # Total # of mpi tasks (or number of MPI processes)
#SBATCH -t 08:00:00                         # Run time (hh:mm:ss)
#SBATCH --mail-user=cfu@haverford.edu       # E-mail address
#SBATCH --mail-type=all                     # Send email at begin and end of job (none for no emails)
#SBATCH -A TG-MCB180055                     # Allocation name (req'd if you have more than 1)


pdbID=CABS_Model_8
copylist=($pdbID"_topol.top" $pdbID"_npt.gro" $pdbID"_em.tpr" $pdbID"_index.ndx" "*.itp")  #files needed for remd steps 

cd $SCRATCH/REMD_042019 
mkdir $pdbID"_remd"   #make a folder for REMD 
cd $pdbID"_prelim_equil"  


for label in $(seq 0 29); do    # for each replica 
	
	#make a replica folder containing necessary files
	mkdir $pdbID"_replica"$label  
	                                   
	for x in ${copylist[@]}; do cp $x  $pdbID"_replica"$label/; done
	
	cd $pdbID"_replica"$label

	#make nvt-remd.tpr files 
	gmx grompp -f $HOME/mdp/6-nvt-remd/6-nvt-remd-$label".mdp"  -c $pdbID"_npt.gro" -p $pdbID"_topol.top" -o $pdbID"_nvt_remd.tpr"                        
	
	cd .. 
	mv  $pdbID"_replica"$label  ../$pdbID"_remd"  
	 
done 	

cd .. 
#mv $pdbID $pdbID"_prelim_equil" 
cd $pdbID"_remd"

#run nvt equilibration 
ibrun mdrun_mpi -v -multidir $pdbID"_replica"[0-9] $pdbID"_replica"[1-2][0-9] -s $pdbID"_nvt_remd.tpr" -deffnm $pdbID"_nvt_remd"  

#make pdb trajectory files for final nvt equilibration 
for label in $(seq 0 29); do 
	cd $pdbID"_replica"$label	
	echo 1 | gmx trjconv -f $pdbID"_nvt_remd.trr" -s $pdbID"_nvt_remd.tpr" -o $pdbID"_nvt_remd.pdb" -pbc mol -ur compact
	cd .. 
done 

	





	 
