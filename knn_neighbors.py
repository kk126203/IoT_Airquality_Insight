import pymysql, sys
import numpy as np
pymysql.install_as_MySQLdb()
import json,time,sys,math,datetime,MySQLdb
from threading import Thread
from scipy.stats.stats import pearsonr
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.neighbors import KNeighborsClassifier


db = MySQLdb.connect(host="iotdbinstance.cajidywjgjlk.us-east-1.rds.amazonaws.com",
                     user="edison1",
                     passwd="12345678",
                     db="iotdata")


training_set = []
target = []
# traing_set vector : [air_q, tem, Dust]
# target : 0-> dorm_indoor, 1-> dorm_outside, 2->restroom, 3-> kitchen

def train():

	#indoor training
	cursor = db.cursor()
	cursor.execute("""SELECT * FROM Airquality WHERE category = 'dorm_indoor'""")
	data_airq = cursor.fetchall()
	cursor.execute("""SELECT * FROM Dustinfo WHERE category = 'dorm_indoor'""")
	data_Dust = cursor.fetchall()

	loop = len(data_airq)/len(data_Dust)

	for i in range (loop):
		vector = []
		vector.append(data_airq[i*len(data_Dust)][1])
		vector.append(data_airq[i*len(data_Dust)][2])
		vector.append(data_Dust[i][3])
		training_set.append(vector)
		target.append(0)
	

	# outdoor training
	cursor = db.cursor()
        cursor.execute("""SELECT * FROM Airquality WHERE category = 'dorm_outside'""")
        data_airq = cursor.fetchall()
        cursor.execute("""SELECT * FROM Dustinfo WHERE category = 'dorm_outside'""")
        data_Dust = cursor.fetchall()

        loop = len(data_airq)/len(data_Dust)

        for i in range (loop):
		vector = []
                vector.append(data_airq[i*len(data_Dust)][1])
                vector.append(data_airq[i*len(data_Dust)][2])
                vector.append(data_Dust[i][3])
		training_set.append(vector)
                target.append(1)


	# restroom training
        cursor = db.cursor()
        cursor.execute("""SELECT * FROM Airquality WHERE category = 'iotdata'""")
        data_airq = cursor.fetchall()
        cursor.execute("""SELECT * FROM Dustinfo WHERE category = 'iotdata'""")
        data_Dust = cursor.fetchall()

        loop = len(data_airq)/len(data_Dust)

        for i in range (loop):
                vector = []
                vector.append(data_airq[i*len(data_Dust)][1])
                vector.append(data_airq[i*len(data_Dust)][2])
                vector.append(data_Dust[i][3])
                training_set.append(vector)
                target.append(2)

	
	# kitchen training
        cursor = db.cursor()
        cursor.execute("""SELECT * FROM Airquality WHERE category = 'kitchen'""")
        data_airq = cursor.fetchall()
        cursor.execute("""SELECT * FROM Dustinfo WHERE category = 'kitchen'""")
        data_Dust = cursor.fetchall()

        loop = len(data_airq)/len(data_Dust)

        for i in range (loop):
                vector = []
                vector.append(data_airq[i*len(data_Dust)][1])
                vector.append(data_airq[i*len(data_Dust)][2])
                vector.append(data_Dust[i][3])
                training_set.append(vector)
                target.append(3)


def main():
	a = 0
	train()
	air_q = int(sys.argv[1])
	tem = int(sys.argv[2])
	dust = int(sys.argv[3])
	k = KNeighborsClassifier(n_neighbors=11)
	k.fit(training_set, target)	
	index = k.predict_proba([[air_q, tem, dust]])
	maxi = 0
	num = 0

	#find the class that has the maximum percentage
	for i in range (len(index[0])):
		if index[0][i]>maxi:
			maxi = index[0][i]
			num = i

	if(num==0):
		print('The location is indoor reading room and confidence is :')
		print(maxi)
	elif num==1:
		print('The location is at outdoors and confidence is :')
		print(maxi)
	elif num==2:
		print('The location is bathroom and confidence is :')
		print(maxi)
	elif num==3:
		print('The location is kitchen and confidence is :')
		print(maxi)
	else:
		print('Unrecognizable')

# main function entry point
if(len(sys.argv)!=4):
	print('need 3 argument : air_q, tem, dust')
	sys.exit(0)
main()
