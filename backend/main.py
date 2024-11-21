import cv2
import os
#from cvzone.HandTrackingModule import HandDetector
from HandTracker import HandDetector
import numpy as np
from collections import deque



width,height=1280,720
folderpath="presentation"
# capture
cap=cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)
pathimages=sorted(os.listdir(folderpath),key=len)
print(pathimages)

imgnumber=0
hs,ws=int(120*1),int(213*1)
gesturethreshold=500
buttonPressed=False
buttoncounter=0
buttondelay=15
annotations=[[]]
annotationnumber=0
annotationstart=False
#handdetector
detector=HandDetector(detectionCon=0.8,maxHands=1   )
#history = deque(maxlen=10)

# Function to detect swipe gesture based on hand movement
"""def detect_swipe(centers):
    if len(centers) < 2:
        return None

    x_diff = centers[-1][0] - centers[0][0]

    # Threshold for significant movement
    if abs(x_diff) > 60:  # Adjust threshold for sensitivity
        if x_diff > 0:
            return "Swipe Right"
        else:
            return "Swipe Left"
    return None
"""
def calculate_distance(lmList, idx1, idx2):
    x1, y1 = lmList[idx1][0], lmList[idx1][1]
    x2, y2 = lmList[idx2][0], lmList[idx2][1]
    return np.hypot(x2 - x1, y2 - y1)

min_distance = 50  # Minimum distance between thumb and index for a pinch gesture
max_distance = 250  # Maximum distance for zoom out


while True:
    success,img=cap.read()
    img=cv2.flip(img,1)
    img=cv2.resize(img,(1080,720))
    pathFullImage=os.path.join(folderpath,pathimages[imgnumber])
    imgcurrent=cv2.imread(pathFullImage)


    imgSmall=cv2.resize(img,(ws,hs))
    h,w,_=imgcurrent.shape
    imgcurrent[0:hs,w-ws:w]=imgSmall 
    
    hands,img=detector.findHands(img)
    cv2.line(img,(0,gesturethreshold),(width,gesturethreshold),(0,255,0),10)
    
    # Ensure the screenshot folder exists
    screenshot_folder = "screenshot"
    os.makedirs(screenshot_folder, exist_ok=True)

    if hands and buttonPressed is False:
        hand=hands[0]
        fingers=detector.fingersUp(hand)
        cx,cy=hand['center']
        lmList=hand['lmList']
        xVal=int(np.interp(lmList[8][0],[width//2,w],[0,width]))
        yVal=int(np.interp(lmList[8][1],[150,height-150],[0,height]))
        indexFinger=xVal,yVal


        # Store the center points of the hand for swipe detection
        #history.append((cx, cy))
        
        # Detect swipe gesture based on hand movement
        #swipe_gesture = detect_swipe(history)
        #if swipe_gesture:
        #   print(swipe_gesture)
        #   if swipe_gesture == "Swipe Left" and imgnumber > 0:
        #      buttonPressed = True
        #       annotations = [[]]
        #       annotationnumber = 0
        #       annotationstart = False
        #       imgnumber -= 1
        #   elif swipe_gesture == "Swipe Right" and imgnumber < len(pathimages) - 1:
        #       buttonPressed = True
        #      annotations = [[]]
        #      annotationnumber = 0
        #       annotationstart = False
        #        imgnumber += 1
        

        if cy<=gesturethreshold:

            #previous
            if fingers==[1,0,0,0,0]:
                print("left")                
                if imgnumber>0:
                    buttonPressed=True
                    annotations=[[]]
                    annotationnumber=0
                    annotationstart=False
                    imgnumber-=1

            #next
            if fingers==[0,0,0,0,1]:
                print("right")               
                if imgnumber<len(pathimages)-1:
                    buttonPressed=True
                    annotations=[[]]
                    annotationnumber=0
                    annotationstart=False
                    imgnumber+=1 

        #pointer
        if fingers==[0,1,1,0,0]:
                cv2.circle(imgcurrent,indexFinger,12,(0,0,255),cv2.FILLED)



        #draw
        if fingers==[0,1,0,0,0]:
                if annotationstart is False:
                     annotationstart=True
                     annotationnumber+=1
                     annotations.append([])
                cv2.circle(imgcurrent,indexFinger,12,(0,255,0),cv2.FILLED)
                annotations[annotationnumber].append(indexFinger)

        else: 
             annotationstart=False



        #Clear screen
        if fingers == [1, 1, 1, 1, 1]:
                if annotations:
                    annot_start = False
                    if annotationnumber >= 0:
                        annotations.clear()
                        annotationnumber = 0
                        #gest_done = True 
                        annotations = [[]]
        #undo
        if fingers==[0,1,1,1,0]:
             if annotations:
                  if annotationnumber>=0:
                    annotations.pop(-1)
                    annotationnumber-=1
                    buttonPressed=True

        
        # Display the current slide number on the image
        cv2.putText(imgcurrent, f"Slide {imgnumber + 1}/{len(pathimages)}", (w - 150, h - 20),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        
        #zoom
        if fingers == [1, 1, 0, 0, 0]:  # Pinch gesture
            dist = calculate_distance(lmList, 4, 8)  # Distance between thumb (4) and index finger (8)

            if dist < min_distance:
                zoom_factor = 1.2  # Zoom in
            elif dist > max_distance:
                zoom_factor = 0.8  # Zoom out
            else:
                zoom_factor = 1.0  # No zoom

        

    # Apply zoom to the current image
            imgcurrent = cv2.resize(imgcurrent, None, fx=zoom_factor, fy=zoom_factor)
            print(f"Zoom: {zoom_factor}")

        # Screenshot
        if fingers == [0, 0, 0, 0, 0]:  # Fist gesture to capture screenshot
            screenshot_path = os.path.join(screenshot_folder, f"screenshot_{imgnumber + 1}.png")
            cv2.imwrite(screenshot_path, imgcurrent)
            print(f"Screenshot of slide {imgnumber + 1} saved in {screenshot_folder}.")



        for i in range (len(annotations)):
            for j in range(len(annotations[i])):
                if j!=0:
                    cv2.line(imgcurrent,annotations[i][j-1],annotations[i][j],(0,0,200),12)    

        
    if buttonPressed:
        buttoncounter+=1
        if buttoncounter>buttondelay:
            buttoncounter=0
            buttonPressed=False

    cv2.imshow("Image",img)
    cv2.imshow("Slides",imgcurrent)
    
    key=cv2.waitKey(1)
    if key==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()