# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 16:02:14 2020

@author: Admin
"""
import cv2
import numpy as np
import math
import webbrowser as wb
import os
import tkinter as tk
from tkinter import messagebox as msg
def clear():
    t1.delete(0,last=len(t1.get())) 
def clear1():    
    t2.delete(0,last=len(t2.get())) 
def clear2():    
    t3.delete(0,last=len(t3.get()))  
    
def Proceed():
    tabs=0
    count=0
    fingers2=t1.get()
    fingers3=t2.get()
    fingers4=t3.get()
    if(len(t1.get())==0 or len(t2.get())==0 or len(t3.get())==0):
        msg.showwarning("Sorry! ","You Are Fail While Giving The Browser Names")
    else:
        cap = cv2.VideoCapture(0)
        while(cap.isOpened()):#ret value
            # read image
            ret, img = cap.read()
            # get hand data from the rectangle sub window on the screen
            cv2.rectangle(img, (400,400), (100,100), (0,255,0),0)
            crop_img = img[100:400, 100:400]
            # convert to grayscale
            grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
            # applying gaussian blur
            value = (35, 35)
            blurred = cv2.GaussianBlur(grey, value, 0)
            # thresholdin: Otsu's Binarization method
            _, thresh1 = cv2.threshold(blurred, 127, 255,
                                   cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
            # show thresholded image, not necessary and can be skipped
            cv2.imshow('Thresholded', thresh1)
            # check OpenCV version to avoid unpacking error
            (version, _, _) = cv2.__version__.split('.')
            if version == '3':
                image, contours, hierarchy = cv2.findContours(thresh1.copy(), \
                cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            elif version == '2':
                contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, \
                cv2.CHAIN_APPROX_NONE)
            # find contour with max area
            cnt = max(contours, key = lambda x: cv2.contourArea(x))
            # create bounding rectangle around the contour (can skip below two lines)
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(crop_img, (x, y), (x+w, y+h), (0, 0, 255), 0)
            # finding convex hull
            hull = cv2.convexHull(cnt)
            # drawing contours
            drawing = np.zeros(crop_img.shape,np.uint8)
            cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 0)
            cv2.drawContours(drawing, [hull], 0,(0, 0, 255), 0)
            # finding convex hull
            hull = cv2.convexHull(cnt, returnPoints=False)#  return point false to find convexity defects
            # finding convexity defects
            defects = cv2.convexityDefects(cnt, hull)
            count_defects = 0
            cv2.drawContours(thresh1, contours, -1, (0, 255, 0), 3)# to draw all contours pass -1
            # applying Cosine Rule to find angle for all defects (between fingers)
            # with angle > 90 degrees and ignore defects
            for i in range(defects.shape[0]):
                s,e,f,d = defects[i,0] #[ start point, end point, farthest point, approximate distance to farthest point ]
                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])
                # find length of all sides of triangle
                a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
                # apply cosine rule here
                angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
                # ignore angles > 90 and highlight rest with red dots
                if angle <= 90:
                    count_defects += 1
                    cv2.circle(crop_img, far, 1, [0,0,255], -1)
            #dist = cv2.pointPolygonTest(cnt,far,True)
        
            # draw a line from start to end i.e. the convex points (finger tips)
            # (can skip this part)
            cv2.line(crop_img,start, end, [0,255,0], 2)
            #cv2.circle(crop_img,far,5,[0,0,255],-1)
            if count==0:
                cv2.putText(img,"Wait for it :p", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, 3)
        # define actions required
            if count_defects == 1 and count!=2 and tabs<=8:
                wb.open_new_tab('http://www.'+fingers2+'.com')
                tabs=tabs+1
                cv2.putText(img,"2."+fingers2, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,0,0), 3)
                count=2    
            elif count_defects == 2 and count!=3 and tabs<=8:
                wb.open_new_tab('http://www.'+fingers3+'.com')
                tabs=tabs+1
                cv2.putText(img, "3."+fingers3, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,255), 3)
                count=3
            elif count_defects == 3 and count!=4 and tabs<=8:
                wb.open_new_tab('http://www.'+fingers4+'.com')
                cv2.putText(img, "4."+fingers4, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,165,0), 3)
                tabs=tabs+1
                count=4
            elif count_defects == 4 and count!=5:
                cv2.putText(img,"5.Close Web browser", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 3, 3)
                os.system("taskkill /im chrome.exe /f")
                tabs=0
                count=5
            else:
                cv2.putText(img,"", (50, 100),\
                cv2.FONT_HERSHEY_SIMPLEX, 3, 3)
            if count==2:
                cv2.putText(img, "2."+fingers2, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,0,0), 3)
            elif count==3:
                cv2.putText(img, "3."+fingers3, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,255), 3)
            elif count==4:
                cv2.putText(img, "4."+fingers4, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,165,0), 3)
            elif count==5:
                cv2.putText(img, "5.WebBrowser close", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, 3)
        # show appropriate images in windows
            cv2.imshow('Gesture', img)
            all_img = np.hstack((drawing, crop_img))
            #not necessary to show contours and can be skipped
            cv2.imshow('Contours', all_img)
            k = cv2.waitKey(10)
            if k == ord('s'):
                break
window=tk.Tk()
c=0
window.configure(width=500,height=500,bg='#ffffff')
lp0=tk.Label(window,width=30,height=2,text="HAND WEB BROWSER",bg='white',fg="purple",font=("times",30,'bold'))
lp0.place(x=400,y=50)
lp1=tk.Label(window,width=50,height=1,text="Enter your browser name1 for two fingers",bg='#fc46aa',fg="white",font=("times",15,'bold'))
lp1.place(x=100,y=200)
lp2=tk.Label(window,width=50,height=1,text="Enter your browser name2 for three fingers",bg='#fc46aa',fg="white",font=("times",15,'bold'))
lp2.place(x=100,y=300) 
lp3=tk.Label(window,width=50,height=1,text="Enter your browser name3 for four fingers",bg='#fc46aa',fg="white",font=("times",15,'bold'))
lp3.place(x=100,y=400)        
t1=tk.Entry(window,width=35,fg='purple',bg='pink',font=("times",15,'bold'))
t1.place(x=750,y=200)  
fingers2=t1.get()
t2=tk.Entry(window,width=35,fg='purple',bg='pink',font=("times",15,'bold'))
t2.place(x=750,y=300)
fingers3=t2.get()
t3=tk.Entry(window,width=35,fg='purple',bg='pink',font=("times",15,'bold'))
t3.place(x=750,y=400)
fingers4=t3.get()
b1=tk.Button(window,width=10,height=1,text="Proceed",command=Proceed,bg='#a8329b',fg='white',font=("times",15,'bold'),activebackground="white")
b1.place(x=650,y=500)
b2=tk.Button(window,width=10,text="Clear",command=clear,bg='#3300ff',fg='white',font=("times",15,'bold'),activebackground="white")
b2.place(x=1200,y=200)
b3=tk.Button(window,width=10,text="Clear",command=clear1,bg='#3300ff',fg='white',font=("times",15,'bold'),activebackground="white")
b3.place(x=1200,y=300)
b4=tk.Button(window,width=10,text="Clear",command=clear2,bg='#3300ff',fg='white',font=("times",15,'bold'),activebackground="white")
b4.place(x=1200,y=400)
window.mainloop()
