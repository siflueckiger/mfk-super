# TODO:
# - make better overlay images
# - after image capture no live preview between capture and display 
#

import picamera
import RPi.GPIO as GPIO
from PIL import Image
import time
import datetime

# --- SETTINGS ---
button_pin = 15
save_path = 'mfk-share/'
overlay_path = 'overlay-images/'
waiting_time_countdown = 0.6
waiting_time_after_capture = 2

GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def remove_overlays(camera):
    # Remove all overlays from the camera preview
    for o in camera.overlays:
        camera.remove_overlay(o)

def load_overlay_image(overlayimage):
    #remove_overlays(camera)
    # Load the arbitrarily sized image
    img = Image.open(overlayimage + '.png')
    
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

    while True:
        camera.start_preview()
        remove_overlays(camera)
        load_overlay_image(overlay_path + 'push')

        # wait for user to push button
        GPIO.wait_for_edge(button_pin, GPIO.RISING)
        filename = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S_mfk-super")

        # start countdown
        # 3
        remove_overlays(camera)
        load_overlay_image(overlay_path + 'drei')
        time.sleep(waiting_time_countdown)

        # 2
        remove_overlays(camera)
        load_overlay_image(overlay_path + 'zwei')
        time.sleep(waiting_time_countdown)

        # 1
        remove_overlays(camera)
        load_overlay_image(overlay_path + 'eins')
        time.sleep(waiting_time_countdown)

        remove_overlays(camera)
        load_overlay_image(overlay_path + 'verarbeitung2')
        camera.capture(save_path + filename + '.png')

        load_overlay_image(save_path + filename)
        load_overlay_image(overlay_path + 'verarbeitung2')
        time.sleep(waiting_time_after_capture)

        remove_overlays(camera)
    
    