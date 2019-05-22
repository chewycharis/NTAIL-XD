# Adapted from Rosalind Xu 18'#
# ChuHui'19 
# to use this file, first edit directory, protein and residue_numbers, then simply type this in terminal: chimera 0-add_mscn.py

import os 
import chimera
import re
from chimera.molEdit import addAtom, addBond
from chimera import Element, Point, Bond
from chimera import runCommand as rc
from chimera import replyobj
from chimera import openModels, Molecule, Element, Coord
from math import radians, sin, cos

#############################################################################
directory='/home/chuhui/Desktop'
#enter working directory here
os.chdir(directory)  

residue_numbers=[":57.B"]    
#,":476.B",":477.B",":479.B",":481.B",":483.B",":484.B",":485.B",":487.B",":488.B",":491.B"
# residues to switch to MSCN 

protein='NIV-NTAIL-XD-parallel.pdb'
#pdbfile with .pdb extension  

foldername=protein[:-4]+"_probe_in"
os.mkdir(foldername)

##############################################################################

#define the "CN residue"
def createCN(): 						
	cn= Molecule() 	# create an instance of a molecule
	# r = cn.newResidue(residue type, chain identifier, sequence number, insertion code)
	r = cn.newResidue("cn", " ", 1, " ")
	# now create the atoms of the residue. 
	atomC = cn.newAtom("CE", Element("C")) 				
	atomN = cn.newAtom("NF", Element("N"))
	bondLength_cn = 1.156
	atomC.setCoord(Coord(0, 0, 0))
	atomN.setCoord(Coord(bondLength_cn, 0, 0))
	r.addAtom(atomC)
	r.addAtom(atomN)
	cn.newBond(atomC, atomN)
	openModels.add([cn])


for res in residue_numbers:
	fn = protein[:-4]+"_"+str(int(res[1:3])+1)
	replyobj.status("Processing " + fn) # print current file 

	#Append CN Probe	
	createCN()	# creates CN "residue"
	rc("open " + protein) 
	rc("swapaa cys " + res)
	rc("show:cys; ~ribbon")
	rc("combine #0#1 close true")
	rc("bond #2:cn@CE#2:CYS@SG")
	rc("adjust length 1.688 #2:CYS@SG#2:cn@CE")
	rc("adjust angle 100.6 #2:cn@CE#2:CYS@SG#2:CYS@CB")
	rc("adjust angle 177.80 #2:cn@NF#2:cn@CE#2:CYS@SG")
	#Caution in adjust angle: if you want atom A to be moved and atom B to be fixed,
	# list atom A before atom B. And always check structure in graphic interface!
	rc("select #2:CYS@SG")
	cys = chimera.selection.currentResidues()[0]
	rc("select #2:cn@CE")
	cn = chimera.selection.currentResidues()[0]
	for a in cn.atoms:
		cn.removeAtom(a)
		cys.addAtom(a)
	cys.type = "MSCN"
	cn.molecule.deleteResidue(cn)
	s = cys.findAtom("SG")
	cys.removeAtom(s)
	s.name = "SD"
	cys.addAtom(s)

	#Add missing hydrogens to MSCN
	rc("addh spec #2:MSCN hbond true" ) 

	# relabels MSCN as ATOM not HETATM
	rc("~select; select #2:MSCN @ *") 
 	atoms=chimera.selection.currentAtoms()
	for a in atoms: 
		chimera.PDBio.addStandardResidue(a.residue.type)
	rc("~select; select #2:HSD @ *") 
 	atoms=chimera.selection.currentAtoms()
	for a in atoms: 
		chimera.PDBio.addStandardResidue(a.residue.type)
	# renumber residues 
	rc("resrenumber 1 #2:.A; resrenumber 53 #2:.B")

	# Write file 
	rc("write format pdb #2 " + foldername+"/"+fn+".pdb")
	
	rc("close all") #close all files associated with one mutant before making the next one
rc("stop")




"""
	#Edit Acetate ( comment this section out if structure doesn't come from a trajectory file) 
	#pymol is very unhappy with OT's and refuse to do amidation if OT's exist
	#I think it doesn't want to replace anything besides H with other atoms,
	#so if c has 4 bonds with 4 non H atoms, pymol can't make carbon have 5 bonds  
	#NTail	
	rc("select #2:71.b")
	ser= chimera.selection.currentResidues()[0]
	#gets rid of OT2	
	ot2b = ser.findAtom("OT2")
	ser.removeAtom(ot2b)
	#renames OT1
	ot1b = ser.findAtom("OT1")
	ser.removeAtom(ot1b)
	ot1b.name="O"
	ser.addAtom(ot1b)
	#XD
	rc("select #2:50.a")
	ile= chimera.selection.currentResidues()[0]
	#gets rid of OT2	
	ot2a = ile.findAtom("OT2")
	ile.removeAtom(ot2a)
	#renames OT1
	ot1a = ile.findAtom("OT1")
	ile.removeAtom(ot1a)
	ot1a.name="O"
	ile.addAtom(ot1a)


"""

	





