from RPi import GPIO
from time import sleep
from motor_controls import motor_controller
from lcd import lcd_controller
from camera import camera_controller
import threading


def main():
    
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    start_button = GPIO.setup(16,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    confirm_button = GPIO.setup(26,GPIO.IN,pull_up_down=GPIO.PUD_UP)

    camera = camera_controller()
    lcd = lcd_controller
    motors = motor_controller()
    
    lcd.lcd_init()
    stepper_start = 0
    
    while True:

        if start_button == GPIO.LOW:
            sleep(0.5)
            if stepper_start == 0:
                threading.Thread(target=motors.stepper_motor,daemon=True).start()
                stepper_start = 1
            
            darts = lcd.lcd_dart_selection()
            
        
        if confirm_button == GPIO.LOW:
            sleep(0.5)
            lcd.lcd_processing(darts)
            good_darts = 0

            while(darts > good_darts):
                motors.servo_2_setup()

                im = camera.image_capture()
                
                processed_labels = camera.process_frame(im)
                
                if not processed_labels:
                     continue

                if all(label == "good-dart" for label in processed_labels):
                    good_darts += 1
                    dart_quality = "good"
                    motors.servo_1_setup(dart_quality)
                    motors.reloading_servo()

                else:
                    dart_quality = "bad"
                    motors.servo_1_setup(dart_quality)
            
            lcd.lcd_finished()
            
        camera.cv2_cleanup()

if __name__ == "__main__":
    main()
