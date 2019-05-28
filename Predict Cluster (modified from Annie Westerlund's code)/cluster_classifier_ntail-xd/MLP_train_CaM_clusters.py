import os
import sys
import argparse
import numpy as np
import MLP_cluster_predictor as mcp

def main(parser):
	args = parser.parse_args()
	distance_maps = np.load(args.distance_maps)

	#load cluster_indices 		
	if args.cluster_indices is None: 
		cluster_indices=None
	else:	
		cluster_indices = np.load(args.cluster_indices)
		
	
	#predicts labels
	if args.predict_from_precomputed:
		print('Predicting labels based on pre-trained classifier.')
		
		# Create classifier object
		classifier = mcp.MLPClusterPredictor(distance_maps, cluster_indices,scale=False)

		# loads trained model and scales sample based on trained model 
		classifier.set_classifier(args.classifier_file_name, args.scaler_file_name)
		
		# Predict samples
		cluster_indices_predicted = classifier.predict()
		
		# Write to file
		np.save(args.cluster_indices_out,cluster_indices_predicted)
	
	#trains model
	else:
		print('Training classifier.')
		# Create classifier object
		classifier = mcp.MLPClusterPredictor(distance_maps, cluster_indices)

		# Train classifier
		classifier.train()
		
		# Save classifier
		classifier.save_classifier(args.classifier_file_name,args.scaler_file_name)


parser = argparse.ArgumentParser(epilog='Predicting clusters using MLP neural network. Annie Westerlund 2019.')
parser.add_argument('-f','--distance_maps',help='Inverse-distance contact maps used for obtaining original CaM clusters.')
parser.add_argument('-cl','--cluster_indices',help='Cluster indices obtained from spectral clustering.',default=None)
parser.add_argument('-cl_o','--cluster_indices_out',help='File where predicted cluster indices (from classifier) are written.',default='')
parser.add_argument('-o','--classifier_file_name',help='File to/from which classifier parameters are written/loaded.')
parser.add_argument('-s','--scaler_file_name',help='File to/from which min-max feature scaler is written/loaded.')
parser.add_argument('-predict','--predict_from_precomputed',help='Flag for predicting samples. If True, the classifier parameters are loaded and samples are classified. If False, the classifier is trained using the distance maps and cluster indices, and its parameters are written to file.',action='store_true')


main(parser)
