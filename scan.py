# import the necessary packages
import numpy as np
import argparse
import cv2 as cv2
import imutils
from pyimagesearch.transform import order_points
from pyimagesearch.transform import four_point_transform
 
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help = "Path to image")
ap.add_argument("-o", "--output", required = True,
	help = "Path to saved the converted/transformed image")
args = vars(ap.parse_args())

# NOTE: Edge Detecion
# load the image and compute the ratio of the old height
# to the new height, clone it, and resize it
image = cv2.imread(args['image'])
print(args['output'])
print(args['image'])
print(type(image))
ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height = 500)
 
# convert the image to grayscale, blur it, and find edges
# in the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 75, 200)
 
print(image.shape)
# show the original image and the edge detected image
print("STEP 1: Edge Detection")

# NOTE: Finding Contours :
#  assuming the largest 4 sided countour(rectangle) in our image is the piece of paper

# find the contours in the edged image, keeping only the largest ones
cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
 
# loop over the contours
for c in cnts:
	# approximate contours
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
 
	# if our approximated contour has four points, then we
	# assume we found the screen
	if len(approx) == 4:
		screenCnt = approx
		break
 
# apply the four point transform to obtain a top-down
# view of the original image
warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
print("warped", warped.shape) 
 
# show the original and scanned images
cv2.imwrite("/home/pi/hackdemyk/scanned_images/{}".format(args['output']), warped)
