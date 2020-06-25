import mysql.connector
import random
import time
import socket

#client parameters
host = '10.0.2.15'
port = 9999
BUFFER_SIZE = 1024

#Database connection parameters
cnx = mysql.connector.connect(user='client1', password='Smpass1$', host = '10.0.2.15', database='smartMeter', port='3306')
cursor = cnx.cursor()

#Initial data just for reference
version = 1.12
clabel = "Online"
instantData = round(random.uniform(2.5, 150.4), 1)
freqData = round(random.uniform(2.5, 150.4), 1)
group = "North"

#Outputting initial data
print("Version = " + str(version))
print("Meter Status = " + str(clabel))
print("Current Data = " + str(instantData))
print("Frequency Data = " + str(freqData))
print("Region Group = " + str(group))
print("\n")

#client connection
client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client1.connect((host, port))

while(1):
	data = client1.recv(1024)

	#Random data gen for instant meter
	updateVal = random.uniform(2.5, 150.4)
	updateVal = round(updateVal, 1)

	#updating current data of smartmeter1
	query = ("UPDATE currentData SET curr_data = "+str(updateVal)+" WHERE curr_id = 1")
	cursor.execute(query)
	cnx.commit()

	#Online/Offline control block
	if data == ("Connect"):
		if clabel == "Online":
			client1.send("Client is already Online")
		else:
			clabel = "Online"
			client1.send("something to update DB")

	if data == ("Disconnect"):
		if clabel == "Offline":
			client1.send("Client is already Offline")

		else:
			clabel = "Offline"
			client1.send("something to update DB")

	#frequency data every 15min (micheal your code would go here)

	#firmware update block
	if data == "Firmware update":
		version = version + 0.1
		print("Version = " + str(version))
		print("Meter Status = " + str(clabel))
		print("Current Data = " + str(updateVal))
		print("Frequency Data = " + str(freqData))
		print("Region Group = " + str(group))
		client1.send("Recieved firmware update")

	#unitprice block
	uprice_query = ("SELECT u_price FROM unitPrice")
	cursor.execute(uprice_query)
	for (u_price) in cursor:
		price = float(u_price[0])

cursor.close()
cnx.close()
client1.close()
