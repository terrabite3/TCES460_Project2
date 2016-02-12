#!/usr/bin/python

# Import the required modules
import cv2, os
import numpy as np
from PIL import Image

# For face detection we will use the Haar Cascade provided by OpenCV
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# For face recognition we will use the LBPH Face Recognizer
recognizer = cv2.createLBPHFaceRecognizer()

def get_images_and_labels(path):
	print "Adding faces to training set..."
	# Append all the absolute image paths in a list image_paths
	image_paths = [os.path.join(path, f) for f in os.listdir(path)]
	# images will contain the face images
	images = []
	# labels will contain the label that is assigned to the image
	labels = []
	for image_path in image_paths:
		print image_path
		nbr = int(os.path.split(image_path)[1].split(".")[0].replace("subject", ""))
		img = cv2.imread(image_path)
		image_pil = Image.open(image_path).convert('L')
		image = np.array(image_pil, 'uint8')
		gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
		faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5, minSize=(30, 30), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
		# If face is detected, append the face to images and label the label to labels.
		for(x, y, w, h) in faces:
			images.append(image[y: y + h, x: x + w])
			labels.append(nbr)
	return images, labels

path = 'yalefaces'
images, labels = get_images_and_labels(path)

# Perform the training
print "Training..."
recognizer.train(np.array(images), np.array(labels))

# Try to predict a face
predict_image = cv2.imread('yalefaces/subject01.wink.png', cv2.CV_LOAD_IMAGE_GRAYSCALE)
faces = faceCascade.detectMultiScale(predict_image,scaleFactor=1.1,minNeighbors=5, minSize=(30, 30), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
for(x, y, w, h) in faces:
	predicted = recognizer.predict(predict_image[y: y + h, x: x + w])
	print predicted
