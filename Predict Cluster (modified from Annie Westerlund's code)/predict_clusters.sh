pypath=cluster_classifier_ntail-xd/
out_dir=./
newprotein=xrotate_3_newtraj
protein=xrotate_3
distance_maps=${out_dir}inverse_CA_${newprotein}.npy
#cluster_indices=example/cluster_indices_$protein.npy

train=0
predict=1

if [ ${train} -eq 1 ]
then
	# Create classifier
	python ${pypath}MLP_train_CaM_clusters.py -f ${distance_maps} -cl ${cluster_indices} -o classifier_$protein.joblib -s scaler_$protein.joblib
fi

if [ ${predict} -eq 1 ]
then
	# Use precreated classifier to predict cluster indices
	python ${pypath}MLP_train_CaM_clusters.py -f ${distance_maps} -cl_o ${out_dir}cluster_indices_${newprotein}_predicted.npy -o classifier_$protein.joblib -s scaler_$protein.joblib -predict
fi


