FROM python:3

WORKDIR /usr/src/app

RUN apt-get update && apt-get install libgl1 -y

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py ./
COPY config.py ./
COPY paho_mqtt.py ./
COPY object_detector.py ./
COPY stream_capture.py ./
COPY SSD_MobileNet.caffemodel ./
COPY SSD_MobileNet_prototxt.txt ./

CMD [ "python", "./main.py" ]
