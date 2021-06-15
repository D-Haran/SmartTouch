#import necessary modules
import cv2
import time
import numpy as np
import Ratnaharan_Derrick_Resources as cpt
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#######################
#Set Webcam Display box height and width in variables
camWidth = 640
camHeight = 480
#######################

#Grab the webcam
cap = cv2.VideoCapture(0)

#Change webcam height and width with the previously initiated variables
cap.set(3, camWidth)
cap.set(4, camHeight)

#Set a variable for the previous time
previousTime = 0


detector = cpt.handRecog(detectionconfidence=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volumeRange = volume.GetVolumeRange()


minVol = volumeRange[0]
maxVol = volumeRange[1]




while True:
    #Read every frame from the webcam
    success, img = cap.read()

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList[2])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 95), 3)
        cv2.circle(img, (cx, cy), 8, (255, 0, 0), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        print(length)

        # Hand Range 50 - 300
        #Volume Range -63.5 - 0
        vol = np.interp(length, [50, 235], [minVol, maxVol])
        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)
        if length < 25:
            cv2.circle(img, (cx, cy), 8, (255, 0, 255), cv2.FILLED)

    #Set a variable to track the current time
    currentTime = time.time()

    #Use the previously initiated variable to show the fps
    fps = 1/(currentTime - previousTime)
    previousTime = currentTime

    cv2.putText(img, f"FPS: {int(fps)}", (40, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)

