import mysql.connector

cnx = mysql.connector.connect(user='DBadmin', password='Theantsgomarching3$', host='localhost', database='smartMeter')
cursor = cnx.cursor()
region = 'West'
# if statement for usage data
# if statement for Security

# if statement for Names ----> Regions

if region == 'West':
    query = ("SELECT id FROM class_SM WHERE grp =%s")
    grp = ('West',)
    cursor.execute(query, grp)
    print(cursor)
    record = cursor.fetchall()
    grp = []
    for var in range(len(record)):
        grp.append(int(record[var][0]))