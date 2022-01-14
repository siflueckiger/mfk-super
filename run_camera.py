import time
import datetime
from PIL import Image
import picamera
from picamera.array import PiRGBArray
from cprint import *
import cv2




# ---- MODULES ----
import camera.camera as Camera
from modules.button.button import Button
import modules.printer.printer as Printer
import modules.flickr.flickr as Flickr




# ---- SETTINGS ----

DEBUG_WAIT_TIME = 1
WAITING_TIME_CONTDOWN = 0.6
WAITING_TIME_AFTER_IMAGE_CAPTURE = 5

OVERLAY_IMAGE_PATH = 'overlay-images/'
SHARE_IMAGE_FILEPATH = '/home/pi/Documents/mfk-super/mfk-share/'




# ---- FUNCTIONS ----

def wait(seconds):
    time.sleep(seconds)

def CAMERA_REMOVE_OVERLAYS(camera):
    # Remove all overlays from the camera preview
    for o in camera.overlays:
        camera.remove_overlay(o)

def CAMERA_LOAD_OVERLAY(overlayimage):
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

def show_countdown_overlay(countdown_image):
    cprint(countdown_image)
    CAMERA_REMOVE_OVERLAYS(camera)
    CAMERA_LOAD_OVERLAY(OVERLAY_IMAGE_PATH + countdown_image)
    wait(WAITING_TIME_CONTDOWN)

def CAMERA_COUNTDOWN_AND_TAKE_IMAGE():
    show_countdown_overlay('drei.png')
    show_countdown_overlay('zwei.png')
    show_countdown_overlay('eins.png')

    CAMERA_REMOVE_OVERLAYS(camera)

    cprint('!!! CLICK !!!')
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array 
    savepath = SHARE_IMAGE_FILEPATH + filename + ".png"
    cv2.imwrite(savepath, image)
    
    cprint('load after capture image')
    CAMERA_LOAD_OVERLAY(savepath)
    CAMERA_LOAD_OVERLAY(OVERLAY_IMAGE_PATH + 'verarbeitung2.png')
    wait(WAITING_TIME_AFTER_IMAGE_CAPTURE)

    CAMERA_REMOVE_OVERLAYS(camera)




# ---- MAIN ----

if __name__ == '__main__':
    button = Button()
    button.initGpioPin()

    wait(DEBUG_WAIT_TIME)

    cprint.info('---> CONNECTING TO FLICKR API')
    Flickr.connect2API()
    
    wait(DEBUG_WAIT_TIME)
    
    cprint.info('---> INIT CAMERA')
    with picamera.PiCamera() as camera:
        camera.resolution = (1920, 1080)
        camera.framerate = 15
        camera.sensor_mode = 2
        camera.rotation = 0
        camera.start_preview()

        rawCapture = PiRGBArray(camera)

        # START CAMERA STREAM
        while True:
            camera.start_preview()
            cprint.info('---> CAMERA STREAM RUNNING')
            
            # TAKE IMAGE LOOP
            while True:
                CAMERA_REMOVE_OVERLAYS(camera)
                CAMERA_LOAD_OVERLAY(OVERLAY_IMAGE_PATH + 'push.png') 

                # WAIT FOR USER INPUT
                if (button.waitForUserInput() == True):
                    filename = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S_mfk-super")
                    cprint('Button pressed')


                    # FLICKR PLACEHOLDER
                    Flickr.uplpoadPlaceholderImage('placeholder.png')
                    Flickr.getPlaceholderImageURL()


                    # START CAMERA COUNTDOWN
                    CAMERA_COUNTDOWN_AND_TAKE_IMAGE()


                    Printer.generateImage('www.mrt.ch')
                    wait(DEBUG_WAIT_TIME)
                    Printer.printImage('2022-01-04_230054_Super.png')
                    wait(DEBUG_WAIT_TIME)
