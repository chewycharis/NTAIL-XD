#!/bin/bash

#########################################################################
# This script is designed to run on a local computer. 
# Script performs the following:
# 1. generate topology files
# 2. put protein in a box
# 3. solvate protein 
# 4. add ions to neutralize box
# 5. generates index file to be used for making check-point pdb files 
#########################################################################

source /packages/gromacs5/bin/GMXRC                                            #reference path to gromacs script
export GMXLIB=/homes/cfu/forcefields                #export path to charmm36 forcefield  

pdbID=NIV-NTAIL-XD-parallel
cd ~/Desktop
mkdir $pdbID; mv $pdbID".pdb" $pdbID 
cd $pdbID


#### STEP 1: Define Topology #####
# if you don't have acetylation and amidation done on the terminals, turn off -ter flag and get rid of echos. 
(echo 3; echo 4; echo 3; echo 4) | gmx pdb2gmx -f $pdbID".pdb" -o $pdbID"_processed.gro" -p $pdbID"_topol.top" -water tip3p -ff charmm36MSCN -ter
#check topology 
gmx editconf -f $pdbID"_processed.gro" -o $pdbID"_processed_checked.pdb" -pbc

##### STEP 2: Put Protein in a Box ####
gmx editconf -f $pdbID"_processed.gro" -o $pdbID"_box.gro" -c -d 1.0 -bt dodecahedron  

#### STEP 3: Put Solvent in the Box ####
gmx solvate -cp $pdbID"_box.gro" -cs spc216.gro -o $pdbID"_solv.gro" -p $pdbID"_topol.top"

#### STEP 4: Add ions to the Box --to obtain neutrality ####
gmx grompp -f ~/NTail-XD/NiV/gromacs_files/parameter_files/0-mini-steep-frozen.mdp -c $pdbID"_solv.gro" -p $pdbID"_topol.top" -o $pdbID"_ions.tpr"
echo 13 | gmx genion -s $pdbID"_ions.tpr" -o $pdbID"_solv_ions.gro"  -p $pdbID"_topol.top" -pname NA -nname CL -neutral -conc 0.2 
#check topology
gmx editconf -f $pdbID"_solv_ions.gro"  -o $pdbID"_solv_ions_checked.pdb" 

#### STEP 5: Generate Index File for Protein ####
# i.e. not water or counter ions
(echo 1; echo q;) | gmx make_ndx -f  $pdbID"_solv_ions.gro" -o $pdbID"_index.ndx"




