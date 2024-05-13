from time import sleep
import math
import RPi.GPIO as GPIO
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory

class motor_controller():
    def __init__(self):
        self.factory = PiGPIOFactory()
        self.servo_1 = Servo(18, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000, pin_factory = self.factory)
        self.servo_2 = Servo(12, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000, pin_factory = self.factory)
        self.servo_3 = Servo(17, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000, pin_factory = self.factory)
        self.servo_1.value = math.sin(math.radians(183))
        self.servo_2.value = math.sin(math.radians(230))
        self.servo_3.value = math.sin(math.radians(190))

        self.control_pins = [2,3,4,14]

        for pin in self.control_pins:
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin,0)

    def reloading_servo(self):
        sleep(1)
        for i in range(0,90):
            self.servo_3.value = math.sin(math.radians(i))
            sleep(0.0001)
        sleep(1)
        self.servo_3.value = math.sin(math.radians(190))
        sleep(1)


    def servo_2_setup(self):
            for i in range(230,200,-1):
                    self.servo_2.value = math.sin(math.radians(i))
                    sleep(0.01)
            sleep(0.5)
            for i in range(200,230):
                    self.servo_2.value = math.sin(math.radians(i))
                    sleep(0.01)
            sleep(0.5)                

    def servo_1_setup(self, dart_quality):

            if(dart_quality == "good"):
                for i in range(-3,40):
                    self.servo_1.value = math.sin(math.radians(i))
                    sleep(0.01)
                sleep(1)
                for i in range(40,-4,-1):
                    self.servo_1.value = math.sin(math.radians(i))
                    sleep(0.01)
            else:
                for i in range(183,230):
                    self.servo_1.value = math.sin(math.radians(i))
                    sleep(0.01)
                sleep(1)
                for i in range(230,182,-1):
                    self.servo_1.value = math.sin(math.radians(i))
                    sleep(0.01)

    def stepper_motor(self):

        halfstep_seq = [
            [1,0,0,0],
            [1,1,0,0],
            [0,1,0,0],
            [0,1,1,0],
            [0,0,1,0],
            [0,0,1,1],
            [0,0,0,1],
            [1,0,0,1],
            [1,0,0,0],
            [1,1,0,0],
            [0,1,0,0]
        ]

        halfstep_seq_reverse = [
            [1,0,0,1],
            [0,0,0,1],
            [0,0,1,1],
            [0,0,1,0],
            [0,1,1,0],
            [0,1,0,0],
            [1,1,0,0],
            [1,0,0,0],
            [1,0,0,1],
            [0,0,0,1],
            [0,0,1,1]
        ]


        while(True):
            for i in range(512):
                for halfstep in range(11):
                    for pin in range(4):
                        GPIO.output(self.control_pins[pin],halfstep_seq[halfstep][pin])
                    sleep(0.007)

            for i in range(512):
                for halfstep in range(11):
                    for pin in range(4):
                        GPIO.output(self.control_pins[pin], halfstep_seq_reverse[halfstep][pin])
                    sleep(0.007)
