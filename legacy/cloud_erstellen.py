import sqlite3

conn = sqlite3.connect('/home/solartest/Documents/Solartest_Hauptordner/cloud.db')
c = conn.cursor()

def create_topic(table): #Erstellt eine Topic auf der Cloud in die Daten geschrieben und ausgelesen werden koennen. Uebergeben wird der Name der zu erstellenden Topic.
    c.execute(f"CREATE TABLE IF NOT EXISTS {table}\n(id INTEGER PRIMARY KEY AUTOINCREMENT, message TEXT)")
    print(f"Topic {table} erstellt")

def del_data(table): #Loescht alle Daten auf der Topic.
    c.execute(f"DELETE FROM {table}")  # Die Tabelle "messages" leeren
    conn.commit()
    print(f"Clouddaten von {table} geleert")


if __name__ == "__main__":
    #Alle drei benoetigten Topics erstellen.
    create_topic("arduino")
    create_topic("nothalt")
    create_topic("gui")

    #Alle erstellten Topics sicherheitshalber leeren.
    del_data("arduino")
    del_data("gui")
    del_data("nothalt")

    conn.close()