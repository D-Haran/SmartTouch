# File Name: Ratnaharan_Derrick_SmartTouch.py
# Description: Virtually use your device based on AI hand recognition. This program controls the mouse & volume functionality on your 
#              PC without your hand touching the pc (hand captured from the webcam) using an AI computer vision model.
# Name: Derrick Ratnaharan
# Date Created: May 31, 2021
# Date Last Modified: June 05, 2021

#Import essential packages
import cv2
import numpy as np
import Ratnaharan_Derrick_Resources as cpt
import time
import autopy
import math
import tkinter as tk
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#Initiate Tkinter window called "root"
root = tk.Tk()

#How many rows & columns are in the webcam
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

#Window height and width
root.geometry("1000x700")

root.resizable(False, False)

root.title("SmartTouch")

#different frames shown in window
mainM = tk.Frame(root, bg="#f4a261")
vcMM = tk.Frame(root, bg="#f4a261")
mtouchMM = tk.Frame(root, bg="#f4a261")
vol_instruc = tk.Frame(root, bg="#f4a261")
smTouch_instruc = tk.Frame(root, bg="#f4a261")



#Show frame if function is called
def show_frame(frame):
    frame.tkraise()

#Initiate frames
for frame in (mainM, vcMM, mtouchMM, vol_instruc, smTouch_instruc):
    frame.grid(row=0, column=0, sticky='nsew')


def smartTouch():
    ############
    camHeight = 480
    camWidth = 640
    #Get width/height of our screen
    screenWidth, screenHeight = autopy.screen.size()
    # print(screenWidth, screenHeight)

    #from running the screen width and height function, I found out that my computer screen is 1280 by 720
    # ****Might be different on other devices****

    frameReduction = 100 #Frame Reduction


    #Grab the Webcam
    capture = cv2.VideoCapture(0)

    #Change width and height of webcam display window (initiate variables)
    capture.set(3, camWidth)
    capture.set(4, camHeight)

    #Initiate variable "previous time"
    previousTime = 0
    #Initiate variable for the previous location of the mouse as well as the current location
    previouslocX, previouslocY = 0, 0
    currentlocX, currentlocY = 0, 0

    #Detect only one hand for this
    detector = cpt.handRecog(maxHands=1)

    #Show this text when smartTouch window is opened
    close = tk.Label(vcMM, text="To close SmartTouch window, type ctrl + \"C\" in terminal, then close window")
    close.pack()

    while True:
    ###########################################
    ########Steps to finish this program########
    # 1. Find Hand Landmarks/Points
        # Read the frame from the Webcam
        success, img = capture.read()

        #Use the find hands function in the resource file and use it to detect the hands in the webcam
        img = detector.findHands(img)

        #Find hands in the webcam frame
        lmList = detector.findPosition(img)
        #print(lmList)
    #2.Get the tip of the index and the middle finger
        if len(lmList) != 0:
            #For index finger
            x1, y1 = lmList[8][1:]
            #for middle finger
            x2, y2 = lmList[12][1:]

    #3. Check which fingers are up
            fingers = detector.fingersUp()
            # print(fingers)
            cv2.rectangle(img, (frameReduction, frameReduction), (camWidth - frameReduction, camHeight - frameReduction),
                        (255, 0, 255), 2)
    #4. If only Index finger is up: Moving Mouse mode
            # If index finger is up and middle finger is down
            if fingers[1] == 1 and fingers[2] == 0:
            #5. Convert Coordinates
                x3 = np.interp(x1, (frameReduction, camWidth - frameReduction), (0, screenWidth))
                y3 = np.interp(y1, (frameReduction, camHeight - frameReduction), (0, screenHeight))

            #6. Move mouse
                autopy.mouse.move(screenWidth - x3, y3)
                cv2.circle(img, (x1, y1), 15, (255, 0, 95), cv2.FILLED)
                previouslocX, previouslocY = currentlocX, currentlocY
    #7. If both index and middle finger is up, then it is in clicking mode
            if fingers[1] == 1 and fingers[2] == 1:
                length, img, lineInfo = detector.findDistance(8, 12, img)
                print(length)

            if len(lmList) != 0:
                # print(lmList[2])

                x1, y1 = lmList[8][1], lmList[8][2]
                x2, y2 = lmList[12][1], lmList[12][2]
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, (x2, y2), 15, (255, 0, 0), cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 95), 3)
                cv2.circle(img, (cx, cy), 8, (255, 0, 0), cv2.FILLED)

                length = math.hypot(x2 - x1, y2 - y1)
                print(length)
                # 8. Find distance between fingers
                if length < 40:
                    #9. Click Mouse if distance is short
                    cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                    autopy.mouse.click()




    #10. Print Frame rate on top left side of screen
        currentTime = time.time()
        fps = 1/(currentTime - previousTime)
        previousTime = currentTime

        #Print text on the window
        cv2.putText(#Put text in the main window
                    img,
                    #Text
                    f"FPS:{int(fps)}",
                    #Where on the screen
                    (20, 50),
                    #What Font
                    cv2.FONT_HERSHEY_PLAIN,
                    #Scale of text
                    3,
                    #Colour of Text
                    (255, 0, 255),
                    #Thickness of Text
                    3)
    #11. Display
        #Show the captured frame
        cv2.imshow("Image", img)
        # Without this, only one frame would show, however, the line of code below refreshes that and shows the current
        # frame every 1 millisecond
        cv2.waitKey(1)

