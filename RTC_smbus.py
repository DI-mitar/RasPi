import RPi.GPIO as GPIO
import time
import smbus
import datetime
import os


def CheckInternetConnectivity():
   Command = "ping -c 1 google.com"
   r = os.system(Command)
   if r == 512:
      print("Raspberry py has no interntion connection")
   else:
      print("Raspberry py is connected to internet")


# Read time from RTC in String
def ReadTimeFromRTC(Address,Register):
   bus = smbus.SMBus(1)
   time = bus.read_i2c_block_data(Address,Register,7)
   time[0] = time[0]&0x7F
   time[1] = time[1]&0x7F
   time[2] = time[2]&0x3F
   time[3] = time[3]&0x07
   time[4] = time[4]&0x3F
   time[5] = time[5]&0x7F
  

   strTime = "20%x-%x-%x %x:%x:%x" %(time[6],time[5],time[4],time[2],time[1],time[0])
   return strTime

#t = ReadTimeFromRTC(0x68,0x00)

def WriteTimeToRTC(Address,Register,Time):
   bus = smbus.SMBus(1)
   bus.write_i2c_block_data(Address,Register,Time)

def ReadTimeFromSystem():
   time = datetime.datetime.now()
   year = int(time.strftime("%Y"),16)
   month = int(time.strftime("%m"),16)
   date = int(time.strftime("%d"),16)
   hour = int(time.strftime("%H"),16)
   minute = int(time.strftime("%M"),16)
   second = int(time.strftime("%S"),16)
   arrTime = [second,minute,hour,0,date,month,year]
   strTime ="%x-%x-%x %x:%x:%x" %(year,month,date,hour,minute,second)

   return (arrTime,strTime)

def WriteTimeToSystem(Time):
   os.system("sudo date -s '%s'"%(Time))


WriteTimeToRTC(0x68,0x00,[0x05,0x05,0x08,0x04,0x12,0x08,0x21])




while True:
   rtctime = ReadTimeFromRTC(0x68,0x00)
   print("RTC:   ",rtctime)
   arrSystemtime,strSystemtime = ReadTimeFromSystem()
   print("System:",strSystemtime)
   time.sleep(1)


"""
while True:
   arrSystemtime,strSystemtime = ReadTimeFromSystem()
   print("System:",strSystemtime)
   WriteTimeToRTC(0x68,0x00,arrSystemtime)
   rtctime = ReadTimeFromRTC(0x68,0x00)
   print("RTC:   ",rtctime)
   time.sleep(1)


#StringTime="sudo date -s '2019-08-08 20:20:20'"
#os.system(StringTime)




Now = datetime.datetime.now()
print(Now)
hour = Now.strftime("%H")

int_hour = int(hour,16)
hex_hour = hex(int_hour)
#print(hex_hour)



SetTime="2021-01-01/20:20:20"

Object_SetTime = datetime.datetime.strptime(SetTime, "%Y-%m-%d/%H:%M:%S")




Address = 0x68
Register = 0x00
NowTime = [0x00,0x00,0x08,0x04,0x12,0x08,0x21]
w = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
bus = smbus.SMBus(1)

def SetTime():
   bus.write_i2c_block_data(Address,Register,NowTime)

def ReadTime():
   return bus.read_i2c_block_data(Address,Register,7)

SetTime()

t = ReadTime()
t[0] = t[0]&0x7F
t[1] = t[1]&0x7F
t[2] = t[2]&0x3F
t[3] = t[3]&0x07
t[4] = t[4]&0x3F
t[5] = t[5]&0x1F
print ("20%x-%x-%x %x:%x:%x %s" %(t[6],t[5],t[4],t[2],t[1],t[0],w[t[3]-1]))
"""


    


   

    
