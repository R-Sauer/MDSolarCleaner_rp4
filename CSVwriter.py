import solarCleanerDB
import datetime
import csv
import os


def writeCSV(databasePath: str):
    db = solarCleanerDB.Database(databasePath)
    try:
        date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path = f"./Logfiles/Log_{date}.csv"
        data = db.getSensorTable()
        if data is not []:
            with open(path, "w", newline = "") as f:
                writer = csv.writer(f)
                for row in data:
                    writer.writerow(row)
        else:
            print("No data available in the Database.")
    finally:
        db.closeConnection()

if __name__ == "__main__":
    databasePath = "./test_mp.db"
    tablename = "sensordata"
    writeCSV(databasePath, tablename)