import socket
from threading import Thread
import csv
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


def serviceto(client):
	f = client.makefile(mode="rw")
	input = f.readline().strip()
	print('%s: read [%s]' % (address, input))
	custMsg = csvWriter(input)
	
	f.write('echo [%s]' % (custMsg))
	f.close()
	client.close()
	
def mailSend(reply,custId):
	fromaddr = "iotprojectpubmeter@gmail.com"
	if(custId == '1099'):
		toaddr = "e0013515@u.nus.edu"
	if(custId == '1091'):
		toaddr = "sourabhthebest@gmail.com"
		
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "PUB Bill"
	
	body = "Your PUB Bill is : $" + str(reply)
	msg.attach(MIMEText(body, 'plain'))
	 
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "dkiong@123")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()
			
def csvWriter(input):
	
	timeStmp = input[5:24]	
	custId = input[0:4]
	readingLength = len(input)
	reading = input[32:readingLength]
	print 'timestamp %s' % timeStmp
	print 'custID %s' % custId
	print 'reading %s' % reading
	outputFile = open('%s.csv' % custId, 'a')
	writer = csv.writer(outputFile)
	writer.writerow([timeStmp,reading])
	outputFile.close()
	print 'Current reading which get saved for next iter : %s' % reading
	prevReading = previousReading(custId)
	fileHandle(reading,custId)
	
	custMsg = billCal(prevReading,reading)
	mailSend(custMsg,custId)
	
	return custMsg
	
def fileHandle(strNum,custId):
	if(custId == '1091'):
		file = open("previousreadings1091.txt","w")
	if(custId == '1099'):
		file = open("previousreadings1099.txt","w")
		
	print 'Current iteration reading saving in previousreadings.txt : %s ' %strNum
	file.write(strNum)
	file.close()

def previousReading(custId):
	if(custId == '1091'):
		file = open("previousreadings1091.txt","r")
	if(custId == '1099'):
		file = open("previousreadings1099.txt","r")
		
	strNum = file.read()
	print 'fetchin from previousreadings.txt %s : ' % strNum
	prevReading = strNum[:-2]
	prevReading = int(prevReading)
	file.close()
	return prevReading

def billCal(prevReading,currentReading):
	#currentReading = currentReading
	currentReading = int(currentReading[:-2])
	billAmt = 5*(currentReading - prevReading)
	billAmt = str(billAmt)
	billMsg = '%s' % billAmt
	print billMsg
	return billMsg

host = ''
port = 8080
backlog = 5
 
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind((host,port))
soc.listen(backlog)
while 1:
    client, address = soc.accept()
    thread1 = Thread(target=serviceto, args=(client,))
    thread1.start()
