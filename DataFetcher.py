import psycopg2
import urllib.request, json

import psycopg2
import urllib.request
import json


class DataFetcher:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def fetchCircuits(self):
        try:
            conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            cursor = conn.cursor()

            with urllib.request.urlopen("http://ergast.com/api/f1/circuits.json?limit=1000") as url:
                data = json.load(url)
                count1 = 0
                count2 = 0
                for circuit in data["MRData"]["CircuitTable"]["Circuits"]:
                    try:
                        cursor.execute("INSERT INTO circuit (name, country, locality) VALUES (%s, %s, %s)",
                                       (circuit["circuitName"], circuit["Location"]["country"],
                                        circuit["Location"]["locality"]))
                        print("Die Strecke " + circuit["circuitName"] + " wurde hinzugefügt :)")
                        count1 += 1
                        conn.commit()
                    except:
                        conn.rollback()
                        count2 += 1
                print("FetchCircuits:")
                print("Already up-to-date: ", count2)
                print("Added: ", count1)

            cursor.close()
            conn.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def fetchDrivers(self):
        try:
            conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            cursor = conn.cursor()

            with urllib.request.urlopen("http://ergast.com/api/f1/2023/drivers.json?limit=1000") as url:
                data = json.load(url)
                count1 = 0
                count2 = 0
                for driver in data["MRData"]["DriverTable"]["Drivers"]:
                    try:
                        cursor.execute("INSERT INTO driver (name, forename, nationality, racenumber, birthday) "
                                       "VALUES (%s, %s, %s, %s, %s)",
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

            cursor.close()
            conn.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def fetchRace(self):
        try:
            conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            cursor = conn.cursor()

            with urllib.request.urlopen("http://ergast.com/api/f1/2023/races.json?limit=1000") as url:
                data = json.load(url)
                count1 = 0
                count2 = 0
                for race in data["MRData"]["RaceTable"]["Races"]:
                    try:
                        cursor.execute("INSERT INTO race (circuit_id, name, season, time, date) "
                                       "SELECT circuit_id, %s, %s, %s, %s "
                                       "FROM circuit "
                                       "WHERE circuit.name = %s",
                                       (race["raceName"], int(race["season"]), race["time"], race["date"],
                                        race["Circuit"]["circuitName"]))
                        count1 += 1
                        conn.commit()
                    except:
                        conn.rollback()
                        count2 += 1
                print("fetchRace")
                print("Already up-to-date: ", count2)
                print("Added: ", count1)

            cursor.close()
            conn.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def fetchRaceresults(self):
        try:
            conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            cursor = conn.cursor()

            with urllib.request.urlopen("http://ergast.com/api/f1/2023/results.json?limit=1000") as url:
                data = json.load(url)
                count1 = 0
                count2 = 0
                for race in data["MRData"]["RaceTable"]["Races"]:
                    cursor.execute("SELECT race_id FROM race INNER JOIN circuit ON race.circuit_id = circuit.circuit_id "
                                   "WHERE circuit.name = %s AND race.season = %s",
                                   (race["Circuit"]["circuitName"], race["season"]))
                    raceID = cursor.fetchone()

                    for result in race["Results"]:
                        try:
                            cursor.execute("SELECT driver_id FROM driver WHERE driver.name = %s "
                                           "AND driver.forename = %s "
                                           "AND driver.nationality = %s "
                                           "AND driver.birthday = %s",
                                           (result["Driver"]["familyName"], result["Driver"]["givenName"],
                                            result["Driver"]["nationality"], result["Driver"]["dateOfBirth"]))
                            driverID = cursor.fetchone()

                            cursor.execute("INSERT INTO raceresults (driver_id, race_id, result) VALUES (%s, %s, %s)",
                                           (driverID, raceID, result["position"]))
                            print("Die Ergebnisse vom", race["raceName"], " wurde für ",
                                  result["Driver"]["familyName"], result["Driver"]["givenName"],
                                  "hinzugefügt")
                            count1 += 1
                            conn.commit()
                        except:
                            count2 += 1
                            conn.rollback()
                print("fetchRaceResults")
                print("Already up-to-date: ", count2)
                print("Added: ", count1)

            cursor.close()
            conn.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
