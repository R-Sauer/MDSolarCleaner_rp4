# author: Raphael Sauer
# mailto: raphael.sauer@haw-hamburg.de
# date: 06/2024

import multiprocessing as mp
from SerialReadToDB_FSM import *
from solarCleanerDB import Database
import time

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
        databasePath = './test_mp_pipe.db'
        if not PERSIST_DATABASE:
            Database(databasePath).deleteDatabase()

        conn1, conn2 = mp.Pipe()
        serConn1, serConn2 = mp.Pipe()
        p1 = mp.Process(target=serialReceiveFSM, args=[databasePath, SENSOR_FIELDS, SERIAL_BAUD, serConn2])
        p2 = mp.Process(target=printLatestEntry, args=[databasePath, conn2])
        p3 = mp.Process(target=controlProcess, args=[conn1])
        p4 = mp.Process(target=controlSerialFSM, args=[serConn1])

        p1.start()
        p2.start()
        p3.start()
        p4.start()

        while(True):
            pass

    finally: 
        p1.join()
        p2.join()
        p3.join()
        p4.join()