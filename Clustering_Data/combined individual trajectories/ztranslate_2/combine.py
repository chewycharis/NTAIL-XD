# combine cluster numbers 

import mdtraj as md
import numpy as np


fl1=np.loadtxt('1st_attempt/frame_list_1st_attempt.txt')
fl2=np.loadtxt('2nd_attempt/frame_list_2nd_attempt.txt')
ci1=np.loadtxt('1st_attempt/clusters_index')
ci2=np.loadtxt('2nd_attempt/clusters_index')
ci3=np.loadtxt('3rd_attempt/clusters_index')

#1 combine c2 and c3 

corrected_ci2=np.copy(ci2)
counter=0
#map 0 to 1, 1 to 4, and 2 to 5 
adjusted_ci3=map(lambda x: 5 if x==1 else x, ci3)
adjusted_ci3=map(lambda x: 6 if x==2 else x, adjusted_ci3)

for x in fl2:
	corrected_ci2[int(x)]=adjusted_ci3[counter]
	counter=counter+1

#2 combine corrected_ci2 with ci1
corrected_ci1=np.copy(ci1)
counter=0
#map 0 to 6, and then self to self for everything else
adjusted_ci2=map(lambda x: 7 if x==1 else x, corrected_ci2)

for x in fl1:
	corrected_ci1[int(x)]=adjusted_ci2[counter]
	counter=counter+1

pfreq=[]
for x in range(0,8):
	pfreq.append(sum(corrected_ci1==x))


np.savetxt('ztranslate_2_combined_index.txt',corrected_ci1,fmt="%.f")
