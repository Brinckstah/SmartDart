from RPLCD.gpio import CharLCD
from RPi import GPIO
from gpiozero import LED

class lcd_controller:
    def __init__(self):
        self.lcd = CharLCD(pin_rs=22, pin_e=23,pins_data=[9,25,11,8],numbering_mode=GPIO.BCM,cols=16,rows=2,charmap="A02")
        self.lcd_mode = 0
        self.led_1 = LED(5)
        self.led_2 = LED(6)

    def lcd_init(self):
        self.lcd.clear()
        self.lcd.write_string("Press to start")

    def lcd_dart_selection(self):
        self.lcd.clear()
        self.lcd.cursor_pos = (0,0)
        self.lcd.write_string("Number of darts")
        self.lcd_mode += 1
        darts = 0
        if self.lcd_mode > 3:
            self.lcd_mode = 1
            darts = 3
            self.lcd.cursor_pos = (1,0)
            self.lcd.write_string(str(darts))
            return darts
        if self.lcd_mode == 1:
            darts = 3
            self.lcd.cursor_pos = (1,0)
            self.lcd.write_string(str(darts))
            return darts
        elif self.lcd_mode == 2:
            darts = 5
            self.lcd.cursor_pos = (1,0)
            self.lcd.write_string(str(darts))
            return darts
        elif self.lcd_mode == 3:
            darts = 8
            self.lcd.cursor_pos = (1,0)
            self.lcd.write_string(str(darts))
            return darts

    def lcd_processing(self, darts):
        self.led_1.on()
        self.led_2.on()
        self.lcd.clear()
        self.lcd.cursor_pos = (0,0)
        self.lcd.write_string("Processing " + str(darts))
        self.lcd.cursor_pos = (1,0)
        self.lcd.write_string("darts")

    def lcd_finished(self):
        self.led_1.off()
        self.led_2.off()
        self.lcd.clear()
        self.lcd.cursor_pos = (0,0)
        self.lcd.write_string("Magazine ready")
        self.lcd.cursor_pos = (1,0)
        self.lcd.write_string("Press to restart")