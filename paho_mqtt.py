import paho.mqtt.client as paho

class paho_mqtt:
	def __init__( self, client_id, user, password, host, port ):
		self.client = paho.Client( client_id )
		self.client.username_pw_set( user, password )
		self.client.connect( host, port )
		self.client.loop_start()
	def publish( self, topic, msg ):
		self.client.publish( topci, msg )
