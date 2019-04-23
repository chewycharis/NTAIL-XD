# combine cluster numbers 

import mdtraj as md
import numpy as np


fl1=np.loadtxt('1st attempt/frame_list_from_cluster_0.txt')
fl2=np.loadtxt('2nd attempt/frame_list_for_cluster_1')
ci1=np.loadtxt('1st attempt/clusters_index_flipped_switch_0_and_1')
#because ci1 is flipped...
ci1=abs(ci1-1)

ci2=np.loadtxt('2nd attempt/clusters_index')
ci3=np.loadtxt('3rd attempt/clusters_index')

#1 combine c2 and c3 

corrected_ci2=np.copy(ci2)
counter=0
#map 0 to 1, 1 to 4, and 2 to 5 
adjusted_ci3=map(lambda x: 4 if x==1 else x, ci3)
adjusted_ci3=map(lambda x: 5 if x==2 else x, adjusted_ci3)
adjusted_ci3=map(lambda x: 1 if x==0 else x, adjusted_ci3)

for x in fl2:
	corrected_ci2[int(x)]=adjusted_ci3[counter]
	counter=counter+1

#2 combine corrected_ci2 with ci1
corrected_ci1=np.copy(ci1)
counter=0
#map 0 to 6, and then self to self for everything else
adjusted_ci2=map(lambda x: 6 if x==1 else x, corrected_ci2)

for x in fl1:
	corrected_ci1[int(x)]=adjusted_ci2[counter]
	counter=counter+1

pfreq=[]
for x in range(0,7):
	pfreq.append(sum(corrected_ci1==x))


np.savetxt('ztranslate_5_combined_index.txt',corrected_ci1,fmt="%.f")
