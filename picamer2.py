#!/usr/bin/python3

import cv2

from picamera2 import Picamera2
cv2.startWindowThread()

picam2 = Picamera2()
preview_config = picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
preview_config["main"]["roi"] = (0.0, 0.0, 1.0, 1.0)
picam2.configure(preview_config)
picam2.start()

while True:
    im = picam2.capture_array()

    cv2.imshow("Camera", im)
    cv2.waitKey(1)