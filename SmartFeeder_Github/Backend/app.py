from repositories.DataRepository import DataRepository
from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS

import RPi.GPIO as GPIO
import time, signal, sys, mysql.connector, threading
from datetime import datetime
from subprocess import check_output

from helpers.LCD import lcd
from helpers.SHIFTREGISTER import shiftregister
from helpers.HX711 import HX711

############### GPIO instellinegn ###############
time.sleep(5)
GPIO.setwarnings(False)
# use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BCM)

########## set GPIO Pins ##########
pinTrigger = 18
pinEcho = 24
IR1 = 19
IR2 = 26

HXdata = 12
HXclk = 16

Servo = 23

# shiftregister
DS = 13
OE = 6
STCP = 5
SHCP = 22
MR = 27
#lcd
rs = 20
E = 21
    
###### set GPIO input and output channels #####
GPIO.setup(pinTrigger, GPIO.OUT)
GPIO.setup(pinEcho, GPIO.IN)
GPIO.setup(IR1, GPIO.IN)
GPIO.setup(IR2, GPIO.IN)

GPIO.setup(Servo,GPIO.OUT)

###### Objecten van klasses maken ######
shiftObj = shiftregister(DS, OE, STCP, SHCP, MR)
lcdObj = lcd(E, rs, shiftObj)
hx = HX711(HXdata, HXclk)
pwm=GPIO.PWM(Servo, 50)

###### Nodige processen voor HX711 ######
err = hx.zero()# Nieuwe tare
hx.set_scale_ratio(821.2888888888889)  # ratio van scale
VoederLoop = True

