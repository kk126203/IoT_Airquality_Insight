import json,time,sys,mraa,math,MySQLdb,datetime
from threading import Thread
from scipy.stats.stats import pearsonr

db = MySQLdb.connect(host="iotdbinstance.cajidywjgjlk.us-east-1.rds.amazonaws.com",
                     user="edison1",
                     passwd="12345678",
                     db="iotdata")

cursor = db.cursor()
cursor.execute("""SELECT * FROM Airquality WHERE category = 'kitchen'""")
data = cursor.fetchall()

tem = []
quality = []

for i in range (len(data)):
    quality.append(data[i][1])
    tem.append(int(data[i][2]))

print(pearsonr(tem,quality))

