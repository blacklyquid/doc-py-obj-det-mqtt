class object_detector:
	def __init__( self, min_confidence, prototxt, model ):
		self.min_confidence = min_confidence
		self.nn = cv2.dnn.readNetFromCaffe(prototxt, model)
	def get_detections( self, blob ):
		self.nn.setInput( blob )
		return self._get_detected_object_list()
	# return list of detected objects from cv2 network
	# return only objects with confidence levels above the min
	def _get_detected_object_list():
		nn_detections = self.nn.forward()
		# detected object list to return
		dol = []
		for i in np.arange(0, nn_detections.shape[2]):
			if nn_detections[0, 0, i, 2] > self.min_confidence:
				dol.append(detected_object( nn_detections[0, 0, i, 2], int(nn_detections[0, 0, i, 1])))

		return dol
