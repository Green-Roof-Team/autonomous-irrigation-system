import serial
import re
#import time
ports = ["/dev/ttyACM0", "/dev/ttyACM1", "/dev/ttyACM2", "/dev/ttyACM3"]
baud = 9600
for port in ports:
    try:
        arduino_port = port
        ser = serial.Serial(port, baud)
        break
    except serial.serialutil.SerialException as e:
        pass
#arduino_port = "/dev/ttyACM0" #serial port of Arduino
#baud = 9600 #arduino uno runs at 9600 baud
fileName="analog-data.csv" #name of the CSV file generated
#ser = serial.Serial(arduino_port, baud)
print("Connected to Arduino port:" + arduino_port)
file = open(fileName, "a") #appends
print("Created file")

while True:
    getData=str(ser.readline())
    data=getData[0:][:-2]
    data2 = re.findall('\d', data)
    print(data2[0])
    file = open(fileName, "a")
    file.write(data2[0]) #write data with a newline 
