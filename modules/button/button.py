#from asyncio.proactor_events import constants
import time
from datetime import datetime
import RPi.GPIO as GPIO
from cprint import *

GPIO_PIN = 15
BUFFERTIME_AFTER_BUTTON_PRESSED = 0.3
counter = 1

class Button:

    def __init__(self):
        self.pin = GPIO_PIN

    def initGpioPin(self):
        cprint.info('---> INIT BUTTON')
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def waitForUserInput(self):
        cprint.warn('Waiting for user to press the button...')
        GPIO.wait_for_edge(self.pin, GPIO.RISING)
        time.sleep(BUFFERTIME_AFTER_BUTTON_PRESSED)
        return True


if __name__ == '__main__':
    button = Button()
    now = datetime.now()
    button.initGpioPin()
    current_time = now.strftime("%H:%M:%S")
    print(current_time, " - Start")

    while True:
        if (button.waitForUserInput() == True):
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(current_time , " - Button pressed: " , counter)
            counter = counter + 1
            time.sleep(1)
