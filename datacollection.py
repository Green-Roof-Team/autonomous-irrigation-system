from time import sleep
import datetime
from UUGear import *
import sqlite3
import requests
import logging
from bs4 import BeautifulSoup

#logging initiaization
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='log.text',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(logging.StreamHandler())

loguugear = logging.getLogger('UUGEAR')
loginternet = logging.getLogger('Internet')
logdb = logging.getLogger('Database')

#UUGEAR Initialization
loguugear.info("Initalizing UUGEAR...")
UUGearDevice.setShowLogs(0)

#initalizing
def init_devices():
    devices = []
    deviceA = UUGearDevice(b'UUGear-Arduino-4465-6200')
    devices.append(["A", deviceA])
    deviceB= UUGearDevice(b'UUGear-Arduino-9800-2956')
    devices.append(["B", deviceB])
    deviceC = UUGearDevice(b'UUGear-Arduino-9151-5860')
    devices.append(["C", deviceC])
    return devices

#forcing device to reset
devices = init_devices()
for device in devices:
    device[1].detach()
    device[1].stopDaemon()
devices.clear()
devices = init_devices()
loguugear.info("Devices Initialized.")


#Weather Data Initialization
url = "https://www.google.com/search?q=weather+carbondale+il"
USER_AGENT = "Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.197 Safari/537.36"
LANGUAGE = "en, en-gb;q=0.8, en;q=0.7"

con = sqlite3.connect('sensor.db')
with con:
    #check if db exists
    c = con.cursor()
    c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='sensordata';")
    if c.fetchone()[0] < 1 : 
        c.execute("CREATE TABLE sensordata(timestamp DATETIME, sensor TEXT, value REAL, voltage REAL, temperature TEXT, weather TEXT, precipitation TEXT, humidity TEXT, wind_speed TEXT);") 
        logdb.info("Sensordata table created")
    c.close()
    logdb.info("Connected to database. Data collection beginning...")

    while True:
        #use this section to get weather data
        with requests.Session() as session:
            session.headers['User-Agent'] = USER_AGENT
            session.headers['Accept-Language'] = LANGUAGE
            session.headers['Content-Language'] = LANGUAGE
            try:
                html = session.get(url)
                # create a new soup
                soup = BeautifulSoup(html.text, "html.parser")
            except Exception as e:
                loginternet.debug(e)
                #print("L+ratio")
                #raise ConnectionError(e
                #continue
                #raise SystemExit(e)
                
            # create a new soup
            # soup = BeautifulSoup(html.text, "html.parser")
            #print(soup.prettify())
            try:
                current_temp = soup.find("span", attrs={"id": "wob_tm"}).text
                current_temp = current_temp + "° F"
                current_weather = soup.find("span", attrs={"id": "wob_dc"}).text
                precipitation = soup.find("span", attrs={"id": "wob_pp"}).text
                humidity = soup.find("span", attrs={"id": "wob_hm"}).text
                wind_speed = soup.find("span", attrs={"id": "wob_ws"}).text
            except Exception as e:
                loginternet.debug("Rate limited. Skipping weather data for this iteration..")
                current_temp = None
                current_weather = None
                precipitation = None
                humidity = None
                wind_speed = None
            
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
                    name = devicename + str(i-2)
                    value = float(device.analogRead(i))
                    voltage = float((device.analogRead(i)/1023.0)*3.3)
                    inserted = (date, name, value, voltage, current_temp, current_weather, precipitation, humidity, wind_speed)
                    logdb.debug(f"{name}: {inserted}")
                    c.execute("INSERT INTO sensordata VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", inserted)
                c.close()
                con.commit()
            else:
                loguugear.debug(f"{d[0]} was unable to connect")
        sleep(300)
























