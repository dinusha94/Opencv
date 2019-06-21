
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import serial

ser = serial.Serial('COM14',9600, timeout=.1)

greenLower = (30, 86, 181)
greenUpper = (32, 255, 255)

camera = cv2.VideoCapture(1)

camera.set(3, 200.)# set the frame size
camera.set(4, 200.) 

	# keep looping
while True:
	# grab the current frame
	(grabbed, frame) = camera.read()
 
	frame = imutils.resize(frame, width=600)
	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
 
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
 	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	cx=center[0]
	#print(cx)
##	k = float(9)/600
##	s = k*cx
##	z=round(s,1)+3
##	pwm.start(z)
	k=str(chr(cx))
	#print(k)
	#Examples of iterable values:
##
##   1. str
##   2. unicode
##   3. list
##   4. tuple
##   5. xrange and range
	# int is not itterable so we need to convert cx to str to send to arduino
	ser.write(k)
 
