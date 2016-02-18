#!/usr/bin/python
import mraa
import pyupm_i2clcd as lcd
import time
import random
import recognizer
import csv
import trainer
import shutil
import subprocess
import os

MAX_PICTURES = 10
BUTTON_PIN = 2
button = mraa.Gpio(BUTTON_PIN)
button.dir(mraa.DIR_IN)
## The LCD can only display 16 characters per line
myLCD = lcd.Jhd1313m1(0, 0x3E, 0x62)
training = True

with open('subjects.csv', 'rb') as f:
	i = 0
	reader = csv.reader(f)
	for row in reader:
		i = i + 1
	subject_number = i 

myLCD.clear()
myLCD.setColor(255, 255, 255)
myLCD.setCursor(0, 0)
myLCD.write("Press button")
myLCD.setCursor(1, 0)
myLCD.write("to begin training")

def take_pictures():
	num_pics = 1
	while(num_pics < (MAX_PICTURES + 1)):
		myLCD.clear()
		myLCD.setColor(255, 255, 0)
		myLCD.setCursor(0, 0)
		myLCD.clear()
                myLCD.write("1...")
                time.sleep(1)
                myLCD.write("2...")
                time.sleep(1)
		myLCD.write("3...")
		time.sleep(1)
		myLCD.clear()
		myLCD.write("Taking picture")
		myLCD.setCursor(1, 0)
		myLCD.write("number %d" %num_pics)
		time.sleep(1)
		img = recognizer.take_picture()
		myLCD.clear()
		myLCD.setColor(255, 255, 0)
		myLCD.setCursor(0, 0)
		myLCD.write("Processing...")
		time.sleep(.5)
		gc_img = recognizer.check_for_face(img)
		if len(gc_img) == 1:
			pic_name = "subject"+str(subject_number)+"."+"picture"+str(num_pics)+".png"
			recognizer.save_picture('temp_pics_for_training',pic_name, gc_img[0])
			num_pics = num_pics + 1
			myLCD.clear()
			myLCD.setColor(0, 255, 0)
			myLCD.write("Success!")
			time.sleep(1)
		elif len(gc_img) > 1:
			myLCD.clear()
			myLCD.setColor(255, 0, 0)
                        myLCD.write("Faces > 1.")
                        myLCD.setCursor(1,0)
                        myLCD.write("... try again.")
			time.sleep(1) 
		else:
			myLCD.clear()
			myLCD.setColor(255, 0, 0)
			myLCD.write("No face found.")
			myLCD.setCursor(1,0)
			myLCD.write("... try again.")
			time.sleep(1)


def begin_training():
	myLCD.clear()
	myLCD.setColor(255, 255, 255)
	myLCD.setCursor(0, 0)
	myLCD.write("Enter name")
	myLCD.setCursor(1, 0)
	myLCD.write("using computer")

	name = raw_input('Enter name: ')
	file = csv.writer(open('subjects.csv', 'a'))
	file.writerow([subject_number, name])
	take_pictures()
	time.sleep(2)
	src = "temp_pics_for_training"
	dst = "saved_pictures"
	listOfFiles = os.listdir(src)
	for f in listOfFiles:
		fullPath = src + "/" + f
		subprocess.Popen("mv" + " " + fullPath + " " + dst,shell=True)
	myLCD.clear()
        myLCD.setColor(255, 255, 0)
       	myLCD.setCursor(0, 0)
       	myLCD.write("Training images...")
       	time.sleep(1)
	trainer.train_2('saved_pictures')
	myLCD.clear()
       	myLCD.setColor (0, 255, 0)
       	myLCD.setCursor(0, 0)
       	myLCD.write("Training complete")
        time.sleep(1)

		
