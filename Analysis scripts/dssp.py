import mdtraj as md
import numpy as np
from sys import argv
if len(argv)==1: 
   print __doc__
   exit()
   
# Name of topology file
top_name = argv[1]
# Name of trajectory
traj_name = argv[2]
# Output file name stem
out_stem = argv[3]

# Import trajectory
traj = md.load_xtc(traj_name,top_name)

# compute % helicity 
helicity=[] #whole complex 
helicitycount=md.compute_dssp(traj)
for i in helicitycount:
	helicity.append(sum(i=='H')/float(73))
np.savetxt(out_stem+'_helicity.txt',helicity)

helicity_ntail=[] #ntail only 
for i in helicitycount:
	helicity_ntail.append(sum(i[53:74]=='H')/float(21))
np.savetxt(out_stem+'_ntail_helicity.txt',helicity_ntail)

	
	

