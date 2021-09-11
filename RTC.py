import sys
import time
import RPi.GPIO 


GPIO_I2C_Data = 3
GPIO_I2C_Clock = 5

I2C_CLOCK_PERIOD = 0.000005
I2C_WORD_BITS = 8

def I2C_Init():
    RPi.GPIO.setmode(RPi.GPIO.BOARD)
    RPi.GPIO.setup(GPIO_I2C_Data,RPi.GPIO.OUT,initial=1)
    RPi.GPIO.setup(GPIO_I2C_Clock,RPi.GPIO.OUT,initial=1)
    

def I2C_StartCom():
    RPi.GPIO.setup(GPIO_I2C_Data,RPi.GPIO.OUT)
    RPi.GPIO.output(GPIO_I2C_Data,0)
    time.sleep(I2C_CLOCK_PERIOD)
    RPi.GPIO.output(GPIO_I2C_Clock,0)
    time.sleep(I2C_CLOCK_PERIOD)

def I2C_EndCom():
    RPi.GPIO.setup(GPIO_I2C_Data,RPi.GPIO.OUT) 
    RPi.GPIO.output(GPIO_I2C_Clock,1)
    time.sleep(I2C_CLOCK_PERIOD)
    RPi.GPIO.output(GPIO_I2C_Data,1)
    time.sleep(I2C_CLOCK_PERIOD)

def I2C_ReadAck():
    RPi.GPIO.setup(GPIO_I2C_Data,RPi.GPIO.IN,pull_up_down=RPi.GPIO.PUD_UP)
    RPi.GPIO.output(GPIO_I2C_Clock,1)
    time.sleep(I2C_CLOCK_PERIOD)
    Ack = RPi.GPIO.input(GPIO_I2C_Data)
    RPi.GPIO.output(GPIO_I2C_Clock,0)
    time.sleep(I2C_CLOCK_PERIOD)
    RPi.GPIO.setup(GPIO_I2C_Data,RPi.GPIO.OUT)

    return Ack

def I2C_WriteAck(DataEndFlag):
    RPi.GPIO.setup(GPIO_I2C_Data,RPi.GPIO.OUT)
    if DataEndFlag == False:
        RPi.GPIO.output(GPIO_I2C_Data,0)
    else:
        RPi.GPIO.output(GPIO_I2C_Data,1)
    RPi.GPIO.output(GPIO_I2C_Clock,1)
    time.sleep(I2C_CLOCK_PERIOD)
    RPi.GPIO.output(GPIO_I2C_Clock,0)
    time.sleep(I2C_CLOCK_PERIOD)
    RPi.GPIO.setup(GPIO_I2C_Data,RPi.GPIO.IN,pull_up_down=RPi.GPIO.PUD_UP)

def I2C_SendReceiveData(Data, ReadByteCount = 0):
   ReceiveData = []

   I2C_StartCom()

   for DataWord in Data:
      BitMask = (1 << (I2C_WORD_BITS - 1))
      for Count in range(I2C_WORD_BITS):
         if (DataWord & BitMask) == 0:
            RPi.GPIO.output(GPIO_I2C_Data, 0)
         else:
            RPi.GPIO.output(GPIO_I2C_Data, 1)
         BitMask = BitMask / 2

         RPi.GPIO.output(GPIO_I2C_Clock, 1)
         time.sleep(I2C_CLOCK_PERIOD)
         RPi.GPIO.output(GPIO_I2C_Clock, 0)
         time.sleep(I2C_CLOCK_PERIOD)

      Ack = I2C_ReadAck()
#      print("DATA OUT: {:02X} ACK: {:02X}".format(DataWord, Ack))

   for ReadDataCount in range(ReadByteCount): 
      RPi.GPIO.setup(GPIO_I2C_Data, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
      DataWord = 0
      for Count in range(I2C_WORD_BITS):
         RPi.GPIO.output(GPIO_I2C_Clock, 1)
         time.sleep(I2C_CLOCK_PERIOD)

         I2C_ReadBit = RPi.GPIO.input(GPIO_I2C_Data)
         DataWord = DataWord * 2 + I2C_ReadBit

         RPi.GPIO.output(GPIO_I2C_Clock, 0)
         time.sleep(I2C_CLOCK_PERIOD)

      Ack = ((ReadDataCount + 1) == ReadByteCount)
      I2C_WriteAck(Ack)
#      print("DATA IN: {:02X} ACK: {:02X}".format(DataWord, Ack))

      ReceiveData.append(DataWord)

   I2C_EndCom()

   return ReceiveData

def Reset():
    RPi.GPIO.cleanup()

if __name__ == '__main__':

    DS1307_WRITE_TIME = [0,  [0xD0, 0x00]]
    DS1307_READ_TIME  = [3,  [0xD1]]
    print ('Program is starting....\n')
    I2C_Init()
    try:
      I2C_SendReceiveData(DS1307_WRITE_TIME[1])
      Result = I2C_SendReceiveData(DS1307_READ_TIME[1], DS1307_READ_TIME[0])
      sys.stdout.write("DS1307 TIME: {:02X}:{:02X}:{:02X}\n".format(Result[2], Result[1], Result[0]))
       
    except KeyboardInterrupt:
        Reset()