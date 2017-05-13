1.Prerequisite : 

To interact with our MySQL database and analyze data store in it, first open the terminal (suppose you are using Ubuntu) and run: 

"sudo pip install PyMySQL"

Then install sklearn package

"sudo apt-get update"
"sudo apt-get install python-sklearn"

Don't forget to install the statistic package for correlation analysis 

"sudo apt-get install python-scipy"
"pip install scipy"

At last, if you have our project devices like the air quality sensor and wish to use our model to find where you are, run the following command on your edison : 

"opkg install mraa"

After all these commands have been done, you should be able to run all the python scripts in this directory without an error.




2. MySQL Database overview : 

If you feel like scanning the data stored in our data base, please run the following command : 

"mysql -u kuan -h iotdbinstance.cajidywjgjlk.us-east-1.rds.amazonaws.com -p iotdata"
The password is : "12345678"

We allocated our project data in three different tables, you can see the tables by typing following command :

"mysql> show tables;"

and it should look like this : 

+-------------------+
| Tables_in_iotdata |
+-------------------+
| Airinfo           |
| Airquality        |
| Dustinfo          |
+-------------------+
3 rows in set (0.04 sec)

In the first table "Airinfo", we stored all the testing set in it. If you run the python code "collection.py", the edison will collect the temperature, air quality and dust concentration data and upload into "Airinfo" table.

The second and third tables were used to store all our traning sets. In "Airquality table", we put temperature and air quality data collected from edison in it. As for "Dustinfo", we stored dust data used for training in it.

You can also view the data your edison just uploaded by typing : 

"select * from Airinfo;"

and you will see : 

mysql> select * from Airinfo;
+---------------+------+---------+-------------------+-------+---------------+----------+
| timestamp     | aq   | temp    | lowPulseOccupancy | ratio | concentration | category |
+---------------+------+---------+-------------------+-------+---------------+----------+
| 1494426568.86 |   93 |  23.422 |              NULL |  NULL |     280.02168 | room     |
| 1494426684.27 |  114 |  23.422 |              NULL |  NULL |       0.62000 | room     |
| 1494428030.14 |  124 |  19.261 |              NULL |  NULL |       0.62000 | outdoor  |
| 1494428340.55 |  122 |  20.378 |              NULL |  NULL |      39.23894 | outdoor  |
| 1494437370.62 |  121 |  23.583 |              NULL |  NULL |       0.62000 | indoor   |
| 1494437560.28 |  121 |  23.503 |              NULL |  NULL |       0.62000 | indoor   |
| 1494439412.09 |  123 |  23.987 |              NULL |  NULL |       0.62000 | indoor   |
                                        .
					.
					.
					.
					.
					.
These are the data used to evalute the machine learning model we trained. After all these stuff done, let's start our demo!!





3.Correlation coeffient and KNN machine learning model : 

First, let's see the correlation analysis for the coefficients between each two attributes from air quality, temperature, and dust concentration. If you would like to understand more about it,please refer to our weebly webpage "Detailed Description". To see the analysis, tun : 

"python Correlation_Analysis.py"

then you will realize the dependencies of the three atributes in different places.

Likewise, you can run the knn_centroid and knn_neighbors to test our models. These two models require three input arguments :  1. airquality (normally between 0 ~ 200)
			       2. temperature in Celcius
			       3. dust concentration (can be 0 ~ 10000, the range is broad)

For example, in the room I am staying when writing this Readme, Edison tells me the current air quality is 141, temperature is 25 degree, and dust concentration is 0.62 which I assume it to be 1 to become an integer. Then I run : 

"python knn_centroid.py 141 25 1", and it shows :
inddor reading room
Total time spent for analyzing : 1.47290682793 seconds

The output is correct !

Let's try another model knn_neighbors, just run : 
"python knn_neighbors.py 141 25 1", and it shows
The location is indoor reading room and confidence is :
0.909090909091

The model is very confident of this output, and it is also correct!!




4. User evaluation : 

To let user try this model on there own, we created "collection.py" and "evaluation.py". First, connect all the devices on your edison board. The following port number "must" be correct.
Air quality sensor : A1
Temperature sensor : A0
Dust sensor: D8

Then run "collection.py" on your edison terminal with one input argument indicates where you arenow (Note: It took dust sensor 30 seconds to finish its job, so you have to wait for a while):

"python collect_current.py indoor_reading_room"

Upon seeing "collection finished" displayd on edison's command line, the code has uploaded your data to MySQL database. Afterwards, go back to the directory on your computer and command : 

"python evaluation.py"

The evaluation model will retrieve the latest uploaded data and predict where the user is now.




