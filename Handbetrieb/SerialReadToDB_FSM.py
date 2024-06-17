import multiprocessing
from multiprocessing.connection import Connection
import serial
import solarCleanerDB
import platform
from enum import Enum
import time

class SerialFSMState(Enum):
    Standby = 0
    ReadFirstLine = 1
    ReadContinuous = 2

class SerialFSMCommand(Enum):
    Start = 0
    Stop = 1

def startSerialReceive(commandPipe: Connection) -> None:
    commandPipe.send(SerialFSMCommand.Start)

def stopSerialReceive(commandPipe: Connection) -> None:
    commandPipe.send(SerialFSMCommand.Stop)

def serialReceiveFSM(databasePath: str, sensorTableColumns: list[str], serial_baud: int, commandPipe: Connection, printToConsole: bool=False) -> None:
    try:
        db = solarCleanerDB.Database(databasePath, sensorTableColumns)
        db.initSensorTable()
        
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
        

        encoding = 'ascii'
        state = SerialFSMState.Standby
        stateNext = SerialFSMState.Standby
        while(True):
            match state:
                case SerialFSMState.Standby:
                    # Get FSM control signal from pipe
                    if commandPipe.poll():
                        if commandPipe.recv() == SerialFSMCommand.Start:
                            stateNext = SerialFSMState.ReadFirstLine
                case SerialFSMState.ReadFirstLine:
                    # Clear input buffer to avoid errors
                    ser.reset_input_buffer()
                    # Discard the first line to make the buffer start at the beginning of a data frame
                    ser.readline()
                    stateNext = SerialFSMState.ReadContinuous
                case SerialFSMState.ReadContinuous:
                    if ser.in_waiting:
                        dataStrList = ser.readline().decode(encoding).rstrip().split(";")
                        dataFloatList = [float(val) for val in dataStrList if val]
                        db.writeSensorTableRow(dataFloatList)
                    if printToConsole:
                        print(dataFloatList)
                    if commandPipe.poll():
                        if commandPipe.recv() == SerialFSMCommand.Stop:
                            stateNext = SerialFSMState.Standby
            state = stateNext
    finally:
        if 'db' in locals():
            db.closeConnection()
        if 'ser' in locals():
            ser.close()


if __name__ == '__main__':
    databasePath = './test_SerialReceive.db'
    SENSOR_FIELDS = ["brush1_rpm", "brush2_rpm", "current_mA"]
    serial_baud = 115200
    conn1, conn2 = multiprocessing.Pipe()
    startSerialReceive(conn1)
    serialReceiveFSM(databasePath, SENSOR_FIELDS, serial_baud, conn2)