# main.py

# import configuration
from config import Config
from paho_mqtt import *
from object_detector import *
from stream_capture import *

if __name__ == "__main__":
	
	mqtt = paho_mqtt( Config.MQTT_CLIENT_ID, Config.MQTT_USER, Config.MQTT_PASSWORD, Config.MQTT_HOST, Config.MQTT_PORT, Config.THROTTLE_TIME)
	detector = object_detector(Config.MIN_CONFIDENCE, Config.FILE_PROTOTXT, Config.FILE_MODEL)
	vs = stream_capture(Config.STREAM_URL)
	
	# sleeping might reset connection on camera
	print("Waiting 60 seconds to start ...",flush=True)
	time.sleep(60.0)
	print("Begining...",flush=True)

	while True:
		detections = detector.get_detections( vs.get_blob() )
		for detection in detections:
			mqtt.publish( Config.MQTT_TOPIC + "/" + detection.label, str(detection) )
