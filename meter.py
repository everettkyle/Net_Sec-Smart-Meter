import socket, threading, time, pickle

def sendTime():
    global s
    start_time = time.time()
    while 1:
        end_time = time.time()
        if end_time - start_time >= 1:
            payload = {'sender':'MAC0','data':'usage data for meter 0'}
            payload = pickle.dumps(payload)
            s.sendall(payload)
            start_time = end_time



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('',3000))

set_thread = threading.Thread(target=sendTime)

payload = {'sender':'MAC0'}
payload = pickle.dumps(payload)
s.sendall(payload)
msg = s.recv(512)
set_thread.start()

print(str(msg))
