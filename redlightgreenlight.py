#!/usr/bin/python
import RPi.GPIO as GPIO
import time
from datetime import datetime


last_isempty = True
last_distance = []
print("time,cm")
while True:
    try:
        GPIO.setmode(GPIO.BOARD)

        PIN_TRIGGER = 7
        PIN_ECHO = 11

        GPIO.setup(PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(PIN_ECHO, GPIO.IN)

        GPIO.output(PIN_TRIGGER, GPIO.LOW)

        current_time = datetime.now()

        GPIO.output(PIN_TRIGGER, GPIO.HIGH)

        time.sleep(0.00001)

        GPIO.output(PIN_TRIGGER, GPIO.LOW)

        while GPIO.input(PIN_ECHO)==0:
                pulse_start_time = time.time()
        while GPIO.input(PIN_ECHO)==1:
                pulse_end_time = time.time()

        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17150, 2)
        # Print time and distance in centimeters
        dt = current_time.strftime("%H:%M:%S")
        print (f"{dt},{distance}")
        if last_isempty == True:
         last_distance.append(str(distance))
         last_distance = (last_distance[0].replace("[" and "]",""))
         last_distance = (last_distance[0].replace("'" and "'", ""))
         last_distance = float(last_distance)
         last_isempty = False
        else:
         pass
        print (last_distance)
        movement_threshold = 1
        current_distance = distance
        delta_distance = abs(current_distance - last_distance)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(32, GPIO.OUT)
        GPIO.setup(33, GPIO.OUT)
        GPIO.output(33,GPIO.HIGH)
        if delta_distance > movement_threshold:
          GPIO.output(32,GPIO.HIGH)
          GPIO.output(33,GPIO.LOW)
        else:
          GPIO.output(32, GPIO.LOW)
          GPIO.output(33, GPIO.HIGH)
        last_distance = current_distance
        time.sleep(1)
    finally:
        GPIO.cleanup()
