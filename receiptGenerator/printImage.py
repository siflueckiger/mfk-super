from escpos.printer import Usb
import argparse

parser = argparse.ArgumentParser(description='print qr code')
parser.add_argument('-i', '--image_name', type=str, metavar="", required=True, help='filename of image to print')
args = parser.parse_args()

p = Usb(0x04b8,0x0e28,0)

def printImage(filename):
	p.image(filename, impl='graphics')
	p.cut()
	print('File %s printed.' % filename)

printImage(args.image_name)
