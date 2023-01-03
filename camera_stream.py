from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import numpy as np
import cv2

capture = cv2.VideoCapture(0)
firstFrame = None

# Check if the webcam is opened correctly
if not capture.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = capture.read()
    frame = cv2.flip(frame, 1)
    text = "Unoccupied"

    c = cv2.waitKey(1)
    if c == 27:
        break

    # resize the frame, convert it to grayscale, and blur it
    frame = cv2.resize(frame, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
	
    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue

    # find the difference between the current frame and the first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    thresh = cv2.dilate(thresh, None, iterations=2)
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    for contour in contours:
        if cv2.contourArea(contour) < 500:
            continue

        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Occupied"

    cv2.putText(frame, "Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), 
                (10, frame.shape[0] - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.35, 
                (0, 0, 255), 
                1)

    cv2.imshow("Tracking Feed", frame)
    cv2.imshow("Threshhold", thresh)
    cv2.imshow("Frame Delta", frameDelta)

capture.release()
cv2.destroyAllWindows()