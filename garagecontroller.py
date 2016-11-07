#!/usr/bin/env python2.7
# Purpose: Process MQTT trigger message from Home Assistant RPi to open garage door.
# Soruce: https://hackaday.io/project/9901/instructions

import sys
import mosquitto
import RPi.GPIO as GPIO
import time
#import picamera

firstRun = 1
doorSensorPIN = 18
relayPIN = 17
relayCmdTopic = 'garage/relay'
cameraTopic = 'garage/camera'
doorStatusTopic = 'garage/status'

GPIO.setmode(GPIO.BCM)
GPIO.setup(relayPIN, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(doorSensorPIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # activate input with PullUp

def getDoorStatus():
	if GPIO.input(doorSensorPIN):
		return 'closed'
	else:
		return 'open'

def publishDoorStatus():
	time.sleep(0.5)
	doorStatus = getDoorStatus()
	print("door status is now... " + doorStatus)
	mqttc.publish(doorStatusTopic, doorStatus, 0, False)

		
def on_connect(mosq, obj, rc):
    print("rc: "+str(rc))

def on_message(mosq, obj, msg):
	print ("TOPIC: " + msg.topic + " - PAYLOAD: " + str(msg.payload))
	global firstRun

	if msg.topic == relayCmdTopic:
		if not firstRun:
			print("not the first run, so allow relay execution.")
			if msg.payload == 'open':
				gdo_relay()
			elif msg.payload == 'close':
				gdo_relay()
		else:
			print("first run. don't allow relay execution.")	

	#elif msg.topic == doorStatusTopic:
	#	if msg.payload == 'get':
	#		doorStatus = getDoorStatus() 
	#		#print("DOOR IS " + doorStatus)
	#		mqttc.publish(doorStatusTopic, doorStatus, 0, False)
			
	firstRun = 0
	print("----------------------------------------------------")

def on_publish(mosq, obj, mid):
    print("mid: "+str(mid))
    print("")
    print("")

def on_subscribe(mosq, obj, mid, granted_qos):
	print("Subscribed: "+str(mid)+" "+str(granted_qos))
	print("")

def on_log(mosq, obj, level, string):
    print(string)

def gdo_relay():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(relayPIN, GPIO.OUT, initial=GPIO.HIGH)
	print "Garage door triggered."
	GPIO.output(relayPIN, False)
	time.sleep(0.5)
	GPIO.output(relayPIN, True)
	publishDoorStatus()
	
def gdo_cam():
	print "Processing request for visual update."
#	camera.capture('/var/www/html/gdoCam/visual_status.jpg')

def main():
	print "Garage Door Opener MQTT script"
	print ""

if __name__ == "__main__":
	main()
	try:
		mqttc = mosquitto.Mosquitto()
		mqttc.on_message = on_message
		mqttc.on_connect = on_connect
		mqttc.on_publish = on_publish
		mqttc.on_subscribe = on_subscribe
		mqttc.username_pw_set("mqttuser", "mqttpassword")
		mqttc.connect("192.168.1.114", 1883, 60)
		mqttc.subscribe("garage/#", 0)
		publishDoorStatus()
		
		rc = 0
		while rc == 0:
			rc = mqttc.loop()
			
	except KeyboardInterrupt:
		GPIO.cleanup()
		
	GPIO.cleanup()
	
