import mdtraj as md
import numpy as np
import argparse 
import itertools as it
from sklearn import metrics
import MD_init

# inverse interatomic distance 
def iiad(traj):
	index=traj.topology.select('name CA')
	traj=traj.atom_slice(index)

	atom_list=tuple(range(0,traj.n_atoms)) # e.g. (0,1,...,n-1)
    	atom_pairs=tuple(it.combinations(atom_list,2)) # e.g. ((0,1),(0,2),...,(n-1,n-2))
    	iiad=1/(md.compute_distances(traj,atom_pairs)) 
    	return iiad

def main(parser):
	init=MD_init.MD_initializer()
	traj,args=init.initialize_trajectory(parser)
	print('Computing all inverse-distance CA distances')
	distance_map=iiad(traj)
	np.save(args.out_directory+'inverse_CA_'+args.file_end_name+'.npy',distance_map)
	


parser=argparse.ArgumentParser(epilog='Creating distance maps used for classification.')

main(parser)
