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
                cur.execute("INSERT INTO circuit (name,country,locality) VALUES (%s, %s, %s)",
                            (circuit["circuitName"], circuit["Location"]["country"],
                             circuit["Location"]["locality"]))
                print("Die Strecke " + circuit["circuitName"] + " wurde hinzugefügt :)")
                count1 += 1
                conn.commit()
            except:
                conn.rollback()  # need a rollback to retry
                count2 += 1
    print("FetchCircuits:")
    print("Already up-to-date: ", count2)
    print("Added: ", count1)


def fetchDrivers():
    with urllib.request.urlopen("http://ergast.com/api/f1/2023/drivers.json?limit=1000") as url:  #
        data = json.load(url)
        print(data)
        count1 = 0
        count2 = 0
    for driver in data["MRData"]["DriverTable"]["Drivers"]:
        try:
            cur.execute("INSERT INTO Driver (name,forename,nationality,racenumber,birthday) VALUES (%s, %s, %s,%s,%s)",
                        (driver["familyName"], driver["givenName"], driver["nationality"],
                         driver["permanentNumber"], driver["dateOfBirth"]))
            print("Der Fahrer " + driver["givenName"] + driver["familyName"] + " wurde hinzugefügt :)")
            count1 += 1
            conn.commit()
        except:
            conn.rollback()
            count2 += 1
    print("fetchDrivers")
    print("Already up-to-date: ", count2)
    print("Added: ", count1)


def fetchRace():
    with urllib.request.urlopen("http://ergast.com/api/f1/2023/races.json?limit=1000") as url:
        data = json.load(url)
        print(data)
        count1 = 0
        count2 = 0
    for race in data["MRData"]["RaceTable"]["Races"]:
     #   try:
            cur.execute("INSERT INTO race(circuit_id, name, season, time, date)  "
                        "SELECT circuit_id, %s, %s, %s, %s "
                        "FROM circuit "
                        "WHERE circuit.name = %s", (race["raceName"], int(race["season"]),
                                                    race["time"], race["date"], race["Circuit"]["circuitName"]))
            count1 += 1
            conn.commit()

      #  except:
            conn.rollback()
            count2 += 1
    print("fetchRace")
    print("Already up-to-date: ", count2)
    print("Added: ", count1)



def fetchRaceresults():
    with urllib.request.urlopen("http://ergast.com/api/f1/2023/results.json?limit=1000") as url:
        data = json.load(url)
        print(data)
        count1 = 0
        count2 = 0
        for race in data["MRData"]["RaceTable"]["Races"]:
            cur.execute("SELECT race_id FROM race inner join circuit  ON race.circuit_id = circuit.circuit_id "
                        " Where circuit.name = %s and race.season= %s",
                        (race["Circuit"]["circuitName"], race["season"]))
            raceID = cur.fetchone()

            for result in race["Results"]:
               # try:
                    print(result["number"], "raceID")
                    cur.execute("Select driver_id from driver where driver.name = %s and driver.forename = %s and "
                                "driver.nationality =%s and driver.birthday= %s", (result["Driver"]["familyName"],
                                                                                   result["Driver"]["givenName"],
                                                                                   result["Driver"]["nationality"],
                                                                                   result["Driver"]["dateOfBirth"]))
                    driverID = cur.fetchone()
                    print(driverID)
                    cur.execute("INSERT INTO raceresults(driver_id, race_id, result) VALUES (%s,%s,%s)",
                                (driverID, raceID, result["position"]))
                    print("Die Ergebnisse vom", race["raceName"], " wurde für ", result["Driver"]["familyName"],
                          result["Driver"]["givenName"], "hinzugefügt")
                    count1 += 1
                    conn.commit()
             #   except:
                    count2 += 1
                    conn.rollback()
            print("fetchRaceResults")
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
fetchRaceresults()

# tabelle grandprix in circuits umbennen
conn.commit()
cur.close()
conn.close()
# Get the json data from the website: drivers,grand prix,Rennergebnis
# fetch it in the database
