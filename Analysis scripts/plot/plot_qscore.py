import matplotlib.pyplot as plt
import numpy as np
import os

labels=['cabs_8']#, 'cabs_7','parallel_3','sonia_1','xrotate_3', 'yrotate_6','ztranslate_2','ztranslate_5']
dic={}
counter=0; 

for counter in range(0,len(labels)):
    l=[]
    for x in os.listdir("/home/chuhui/Desktop/qscore/"+labels[counter]+"/"):
        if x.endswith('.txt'):
            print(x)
            l.append(np.loadtxt("/home/chuhui/Desktop/qscore/"+labels[counter]+"/"+x))
            dic[labels[counter]]=l
    counter+=1


plt.rcParams.update({'font.size':12})

for x in dic:
    plt.clf()
    fig,ax=plt.subplots(1,len(dic[x]),squeeze=False,figsize=(len(dic[x])*6,6))
    for i in range(len(dic[x])):
        x1=range(2,len(dic[x][i])+2);
        y1=dic[x][i]
    	ax[0,i].scatter(x1,y1)
    	ax[0,i].set_title('Clustering Attempt #'+str(i+1))
        ax[0,i].set(xlabel='k',ylabel='Q score')
  
    fig.savefig(str(x)+"_qscore.png",bbox_inches='tight')
    plt.close()





