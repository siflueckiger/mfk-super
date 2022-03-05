import flickrapi
import webbrowser
import os.path
import re
import lxml.etree as etree




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


class Flickr:

    def __init__(self, api_key, api_secret):

        api = flickrapi.FlickrAPI(api_key, api_secret, format="parsed-json")
        if not api.token_valid(perms='write'):

            api.get_request_token(oauth_callback='oob')

            authorize_url = api.auth_url(perms='write')
            webbrowser.open_new_tab(authorize_url)
            print(authorize_url)

            verifier = str(input('Verifier code: '))

            api.get_access_token(verifier)
        self.api = api
    
    def getInfo(self, id):
        resp = self.api.photos.getInfo(photo_id=id)
        print(resp)

    def upload(self, filename):
        fileobj = FileWithCallback(filename, callback)
        resp = self.api.upload("Test", fileobj, format="etree")
        resp=etree.tostring(resp).decode('UTF-8')
        pattern = r'.*?photoid>(.*)<.*'
        match = re.search(pattern, resp)
        id = match.group(1)
        return(id)

    def putPlaceholder(self):
        id = self.upload("./placeholder.png")
        return(id)

    def replace(self, filename, id ):
        fileobj = FileWithCallback(filename, callback)
        resp = self.api.replace(filename, photo_id=id, fileobj=fileobj, format="etree")
        return(resp)

    def getUrl(self, id):
        resp = self.api.photos.getInfo(photo_id = id, format = "etree")

        for urls in resp.iter('urls'):
            for u in urls.iter('url'):    
                photoUrl = u.text
        return(photoUrl)



if __name__ == "__main__":
    import time
    import cv2
    import lxml.etree as etree
    from config import api_secret, api_key
    import qrcode

    #import xml.etree.ElementTree as ET


    print("Take Picture")
    camera_port = 0
    camera = cv2.VideoCapture(camera_port)
    time.sleep(0.1)  # If you don't wait, the image will be dark
    return_value, image = camera.read()
    cv2.imwrite("./test.png", image)

    print("Flicker Authentication")
    flickr = Flickr(api_key, api_secret)
    id = flickr.putPlaceholder()

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

