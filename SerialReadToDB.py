import sqlite3
import serial
import solarCleanerDB

def serialReceive(databasePath, sensorTableColumns, serial_baud):
    try:
        # ser = serial.Serial('/dev/ttyACM0', serial_baud, dsrdtr=True)  # Raspberry Pi
        ser = serial.Serial('COM7', serial_baud, timeout = 1, dsrdtr=True)  # Windows PC
        
        db = solarCleanerDB.Database(databasePath, sensorTableColumns)
        db.initSensorTable()

        firstLine = True

        while(True):
            # try:
                if ser.in_waiting:
                    if firstLine:
                        ser.reset_input_buffer()
                        ser.readline()
                        firstLine = False
                    dataStrList = ser.readline().decode().rstrip().split(";")
                    dataFloatList = [float(val) for val in dataStrList]
                    db.writeSensorTableRow(dataFloatList)
            # except:
            #      pass
    finally:
        db.closeConnection()
        ser.close()


if __name__ == '__main__':
    databasePath = './test.db'
    sensorTableColumns = ["brush1_rpm", "brush2_rpm", "current_mA"]
    serial_baud = 115200
    serialReceive(databasePath, sensorTableColumns, serial_baud)
