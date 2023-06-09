import psycopg2
from Player import Player


def register():
    gamertag = input()
    name = input()
    forename = input()
    password = input()
    player = Player(gamertag, name, forename, password)
    player.save()
    return player


def login():
    username = input("Username: ")
    password = input("Password: ")
    cur.execute(
        "SELECT Player_ID, Name, Forename FROM Player WHERE Gamertag = %s AND Password = %s",
        (username, password)
    )
    result = cur.fetchone()
    if result:
        playerID = result[0]
        name = result[1]
        forename = result[2]
        player = Player(username, name, forename, password)
        player.playerID = playerID
        print("Login erfolgreich!")
        return player
    else:
        print("Falsche Anmeldeinformationen!")
        return None


# thread 2
# datenn an jedem mittwoch abrufen
# tipps bewerten und dem spieler gutschreiben
try:
    conn = psycopg2.connect(  # making a connection to the server
        host="localhost",
        database="racing",
        user="postgres",
        password="")
except:
    print("Unable to connect to database")

# login("d","d")
cur = conn.cursor()
while 1:
    print("********** Login System **********")
    print("1.Signup")
    print("2.Login")
    print("3.Exit")
    ch = int(input("Enter your choice: "))
    if ch == 1:
        player = register()
        player.giveTip()
    elif ch == 2:
        player = login()
        player.giveTip()

    elif ch == 3:
        break
    else:
        print("Wrong Choice!")


# datenbank tipp mit erge
# für jedes tipp soll erstmal abgeglichen werden ob die renn und fahrer id bereits in raceresults existiert
#
cur.execute("Select driver_id, race_id from tip where points = -1")
print(cur.fetchall())
# cur.execute("Select result from raceresults  where driver_id = %s and race_id = %s")
# cur.execute()
# fahrer auswählen


# tabelle grandprix in circuits umbennen
conn.commit()
cur.close()
conn.close()
# Get the json data from the website: drivers,grand prix,Rennergebnis
# fetch it in the database
