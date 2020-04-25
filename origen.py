import time,imutils
import cv2
from PIL import Image
import numpy as np
from twilio.rest import Client
import tkinter
from threading import Thread

cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height

mode = 0

def chng():
    global mode
    mode = 1 
    
def call():
    
    print("estas muerto")

def init():
    Thread(target=mt).start()
    top = tkinter.Tk()
    B = tkinter.Button(top, text ="Start Alarm", command=chng)
    B.pack()
    top.mainloop()



def mt():
    con = 0
    global  mode
    
    e,f_start = cap.read()
    f_start = imutils.resize(f_start, width=500)
    gray = cv2.cvtColor(f_start, cv2.COLOR_BGR2GRAY)
    f_start = cv2.GaussianBlur(gray, (21, 21), 0)

    while True:
        ret, frame = cap.read()
        frame = imutils.resize(frame, width=500)
        
        if(mode==1):
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (5, 5), 0)
            frameDelta = cv2.absdiff(gray, f_start)
            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
            f_start = gray

            if(thresh.sum()>100):
                con+=1
            else:
                if(con>0):
                    con-=1
            
            cv2.imshow('vi',thresh)
       
            if(con>20):
                print("calling")
                mode =0
                con = 0
                call()
                cv2.destroyWindow('vi')
                
           
            else:
                pass

    
        if(mode==0):
            #print("showing")
            cv2.imshow('video',frame)
            
        #print(mode)
    #     cv2.imwrite('hello.jpg',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27: # press 'ESC' to quit
            break

    cap.release()
    cv2.destroyAllWindows()
    
init()