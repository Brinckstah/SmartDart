import cv2
import os
import re
from picamera2 import Picamera2

def find_next_counter(path):
    files = os.listdir(path)
    max_counter = -1
    for file in files:
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

file_path = os.path.join(os.getcwd(), 'Pictures')
counter = find_next_counter(file_path)

while True:
    im = picam2.capture_array()

    cv2.imshow("Camera", im)
    c = cv2.waitKey(1)
    if c & 0xFF == ord('c'):  # If 'c' is pressed, capture image
        img_name = f"picture_{counter}.jpg"
        path = os.path.join(file_path, img_name)
        cv2.imwrite(path, im)
        counter += 1
    elif c & 0xFF == ord('q'):  # If 'q' is pressed, quit
        break
    
cv2.destroyAllWindows()