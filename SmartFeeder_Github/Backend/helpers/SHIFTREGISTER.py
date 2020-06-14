import time
from RPi import GPIO

class shiftregister:
    def __init__(self,DS,OE,STCP,SHCP,MR):
        self.DS = DS
        self.OE =OE
        self.STCP =STCP
        self.SHCP = SHCP
        self.MR = MR

    def init_shift_register(self):
        # mr low -> cleanen
        GPIO.output(self.MR, GPIO.LOW)
        time.sleep(0.01)
        # mr high -> om terug te kunnen schrijven
        GPIO.output(self.MR, GPIO.HIGH)
        # enable output
        GPIO.output(self.OE, GPIO.LOW)
        #print("init_shift_register finished")

    # bit naar shiftregister
    def write_one_bit(self, bit):
        #Data input (welke bit moet geschreven worden)
        GPIO.output(self.DS,bit)
        #Clockpulse
        GPIO.output(self.SHCP,1)
        time.sleep(0.01)
        GPIO.output(self.SHCP,0)

    def copy_to_storage_register(self):
        GPIO.output(self.STCP, GPIO.HIGH)
        GPIO.output(self.STCP, GPIO.LOW)