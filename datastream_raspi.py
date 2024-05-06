import cv2
from ultralytics import YOLO
import supervision as sv
from picamera2 import Picamera2
from RPLCD.gpio import CharLCD
from RPi import GPIO
from time import sleep
from gpiozero import Servo
from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
import math

GPIO.setmode(GPIO.BOARD)
GPIO.setup(36,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(37,GPIO.IN,pull_up_down=GPIO.PUD_UP)


# Setup and return bounding box and label annotators
def setup_annotators():
    bounding_box_annotator = sv.BoundingBoxAnnotator()
    label_annotator = sv.LabelAnnotator()
    return bounding_box_annotator, label_annotator


 # Process frames for object detection and annotation
def process_frame(frame, model, bounding_box_annotator, label_annotator):
    if frame.shape[2] == 4:
    # Convert from RGBA to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    result = model.predict(frame)[0]
    detections = sv.Detections.from_ultralytics(result)
    print(detections.confidence)

    labels = [model.model.names[class_id] for class_id in detections.class_id]
    
    annotated_frame = bounding_box_annotator.annotate(scene=frame, detections=detections)
    return labels

def servo_2_setup(servo_2):
        for i in range(230,200,-1):
                servo_2.value = math.sin(math.radians(i))
                sleep(0.01)
        sleep(1)
        for i in range(200,230):
                servo_2.value = math.sin(math.radians(i))
                sleep(0.01)

def servo_1_setup(servo_1, dart_quality):

        if(dart_quality == "good"):
            for i in range(0,40):
                servo_1.value = math.sin(math.radians(i))
                sleep(0.01)
            sleep(1)
            for i in range(40,-1,-1):
                servo_1.value = math.sin(math.radians(i))
                sleep(0.01)
        elif(dart_quality == "bad"):
            for i in range(180,230):
                servo_1.value = math.sin(math.radians(i))
                sleep(0.01)
            sleep(1)
            for i in range(230,180,-1):
                servo_1.value = math.sin(math.radians(i))
                sleep(0.01)

def main():
    cv2.startWindowThread()
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (720, 720)}))
    picam2.start()

    model = YOLO(r"/home/thomas/bachelor/SmartDart/runs/detect/train/weights/best.pt")
    model.conf = 0.25  # Set confidence threshold

    bounding_box_annotator, label_annotator = setup_annotators()

    lcd = CharLCD(pin_rs=15,pin_e=16,pins_data[21,22,23,24],numbering_mode=GPIO.BOARD,cols=16,rows=2,charmap="A02")
    lcd.clear()
    lcd_mode = 0
    darts = 0
    lcd.write_string("Press to start")

    factory = PiGPIOFactory()
    servo_1 = Servo(18, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000, pin_factory = factory)
    servo_2 = Servo(12, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000, pin_factory = factory)
    servo_2.value = math.sin(math.radians(230))

    led_1 = LED(5)
    led_2 = LED(6)

    while True:

        if GPIO.input(36) == GPIO.LOW:
            sleep(0.5)
            lcd.clear()
            lcd.cursor_pos = (0,0)
            lcd.write_string("Number of darts")
            lcd_mode += 1
            if lcd_mode > 3:
                lcd_mode = 1
                darts = 12
                lcd.cursor_pos = (1,0)
                lcd.write_string(str(darts) + "   ")
                continue
            if lcd_mode == 1:
                darts = 12
                lcd.cursor_pos = (1,0)
                lcd.write_string(str(darts) + "   ")
            elif lcd_mode == 2:
                darts = 15
                lcd.cursor_pos = (1,0)
                lcd.write_string(str(darts) + "   ")
            elif lcd_mode == 3:
                darts = 18
                lcd.cursor_pos = (1,0)
                lcd.write_string(str(darts) + "   ")
        
        if GPIO.input(37) == GPIO.LOW:
            sleep(0.5)
            lcd.clear()
            lcd.cursor_pos = (0,0)
            lcd.write_string("Processing " + str(darts))
            lcd.cursor_pos = (1,0)
            lcd.write_string("darts")
            good_darts = 0

            while(darts >= good_darts):
                servo_2_setup()

                im = picam2.capture_array()

                processed_labels = process_frame(im, model, bounding_box_annotator, label_annotator)
                
                if all(label == "good-dart" for label in processed_labels):
                    good_darts += 1
                    dart_quality = "good"
                    servo_1_setup(servo_1, dart_quality)
                else:
                    dart_quality = "bad"
                    servo_1_setup(servo_1,dart_quality)
            
            lcd.cursor_pos = (0,0)
            lcd.write_string("Magazine ready")
            lcd.cursor_pos = (1,0)
            lcd.write_string("Press to restart")
            


        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
