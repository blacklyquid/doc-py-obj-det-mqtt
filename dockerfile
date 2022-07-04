FROM python:3

WORKDIR /usr/src/app

RUN apt-get update && apt-get install libgl1 -y

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY object_detection.py ./
COPY SSD_MobileNet.caffemodel ./
COPY SSD_MobileNet_prototxt.txt ./

CMD [ "python", "./object_detection.py" ]
