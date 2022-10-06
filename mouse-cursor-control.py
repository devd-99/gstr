from imutils import face_utils
from utils import *
import time
import numpy as np
import pyautogui as pag
import imutils
import dlib
import cv2
import win32gui
import win32con
# import threading
# from voice import *

pag.FAILSAFE = False

# t1 = threading.Thread(target = convSpeechToText)
# t1.start()


# Thresholds and consecutive frame length for triggering the mouse action.
MOUTH_AR_THRESH = 0.6
MOUTH_AR_CONSECUTIVE_FRAMES = 15
EYE_AR_THRESH = 0.19
EYE_AR_CONSECUTIVE_FRAMES = 5
WINK_AR_DIFF_THRESH = 0.04
WINK_AR_CLOSE_THRESH = 0.19
WINK_CONSECUTIVE_FRAMES = 10
JOR_LIMIT = 1.35
JOR_FRAMES = 5
BROWRAISE_LIMIT = 0.32
BROWRAISE_FRAMES = 5
SMILE_THRESH = 0.3
SMILE_FRAMES = 0
hwnd = None

# Initialize the frame counters for each action as well as 
# booleans used to indicate if action is performed or not
MOUTH_COUNTER = 0
EYE_COUNTER = 0
WINK_COUNTER = 0
BROW_COUNTER = 0
BLINK_COUNTER = 1
JOR_COUNTER = 0
INPUT_MODE = True
EYE_CLICK = False
LEFT_WINK = False
RIGHT_WINK = False
SCROLL_MODE = False
SET_ANCHOR = False
ON_TOP = False
#Proc flag is for detecting mouth motion
PROC_FLAG = False
#Anchor Flag is for setting anchor point
ANCHOR_FLAG = False
ANCHOR_POINT = (0, 0)
WHITE_COLOR = (255, 255, 255)
YELLOW_COLOR = (0, 255, 255)
RED_COLOR = (0, 0, 255)
GREEN_COLOR = (0, 255, 0)
BLUE_COLOR = (255, 0, 0)
BLACK_COLOR = (0, 0, 0)

# Initialize Dlib's face detector (HOG-based) and then create
# the facial landmark predictor
shape_predictor = "model/shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(shape_predictor)

