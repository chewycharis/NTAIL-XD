#!/bin/bash 
protein=(cabs_7 cabs_8 parallel_3 yrotate_6 ztranslate_2 ztranslate_5   sonia_1 xrotate_3) 
k=(39 14 9 9 7 6 15 2) #number of cluster -1 
var=(helicity ntail-xd-distance angleBC angleCD sasa ntail-helicity)  #this is not used currently 
declare -a protein
declare -a k
declare -a var


for i in $(seq 0 7); # for each protein 
	do
	p=${protein[$i]}
	cd ~/Desktop/cluster_analysis/$p
	mkdir 2dplots
	mkdir ntail-helicity-vs-angleCD
	mkdir ntail-xd-distance-vs-angleCD
	mkdir protein-sasa-vs-angleCD
	
	
	for x in $(seq 0 ${k[$i]}); #for each cluster 
		do 
		#ntail helicity vs angleCD
		paste <(awk '{print $1}' ntail-helicity/$p"_cluster_25ns_"$x"_ntail_helicity.txt" ) <(awk '{print $2}' angleCD/$p"_cluster_25ns_"$x"-helix_angle-CD.dat" ) > $p"_cluster_"$x"_ntail-helicity-vs-angleCD.dat"
		#ntail-xd-distance vs angleCD 
		paste <(awk '/^[^#^@]/{print $2}' ntail-xd-distance/$p"_"$x"_ntail-xd.xvg" ) <(awk '{print $2}' angleCD/$p"_cluster_25ns_"$x"-helix_angle-CD.dat" ) > $p"_cluster_"$x"_ntail-xd-distance-vs-angleCD.dat"
		#protein sasa vs angleCD
		paste <(awk '/^[^#^@]/{print $3}' sasa/$p"_"$x"_ntailsides_sasa.xvg" ) <(awk '{print $2}' angleCD/$p"_cluster_25ns_"$x"-helix_angle-CD.dat" ) > $p"_cluster_"$x"_protein-sasa-vs-angleCD.dat"
		echo "finished organizing data for making 2d plots for  $p cluster $x..."
		

	done 
	mv $p"_cluster_"*"_ntail-helicity-vs-angleCD.dat" ntail-helicity-vs-angleCD
	mv $p"_cluster_"*"_ntail-xd-distance-vs-angleCD.dat" ntail-xd-distance-vs-angleCD
	mv $p"_cluster_"*"_protein-sasa-vs-angleCD.dat" protein-sasa-vs-angleCD
	mv ntail-helicity-vs-angleCD 2dplots
	mv ntail-xd-distance-vs-angleCD 2dplots
	mv protein-sasa-vs-angleCD 2dplots
done
		


