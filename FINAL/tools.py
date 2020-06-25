import pickle


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
def generateMSG(sender, region, role, action, data, IP, PORT):
    payload = {'sender':sender,'region':region,'role':role,'action':action,'data':data,'ip':IP, 'port':PORT}
    payload = pickle.dumps(payload)
    return payload
