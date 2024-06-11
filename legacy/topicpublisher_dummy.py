# Kommunikation
import sqlite3

def send_to_topic(topic, message):
    conn = sqlite3.connect('/home/solartest/Documents/Solartest_Hauptordner/cloud.db')
    c = conn.cursor()
    c.execute(f"INSERT INTO {topic} (message) VALUES (?)", (message,))
    conn.commit()
    conn.close()

send_to_topic("gui","Test")