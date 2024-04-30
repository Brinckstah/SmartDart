import cv2
import os
import re
from picamera2 import Picamera2
from gpiozero import Servo
from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import math
import threading

led_1 = LED(5)
led_2 = LED(6)

class servo_controller():
    def __init__(self):
        self.factory = PiGPIOFactory()
        self.servo_1 = Servo(18, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000, pin_factory = self.factory)
        self.servo_2 = Servo(12, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000, pin_factory = self.factory)
    
    def servo_1_setup(self):
        dart = int(input("Press 1 for good dart and 2 for bad dart\n"))

        if(dart == 1):
            for i in range(0,40):
                self.servo_1.value = math.sin(math.radians(i))
                sleep(0.01)
            sleep(1)
            for i in range(40,-1,-1):
                self.servo_1.value = math.sin(math.radians(i))
                sleep(0.01)
        elif(dart == 2):
            for i in range(180,230):
                self.servo_1.value = math.sin(math.radians(i))
                sleep(0.01)
            sleep(1)
            for i in range(230,180,-1):
                self.servo_1.value = math.sin(math.radians(i))
                sleep(0.01)

    def servo_2_setup(self):
        self.servo_2.value = math.sin(math.radians(230))
        sleep(3)
        for i in range(230,200,-1):
                self.servo_2.value = math.sin(math.radians(i))
                sleep(0.01)
        sleep(2)
        for i in range(200,230):
                self.servo_2.value = math.sin(math.radians(i))
                sleep(0.01)

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

def control_servos():
    controller = servo_controller()
    while True:
        controller.servo_2_setup()
        controller.servo_1_setup()


cv2.startWindowThread()
threading.Thread(target=control_servos, daemon=True).start()

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (720, 720)}))
picam2.start()

print("Press 'c' to capture an image, 'q' to quit")

file_path = os.path.join(os.getcwd(), 'Pictures')
counter = find_next_counter(file_path)

controller = servo_controller()

while True:
    led_1.on()
    led_2.on()
    
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