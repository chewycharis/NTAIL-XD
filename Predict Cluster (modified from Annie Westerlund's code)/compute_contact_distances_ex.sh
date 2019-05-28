#!/bin/bash

pypath=cluster_classifier_ntail-xd/
out_dir=./
top=example/xrotate_3_protein.gro
trajectories=(example/newtraj.xtc ) 


### Compute residue-residue distances
	python ${pypath}create_distance_maps.py -top ${top} -trj ${trajectories[@]} -fe xrotate_3_newtraj -od $out_dir -dt 1


