import time
import cv2
import lxml.etree as etree
from flickrQr.config import api_secret, api_key
import qrcode

from flickrQr.flickrApi import Flickr
#import xml.etree.ElementTree as ET


print("Take Picture")
camera_port = 0
camera = cv2.VideoCapture(camera_port)
time.sleep(0.1)  # If you don't wait, the image will be dark
return_value, image = camera.read()
cv2.imwrite("./test.png", image)

print("Flicker Authentication")
flickr = Flickr(api_key, api_secret)

id = flickr.upload("./flickrQr/placeholder.png")

print(id)

photoUrl = flickr.getUrl(id)

print(photoUrl)
print("Make QR-Code")

img = qrcode.make(photoUrl)
img.show()

if (input("replace placeholder with processed image?")!=0):
    resp = flickr.replace("./test.png", id)
    print(etree.tostring(resp, encoding='utf8').decode('utf8'))
    print()
    print("Image replaced.")
