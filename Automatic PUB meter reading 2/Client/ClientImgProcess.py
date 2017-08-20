import socket
from datetime import datetime
import time
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import random
import os
import ImgProccessor
import glob
from PIL import Image
from pytesser import *
imageFolderPath = 'C:\\Users\\sachi\\Desktop\\IOT\\Project\\ImageDatabase'
imagePath = glob.glob(imageFolderPath+'/*.png')
for i in range(1,len(imagePath) + 1):
	ImgProccessor.process(i)

	def readingValue():
		file = open("readings.txt","r")
		fileName = file.name
		print fileName
		strNum = file.read()
		print strNum
		newReading = strNum
		number = int(strNum)
		meterReading = number 
		#+ round(random.randrange(100,750))
		strNum = str(meterReading)
		#strNum = strNum[:-2]
		file.close()
		os.remove(fileName)
		fileHandle(strNum)
		return meterReading
		
	def fileHandle(strNum):
		file = open("readings.txt","w")
		print 'New reading before assigning is %s :' %strNum
		file.write(strNum)
		file.close()
     
	def mailSend(reply):
		fromaddr = "iotprojectpubmeter@gmail.com"
		toaddr = "sachinpawar1989@gmail.com"
		msg = MIMEMultipart()
		msg['From'] = fromaddr
		msg['To'] = toaddr
		msg['Subject'] = "PUB Bill"
		#reply = 100
		body = "Your PUB Bill is : $" + str(reply)
		msg.attach(MIMEText(body, 'plain'))
 
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(fromaddr, "dkiong@123")
		text = msg.as_string()
		server.sendmail(fromaddr, toaddr, text)
		server.quit()

	host = '172.23.133.204'
	port = 8080
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ip = socket.gethostbyname(host)
	soc.connect((ip, port))
	 
	f = soc.makefile(mode="rw")

	meterReading = readingValue()
	networkVar = str(datetime.now())+' '+str(meterReading)
	f.write('9999 %s \n' % networkVar)
	f.flush()
	reply = f.readline()
	reply = reply[5:len(reply)]
	print reply
	mailSend(reply)
	print(reply)
	f.close()
	soc.close()
	time.sleep(7)