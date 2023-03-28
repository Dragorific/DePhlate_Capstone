import argparse
import datetime
import imutils
import time
import numpy as np
import cv2
#from clarifai import clarifaiFood
from nutrition import get_food_info
from serial_sensor import get_measurement

capture = cv2.VideoCapture(0)
firstFrame = None
text = "Unoccupied"
tableText = ""
oldX = 0
oldY = 0

# Check if the webcam is opened correctly
if not capture.isOpened():
    raise IOError("Cannot open webcam")

while True:
    counter = 0
    ret, frame = capture.read()
    frame = cv2.flip(frame, 1)

    if cv2.waitKey(67) == 27:
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
        if cv2.contourArea(contour) < 2000:
            continue

        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        if(oldX == x and oldY == y):
            foodImg = frame[y:y+h, x:x+w]
            cv2.imwrite("foodCutOut.jpg", foodImg)
            with open('foodCutOut.jpg', 'rb') as file:
                image_data = file.read()
                image_bytes = bytes(image_data)
            
            # prediction, rating = clarifaiFood(image_bytes)
            prediction = "chocolate"
            rating = "0.54"
            calories, serving_size = get_food_info(prediction.upper())
            weight = get_measurement()
            calories = str(calories*(weight/serving_size))
            text = prediction + ", confidence: " + rating + ", calories: " + calories
            tableText += str(weight) + "g of " + prediction + ", calories: " + calories + "\n"
            firstFrame = gray
        else:
            oldX = x
            oldY = y
        

    cv2.putText(frame, "Output: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), 
                (10, frame.shape[0] - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.35, 
                (0, 0, 255), 
                1)
    for text in tableText.split("\n"):
        cv2.putText(frame, text, 
                    (400, frame.shape[0] - (100 - 15*counter)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.35, 
                    (0, 0, 255), 
                    1)
        
        counter += 1

    cv2.imshow("Tracking Feed", frame)
    cv2.imshow("Threshhold", thresh)
    cv2.imshow("Frame Delta", frameDelta)

capture.release()
cv2.destroyAllWindows()