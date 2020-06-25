import sys
import socket
from threading import Thread
from socketserver import ThreadingMixIn

# Multithreaded Python server : TCP Server Socket Thread Pool for meter 001
#single request class
class ClientThread001(Thread):

    def __init__(self,ip,port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print("[+] New server socket thread started for " + ip + ":" + str(port))

    def run(self):
        while True:
            data = conn.recv(2048)
            print("Server received single SmartMeter001 query", data)
            MESSAGE001 = input("Multithreaded Python server : Enter Response from Server/Enter exit:")
            if MESSAGE001 == 'exit':
                break
            conn.send(MESSAGE001)  # echo

# Multithreaded Python server : TCP Server Socket Thread Pool for meter 002

#group request class
class ClientThread002(Thread):

    def __init__(self,ip,port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print("[+] New server socket thread started for " + ip + ":" + str(port))

    def run(self):
        while True :
            data = conn.recv(2048)
            print("Server received single SmartMeter002 query", data)
            MESSAGE002 = input("Multithreaded Python server : Enter Response from Server/Enter exit:")
            if MESSAGE002 == 'exit':
                break
            conn.send(MESSAGE002)  # echo

# Multithreaded Python server : TCP Server Socket Thread Pool for meter 003

#ALL request class
class ClientThread003(Thread):

    def __init__(self,ip,port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print("[+] New server socket thread started for " + ip + ":" + str(port))

    def run(self):
        while True:
            data = conn.recv(2048)
            print("Server received single SmartMeter003 query:", data)
            MESSAGE003 = input("Multithreaded Python server : Enter Response from Server/Enter exit:")
            if MESSAG003E == 'exit':
                break
            conn.send(MESSAGE003)  # echo

# Multithreaded Python server : TCP Server Socket Thread Pool for multiple meters
class ClientThreadALL(Thread):

    def __init__(self,ip,port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print("[+] New server socket thread started for " + ip + ":" + str(port))

    def run(self):
        while True :
            data = conn.recv(2048)
            print("Server received multiple queries", data)
            MESSAGEALL = input("Multithreaded Python server : Enter Response from Server/Enter exit:")
            if MESSAGEALL == 'exit':
                break
            conn.send(MESSAGEALL)  # echo

# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '0.0.0.0'
TCP_PORT = 2004
BUFFER_SIZE = 20  # Usually 1024, but we need quick response

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    user_entry1 = input(">>Enter 'y' for entry into SmartMeter Query System>>")
    if user_entry1 == 'y':
        print('\tEnter alpha-numeric number for the corresponding data:')
        print('\t\t1.Single Meter Instant Reading...')
        print('\t\t2.Group-Meter Instant Reading...')
        print('\t\t3.Enter "exit" if you want to exit this system')

        user_entry2 = input('\t\t>>')
        if user_entry2 == '1': #enter single reading
            print('\t\t\tEnter alphabetic number for the corresponding SmartMeter:')
            print("\t\t\t\ta.SmartMeter 001:")
            print("\t\t\t\tb.SmartMeter 002:")
            print("\t\t\t\tc.SmartMeter 003:")

            user_entry3 = input('\t\t\t\t>>')
            if user_entry3 == 'a':
                print('\t\t\t\t\tSmartMeter 001:')
                while True:
#make loop bind to one instance of a smartmeter
                    tcpServer.listen(4)
                    print("\t\t\t\t\t\t001-Waiting for connections from TCP clients:")
                    (conn, (ip,port)) = tcpServer.accept()
                    newthread = ClientThread001(ip,port)
                    newthread.start()
                    threads.append(newthread)
                    for t in threads:
                        t.join()
                    print("Enter 'x' if you'd like to exit, else press 'enter'")
                    user_entry4 = input('\t\t\t\t\t\t>>')
                    if user_entry4 == 'x':
                        break
                    else:
                        continue

            elif user_entry3 == 'b':
                print('\t\t\t\t\tSmartMeter 002:')
                while True:
#make loop bind to one instance of a smartmeter
                    tcpServer.listen(4)
                    print("\t\t\t\t\t\t002-Waiting for connections from TCP clients:")
                    (conn, (ip,port)) = tcpServer.accept()
                    newthread = ClientThread002(ip,port)
                    newthread.start()
                    threads.append(newthread)
                    for t in threads:
                        t.join()
                    print("Enter 'x' if you'd like to exit, else press 'enter'")
                    user_entry4 = input('\t\t\t\t\t\t>>')
                    if user_entry4 == 'x':
                        break
                    else:
                        continue

            elif user_entry3 == 'c':
                print('\t\t\t\t\tSmartMeter 003:')
                while True:
#make loop bind to one instance of a smartmeter
                    tcpServer.listen(4)
                    print("\t\t\t\t\t\t003-Waiting for connections from TCP clients...")
                    (conn, (ip,port)) = tcpServer.accept()
                    newthread = ClientThread003(ip,port)
                    newthread.start()
                    threads.append(newthread)
                    for t in threads:
                        t.join()
                    print("Enter 'x' if you'd like to exit, else press 'enter'")
                    user_entry4 = input('\t\t\t\t\t\t>>')
                    if user_entry4 == 'x':
                        break
                    else:
                        continue

        elif user_entry2 == '2': #enter group reading
            while True:
#make loop functional to recieve data from multiple smart meters
                tcpServer.listen(4)
                print("\t\t\t\tALL-Waiting for connections from TCP multiple meters...")
                (conn, (ip,port)) = tcpServer.accept()
                newthread = ClientThreadALL(ip,port)
                newthread.start()
                threads.append(newthread)
                for t in threads:
                    t.join()
        elif user_entry2 == '3':
            sys.exit()
