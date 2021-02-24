import serial
import re
#import time

arduino_port = "/dev/ttyACM1" #serial port of Arduino
baud = 9600 #arduino uno runs at 9600 baud
fileName="analog-data.csv" #name of the CSV file generated

ser = serial.Serial(arduino_port, baud)
print("Connected to Arduino port:" + arduino_port)
file = open(fileName, "a") #appends
print("Created file")

while True:
    getData=str(ser.readline())
    data=getData[0:][:-2]

    data2 = re.findall('\d', data)
    print(data2[0]);

    file = open(fileName, "a")
    file.write(data2[0]) #write data with a newline
