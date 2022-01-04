# This script is running the camera stream and waits for the user input

import picamera
import RPi.GPIO as GPIO
from picamera.array import PiRGBArray
import datetime

import camera.takeImage


# VARIABLES
button_pin = 15

# INIT GPIO PIN
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# INIT CAMERA STREAM
with picamera.PiCamera() as camera:
    camera.resolution = (1920, 1080)
    camera.framerate = 15
    camera.sensor_mode = 2
    camera.rotation = 180
    camera.start_preview()

    rawCapture = PiRGBArray(camera)

    while True:
        camera.start_preview()
        print('camera running. waiting for user input..')

        # LISTEN FOR USERINPUT
        GPIO.wait_for_edge(button_pin, GPIO.RISING)
        filename = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S_mfk-super")

        print('button pressed. exit code..')
        exit()