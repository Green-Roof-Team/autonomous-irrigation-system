from time import sleep
import datetime
from UUGear import *
import sqlite3
import requests
from bs4 import BeautifulSoup

#UUGEAR Initialization
print("Initalizing...")
UUGearDevice.setShowLogs(0)

devices = []
deviceA = UUGearDevice(b'UUGear-Arduino-4465-6200')
devices.append(["A", deviceA])
print("Added Device A")
deviceB= UUGearDevice(b'UUGear-Arduino-9800-2956')
devices.append(["B", deviceB])
print("Added Device B")
deviceC = UUGearDevice(b'UUGear-Arduino-9151-5860')
devices.append(["C", deviceC])
print("Added Device C")

for device in devices:
    device[1].detach()
    device[1].stopDaemon()

#Weather Data Initialization
url = "https://www.google.com/search?q=weather+carbondale+il"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43"
LANGUAGE = "en, en-gb;q=0.8, en;q=0.7"

con = sqlite3.connect('sensorad.db')
with con:
    #check if db exists
    c = con.cursor()
    c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='sensordata';")
    if c.fetchone()[0] < 1 : 
        c.execute("CREATE TABLE sensordata(timestamp DATETIME, sensor TEXT, value REAL, voltage REAL);") 
    c.close()

    while True:
        #use this section to get weather data
        with requests.Session() as session:
            session.headers['User-Agent'] = USER_AGENT
            session.headers['Accept-Language'] = LANGUAGE
            session.headers['Content-Language'] = LANGUAGE
            html = session.get(url)
            # create a new soup
            soup = BeautifulSoup(html.text, "html.parser")
            current_temp = soup.find("span", attrs={"id": "wob_tm"}).text
            current_weather = soup.find("span", attrs={"id": "wob_dc"}).text
            precipitation = soup.find("span", attrs={"id": "wob_pp"}).text
            humidity = soup.find("span", attrs={"id": "wob_hm"}).text
            wind_speed = soup.find("span", attrs={"id": "wob_ws"}).text

        #use this section to get data from sensehat

        #use this section to get data from sensors
        for d in devices:
            device = d[1]
            if device.isValid():
                # EXTERNAL REFERENCE
                device.analogReference(1)
                devicename = d[0]
                c = con.cursor()
                date = datetime.datetime.now()
                for i in range(3,13):
                    name = devicename + str(i+1)
                    print(name)
                    value = float(device.analogRead(i))
                    voltage = float((device.analogRead(i)/1023.0)*3.3)
                    inserted = (date, name, value, voltage)
                    print(inserted)
                    c.execute("INSERT INTO sensordata VALUES (?, ?, ?, ?);", inserted)
                c.close()
                con.commit()
        
        sleep(300)



            



#con = sqlite3.connect('sensor.db')

#could probably use multithreading to get data from all arduinos at once
#device = UUGearDevice(b'UUGear-Arduino-9800-2956')
#con = sqlite3.connect('sensor.db')

with con:
    #check if db exists
    c = con.cursor()
    c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='sensordata';")
    if c.fetchone()[0] < 1 : 
        c.execute("CREATE TABLE sensordata(timestamp DATETIME, sensor TEXT, value REAL, voltage REAL);")


    if device.isValid():
        # EXTERNAL REFERENCE
        device.analogReference(1)
        devicename = "A"
        date = datetime.datetime.now()
        #data collecting: sensorname, timestamp, sensorvalue, sensorvoltage

        #iterating through all the pins
        for i in range(0,10):
            name = devicename + str(i+1)
            print(name)
            value = float(device.analogRead(i))
            voltage = float((device.analogRead(i)/1023.0)*3.3)
            inserted = (date, name, value, voltage)
            print(inserted)
            c.execute("INSERT INTO sensordata VALUES (?, ?, ?, ?);", inserted)
	


