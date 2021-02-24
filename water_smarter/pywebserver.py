from flask import Flask
import serial
import re

arduino_port = "/dev/ttyACM1" #serial port of Arduino
baud = 9600 #arduino uno runs at 9600 baud

ser = serial.Serial(arduino_port, baud)
getData=str(ser.readline())
data=getData[0:][:-2]

data2 = re.findall('\d', data)
str2 = str(data2[0])
print(data2[0]);

app = Flask(__name__)
@app.route('/')

def index():
   str = "Smarter Water "+ str2
   return str

if __name__ == '__main__':
   app.run(debug=False, host='0.0.0.0')
