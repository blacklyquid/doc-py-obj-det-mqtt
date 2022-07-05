# config.py

import os

class config:
  # MQTT connection
  MQTT_HOST = os.environ.get('MQTT_HOST', None)     # 192.168.1.225'
  MQTT_PORT = int(os.environ.get('MQTT_PORT', 1883))           # 1883
  MQTT_CLIENT_ID = os.environ.get('MQTT_CLIENT_ID', 'obj-detection-python' )
  MQTT_USER = os.environ.get('MQTT_USER', '')
  MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD','')

  # the base mqtt topic
  MQTT_TOPIC = os.environ.get('MQTT_TOPIC','home/object-detected/')

  # The stream we are detecting objects in
  STREAM_URL = os.environ.get('STREAM_URL',None)

  # simple throttle
  # for each object detected only send MQTT message once every 30 seconds
  THROTTLE_TIME = int(os.environ.get('THROTTLE_TIME', 30))

  # Ignore detections with a confidence level lower than this, must be between 0-1
  MIN_CONFIDENCE = float(os.environ.get('MIN_CONFIDENCE', .40))

  FILE_PROTOTXT = "SSD_MobileNet_prototxt.txt"
  FILE_MODEL = "SSD_MobileNet.caffemodel"
Config = config();