# Grab the indexes of the facial landmarks for the left and
# right eye, nose and mouth respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(nStart, nEnd) = face_utils.FACIAL_LANDMARKS_IDXS["nose"]
(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

#grab the indexes of the facial lmks for left and right eyebrow and jaw
(lbrowStart, lbrowEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eyebrow"]
(rbrowStart, rbrowEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eyebrow"]
(jawStart, jawEnd) = face_utils.FACIAL_LANDMARKS_IDXS["jaw"]

# Video capture
vid = cv2.VideoCapture(0)
resolution_w = 1920
resolution_h = 1080
cam_w = 640
# cam_w = 1366
cam_h = 480
# cam_h = 480
unit_w = resolution_w / cam_w
unit_h = resolution_h / cam_h

#vars and flags for blinking motion

#marks that process for detecting the 2 blinks has started
method_start = False
#stores the time when the first blink started.
blink1_start = 0.0
#stores time of when first blink ends
blink1_end = 0.0
#stores time when second blink starts
blink2_start = 0.0
#stores time of when second blink ends
# blink2_end = 0.0
current_time = 0.0

# nose_point = [cam_h/2, cam_h/2]
# faceheight = 50
# facewidth = 50
showframe = None

# cv2.namedWindow("MainFrame")

while True:

    # Grab the frame from the threaded video file stream, resize
    # it, and convert it to grayscale
    # channels)
    _, frame = vid.read()
    frame = cv2.flip(frame, 1)
    # frame2  = frame
    # cv2.convertScaleAbs(frame, frame2, 0.6, 50)
    # frame = frame2
    frame = imutils.resize(frame, width=cam_w, height=cam_h)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the grayscale frame
    rects = detector(gray, 0)

    # Loop over the face detections
    if len(rects) > 0:
        rect = rects[len(rects)-1]
        # if not ON_TOP:
        #     if showframe is not None:
        #         window_handle = win32gui.FindWindow(None, "MainFrame")
        #         win32gui.SetWindowPos(window_handle, win32con.HWND_TOPMOST, 860, 0, 150, 200, 0)
    else:
        if showframe is not None:
            # showframe = frame[nose_point[0]-faceheight : nose_point[0]+faceheight, nose_point[1]-facewidth: nose_point[1]+faceheight]
            cv2.imshow("MainFrame", showframe)
            window_handle = win32gui.FindWindow(None, "MainFrame")
            # print("Window Handle is", str(window_handle))
            win32gui.SetWindowPos(window_handle, win32con.HWND_TOPMOST, 860, 0, 150, 200, 0)
        else:
            cv2.imshow("MainFrame", frame)
        # window_handle = win32gui.FindWindow(None, "MainFrame")
        # win32gui.SetWindowPos(window_handle, win32con.HWND_TOPMOST, 860, 0, 300, 300, 0)
        # cv2.namedWindow("MainFrame",cv2.WND_PROP_FULLSCREEN)
        # cv2.setWindowProperty("MainFrame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        key = cv2.waitKey(1) & 0xFF
        continue


    
    # if not ON_TOP:
    #     # hwnd = win32gui.FindWindow("MainFrame", None)
    #     # if hwnd is not None:
    #         # print(hwnd)
    #     window_handle = win32gui.FindWindow(None, "MainFrame")
    #     print("Window Handle is", str(window_handle))
    #     # win32gui.SetWindowPos(window_handle, win32con.HWND_TOPMOST, 860, 0, 200, 150, 0)
    #     ON_TOP = True
    #     # win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 100, 100, 300, 200, 0) 
    


    # Determine the facial landmarks for the face region, then
    # convert the facial landmark (x, y)-coordinates to a NumPy
    # array
    shape = predictor(gray, rect)
    shape = face_utils.shape_to_np(shape)

    # window_handle = win32gui.FindWindow(None, "MainFrame")
    # win32gui.SetWindowPos(window_handle, win32con.HWND_TOPMOST, 860, 0, 300, 300, 0)

    # Extract the left and right eye coordinates, then use the
    # coordinates to compute the eye aspect ratio for both eyes
    mouth = shape[mStart:mEnd]
    leftEye = shape[lStart:lEnd]
    rightEye = shape[rStart:rEnd]
    nose = shape[nStart:nEnd]
    lbrow = shape[lbrowStart:lbrowEnd]
    rbrow = shape[rbrowStart:rbrowEnd]
    jaw = shape[jawStart:jawEnd]

    # Because I flipped the frame, left is right, right is left.
    temp = leftEye
    leftEye = rightEye
    rightEye = temp

    #similar for eyebrows
    temp = lbrow
    lbrow = rbrow
    rbrow = temp

    # Average the mouth aspect ratio together for both eyes
    mar = mouth_aspect_ratio(mouth)
    leftEAR = eye_aspect_ratio(leftEye)
    rightEAR = eye_aspect_ratio(rightEye)
    ear = (leftEAR + rightEAR) / 2.0
    diff_ear = np.abs(leftEAR - rightEAR)
    jor = jaw_open_ratio(lbrow, rbrow, jaw)
    eyeRaise = eyebrowRaise(leftEye, rightEye, lbrow, rbrow, jaw)
    nose_point = (nose[3, 0], nose[3, 1])
    smile = smileRatio(mouth)

    # Compute the convex hull for the left and right eye, then
    # visualize each of the eyes
    # mouthHull = cv2.convexHull(mouth)
    # leftEyeHull = cv2.convexHull(leftEye)
    # rightEyeHull = cv2.convexHull(rightEye)
    # leftBrowHull = cv2.convexHull(lbrow)
    # rightBrowHull = cv2.convexHull(rbrow)
    # cv2.drawContours(frame, [mouthHull], -1, YELLOW_COLOR, 1)
    # cv2.drawContours(frame, [leftEyeHull], -1, YELLOW_COLOR, 1)
    # cv2.drawContours(frame, [rightEyeHull], -1, YELLOW_COLOR, 1)
    # cv2.drawContours(frame, [leftBrowHull], -1, YELLOW_COLOR, 1)
    # cv2.drawContours(frame, [rightBrowHull], -1, YELLOW_COLOR, 1)


    # for (x, y) in np.concatenate((mouth, rightEye, rbrow, leftEye, lbrow), axis=0):
    #     cv2.circle(frame, (x, y), 2, GREEN_COLOR, -1)

    #setting anchor for the first time
    if not SET_ANCHOR:
        ANCHOR_POINT = nose_point
        SET_ANCHOR = not SET_ANCHOR
        if SET_ANCHOR:
            cv2.putText(frame, "Anchor Set", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)

    if(blink1_start!=0):
        if(not isTimeDiffOkay(time.time(), blink1_start)):
            blink1_end=0
            blink1_start=0
            blink2_start=0
    

    # Check whether person in blinking or winking.
    if diff_ear > WINK_AR_DIFF_THRESH:
        print("", end="")
        #find out which eye it is
        # pag.click(button='right')
    else:
        # pag.click(button='left')
        if ear < EYE_AR_THRESH:
            if blink1_start == 0:
                blink1_start = time.time()
                pag.click(button='left')
                # print("blink 1 started. ", blink1_start)
            else:
                if blink1_end !=0:
                    blink2_start = time.time()
                    # print("blink 2 started. ", blink2_start)
                    if(isTimeDiffOkay(blink1_start, blink2_start)):
                        #double click action
                        print("Double Click")
                        pag.click(button='left')
                        # pag.click(button='left')
                    blink1_end=0
                    blink1_start=0
                    blink2_start=0
        else:
           if blink1_start!=0:
              if blink1_end==0:
                    # print("blink 1 ended. ", blink1_end)
                   blink1_end = time.time()

    # check whether the user has opened his mouth through measuring the distance between the eyebrows and the jaw
    if jor > JOR_LIMIT:
        JOR_COUNTER += 1
        if JOR_COUNTER >= JOR_FRAMES:
            if not PROC_FLAG:
                SCROLL_MODE = not SCROLL_MODE
                print("scroll mode turned to ", SCROLL_MODE)
            PROC_FLAG = True
            JOR_COUNTER = 0
    if jor < JOR_LIMIT:
        if PROC_FLAG:
            PROC_FLAG = False


    # check whether the user has raised eyebrows
    if eyeRaise > BROWRAISE_LIMIT:
        BROW_COUNTER += 1
        if BROW_COUNTER>=BROWRAISE_FRAMES:
            ANCHOR_POINT = nose_point
            BROW_COUNTER = 0

    #check whether person is smiling
    # print(smile)
    if smile < SMILE_THRESH:
        SMILE_FRAMES += 1
        # print(SMILE_FRAMES)
        if SMILE_FRAMES > 1:
            print('smile')
            pag.click(button='right')
            SMILE_FRAMES = 0
    else:
        if SMILE_FRAMES != 0:
            SMILE_FRAMES = 0



    if INPUT_MODE:
        cv2.putText(frame, "READING INPUT!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)
        x, y = ANCHOR_POINT
        nx, ny = nose_point
        w, h = 60, 35
        multiple = 1
        # cv2.rectangle(frame, (x - w, y - h), (x + w, y + h), GREEN_COLOR, 2)
        cv2.line(frame, ANCHOR_POINT, nose_point, BLUE_COLOR, 2)


        
        # dir = direction(nose_p   oint, ANCHOR_POINT, w, h)
        if not SCROLL_MODE:
            dir = direction2(nose_point, ANCHOR_POINT, w, h)
            cv2.putText(frame, 'Movement happening', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)
            pag.moveRel(dir[0], dir[1], 0)
        else:
            dir = direction(nose_point, ANCHOR_POINT, w, h)
            cv2.putText(frame, 'Scrolling happening', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)
            if dir=='up':
                pag.scroll(40)
            elif dir=='down':
                pag.scroll(-40)

    # Show the frame
    dims = getDims(jaw, lbrow, rbrow)
    facewidth = int(dims[0]/unit_w)
    faceheight = int(dims[1]/unit_h)

    showframe = frame[nose_point[1]-faceheight : nose_point[1]+faceheight, nose_point[0]-facewidth: nose_point[0]+faceheight]
    tempframe = imutils.resize(showframe, 150, 200)
    showframe = tempframe
    cv2.imshow("MainFrame", showframe)
    key = cv2.waitKey(1) & 0xFF
    # cv2.namedWindow('img_file_name', cv2.WINDOW_NORMAL) # Creates a window
    # os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "python" to true' ''') # To make window active

    # If the `Esc` key was pressed, break from the loop
    if key == 27:
        print("Exiting")
        # t1.kill=True
        break

# Do a bit of cleanup
cv2.destroyAllWindows()
vid.release()
