import multiprocessing as mp
import cloud_gesamt
import serial

SERIAL_BAUD = 115200

def serialReceiveToDatabase(databasePath):
    try:
        # ser = serial.Serial('/dev/ttyACM0', SERIAL_BAUD)  # Fuer Programm auf raspy
        ser = serial.Serial('COM7', SERIAL_BAUD)  # Zum testen fuer PC
        
        db = cloud_gesamt.Cloud(databasePath)
        db.create_topic("sensordata")

        while(True):
            if ser.in_waiting > 0:
                data = ser.readline().decode().rstrip()
                db.send_to_topic("sensordata", data)

    finally:
        db.stop_cloud()


def printLatestEntry(databasePath):
    try:
        db = cloud_gesamt.Cloud(databasePath)
        lastentry = ''
        while(True):
            currententry = db.readLastEntry('sensordata')
            if currententry != lastentry:
                print(lastentry)
            lastentry = currententry
    finally:
        db.stop_cloud()

### Setup and execution of separate processes

if __name__ == '__main__':
    databasePath = './test_mp.db'

    p1 = mp.Process(target=serialReceiveToDatabase, args=[databasePath])
    p2 = mp.Process(target=printLatestEntry, args=[databasePath])

    p1.start()
    p2.start()








