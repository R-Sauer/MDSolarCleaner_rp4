import sqlite3
import os

class Database:
    def __init__(self, _databasePath: str, _sensorTableColumns: list=[], _guiTableColumns: list=[]) -> None:
        self.sensorTableColumns = _sensorTableColumns
        self.guiTableColumns = _guiTableColumns
        self.databasePath = _databasePath

        self.conn = sqlite3.connect(self.databasePath)
        self.c = self.conn.cursor()
        self.c.execute('PRAGMA journal_mode=WAL')

    def initTable(self, tablename: str, columns: list):
        columnsString = " REAL, ".join(columns) + " REAL"
        self.c.execute(f"""
                       CREATE TABLE IF NOT EXISTS {tablename} 
                       (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       {columnsString}
                       )
                       """)
        
    def closeConnection(self):
        self.conn.close()
            
    def initSensorTable(self):
        self.initTable("sensordata", self.sensorTableColumns)

    def initGuiTable(self):
        self.initTable("GUI", self.guiTableColumns)
    
    def deleteTable(self, table: str):
        self.c.execute(f"""
                       DROP TABLE {table}
                       """)
    
    def getTable(self, tablename: str):
        self.c.execute(f"""
                       SELECT * FROM {tablename}
                       """)
        return self.c.fetchall()

    def getLastTableRow(self, table):
        self.c.execute(f"SELECT * FROM {table} ORDER BY id DESC LIMIT 1;")
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
        self.writeRowToTable("GUI", rowdata, self.sensorTableColumns)

    def deleteDatabase(self):
        self.conn.close()
        if os.path.exists(self.databasePath):
            os.remove(self.databasePath)
