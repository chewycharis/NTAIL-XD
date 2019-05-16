#!/bin/bash 

#SBATCH -J CABS_Model_7_remd_40ns                                             # Job name
#SBATCH -o /work/05752/chuhuifu/stampede2/output_files/CABS_Model_7_remd.o%j     # Name of stdout output file
#SBATCH -e /work/05752/chuhuifu/stampede2/output_files/CABS_Model_7_remd.e%j     # Name of stderr error file
#SBATCH -p normal                                                               # Queue (partition) name
#SBATCH -N 30                                                                   # Total # of nodes
#SBATCH -n 1920                                                                 # Total # of mpi tasks (or number of MPI processes)
#SBATCH -t 48:00:00                                                             # Run time (hh:mm:ss)
#SBATCH --mail-user=cfu@haverford.edu                                           # E-mail address
#SBATCH --mail-type=all                                                         # Send email at begin and end of job (none for no emails)
#SBATCH -A TG-MCB180055                                                         # Allocation name (req'd if you have more than 1)


pdbID=CABS_Model_7

cd $SCRATCH/REMD_042019
cp -r $pdbID"_remd" $pdbID"_remd-backup-20ns"
cd $pdbID"_remd" 

#make remd.tpr files 
for label in $(seq 0 29); do 
	cd $pdbID"_replica"$label
#gmx grompp -f $HOME/mdp/7-remd/7-remd-$label".mdp" -c $pdbID"_nvt_remd.gro" -p $pdbID"_topol.top" -o $pdbID"_remd.tpr"
	gmx grompp -f $HOME/mdp/7-remd/7-remd-$label".mdp" -c $pdbID"_remd.tpr" -p $pdbID"_topol.top" -o $pdbID"_remd-40ns.tpr"

	cd ..
done 


#run remd (current exchanging a lot since very few replica; tutorial used 1ps waiting time; current waiting time between exchange is 0.5ps)
ibrun mdrun_mpi -v -multidir $pdbID"_replica"[0-9] $pdbID"_replica"[1-2][0-9] -s $pdbID"_remd-40ns.tpr" -deffnm $pdbID"_remd" -replex 100 -cpi $pdbID"_remd.cpt" -noappend





cd $pdbID"_replica0"
#trim replica 0
#### Trajectory Trimming 1- to keep original whole molecules whole ####
#(echo 1;echo 0) | gmx trjconv -f $pdbID"_remd.trr" -s $pdbID"_em.tpr" -n $pdbID"_index.ndx" -o $pdbID"_nojump.xtc" -pbc nojump -center

#### Trajectory Trimming 2- to make protein whole by removing jumps_ ####
#(echo 1;echo 0) | gmx trjconv -f $pdbID"_nojump.xtc" -s $pdbID"_em.tpr" -n $pdbID"_index.ndx" -o $pdbID"_nojump_whole.xtc" -pbc whole -center

#### Trajectory Trimming 3- to cluster protein so that chains are together####
#(echo 1; echo 1; echo 0) | gmx trjconv -f $pdbID"_nojump_whole.xtc" -s $pdbID"_remd.tpr" -n $pdbID"_index.ndx" -o $pdbID"_nojump_whole_cluster.xtc" -pbc cluster -center

#### Trajectory Trimming 4- to pull water in and surround protein with them in box ####
#(echo 1;echo 0) | gmx trjconv -f $pdbID"_nojump_whole_cluster.xtc" -s $pdbID"_remd.tpr" -n $pdbID"_index.ndx" -o $pdbID"_nojump_whole_cluster_atom.xtc" -pbc atom -ur compact -center

#### Trajectory Trimming 5- fix broken waters and protein across periodic boundaries ####
#(echo 1; echo 0; ) | gmx trjconv -f $pdbID"_nojump_whole_cluster_atom.xtc" -s $pdbID"_remd.tpr" -n $pdbID"_index.ndx" -o $pdbID"_nojump_whole_cluster_atom_whole.xtc" -pbc whole -center


#### Generate System and Protein Trajectory pdb Files #### 
#ouput system 
#(echo 1; echo 0; ) | gmx trjconv -f $pdbID"_nojump_whole_cluster_atom_whole.xtc" -s $pdbID"_remd.tpr" -n $pdbID"_index.ndx" -o $pdbID"_md_system_trajectory.pdb" -fit rot+trans -dt 1000
#output protein 
#(echo 1; echo 1; ) |gmx trjconv -f $pdbID"_nojump_whole_cluster_atom_whole.xtc" -s $pdbID"_remd.tpr" -n $pdbID"_index.ndx" -o $pdbID"_md_protein_trajectory.pdb" -fit rot+trans -dt 100 

#check minimum distance to periodic image (expect to be >2) 
#echo 1 | gmx mindist -f $pdbID"_nojump_whole_cluster_atom_whole.xtc" -s $pdbID"_remd.tpr" -n $pdbID"_index.ndx" -od $pdbID"_remd_mindist.xvg" -pi 


#cd ..
#cp -r $pdbID"_replica0" $WORK/REMD_042019/remd_replica0/ 





	 
