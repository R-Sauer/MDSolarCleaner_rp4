from multiprocessing.connection import PipeConnection
import multiprocessing
import serial
import solarCleanerDB
import platform
from enum import Enum

class SerialFSMState(Enum):
    Standby = 0
    ReadFirstLine = 1
    ReadContinous = 2

class SerialFSMCommand(Enum):
    Start = 0
    Stop = 1

def startSerialReceive(commandPipe: PipeConnection) -> None:
    commandPipe.send(SerialFSMCommand.Start)

def stopSerialReceive(commandPipe: PipeConnection) -> None:
    commandPipe.send(SerialFSMCommand.Stop)

def serialReceiveFSM(databasePath: str, sensorTableColumns: list[str], serial_baud: int, commandPipe: PipeConnection) -> None:
    try:
        db = solarCleanerDB.Database(databasePath, sensorTableColumns)
        db.initSensorTable()
        
        try:    
            if platform.system() == 'Linux':
                ser = serial.Serial('/dev/ttyACM0', serial_baud, dsrdtr=True)  # Raspberry Pi
            else:
                ser = serial.Serial('COM7', serial_baud, timeout = 1, dsrdtr=True)  # Windows PC
        except serial.serialutil.SerialException:
            print("Serial connection failed. Check USB connection to Arduino, and COM port access")
            return
        
        state = SerialFSMState.Standby
        stateNext = SerialFSMState.Standby
        while(True):
            match state:
                case SerialFSMState.Standby:
                    # Get FSM control Signal from Pipe
                    if commandPipe.poll():
                        if commandPipe.recv() == SerialFSMCommand.Start:
                            stateNext = SerialFSMState.ReadFirstLine
                case SerialFSMState.ReadFirstLine:
                    # Clear Input Buffer to avoid errors
                    ser.reset_input_buffer()
                    # Make the buffer start at the beginning of a data frame
                    ser.readline()
                    stateNext = SerialFSMState.ReadContinous
                case SerialFSMState.ReadContinous:
                    if commandPipe.poll():
                        if commandPipe.recv() == SerialFSMCommand.Stop:
                            stateNext = SerialFSMState.Standby
                    if ser.in_waiting:
                        dataStrList = ser.readline().decode().rstrip().split(";")
                        dataFloatList = [float(val) for val in dataStrList]
                        db.writeSensorTableRow(dataFloatList)
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