import cv2
import time
import imutils
import numpy as np

# import configuration
from config import Config
from paho_mqtt import *

# Check throttling of the MQTT output for an object
# detected object list with label->time accociation
detected_objects = {}
def throttle_output(object_label, obj_detection_time, throttle_time):
    if object_label in detected_objects:
        # check if time since last detection
        # if less than THROTTLE_TIME, return true, we are throttling
        # if greater than THROTTLE_TIME, return false, we are not throttling
        if obj_detection_time - detected_objects[object_label] < throttle_time:
            return True
        else:
            detected_objects[object_label] = obj_detection_time
            return False
    else:
        # set time in dictionary for this object
        # return false meaning we are not throttling for this object
        detected_objects[object_label] = obj_detection_time
        return False

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


# return list of detected objects from cv2 network
# return only objects with confidence levels above the min
def get_detected_object_list( nn_detections, min_confidence_level ):
	# detected object list to return
	dol = []
	for i in np.arange(0, nn_detections.shape[2]):
		if nn_detections[0, 0, i, 2] > min_confidence_level:
			dol.append(detected_object( nn_detections[0, 0, i, 2], int(nn_detections[0, 0, i, 1])))
	
	return dol

class stream_capture:
	def __init__(self, stream_url):
		self.url = stream_url
		self.stream = cv2.VideoCapture(self.url)
	
	def get_blob(self):
		while True:
			ret, frame = self.stream.read()
			if ret:
				frame = imutils.resize(frame, width=400)
				blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
				return blob
	def __del__(self):
		self.stream.release()

if __name__ == "__main__":
	
	mqtt = paho_mqtt( Config.MQTT_CLIENT_ID, Config.MQTT_USER, Config.MQTT_PASSWORD, Config.MQTT_HOST, Config.MQTT_PORT)
	#Loading Caffe Model
	nn = cv2.dnn.readNetFromCaffe(Config.FILE_PROTOTXT, Config.FILE_MODEL)

	#Initialize Video Stream
	vs = stream_capture(Config.STREAM_URL)
	
	# sleeping might reset connection on camera
	print("Waiting 60 seconds to start ...",flush=True)
	# time.sleep(60.0)
	print("Begining...",flush=True)

	#Loop Video Stream
	while True:
		# Read frame and resize to 400px
		
		nn.setInput( vs.get_blob() )
		detections = get_detected_object_list( nn.forward(), Config.MIN_CONFIDENCE )

		#Loop over the detections
		for detection in detections:

			#Filtering out weak predictions
			#if confidence > MIN_CONFIDENCE and idx == 15:
			if not throttle_output(detection.label, detection.timestamp, Config.THROTTLE_TIME):
				# Publish the MQTT msg
				mqtt.publish( Config.MQTT_TOPIC + "/" + detection.label, str(detection) )
				print(detection, flush=True)
		del detections
