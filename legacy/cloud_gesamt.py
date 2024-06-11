import sqlite3 #Standardmaessig in Python integriert (kein extra install benötigt)

#Uebersicht ueber alle Funktionalitaeten, welche in dem Projekt in den einzelnen Dateien genutzt werden
class Cloud:
    def __init__(self, path):   
        self.conn = sqlite3.connect(path) #Verbindung zu der Cloud, es wird eine cloud.db Datei erstellt wenn noch keine vorhanden ist.
        self.c = self.conn.cursor()
        self.c.execute('PRAGMA journal_mode=WAL')

    def create_topic(self, table): #Erstellt eine Topic auf der Cloud in die Daten geschrieben und ausgelesen werden koennen. Uebergeben wird der Name der zu erstellenden Topic.
        self.c.execute(f"CREATE TABLE IF NOT EXISTS {table}\n(id INTEGER PRIMARY KEY AUTOINCREMENT, message TEXT)")
        print(f"Cloud {table} erstellt")

    def del_data(self, table): #Loescht alle Daten auf der Topic.
        self.c.execute(f"DELETE FROM {table}")  # Die Tabelle "table" leeren
        self.conn.commit()
        print(f"Clouddaten von {table} geleert")
    
    def stop_cloud(self): #Stoppt die Verbindung zu der Cloud.
        self.conn.close()

    def send_to_topic(self, topic, message): #Sendet die uebergebene message an die uebergebene Topic
        self.c.execute(f"INSERT INTO {topic} (message) VALUES (?)", (message,))
        self.conn.commit()
        # self.conn.close()

    def read_from_cloud(self, table): #Liest die Daten aus, die auf der Topic liegen und returned sie.
        self.c.execute(f"SELECT * FROM {table}")
        messages = self.c.fetchall()
        #print(f"{messages}")
        return messages
    
    def readLastEntry(self, table):
        self.c.execute(f"SELECT * FROM {table} ORDER BY id DESC LIMIT 1;")
        return self.c.fetchall()

    def read_data(self, table): #Ausbau der read_from_cloud: Hier wird der jeweils letzte Eintrag von der Topic in das Terminal geprinted.
        data = self.read_from_cloud(table)
        if data != []:
            print(table)
            print(data[-1])
            self.del_data(table)


#Beispielklasse fuer eine Datei die nur senden muss.
class Sender:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('cloud.db')
        self.c = self.conn.cursor()

    def send_to_topic(self, topic, message):
        conn = sqlite3.connect('cloud.db')
        c = conn.cursor()
        c.execute(f"INSERT INTO {topic} (message) VALUES (?)", (message,))
        conn.commit()
        conn.close()

#Beispielklasse fuer eine Datei, die nur empfangen muss.
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


#Beispielbefehle:
# cloud = Cloud()
"""
cloud.create_topic("arduino")
cloud.create_topic("nothalt")
cloud.create_topic("gui")

cloud.send_to_topic("arduino", "ARDUINO: distance_up,distance_down;distance_right;distance_left;temperature;humidity;air_dust_density;brush1_speed;brush2_speed;flow_velocity;vibration")
cloud.send_to_topic("gui","test")

cloud.read_data("nothalt")
cloud.read_data("arduino")

cloud.del_data("arduino")

cloud.stop_cloud()
"""