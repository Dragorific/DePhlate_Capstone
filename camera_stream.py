import cv2

capture = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not capture.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = capture.read()
    frame = cv2.resize(frame, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
    frame = cv2.flip(frame, 1)
    cv2.imshow('Input', frame)

    c = cv2.waitKey(1)
    if c == 27:
        break

capture.release()
cv2.destroyAllWindows()