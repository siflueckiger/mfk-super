from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import datetime


img_width  = 1920
img_height = 1080

# setup the camera
camera = PiCamera()
camera.resolution = (img_width, img_height)
camera.framerate = 30
camera.rotation = 180

# setup array for opencv
rawCapture_stream = PiRGBArray(camera, size=(img_width, img_height))
cv2.namedWindow("MfK-Super", cv2.WINDOW_FREERATIO)
cv2.setWindowProperty("MfK-Super", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

time.sleep(0.1)

# start preview
for frame in camera.capture_continuous(rawCapture_stream, format="bgr", use_video_port=True):
    image = frame.array 
    
    cv2.imshow("MfK-Super", image)
    key = cv2.waitKey(1) & 0xFF

    rawCapture_stream.truncate(0)

    if key == ord("q"):
        break

    if key == ord("c"):
        filename = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S_mfk-super")
        cv2.imwrite("/home/pi/Desktop/mfk-super/super-camera/mfk-share/" + filename + ".png", image)