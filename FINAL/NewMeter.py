import socket, threading, time, pickle, tools, sys,random
from Crypto.PublicKey import RSA
from Crypto import Random


#Generate private and public keys
random_generator = Random.new().read
private_key = RSA.generate(1024, random_generator)
public_key = private_key.publickey()
server_pubkey = None


#Handles Servers requests
def requestHandler(data):
    global POWERSTATUS, FIRMWAREV, PRICE, public_key, private_key, server_pubkey
    sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender.connect((data['ip'],data['port']))

    data = private_key.decrypt(data)

    msg = {'data':'failure'}
    if data['action'] == 'CONNECT':
        POWERSTATUS = 'CONNECTED'
        print('POWER:',POWERSTATUS)
        msg = tools.generateMSG(1,'North','METER','CONNECT','Status: ' + POWERSTATUS,'10.0.2.4',3501)
    elif data['action'] == 'DISCONNECT':
        POWERSTATUS = 'DISCONNECTED'
        print('POWER:',POWERSTATUS)
        msg = tools.generateMSG(1,'North','METER','DISCONNECT','STATUS: ' + POWERSTATUS,'10.0.2.4',3501)
    elif data['action'] == 'UPDATEUSE':
        print('SENDING RECENT USAGE')
        msg = tools.generateMSG(1,'North','METER','UPDATEUSE',random.uniform(10,200),'10.0.2.4',3501)
    elif data['action'] == 'UFIRM':
        FIRMWAREV += .01
        print('UPDATED FIRMWARE:',FIRMWAREV)
        msg = tools.generateMSG(1,'North','METER','UFIRM',FIRMWAREV,'10.0.2.4',3501)
        pass
    elif data['action'] == 'GETPRICE': #Reciever recieves the get price data
        pass
    elif data['action'] == 'SECURE':#this is where the secuirty routine will begin

        server_pubkey = data['data']
        print("\n\n")
        print("Server: ", server_pubkey)
        print("\n\n")
        msg = tools.generateMSG(1,'North','METER','SECURED','MAC0 has sent public key to server hub.','10.0.2.4',3501)
    msg = public_key.encrypt(msg)

    sender.sendall(msg)
    sender.close()


#Recivers Info from the Server
def recieve(sender,reciever):
    global private_key
    try:
        HOST = ''
        PORT = 3501
        reciever.bind((HOST,PORT))
        reciever.listen(5)
        while 1:
            conn, IP = reciever.accept()
            data = conn.recv(4096)

            data = pickle.loads(data)
            data = private_key.decrypt(data)


            requestHandler(data)
            print(data)
            conn.close()
    finally:
        reciever.close()
    return

#Main regularly Updates the server with usage and starts
#The Initial Threads
def main(sender,reciever):
    global server_pubkey
    server_pubkey = 0
    HOST = '10.0.2.15'
    PORT = 3500
    #Start the Threads here
    recieverThread = threading.Thread(target=recieve,args=(sender,reciever,))
    recieverThread.daemon = True
    recieverThread.start()
    #Start Updating
    public_key_meter = public_key
    sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender.connect((HOST, PORT))
    data = tools.generateMSG(1, 'North', 'METER', 'SECURE', public_key_meter,'10.0.2.4' , 3501)

    data = server_pubkey.encrypt(data['data'], server_pubkey )
    data = pickle.dumps(data)

    sender.sendall(data)
    sender.close()
    start_time = time.time()
    while 1:
        end_time = time.time()
        if end_time - start_time >= 20: #Constantly UpDates the server every duration
            sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sender.connect((HOST,PORT))
            data = tools.generateMSG(1,'North','METER','UPDATEUSE', 133.4,'10.0.2.4',3501)

            data = server_pubkey.encrypt(data)
            data = pickle.dumps(data)

            sender.sendall(data)
            start_time = end_time
            print('sending...')
            print("\n\n")
            print("Meter: ", public_key_meter)
            sender.close()
        time.sleep(10)
    return



#METER INFORMATION
POWERSTATUS = 'CONNECTED'
FIRMWAREV   = 1.00
PRICE = 0.0
REGION = 'North'

if __name__ == '__main__':
    sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    reciever = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    main(sender, reciever)
