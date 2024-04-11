# Script, um ein bestimmtes Topic auszulesen und auf die Konsole zu schreiben
# Dieses Script kann in der Powershell über py Test_empfaenger.py gestartet werden
import sqlite3
import time

class Empfaenger:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('cloud.db')
        self.c = self.conn.cursor()

    def read_from_cloud(self, table):
        self.c.execute(f"SELECT * FROM {table}")
        messages = self.c.fetchall()
        #print(f"{messages}")
        return messages

    def read_data(self, table):
        data = self.read_from_cloud(table)
        if data != []:
            print(table)
            print(data[-1])
            self.del_data(table)

    def del_data(self, table):
        self.c.execute(f"DELETE FROM {table}")  # Die Tabelle "messages" leeren
        self.conn.commit()
        print(f"Clouddaten von {table} geleert")

zu_abbonierendes_topic = "arduino"
ausleser = Empfaenger()
while True:
    ausleser.read_data(zu_abbonierendes_topic)
    time.sleep(1)