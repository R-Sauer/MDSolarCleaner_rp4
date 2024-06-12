import serial
import solarCleanerDB
import platform

def serialReceive(databasePath, sensorTableColumns, serial_baud):
    try:    
        if platform.system() == 'Linux':
            ser = serial.Serial('/dev/ttyACM0', serial_baud, dsrdtr=True)  # Raspberry Pi
        else:
            ser = serial.Serial('COM7', serial_baud, timeout = 1, dsrdtr=True)  # Windows PC
        
        db = solarCleanerDB.Database(databasePath, sensorTableColumns)
        db.initSensorTable()

        firstLine = True
        while(True):
                if ser.in_waiting:
                    if firstLine:
                        ser.reset_input_buffer()
                        ser.readline()
                        firstLine = False
                    dataStrList = ser.readline().decode().rstrip().split(";")
                    dataFloatList = [float(val) for val in dataStrList]
                    db.writeSensorTableRow(dataFloatList)
    finally:
        db.closeConnection()
        ser.close()


if __name__ == '__main__':
    databasePath = './test.db'
    SENSOR_FIELDS = ["brush1_rpm", "brush2_rpm", "current_mA"]
    serial_baud = 115200
    serialReceive(databasePath, SENSOR_FIELDS, serial_baud)
