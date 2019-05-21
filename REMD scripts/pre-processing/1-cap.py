import os
import pymol
from pymol import cmd, stored
from sys import argv
#this file is the the second step for cyanylation.
#it caps n/c terminals of the protein with acetyl/methyl amine. 
#ChuHui'19

directory= argv[2]
protein=argv[3]

os.chdir(directory)     #working directory
cmd.load(protein)

####caps the protein####

#setup wizard 
cmd.wizard("mutagenesis")
cmd.get_wizard().set_mode('current') #keep current residue (i.e. Ala doesn't become Gly) 
cmd.get_wizard().set_n_cap('acet') #n terminal acetylation 
cmd.get_wizard().set_c_cap('nmet') #c terminal amidation 
cmd.get_wizard().set_dep('ind') # use backbone independent rotamers #because no phi/psi

#mutate residue in NTail 
cmd.get_wizard().do_select('resi 53 in chain B') #thr 473, n terminal
#use default rotamer: rotamers in pymol are listed in descending order, so the first one has the highest probability
#you change change rotamer by going into GUI lower right cornor where there are lots of "video buttons"
cmd.get_wizard().apply()
cmd.get_wizard().do_select('resi 73 in chain B') #ser 493, c terminal
cmd.get_wizard().apply()

#mutate residue in XD
cmd.get_wizard().do_select('resi 1 in chain A') #ser 660, n terminal
cmd.get_wizard().apply()
cmd.get_wizard().do_select('resi 50 in chain A') #ile 709, c terminal
cmd.get_wizard().apply()

cmd.set_wizard() #turns wizard off 

####visualization ####
cmd.select('nterm_ntail', 'resi 52 in chain B + resi 53 in chain B')
cmd.select('cterm_ntail', 'resi 73 in chain B + resi 74 in chain B')
cmd.select('nterm_xd', 'resi 1 in chain A + resi 0 in chain A')
cmd.select('cterm_xd', 'resi 50 in chain A + resi 51 in chain A')
#cmd.select("mscn", "resn MSCN in chain B")
cmd.hide('everything', 'all')
#check probe 
#cmd.show_as('sticks','MSCN')
#check caps 
cmd.show_as('sticks','nterm_ntail')
cmd.show_as('sticks','cterm_ntail')
cmd.show_as('sticks','nterm_xd')
cmd.show_as('sticks','cterm_xd')
cmd.center()

#you should actually look at this before you save the pdb file 
cmd.save(protein[:-4]+"_cap.pdb")
cmd.quit()


