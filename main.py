import psycopg2
from Player import Player
from  threading import Thread


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
        "SELECT Player_ID, Name, Forename FROM Player WHERE Gamertag = %s AND Password = crypt(%s,Password)",
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


def ui_thread():
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
            #   player.giveTip()

            player.getAllTips()

        elif ch == 3:
            break
        else:
            print("Wrong Choice!")
            threading.Thread.start()
# datenbank tipp mit erge
# für jedes tipp soll erstmal abgeglichen werden ob die renn und fahrer id bereits in raceresults existiert
#

def evaluateTips_thread():
    cur.execute("Select driver_id, race_id, result from tip where points = -1")

    tips = cur.fetchall()

    for tip in tips:
        driver = 0
        race = 0
        result = 0
        raceResult = 0
        diff = 0

        print(tip)
        driver = tip[0]
        race = tip[1]
        result = tip[2]
        print(race)
        cur.execute("Select result from raceresults  where driver_id = %s and race_id = %s", (driver, race))
        if cur.fetchone() != None:
            raceResult = cur.fetchone()[0]
            diff = abs(raceResult - result)

            match diff:
                case 0:
                    points = 25
                case 1:
                    points = 18
                case 2:
                    points = 15
                case 3:
                    points = 12
                case 4:
                    points = 10
                case 5:
                    points = 8
                case 6:
                    points = 6
                case 7:
                    points = 4
                case 8:
                    points = 2
                case 9:
                    points = 1
                case default:
                    points = 0

            cur.execute("UPDATE tip set points = %s where driver_id = %s and race_id =%s", (points, driver, race))
            cur.execute("UPDATE player  set points = sum(tip.points)  "
                        "from bet inner join player p on bet.player_id = p.player_id inner join tip on tip.tip_id = bet.tip_id ")

            conn.commit()

        else:
            print("Nothing new")

    # cur.execute()
    # fahrer auswählen
    # tabelle grandprix in circuits umbennen
    conn.commit()
    cur.close()
    conn.close()
    # Get the json data from the website: drivers,grand prix,Rennergebnis
    # fetch it in the database


t1 = Thread(target= ui_thread())
t2 = Thread(target=evaluateTips_thread())
