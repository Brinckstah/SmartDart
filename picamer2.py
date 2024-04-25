#!/usr/bin/python3

import cv2

from picamera2 import Picamera2

import os
import re


# Return the next counter value (one more than the highest found)
def find_next_counter(path):
    # List all files in the directory
    files = os.listdir(path)
    max_counter = -1
    for file in files:
        # Match files with the pattern "picture_X.jpg"
        match = re.match(r"picture_(\d+)\.jpg", file)
        if match:
            counter = int(match.group(1))
            if counter > max_counter:
                max_counter = counter
    return max_counter + 1


cv2.startWindowThread()

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (720, 720)}))
picam2.start()

print("Press 'c' to capture an image, 'q' to quit")

# To count amount of pictures
counter = 0

file_path = os.path.join(os.getcwd(), 'Pictures')
counter = find_next_counter(file_path)
print(counter)

while True:
    im = picam2.capture_array()

    cv2.imshow("Camera", im)
    c = cv2.waitKey(1)
    if c & 0xFF == ord('c'):  # If 'c' is pressed, capture image
        img_name = f"picture_{counter}.jpg"
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        path = os.path.join(file_path, img_name)
        cv2.imwrite(path, gray_image)
        counter += 1
    elif c & 0xFF == ord('q'):  # If 'q' is pressed, quit
        break
    
cv2.destroyAllWindows()