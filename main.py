from modules import *
from multiprocessing import Process, Queue
import test_distances as test
try:
    import RPi.GPIO as GPIO
except ImportError:
    import SimulRPi.GPIO as GPIO
import time

def get_and_unpack_data(incoming: Queue, outgoing: Queue):
   datastream = DataStream()

   while(True):   # Simulates incoming data from Arduino
      data = incoming.get()
      #print(data)
      unpacked_data = datastream.unpack_arduino_data(data)
      outgoing.put(unpacked_data)
      
if __name__ == '__main__':
   #vw = Verfahrwege()
   #vw.x_step.move(100,"Left", 120)
   
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21, GPIO.OUT)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
    GPIO.output(16, False)
    for i in range(10000):
        GPIO.output(21, True)
        print(f"Step: --- {i+1} ---")
        time.sleep(1)
        GPIO.output(21, False)
        time.sleep(1)
   
''' 
   processhandler = ProcessHandler()
   incoming = processhandler.memory()
   outgoing = processhandler.memory()

   processhandler.start_process(test.get_test_distance_data, incoming)
   processhandler.start_process(get_and_unpack_data, incoming, outgoing)

   while(True):
      print(outgoing.get())
'''



