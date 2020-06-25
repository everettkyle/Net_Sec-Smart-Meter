from flask import (Flask,redirect, render_template, request,url_for)
import socket, pickle, tools
from Crypto.Cipher import AES

salt = '!%F=-?Pst970'
aes_key = "{: <32}".format(salt).encode("utf-8")
iv = Random.new().read(AES.block_size)
aes_cipher = AES.new(aes_key, AES.MODE_CBC, iv)

app = Flask(__name__)

#METER SERVER HOST AND PORT
HOST = ''
PORT = 3500
adminPass = 'RAMK'

@app.route('/',methods=['GET'])
def Index():
    global HOST, PORT
    try:
        data = tools.generateMSG('','','APP','GETMETERS','','',5001)
        data = askAndRecieve((HOST,PORT),('',5001),data)
        meters = data.get('data')
        meters = meters.get('meters')
        regions = data.get('data')
        regions = regions.get('regions')
        regions.append('All Region')
    except:
        return render_template('cmdCnter.html')
    return render_template('cmdCnter.html',Meters=meters, regions=regions)

@app.route('/action',methods=['POST'])
def connect():
    global HOST, PORT,adminPass
    print('data:',request.json)
    data = request.json
    action = request.args.get('action')
    if action in ['DISCONNECT','CONNECT'] and data.get('password',-1) != adminPass:
        data['sender'] = 'Nothing'
    else:
        data = tools.generateMSG(request.json['name'],'','APP',action,'','',5001)
        data = askAndRecieve((HOST,PORT),('',5001),data)
        print(data)
        data['sender'] = request.json['name']
    return str(data['sender'])

'''
@function askAndRecieve() - sends the data to the server then retrieves it
@param sendTo   - tuple of (host,port) of where to send the data to
@param sendBack - tuple of (hosy,port) of where to send the data back after
@param dataToSend     - dictionary of data to send
'''
def askAndRecieve(sendTo, sendBack,dataToSend):
    global aes_cipher
    sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    reciever = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data = {'failuremsg':'failure'}
    try:
        reciever.bind(sendBack)
        reciever.listen(5)
        sender.connect(sendTo)

        dataToSend = aes_cipher.encrypt(dataToSend)
        dataToSend = pickle.dumps(dataToSend)

        sender.sendall(dataToSend)
        (conn, ip) = reciever.accept()
        data = conn.recv(1024)

        data = pickle.loads(data)
        data = aes_cipher.decrypt(data)

        conn.close()
        sender.close()
        reciever.close()
    except:
        sender.close()
        reciever.close()
    return data

def send(dataToSend,sendTo):
    global aes_cipher
    sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sender.connect(sendTo)

        dataToSend = aes_cipher.encrypt(dataToSend)
        dataToSend = pickle.dumps(dataToSend)

        sender.sendall(dataToSend)
    finally:
        sender.close()
    return


'''
@function generateMSG - this function puts the information in the correct format to be sent to the server
@param sender - name of sender
@param region - region that the meter is in
@param role   - role of the sender {SERVER, METER, WEBAPP}
@param action - action that is needed to be completed
@param data   - data being sent
@param IP     - callback IP
@param PORT   - callback port
'''

if __name__=='__main__':
    # app.run(ssl_context=('cert.pem', 'key.pem'))
    app.run()
