import RPi.GPIO as GPIO
import time
import sqlite3


# GPIO-Pin-Nummer konfigurieren (hier GPIO 18 verwenden)
GPIO_PIN = 18

# Funktion zum Daten in ein Topic senden
def send_to_topic(topic, message):
    conn = sqlite3.connect('/home/solartest/Documents/Solartest_Hauptordner/cloud.db')
    c = conn.cursor()
    c.execute(f"INSERT INTO {topic} (message) VALUES (?)", (message,))
    conn.commit()
    conn.close()

def setup():
    # GPIO-Modus als BCM festlegen
    GPIO.setmode(GPIO.BCM)
    # Den GPIO-Pin als Eingang konfigurieren
    GPIO.setup(GPIO_PIN, GPIO.IN)

def loop():
    while True:
        # GPIO-Pin-Wert auslesen
        pin_value = GPIO.input(GPIO_PIN)
        # Pin-Wert ausgeben
        print("Pin-Wert:", pin_value)
        send_to_topic("nothalt", pin_value) # Arduino Daten in Topic publishen
        # Kurze Pause
        time.sleep(0.5)

def cleanup():
    # GPIO aufraeumen
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    loop()

