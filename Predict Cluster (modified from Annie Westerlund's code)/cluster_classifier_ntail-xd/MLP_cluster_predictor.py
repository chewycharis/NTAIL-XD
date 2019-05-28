import numpy as np
from joblib import dump, load
import sklearn.neural_network as nn
from sklearn.preprocessing import MinMaxScaler

class MLPClusterPredictor():

	def __init__(self, samples, labels=None, hidden_layer_sizes=(100,),
				 solver='adam', max_train_iter=100000, activation='relu',
				 learning_rate='adaptive',scale=True):
		
		if scale: #scaling sample before training improves model stability 
			self.scaler = MinMaxScaler()
			self.samples = self.scaler.fit(samples).transform(samples)
		else:
			self.samples = samples

		self.labels = self.set_labels(labels)

		self.classifier = nn.MLPClassifier(
			solver=solver,
			hidden_layer_sizes=hidden_layer_sizes,
			random_state=None,
			activation=activation,
			learning_rate=learning_rate,
			max_iter=max_train_iter)

	def set_labels(self,labels):
		if labels is None:
			return None
		# create label matrix 
		labels -= labels.min() # label starts at 0
		labels = labels.astype(int)
		n_classes = len(np.unique(labels))
		new_labels = np.zeros((labels.shape[0],n_classes))
		for i_label,label in enumerate(labels):
			new_labels[i_label,label] = 1
		return new_labels

	def convert_to_input_labels(self,labels):
		new_labels = np.argmax(labels,axis=1)
		return new_labels

	def train(self): #returns MLP trained model
		self.classifier.fit(self.samples, self.labels)
		print('Training score: '+str(self.classifier.score(self.samples,self.labels)))

	def predict(self): #returns predicted label for new data based on trained model
		labels = self.classifier.predict(self.samples)
		if self.labels is not None:
			print('Predicting score: ' + str(self.classifier.score(self.samples, self.labels)))
		return self.convert_to_input_labels(labels)

	def save_classifier(self,filename_classifier,filename_scaler): # saves trained models 
		dump(self.classifier, filename_classifier)
		dump(self.scaler, filename_scaler)

	def set_classifier(self,filename_classifier,filename_scaler): 
		#loads trained model and scales sample based on trained scaler library
		self.classifier = load(filename_classifier)
		self.scaler = load(filename_scaler)
		self.samples = self.scaler.transform(self.samples)
