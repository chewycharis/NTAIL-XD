# ChuHui '19

########## READ ME PLEASE ~  ##############################################
# WARNING: This file CANNOT deal with pdb with solvents. 
#  
#  This file is designed to be run prior to starting first step of gromacs; it generates a pdb file upon execution. 
# 
#  This file is designed to do 3 things: 
#  1. To check if there are any "WEIRD" residues  -- "weird" as in has an extra atom or has a wrong element
# 2. To replace names of RESIDUES if they are different from the names listed on the forcefield RTP file 
# 3. To replace names of ATOMS if they are different from names from the RTP file 
#     Note: 2 and 3 will only be accomplished for residues that are not "weird", i.e. 1 turns out fine
#
#  This file is divided into 4 sections :
#  A - class definitions; B - build dictionaries; C - find differently named atoms; D - replace them
#
#  Forcefields that have used this script so far: 
# 1. CHARMM36:  To run this file for CHARMM36, change file_directory , PDB_FILE, and RTP_FILE
# 2. AMBER: To run this file for AMBER, change file_directory, PDB_FILE, and RTP_FILE,  
#                   uncomment section B 2.1 FOR AMBER FORCEFIELD ONLY part, 
#                   and then change HSD (CHARMM36's name for histidine) to HID (AMBER's name). 
#
#  Other places that you might want to edit:
#  a. Section B 2.1 wanted list -- if you want to modify more residues's protonation states, see code for HIS
#  b. Section B2.1 and D 1 alert statements --you might want to change what you will be alerted to; current setting
#      reports missing atoms, atoms of the wrong element, residue name changes, and non hydrogen atom name changes 
#####################################################################

import os
import re
import math
from itertools import chain 
from shutil import copyfile
from fileinput import FileInput
from copy import copy
from string import replace
from string import rstrip 
from sys import argv

file_directory=argv[1]
os.chdir(file_directory)
PDB_FILE = argv[2] 
RTP_FILE = argv[3]  
PDB_FILE_ATOMS_CORRECTED = PDB_FILE[:-4]+"_corrected.pdb"




# A. START CLASS DEFINITIONS

# the classes Atom and Residue are results of section A.
# Atom object has attributes (name, aminoacid, element, atomnumber=None,residuenumber=None,chain=None)
# Residue object has atrributes (aminoacid, residuenumber=None,chain=None)

#### 1. DEFINE CLASS Atom ####
class Atom:
        def __init__(self, name, aminoacid, element, atomnumber=None,residuenumber=None,chain=None):
                self.atomnumber=atomnumber      #e.g. 8
                self.name=name                           #e.g. H1
                self.aminoacid=aminoacid                #e.g. SER
                self.element=element                     #e.g. H
                self.residuenumber=residuenumber  #e.g. 660
                self.chain=chain
        def __repr__(self):
                return ( str(self.name) )

#### 2. DEFINE CLASS Residue ####
class Residue:
        def __init__(self, aminoacid, residuenumber=None,chain=None):
                self.aminoacid=aminoacid		   #e.g. SER
                self.residuenumber=residuenumber	   #e.g. 661
                self.chain=chain
                self.atom=[]                               #e.g. [name,atom#: N , 7, name,atom#: CA , 8...]
        def __repr__(self):
                return str(self.aminoacid)+str(self.residuenumber)
        def atomlist(self,atom_dict):  #attach atoms to residue
                for atomnumber in atom_dict:
                        if atom_dict[atomnumber].aminoacid ==self.aminoacid and  atom_dict[atomnumber].residuenumber ==self.residuenumber:
                                self.atom.append(atom_dict[atomnumber])
                                
#END CLASS DEFINITIONS
				



# B. START DICTIONARIES

# Section B builds 4 dictionaries: NiV_residue_dict, NiV_atom_dict, FF_residue_dict, FF_atom_dict
# the first two belong to the pdb file you want to correct atom names
# the second two belong to the forcefield 

## 1. NiV DICTIONARIES 

#### 1.1 GET NIV FILE DATA ####
with open(PDB_FILE) as pdb: 
        list1=[]       # contains only lines that describe an atom e.g. not CONECT or TER 
        for line in pdb:
                if 'ATOM' in line: list1.append(line) 

