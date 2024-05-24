# Autor: Erik Vinueza Orbea
# 21.05.2024

import time
from threading import Thread, Event
try:
 import RPi.GPIO as GPIO
except ImportError:
 import SimulRPi.GPIO as GPIO
#import RPi.GPIO as GPIO

#Class Motor definieren
class StepMotor:
    def __init__(self, motorStepPin, motorDirPin):
        self.motorStepPin = motorStepPin        #Pin Nummer des Motors für die Steps ausgaben
        self.motorDirPin = motorDirPin          #Pin Nummer des Motors für die Richtung 0 => dir_pin=low  1 => dir_pin=high
        self.stepPeriod = 2500                  #Dauer eines Schrittes in us
        self.stop_requested = Event()           # Event to signal stop


        # Initialisierung der GPIO-Pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(motorStepPin, GPIO.OUT)
        GPIO.setup(motorDirPin, GPIO.OUT)
        
        
    def setFrequencyInHz(self, frequency):
       self.stepPeriod = (10000)/(4*frequency)            #Frequenz in Hz und Period in us
    
    def setSpeedInMPS(self, velocity):
       self.stepPeriod = (10000)/(28*velocity)           #velocity in m/s und Peruid in us   


    def start_steps(self, stepsNr, dir):
        self.stop_requested.clear()
        self.thread = Thread(target=self.makeSteps, args=(stepsNr, dir))
        self.thread.start()
 
         
    def makeSteps(self, stepsNr, dir):
        # Set direction
        GPIO.output(self.motorDirPin, dir)
        # Move the motor the specified number of steps
        for steps in range(stepsNr):
            if self.stop_requested.is_set():
                break  # Exit the loop if stopping is requested
            print(f"motor up, step: {steps + 1}")
            GPIO.output(self.motorStepPin, GPIO.HIGH)
            time.sleep(self.stepPeriod / 2000000)  # The function has seconds as input
            GPIO.output(self.motorStepPin, GPIO.LOW)
            time.sleep(self.stepPeriod / 2000000)  # There are two delays, hence only half the period
    

          
    def stop_motor(self):
        self.stop_requested.set()
        if self.thread:
            self.thread.join()
        print("Motor stop requested.")

    def reset_stop_request(self):
        self.stop_requested.clear()

    
   
    
class BrushMotor:
    def __init__(self, pwm_pin, dir_pin_1):
        self.pwm_pin = pwm_pin
        self.dir_pin_1 = dir_pin_1
        self.speed = 0
        self.is_active = False
        
        # Initialisierung der GPIO-Pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pwm_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin_1, GPIO.OUT)
        
        # PWM-Objekt für die Geschwindigkeitssteuerung
        self.pwm = GPIO.PWM(self.pwm_pin, 100)  # 100 Hz PWM
        self.pwm.start(0)  # Start PWM with 0% duty cycle

    def setSpeedPercent(self, value):
        # Setze Geschwindigkeit
        self.speed = value
    
    def move(self, direction):
        # Setze Richtung
        self.is_active = True
        GPIO.output(self.dir_pin_1, direction)
        self.pwm.ChangeDutyCycle(self.speed)
        
    def stop(self):
      self.pwm.ChangeDutyCycle(0)
