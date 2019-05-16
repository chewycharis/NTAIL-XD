#!/bin/bash

#SBATCH -J FPD_Parallel_3_equil1_remd                   # Job name
#SBATCH -o /work/05752/chuhuifu/stampede2/output_files/FPD_Parallel_3_equil1_remd.o%j               # Name of stdout output file
#SBATCH -e /work/05752/chuhuifu/stampede2/output_files/FPD_Parallel_3_equil1_remd.e%j       # Name of stderr error file
#SBATCH -p normal                           # Queue (partition) name
#SBATCH -N 1                                # Total # of nodes
#SBATCH -n 64                               # Total # of mpi tasks (or number of MPI processes)
#SBATCH -t 10:00:00                         # Run time (hh:mm:ss)
#SBATCH --mail-user=cfu@haverford.edu       # E-mail address
#SBATCH --mail-type=all                     # Send email at begin and end of job (none for no emails)
#SBATCH -A TG-MCB180055                     # Allocation name (req'd if you have more than 1)

# protein name
pdbID=FPD_Parallel_3 
workspace=$SCRATCH/REMD_092018 
storage=$WORK
cd $workspace/$pdbID

# job sript 

#### STEP 1: Energy Minimization 1 - to minimize energy of solvent and ions when they are by themselves
#gmx grompp -f $HOME/mdp/1-steep.mdp -c $pdbID"_solv_ions.gro" -p $pdbID"_topol.top" -o $pdbID"_em.tpr"
#ibrun mdrun_mpi -v -deffnm $pdbID"_em"
echo 1 | gmx trjconv -f $pdbID"_em.trr" -s $pdbID"_em.tpr" -o $pdbID"_em.pdb" -pbc mol -ur compact

#### STEP 2: NVT Equilibration - to stabilize temperature of the system 
gmx grompp -f $HOME/mdp/2-solvent-eqlb-nvt.mdp -c $pdbID"_em.gro" -p $pdbID"_topol.top" -o $pdbID"_nvt.tpr"
ibrun mdrun_mpi -v -deffnm $pdbID"_nvt"
echo 0 | gmx trjconv -f $pdbID"_nvt.trr" -s $pdbID"_nvt.tpr" -o $pdbID"_nvt.pdb" -pbc mol -ur compact -dt 10

#### STEP 3: Energy Minimization 2 - to minimize energy of the whole system 
gmx grompp -f $HOME/mdp/3-steep.mdp -c $pdbID"_nvt.gro" -p $pdbID"_topol.top" -o $pdbID"_em-post-nvt.tpr"
ibrun mdrun_mpi -v -deffnm $pdbID"_em-post-nvt"
echo 1 | gmx trjconv -f $pdbID"_em-post-nvt.trr" -s $pdbID"_em-post-nvt.tpr" -n $pdbID"_index.ndx" -o $pdbID"_em-post-nvt.pdb" -pbc mol -ur compact

#### STEP 4: Temperature Annealing -to obtain optimal structure of system (and avoid overfitting) by repeatedly cooling and heating the system 
gmx grompp -f  $HOME/mdp/4-anneal.mdp -c $pdbID"_em-post-nvt.gro" -p $pdbID"_topol.top" -o $pdbID"_temp-anneal.tpr" -maxwarn 2
ibrun mdrun_mpi -v -deffnm $pdbID"_temp-anneal"
echo 1 | gmx trjconv -f $pdbID"_temp-anneal.trr" -s $pdbID"_temp-anneal.tpr" -n $pdbID"_index.ndx" -o $pdbID"_temp-anneal.pdb" -pbc mol -ur compact -skip 10

#### STEP 5: NPT Equilibration - to stabilize system's pressure and thus its density
#switch mdp file depending on remd or md. for remd, this step is 1ns instead of 2ns. 
gmx grompp -f  $HOME/mdp/5-npt-remd.mdp -c $pdbID"_temp-anneal.gro" -p $pdbID"_topol.top" -o $pdbID"_npt.tpr"
ibrun mdrun_mpi -v -deffnm $pdbID"_npt"
#check trajectory; choose protein (group 1)
echo 1 | gmx trjconv -f $pdbID"_npt.trr" -s $pdbID"_npt.tpr" -n $pdbID"_index.ndx" -o $pdbID"_npt.pdb" -pbc mol -ur compact -skip 10

cd ..

