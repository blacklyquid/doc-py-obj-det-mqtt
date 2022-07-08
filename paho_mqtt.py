# paho_mqtt.py

import time
import paho.mqtt.client as paho

class paho_mqtt:
	def __init__( self, client_id, user, password, host, port, throttle_time = 0 ):
		self.client = paho.Client( client_id )
		self.client.username_pw_set( user, password )
		self.client.connect( host, port )
		self.client.loop_start()
		self.throttle_list = {}
		self.throttle_time = throttle_time
		
	def publish( self, topic, msg ):
		if not self.throttle_output( topic, time.time() ):
			self.client.publish( topic, msg )

	def throttle_output( self, topic, timestamp ):
		if topic in self.throttle_list:
			# check if time since last detection
			# if less than THROTTLE_TIME, return true, we are throttling
			# if greater than THROTTLE_TIME, return false, we are not throttling
			if timestamp - self.throttle_list[topic] < self.throttle_time:
				return True
			else:
				self.throttle_list[topic] = timestamp
				return False
		else:
			# set time in dictionary for this object
			# return false meaning we are not throttling for this object
			self.throttle_list[topic] = timestamp
			return False
