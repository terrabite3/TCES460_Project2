#!/usr/bin/python
import pyupm_i2clcd as lcd
import time

myLCD = lcd.Jhd1313m1(0, 0x3E, 0x62)

myLCD.setCursor(0, 0)

myLCD.write("Hello, world!")
myLCD.setCursor(1, 0)
while True:
    time.sleep(1)
