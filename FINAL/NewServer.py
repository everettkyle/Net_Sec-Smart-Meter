import socket, pickle, threading, tools, sys
import test_queries as db
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import AES

salt = '!%F=-?Pst970'
aes_key = "{: <32}".format(salt).encode("utf-8")
iv = Random.new().read(AES.block_size)
aes_cipher = AES.new(aes_key, AES.MODE_CBC, iv)

#Generate private and public keys
random_generator = Random.new().read
private_key = RSA.generate(1024, random_generator)
public_key = private_key.publickey()
meter_pubkey = None


def sendToMeter(data,MeterID):
    global meter_pubkey
    try:
         data['ip'] = '10.0.2.15'     #Set the data to return to the server
         data['port'] = 3500 #Set the data to return to the server
         print(data)
         conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         conn.connect(MeterID) #We'd connect to where the database tells us to

         data = meter_pubkey.encrypt(data['sender'], meter_pubkey) #this is what I changed
         data = pickle.dumps(data)

         conn.sendall(data)
         conn.close()
    except Exception as e:
        print('Error in sendToMeter():',e)
    finally:
        conn.close()
    return

def handleRegion(data):
    global aes_cipher
    try:
        ip = data['ip']
        port = data['port']
        data['sender'] = data['sender'].split(' ')
        region = data['sender'][0]
        names = db.queryDatabase(data,region) # Query the database for meternames in a region list[]
        print('NAMES',names)
        action = data['action']
        package = list()
        for meter in names:
            data['sender'] = meter
            package.append(handleWebApp(data,False))
        payload = tools.generateMSG('','','',action,package,'10.0.2.15',3500)
        sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender.connect((ip, port))

        payload = aes_cipher.encrypt(payload)
        payload = pickle.dumps(payload)

        sender.sendall(payload)
        sender.close()
    except Exception as e:
        print('Error in handleRegion():', e)
        sender.close()
    return

def handleAll(data):
    global aes_cipher
    try:
        ip = data['ip']
        port = data['port']
        names = db.queryDatabase(data,'ALL') # Query the database for meternames in a region list[]
        print('NAMES',names)
        action = data['action']
        package = list()
        for meter in names:
            data['sender'] = meter
            package.append(handleWebApp(data,False))
        payload = tools.generateMSG('','','',action,package,'10.0.2.15',3500)
        sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender.connect((ip,port))

        payload = aes_cipher.encrypt(payload)
        payload = pickle.dumps(payload)

        sender.sendall(payload)
        sender.close()
    except Exception as e:
        print('Error in handleRegion():', e)
        sender.close()
    return
    pass

def handleMeter(data):
    global meter_pubkey, public_key
    if data['action'] == 'UPDATEUSE':
        db.queryDatabase(data, 'UPDATEUSE')
        #A DB Call would be made here using the sender's name
        #to update ussage
        pass
    elif data['action'] == 'GETPRICE':
        db.queryDatabase(data, 'GETPRICE')
        #Using the Port attribute a return call
        #can be made to send the prices.
        pass
    elif data['action'] == 'SECURE':

        meter_pubkey = data["data"]
        print("\n")
        print("Meter:", meter_pubkey)
        print('i went through')
        print("\n")
        data['data'] = public_key
        sendToMeter(data,(data['ip'], data['port']))

    elif data['action'] == 'SECURED':
        print(data['ip'])
        db.queryDatabase(data['ip'], 'UPSECURED')
        print('Trying to secure')
        pass#db to mark meter as authenticated given the name and IP
    elif data['action'] == 'CONNECT':
        db.queryDatabase(data, 'CONNECT')
        pass #DB CALL TO update status to connected
    elif data['action'] == 'DISCONNECT':
        db.queryDatabase(data, 'DISCONNECT')
        pass#DB Call to make status disconnected
    elif data['action'] == 'UFIRM':
        db.queryDatabase(data, 'UFIRM')
        pass #DB Call to use the data['data'] (str) the new firmware value
    else:
        print('Unable to process request', data)
    return

