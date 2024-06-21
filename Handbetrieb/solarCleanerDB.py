# author: Raphael Sauer
# mailto: raphael.sauer@haw-hamburg.de
# date: 06/2024

import sqlite3
import os

class Database:
    def __init__(self, databasePath: str, sensorTableColumns: list[str]=[], guiTableColumns: list[str]=[], motorControlTableColumns: list[str]=[]) -> None:
        self.databasePath = databasePath
        # The desired columns of the Database are given as arguments and stored in class members
        self.sensorTableColumns = sensorTableColumns
        self.guiTableColumns = guiTableColumns
        self.motorControlTableColumns = motorControlTableColumns

        self.conn = sqlite3.connect(self.databasePath)
        self.c = self.conn.cursor()
        self.c.execute('PRAGMA journal_mode=WAL')

    def initTable(self, tablename: str, columns: list):
        columnsString = " REAL, ".join(columns) + " REAL"
        self.c.execute(f"""
                       CREATE TABLE IF NOT EXISTS {tablename} 
                       (
                       time DEFAULT (STRFTIME('%H:%M:%f', 'NOW', 'localtime')),
                       {columnsString}
                       )
                       """)
        
    def closeConnection(self):
        self.conn.close()
            
    def initSensorTable(self):
        self.initTable("sensordata", self.sensorTableColumns)

    def initGuiTable(self):
        self.initTable("GUI", self.guiTableColumns)

    def initMotorControlTable(self):
        self.initTable("motorcontrol", self.motorControlTableColumns)

    def getSensorTable(self):
        return self.getTable("sensordata")
    
    def getGUITable(self):
        return self.getTable("GUI")

    def getMotorControlTable(self):
        return self.getTable("motorcontrol")
    
    def deleteTable(self, table: str):
        self.c.execute(f"""
                       DROP TABLE {table}
                       """)

    def deleteSensorTable(self):
        self.deleteTable("sensordata")
    
    def getTable(self, tablename: str):
        self.c.execute(f"""
                       SELECT * FROM {tablename}
                       """)
        return self.c.fetchall()

    def getLastTableRow(self, table):
        self.c.execute(f"SELECT * FROM {table} ORDER BY time DESC LIMIT 1;")
        return self.c.fetchall()
    
    def writeRowToTable(self, tablename: str, rowdata: list, columns: list):
        columnsString = ", ".join(columns)
        placeholders = ", ".join(["?" for _ in columns])
        insertCommand = f"INSERT INTO {tablename} ({columnsString}) VALUES({placeholders})"
        self.c.execute(insertCommand, tuple(rowdata))
        self.conn.commit()

    def writeSensorTableRow(self, rowdata: list):
        self.writeRowToTable("sensordata", rowdata, self.sensorTableColumns)

    def writeGuiTableRow(self, rowdata: list):
        self.writeRowToTable("GUI", rowdata, self.guiTableColumns)
    
    def writeMotorControlTableRow(self, rowdata: list):
        self.writeRowToTable("motorcontrol", rowdata, self.motorControlTableColumns)
        
    def deleteDatabase(self):
        self.conn.close()
        if os.path.exists(self.databasePath):
            os.remove(self.databasePath)
