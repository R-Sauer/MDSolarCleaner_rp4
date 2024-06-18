import serial
import solarCleanerDB
import platform
import time

def serialReceive(databasePath, sensorTableColumns, serial_baud):
    try:    
        try:    
            if platform.system() == 'Linux':
                ser = serial.Serial('/dev/ttyACM0', serial_baud, dsrdtr=True, timeout=1)  # Raspberry Pi
            else:
                ser = serial.Serial('COM7', serial_baud, dsrdtr=True, timeout=1)  # Windows PC
        except serial.serialutil.SerialException as e:
            print(f"Serial connection failed. Check USB connection to Arduino, and COM port access: {e}")
            return
        
        # Sleep for 0.2 sec to give serial interface time to initialize
        time.sleep(0.2)
        
        db = solarCleanerDB.Database(databasePath, sensorTableColumns)
        db.initSensorTable()
        firstLine = True
        while(True):
                if ser.in_waiting:
                    if firstLine:
                        ser.reset_input_buffer()
                        ser.readline()
                        firstLine = False
                    dataStrList = ser.readline().decode(encoding='ascii').rstrip().split(";")
                    dataFloatList = [float(val) for val in dataStrList]
                    db.writeSensorTableRow(dataFloatList)
    finally:
        if 'db' in locals():
            db.closeConnection()
        if 'ser' in locals():
            ser.close()


if __name__ == '__main__':
    databasePath = './test.db'
    SENSOR_FIELDS = ["brush1_rpm", "brush2_rpm", "current_mA"]
    serial_baud = 115200
    serialReceive(databasePath, SENSOR_FIELDS, serial_baud)