#@param flag - determines behavior of function True for single meters. False for region wide.
def handleWebApp(data,flag):
    global aes_cipher
    #Through the web app requests the server will
    #know when to ask for updated info
    sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        #Not sure if I'm going to keep this if else ladder, it just makes sure only valid requests get through
        if data['action'] in ['UPDATEUSE','DISCONNECT','CONNECT','UFIRM']:
            if flag:
                sender.connect((data['ip'],data['port'])) #send back to the web app
            if data['action'] == 'CONNECT':
                data['data'] = 'Connection confirmed'
            elif data['action'] == 'DISCONNECT':
                data['data'] = 'Connection disconnected'
            elif data['action'] == 'UPDATEUSE':
                data['data'] = 'Usage is updated'
            elif data['action'] == 'UFIRM':
                data['data'] = 'Firmware updated'

            meterAddress = db.queryDatabase(data,'ADDRESS')     #I want the address and port (tuple()) given the name
                                                                #can also be list to turn into tuple honestly up to you
            sendToMeter(data,(meterAddress,3501))               #put variable meter address back in here
        elif data['action'] == 'GETMETERS':                     #Will send the names of the meters to the web app
            #make the db call to get the data from the meters
            sender.connect((data['ip'],data['port']))
            # regions = queryDatabase(data,'METERS','REGIONS' ) #Query the database for all used regions return list[]
            names = db.queryDatabase(data,'ALL') #I want the names of all the meters list[]
            data['data'] = {'meters':names,'regions':['West Region','East Region','South Region', 'North Region']}#Dumby
        else:
            print('Unable to process application request')
            sender.close()
            return
        if flag:

            data = aes_cipher.encrypt(data)
            data = pickle.dumps(data)

            sender.sendall(data)
        else:
            return data
    except Exception as e:
        print('Error in handleWebApp():',e)
    finally:
        sender.close()
    return


def routeHandleClients(data,ip):
    #Routes the requests to their action based on the role
    if data['role'] == 'METER':
        handleMeter(data)

    elif data['role'] == 'APP' and ip[0] == '127.0.0.1':
        if data['sender'].split(' ')[-1] == 'Region': #regions will call handleWebApp() multiple times
            if data['sender'].split(' ')[0] == 'All':
                handleAll(data)
        else:
            handleWebApp(data,True)
    else:
        print('request could not be handled:', data)
    return


#Main Routine that listens for connections and then calls routeHandler
def main(s):
    global private_key
    try:
        HOST = ''
        PORT = 3500
        s.bind((HOST,PORT))
        s.listen(5)
        print('Listening @ Port:',PORT)
        while 1: #This will constantly recieve requests and direct them to the handler
            try:
                conn, IP = s.accept()
                data = conn.recv(4096)
                data = pickle.loads(data)
                print(IP)
                print(data)
                print(sys.getsizeof(data))
                if IP[0] == '127.0.0.1':
                    print('local access granted')
                    pass
                elif int(db.queryDatabase(IP[0],'ISSECURED')):
                    print('SECURED')

                    data = private_key.decrypt(data)

                    print('PASS')
                    pass
                elif not int(db.queryDatabase(IP[0],'ISSECURED')) and data['action'] in ['SECURE','SECURED']:
                    print('TRYING to secure')
                    pass
                else:
                    print('not secure or trying to')
                    conn.close()
                    continue
                routeHandleClients(data,IP) #Single thread option
                conn.close()
            except Exception as e:
                print('ERROR in main():',e)
    except KeyboardInterrupt:
        s.close()
    return

if __name__=='__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    main(s)

#THOUGHTS:
#send secure request to server
#server recieves data and sees it's secure
#if it was an encrypted packet (don't encrypt the whole thing)
#check the name and query db to see if its secured