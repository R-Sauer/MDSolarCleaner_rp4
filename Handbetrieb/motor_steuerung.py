# Autor: Erik Vinueza Orbea
# 29.05.2024

import time
from threading import Thread, Event

try:
 import RPi.GPIO as GPIO
except ImportError:
 import SimulRPi.GPIO as GPIO
#import RPi.GPIO as GPIO

#Class Motor definieren
class StepMotor:
    def __init__(self, motorStepPin, motorDirPin, endStopPin1, endStopPin2):
        self.motorStepPin = motorStepPin        #Pin Nummer des Motors für die Steps ausgaben
        self.motorDirPin = motorDirPin          #Pin Nummer des Motors für die Richtung 0 => dir_pin=low  1 => dir_pin=high
        self.endStopPin1 = endStopPin1          #Pin für Endstopschalter1
        self.endStopPin2 = endStopPin2          #Pin für Endstopschalter2
        self.stop_requested = Event()           # Event to signal stop
        self.initStepPeriod = 2500              #Dauer eines Schrittes in us -> 1Hz -> 0,14 m/s
        self.stepPeriod = self.initStepPeriod
        self.currentStepPeriod = self.initStepPeriod                  
        self.totalSteps = 0                     #Anzahl der gelaufende steps
        self.totalDistanceInCm = self.totalSteps/28         
        
        # Initialisierung der GPIO-Pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(motorStepPin, GPIO.OUT)
        GPIO.setup(motorDirPin, GPIO.OUT)
        GPIO.setup(endStopPin1, GPIO.IN)
        GPIO.setup(endStopPin2, GPIO.IN)
          
    def makeSteps(self, stepsNr, dir):
       #Setze Richtung
       GPIO.output(self.motorDirPin, dir)
       self.stop_requested.clear()
       #neu Initializierung von currentStepPeriod für Anfahrgeschwindigkeit
       self.currentStepPeriod = self.initStepPeriod  
       #Bewegung des Motors in die angegebene Schritte
       for _ in range (stepsNr):
          #Nothaltfunktion
          if self.stop_requested.is_set():
                break  # Exit the loop if stopping is requested
          #Endstopsauswertung
          #if ((GPIO.input(self.endStopPin1) != GPIO.HIGH) & (dir == 1)) | ((GPIO.input(self.endStopPin2) != GPIO.HIGH) & (dir == 0)):
          #   break
          #Schritte machen
          GPIO.output(self.motorStepPin, GPIO.HIGH)
          time.sleep(self.currentStepPeriod/2000000)           #Die Funktion hat Sekunde als input
          GPIO.output(self.motorStepPin, GPIO.LOW)
          time.sleep(self.currentStepPeriod/2000000)            #Es gibt zwei Delays und deswegen nur halbe Periode
          #Anfahrgeschwindigkeit anpassen
          if(self.currentStepPeriod > self.stepPeriod):
              self.currentStepPeriod = self.currentStepPeriod - 3
          #Schritte zählen
          if(dir == 0):
             self.totalSteps =+ 1
          if(dir == 1):
            self.totalSteps =- 1
            
    def moveInCm(self, distanceInCm, dir):
        self.makeSteps(distanceInCm*28,dir)
    
    def start_steps(self, stepsNr, dir):
        self.stop_requested.clear()
        self.thread = Thread(target=self.moveInCm, args=(stepsNr, dir))
        self.thread.start()

    def stop_motor(self):
        self.stop_requested.set()
        if self.thread:
            self.thread.join()
        print("Motor stop requested.")

    def reset_stop_request(self):
        self.stop_requested.clear()

    def setFrequencyInHz(self, frequency):
       self.stepPeriod = (10000)/(4*frequency)            #Frequenz in Hz und Period in us
    
    def setSpeedInMPS(self, velocity):
       self.stepPeriod = (10000)/(28*velocity)           #velocity in m/s und Period in us
    
    def getSteps(self):
        return self.totalSteps
    
    def getDistanceInCm(self):
       return self.totalDistanceInCm
    
class BrushMotor:
    def __init__(self, pwm_pin):
        self.pwm_pin = pwm_pin
        self.speedInPercent = 0          #kann Werte zwischen -100 und 100 haben. Vorzeichnen bestimmt die Richtung
        self.dutyCycle = self.speedInPercent*0.168 + 55.6  #Tastenverhältnis kann Werte zwischen 0 und 100 haben
        self.direction = 0 # diese Attribute ist nicht verwendet
        self.is_active = False
        
        # Initialisierung der GPIO-Pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pwm_pin, GPIO.OUT)
        
        # PWM-Objekt für die Geschwindigkeitssteuerung
        self.pwm = GPIO.PWM(self.pwm_pin, 1000)  # 100 Hz PWM
        self.pwm.start(0)  # Start PWM with 0% duty cycle (Tastenverhältnis von 0)

    def setSpeedPercent(self, value):
        # Setze Geschwindigkeit in Procent zwischen -100 und 100
        self.speedInPercent = float(value)
        self.dutyCycle = self.speedInPercent*0.168 + 55.6
        print("duty cycle : " , self.dutyCycle)
    
    def move(self):
        self.is_active = True
        self.pwm.ChangeDutyCycle(self.dutyCycle)
        
    def stop(self):
      self.pwm.ChangeDutyCycle(55.6)
      
    def getSpeedInPercent(self):
        return self.speedInPercent
     
