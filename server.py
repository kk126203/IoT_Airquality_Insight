from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
from dateutil import tz
import csv,sqlite3,pymysql,requests,ast,pprint,sys,SocketServer,json,requests,ast
pymysql.install_as_MySQLdb()
import MySQLdb


database = MySQLdb.connect(host = "palmos.cddqndcuappw.us-east-1.rds.amazonaws.com",
                    user = "KuanSheng",
                    passwd = "12345678",
                    db = "test"
)
link = "http://api.wunderground.com/api/ca8aaa2c20713339/conditions/q/MA/Somerville.json"
cur = database.cursor()


class S(BaseHTTPRequestHandler):
    
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        print('catch get request')
        self._set_headers()
        self.wfile.write("<html><body><h1>hi!</h1></body></html>")

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print("Get message : "+post_data)    
        self._set_headers()
        self.wfile.write("ack sent!!")  
        print("Ack send back to server")
        if(post_data[0]=='H'):
            print("hand shake completed")
        else:

            # Data from Adafruit IoT parts
            list_data = post_data.split()     
            t1 = list_data[0]       

            from_zone = tz.gettz('UTC')                   ##convert UTC time to local time begins
            to_zone = tz.gettz('America/New_York')
            import datetime as dd
            date = dd.datetime.strptime(t1, '%Y%m%d%H%M%S')
            utc = date.replace(tzinfo=from_zone)
            central = utc.astimezone(to_zone)
            datetime = central.strftime('%Y%m%d%H%M%S')   ##date time conversion end
            
            temp = list_data[1]
            temp = temp[:-2]        ## data processing to decimal 2
            humi = list_data[2]
            humi = humi[:-2]        ## the same
            row_x = list_data[3]    ## deal with 0.-xxx problem 
            axis_x = self.parse_axis(row_x)
            row_y = list_data[4]
            axis_y = self.parse_axis(row_y)
            row_z = list_data[5]
            axis_z = self.parse_axis(row_z)
            latitude = list_data[6]
            longitude = list_data[7]
            height = list_data[8]
            cur.execute("""insert into adafruit_data_office (datetime, latitude, longitude, height, temperature, humidity, axis_x, axis_y, axis_z)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", (datetime, latitude, longitude, height, temp, humi, axis_x, axis_y, axis_z))
            database.commit()
            
            
            # Data from Open source WeatherUndergrounde
            file = requests.get(link)
            d = ast.literal_eval(file.text)
            d = d['current_observation']
            city = d['display_location']['city']
            status = d['icon']
            feel = d['feelslike_f']
            real_temp = d['temp_f']
            precip_1hr = d['precip_1hr_in']
            precip_today = d['precip_today_in']
            humidity = d['relative_humidity']
            wind_degree = d['wind_degrees']
            wind_dir = d['wind_dir']
            wind_gust = d['wind_gust_mph']
            wind = d['wind_mph']
            visibility = d['visibility_mi']
            pressure = d['pressure_in']
            cur.execute("""insert into Open_Source_office (datetime, city, status, feel, real_temp, precip_1hr, precip_today, humidity, wind_degree, wind_dir, wind_gust, wind, visibility, pressure) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""",(datetime,city,status,feel,real_temp,precip_1hr,precip_today,humidity,wind_degree,wind_dir,wind_gust,wind,visibility,pressure))
            database.commit()

            time1 = datetime[8:]
            print("Data upload to Palmos database succeeded at "+time1)
            
        
    def parse_axis(self, s):
        m = -1
        for i in range (0, len(s)):
            if s[i]=='-':
                m = i
                break;
        if m==-1:
            return s
        a = s[:i]
        b = s[i+1:]
        c = '-'+a+b
        return c

                
def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
