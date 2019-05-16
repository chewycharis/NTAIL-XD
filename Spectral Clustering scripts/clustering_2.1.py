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
"""
if len(argv)==1: 
   print __doc__
   exit()

xtc=argv[1]
topology=argv[2]
adjacency_matrix=argv[3]
protein=argv[4]


xtc='FPD_Sonia_1_protein_50ns.xtc' #always input xtc. NOT pdb, which takes forever.
topology='FPD_Sonia_1_remd_protein.gro'
adjacency_matrix='FPD_Sonia_1_adjacency_matrix.txt'
protein="FPD_Sonia_1"

# 0. load frame-to-frame distance matrix
traj=md.load(xtc,top=topology)
index=traj.topology.select('name CA')
trajCA=traj.atom_slice(index) #trajCA to save output

adjacency=np.loadtxt(adjacency_matrix)
print("frame to frame distance matrix and trajectory have been loaded")
print("it took %s to complete." %(datetime.now()-starttime) )

"""

# 1. calculate gamma 
dumb=np.diag(np.sum(adjacency,axis=1)) #to make self-to-self distance non-zero
gamma=np.mean(np.amin(adjacency+dumb,axis=1))
print("gamma is %.8f" %gamma)


# 2. compute normalized laplacian matrix
affinity=np.exp(-(adjacency**2)/(2*gamma**2))
row_sums=(np.sum(affinity,axis=1))**(-0.5)
diagonal2=np.diag(row_sums)
lsym=diagonal2 .dot(affinity) .dot(diagonal2)


# 3. compute eigensystem for normalized laplacian matrix
starttime2=datetime.now()

eigensys=np.linalg.eig(lsym)
eigenvalues=eigensys[0]
index=eigenvalues.argsort()[::-1] #sort eigenvalues in descending order 
eigenvalues=eigenvalues[index]
eigenvectors=(eigensys[1].real)[:,index]
#np.savetxt(protein+"_eigenvectors_unnormalized_25ns.txt",eigenvectors,fmt='%.8f')
#np.savetxt(protein+"_eigenvalues_unnormalized_25ns.txt",eigenvalues,fmt='%.8f')
print("eigensystem has been computed for laplacian matrix")
print("it took %s to complete." %(datetime.now()-starttime2) )

#print(protein+"'s clusters are being calculated!")
#eigenvectors=np.loadtxt(protein+"_eigenvectors_unnormalized_25ns.txt")
#eigenvalues=np.loadtxt(protein+"_eigenvalues_unnormalized_25ns.txt")


# 4. identify largest eigengap to define k  

diff=abs(np.diff(eigenvalues[0:100])) # max number of cluster =100  
maxdiff_ind=np.argmax(diff[1:])
print("the largest eigengap is between %d th and %d th eigenvalues" %(maxdiff_ind+1 ,maxdiff_ind + 2))
print("this is the value of the eigengap: %.4f" %diff[maxdiff_ind])

k_eigen=maxdiff_ind+2
print("this is k_eigengap")
print(k_eigen)

qscore_start_time=datetime.now()
q_score_list=[]
print("estimating q score for k between 2 and 50...")
for k in range(2,min(51,len(traj))):
    print("computing k=%d clusters..." %k)

    # 5. choose first k eigenvectors and normalize them by row  
    u=eigenvectors[:,0:k]
    row_norm=np.linalg.norm(u,axis=1)
    t=(u.T/row_norm).T

    # 6. use KMeans to identify clusters 
    kmeans=KMeans(k).fit(t)
    clusters_index=kmeans.labels_

    # 7. generate files for representatives from each cluster
    rep=metrics.pairwise_distances_argmin_min(kmeans.cluster_centers_,t)[0]    

    #8. Q score
    def d(x,y):
	cos_value=(x .dot(y) /(np.linalg.norm(x) * np.linalg.norm(y)))
	if cos_value > 1 or cos_value < -1:
		cos_value=round(cos_value,5)        
	return math.acos(cos_value)
    def ratio(x,c1,c2):
	if d(x,c1)!=0:
        	return d(x,c2)/d(x,c1)
    lr=[]
    for i in range(0, len(t)):
        # best and second best are indices
        best=clusters_index[i] # the representative structure in its cluster
        s=np.delete(t[rep],best,0)
        second_best=metrics.pairwise_distances_argmin_min(np.array([t[i]]),s)[0]
        r=ratio(t[i],t[rep][best],s[second_best[0]])         
	if r!= None:	
		lr.append(r)
    q_score=np.median(lr)
    q_score_list.append(q_score)
print('this is K_qscore')
print(np.where(q_score_list==max(q_score_list))[0][0]+2)
print("it took %s to compute q score" %(datetime.now()-qscore_start_time))


k=np.where(q_score_list==max(q_score_list))[0][0]+2


print("based on this result, we will try to find %d clusters" %k)


