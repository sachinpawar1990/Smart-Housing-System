from PIL import Image
from pytesser import *
import time

def process(i):
	#im = Image.open('C:\\Users\\sachi\\Desktop\\IOT\\Project\\1234.png')
	text = imageCapture(i)
	file = open("readings.txt","w")
	#print 'Img Pro value saved in file %s' % text
	file.write(text)
	file.close()
	
def imageCapture(i):
	im = Image.open('C:\\Users\\sachi\\Desktop\\IOT\\Project\\ImageDatabase\\%s.png' % i)
	text = image_to_string(im)
	return text