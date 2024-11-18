import cv2
import numpy as np
from HandTracker import HandDetector 
from image_handle import ImageHandler
import zmq

# Configurations
width, height = 1280, 720
gesturethreshold = 500
min_distance = 50
max_distance = 250
buttondelay = 15

# Initialize
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)
hs, ws = int(120 * 1), int(213 * 1)

# Update the path to the correct location of the presentation folder
image_handler = ImageHandler(r"D:\S07-MINOR PROJECT\Project\backend\presentation", hs, ws)
detector = HandDetector(detectionCon=0.8, maxHands=1)
buttonPressed, buttoncounter = False, 0

# Setup ZMQ context and sockets
context = zmq.Context()
video_socket = context.socket(zmq.PUB)
video_socket.bind("tcp://*:5555")
slide_socket = context.socket(zmq.PUB)
slide_socket.bind("tcp://*:5556")

def calculate_distance(lmList, idx1, idx2):
    x1, y1 = lmList[idx1][0], lmList[idx1][1]
    x2, y2 = lmList[idx2][0], lmList[idx2][1]
    return np.hypot(x2 - x1, y2 - y1)

# Main Loop
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = cv2.resize(img, (1080, 400))
    imgcurrent = image_handler.load_image()
    imgSmall = image_handler.resize_for_overlay(img)
    imgcurrent = image_handler.overlay_image(imgcurrent, imgSmall)
    
    hands, img = detector.findHands(img)
    cv2.line(img, (0, gesturethreshold), (width, gesturethreshold), (0, 255, 0), 10)

    if hands and not buttonPressed:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        lmList = hand['lmList']
        indexFinger = (int(np.interp(lmList[8][0], [width // 2, width], [0, width])),
                       int(np.interp(lmList[8][1], [150, height - 150], [0, height])))

        # Gesture-based Controls
        if fingers == [1, 0, 0, 0, 0]:  # Thumb up
            image_handler.decrement_slide()
            buttonPressed = True
        elif fingers == [0, 0, 0, 0, 1]:  # Pinky up
            image_handler.increment_slide()
            buttonPressed = True
        elif fingers == [0, 1, 0, 0, 0]:  # Index finger up
            image_handler.update_annotations(indexFinger)
        elif fingers == [1, 1, 1, 1, 1]:  # All fingers up
            image_handler.clear_annotations()

        # Zoom Gesture
        if fingers == [1, 1, 0, 0, 0]:
            distance = calculate_distance(lmList, 4, 8)
            if distance < min_distance:
                image_handler.decrement_slide()
                buttonPressed = True
            elif distance > max_distance:
                image_handler.increment_slide()
                buttonPressed = True

    if buttonPressed:
        buttoncounter += 1
        if buttoncounter > buttondelay:
            buttoncounter = 0
            buttonPressed = False

    # Display Slide and Annotations
    imgcurrent = image_handler.draw_annotations(imgcurrent)
    cv2.putText(imgcurrent, f"Slide {image_handler.imgnumber + 1}/{image_handler.get_slide_count()}", 
                (imgcurrent.shape[1] - 150, imgcurrent.shape[0] - 20), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Send video frame and slide frame via ZMQ
    _, video_frame = cv2.imencode('.jpg', img)
    video_socket.send(video_frame.tobytes())
    _, slide_frame = cv2.imencode('.jpg', imgcurrent)
    slide_socket.send(slide_frame.tobytes())

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()