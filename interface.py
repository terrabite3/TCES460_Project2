#!/usr/bin/python
import mraa
import pyupm_i2clcd as lcd
import time
import random
import recognizer
import training_interface

from Servo import *

def find_face():
	print("TODO: Entering authenticate() stub")

   	myLCD.clear()
	myLCD.setColor(255, 255, 0)
	myLCD.setCursor(0, 0)
	myLCD.write("Taking picture...")

	time.sleep(2)
	img = recognizer.take_picture()
	myLCD.clear()
	myLCD.setCursor(0,0)
	myLCD.write("Searching for")
	myLCD.setCursor(1,0)
	myLCD.write("faces...")
	images = recognizer.check_for_face(img)
	
	numfaces = len(images)
	print numfaces
	if numfaces == 0:
		myLCD.clear()
		myLCD.setColor(255, 0, 0)
		myLCD.setCursor(0,0)
		myLCD.write("Face not detected")
		time.sleep(2)
		return None
	else:
		return images	

def authenticate():
	images = find_face()
	if images:
		for image in images:
			recognizer.save_picture("access_request_images","accessimage.png", image)
		recognized = recognizer.recognize_face(images)
		print recognized
		if type(recognized) is str:
			denied()
		else:
			granted()			

def granted():
	print("TODO: Entering granted() stub")
	    
	myLCD.clear()
	myLCD.setColor(0, 255, 0)
	myLCD.setCursor(0, 0)
	myLCD.write("Welcome home,")
	myLCD.setCursor(1, 0)
	name = random.choice(["Stefan", "Demetra", "Gabrielle"])
	myLCD.write(name)

	servo.write(170)
	time.sleep(5)
	servo.write(0)

def denied():
	print("TODO: Entering denied() stub")
    
	myLCD.clear()
	myLCD.setColor(255, 0, 0)
	myLCD.setCursor(0, 0)
	myLCD.write("Unauthorized")
	myLCD.setCursor(1, 0)
	myLCD.write("Calling 911")

	time.sleep(5)

def greeting():
	myLCD.clear()
	myLCD.setColor(255, 255, 255)
	myLCD.setCursor(0, 0)
	myLCD.write("FaceLock")
	myLCD.setCursor(1, 0)
	myLCD.write("Press button")

	servo.write(0)

BUTTON_PIN = 2
TRAINING_BUTTON_PIN = 8
button = mraa.Gpio(BUTTON_PIN)
training_button = mraa.Gpio(TRAINING_BUTTON_PIN)
button.dir(mraa.DIR_IN)
training_button.dir(mraa.DIR_IN)

## The LCD can only display 16 characters per line
myLCD = lcd.Jhd1313m1(0, 0x3E, 0x62)

servo = Servo("Lock")
servo.attach(3)

greeting()

while True:

	if button.read():
		authenticate() 
	if training_button.read():
		training_interface.begin_training()
        greeting()
	time.sleep(0.1)
