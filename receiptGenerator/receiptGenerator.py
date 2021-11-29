from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import argparse
import qrcode
import pyshorteners

s = pyshorteners.Shortener()

parser = argparse.ArgumentParser(description='Generate an image from a phrase using VQGAN')
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


# add content
draw = ImageDraw.Draw(img)
# header
addText('MfK-Super-KI-Foto', 30, h1, 'black')
addText('by Magic Ramba Trash', 85, h2, 'black')

# main content
# generate qr-code
link = 'https://giphy.com/gifs/reactionseditor-yes-awesome-3ohzdIuqJoo8QdKlnW/fullscreen'
generateQRCode(link)
# paste qr-code
xPos = int((W - 450) / 2)
img.paste(qr_img, (xPos, 195))

addText('DEIN BILD | TA PHOTO | YOUR PICTURE', 150, p, 'black')
date = datetime.today().strftime('%d.%m.%Y - %H:%M:%S')
addText(date, 180, p, 'black')

short_link = s.tinyurl.short(link)
print(short_link)
addText(short_link, 620, footer, 'black')

# footer
addText('www.mfk.ch', 730, footer, 'black')
addText('www.magicrambatrash.ch', 760, footer, 'black')

# save image
#date = datetime.today().strftime('%Y-%m-%d_%H%M%S')
#filename = date + '_MfK-Super-Foto.png'
#img.save(filename)
qr_img.save('qr.png')
img.save('test.png')