def SetAngle(duty):
    GPIO.output(23,True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(23, False)
    pwm.ChangeDutyCycle(0)

def ServoBeweging():
    SetAngle(3)
    SetAngle(4.5)
    SetAngle(3)

def Voeden_loop(gewicht):
    print("voederloop gestart")
    pwm.start(0)
    VoederLoop = True
    while VoederLoop==True:
        meting = round(hx.get_weight_mean(10),2)
        print(meting, 'g')
        if meting < gewicht:
            print("servo")
            ServoBeweging()
        else:
            VoederLoop=False
        time.sleep(0.5)
    pwm.stop()
    meting = round(hx.get_weight_mean(10),2)
    datum = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    DataRepository.create_meting('4', 'PORTIE', '0000000000', meting, datum)
    time.sleep(60)

def Maak_dict_voedermomenten():
    voedermomenten = {}
    data = DataRepository.read_voedermomenten()
    for x in data:
        uur_lang = x.get('Uur')
        uur = uur = uur_lang[:-3]
        gewicht = x.get('Gewicht')
        voedermomenten[uur] = gewicht
    return voedermomenten

def Voederloop_databank_trigger():
    while True:
        nu = datetime.now()
        minuut = str(nu.minute)
        uur_nu =f'{nu.hour}:{minuut.zfill(2)}'
        dict_voedermomenten = Maak_dict_voedermomenten()
        print(uur_nu)
        print(dict_voedermomenten)
        if uur_nu in dict_voedermomenten.keys():
            portie = dict_voedermomenten.get(uur_nu)
            Voeden_loop(portie)
        print("hello")
        time.sleep(5)

def lcd_setup():
    print("setup starten")
    GPIO.setup(STCP,GPIO.OUT)
    GPIO.setup(SHCP,GPIO.OUT)
    GPIO.setup(MR,GPIO.OUT)
    GPIO.setup(DS,GPIO.OUT)
    GPIO.setup(OE,GPIO.OUT)

    GPIO.setup(rs,GPIO.OUT)
    GPIO.setup(E,GPIO.OUT)

    #init's runnen
    shiftObj.init_shift_register()
    lcdObj.init_lcd()

def schrijven_op_lcd():
    print("Tekst op lcd")
    #ip adressen ophalen via command
    adressen_string = str(check_output(['hostname','--all-ip-addresses']))
    #overbodige tekens uit de string halen
    adressen_string = adressen_string.replace("n","")
    adressen_string = adressen_string.replace("b","")
    adressen_string = adressen_string.replace("'","")
    #ipv6 weghalen (zorgt voor slechte weergave)
    adressen_string = adressen_string[0:25]
    adressen_string = "IP: "+adressen_string
    # ip weergeven op lcd

    lcdObj.write_message(adressen_string)

def Sensoren():
    while True:
        # set Trigger to HIGH
        GPIO.output(pinTrigger, True)
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(pinTrigger, False)

        startTime = time.time()
        stopTime = time.time()

        #Waarden van IR sensoren ophalen
        IR1_waarde = int(not GPIO.input(IR1))
        IR2_waarde = int(not GPIO.input(IR2))

        # save start time
        while 0 == GPIO.input(pinEcho):
            startTime = time.time()

        # save time of arrival
        while 1 == GPIO.input(pinEcho):
            stopTime = time.time()

        # time difference between start and arrival
        TimeElapsed = stopTime - startTime
        # vermenigvuldigen met Sonic speed (34300 cm/s)
        # gedeelt door 2, want het signaal gaat door en komt terug
        distance = TimeElapsed * 34300 / 2
        percent = round(100-((distance-2)/25*100))
        datum = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print (f"Distance: {percent}% en de datum is {datum}")
        time.sleep(0.5)

        DataRepository.create_meting('1', 'WATER', '0000000000', percent, datum)
        DataRepository.create_meting('2', 'VOEDING', '0000000000', IR1_waarde, datum)
        DataRepository.create_meting('3', 'VOEDING', '0000000000', IR2_waarde, datum)
        print("records were inserted.")

        time.sleep(900)

lcd_setup()
schrijven_op_lcd()


voederloop_trigger = threading.Thread(target=Voederloop_databank_trigger)
voederloop_trigger.start()

# Sensoren_uitlezen = threading.Thread(target=Sensoren)
# Sensoren_uitlezen.start()


# ------------------------------------------------------   FLASK   -----------------------------------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Secret Key'

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# API ENDPOINTS
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

@app.route('/water', methods=['GET'])
def water():
    data = DataRepository.read_water()
    return jsonify(water = data),200

@app.route('/voeding', methods=['GET'])
def IR():
    data = DataRepository.read_IR()
    return jsonify(voeding = data),200

@app.route('/portie', methods=['GET'])
def portie():
    data = DataRepository.read_portie()
    return jsonify(portie = data),200

@app.route('/porties', methods=['GET'])
def porties():
    data = DataRepository.read_porties()
    return jsonify(porties = data),200

@app.route('/voedermomenten', methods=['GET', 'POST'])
def voedermomenten():
    if request.method == 'GET':
        data = DataRepository.read_voedermomenten()
        return jsonify(voedermomenten = data),200
    elif request.method == 'POST':
        gegevens = DataRepository.json_or_formdata(request)
        nieuw_id = DataRepository.create_voedermoment(
            gegevens['FeederCode'], gegevens['Uur'], gegevens['Gewicht'])
    return jsonify(voedermomentid=nieuw_id), 201

@app.route('/voedermoment/<voedermomentid>', methods=['GET', 'PUT', 'DELETE'])
def get_voedermoment(voedermomentid):
    if request.method == 'GET':
        return jsonify(DataRepository.read_voedermoment(voedermomentid))
    # elif request.method == 'PUT':
    #     gegevens = DataRepository.json_or_formdata(request)
    #     data = DataRepository.update_trein(gegevens['vertrek'], gegevens['bestemmingID'],
    #                                        gegevens['spoor'], gegevens['vertraging'], gegevens['afgeschaft'], trein_id)
    #     print(data)
    #     return jsonify(trein_id=trein_id), 200
    elif request.method == 'DELETE':
        data = DataRepository.delete_voedermoment(voedermomentid)
        if data > 0:
            return jsonify(status="success", row_count=data), 201
        else:
            return jsonify(status="no update", row_count=data), 201



if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')

