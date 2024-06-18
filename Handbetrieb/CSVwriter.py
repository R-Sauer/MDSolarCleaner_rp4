import solarCleanerDB
import datetime
import csv


def writeCSV(databasePath: str, sensorTableColumns: list[str]):
    db = solarCleanerDB.Database(databasePath)
    try:
        date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path = f"./Logfiles/Log_{date}.csv"
        data = db.getSensorTable()
        if data is not []:
            with open(path, "w", newline = "") as f:
                writer = csv.writer(f)
                writer.writerow(["System Time"] + sensorTableColumns)
                for row in data:
                    writer.writerow(row)
        else:
            print("No data available in the Database.")
    finally:
        db.closeConnection()

if __name__ == "__main__":
    databasePath = "./test_mp.db"
    SENSOR_FIELDS = ["brush1_rpm", "brush2_rpm", "current_mA"]
    writeCSV(databasePath, SENSOR_FIELDS)