def volcntrl():
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

    #Detect hands only if the model has a 0.7 confidence
    detector = cpt.handRecog(detectionconfidence=0.7)

    #Initiate Variable
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volumeRange = volume.GetVolumeRange()

    #Max & Min vol ranges
    minVol = volumeRange[0]
    maxVol = volumeRange[1]

    close = tk.Label(vcMM, text="To close SmartTouch window, type ctrl + \"C\" in terminal, then close window")
    close.pack()

    while True:
        #Read every frame from the webcam
        success, img = cap.read()

        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        if len(lmList) != 0:
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

        #Show FPS
        cv2.putText(img, f"FPS: {int(fps)}", (40, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
        cv2.imshow("Img", img)
        cv2.waitKey(1)
        




################ Main Menu Frame
welcome = tk.Label(mainM, text="Welcome to the Main Menu", pady= 40, font=6, bg="#f4a261", fg="#264653")

smartTouchbutton = tk.Button(mainM, text="SmartTouch", command=lambda: show_frame(mtouchMM), width=20, pady=20, border=7, bg="#2a9d8f", fg="#e9c46a")
volcntrlbutton = tk.Button(mainM, text="Volume Control", command=lambda: show_frame(vcMM), width=20, pady=20, border=7, bg="#e76f51", fg="#2a9d8f")
madeBy = tk.Label(mainM, text="Made By Derrick Ratnaharan using OpenCv & Tkinter in Python3", pady= 40, font=6, bg="#f4a261", fg="#264653")

welcome.place(relx=0.41, rely=0.1)
smartTouchbutton.place(relx=0.45, rely=0.3)
volcntrlbutton.place(relx=0.45, rely=0.5)
madeBy.place(relx=0.245, rely=0.69)

show_frame(mainM)

################## Volume Control Main Frame
vcContrMM = tk.Label(vcMM, text="VolCntrl", pady= 40, padx=70, font=6, bg="#f4a261", fg="#264653")
volumeinstrucbutton = tk.Button(vcMM, text="INSTRUCTIONS", width=27, pady=40, border=6, command=lambda: show_frame(vol_instruc), bg="#2a9d8f", fg="#e9c46a")
volumestart = tk.Button(vcMM, text="START PROGRAM", width=27, pady=40, border=6, command=lambda: volcntrl(), bg="#2a9d8f", fg="#e9c46a")
back = tk.Button(vcMM, text="Back", width=17, pady=20, border=6, command=lambda: show_frame(mainM), bg="#e76f51", fg="#e9c46a")
vcContrMM.place(relx=0.44, rely=0.1)
volumeinstrucbutton.place(relx=0.45, rely=0.3)
volumestart.place(relx=0.45, rely=0.5)
back.place(relx=0.49, rely=0.7)


################## SmartTouch Main Frame
smtouchlabel = tk.Label(mtouchMM, text="SmartTouch", pady= 40,font=6, bg="#f4a261", fg="#264653")
mtouch_instruc = tk.Button(mtouchMM, text="INSTRUCTIONS", width=27, pady=40, border=6, bg="#2a9d8f", fg="#e9c46a", command=lambda: show_frame(smTouch_instruc))
mtouch_start = tk.Button(mtouchMM, text="START PROGRAM", width=27, pady=40, border=6, bg="#2a9d8f", fg="#e9c46a", command=lambda: smartTouch())
back = tk.Button(mtouchMM, text="Back", width=17, pady=20, border=6, command=lambda: show_frame(mainM), bg="#e76f51", fg="#2a9d8f")
smtouchlabel.place(relx=0.49, rely=0.1)
mtouch_instruc.place(relx=0.45, rely=0.35)
mtouch_start.place(relx=0.45, rely=0.55)
back.place(relx=0.49, rely=0.75)

################### VolumeCntrl Instructions Frame
vol_instruc_Label = tk.Label(vol_instruc, text="VolCntrl Instructions", pady= 40,font=6, bg="#f4a261", fg="#264653")
volcntrl_instruc = tk.Label(vol_instruc, text="1. Keep your fist within the camera frame \n2. Volume Changes according to the distance between your finger and thumb", font=3, bg="#f4a261")
back = tk.Button(vol_instruc, text="Back", width=17, pady=20, border=6, command=lambda: show_frame(vcMM), bg="#2a9d8f", fg="#e9c46a")
vol_instruc_Label.place(relx=0.463, rely=0.1)
volcntrl_instruc.place(relx=0.2, rely=0.3)
back.place(relx=0.49, rely=0.5)

################### SmartTouch Instructions Frame
vol_instruc_Label = tk.Label(smTouch_instruc, text="SmartTouch Instructions", pady= 40,font=6, bg="#f4a261", fg="#264653")
volcntrl_instruc = tk.Label(smTouch_instruc, text="1. Keep your fist within the webcam frame\n2. If index finger is held up, mouse moving mode is on\n3. If both index & middle fingers are held up, clicking mode is on.", font=3, bg="#f4a261")
back = tk.Button(smTouch_instruc, text="Back", width=17, pady=20, border=6, command=lambda: show_frame(vcMM), bg="#2a9d8f", fg="#e9c46a")
vol_instruc_Label.place(relx=0.463, rely=0.1)
volcntrl_instruc.place(relx=0.2, rely=0.3)
back.place(relx=0.49, rely=0.5)

root.mainloop()
