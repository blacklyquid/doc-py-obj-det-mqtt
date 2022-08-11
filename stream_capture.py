# stream_capture.py
# blacklyquid@outlook.com
# 2022
import cv2, imutils, time

class stream_capture:
	
	def __init__(self, stream_url):
		self.url = stream_url
		self.error_counter = 0
		self.auto_reset = True
		self.reset_timeout = 0
		self.capture()
	
	def get_blob(self):
		if self.read():
			frame = imutils.resize(self.frame, width=400)
			blob = cv2.dnn.blobFromImage(cv2.resize(self.frame, (300, 300)), 0.007843, (300, 300), 127.5)
			return blob
		else:
			return False
	
	def read(self):
		try:
			ret, frame = self.stream.read()
			self.frame = frame.copy()
		except:
			print("Reseting...",flush=True)
			if self.auto_reset == True:
				self.error_counter += 1
				self.reset()
	
	def reset(self):
		self.release()
		self.capture()
		
	def capture(self):
		print("Waiting " + str(self.reset_timeout) + " Seconds...",flush=True)
		time.sleep(self.reset_timeout)
		print("Capturing Stream...",flush=True)
		self.stream = cv2.VideoCapture(self.url)
	
	def release(self):
		if self.stream:
			self.stream.release()
	
	def __del__(self):
		self.release()
