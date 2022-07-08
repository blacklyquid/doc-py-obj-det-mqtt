# object_detector.py

import cv2, time
import numpy as np

class detected_object:
	labels = ["background", "aeroplane", "bicycle", "bird", 
	"boat","bottle", "bus", "car", "cat", "chair", "cow", 
	"diningtable","dog", "horse", "motorbike", "person", "pottedplant", 
	"sheep","sofa", "train", "tvmonitor"]
	def __init__(self, detected_confidence, label_index):
		self.confidence = detected_confidence
		self.label = self.labels[label_index]
		self.timestamp = time.time()
		self.label_index = label_index
		self.json_string = '{ "object":"' + self.label + '", "idx":"' + str(self.label_index) + '","confidence":"' + str(self.confidence) + '","time":"' + str(self.timestamp) + '"}'
	def __str__(self):
		return self.json_string

class object_detector:
	def __init__( self, min_confidence, prototxt, model ):
		self.min_confidence = min_confidence
		self.nn = cv2.dnn.readNetFromCaffe(prototxt, model)
	def get_detections( self, blob ):
		self.nn.setInput( blob )
		nn_detections = self.nn.forward()
		# detected object list to return
		dol = []
		for i in np.arange(0, nn_detections.shape[2]):
			if nn_detections[0, 0, i, 2] > self.min_confidence:
				dol.append(detected_object( nn_detections[0, 0, i, 2], int(nn_detections[0, 0, i, 1])))

		return dol
