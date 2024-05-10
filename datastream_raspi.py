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
from motor_controls import reloading_servo, servo_1_setup, servo_2_setup, stepper_motor
from lcd import lcd_init, lcd_dart_selection, lcd_processing, lcd_finished
import threading
import math


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


def main():
    cv2.startWindowThread()
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (720, 720)}))
    picam2.start()

    model = YOLO(r"/home/filip/bachelor/SmartDart/runs/detect/train/weights/best.pt")
    model.conf = 0.25  # Set confidence threshold

    bounding_box_annotator, label_annotator = setup_annotators()

    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(26,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    led_1 = LED(5)
    led_2 = LED(6)

    lcd = CharLCD(pin_rs=22, pin_e=23,pins_data=[9,25,11,8],numbering_mode=GPIO.BCM,cols=16,rows=2,charmap="A02")
    lcd_mode = 0
    lcd_init(lcd)


    factory = PiGPIOFactory()
    servo_1 = Servo(18, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000, pin_factory = factory)
    servo_2 = Servo(12, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000, pin_factory = factory)
    servo_3 = Servo(17, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000, pin_factory = factory)
    servo_2.value = math.sin(math.radians(230))
    servo_3.value = math.sin(math.radians(0))


    threading.Thread(target=stepper_motor,daemon=True).start()
    while True:

        if GPIO.input(16) == GPIO.LOW:
            sleep(0.5)
            darts, lcd_mode = lcd_dart_selection(lcd,lcd_mode)
            
        
        if GPIO.input(26) == GPIO.LOW:
            sleep(0.5)
            lcd_processing(lcd, darts)
            good_darts = 0

            led_1.on()
            led_2.on()

            while(darts > good_darts):
                servo_2_setup(servo_2)

                im = picam2.capture_array()
                
                processed_labels = process_frame(im, model, bounding_box_annotator, label_annotator)
                
                if not processed_labels:
                     continue

                if all(label == "good-dart" for label in processed_labels):
                    good_darts += 1
                    dart_quality = "good"
                    servo_1_setup(servo_1, dart_quality)
                    reloading_servo(servo_3)

                else:
                    dart_quality = "bad"
                    servo_1_setup(servo_1,dart_quality)
            
            led_1.off()
            led_2.off()
            
            lcd_finished(lcd)
            
            


        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
