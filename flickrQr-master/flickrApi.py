import flickrapi
import webbrowser
import os.path
import re
import qrcode 




class FileWithCallback(object):
    def __init__(self, filename, callback):
        self.file = open(filename, 'rb')
        self.callback = callback
        self.len = os.path.getsize(filename)
        self.fileno = self.file.fileno
        self.tell = self.file.tell

    def read(self, size):
        if self.callback:
            self.callback(self.tell() *100 //self.len)
        return self.file.read(size)


def callback(progress):
    print("Uploading {} %".format(progress), end="\r")  


def initFlickr(api_key, api_secret):

    flickr = flickrapi.FlickrAPI(api_key, api_secret, format="parsed-json")
    # Only do this if we don't have a valid token already
    if not flickr.token_valid(perms='write'):

        # Get a request token
        flickr.get_request_token(oauth_callback='oob')

        # Open a browser at the authentication URL. Do this however
        # you want, as long as the user visits that URL.
        authorize_url = flickr.auth_url(perms='write')
        webbrowser.open_new_tab(authorize_url)

        # Get the verifier code from the user. Do this however you
        # want, as long as the user gives the application the code.
        verifier = str(input('Verifier code: '))

        # Trade the request token for an access token
        flickr.get_access_token(verifier)
    return(flickr)

if __name__ == "__main__":
    import time
    import cv2
    import lxml.etree as etree
    from config import api_secret, api_key
    #import xml.etree.ElementTree as ET


    print("Take Picture")
    camera_port = 0
    camera = cv2.VideoCapture(camera_port)
    time.sleep(0.1)  # If you don't wait, the image will be dark
    return_value, image = camera.read()
    cv2.imwrite("./test.png", image)

    print("Flicker Authentication")
    flickr = initFlickr(api_key, api_secret)
    resp = flickr.photos.getInfo(photo_id='7658567128')

    fileobj = FileWithCallback("./placeholder.png", callback)

    resp = flickr.upload("Test", fileobj, format="etree")
    print()

    resp=etree.tostring(resp).decode('UTF-8')
    pattern = r'.*?photoid>(.*)<.*'
    match = re.search(pattern, resp)
    id = match.group(1)

    resp=flickr.photos.getInfo(photo_id = id, format = "etree")


    for urls in resp.iter('urls'):
        for u in urls.iter('url'):    
            photoUrl = u.text
    
    print(photoUrl)
    
    print("Make QR-Code")
    
    img = qrcode.make(photoUrl)
    img.show()

    if (input("replace placeholder with processed image?")!=0):
        fileobj = FileWithCallback("./test.png", callback)
        resp = flickr.replace(filename="./test.png",photo_id=id, fileobj=fileobj, format="etree")
        print()
        print("Image replaced.")
        print(etree.tostring(resp, encoding='utf8').decode('utf8'))

    #print('First set title: %s' % title)
    ##print(etree.tostring(resp, pretty_print = True))

