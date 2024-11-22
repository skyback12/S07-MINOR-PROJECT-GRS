import cv2
import time
import numpy as np
from HandTracker import HandDetector
import zmq
from image_upload_handle import get_ppt_images  # Importing the function from image_upload_handle.py

# Configuration
width, height = 1280, 720
ppt_folder = "PPT"
gesturethreshold = 500
buttondelay = 20  # Increased button delay to slow transitions
imgnumber = 0
buttonPressed, buttoncounter = False, 0
annotations = [[]]
annotationnumber, annotationstart = 0, False
min_distance = 30  # Adjust this threshold based on testing
max_distance = 150

# Initialize Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Setup ZMQ context and sockets for video and slide transmission
context = zmq.Context()
video_socket = context.socket(zmq.PUB)
video_socket.bind("tcp://*:5555")  # Bind video frame socket

slide_socket = context.socket(zmq.PUB)
slide_socket.bind("tcp://*:5556")  # Bind slide frame socket

# Load PowerPoint and get slide images
pathimages = get_ppt_images(ppt_folder)
if not pathimages:
    print("No slides to display.")
    exit(1)

# Setup Camera
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Define the function to calculate the Euclidean distance between two landmarks
def calculate_distance(lmList, point1, point2):
    x1, y1, z1 = lmList[point1]
    x2, y2, z2 = lmList[point2]
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)  # 2D distance

while True:
    # Capture and flip the frame
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Resize image for display
    img = cv2.resize(img, (1240, 720))

    # Load and display the current slide image
    imgcurrent = cv2.imread(pathimages[imgnumber])
    if imgcurrent is None:
        print("Error loading slide image.")
        break

    # Add a camera thumbnail
    hs, ws = int(120 * 1), int(213 * 1)
    imgSmall = cv2.resize(img, (ws, hs))
    h, w, _ = imgcurrent.shape
    imgcurrent[0:hs, w - ws:w] = imgSmall

    # Detect hands and process gestures
    hands, img = detector.findHands(img)
    if hands and not buttonPressed:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy = hand['center']
        lmList = hand['lmList']
        xVal = int(np.interp(lmList[8][0], [width // 2, w], [0, width]))
        yVal = int(np.interp(lmList[8][1], [150, height - 150], [0, height]))
        indexFinger = xVal, yVal

        if cy <= gesturethreshold:

            # Previous Slide
            if fingers == [1, 0, 0, 0, 0] and imgnumber > 0:
                print("Left (Previous Slide)")
                buttonPressed = True
                annotations = [[]]
                annotationnumber = 0
                annotationstart = False
                imgnumber -= 1
                time.sleep(0.5)  # Add delay for smoother transition

            # Next Slide
            elif fingers == [0, 0, 0, 0, 1] and imgnumber < len(pathimages) - 1:
                print("Right (Next Slide)")
                buttonPressed = True
                annotations = [[]]
                annotationnumber = 0
                annotationstart = False
                imgnumber += 1
                time.sleep(0.5)  # Add delay for smoother transition

        # Pointer mode
        if fingers == [0, 1, 1, 0, 0]:
            cv2.circle(imgcurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

        # Drawing mode
        if fingers == [0, 1, 0, 0, 0]:
            if not annotationstart:
                annotationstart = True
                annotationnumber += 1
                annotations.append([])
            cv2.circle(imgcurrent, indexFinger, 12, (0, 255, 0), cv2.FILLED)
            annotations[annotationnumber].append(indexFinger)
        else:
            annotationstart = False

        # Clear Screen
        if fingers == [1, 1, 1, 1, 1] and annotations:
            annotations.clear()
            annotationnumber = 0
            annotations = [[]]
            print("Screen Cleared")

        # Undo Last Annotation
        if fingers == [0, 1, 1, 1, 0] and annotationnumber >= 0:
            if annotations:
                annotations.pop(-1)
                annotationnumber -= 1
                buttonPressed = True
                print("Undo Last Annotation")

        # Zoom Gesture
        if fingers == [1, 1, 0, 0, 0]:  # Pinch gesture
            dist = calculate_distance(lmList, 4, 8)  # Distance between thumb (4) and index finger (8)
            if dist < min_distance:
                zoom_factor = 1.2  # Zoom in
            elif dist > max_distance:
                zoom_factor = 0.8  # Zoom out

        # Screenshot
        if fingers == [0, 0, 0, 0, 0]:  # Fist gesture to capture screenshot
            cv2.imwrite(f"screenshot_{imgnumber + 1}.png", imgcurrent)
            print(f"Screenshot of slide {imgnumber + 1} saved.")

    # Draw annotations on the slide
    for i in range(len(annotations)):
        for j in range(1, len(annotations[i])):
            cv2.line(imgcurrent, annotations[i][j - 1], annotations[i][j], (0, 0, 200), 12)

    # Display slide number
    cv2.putText(imgcurrent, f"Slide {imgnumber + 1}/{len(pathimages)}", (w - 150, h - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Encode and send video and slide frames over ZMQ sockets
    _, video_frame = cv2.imencode('.jpg', img)
    video_socket.send(video_frame.tobytes())  # Send video frame

    _, slide_frame = cv2.imencode('.jpg', imgcurrent)
    slide_socket.send(slide_frame.tobytes())  # Send slide frame

    # Display images
    cv2.imshow("Slides", imgcurrent)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

    # Reset button press state
    if buttonPressed:
        buttoncounter += 1
        if buttoncounter >= buttondelay:
            buttonPressed = False
            buttoncounter = 0

cap.release()
cv2.destroyAllWindows()
