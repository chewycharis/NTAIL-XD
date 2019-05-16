# ChuHui'19
# Sources: "Effect of Ca2+ on the promiscuous target-protein binding of calmodulin" https://doi.org/10.1371/journal.pcbi.1006072

import mdtraj as md
import numpy as np
import itertools as it
from sklearn import metrics
from datetime import datetime 
starttime=datetime.now()

"""
# file input
from sys import argv
if len(argv)==1: 
   print __doc__
   exit()
xtc=argv[1]
topology=argv[2]
protein=argv[3]

xtc='traj.xtc'
topology='FPD_ZTranslate_5_remd_protein.gro'
protein='FPD_ZTranslate_5'


# define trajecotry
traj=md.load(xtc, top=topology) 
"""
index=traj.topology.select('name CA')
trajCA=traj.atom_slice(index)
if traj.n_atoms > 1156: #make sure trajectory excludes solvent 
   print("please include only protein in trajectory.")
   exit()
print("it took "+str(datetime.now()-starttime)+" to load trajectory.")


# inverse interatomic distance 
def iiad(traj):
    starttime2=datetime.now()
    print("starting inverse interatomic distance calculations...")
    atom_list=tuple(range(0,traj.n_atoms)) # e.g. (0,1,...,n-1)
    print("atom indices have been generated")
    atom_pairs=tuple(it.combinations(atom_list,2)) # e.g. ((0,1),(0,2),...,(n-1,n-2))
    print("atom pairs have been compared: ")
    iiad=1/(md.compute_distances(traj,atom_pairs)) 
    print("Inverse interatomic distances have been computed.")
    print("It took " + str(datetime.now() - starttime2)+" to compute them." )
    #np.savetxt(protein+"_iiad.txt",iiad,fmt='%.8f')
    return iiad

# frame to frame distance 
def ffd(iiad):
    print("starting frame-to-frame distance calculations...")
    starttime3=datetime.now()
    ffd=metrics.pairwise.euclidean_distances(iiad)
    # frame to frame distance array, distances listed as ((0,1),(0,2),(0,3)...(0,f-1),(1,2),...,(f-1,f-2))
    print("frame to frame distances have been computed.")
    print("It took " + str(datetime.now() - starttime3)+" to compute them." )
    #np.savetxt(protein+"_adjacency_matrix.txt",ffd,fmt='%.8f')
    return ffd


iiad=iiad(trajCA)
ffd=ffd(iiad)
adjacency=ffd

#to retrieve the matrix, use this command: np.loadtxt('adjacency_matrix.txt')
print("Here is the total time for running this script:")
print(datetime.now() - starttime)
