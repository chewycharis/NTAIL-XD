import matplotlib.pyplot as plt
import numpy as np
import os

labels=['ztranslate_5', 'parallel_3','ztranslate_2','cabs_8','cabs_7','xrotate_3','sonia_1','yrotate_6']
dic={}
counter=0
for x in os.listdir("./"):
    if x.endswith('.txt'):
        dic[labels[counter]]=np.loadtxt(x)
        counter+=1

plt.rcParams.update({'font.size':22})
for x in dic:
    plt.clf()
    plt.bar(range(0,len(dic[x])),dic[x])
    plt.xlabel('cluster #')
    plt.ylabel('% Frequency in Current Trajectory')
    plt.savefig(str(x)+"_pfreq.png",bbox_inches='tight')

#plt.annotate('A',xy=(2,14.4),xytext=(5,14.2),arrowprops=dict(facecolor='red',shrink=0.05))
#plt.annotate('B',xy=(3,5.6),xytext=(7,5.4),arrowprops=dict(facecolor='red',shrink=0.05))
#plt.annotate('C',xy=(4,3.5),xytext=(7,3.3),arrowprops=dict(facecolor='red',shrink=0.05))
#plt.annotate('D',xy=(5,3),xytext=(8,2.8),arrowprops=dict(facecolor='red',shrink=0.05))


