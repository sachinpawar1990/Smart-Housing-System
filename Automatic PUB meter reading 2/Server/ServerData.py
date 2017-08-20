import socket
from threading import Thread
import csv
import sqlite3
import sys


def serviceto(client):
	f = client.makefile(mode="rw")
	input = f.readline().strip()
	print('%s: read [%s]' % (address, input))
	custMsg = csvWriter(input)
	f.write('echo [%s]' % (custMsg))
	f.close()
	client.close()
			
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
	#print 'Current reading which get saved for next iter : %s' % reading
	prevReading = previousReading()
	fileHandle(reading)
	
	custMsg = billCal(prevReading,reading)
	database(custId,timeStmp,reading)
	return custMsg

def database(custId,timeStmp,reading):
	row = (custId,timeStmp,reading)
	connection = None
	try:
		connection = sqlite3.connect('mydatabase.db')
		cursor = connection.cursor()
		
		#cursor.execute("CREATE TABLE Customer(Id Text, Date_Time TEXT, Reading_Value Text)")
		cursor.execute("INSERT INTO Customer(Id,Date_Time,Reading_Value) VALUES (?,?,?)", row)
		connection.commit()
	except sqlite3.Error, e:
		print "Error %s:" % e.args[0]
		sys.exit(1)
	finally:
		if connection:
			connection.close()
	
def fileHandle(strNum):
	file = open("previousreadings.txt","w")
	#print 'Current iteration reading saving in previousreadings.txt : %s ' %strNum
	file.write(strNum)
	file.close()

def previousReading():
	file = open("previousreadings.txt","r")
	strNum = file.read()
	#print 'fetchin from previousreadings.txt %s : ' % strNum
	prevReading = strNum
	prevReading = int(strNum)
	file.close()
	return prevReading

def billCal(prevReading,currentReading):
	#currentReading = currentReading
	currentReading = int(currentReading)
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
