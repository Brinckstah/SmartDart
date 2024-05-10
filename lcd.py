

def lcd_init(lcd):
    lcd.clear()
    lcd.write_string("Press to start")

def lcd_dart_selection(lcd, lcd_mode):
    lcd.clear()
    lcd.cursor_pos = (0,0)
    lcd.write_string("Number of darts")
    lcd_mode += 1
    darts = 0
    if lcd_mode > 3:
        lcd_mode = 1
        darts = 3
        lcd.cursor_pos = (1,0)
        lcd.write_string(str(darts))
        return darts, lcd_mode
    if lcd_mode == 1:
        darts = 3
        lcd.cursor_pos = (1,0)
        lcd.write_string(str(darts))
        return darts, lcd_mode
    elif lcd_mode == 2:
        darts = 5
        lcd.cursor_pos = (1,0)
        lcd.write_string(str(darts))
        return darts, lcd_mode
    elif lcd_mode == 3:
        darts = 8
        lcd.cursor_pos = (1,0)
        lcd.write_string(str(darts))
        return darts, lcd_mode

def lcd_processing(lcd, darts):
    lcd.clear()
    lcd.cursor_pos = (0,0)
    lcd.write_string("Processing " + str(darts))
    lcd.cursor_pos = (1,0)
    lcd.write_string("darts")

def lcd_finished(lcd):
    lcd.clear()
    lcd.cursor_pos = (0,0)
    lcd.write_string("Magazine ready")
    lcd.cursor_pos = (1,0)
    lcd.write_string("Press to restart")