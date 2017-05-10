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


cursor.execute("""SELECT * FROM Airquality WHERE category = 'dorm_indoor'""")
data = cursor.fetchall()
cursor.execute("""SELECT * FROM Dustinfo WHERE category = 'dorm_indoor'""")
data1 = cursor.fetchall()
total = len(data)/len(data1)
start = len(data) - len(data1)*total


#Air quality vs temperature
for i in range (start,len(data)):
    quality.append(data[i][1])
    tem.append(int(data[i][2]))

print('Air quality vs temperature : ')
print (pearsonr(tem,quality))


# Dust vs Air qualityv
for i in range (len(data1)):
    for j in range (0,total):
	dust.append(int(data1[i][3]))

print ('Dust vs Air quality : ')
print (pearsonr(dust,quality))

#Dust vs temperature

print ('Dust vs temperature')
print (pearsonr(tem,dust))


