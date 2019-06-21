import numpy as np
import cv2
import time

#### working better for slow frame rate ###

# Capture video from file
cap = cv2.VideoCapture('vid1.avi')
car_cascade = cv2.CascadeClassifier('car1.xml')


##img = cv2.imread('car5.jpg')
##
##blur = cv2.GaussianBlur(img, (5,5),0)
##
##gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
##       
##cars = car_cascade.detectMultiScale(gray, 1.1, 3)
##        
##for (x,y,w,h) in cars:
##    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
##
##cv2.imshow('frame',img)
##cv2.waitKey(0)
##cv2.destroyAllWindows()

        
while True:

    ret, frame = cap.read()
    ##print frame.shape[:2]
    
    if ret == True:
        ##blur = cv2.GaussianBlur(frame, (5,5),0)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
       
        cars = car_cascade.detectMultiScale(gray, 1.2, 5)
        
        for (x,y,w,h) in cars:
            if w < 120:
                break##skip those detections not dangeres
            else:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                normal_dist = int(360 - (y+h))
                if normal_dist < 50:
                    print "slow"
                
        cv2.line(frame, (0,360), (720,360), (255,255,0),3)## for cars line should be moved further    
        cv2.imshow('frame',frame)
        ##time.sleep(0.001)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()
