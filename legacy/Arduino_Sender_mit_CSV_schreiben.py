# Dieses Script liest die Daten vom Arduino ueber USB ein und published sie ins Topic arduino
import sqlite3
import serial
import datetime

# Funktion zum Daten in ein Topic senden
def send_to_topic(topic, message):
    conn = sqlite3.connect('/home/solartest/Documents/Solartest_Hauptordner/cloud.db')
    c = conn.cursor()
    c.execute(f"INSERT INTO {topic} (message) VALUES (?)", (message,))
    conn.commit()
    conn.close()

# Funktion zum Auslesen von Daten aus einem Topic
def read_from_cloud(table):
    conn = sqlite3.connect('/home/solartest/Documents/Solartest_Hauptordner/cloud.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM {table}")
    messages = c.fetchall()
    #print(f"{messages}")
    return messages

# Funktion zum Daten aus einzelnen Topics der Cloud loeschen
def del_data(table):
    conn = sqlite3.connect('/home/solartest/Documents/Solartest_Hauptordner/cloud.db')
    c = conn.cursor()
    c.execute(f"DELETE FROM {table}")  # Die Tabelle "messages" leeren
    conn.commit()
    print(f"Clouddaten von {table} geleert")

# Funktion zum erstellen einer neuen Datei. Der Name ist entsprechend dem aktuellen Zeitstempel + _Solartest_Durlauf.csv
def neue_datei_erstellen():
    aktuelles_datum_und_zeit = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dateiname = f"/home/solartest/Documents/Solartest_Hauptordner/Logdateien/{aktuelles_datum_und_zeit}_Solartest_Durchlauf_.csv"
    return dateiname

# Funktion zum oeffnen und Schreiben in eine Datei
def schreibe_in_datei(dateiname, text):
    with open(dateiname, 'a') as f:
        f.write(text + '\n')


# oeffnen der Seriellen Schnittstelle zum Arduino
ser = serial.Serial('/dev/ttyACM0', 9600)  # Fuer Programm auf raspy
#ser = serial.Serial('COM7', 9600)  # Zum testen fuer PC

# Variable fuer Status des Systems
status = "standby"

# Erstmal alle Topics leeren (zum Start des Systems)
del_data("arduino")
del_data("gui")
del_data("nothalt")

filename = "" # Variable fuer Dateiname der aktuellen CSV Datei

while(True):
    if ser.in_waiting > 0:  # Wenn Daten vom Arduino verfuegbar sind
        data = ser.readline().decode().rstrip() # Daten vom Arduino auslesen
        send_to_topic("arduino", data) # Arduino Daten in Topic publishen
        
        # Schreiben der Arduino Daten in die aktuelle Datei, wenn System laeuft
        if status == "run":
            schreibe_in_datei(filename, data)

        # Wenn in GUI Startknopf gedrueckt wird, dann beginne die Daten zu speichern, bis Verfahrweg abgeschlossen ist
        if read_from_cloud("gui") != [] and status == "standby": # Beginne Speichern 
            status = "run"
            filename = neue_datei_erstellen()
            setupdata = str(read_from_cloud("gui")).split(",")[1].replace("'","").replace(")]","").replace(" ","") # Die Setupdaten der GUI aus dem Topic auslesen und so umwandeln, dass sie verarbeitet werden koennen

            # Header fuer Setupdaten
            Header_setupdata = "Marke Buerste 1;Material Buerste 1;Durchmesser Buerste 1[mm];Drehzahl Buerste 1[U/min];Marke Buerste 2;Material Buerste 2;Durchmesser Buerste 2[mm];Drehzahl Buerste 2[U/min];Staubdichte[g/m3];Staubprobe;Verfahrweg;Drehrichtung Buerste 1;Drehrichtung Buerste 2;Nullhoehe[cm];Aktuelle Hoehe[cm]"
            schreibe_in_datei(filename, Header_setupdata) # Setupdaten header in CSV schreiben
            schreibe_in_datei(filename, setupdata) # Setupdaten in CSV schreiben

            # Header fuer Arduino Daten
            Header_arduinodata = "\nDistanz Up[cm];Distanz Down[cm];Distanz Right[cm];Distanz Left[cm];Temperatur[Grad Celsius];Oberflaechentemperatur[Grad Celsius];Luftfeuchtigkeit[%];Staubdichte[g/m3];Drehzahl Buerste 1[U/min];Drehzahl Buerste 2[U/min];Stroemungsvolumen[L/min];Beschleunigung in Z Richtung[g]"
            schreibe_in_datei(filename, Header_arduinodata) # Arduino Header in CSV schreiben
            print("Beginne Testdurchlauf")


        if read_from_cloud("gui") == [] and status == "run": # Beende Speichern
            status = "standby"
            print("Testdurchlauf abgeschlossen")


