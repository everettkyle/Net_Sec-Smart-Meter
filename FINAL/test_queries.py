import mysql.connector

def queryDatabase(data, param1):
    cnx = mysql.connector.connect(user='DBadmin', password='Theantsgomarching3$', host='localhost', database='smartMeter')
    cursor = cnx.cursor()

    # if statement for ALL id
    if param1 == 'ALL':
        query = ("SELECT id FROM class_SM")
        cursor.execute(query)
        record = cursor.fetchall()
        ids = []
        for var in range(len(record)):
            ids.append(int(record[var][0]))
        cursor.close()
        cnx.close()
        return ids

    # if statement that returns 1 or 0 based on secured status
    if param1 == 'ISSECURED':
        query = ("SELECT secure_status FROM class_SM WHERE ip_addr =%s")
        q1 = (data,)
        cursor.execute(query, q1)
        record = cursor.fetchall()
        cursor.close()
        cnx.close()
        return record[0][0]

    if param1 == 'UPSECURED':
        query = ("UPDATE class_SM SET secure_status = 1 WHERE ip_addr =%s")
        q1 = (data,)
        cursor.execute(query, q1)
        cnx.commit()
        print("Secure status updated for smart meter" + str(data['sender']))
        cursor.close()
        cnx.close()

    # if statement for usage data (instant meter update)
    if param1 == 'UPDATEUSE':
        #dum_val = 133.4
        query = ("UPDATE currentData SET curr_data = " + str(data['data']) + "WHERE curr_id =" + str(data['sender']))
        cursor.execute(query)
        cnx.commit()
        print("Frequency data updated in database for smart meter " + str(data['sender']))
        cursor.close()
        cnx.close()

    # if statement for get unit price
    if param1 == 'GETPRICE':
        query = ("SELECT * FROM unitPrice")
        cursor.execute(query)
        record = cursor.fetchall()
        unitPrice = float(record[0][1])
        cursor.close()
        cnx.close()
        return unitPrice

    # if statement to turn a certain meter ON
    if param1 == 'CONNECT':
        query = ("UPDATE class_SM SET status =%s WHERE id =" + str(data['sender']))
        status = ('Online',)
        cursor.execute(query, status)
        cnx.commit()
        print("Status updated to Online")
        cursor.close()
        cnx.close()

    # if statement to turn a certain meter OFF
    if param1 == 'DISCONNECT':
        query = ("UPDATE class_SM SET status =%s WHERE id =" + str(data['sender']))
        status = ('Offline',)
        cursor.execute(query, status)
        cnx.commit()
        print("Status updated to Offline")
        cursor.close()
        cnx.close()

    # if statement for firmware update
    if param1 == 'UFIRM':
        query = ("UPDATE firmwareData SET version = " + str(data['data']) + " WHERE firm_id =" + str(data['sender']))
        cursor.execute(query)
        cnx.commit()
        print("Firmware update for Smart Meter " + str(data))
        cursor.close()
        cnx.close()

    # if statement for ip address based id's
    if param1 == 'ADDRESS':
        query = ("SELECT ip_addr FROM class_SM WHERE id=" + str(data['sender']))
        cursor.execute(query)
        record = cursor.fetchall()
        ip = str(record[0][0])
        return ip

    # This query returns a list of the names(id's) related to a certain region
    if param1 in ['West', 'North','East','South']:
        query = ("SELECT id FROM class_SM WHERE grp =%s")
        grp = (param1,)
        cursor.execute(query, grp)
        record = cursor.fetchall()
        grp = []
        for var in range(len(record)):
            grp.append(int(record[var][0]))
        cursor.close()
        cnx.close()
        return grp


#region = 'West'
#data = 1

#region = queryDatabase(data, region)
#instant_update = queryDatabase(data, 'UPDATEUSE')
#get_uprice = queryDatabase(data, 'GETPRICE')

#print(region)
#print(get_uprice)
#print(queryDatabase(data, 'ADDRESS'))

#queryDatabase('10.0.2.4', 'UPSECURED')
#queryDatabase(data, 'DISCONNECT')
#queryDatabase(data, 'UFIRM')
#rec = queryDatabase('10.0.2.4', 'SECURED')
#print(rec)
#print(queryDatabase(data, 'ALL'))
