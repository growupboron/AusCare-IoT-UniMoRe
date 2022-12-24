# Independent Display testing code

from PIL import Image
import ST7735

disp = ST7735.ST7735(port=0, cs=0, dc=24, backlight=None, rst=25, width=80, height=160, rotation=90, invert=True)
WIDTH = disp.width
HEIGHT = disp.height

img = Image.open("images/face.jpeg")
#img = img.rotate(90)
img = img.resize((WIDTH,HEIGHT))
img.show()
disp.display(img)
