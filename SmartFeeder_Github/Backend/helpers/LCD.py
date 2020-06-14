import time
from RPi import GPIO
class lcd:

    def __init__(self,E,RS,shift):
        self.E = E
        self.RS = RS
        self.shift = shift

    def send_instruction(self, value):
        #rs low -> aangeven dat het over een instructie gaat
        GPIO.output(self.RS,GPIO.LOW)
        #e high
        GPIO.output(self.E,GPIO.HIGH)
        #bits klaarzetten
        self.set_data_bits(value)
        #e low -> zodat bit ingelezen wordt
        GPIO.output(self.E,GPIO.LOW)
        time.sleep(0.0001)

    def send_character(self, value):
        #rs high -> gaat om een data input
        GPIO.output(self.RS,GPIO.HIGH)
        GPIO.output(self.E,GPIO.HIGH)
        #bits klaarzetten
        self.set_data_bits(value)
        #e low -> zodat bit ingelezen wordt
        GPIO.output(self.E,GPIO.LOW)
        time.sleep(0.0001)

    def init_lcd(self):
        #0 instructie clear display en cursor home
        self.send_instruction(1)
        #15 instructie -> Display on, cursor on, cursor blink
        self.send_instruction(15)
        #56 instructie -> 8bit datalength, 2 line display, character font
        self.send_instruction(56)

    def set_data_bits(self, byte):
        mask = 1
        #8 bits overlopen -> 1 byte
        for i in range(0,8):
            #kijken of het een 1 is
            if byte & (mask << i):
                #1 bit schrijven
                self.shift.write_one_bit(1)
            else:
                #0 bit schrijven
                self.shift.write_one_bit(0)
        #print("------ End byte ------")
        self.shift.copy_to_storage_register()

    def write_message(self, message):
        teller = 0
        #elk karakter in de message overlopen
        for char in message:
            #ascii waarde van karakter ophalen
            char = ord(char)
            #ascii waarde doorsturen naar lcd
            self.send_character(char)
            
            # teller om van lijn te veranderen
            teller = teller +1
            if teller == 16:
                #instructie om van lijn teveranderen
                self.send_instruction(168)
