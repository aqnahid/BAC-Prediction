from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from Definitions.jerkDetector import detectors
from Definitions.predictor import predictor

import cv2
import numpy as np

Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (640, 480)
        play: False
    Button:
        text: 'Measure BAC'
        on_press: root.capture0()
        size_hint_y: None
        height: '48dp'
''')

class CameraClick(BoxLayout):
    def capture0(self):
        #Eye Cascade can be found at:
        #https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
        #Download the haarcascade_eye.xml and paste it tho the same folder of "run.py"
        eyes = cv2.CascadeClassifier('haarcascade_eye.xml')

        #Capture video:
        self.capture = cv2.VideoCapture(0)
        cap = self.capture

        w = 640
        h = 480
        thresh = 0      #0 for black, 255 for white
        maxValue = 200

        notDetected = True
        threshIncrement=5
        
        pupilX=[]
        pupilY=[]
        
        while(cap.isOpened()):
            ret, frame = cap.read()
            frameShow=frame
            if ret==True:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                detected = eyes.detectMultiScale(frame, 1.3, 5)
                pupilFrame = frame
                pupilO = pupilFrame
                windowClose = np.ones((5,5),np.uint8)
                windowOpen = np.ones((2,2),np.uint8)
                windowErode = np.ones((2,2),np.uint8)

                for (x,y,w,h) in detected:
                    cv2.rectangle(frameShow,(x,y),((x+w),(y+h)), (0,0,255),1)
                    cv2.line(frameShow,(x,int(y+h*.5)),(x+w,int(y+h*.5)),(255,0,0),1)
                    pupilFrame = cv2.equalizeHist(frame[int(y+(h*.25)):(y+h), x:(x+w)])
                    #BLURR to reduce computation:
                    pupilFrame = cv2.bilateralFilter(pupilFrame,15,90,90)
                    pupilO = pupilFrame
                    #Thershold of pupilFrame
                    _,pupilFrame = cv2.threshold(pupilFrame,thresh,maxValue,cv2.THRESH_BINARY)
                    pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_CLOSE, windowClose)
                    pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_ERODE, windowErode)
                    pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_OPEN, windowOpen)
                    threshold = cv2.inRange(pupilFrame,0,50) #CHANGE 250 to 0
                    _,contours, hierarchy = cv2.findContours(threshold,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
                    #Thresh Increment
                    if len(contours)<=0 and notDetected == True:
                        thresh=thresh+threshIncrement
                    else:
                        notDetected = False
                        
                    #Detect the biggest contur
                    if len(contours)>0:
                        bigRad=0
                        bigRadI=0
                        rad=[]
                        contX=[]
                        contY=[]
                        maxDivDY=h/5  #Max Allowed Diviation for Down Y
                        maxDivUY=int(0-h/47)  #Max Allowed Diviation for Upper Y

                        for cnt in contours:
                            (crx,cry),radius = cv2.minEnclosingCircle(cnt)
                            rad.append(int(radius))
                            contX.append(int(crx))
                            contY.append(int(cry))
                        for i in range(0,len(rad)):
                            if rad[i]>bigRad:
                                bigRad=rad[i]
                                bigRadI=i
                        #RED Dot on pupil
                        if (contY[bigRadI]+y+int(h*.35))-(y+int(h*.5))<maxDivDY and (contY[bigRadI]+y+int(h*.35))-(y+int(h*.5))>maxDivUY:
                            cv2.circle(frameShow,(x+contX[bigRadI],y+int(h*.35)+contY[bigRadI]),5,(0,0,255),-1)
                            pupilX.append(contX[bigRadI])
                            pupilY.append(contY[bigRadI])
                        del rad[:]
                        del contX[:]
                        del contY[:]

            cv2.imshow('frameShow',frameShow)

            k = cv2.waitKey(30) & 0xff
            if k==27:   #esc key
                break
            
        J=detectors.jerking_detection(pupilX)
        bac=predictor.dataAnalysis(J)

        self.add_widget(Label(text="BAC: "+str(bac),size_hint=(.1,.1), pos_hint={'center_x':.5,'center_y':.5}))
        
        cap.release()
        self.capture.release()
        cv2.destroyAllWindows()
                        


class TestCamera(App):

    def build(self):
        return CameraClick()


TestCamera().run()
