import threading
from Player import Player
from PlayerDAO import PlayerDAO
from databaseTables import TipDAO, RaceResultsDAO
from Admin import Admin



def register():
    gamertag = input()
    name = input()
    forename = input()
    password = input()


    player = Player(gamertag, name, forename, password)
    t = player.save()
    if t == 1:
        return player
    else:
        print("Gib bitte einen anderen gamertag an")
        return register()


def login(type):
    username = input("Gamertag: ")
    password = input("Password: ")
    if type == 1:

        p = PlayerDAO()

        result = p.login(username, password)
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
    if type == 2:
        if username == "Admin" and password == "test":
            a = Admin("Admin","Admin","Admin", "test")
            return a
        else:
            print("Falsche Anmeldeinformationen!")
            return None


# thread 2
# datenn an jedem mittwoch abrufen
# tipps bewerten und dem spieler gutschreiben


# login("d","d")


def ui():
    while 1:
        print("********** Login System **********")
        print("1.Signup")
        print("2.Login")
        print("3.Exit")
        print("4.Admin Login")
        ch = int(input("Enter your choice: "))
        if ch == 1:
            player = register()
            th = int(input("1 = Tipp abgeben; 2 = alle tips sehen ; 3= tips von einem rennen sehen, "))

            if th == 1:
                try:
                    player.giveTip()
                except:
                    print("Fehlgeschlagene")
                    break
            if th == 2:
                try:
                    player.getAllTips()
                except:
                    print("Fehlgeschlagen")
            if th == 3:
                print("Welches Rennen dieser Saison?")
                id = input()
                try:
                    player.getTipsRace(id)
                except:
                    print("Fehlgeschlagen")

        elif ch == 2:
            player = login(1)
            th = int(input("1 = Tipp abgeben; 2 = alle tips sehen ; 3= tips von einem rennen sehen"))

            if th == 1:
                player.giveTip()
            if th == 2:
                player.getAllTips()
            if th== 3:
                print("Welches Rennen dieser Saison?")
                id = input()
                player.getTipsRace(id)

        elif ch == 3:
            break
        elif ch == 4:
            admin = login(2)

            th = int(input("1 = Renndatenbank updaten, 2 = Spieler löschen"))
            if th == 1:
                try:
                    admin.updateAll()
                except:
                    print("Fehlgeschlagen")
            if th == 2:
                gamertag = input("Wie heißt der Gamertag des Spielers")
                try:
                    admin.deletePlayer(gamertag)
                except:
                    print("Fehlgeschlagen")

        else:
            print("Wrong Choice!")


# datenbank tipp mit erge
# für jedes tipp soll erstmal abgeglichen werden ob die renn und fahrer id bereits in raceresults existiert
#

def evaluateTips_thread():

    t = TipDAO.TipDAO()
    r = RaceResultsDAO.RaceResultsDAO()
    p = PlayerDAO()

    tips = t.unevaluatedTips()
    print(tips)

    for tip in tips:
        raceResult = 0
        print(tip)
        driver = tip[0]
        race = tip[1]
        result = tip[2]
        print(race)
        print(result)
        row = r.readResultRaceDriver(race, driver)
       # cur.execute("Select result from raceresults  where driver_id = %s and race_id = %s", (driver, race))
       # row = cur.fetchone()
        if row is not None:
            raceResult = row[0]
            print(raceResult)
        else:
            print("Kein Ergebnis gefunden.")

        if raceResult != 0:

            print(raceResult)
            print(result)
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
            t.updateTips(points, driver, race)
            p.updatePlayerPoints()

           # cur.execute("UPDATE tip set points = %s where driver_id = %s and race_id =%s", (points, driver, race))
         #   conn.commit()
         #   cur.execute("UPDATE player p SET points = "
            #            "(SELECT SUM(t.points) FROM tip t "
        #            "INNER JOIN bet b ON b.tip_id = t.tip_id "
                 #       "WHERE b.player_id = p.player_id)")

           # conn.commit()

        else:
            print("Nothing new")

    # cur.execute()
    # fahrer auswählen
    # tabelle grandprix in circuits umbennen
    #  conn.commit()
    # cur.close()
    # conn.close()
    # Get the json data from the website: drivers,grand prix,Rennergebnis
    # fetch it in the database
t1 = threading.Thread(target=ui())
t2 = threading.Thread(target=evaluateTips_thread)
t1.start()
t2.start()
t1.join()
t2.join()