#### 1.2 BUILD NIV ATOM and RESIDUE DICTIONARIES ####
i=0 ; j=1
NiV_atom_dict=dict()     # key = atom number  and value = object Atom 
NiV_residue_dict=dict()  # key = residue number and value = object Residue 
helper_list=[]          #tracks residue number
while i< len(list1):
        sp= list1[i].split()
        if 'MSCN' in sp[3]:          #'MSCN', not 'MSCNB'; correct python split mistake
               NiV_atom_dict[i+1]=Atom( sp[2], sp[3][:-1], sp[-1][0], int(sp[1]), int(sp[4]), sp [3][-1] )
               if sp[4] not in helper_list: helper_list.append(sp[4]) ; NiV_residue_dict[ j ]=Residue(sp[3][:-1],int(sp[4]), sp[3][-1]); j+=1
        else:
                NiV_atom_dict[i+1]=Atom(sp[2], sp[3], sp[-1][0], int(sp[1]), int(sp[5]), sp[4])
                if sp[5] not in helper_list: helper_list.append(sp[5]) ; NiV_residue_dict[ j ]=Residue(sp[3],int(sp[5]), sp[4]); j+=1
        i=i+1
for residuenumber in NiV_residue_dict: #add atoms to residues
        NiV_residue_dict[ residuenumber ].atomlist(NiV_atom_dict)

## 2. Forcefield DICTIONARIES 

#### 2.1 GET USEFUL(RESIDUES ACTUALLY IN PDB) FORCEFIELD FILE DATA #### 

#################################################
# WARNING: BE CAREFUL FO WHAT YOU WISH FOR these particular residues:     
# 1.HIS - HIP or HID? (HIS is NOT an option) ; 2. CYS- CYS, CYM or CYX?;  
# 3.ARG - ARG or ASH?                                   ; 4. GLN - GLH or GLN?       
#################################################

nivres=[]
ffres=[]
wanted_list=[] #contains residues
"""
#AMBER FORCEFIELD ONLY 
for residuenumber in NiV_residue_dict:  # First get the terminal residues 
        res=NiV_residue_dict[ residuenumber ] #res is a Residue        
        #N terminal statements
        state2= (residuenumber == 1 and res.aminoacid != 'ACE' ) # first residue and no acetylation 
        state3= (residuenumber  != 1 and NiV_residue_dict[ residuenumber - 1].chain != res.chain and NiV_residue_dict[ residuenumber].aminoacid != 'ACE' )
        # not first residue, chain changed and no acetylation
        
        #C terminal statements 
        t = len(NiV_residue_dict)
        state5 = (residuenumber==t and res.aminoacid != 'NME') # last residue and no C terminal amidation 
        state6= (residuenumber !=t and NiV_residue_dict[residuenumber+1].chain != res.chain and NiV_residue_dict[ residuenumber].aminoacid !='NME')
        # not last residue, chain changed and no amidation
           
        if  state2 or state3:                  # N terminal residues                
                if res.aminoacid not in wanted_list:                        
                        nivres.append(copy(res))
                        for x in NiV_atom_dict:
                                if NiV_atom_dict[x].residuenumber==res.residuenumber: NiV_atom_dict[x].aminoacid='N'+ NiV_atom_dict[x].aminoacid
                        res.aminoacid='N'+ res.aminoacid ; ffres.append(copy(res))
                        wanted_list.append(res.aminoacid)

        elif state5 or state6:                 # C terminal residues
                if res.aminoacid not in wanted_list: 
                        nivres.append(copy(res))
                        for x in NiV_atom_dict:
                                if NiV_atom_dict[x].residuenumber==res.residuenumber: NiV_atom_dict[x].aminoacid='C'+ NiV_atom_dict[x].aminoacid
                        res.aminoacid='C'+ res.aminoacid ; ffres.append(copy(res))
                        wanted_list.append(res.aminoacid)
"""

for residuenumber in NiV_residue_dict:  # now get the rest of the residues 
        res=NiV_residue_dict[ residuenumber ] #res is a Residue
        if res.aminoacid not in wanted_list:
                
                if res.aminoacid == 'HIS':                  # Histidines   
                        nivres.append(copy(res)) 
                        for x in NiV_atom_dict:
                                if NiV_atom_dict[x].aminoacid=='HIS': NiV_atom_dict[x].aminoacid='HSD' #default state is 'HSD'
                        res.aminoacid='HSD'
                        wanted_list.append(res.aminoacid) ; ffres.append(copy(res))
                                # Add more branches if you want to edit other residues
                else:
                        wanted_list.append(res.aminoacid) 

#### 2.2 Build Forcefield Atom and Residue Dictionaries ####
with open(RTP_FILE) as ff: 
        ffdata=ff.read()
c=0;
indatom=1 ; indresidue=1
FF_atom_dict=dict()
FF_residue_dict=dict()

