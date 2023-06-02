import psycopg2
import urllib.request, json
from datetime import date


def createPlayer(gamertag,name,forename,password):
    cur.execute("INSERT INTO player(GAMERTAG, NAME, FORENAME, PASSWORD) VALUES (%s,%s,%s,%s)",(gamertag,name,forename,password))

def einloggen(gamertag,password):
    cur.execute("Select gamertag From player where password = %s and gamertag= %s ",(gamertag,password))

    if cur.fetchone() is not None:
        print("Login erfolgreich!")
    else:
        print("Falsche Anmeldeinformationen!")

try:
    conn = psycopg2.connect(  # making a connection to the server
            host="localhost",
            database="racing",
            user="postgres",
            password="")
except:
    print("Unable to connect to database")


cur = conn.cursor()

with urllib.request.urlopen("http://ergast.com/api/f1/"+ str(date.today().year)+
                            "/drivers.json?limit=1000") as url:
    test = json.load(url)
    print(test)
    print(date.today())

    for data in test["MRData"]["DriverTable"]["Drivers"]:
        cur.execute(
                "SELECT name, forename from driver where name = %s and forename = %s and nationality =%s and racenumber=%s and birthday =%s",
                (data["familyName"], data["givenName"], data["nationality"],
                 data["permanentNumber"], data["dateOfBirth"]))
        print(cur.fetchall())
    cur.execute(
        "SELECT race.name, circuit.name from race inner join circuit on race.circuit_id = circuit.circuit_id where date> %s order by date",
        (date.today(),))


    #fahrer auswählen



# tabelle grandprix in circuits umbennen
conn.commit()
cur.close()
conn.close()
    # Get the json data from the website: drivers,grand prix,Rennergebnis
    # fetch it in the database
