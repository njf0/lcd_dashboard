import RPi.GPIO as GPIO
from RPLCD import CharLCD

GPIO.setmode(GPIO.BCM)

GPIO.setup(24, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)

GPIO_PIN_RS = 25
GPIO_PIN_RW = None
GPIO_PIN_E1 = 24
GPIO_PIN_E2 = 10
GPIO_PIN_DB4 = 22
GPIO_PIN_DB5 = 23
GPIO_PIN_DB6 = 27
GPIO_PIN_DB7 = 17
LCD_COLUMNS = 40
LCD_ROWS = 2
LCD_DOT_SIZE = 8
LCD_BRIGHTNESS = 0

lcd_top = CharLCD(pin_rs = GPIO_PIN_RS,
                  pin_rw = GPIO_PIN_RW,
                  pin_e = GPIO_PIN_E1,
                  pins_data = [GPIO_PIN_DB4,
                               GPIO_PIN_DB5,
                               GPIO_PIN_DB6,
                               GPIO_PIN_DB7],
                  numbering_mode = GPIO.BCM,
                  cols = LCD_COLUMNS,
                  rows = LCD_ROWS,
                  dotsize = LCD_DOT_SIZE)

lcd_bot = CharLCD(pin_rs = GPIO_PIN_RS,
                  pin_rw = GPIO_PIN_RW,
                  pin_e = GPIO_PIN_E2,
                  pins_data = [GPIO_PIN_DB4,
                               GPIO_PIN_DB5,
                               GPIO_PIN_DB6,
                               GPIO_PIN_DB7],
                  numbering_mode = GPIO.BCM,
                  cols = LCD_COLUMNS,
                  rows = LCD_ROWS,
                  dotsize = LCD_DOT_SIZE)

GPIO.setwarnings(False)

def print_line(line_num, str):
    
    if line_num == 0 or line_num == 1:
        lcd_top.cursor_pos = (line_num, 0)
        lcd_top.write_string(str)
    elif line_num == 2 or line_num == 3:
        lcd_bot.cursor_pos = (line_num - 2, 0)
        lcd_bot.write_string(str)
