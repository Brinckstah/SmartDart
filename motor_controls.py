from time import sleep
import math
import RPi.GPIO as GPIO


def reloading_servo(servo_3):
    sleep(1)
    for i in range(0,90):
        servo_3.value = math.sin(math.radians(i))
        sleep(0.0001)
    sleep(1)
    servo_3.value = math.sin(math.radians(190))
    sleep(1)



def servo_2_setup(servo_2):
        for i in range(230,200,-1):
                servo_2.value = math.sin(math.radians(i))
                sleep(0.01)
        sleep(0.5)
        for i in range(200,230):
                servo_2.value = math.sin(math.radians(i))
                sleep(0.01)
        sleep(0.5)                

def servo_1_setup(servo_1, dart_quality):

        if(dart_quality == "good"):
            for i in range(0,40):
                servo_1.value = math.sin(math.radians(i))
                sleep(0.01)
            sleep(1)
            for i in range(40,-1,-1):
                servo_1.value = math.sin(math.radians(i))
                sleep(0.01)
        else:
            for i in range(180,230):
                servo_1.value = math.sin(math.radians(i))
                sleep(0.01)
            sleep(1)
            for i in range(230,180,-1):
                servo_1.value = math.sin(math.radians(i))
                sleep(0.01)

def stepper_motor():
    
    control_pins = [2,3,4,14]

    for pin in control_pins:
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin,0)

    halfstep_seq = [
        [1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1]
    ]

    halfstep_seq_reverse = [
        [1,0,0,1],
        [0,0,0,1],
        [0,0,1,1],
        [0,0,1,0],
        [0,1,1,0],
        [0,1,0,0],
        [1,1,0,0],
        [1,0,0,0]
    ]


    while(True):
        for i in range(512):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(control_pins[pin],halfstep_seq[halfstep][pin])
                sleep(0.007)

        for i in range(512):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(control_pins[pin], halfstep_seq_reverse[halfstep][pin])
                sleep(0.007)
