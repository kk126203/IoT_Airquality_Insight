import pymysql
pymysql.install_as_MySQLdb()
import json,time,sys,mraa,math,datetime,boto,MySQLdb
from threading import Thread
from upm import pyupm_ppd42ns as upmPpd42ns


db = MySQLdb.connect(host="iotdbinstance.cajidywjgjlk.us-east-1.rds.amazonaws.com",
                     user="edison1",
                     passwd="12345678",
                     db="iotdata")


def sensors(db, cat):
    dust = upmPpd42ns.PPD42NS(8)
    index = dust.getData().concentration
    aqPN = 1
    tempPN = 0
    B = 4275.0
    cur = db.cursor()
    airSensor = mraa.Aio(aqPN)
    tempSensor = mraa.Aio(tempPN)
    aq = airSensor.read()
    print("Air quality: " + str(aq))
    tempRead = tempSensor.read()
    R = 1023.0*100000.0/tempRead-100000.0
    temp = 1.0/(math.log(R/100000.0)/B+1.0/298.15)-273.15
    timestamp = time.time() - 4.0*60.0*60.0
    print(temp)
    cur.execute("""INSERT INTO Airinfo (timestamp, aq, temp, concentration, category)
                 VALUES (%s, %s, %s, %s, %s)""", (timestamp, aq, temp, index, cat))
    db.commit()
    print("Temperature: " + str(temp))
    print(str(timestamp))
    print("collection finished")

try:
    if(len(sys.argv) < 2):
        print("Usage: python .py category")
        sys.exit(0)
    sensorsThread = Thread(target=sensors, args=(db, sys.argv[1]))
    sensorsThread.start()
except KeyboardInterrupt:
    sys.exit(0)
