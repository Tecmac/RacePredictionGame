import psycopg2
import urllib.request, json
from DatabaseConnection import DatabaseConnection
from datetime import date
from User import User


class Player(User):

    def __init__(self, gamertag, name, forename, password):
        super().__init__(gamertag, name, forename, password)
        self.playerID = None
        self.points = 0
        self.conn = DatabaseConnection().connect()
        self.cur = self.conn.cursor()

    def save(self):
        self.cur.execute(
            "INSERT INTO Player (Gamertag, Name, Forename, Password) VALUES (%s, %s, %s, crypt(%s, gen_salt('bf'))) "
            "RETURNING Player_ID",
            (self.gamertag, self.name, self.forename, self.password))
        self.playerID = self.cur.fetchone()[0]
        self.conn.commit()
    def giveTip(self):
        # zeige die Rennen die anstehen
        # wähle das rennen aus dropdown menü
        # zeige die Fahrer
        # wähle fahrer aus den dropdown
        with urllib.request.urlopen("http://ergast.com/api/f1/" + str(date.today().year) +
                                    "/drivers.json?limit=1000") as url:
            test = json.load(url)
            print(test)
            print(date.today())

            for data in test["MRData"]["DriverTable"]["Drivers"]:
                self.cur.execute(
                    "SELECT driver_id,name, forename from driver where name = %s and forename = %s and nationality =%s and racenumber=%s and birthday =%s",
                    (data["familyName"], data["givenName"], data["nationality"],
                     data["permanentNumber"], data["dateOfBirth"]))
                print(self.cur.fetchall())
            print("Gebens Sie die FahrerID ein ( Zahl am Anfang des Fahrers)")
            fahrer: int = input()

            self.cur.execute(
                "SELECT race_id,race.name, circuit.name from race inner join circuit on race.circuit_id = circuit.circuit_id where "
                "date > %s order by date",
                (date.today(),))
            print("\n", self.cur.fetchall())
            print("Geben Sie die Renn_ID ein")
            rennen = input()

            print("Welchen Platz erreicht der Fahrer? 1-20")
            platzierung = input()
            self.cur.execute("INSERT INTO Tip (driver_id, race_id, result) VALUES (%s,%s,%s) RETURNING tip_id", (fahrer, rennen, platzierung))
            tipID = self.cur.fetchone()
            self.cur.execute("INSERT INTO bet(player_id, tip_id) VALUES (%s,%s)",(self.playerID, tipID))
            #self.cur.execute("")
            self.conn.commit()



