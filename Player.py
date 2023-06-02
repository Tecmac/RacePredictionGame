import psycopg2
import urllib.request, json
from DatabaseConnection import DatabaseConnection
from datetime import date


class Player:

    def __init__(self, gamertag, name, forename, password):
        super().__init__(gamertag, name, forename, password)
        self.conn = DatabaseConnection().connect()
        self.cur = self.conn.cursor()

    def giveTip(self):
        # zeige die Rennen die anstehen
        # wähle das rennen aus dropdown menü
        # zeige die Fahrer
        # wähle fahrer aus den dropdown
        #
        self.cur.execute("SELECT name, season FROM race where date> %s", str(date.today()))

        with urllib.request.urlopen("http://ergast.com/api/f1/" + str(date.today().year) +
                                    "/drivers.json?limit=1000") as url:
            data = json.load(url)

        self.cur.execute("SELECT name, forename from driver where name = %s and forename = %s and nationality =%s and racenumber=%s and birthday =%s",(data["familyName"], data["givenName"], data["nationality"],
                                        data["permanentNumber"], data["dateOfBirth"]))
        print(self.cur.fetchall())
        self.cur.execute("SELECT name, circuit.name from race inner join circuit on race.circuit_id = circuit.circuit_id where date> %s",str(date.today()))

        print(self.cur.fetchall())
