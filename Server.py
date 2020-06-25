import socket, pickle, threading
# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to a public host, and a well-known port
serversocket.bind(('', 3000))
# become a server socket
serversocket.listen(5)

clients = dict()

def handleClient(ID):
    try:
        while 1:
            data = ID[0].recv(512)
            data = pickle.loads(data)
            if data.get('data', -1) != -1:
                print(data['data'])
    except:
        ID[0].close()
    return


try:
    while 1:
        #accept connections from outside
        ID = serversocket.accept()
        #now do something with the clientsocket
        if ID:
            msg = ID[0].recv(512)
            msg = pickle.loads(msg)
            if clients.get(msg['sender'],-1) == -1:
                clients[msg['sender']] = ID
                print('New Log On: ' + msg['sender'])
                ID[0].sendall(b'hello')
                set_thread = threading.Thread(target=handleClient, args=(ID,))
                set_thread.start()

except KeyboardInterrupt:
        for ID in clients.values():
            ID[0].close()
            print('closing socket')
        serversocket.shutdown(1)
