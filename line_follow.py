import cv2
import numpy as np
import time
from numpy import interp
import serial
import time

capture = cv2.VideoCapture(0)
##    capture.set(3, 255)# set the frame size
##    capture.set(4, 255)
ser = serial.Serial('COM14',9600, timeout=.1)
    

# Threshold the HSV image for only green colors
lower_black = np.array([0,0,0])
upper_black = np.array([109,180,135])     
    
    
    
  
        
while True:
    okay, image = capture.read()
    img = image[160:320, 0:640]
    # Blur the image to reduce noise
    blur = cv2.GaussianBlur(img, (5,5),0)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    

    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_black, upper_black)
    
    # Blur the mask
    bmask = cv2.GaussianBlur(mask, (5,5),0)
    
    contours,hier = cv2.findContours(bmask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    #sort the conture list to get the two largest contures
    contours.sort(key = cv2.contourArea,reverse = 1 )

    #left lane line
    M = cv2.moments(contours[0])
    ctr = (int(M["m10"] / M["m00"]),int(M["m01"] / M["m00"]))
    cv2.circle(image, ctr, 4, (0,0,0))

    #right lane line
    M1 = cv2.moments(contours[1])
    ctr1 = (int(M1["m10"] / M1["m00"]),int(M1["m01"] / M1["m00"]))
    cv2.circle(image, ctr1, 4, (0,0,0))
    
    # send data to controller
    diviation = int((160 - ctr[0])//2 + (480 - ctr1[0])//2)
    print(diviation)
    k = str(chr(diviation))
    
    #print(k)
    

    cv2.line(image, (ctr[0],380), (ctr[0],420), (0,0,255),3)
    cv2.line(image, (ctr1[0],380), (ctr1[0],420), (0,0,255),3)

    cv2.line(image, (160,380), (160,420), (0,255,0),3)## left limit
    cv2.line(image, (480,380), (480,420), (0,255,0),3)## right limit
    
    cv2.line(image, (40,400), (600,400), (255,255,0),3)
    cv2.line(image, (320,380), (320,420), (255,0,0),3) 

    # Display full-color image
    cv2.imshow('LANE Tracker', image)
    cv2.imshow("Frame", bmask)
    key = cv2.waitKey(1) & 0xFF
    ser.write(k)
   
          
