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
                    cur.execute("INSERT INTO circuit (name,country,locality) VALUES (%s, %s, %s)",(circuit["circuitName"], circuit["Location"]["country"], circuit["Location"]["locality"]))
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
    for driver in data["MRData"]["DriverTable"]["Drivers"]:
        try:
            cur.execute("INSERT INTO Driver (name,forename,nationality,racenumber,birthday) VALUES (%s, %s, %s,%s,%s)", (driver["givenName"], driver["familyName"], driver["nationality"], driver["permanentNumber"],driver["dateOfBirth"]))
            print("Der Fahrer "+ driver["givenName"]+driver["familyName"]+" wurde hinzugefügt :)")
            count1 += 1
        except:
            conn.rollback()
            count2 += 1
    print("Already up-to-date: ",count2)
    print("Added: ",count1)

def fetchRace():
    with urllib.request.urlopen("http://ergast.com/api/f1/2023/races.json?limit=1000") as url:
        data =json.load(url)
        print(data)
        count1 = 0
        count2 = 0
    for race in data["MRData"]["RaceTable"]["Races"]:
        try:
            cur.execute("INSERT INTO race (season, time, date, circuit_id) "
                    "SELECT %s, %s, %s, circuit_id "
                    "FROM circuit "
                    "WHERE name = %s",(race["season"], race["time"], race["date"], race["Circuit"]["circuitName"]))
            count1 += 1

        except:
            conn.rollback()
            count2 += 1
    print("Already up-to-date: ", count2)
    print("Added: " ,  count1)


def fetchRaceResults():
    with urllib.request.urlopen("http://ergast.com/api/f1/2023/results.json?limit=1000") as url:
        data = json.load(url)
        count1 = 0
        count2 = 0
        for race in data["MRData"]["RaceTable"]["Races"]:
            try:
                race_season = race["season"]
                race_date = race["date"]

                cur.execute("SELECT Race_ID FROM Race WHERE Season = %s AND Date = %s", (race_season, race_date))
                race_id = cur.fetchone()[0]
                print(race_id)

                for result in race["Results"]:
                    driver_name = result["Driver"]["driverId"]

                    cur.execute("SELECT Driver_ID FROM Driver WHERE Name = %s", (driver_name,))
                    driver_row = cur.fetchone()

                    if driver_row:
                        driver_id = driver_row[0]

                        cur.execute("INSERT INTO Raceresults (Driver_ID, Race_ID, result) VALUES (%s, %s, %s)",
                                    (driver_id, race_id, result["position"]))
                        count1 += 1
                    else:
                        print("Fahrer '{}' nicht gefunden.".format(driver_name))
            except:
                conn.rollback()
                count2 += 1

    print("Already up-to-date: ", count2)
    print("Added: ", count1)


# daten einfügen und gp id eintragen wo bei der tabelle grandprix

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
fetchRace()
fetchRaceResults()

# tabelle grandprix in circuits umbennen
conn.commit()
cur.close()
conn.close()
# Get the json data from the website: drivers,grand prix,Rennergebnis
# fetch it in the database
