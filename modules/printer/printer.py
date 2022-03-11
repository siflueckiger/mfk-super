from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from escpos.printer import Usb
import argparse
import qrcode
import pyshorteners




def generateQRCode(link):
    qr = qrcode.QRCode(box_size=10, version=1)
    qr.add_data(link)
    qr.make()
    global qr_img
    qr_img = qr.make_image(fill_color="black", back_color="white")


class receiptPrinter:
    def __init__(self):
        self.shortener = pyshorteners.Shortener()
        self.printer = Usb(0x04b8,0x0e28,0)
        self.W = 550
        self.H = 700
        self.initImage()
    
    def initImage(self):
        COLOR_MODE = 'RGB'
        BG_COLOR = 'white'
        COLOR = 'black'
        self.img  = Image.new(COLOR_MODE, (self.W, self.H), BG_COLOR)
        self.draw = ImageDraw.Draw(self.img)

    def drawTextToImage(self, text, posY, myFont, color):
        w, h = self.draw.textsize(text, font=myFont)
        self.draw.text(((self.W-w)/2, posY), text, fill=color, font=myFont)

    def print(self, url):
        # fonts
        h1 = ImageFont.truetype('/home/pi/Documents/mfk-super/modules/printer/font/Source_Code_Pro/SourceCodePro-Medium.ttf', 50)
        h2 = ImageFont.truetype('/home/pi/Documents/mfk-super/modules/printer/font/Source_Code_Pro/SourceCodePro-SemiBold.ttf', 25)
        p = ImageFont.truetype('/home/pi/Documents/mfk-super/modules/printer/font/Source_Code_Pro/SourceCodePro-SemiBold.ttf', 25)
        footer = ImageFont.truetype('/home/pi/Documents/mfk-super/modules/printer/font/Source_Code_Pro/SourceCodePro-Regular.ttf', 23)

        # header
        self.drawTextToImage('MfK-Super-KI-Foto', 15, h1, 'black')
        self.drawTextToImage('by Magic Ramba Trash', 75, h2, 'black')

        # main content
        # generate qr-code
        # link = 'https://giphy.com/gifs/reactionseditor-yes-awesome-3ohzdIuqJoo8QdKlnW/fullscreen'
        link = url
        generateQRCode(link)

        # paste qr-code
        xPos = 95
        self.img.paste(qr_img, (xPos, 195))

        self.drawTextToImage(url, 550, footer, 'black')

        self.drawTextToImage('DEIN BILD | TA PHOTO | YOUR PICTURE', 150, p, 'black')
        date = datetime.today().strftime('%d.%m.%Y - %H:%M:%S')
        self.drawTextToImage(date, 180, p, 'black')

        # footer
        self.drawTextToImage('www.mfk.ch', 610, footer, 'black')
        self.drawTextToImage('www.magicrambatrash.ch', 640, footer, 'black')
        self.drawTextToImage('follow us on instagram: magicrambatrash', 670, footer, 'black')

        # save image
        date = datetime.today().strftime('%Y-%m-%d_%H%M%S')
        filename = '/home/pi/Documents/mfk-super/QR-Codes/' + date + '_MfK-Super-Foto.png'
        
        self.img.save(filename)

        # print image
        self.printer.image(filename, impl='graphics')
        self.printer.cut()
        print('File %s printed.' % filename)



if __name__ == "__main__":
    printer = receiptPrinter()
    printer.print('https://tinyurl.com/y8vqzxap')