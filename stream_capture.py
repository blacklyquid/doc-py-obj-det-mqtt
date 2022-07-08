# stream_capture.py

import cv2, imutils

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
