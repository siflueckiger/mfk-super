# TODO:
# - after image capture no live preview between capture and display
#       - use open cv for image capture
#

import picamera
import RPi.GPIO as GPIO
from PIL import Image
import time
import datetime
from picamera.array import PiRGBArray
import cv2

# --- SETTINGS ---
button_pin = 15
save_path = 'mfk-share/'
overlay_path = 'overlay-images/'
waiting_time_countdown = 0.6
waiting_time_after_capture = 5

GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def remove_overlays(camera):
    # Remove all overlays from the camera preview
    for o in camera.overlays:
        camera.remove_overlay(o)

def load_overlay_image(overlayimage):
    #remove_overlays(camera)
    # Load the arbitrarily sized image
    img = Image.open(overlayimage).convert("RGBA")
    
    # Create an image padded to the required size with
    # mode 'RGB'
    pad = Image.new('RGBA', (
        ((img.size[0] + 31) // 32) * 32,
        ((img.size[1] + 15) // 16) * 16,
        ))
    
    # Paste the original image into the padded one
    pad.paste(img, (0, 0), img)

    # Add the overlay with the padded image as the source,
    # but the original image's dimensions
    o = camera.add_overlay(pad.tobytes(), size=img.size)

    
    # By default, the overlay is in layer 0, beneath the
    # preview (which defaults to layer 2). Here we make
    # the new overlay semi-transparent, then move it above
    # the preview
    o.alpha = 255
    o.layer = 3



with picamera.PiCamera() as camera:
    camera.resolution = (1920, 1080)
    camera.framerate = 15
    camera.sensor_mode = 2
    camera.rotation = 180
    camera.start_preview()

    rawCapture = PiRGBArray(camera)

    while True:
        camera.start_preview()
        remove_overlays(camera)
        load_overlay_image(overlay_path + 'push.png')

        # wait for user to push button
        GPIO.wait_for_edge(button_pin, GPIO.RISING)
        filename = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S_mfk-super")

        # start countdown
        # 3
        remove_overlays(camera)
        load_overlay_image(overlay_path + 'drei.png')
        time.sleep(waiting_time_countdown)

        # 2
        remove_overlays(camera)
        load_overlay_image(overlay_path + 'zwei.png')
        time.sleep(waiting_time_countdown)

        # 1
        remove_overlays(camera)
        load_overlay_image(overlay_path + 'eins.png')
        time.sleep(waiting_time_countdown)

        remove_overlays(camera)
      
        # save image with open cv 
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array 
        cv2.imwrite("/home/pi/Desktop/mfk-super/super-camera/mfk-share/" + filename + ".png", image)
      
        load_overlay_image("/home/pi/Desktop/mfk-super/super-camera/mfk-share/" + filename + ".png")
        load_overlay_image(overlay_path + 'verarbeitung2.png')
        time.sleep(waiting_time_after_capture)

        remove_overlays(camera)
    
    