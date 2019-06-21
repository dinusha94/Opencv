from threading import Thread,Event
import time
import cv2
import numpy as np
#from Tkinter import*
import Tkinter as tk
from multiprocessing import Array
from ctypes import c_int32

camera = cv2.VideoCapture(0)

class firstclass(tk.Frame):
    
    def __init__(self,master):#self is the class object variable master is the tkinter variable
        tk.Frame.__init__(self)#initiate main WINDOW for GUI
        self.master = master
        
        
        self.hsvArray = Array(c_int32,6)#Array to store HSV slider data

        self.s1 = tk.Scale(self, from_=0, to=255, orient=tk.HORIZONTAL,label ="H_min",
                         command=lambda pos:self.update_s1(pos))
        self.s1.pack(side=tk.LEFT)
        
        self.s2 = tk.Scale(self, from_=0, to=255, orient=tk.HORIZONTAL,label ="S_min",
                         command=lambda pos:self.update_s2(pos))
        self.s2.pack(side=tk.LEFT)
        
        self.s3 = tk.Scale(self, from_=0, to=255, orient=tk.HORIZONTAL,label ="V_min",
                         command=lambda pos:self.update_s3(pos))
        self.s3.pack(side=tk.LEFT)
        
        self.s4 = tk.Scale(self, from_=0, to=255, orient=tk.HORIZONTAL,label ="H_max",
                         command=lambda pos:self.update_s4(pos))
        self.s4.pack(side=tk.LEFT)
        
        self.s5 = tk.Scale(self, from_=0, to=255, orient=tk.HORIZONTAL,label ="S_max",
                         command=lambda pos:self.update_s5(pos))
        self.s5.pack(side=tk.LEFT)
        
        self.s6 = tk.Scale(self, from_=0, to=255, orient=tk.HORIZONTAL,label ="V_max",
                         command=lambda pos:self.update_s6(pos))
        self.s6.pack(side=tk.LEFT)
        
        self.quitbtn = tk.Button(self,text = "Quit",command=self.quit)
        self.quitbtn.pack(side=tk.BOTTOM)
        self._quit = Event()
        
        
       

    def update_s1(self,pos):
        self.hsvArray[0] = c_int32(int(pos))
        
    def update_s2(self,pos):
        self.hsvArray[1] = c_int32(int(pos))
        
    def update_s3(self,pos):
        self.hsvArray[2] = c_int32(int(pos))    
        
    def update_s4(self,pos):
        self.hsvArray[3] = c_int32(int(pos))

    def update_s5(self,pos):
        self.hsvArray[4] = c_int32(int(pos))

    def update_s6(self,pos):
        self.hsvArray[5] = c_int32(int(pos))

    def video_capture(self):
        self._quit.clear()
        self.capture_thread = Thread(target=track, args=(self.hsvArray,self._quit))
        self.capture_thread.start()

    def quit(self):
        self._quit.set()
        try:
            self.capture_thread.join()
        except TypeError:
            pass
        self.master.destroy()    
        

        
#main loop
def track(hsvArray,quit):
    while not quit.is_set():
        #print hsvArray[:]
        
        (grabbed, image) = camera.read()

        # Blur the image to reduce noise
        #blur = cv2.GaussianBlur(image, (5,5),0)
        blur = cv2.pyrMeanShiftFiltering(image,10,50)#advanced
        
        # Convert BGR to HSV
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        # Threshold the HSV image for only green colors
        lower_green = np.array([hsvArray[0],hsvArray[1],hsvArray[2]])
        upper_green = np.array([hsvArray[3],hsvArray[4],hsvArray[5]])
        
        # Threshold the HSV image to get only green colors
        mask = cv2.inRange(hsv, lower_green, upper_green)

       
        contours,_ = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        #print contours
        cv2.drawContours(image, contours, -1, (0,255,0), 3)
##        largest_area = 10000
##        for c in contours:
##            area = cv2.contourArea(c)
##            if area > largest_area:
##                largest_area = area
##                largest_contour_index = c
##                (x, y, w, h) = cv2.boundingRect(c)
##                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
        cv2.imshow("Frame", mask)
        cv2.imshow('Frame2',image)
        #cv2.imshow('Frame3',hsv)
        key = cv2.waitKey(1) & 0xFF



if __name__ == "__main__":
    root = tk.Tk()
    selectors = firstclass(root)
    selectors.pack()
    selectors.video_capture()
    root.mainloop()
##    t1=threading.Thread(target=track,args=())
##    t2=threading.Thread(target=scalegui,args=())
##    t1.start()
##    t2.start()
##    t1.join()
##    t2.join()
