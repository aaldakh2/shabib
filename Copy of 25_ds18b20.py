#!/usr/bin/env python
#----------------------------------------------------------------
#Note:
#ds18b20's data pin must be connected to pin7.
#replace the 28-0316a0cf12ff as yours.
#----------------------------------------------------------------
import os

ds18b20 = ''

def setup():
	global ds18b20
	for i in os.listdir('/sys/bus/w1/devices'):
		if i != 'w1_bus_master1':
			ds18b20 = i

def read():
#	global ds18b20
	location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
	tfile = open(location)
	text = tfile.read()
	tfile.close()
	secondline = text.split("\n")[1]
	temperaturedata = secondline.split(" ")[9]
	temperature = float(temperaturedata[2:])
	temperature = temperature / 1000
	return temperature

def loop():
	while True:
		if read() != None:
			print "Current temperature : %0.3f C" % read()
			if read() < 24:
				import RPi.GPIO as GPIO
				GPIO.setmode(GPIO.BCM)
				GPIO.setwarnings(False)
				GPIO.setup(18,GPIO.OUT)
				print "LED on"
				GPIO.output(18,GPIO.HIGH)
			else:
				import RPi.GPIO as GPIO
				GPIO.setwarnings(False)
				GPIO.setmode(GPIO.BCM)
				GPIO.setup(18,GPIO.OUT)
				print "LED off"
				GPIO.output(18,GPIO.LOW)
def destroy():
	pass

if __name__ == '__main__':
	try:
		setup()
		loop()
	except KeyboardInterrupt:
		destroy()
