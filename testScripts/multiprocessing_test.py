# author: Raphael Sauer
# mailto: raphael.sauer@haw-hamburg.de
# date: 06/2024

import multiprocessing as mp
import SerialReadToDB
import solarCleanerDB

SERIAL_BAUD = 115200
SENSOR_FIELDS = ["brush1_rpm", "brush2_rpm", "current_mA"]

### Example for a process, that reads from the database in parallel

def printLatestEntry(databasePath):
    try:
        db = solarCleanerDB.Database(databasePath)
        db.initSensorTable()
        lastEntry = ""
        while(True):
            currentEntry = db.getLastTableRow('sensordata')
            if currentEntry != lastEntry:
                print(lastEntry)
            lastEntry = currentEntry
    finally:
        db.closeConnection()

### Setup and execution of separate processes

if __name__ == '__main__':
    try:
        databasePath = './test_mp.db'
        solarCleanerDB.Database(databasePath).deleteDatabase()

        p1 = mp.Process(target=SerialReadToDB.serialReceive, args=[databasePath, SENSOR_FIELDS, SERIAL_BAUD])
        p2 = mp.Process(target=printLatestEntry, args=[databasePath])

        p1.start()
        p2.start()

        while(True):
            pass

    finally: 
        p1.terminate()
        p2.terminate()