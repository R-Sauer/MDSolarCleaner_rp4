import sqlite3
import time

conn = sqlite3.connect('cloud.db')
c = conn.cursor()

def create_cloud(table):
    c.execute(f"CREATE TABLE IF NOT EXISTS {table}\n(id INTEGER PRIMARY KEY AUTOINCREMENT, message TEXT)")
    print(f"Cloud {table} erstellt")

def del_data(table):
    c.execute(f"DELETE FROM {table}")  # Die Tabelle "messages" leeren
    conn.commit()
    print(f"Clouddaten von {table} geleert")



if __name__ == "__main__":
    del_data("arduino")
    del_data("gui")

    conn.close()