while c < len(wanted_list):
        p1="\[ "+str(wanted_list[c])+" \](.*?)bonds \]" ; c=c+1 #look for paragraph between [residue] and [bond]
        p2= ";(.*?)\[" #look for comments which start ;
	line1=re.search(p1,ffdata,re.DOTALL).group() [:-9] #one residue's atoms' info
        search=re.search(p2,line1,re.DOTALL) #get rid of comments
	if type(search) != type(None): line1=line1.replace(search.group()[:-3],"")
	splist=line1.split()
        FF_residue_dict[ indresidue ]= Residue(splist[1]); indresidue+=1 #build residue_dict
        c1=6
        while c1 < len(splist)-1:
                FF_atom_dict[ indatom ] = Atom(splist[c1],splist[1],splist[c1][0]); #build atom_dict
                indatom+=1; c1+=4 

for residuenumber in FF_residue_dict: 
        FF_residue_dict[ residuenumber ].atomlist(FF_atom_dict) #add atoms to residues



def check_residue_dictionary(dictionary,aminoacid): #outputs the amino acid's atom list 
        for x in dictionary:
                if dictionary[x].aminoacid == aminoacid: 
                        print(x)


#END DICTIONARIES




# C. START DIFFERENT ATOMS' LISTS

# niv and ff are the reasons for section C.
# they are two atom lists with same indices, i.e. niv[0] corresponds with ff[0]
# if an atom is listed on these lists, it is named differently in pdb file than from the forcefield file 

## 1. Define Functions 

#### 1.1 Creat Lists of Differently Named Atoms (Being Same Elements and In the Same Residues)  #### 

def sort(niv):
        #sorts lists of niv and ff such that they match 
        niv.sort(key=lambda x:x.name)          #sort by name (i.e. HE goes before HG)
        niv.sort(key=lambda x:x.name[1:])      #sort by 1st number after characters (i.e. 2H1 goes before 1H2)
        for x in niv:                                       # if name doesn't contain number, move to back of list 
                if type(re.search('\d', x.name)) == type(re.search('\d', 'H')): #NoneType
                        niv.remove(x)
                        niv.append(x)
        return niv

def compare_atoms(niv, ff):
        # generate lists of different atoms 
         # precondition: lists here should have same number of atoms that are the same element 
        same_list=[]
        for x in niv[:]:
                for y in ff[:]: 
                        if y.name ==x.name:
                                same_list.append([x,y]);    niv.remove(x);   ff.remove(y)
        if len(niv)!=0: # some atoms are named differently
                ff = sort(ff)
                niv=sort(niv)
                return  niv, ff 

#### 1. 2 Creat Lists of Atoms (Being Same Elements and In the Same Residues) ####

def helper_element_list(atomlist):
        # make lists that only contain atoms being the same elment in the same residue 
        newlist=[  atomlist[0]  ]
        for atom in atomlist[1:]:
                if atom.element ==atomlist[0].element:
                        newlist.append(atom); atomlist.remove(atom)
        atomlist.remove(atomlist[0])
        return  atomlist,newlist

def element_list(niv_atomlist,ff_atomlist):
        # creates 2 lists for niv and ff, where the lists only contain atoms being the same elment
        # precondition: the two  lists should have the same number of each element and are sorted
        returnlist0=[]; returnlist1=[]
        while len(niv_atomlist) > 0:  
                n=helper_element_list(niv_atomlist)[:] ;       niv_atomlist=n[0] ;  new_niv_atomlist=n[1]
                f=helper_element_list(ff_atomlist)[:];          ff_atomlist=f[0];   new_ff_atomlist=f[1]
                #compare_atoms(new_niv_atomlist,new_ff_atomlist)
                if compare_atoms(new_niv_atomlist,new_ff_atomlist)!=None:       # something is different
                        x= compare_atoms(new_niv_atomlist,new_ff_atomlist)
                        for n in x[0]:  returnlist0.append( n)
                        for f in x[1]: returnlist1.append( f)
        return returnlist0,returnlist1

