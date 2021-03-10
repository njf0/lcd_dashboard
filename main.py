# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from RPLCD import CharLCD
import train_update
import weather_update
import bus_update2
import time, sched
import schedule
import data
import sys
import datetime
import display_function

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

def get_date_and_time():
    '''
    Would rather not use global variables but they make things easier
    here, in a relatively low risk environment.
    '''
    global date_str, time_str
    
    dayname = time.strftime("%A, ")
    month = time.strftime("%B ")
    daynum = time.strftime("%d")
    
    j = int(daynum)%10
    k = int(daynum)%100
    if j == 1 and k != 11:
        suffix = 'st'
    elif j == 2 and k != 12:
        suffix = 'nd'
    elif j == 3 and k != 13:
        suffix = 'rd'
    else: suffix = 'th'
    
    time_str = time.strftime("%H:%M")
    date_str = dayname + daynum + suffix + month
    
    datetime_str = date_str + ' ' * (40 - len(date_str) - len(time_str)) + time_str
    
    return datetime_str

def get_weather_update():
    
    global currently, cur_temp, hourly_trimmed_with_padding
    
    cur_temp, summary, rain_chance, wind_speed, _, hourly = weather_update.get_current_conditions()
    temp_cond = str(cur_temp) + chr(223) + 'C, ' + summary + '.'
    rain_wind = '{}% '.format(rain_chance) + '{}mph'.format(wind_speed)
    hourly_trimmed = hourly.split(',')[0]
    if hourly_trimmed[-1] != '.':
        hourly_trimmed += '.'
    hourly_trimmed_with_padding = hourly_trimmed + ' ' * (40 - len(hourly_trimmed))
        
    currently = temp_cond + ' ' * (40 - len(temp_cond) - len(rain_wind)) + rain_wind
        
    return currently

def get_bus_update():
    
    global nextbuses
    
    bus_times = bus_update2.get_buses()
    
    num_buses = len(bus_times)
    if num_buses >= 3:
        prefix = 'Buses to Oxford: '
        bus_str = ', '.join(bus_times[:3]) + '.'
    elif num_buses < 3 and num_buses >= 1:
        prefix = 'Buses to Oxford: '        
        bus_str = ', '.join(bus_times[:num_buses]) + '.'
    elif num_buses == 0:
        prefix = ''
        bus_str = 'No buses in the next 5 hours.'
    
    padding = 40 - len(bus_str) - len(prefix)
    nextbuses = prefix + bus_str + ' ' * padding
    
    return nextbuses

def get_train_update():
    
    global nexttrains
    
    string = train_update.next_trains(data.TUBE_STATION_FROM, data.TUBE_STATION_TO, 3)
    nexttrains = string + ' ' * (40 - len(string))
    
    return nexttrains

def line0_string():
    
    str = date_str + ' ' * (40 - len(date_str) - len(time_str)) + time_str
    
    return str

def line1_string():
    
    str = currently
        
    return str

def line2_string():
    
    str = hourly_trimmed_with_padding
    
    return str

def line3_string():

    str = nextbuses
    
    return str

def update_lcd():
    display_function.print_line(0, line0_string())
    display_function.print_line(1, line1_string())
    display_function.print_line(2, line2_string())
    display_function.print_line(3, line3_string())

if __name__ == '__main__':
    
    display_function.lcd_top.clear()
    display_function.lcd_bot.clear()

    get_date_and_time()
    display_function.print_line(1, '{:^40}'.format('Updating weather...'))
    get_weather_update()
    display_function.print_line(1, '{:^40}'.format('Updating buses...'))
    get_bus_update()
    
    schedule.every().second.do(get_date_and_time)
    schedule.every(2).minutes.do(get_weather_update)
    schedule.every(60).seconds.do(get_bus_update)
    #schedule.every(30).seconds.do(get_train_update)
    
    display_function.lcd_top.clear()
    display_function.lcd_bot.clear()
    
    while(1):
        schedule.run_pending()
        update_lcd()
        time.sleep(1)
