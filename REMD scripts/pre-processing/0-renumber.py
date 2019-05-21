# ChuHui'19 
# this file renumbers NTail-XD residues starting from 1

import os 
import chimera
from chimera import runCommand as rc
from sys import argv
directory= argv[2]
protein=argv[3]

##########################################

#enter working directory here
os.chdir(directory)   

############################################

rc("open " + protein) 
# change chains as necessary
#rc ("changechains A B :.a")
#rc("changechains X A :.x")
#add hydrogens as necessary
rc ("addh")
# renumber residues 
rc("resrenumber 1 #0:.A; resrenumber 53 #0:.B")
rc("write format pdb #0 " + protein[:-4]+"_renumber.pdb")
rc("close all")
rc("stop")
	