def compare_aminoacid(niv_atomlist, ff_atomlist): 
        #filters out residues that have unusual atoms numbers or types (in comparison to forcefield)
        # precondition: the lists should have atoms belonging to the same residue
        if len(niv_atomlist) != len(ff_atomlist):   # check number of atoms 	
                print( "\n check for missing atoms in " + niv_atomlist[0].aminoacid +" "+ str(niv_atomlist[0].residuenumber)+" !!! \n")
		print niv_atomlist; print ff_atomlist
        else:
                newff=ff_atomlist[:]
                for x in niv_atomlist:          # check number of each element. 
                    for y in newff:  
                        if y.element == x.element:
                                newff.remove(y)
                if len(newff) !=0 :
                        print( niv_atomlist[0].aminoacid +" "+ str(niv_atomlist[0].residuenumber)+" has an element that is not usually found in " + niv_atomlist[0].aminoacid + "." )
			print(niv_atomlist)
			print(ff_atomlist)
                else:                                      #sort list by element 
                        niv_atomlist.sort(key=lambda niv: niv.element);ff_atomlist.sort(key=lambda ff: ff.element)
                        return element_list(niv_atomlist, ff_atomlist)     # passes a 'sorted' list of atoms for one residue

## 2. Execute previously defined functions 

x=1;
diff = [] ; niv=[] ; ff=[]
while x <len(NiV_residue_dict)+1:
        y=1
        while y< len(FF_residue_dict)+1:
                if NiV_residue_dict[x].aminoacid == FF_residue_dict[y].aminoacid:
                        NiVlist = NiV_residue_dict[x].atom[:] ; FFlist= FF_residue_dict[y].atom[:]

                        newpair= compare_aminoacid(NiVlist, FFlist)   #passes a list of atoms for one residue
                        if newpair !=None:                                           #can get None if residue has wrong number of each type of atoms
                                niv.append(newpair[0]); ff.append(newpair[1])
                                
                                
                y+=1
        x+=1



niv=list(chain.from_iterable(niv))
ff=list(chain.from_iterable(ff))



# END DIFFERENT ATOMS' LISTS





# D. START REPLACE DIFFERENTLY NAMED ATOMS AND RESIDUES

# This the final step of this algorithm :) 
# As section title suggests, it replaces all the atoms that have been listed as different 
# Note: atoms that come from residues with unusual number of atoms or types of atoms are not checked,
#           but I am sure there're not too many of those, and you will be notified on terminal if that's the case. 

#### 1. WRITE REPLACE FUNCTIONS ####
alert_statements = [] 
def replace_atom (line):
        counter = 0 
        for atom in niv:
                thingy = ('ATOM' in line and ' '+str(atom.atomnumber)+' ' in line and ' '+atom.name+' ' in line and atom.chain in line and str(atom.residuenumber )+' ' in line and ' '+atom.element in line)
                if  thingy :                       
                        i= niv.index(atom)
                        # nontrivial switch 
                        if atom.element !='H':  alert_statements . append ("ALERT: "+ atom.name+' in '+ atom.aminoacid+str(atom.residuenumber)+' in chain '+atom.chain + ' has been replaced by '+ff[i].name + " !!! \n")
                        old= line[11:17] ; new = ff[i].name.center(6, ' ')                                
                        line = replace (line, old, new )  ; niv.remove(niv[i]); ff.remove(ff[i])
                        print line.rstrip('\n')
                        counter +=1 
                        break
                else:
                        continue
        if counter == 0 :   print line.rstrip('\n') 

def replace_residue(line):
        counter2=0
        for residue in nivres:
                thingy = ('ATOM' in line and residue.aminoacid in line and residue.chain in line  and str(residue.residuenumber) in line )
                if  thingy:
                        i= nivres.index(residue)
                        # I consider all residue name changes to be nontrivial  
                        alert_statements.append( "ALERT: "+ residue.aminoacid+str(residue.residuenumber)+' in chain '+residue.chain + ' is being replaced by '+str(ffres[i].aminoacid) + " !!! \n")
                        old= line[16:21]  ;  new = ffres[i].aminoacid.center(5, ' ')
                        line= replace (line,old,new)  
                        print line.rstrip('\n')
                        counter2 +=1
                        break
                else:
                        continue
        if counter2 == 0 : print line.rstrip('\n')
                                 


#### 2.  EXECUTE REPLACE FUNCTIONS ####
                        
copyfile( PDB_FILE, PDB_FILE_ATOMS_CORRECTED )  #avoids accidentally destroying your original file
tired=FileInput( PDB_FILE_ATOMS_CORRECTED, inplace=1 )

for line in  tired:
        replace_residue(line)
tired.close()

verytired=FileInput( PDB_FILE_ATOMS_CORRECTED, inplace=1 )
for line in verytired:
        replace_atom(line)
verytired.close()

number=0         # this last part prints all the alert statements accumulated in section D
alert_statements = list(set(alert_statements))
while number < len(alert_statements):  
        print alert_statements[number]; number +=1 







