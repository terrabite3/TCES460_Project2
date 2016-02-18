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
	while(num_pics < 31):
		myLCD.clear()
		myLCD.setColor(0, 0, 100)
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
		img = recognizer.take_picture()
		myLCD.clear()
		myLCD.write("Processing...")
		myLCD.clear()
		if len(recognizer.check_for_face(img)) > 0:
			pic_name = "subject"+str(subject_number)+"."+"picture"+str(num_pics)+".png"
			recognizer.save_picture(pic_name, img)
			num_pics = num_pics + 1
			myLCD.setColor(0, 255, 0)
			myLCD.write("Success!")
		else:
			myLCD.setColor(255, 0, 0)
			myLCD.write("No face found.")
			myLCD.setCursor(1,0)
			myLCD.write("... try again.")
		time.sleep(1)


while training:
	if button.read():
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
		trainer.train_2()
		src = "temp_pics_for_training"
		dst = "saved_pictures"
		listOfFiles = os.listdir(src)
		for f in listOfFiles:
			fullPath = src + "/" + f
			subprocess.Popen("mv" + " " + fullPath + " " + dst,shell=True)
		training = False
		
