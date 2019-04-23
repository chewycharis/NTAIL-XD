import numpy as np
import matplotlib.pyplot as plt
import os 

os.chdir('/homes/cfu/Desktop/cluster_analysis')
protein_list=["cabs_7", "cabs_8" ,"parallel_3" ,"yrotate_6", "ztranslate_2", "ztranslate_5", "sonia_1", "xrotate_3" ]
k=[40 ,15, 10, 10, 8, 7, 16, 3] 
colors=['r','b','g','saddlebrown','orange','violet','hotpink','grey','indianred','teal','black','goldenrod','darkslateblue','cyan'] #wow  I must have been bored


for p in range(0, 8): #for each protein 
	protein=protein_list[p]
	
	#### protein-sasa-vs-angleCD ####
	os.chdir('/homes/cfu/Desktop/cluster_analysis/'+protein+'/2dplots')
	os.chdir('protein-sasa-vs-angleCD')
	# to not kill your eyes, only plot 5 largest clusters 
	size=[]	
	for f in range(0, k[p]):
		size.append(os.path.getsize(protein+'_cluster_'+str(f)+'_protein-sasa-vs-angleCD.dat')) #size of files in a list 
	if len(size) <5:
		index=np.array(range(0, len(size)) )#you might not have more than 5 clusters 
	else:39
		index=np.argpartition(np.array(size),-5)[-5:]  # index of 5 largest cluster, (larger cluster = larger file)
	#append data 
	list1=[]
	for i in index: 
		list1.append(np.loadtxt(protein+'_cluster_'+str(i)+'_protein-sasa-vs-angleCD.dat'))
	#plot figure 
	fig = plt.figure()
	ax1 = fig.add_subplot(111)
	for  x in range(len(list1)):
        	ax1.scatter(list1[x][:,0], list1[x][:,1], s=10, c=colors[x],edgecolors='none', marker="o", label='cluster '+str(index[x]))
	plt.xlabel('Solvent Assessible Surface Area (nm^2)')
	plt.ylabel('Interhelical Angle between NTail and Alpha 3 (degree)')
	plt.legend(loc='upper left');
	plt.savefig(protein+'__protein-sasa-vs-angleCD_top-5-cluster.png')
	plt.close()

	
	#### ntail-xd-distance-vs-angleCD ####
	os.chdir('/homes/cfu/Desktop/cluster_analysis/'+protein+'/2dplots')
	os.chdir('ntail-xd-distance-vs-angleCD')
	# to not kill your eyes, only plot 5 largest clusters 
	size=[]	
	for f in range(0, k[p]):
		size.append(os.path.getsize(protein+'_cluster_'+str(f)+'_ntail-xd-distance-vs-angleCD.dat')) #size of files in a list 
	if len(size) <5:
		index=np.array(range(0, len(size)) )#you might not have more than 5 clusters 3939
	else:
		index=np.argpartition(np.array(size),-5)[-5:]  # index of 5 largest cluster, (larger cluster = larger file)
	#append data 
	list1=[]
	for i in index: 
		list1.append(np.loadtxt(protein+'_cluster_'+str(i)+'_ntail-xd-distance-vs-angleCD.dat'))
	#plot figure 
	fig = plt.figure()
	ax1 = fig.add_subplot(111)
	for  x in range(len(list1)):
        	ax1.scatter(list1[x][:,0], list1[x][:,1], s=10, c=colors[x],edgecolors='none', marker="o", label='cluster '+str(index[x]))
	plt.xlabel('NTAIL-XD Distance (nm)')
	plt.ylabel('Interhelical Angle between NTail and Alpha 3 (degree)')
	plt.legend(loc='upper left');
	plt.savefig(protein+'__ntail-xd-distance-vs-angleCD_top-5-cluster.png')
	plt.close()

	#### ntail-helicity vs angleCD ####
	os.chdir('/homes/cfu/Desktop/cluster_analysis/'+protein+'/2dplots')
	os.chdir('ntail-helicity-vs-angleCD')
	# to not kill your eyes, only plot 5 largest clusters 
	size=[]	
	for f in range(0, k[p]):
		size.append(os.path.getsize(protein+'_cluster_'+str(f)+'_ntail-helicity-vs-angleCD.dat')) #size of files in a list 
	if len(size) <5:
		index=np.array(range(0, len(size)) )#you might not have more than 5 clusters 
	else:
		index=np.argpartition(np.array(size),-5)[-5:]  # index of 5 largest cluster, (larger cluster = larger file)
	#append data 
	list1=[]
	for i in index: 
		list1.append(np.loadtxt(protein+'_cluster_'+str(i)+'_ntail-helicity-vs-angleCD.dat'))
	#plot figure 
	fig = plt.figure()
	ax1 = fig.add_subplot(111)
	for  x in range(len(list1)):
        	ax1.scatter(list1[x][:,0], list1[x][:,1], s=10, c=colors[x],edgecolors='none', marker="o", label='cluster '+str(index[x]))
	plt.xlabel('% helicity in NTAIL')
	plt.ylabel('Interhelical Angle between NTail and Alpha 3 (degree)')
	plt.legend(loc='upper left');
	plt.savefig(protein+'_ntail-helicity-vs-angleCD_top-5-cluster.png')
	plt.close()

os.chdir('/homes/cfu/Desktop')




