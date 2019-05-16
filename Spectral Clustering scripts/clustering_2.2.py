# ChuHui'19
# Sources: "Effect of Ca2+ on the promiscuous target-protein binding of calmodulin" https://doi.org/10.1371/journal.pcbi.1006072

import mdtraj as md
import numpy as np
import itertools as it
from sklearn import metrics
from sklearn.cluster import KMeans
import os
import math
from datetime import datetime 
starttime=datetime.now()
from sys import argv


# 5. choose first k eigenvectors and normalize them by row  
u=eigenvectors[:,0:k]
row_norm=np.linalg.norm(u,axis=1)
t=(u.T/row_norm).T
#np.savetxt("eigenvectors.txt",t,fmt='%.8f')
#np.savetxt("eigenvalues.txt",eigenvalues[0:k],fmt='%.8f')


# 6. use KMeans to identify clusters 
starttime3=datetime.now()

kmeans=KMeans(k).fit(t)
clusters_index=kmeans.labels_

print("KMeans clustering is complete")
#print("it took %s to complete." %(datetime.now()-starttime3) )
print("here are some of the cluster assignments: ")
print(clusters_index)

# 7. generate files for representatives from each cluster
rep=metrics.pairwise_distances_argmin_min(kmeans.cluster_centers_,t)[0]   

reptraj=traj.slice(rep)
reptraj.save_pdb(protein+'cluster_25ns_reps.pdb')
reptraj.save_xtc(protein+'cluster_25ns_reps.xtc')
print("trajectory files for cluster representatives have been generated.")


# 8. generate files for each clusters
print("we will now generate trajectory files in .xtc and .pdb format for each cluster")
freq=[]
for x in range(0,k):
    frame_list=np.where(clusters_index==x)[0]
    freq.append(len(frame_list))
    newtrajCA=trajCA.slice(frame_list)
    newtraj=traj.slice(frame_list)
    newtraj.save_xtc(protein+' '+'cluster_25ns_'+str(x)+'.xtc')
    newtrajCA.save_pdb(protein+ ' '+'cluster_25ns_'+str(x)+'.pdb')
    print("trajectory files for cluster %d has been generated" %x)

print("%d clusters have all been generated" %k)
print("this is the probability/frequency of each cluster:")
pfreq=np.divide(freq,float(sum(freq)))
print(pfreq)
print("it took %s to do this whole process" %(datetime.now()-starttime))
np.savetxt('clusters_index',clusters_index)


