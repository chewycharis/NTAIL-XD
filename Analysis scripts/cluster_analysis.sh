# !/bin/bash
k=9            #number of clusters -1
pdbID=yrotate_6
cd $HOME/Desktop/
cd $pdbID
# 10-ntail, 11-xd, 12-xd alpha2-alpha3, 13-ntail side 1, 14-ntail side 2
(echo r 53-73; echo r 1-50; echo r 14-50; echo r 56 59 60 63 66 67 70; echo r 54 57 58 61 62 64 65 68 72; echo q;)| gmx make_ndx -f $pdbID'_protein.gro' -o $pdbID.ndx

for x in $(seq 0 $k);
	do 
	#rmsd of complex
	(echo 1; echo 1;) | gmx rms -f $pdbID' cluster_25ns_'$x.xtc   -s $pdbID'_protein.gro' -n $pdbID.ndx -o $pdbID"_"$x"_rms.xvg"
	#sasa ntail side 1 vs 2
	echo 1| gmx sasa -s $pdbID'_protein.gro'  -f $pdbID' cluster_25ns_'$x.xtc  -n $pdbID.ndx  -o $pdbID'_'$x'_ntailsides_sasa'.xvg -output '1' '13' '14'
	#interhelical angles alpha2-alpha3 and alpha3-ntail
	python $HOME/Desktop/calc_helix_vector.py $pdbID'_protein.gro' $pdbID' cluster_25ns_'$x.xtc $pdbID'_cluster_25ns_'$x #vectors 
	python $HOME/Desktop/calc_helix_angle.py $pdbID'_cluster_25ns_'$x #angle
	rm *vectors*; rm *angle-A*; rm *angle-BD*
        # ntail-xd distance 
	gmx distance  -f $pdbID' cluster_25ns_'$x.xtc -s $pdbID'_protein.gro' -n $pdbID.ndx -select 10 12 -selrpos res_com  -oall $pdbID'_'$x'_ntail-xd'.xvg
	#alpha helicity 
	python $HOME/Desktop/dssp.py $pdbID'_protein.gro' $pdbID' cluster_25ns_'$x.xtc $pdbID'_cluster_25ns_'$x 

done

#organizing files... 
mkdir rms; mkdir sasa; mkdir angleBC; mkdir angleCD; mkdir ntail-xd-distance; mkdir helicity
mv *ntail-xd.xvg ntail-xd-distance 
mv *rms*.xvg rms
mv *sasa*.xvg sasa
mv *angle-CD.dat angleCD
mv *angle-BC.dat angleBC
mv *helicity*.txt helicity 



