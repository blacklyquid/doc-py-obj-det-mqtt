import cv2
import time
import imutils
import numpy as np

# import configuration
from config import Config
from paho_mqtt import *
from throttle import *
from object_detector import *
from stream_capture import *

if __name__ == "__main__":
	
	mqtt = paho_mqtt( Config.MQTT_CLIENT_ID, Config.MQTT_USER, Config.MQTT_PASSWORD, Config.MQTT_HOST, Config.MQTT_PORT)
	detector = object_detector(config.MIN_CONFIDENCE, Config.FILE_PROTOTXT, Config.FILE_MODEL)
	vs = stream_capture(Config.STREAM_URL)
	
	# sleeping might reset connection on camera
	print("Waiting 60 seconds to start ...",flush=True)
	# time.sleep(60.0)
	print("Begining...",flush=True)

	#Loop Video Stream
	while True:
		# Read frame and resize to 400px
		detections = detector.get_detections( vs.get_blob() )

		#Loop over the detections
		for detection in detections:

			#Filtering out weak predictions
			#if confidence > MIN_CONFIDENCE and idx == 15:
			if not throttle_output(detection.label, detection.timestamp, Config.THROTTLE_TIME):
				# Publish the MQTT msg
				mqtt.publish( Config.MQTT_TOPIC + "/" + detection.label, str(detection) )
				print(detection, flush=True)
		del detections
