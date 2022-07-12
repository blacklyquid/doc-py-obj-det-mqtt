# docker-python-object-detection -> MQTT

Dockerfile and python scripts to build a docker image that utilizes ssd to detect objects in a video stream.<br/>
It will then send an MQTT message for each object detected. The MQTT topic is built using the objects label and a base topic.<br/>
The MQTT messages can be throttle to 1 message every X seconds for each object detected.

```
git clone https://github.com/blacklyquid/docker-python-object-detection.git
cd docker-python-object-detection
docker build -t blacklyquid/docker-python-object-detection .
```
```
docker run -d
  -e MQTT_HOST='192.168.1.55' \                    # required - just an ip address
  -e MQTT_PORT=1883 \                              # optional
  -e MQTT_CLIENT_ID='obj-detection-python' \       # optional
  -e MQTT_USER='' \                                # optional
  -e MQTT_PASSWORD='' \                            # optional
  -e MQTT_TOPIC='home/object-detected' \           # optional - home/object-detected/person .... and so on
  -e STREAM_URL='http://your-stream/url' \         # required - stream url, works with rtsp://, http://
  -e MIN_CONFIDENCE=.40 \                          # optional - Ignore detections with less than 40% confidence - DECIMAL
  -e THROTTLE_TIME=30 \                            # optional - send MQTT message only once every 30 seconds    - INTEGER
  blacklyquid/docker-python-object-detection
```
