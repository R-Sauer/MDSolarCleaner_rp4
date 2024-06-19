# author: Raphael Sauer
# mailto: raphael.sauer@haw-hamburg.de
# date: 06/2024

import multiprocessing as mp
from SerialReadToDB_FSM import *
from solarCleanerDB import Database
import time
from Handbetrieb import handbetrieb

SERIAL_BAUD = 115200
SENSOR_FIELDS = ["brush1_rpm", "brush2_rpm", "current_mA"]
PERSIST_DATABASE = False

### Setup and execution of separate processes

if __name__ == '__main__':
    try:
        databasePath = './sandUp_Logging_DB.db'
        if not PERSIST_DATABASE:
            Database(databasePath).deleteDatabase()

        serConn1, serConn2 = mp.Pipe()
        sensorProcess = mp.Process(target=serialReceiveFSM, args=[databasePath, SENSOR_FIELDS, SERIAL_BAUD, serConn1, False])
        handbetriebProcess = mp.Process(target=handbetrieb, args=[databasePath, SENSOR_FIELDS, serConn2])

        sensorProcess.start()
        handbetriebProcess.start()

        while(True):
            pass

    finally: 
        sensorProcess.join()
        handbetriebProcess.join()