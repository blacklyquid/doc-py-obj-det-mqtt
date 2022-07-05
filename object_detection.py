import cv2
import time
import imutils
import numpy as np
import paho.mqtt.client as paho
# import configuration
from config import Config

#from imutils.video import FPS
#from imutils.video import VideoStream

client = paho.Client(Config.MQTT_CLIENT_ID)
client.username_pw_set(Config.MQTT_USER, Config.MQTT_PASSWORD)
client.connect(Config.MQTT_HOST, Config.MQTT_PORT)
# call loop_start for auto reconnections
client.loop_start()

detected_objects = {}

if not Config.MQTT_HOST:
	sys.exit('Please set the MQTT_HOST enviroment variable')
if not Config.STREAM_URL:
	sys.exit('Please set the STREAM_URL enviroment variable')
if Config.MIN_CONFIDENCE > 1 or Config.MIN_CONFIDENCE < 0:
	sys.exit('Enviroment variable MIN_CONFIDENCE must be between 0 and 1')

	

# Check throttling of the MQTT output for an object
# obj - String - the detected object label
# obj_detection_time - time in seconds when the object was detected
def throttle_output(object_label, obj_detection_time):
    if object_label in detected_objects:
        # check if time since last detection
        # if less than THROTTLE_TIME, return true, we are throttling
        # if greater than THROTTLE_TIME, return false, we are not throttling
        if obj_detection_time - detected_objects[object_label] < Config.THROTTLE_TIME:
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
		self.detection_time = time.time()
		
def detected_object_list( nn_detections ):
	dol = []
	for i in np.arange(0, nn_detections.shape[2]):
		dol.append(detected_object( detections[0, 0, i, 2], int(detections[0, 0, i, 1]))
	
	return dol
	
if __name__ == "__main__":

	#Initialize Objects and corresponding colors which the model can detect
	labels = ["background", "aeroplane", "bicycle", "bird", 
	"boat","bottle", "bus", "car", "cat", "chair", "cow", 
	"diningtable","dog", "horse", "motorbike", "person", "pottedplant", 
	"sheep","sofa", "train", "tvmonitor"]

	#Loading Caffe Model
	nn = cv2.dnn.readNetFromCaffe(Config.FILE_PROTOTXT, Config.FILE_MODEL)

	#Initialize Video Stream
	vs = cv2.VideoCapture(Config.STREAM_URL)
	
	# sleeping might reset connection on camera
	print("Waiting 60 seconds to start ...",flush=True)
	time.sleep(60.0)
	print("Begining...",flush=True)
	
	
	
	
	#Loop Video Stream
	while True:
		# Read frame and resize to 400px
		ret, frame = vs.read()
		if ret:
			frame = imutils.resize(frame, width=400)
			#(h, w) = frame.shape[:2]

			#Converting Frame to Blob
			blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

			#Passing Blob through network to detect and predict
			nn.setInput(blob)
			detections = nn.forward()


			#Loop over the detections
			for i in np.arange(0, detections.shape[2]):

				#Extracting the confidence of predictions
				confidence = detections[0, 0, i, 2]

				#object label id
				idx = int(detections[0, 0, i, 1])

				# the object label
				label = labels[idx]

				#Filtering out weak predictions
				#if confidence > MIN_CONFIDENCE and idx == 15:
				if confidence > Config.MIN_CONFIDENCE and not throttle_output(label, time.time()):

						# build json string
						json_string = '{ "object":"' + label + '", "idx":"' + str(idx) + '","confidence":"' + str(confidence) + '","time":"' + str(detected_objects[label]) + '"}'

						# Build the MQTT topic
						topic = Config.MQTT_TOPIC + '/' + label

						# Publish the MQTT msg
						client.publish( topic, json_string )

						print(json_string, flush=True)



	   

	vs.stop()
	vs.release()
