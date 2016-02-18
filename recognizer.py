#!/usr/bin/python

import cv2, os
import numpy
import trainer

TRAINING_FILE = 'training.xml'

# For face recognition we will use the LBPH Face Recognizer
recognizer = cv2.createLBPHFaceRecognizer()
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier('haarcascade_eye.xml')

def is_non_zero_file(fpath):
	return True if os.path.isfile(fpath) and os.path.getsize(fpath) > 0 else False
	
def take_picture():
	cam = cv2.VideoCapture(0)
	ret, img = cam.read()
	return img

def save_picture(pictureName, img):
	cv2.imwrite("temp_pics_for_training/" + pictureName, img)
	return img
	
def check_for_face(image):
	images = []
	gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
	faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5, minSize=(30, 30), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
	# If face is detected, append the face to images and label the label to labels.
	for(x, y, w, h) in faces:
		print "GOOD"
		images.append(gray[y: y + h, x: x + w])
	return images

def recognize_face(images):
	predicted_saved = []
	face_authorized = False
	# Checking a trained file already exists
	if is_non_zero_file(TRAINING_FILE):
		print "Loading training file..."
		recognizer.load(TRAINING_FILE)
		for image in images:
			predicted = recognizer.predict(image)
			if predicted[1] < 100:
				predicted_saved = predicted
				face_authorized = true
	
		if face_authorized:
			return predicted_saved
		else: 
			return "Face not authorized"
	else:
		return "Training file not found"
