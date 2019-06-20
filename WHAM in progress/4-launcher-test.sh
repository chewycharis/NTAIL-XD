#!/bin/bash
#SBATCH -J launcher-equil                   # Job name
#SBATCH -o /work/05752/chuhuifu/stampede2/output_files/launcher-test.o%j               # Name of stdout output file
#SBATCH -e /work/05752/chuhuifu/stampede2/output_files/launcher-test.e%j       # Name of stderr error file
#SBATCH -p normal                            # Queue (partition) name
#SBATCH -N 2                                # Total # of nodes
#SBATCH -n 98                                # Total # of mpi tasks (or number of MPI processes)
#SBATCH -t 24:00:00                         # Run time (hh:mm:ss)
#SBATCH --mail-user=cfu@haverford.edu       # E-mail address
#SBATCH --mail-type=all                     # Send email at begin and end of job (none for no emails)
#SBATCH -A TG-MCB180055                     # Allocation name (req'd if you have more than 1)

module load launcher

## set working directory and scripts to be run ##
working_directory=$SCRATCH/NIV-NTAIL-XD-parallel_ALA66
jobscript=jobscript-062019                #make sure you actually want to run this  

#True=1 False=0
combine_scripts=0
create_jobscript=1 


cd $working_directory
pwd



## create jobscript to run all bash scripts in working directory ##
## please make sure no other jobscript exists ##
if [ $combine_scripts -eq 1 ]
then
files_in_working_directory=$(cd $working_directory; ls)
num_files_expected=0
num_files_actual=$(cd $working_directory; ls -1 | wc -l)
	if [ $num_files_expected -ne $num_files_actual ] #sanity check
	then
		echo "you might have set up the wrong directory";
		echo "is this the directory you want to be working in?";
		echo  $working_directory;
		echo "do you want to run all of these files?";
		echo  $files_in_working_directory;
		exit
	else  
		for file in $files_in_working_directory; 
		do
        		echo "bash $file"
		done >> $jobscript 
	fi
fi

## create jobscript here ##
if [ $create_jobscript -eq 1 ]
then
protein=NIV-NTAIL-XD-parallel
a=$(seq 0 30 180)
        #enter your script here
        #example
        for i in $a;
        do
                for j in $a;
                do
                        echo "pdbID=${protein}_${i}-${j} && cd ${working_directory} && cd \${pdbID} && gmx grompp -f \${HOME}/mdp/umbrella/1-steep.mdp -c \${pdbID}_solv_ions.gro -p \${pdbID}-umbrella.top -o \${pdbID}_em.tpr && ibrun mdrun_mpi -v -deffnm \${pdbID}_em && gmx grompp -f \${HOME}/mdp/umbrella/2-solvent-eqlb-nvt.mdp -c \${pdbID}_em.gro -p \${pdbID}-umbrella.top -o \${pdbID}_nvt.tpr && ibrun mdrun_mpi -v -deffnm \${pdbID}_nvt && gmx grompp -f  \${HOME}/mdp/umbrella/5-npt-remd.mdp -c \${pdbID}_nvt.gro -p \${pdbID}-umbrella.top -o \${pdbID}_npt.tpr && ibrun mdrun_mpi -v -deffnm \${pdbID}_npt"
                done
        done >> $jobscript

fi



## set LAUNCHER environment variables ##
export LAUNCHER_PLUGIN_DIR=${LAUNCHER_DIR}/plugins
export LAUNCHER_RMI=SLURM
export LAUNCHER_JOB_FILE=$jobscript
export LAUNCHER_WORKDIR=$working_directory

## run LAUNCHER ##
$LAUNCHER_DIR/paramrun
