import sqlite3
import os

conn = sqlite3.connect("car_data.db")
cursor = conn.cursor()



def getVehicleID(model, make):
    # search db for model and make
    cursor.execute("SELECT vehicle_id FROM Vehicles WHERE model=:model AND make=:make", 
                   {'model':model, 'make':make})
    result = cursor.fetchone()
    # returns as tuple, so store sinlge ID value as int
    vID = result[0]

    print("year still needs to be implemented")

    return vID

# 
def getInformation(vID):
    cursor.execute()

print(getVehicleID("350Z","Nissan"))
