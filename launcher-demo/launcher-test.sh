#!/bin/bash
#SBATCH -J launcher-test                   # Job name
#SBATCH -o /work/05752/chuhuifu/stampede2/output_files/launcher-test.o%j               # Name of stdout output file
#SBATCH -e /work/05752/chuhuifu/stampede2/output_files/launcher-test.e%j       # Name of stderr error file
#SBATCH -p development                            # Queue (partition) name
#SBATCH -N 1                                # Total # of nodes
#SBATCH -n 2                                # Total # of mpi tasks (or number of MPI processes)
#SBATCH -t 00:05:00                         # Run time (hh:mm:ss)
#SBATCH --mail-user=cfu@haverford.edu       # E-mail address
#SBATCH --mail-type=all                     # Send email at begin and end of job (none for no emails)
#SBATCH -A TG-MCB180055                     # Allocation name (req'd if you have more than 1)

module load launcher

## set working directory and scripts to be run ##
working_directory=$SCRATCH/jobfiles
files_in_working_directory=$(cd $working_directory; ls)
num_files_expected=2
num_files_actual=$(cd $working_directory; ls -1 | wc -l)
jobscript=jobscript                #make sure you actually want to run this  

#True=1 False=0
combine_scripts=0
create_jobscript=0 


cd $working_directory
pwd



## create jobscript to run all bash scripts in working directory ##
## please make sure no other jobscript exists ##
if [ $combine_scripts -eq 1 ]
then
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
        #enter your script here
        #example
        for task in {1..10};
        do
                # each continuous line is recognized as an individual task 
                # use && if you want multiple commands to be viewed as a single task
                echo " echo \"task $task banana!!!\" && echo \"task $task is running on node \${HOSTNAME} with task ID \${LAUNCHER_TSK_ID}\" && echo \" task $task apple!!! \" "
        done >> $jobscript
fi


## set LAUNCHER environment variables ##
export LAUNCHER_PLUGIN_DIR=${LAUNCHER_DIR}/plugins
export LAUNCHER_RMI=SLURM
export LAUNCHER_JOB_FILE=$jobscript
export LAUNCHER_WORKDIR=$working_directory

## run LAUNCHER ##
$LAUNCHER_DIR/paramrun
