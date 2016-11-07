#!/usr/bin/env python2.7
# Purpose: Process MQTT trigger message from Home Assistant RPi to open garage door.
# Soruce: https://hackaday.io/project/9901/instructions

import sys
import mosquitto
import RPi.GPIO as GPIO
import datetime, time
import logging, json


logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('/home/pi/garagedoor/update_garagestatus.log')
formatter = logging.Formatter("%(asctime)s     %(levelname)s     %(message)s")
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)

firstRun = 1
doorSensorPIN = 18

doorStatusTopic = 'garage/status2'

GPIO.setmode(GPIO.BCM)
GPIO.setup(doorSensorPIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # activate input with PullUp

def getDoorStatus():
	if GPIO.input(doorSensorPIN):
		return 'closed'
	else:
		return 'open'

def publishDoorStatus():
	doorStatus = getDoorStatus()
	currtime = time.strftime("%Y-%m-%d %H:%M:%S")
	payload = { 'datetime_publised': currtime, 'status': doorStatus }
	payload_json = json.dumps(payload)
	print("door status is now... " + payload_json)
	mqttc.publish(doorStatusTopic, payload_json, 0, False)

def main():
	print "Update status of garage door in MQTT broker"
	print ""

if __name__ == "__main__":
	main()
	try:
		mqttc = mosquitto.Mosquitto()
		mqttc.username_pw_set(<user>, <password>)
		mqttc.connect(<mqtt broker address>, 1883, 60)
		mqttc.subscribe("garage/status", 0)	
		
		rc = 0
		while rc == 0:
			time.sleep(5)
			publishDoorStatus()
			
	except Exception, e:
		print str(e)
		logger.error(str(e))
		GPIO.cleanup()
		
	GPIO.cleanup()
	
