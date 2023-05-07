import psycopg2
import urllib.request, json

def fetchCircuits():
    with urllib.request.urlopen("http://ergast.com/api/f1/circuits.json") as url:
        data = json.load(url)
        print(data)

    for circuit in data["MRData"]["CircuitTable"]["Circuits"]:
        try:
            cur.execute("INSERT INTO grandprix (name,land,ort) VALUES (%s, %s, %s)", (circuit["circuitName"], circuit["Location"]["country"], circuit["Location"]["locality"]))
        except:
            print("Already up-to-date")

def fetchDrivers():
    with urllib.request.urlopen("http://ergast.com/api/f1/drivers.json") as url:
        data = json.load(url)
        print(data)

    for circuit in data["MRData"]["DriverTable"]["Circuits"]:
        try:
            cur.execute("INSERT INTO grandprix (name,land,ort) VALUES (%s, %s, %s)",
                        (circuit["circuitName"], circuit["Location"]["country"], circuit["Location"]["locality"]))
        except:
            print("Already up-to-date")

try:
    conn = psycopg2.connect(  #making a connection to the server
        host="localhost",
        database="racing",
        user="postgres",
        password="")
except:
    print("Unable to connect to database")

cur = conn.cursor()

fetchCircuits()



conn.commit()
cur.close()
conn.close()
# Get the json data from the website: drivers,grand prix,Rennergebnis
# fetch it in the database