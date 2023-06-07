import psycopg2
import urllib.request, json
from datetime import date

from Player import Player


def createPlayer(gamertag, name, forename, password):
    player = Player(gamertag, name, forename, password)
    player.save()
    #cur.execute("INSERT INTO player(GAMERTAG, NAME, FORENAME, PASSWORD) VALUES (%s,%s,%s,%s)",(gamertag,name,forename,password))

def einloggen(gamertag, password):
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

createPlayer("d", "d", "d", "e")

#

    #fahrer auswählen



# tabelle grandprix in circuits umbennen
conn.commit()
cur.close()
conn.close()
    # Get the json data from the website: drivers,grand prix,Rennergebnis
    # fetch it in the database
