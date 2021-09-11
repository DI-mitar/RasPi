import RPi.GPIO as GPIO
import time




O_Watchdog = 11 #this pin is for testing purpose

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(O_Watchdog,GPIO.OUT)
    GPIO.output(O_Watchdog,GPIO.LOW)

def Watchdog():
    while True:
        GPIO.output(O_Watchdog,GPIO.HIGH)   
        time.sleep(5)
        GPIO.output(O_Watchdog,GPIO.LOW)
        time.sleep(5)

def Reset():
    GPIO.cleanup()

if __name__ == '__main__':
    print ('Program is starting....\n')
    setup()
    try:
        Watchdog()
    except KeyboardInterrupt:
        Reset()

    
