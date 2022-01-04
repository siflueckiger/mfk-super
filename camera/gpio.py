import RPi.GPIO as GPIO
import time

button_pressed = False
button_pin = 15

GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def action1(self):
    global button_pressed
    button_pressed = True

GPIO.add_event_detect(button_pin, GPIO.RISING, callback=action1,bouncetime=300)

    
while True:
    while button_pressed == False:
        print('wait for input')
        time.sleep(1)
    
    print('button pressed')
    time.sleep(1)
    print('taking picture')
    time.sleep(1)
    print('save image')
    time.sleep(1)
    button_pressed = False
