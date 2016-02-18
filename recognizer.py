#!/usr/bin/python

import cv2, os
import numpy
import trainer
import socket

TRAINING_FILE = 'training.xml'

# Stefan's hardcoded IP address, dynamic
HOST_IP = '10.16.3.253'
HOST_PORT = 5001

# For face recognition we will use the LBPH Face Recognizer
recognizer = cv2.createLBPHFaceRecognizer()
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier('haarcascade_eye.xml')

def is_non_zero_file(fpath):
	return True if os.path.isfile(fpath) and os.path.getsize(fpath) > 0 else False
	
def take_picture():
	cam = cv2.VideoCapture(0)
	ret, img = cam.read()
	
	socket.settimeout(1)
	sock = socket.socket()
	neterror = sock.connect_ex((HOST_IP, HOST_PORT))
	if neterror:
		return img
	else:
		encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
		result, imgencode = cv2.imencode('.jpg', img, encode_param)
		data = numpy.array(imgencode)
		stringData = data.tostring()

		sock.send( str(len(stringData)).ljust(16));
		sock.send( stringData );
		sock.close()
	
		return img

def save_picture(path, pictureName, img):
	cv2.imwrite(path + "/" + pictureName, img)
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
			print predicted
			if predicted[1] < 20:
				predicted_saved = predicted
				face_authorized = True
	
		if face_authorized:
			return predicted_saved
		else: 
			return "Face not authorized"
	else:
		return "Training file not found"
