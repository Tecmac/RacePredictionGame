import psycopg2
import urllib.request, json

def fetchCircuits():
    with urllib.request.urlopen("http://ergast.com/api/f1/circuits.json?limit=1000") as url:
        data = json.load(url)
        print(data)
        count1 = 0
        count2 = 0
        for circuit in data["MRData"]["CircuitTable"]["Circuits"]:

                try:
                    cur.execute("INSERT INTO grandprix (name,land,ort) VALUES (%s, %s, %s)",(circuit["circuitName"], circuit["Location"]["country"], circuit["Location"]["locality"]))
                    print("Die Strecke "+ circuit["circuitName"]+" wurde hinzugefügt :)")
                    count1 += 1
                except:
                    conn.rollback() #need a rollback to retry
                    count2 += 1

    print("Already up-to-date: ",count2)
    print("Added: ",count1)

def fetchDrivers():
    with urllib.request.urlopen("http://ergast.com/api/f1/2023/drivers.json?limit=1000") as url: #
        data = json.load(url)
        print(data)
        count1 = 0
        count2 = 0
    for drivers in data["MRData"]["DriverTable"]["Drivers"]:
        try:
            cur.execute("INSERT INTO Fahrer (name,vorname,nationalität,rennnumer,geburtstag) VALUES (%s, %s, %s,%s,%s)",(drivers["givenName"], drivers["familyName"], drivers["nationality"], drivers["permanentNumber"],drivers["dateOfBirth"]))
            print("Der Fahrer "+ drivers["givenName"]+drivers["familyName"]+" wurde hinzugefügt :)")
            count1 += 1
        except:
            conn.rollback()
            count2 += 1
    print("Already up-to-date: ",count2)
    print("Added: ",count1)


try:
    conn = psycopg2.connect(  # making a connection to the server
        host="localhost",
        database="racing",
        user="postgres",
        password="")
except:
    print("Unable to connect to database")

cur = conn.cursor()

fetchCircuits()
fetchDrivers()

conn.commit()
cur.close()
conn.close()
# Get the json data from the website: drivers,grand prix,Rennergebnis
# fetch it in the database
