import socket
from datetime import datetime
import random
import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def readingValue():
	file = open("readings.txt","r")
	fileName = file.name
	print fileName
	strNum = file.read()
	print strNum
	newReading = strNum
	number = int(strNum)
	meterReading = number + round(random.randrange(100,750))
	strNum = str(meterReading)
	strNum = strNum[:-2]
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
        toaddr = "e0013515@u.nus.edu"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "PUB Bill"
        reply = 100
        body = "Your PUB Bill is : $" + str(reply)
        msg.attach(MIMEText(body, 'plain'))
 
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "dkiong@123")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()

host = '10.10.24.165'
port = 8080
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = socket.gethostbyname(host)
soc.connect((ip, port))
 
f = soc.makefile(mode="rw")

meterReading = readingValue()
#fileHandle()
networkVar = str(datetime.now())+' '+str(meterReading)

x=len(str(datetime.now()))


f.write('1099 %s \n' % networkVar)
f.flush()
reply = f.readline()
#mailSend(reply)
print(reply)
f.close()
soc.close()
