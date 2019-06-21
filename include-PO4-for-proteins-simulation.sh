!/bin/bash 

pdbID=protein 

# 0. Use CHARMM-GUI ligand modeler to generate parameters for PO4 ion 
# 1. create residue entry in .rtp file for PO4 based on .rtf file; set chargegroup as 1 for all atoms of the residue 
# 2. append #include "PO4.itp" to ions.itp and add PO4 as an ion to residuetypes.dat (this step might not be necessary) 
# 3. run the following commands to generate .gro and topology files for both protein and PO4, then put protein in a box, and then put PO4 into the protein's box. 

(echo 3; echo 4; echo 3; echo 4) | gmx pdb2gmx -f $pdbID".pdb" -o $pdbID"_processed.gro" -p $pdbID"_topol.top" -water tip3p -ff charmm36m -ter
gmx pdb2gmx -f ligandrm.pdb -o po4.gro -p po4_topol.top -ff charmm36m -water tip3p
gmx editconf -f $pdbID"_processed.gro" -o $pdbID"_box.gro" -c -d 1 -bt dodecahedron  

# 4. manually calculate number of ions to add by considering size of the box, which can be calculated based on box's vectors; i.e. Vol*Conc=#mol
# 5. insert polyatomic ions 
gmx insert-molecules -f protein_box.gro -ci po4.gro -nmol 19 -o protein_po4.gro

# 6. append PO4 nmol (in this case 19) to the end of the topology file 
# 7. run the following commands to solvate the box; remember to change NA concentration   
gmx solvate -cp $pdbID"_po4.gro" -cs spc216.gro -o $pdbID"_solv.gro" -p $pdbID"_topol.top"
gmx grompp -f ~/mdp/0-mini-steep-frozen.mdp -c $pdbID"_solv.gro" -p $pdbID"_topol.top" -o $pdbID"_ions.tpr"
echo 15 | gmx genion -s $pdbID"_ions.tpr" -o $pdbID"_solv_ions.gro"  -p $pdbID"_topol.top" -pname NA -nname CL -nn 0 -np 58


