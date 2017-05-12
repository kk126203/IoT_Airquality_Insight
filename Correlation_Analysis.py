import pymysql
pymysql.install_as_MySQLdb()
import json,time,sys,math,datetime,MySQLdb
from threading import Thread
from scipy.stats.stats import pearsonr

db = MySQLdb.connect(host="iotdbinstance.cajidywjgjlk.us-east-1.rds.amazonaws.com",
                     user="edison1",
                     passwd="12345678",
                     db="iotdata")

cursor = db.cursor()
tem = []
quality = []
dust = []


# bathroom analysis
cursor.execute("""SELECT * FROM Airquality WHERE category = 'iotdata'""")
data = cursor.fetchall()
cursor.execute("""SELECT * FROM Dustinfo WHERE category = 'iotdata'""")
data1 = cursor.fetchall()
total = len(data)/len(data1)
start = len(data) - len(data1)*total

for i in range (start,len(data)):
    quality.append(data[i][1])
    tem.append(int(data[i][2]))

for i in range (len(data1)):
    for j in range (0,total):
	dust.append(int(data1[i][3]))

print  
print ('In bathroom, the correlation coefficents between each two of the three attributes are listed below')
print ('Air quality vs temperature : ')
print (pearsonr(tem,quality)[0])
print ('Dust concentration vs Air quality : ')
print (pearsonr(dust,quality)[0])
print ('Dust and temperature')
print (pearsonr(tem,dust)[0])


#kitchen analysis
cursor.execute("""SELECT * FROM Airquality WHERE category = 'kitchen'""")
data = cursor.fetchall()
cursor.execute("""SELECT * FROM Dustinfo WHERE category = 'kitchen'""")
data1 = cursor.fetchall()
total = len(data)/len(data1)
start = len(data) - len(data1)*total

del tem[:]
del quality[:]
del dust[:]

for i in range (start,len(data)):
    quality.append(data[i][1])
    tem.append(int(data[i][2]))

for i in range (len(data1)):
    for j in range (0,total):
        dust.append(int(data1[i][3]))

print
print ('At kitchen, the correlation coefficents between each two of the three attributes are listed below')
print ('Air quality vs temperature : ')
print (pearsonr(tem,quality)[0])
print ('Dust concentration vs Air quality : ')
print (pearsonr(dust,quality)[0])
print ('Dust and temperature')
print (pearsonr(tem,dust)[0])


# indoor reading room analysis
cursor.execute("""SELECT * FROM Airquality WHERE category = 'dorm_indoor'""")
data = cursor.fetchall()
cursor.execute("""SELECT * FROM Dustinfo WHERE category = 'dorm_indoor'""")
data1 = cursor.fetchall()
total = len(data)/len(data1)
start = len(data) - len(data1)*total

del tem[:]
del quality[:]
del dust[:]

for i in range (start,len(data)):
    quality.append(data[i][1])
    tem.append(int(data[i][2]))

for i in range (len(data1)):
    for j in range (0,total):
        dust.append(int(data1[i][3]))

print
print ('In indoor reading room, the correlation coefficents between each two of the three attributes are listed below')
print ('Air quality vs temperature : ')
print (pearsonr(tem,quality)[0])
print ('Dust concentration vs Air quality : ')
print (pearsonr(dust,quality)[0])
print ('Dust and temperature')
print (pearsonr(tem,dust)[0])


# outdoor analysis
cursor.execute("""SELECT * FROM Airquality WHERE category = 'dorm_outside'""")
data = cursor.fetchall()
cursor.execute("""SELECT * FROM Dustinfo WHERE category = 'dorm_outside'""")
data1 = cursor.fetchall()
total = len(data)/len(data1)
start = len(data) - len(data1)*total

del tem[:]
del quality[:]
del dust[:]

for i in range (start,len(data)):
    quality.append(data[i][1])
    tem.append(int(data[i][2]))

for i in range (len(data1)):
    for j in range (0,total):
        dust.append(int(data1[i][3]))

print
print ('On outdoor streets, the correlation coefficents between each two of the three attributes are listed below')
print ('Air quality vs temperature : ')
print (pearsonr(tem,quality)[0])
print ('Dust concentration vs Air quality : ')
print (pearsonr(dust,quality)[0])
print ('Dust and temperature')
print (pearsonr(tem,dust)[0])

