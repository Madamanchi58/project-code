# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 07:29:24 2020

@author: Admin
"""

# Imports
import numpy as np
import cv2
import math
import webbrowser as wb
import tkinter as tk
from tkinter import messagebox as msg
#Definitions for clear button actions
def clear1():
    t1.delete(0,last=len(t1.get())) 
def clear2():    
    t2.delete(0,last=len(t2.get())) 
def clear3():    
    t3.delete(0,last=len(t3.get()))
def clear4():    
    t4.delete(0,last=len(t4.get()))
def clear5():    
    t5.delete(0,last=len(t5.get()))
def clear6():    
    t6.delete(0,last=len(t6.get()))
#Definition for proceed button action   
def Proceed():
    #Assign domain data to finger variables as input
    finger1=t1.get()
    finger2=t2.get()
    finger3=t3.get()
    finger4=t4.get()
    finger5=t5.get()
    finger6=t6.get()
    #Check whether the length is empty or not
    if(len(t1.get())==0  or len(t2.get())==0 or len(t3.get())==0 or len(t4.get())==0  or len(t5.get())==0 or len(t6.get())==0):
        #Display warning message when length of string is empty
        msg.showwarning("Sorry! ","You Are Fail While Giving The Browser Names")
    else:
    
    
    # Open Camera
        capture = cv2.VideoCapture(0)
        o=t=th=f=fi=s=1
        
        while capture.isOpened():
        
            # Capture frames from the camera
            ret, frame = capture.read()
        
        
            # Get hand data from the rectangle sub window
            cv2.rectangle(frame, (50, 50), (400, 400), (0, 255, 0), 3)
            crop_image = frame[50:400, 50:400]
            #crop_image
            
            # Apply Gaussian blur
            blur = cv2.GaussianBlur(crop_image, (3, 3), 0)
           
        
            # Change color-space from BGR -> HSV
            hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
            
            # Create a binary image with where white will be skin colors and rest is black
            mask = cv2.inRange(hsv, np.array([2, 0, 0]), np.array([20, 255, 255]))
            # Kernel for morphological transformation
            kernel = np.ones((5, 5))
        
            # Apply morphological transformations to filter out the background noise
            dilation = cv2.dilate(mask, kernel, iterations=1)
            erosion = cv2.erode(dilation, kernel, iterations=1)
            
        
            # Apply Gaussian Blur and Threshold
            filtered = cv2.GaussianBlur(erosion, (3, 3), 0)
            ret, thresh = cv2.threshold(filtered, 127, 255, 0)
        
        
            # Show threshold image
            cv2.imshow("Thresholded", thresh)
        
            # Find contours
            image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
            try:
                # Find contour with maximum area
                contour = max(contours, key=lambda x: cv2.contourArea(x))
        
                # Create bounding rectangle around the contour
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(crop_image, (x, y), (x + w, y + h), (0, 0, 255), 0)
        
        
                # Find convex hull
                hull = cv2.convexHull(contour)
        
                # Draw contour
                drawing = np.zeros(crop_image.shape, np.uint8)
                cv2.drawContours(drawing, [contour], -1, (0, 255, 0), 0)
        
                # Find convexity defects
                hull = cv2.convexHull(contour, returnPoints=False)
                defects = cv2.convexityDefects(contour, hull)
        
                # Use cosine rule to find angle of the far point from the start and end point i.e. the convex points (the finger
                # tips) for all defects
                count_defects = 0
        
                for i in range(defects.shape[0]):
                    s, e, f, d = defects[i, 0]
                    start = tuple(contour[s][0])
                    end = tuple(contour[e][0])
                    far = tuple(contour[f][0])
        
                    a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                    b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                    c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                    angle = (math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 180) / 3.14
        
                    # if angle > 90 draw a circle at the far point
                    if angle <= 90:
                        count_defects += 1
                        cv2.circle(crop_image, far, 1, [0, 0, 255], -1)
        
                    cv2.line(crop_image, start, end, [0, 255, 0], 2)
        
                # Print number of fingers
                if count_defects == 0:
                    cv2.putText(frame, "ONE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255),2)
                elif count_defects == 1:
                    cv2.putText(frame, "TWO", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
                elif count_defects == 2:
                    cv2.putText(frame, "THREE", (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
                elif count_defects == 3:
                    cv2.putText(frame, "FOUR", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
                elif count_defects == 4:
                    cv2.putText(frame, "FIVE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
                elif count_defects == 5:
                    cv2.putText(frame, "SIX", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
                else:
                    pass
                
                if count_defects == 0:
                    if o==1:
                        wb.open_new_tab('http://www.'+finger1+'.com')
                        o=o+1
                elif count_defects == 1:
                    if t==1:
                        wb.open_new_tab('http://www.'+finger2+'.com')
                        t=t+1
                elif count_defects == 2:
                    if th==1:
                        wb.open_new_tab('http://www.'+finger3+'.com')
                        th=th+1
                elif count_defects == 3:
                    if f==1:
                        wb.open_new_tab('http://www.'+finger4+'.com')
                        f=f+1
                elif count_defects == 4:
                    if fi==1:
                        wb.open_new_tab('http://www.'+finger5+'.com')
                        fi=fi+1
                elif count_defects == 5:
                    if s==1:
                        wb.open_new_tab('http://www.'+finger6+'.com')
                        s=s+1
                else:
                    pass
                
            except:
                pass
        
            # Show required images
            cv2.imshow("Gesture", frame)
            all_image = np.hstack((drawing, crop_image))
            cv2.imshow('Contours', all_image)
        
            # Close the camera if 'q' is pressed
            if cv2.waitKey(1) == ord('q'):
                break
        #destroy the opened windows
        cv2.destroyAllWindows()
        capture.release()
       
#Create window using tkinter 
window=tk.Tk()
window.configure(width=1000,height=1000,bg='#ffffff')
#create labels
lp0=tk.Label(window,width=30,height=2,text="HAND WEB BROWSER",bg='white',fg="purple",font=("times",30,'bold'))
lp0.place(x=400,y=5)
lp1=tk.Label(window,width=50,height=1,text="Enter your browser name1 for one finger",bg='#fc46aa',fg="white",font=("times",15,'bold'))
lp1.place(x=100,y=140)
lp2=tk.Label(window,width=50,height=1,text="Enter your browser name2 for two fingers",bg='#fc46aa',fg="white",font=("times",15,'bold'))
lp2.place(x=100,y=200) 
lp3=tk.Label(window,width=50,height=1,text="Enter your browser name3 for three fingers",bg='#fc46aa',fg="white",font=("times",15,'bold'))
lp3.place(x=100,y=260)     
lp4=tk.Label(window,width=50,height=1,text="Enter your browser name4 for four fingers",bg='#fc46aa',fg="white",font=("times",15,'bold'))
lp4.place(x=100,y=320)    
lp5=tk.Label(window,width=50,height=1,text="Enter your browser name5 for five fingers",bg='#fc46aa',fg="white",font=("times",15,'bold'))
lp5.place(x=100,y=380)    
lp6=tk.Label(window,width=50,height=1,text="Enter your browser name6 for six fingers",bg='#fc46aa',fg="white",font=("times",15,'bold'))
lp6.place(x=100,y=440)       
lp7=tk.Label(window,width=50,height=2,text="SAI TIRUMALA NVR ENGINEERING COLLEGE",bg='yellow',fg='red',font=("times",35,'bold'))
lp7.place(x=50,y=650)
#create entry boxes
t1=tk.Entry(window,width=35,fg='purple',bg='pink',font=("times",15,'bold'))
t1.place(x=750,y=140)  
finger1=t1.get()
t2=tk.Entry(window,width=35,fg='purple',bg='pink',font=("times",15,'bold'))
t2.place(x=750,y=200)
finger2=t2.get()
t3=tk.Entry(window,width=35,fg='purple',bg='pink',font=("times",15,'bold'))
t3.place(x=750,y=260)
finger3=t3.get()
t4=tk.Entry(window,width=35,fg='purple',bg='pink',font=("times",15,'bold'))
t4.place(x=750,y=320)
finger4=t4.get()
t5=tk.Entry(window,width=35,fg='purple',bg='pink',font=("times",15,'bold'))
t5.place(x=750,y=380)
finger5=t5.get()
t6=tk.Entry(window,width=35,fg='purple',bg='pink',font=("times",15,'bold'))
t6.place(x=750,y=440)
finger6=t6.get()
#create buttons
b1=tk.Button(window,width=10,height=1,text="Proceed",command=Proceed,bg='#a8329b',fg='white',font=("times",15,'bold'),activebackground="white")
b1.place(x=650,y=550)
b2=tk.Button(window,width=10,text="Clear",command=clear1,bg='#3300ff',fg='white',font=("times",15,'bold'),activebackground="white")
b2.place(x=1200,y=140)
b3=tk.Button(window,width=10,text="Clear",command=clear2,bg='#3300ff',fg='white',font=("times",15,'bold'),activebackground="white")
b3.place(x=1200,y=200)
b6=tk.Button(window,width=10,text="Clear",command=clear3,bg='#3300ff',fg='white',font=("times",15,'bold'),activebackground="white")
b6.place(x=1200,y=260)
b4=tk.Button(window,width=10,text="Clear",command=clear4,bg='#3300ff',fg='white',font=("times",15,'bold'),activebackground="white")
b4.place(x=1200,y=320)
b5=tk.Button(window,width=10,text="Clear",command=clear5,bg='#3300ff',fg='white',font=("times",15,'bold'),activebackground="white")
b5.place(x=1200,y=380)
b6=tk.Button(window,width=10,text="Clear",command=clear6,bg='#3300ff',fg='white',font=("times",15,'bold'),activebackground="white")
b6.place(x=1200,y=440)
#exit from loop
window.mainloop()
