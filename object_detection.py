import cv2
import time
import imutils
import os
import numpy as np
import paho.mqtt.client as paho

#from imutils.video import FPS
#from imutils.video import VideoStream

# MQTT connection
MQTT_HOST = os.environ.get('MQTT_HOST', None)     # 192.168.1.225'
MQTT_PORT = os.environ.get('MQTT_PORT', 1883)           # 1883
MQTT_CLIENT_ID = os.environ.get('MQTT_CLIENT_ID', 'obj-detection-python' )
MQTT_USER = os.environ.get('MQTT_USER', '')
MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD','')

# the base mqtt topic
MQTT_TOPIC = os.environ.get('MQTT_TOPIC','home/object-detected/')

# The stream we are detecting objects in
STREAM_URL = os.environ.get('STREAM_URL',None)

# simple throttle
# for each object detected only send MQTT message once every 30 seconds
THROTTLE_TIME = os.environ.get('THROTTLE_TIME', 30)

# Ignore detections with a confidence level lower than this, must be between 0-1
MIN_CONFIDENCE = float(os.environ.get('MIN_CONFIDENCE', .40))

FILE_PROTOTXT = "SSD_MobileNet_prototxt.txt"
FILE_MODEL = "SSD_MobileNet.caffemodel"

client = paho.Client(MQTT_CLIENT_ID)
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.connect(MQTT_HOST, MQTT_PORT)
# call loop_start for auto reconnections
client.loop_start()

detected_objects = {}

if not MQTT_HOST:
	sys.exit('Please set the MQTT_HOST enviroment variable')
if not STREAM_URL:
	sys.exit('Please set the STREAM_URL enviroment variable')
if MIN_CONFIDENCE > 1 or MIN_CONFIDENCE < 0:
	sys.exit('Enviroment variable MIN_CONFIDENCE must be between 0 and 1')
	
# Check throttling of the MQTT output for an object
# obj - String - the detected object label
# obj_detection_time - time in seconds when the object was detected
def throttle_output(object_label, obj_detection_time):
    if object_label in detected_objects:
        # check if time since last detection
        # if less than THROTTLE_TIME, return true, we are throttling
        # if greater than THROTTLE_TIME, return false, we are not throttling
        if time.time() - detected_objects[object_label] < THROTTLE_TIME:
            return True
        else:
            detected_objects[object_label] = time.time()
            return False
    else:
        # set time in dictionary for this object
        # return false meaning we are not throttling for this object
        detected_objects[object_label] = time.time()
        return False

if __name__ == "__main__":

	#Initialize Objects and corresponding colors which the model can detect
	labels = ["background", "aeroplane", "bicycle", "bird", 
	"boat","bottle", "bus", "car", "cat", "chair", "cow", 
	"diningtable","dog", "horse", "motorbike", "person", "pottedplant", 
	"sheep","sofa", "train", "tvmonitor"]

	#Loading Caffe Model
	nn = cv2.dnn.readNetFromCaffe(FILE_PROTOTXT, FILE_MODEL)

	#Initialize Video Stream
	vs = cv2.VideoCapture(STREAM_URL)
	
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
				if confidence > MIN_CONFIDENCE and not throttle_output(label, time.time()):

						# build json string
						json_string = '{ "object":"' + label + '", "idx":"' + str(idx) + '","confidence":"' + str(confidence) + '","time":"' + str(detected_objects[label]) + '"}'

						# Build the MQTT topic
						topic = MQTT_TOPIC + '/' + label

						# Publish the MQTT msg
						client.publish( topic, json_string )

						print(json_string, flush=True)



	   

	vs.stop()
	vs.release()
