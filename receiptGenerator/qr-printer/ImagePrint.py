# Code for Raspberry Pi

from escpos.printer import Usb

p = Usb(0x04b8,0x0e28,0)

image = "test.png"
p.image(image, impl='graphics')

p.cut()
