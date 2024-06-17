import multiprocessing as mp
from SerialReadToDB_FSM import *
from SerialReadToDB import serialReceive
from solarCleanerDB import Database
import time
from Handbetrieb import handbetrieb

SERIAL_BAUD = 115200
SENSOR_FIELDS = ["brush1_rpm", "brush2_rpm", "current_mA"]
PERSIST_DATABASE = False

def controlProcess(connection):
    toggle = False
    while(True):
        toggle = not toggle
        connection.send(toggle)
        time.sleep(2)

def controlSerialFSM(commandPipe):
    toggle = False
    while(True):
        toggle = not toggle
        if toggle:
            commandPipe.send(SerialFSMCommand.Start)
        else:
            commandPipe.send(SerialFSMCommand.Stop)
        time.sleep(2)

### Example for a process, that reads from the database in parallel
def printLatestEntry(databasePath, connection):
    try:
        db = Database(databasePath)
        db.initSensorTable()
        lastEntry = ""
        printState = True
        while(True):
            if connection.poll():
                printState = connection.recv()
            if printState:
                currentEntry = db.getLastTableRow('sensordata')
                if currentEntry != lastEntry:
                    print(lastEntry)
                lastEntry = currentEntry
    finally:
        db.closeConnection()

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