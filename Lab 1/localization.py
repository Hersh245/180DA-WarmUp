"""
Citations

https://docs.opencv.org/4.x/da/d0c/tutorial_bounding_rects_circles.html
https://stackoverflow.com/questions/30331944/finding-red-color-in-image-using-python-opencv
https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
"""


import cv2
import numpy as np

# Start capturing video from the webcam
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the range for red-ish colors
    lower = np.array([0, 50, 50])
    upper = np.array([10, 255, 255])

    # # Convert the frame to RGB color space (OpenCV captures in BGR by default)
    # rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # # Define the range for white-ish colors in RGB
    # lower_yellow = np.array([230, 160, 0])  # Adjust these values as needed
    # upper_yellow = np.array([270, 200, 20])

    # # Create a mask that only includes white-ish colors
    # mask = cv2.inRange(rgb, lower_yellow, upper_yellow)

    # Create a mask that only includes white-ish colors
    mask = cv2.inRange(hsv, lower, upper)

    # Find contours of the white-ish areas
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour and draw a bounding box around it
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the original frame with the bounding box
    cv2.imshow("Frame", frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
