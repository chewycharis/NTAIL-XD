import os
import pymol
from pymol import cmd, stored
#this file adjusts the dihedral angles of the scn probe. 
#ChuHui'19

os.chdir("/home/chuhui/Desktop")     #working directory
protein="NIV-NTAIL-XD-parallel"      #filename in working directory, w/o .pdb extension 
os.chdir(protein+"_probe_in")
cmd.load(protein+"_58.pdb")
cacb_list=[0] #dihedral angle with rotation around CA-CB bond
cbsd_list=[0,30,60,90,120,150,180,210,240,270,300,330] #dihedral angle with rotation around CB-SD bond 

### remove random bonds ###
#PyMOL might attempt to add random bonds connecting NF, CE, SD to other residues, which will prevent you from doing any rotation. 
cmd.unbond("resn mscn and name nf", "all")
cmd.bond("resn mscn and name nf", "resn mscn and name ce")

cmd.unbond("resn mscn and name ce", "all")
cmd.bond("resn mscn and name sd", "resn mscn and name ce")
cmd.bond("resn mscn and name nf", "resn mscn and name ce")

cmd.unbond("resn mscn and name sd", "all")
cmd.bond("resn mscn and name sd", "resn mscn and name ce")
cmd.bond("resn mscn and name sd", "resn mscn and name cb")
####change dihedral angles####
for x in cacb_list:
	cmd.set_dihedral("resn mscn and name C", "resn mscn and name CA", "resn mscn and  name CB", "resn mscn and name SD", x)
	for y in cbsd_list:
		cmd.set_dihedral("resn mscn and name CA", "resn mscn and name CB", "resn mscn and  name SD", "resn mscn and name CE", y)
		cmd.save(protein+"_"+str(x)+"-"+str(y)+".pdb")
# remember to look at these files to make sure they look right. :) 





