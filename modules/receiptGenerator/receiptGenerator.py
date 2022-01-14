# TODO:
# Zeit in Filname und auf Quittung die selbe

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from escpos.printer import Usb
import argparse
import qrcode
import pyshorteners

# init url shortener
shortener = pyshorteners.Shortener()

# init printer
printer = Usb(0x04b8,0x0e28,0)

parser = argparse.ArgumentParser(description='Print a receipt with a qr code to image for mfk-super')
parser.add_argument('-qr', '--qr_string', type=str, metavar="", required=True, help='String for QR-Code')
args = parser.parse_args()

# generate image
COLOR_MODE = 'RGB'
W, H = (550, 800)
BG_COLOR = 'white'
COLOR = 'black'
img = Image.new(COLOR_MODE, (W, H), BG_COLOR)

# fonts
h1 = ImageFont.truetype('font/Source_Code_Pro/SourceCodePro-Medium.ttf', 50)
h2 = ImageFont.truetype('font/Source_Code_Pro/SourceCodePro-Italic.ttf', 30)
p = ImageFont.truetype('font/Source_Code_Pro/SourceCodePro-SemiBold.ttf', 25)
footer = ImageFont.truetype('font/Source_Code_Pro/SourceCodePro-Regular.ttf', 25)

def addText(text, posY, myFont, color):
    w, h = draw.textsize(text, font=myFont)
    draw.text(((W-w)/2, posY), text, fill=color, font=myFont)

def generateQRCode(link):
    qr = qrcode.QRCode()
    qr.add_data(link)
    qr.make()
    global qr_img
    qr_img = qr.make_image(fill_color="black", back_color="white")
    print(qr_img.size)

# add content
draw = ImageDraw.Draw(img)

# header
addText('MfK-Super-KI-Foto', 30, h1, 'black')
addText('by Magic Ramba Trash', 85, h2, 'black')

# main content
# generate qr-code
# link = 'https://giphy.com/gifs/reactionseditor-yes-awesome-3ohzdIuqJoo8QdKlnW/fullscreen'
link = args.qr_string
generateQRCode(link)

# paste qr-code
xPos = int((W - 450) / 2)
img.paste(qr_img, (xPos, 195))

# add short url (qr-code-link)
print('original url: ' + link)
short_link = shortener.tinyurl.short(link)
print('short url: ' + short_link)
addText(short_link, 620, footer, 'black')

addText('DEIN BILD | TA PHOTO | YOUR PICTURE', 150, p, 'black')
date = datetime.today().strftime('%d.%m.%Y - %H:%M:%S')
addText(date, 180, p, 'black')

# footer
addText('www.mfk.ch', 730, footer, 'black')
addText('www.magicrambatrash.ch', 760, footer, 'black')

# save image
date = datetime.today().strftime('%Y-%m-%d_%H%M%S')
filename = date + '_MfK-Super-Foto.png'
img.save(filename)
print('Filename: ' + filename)

# print image
printer.image(filename, impl='graphics')
printer.cut()
print('File %s printed.' % filename)
