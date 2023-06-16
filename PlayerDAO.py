import Player
from DatabaseConnection import DatabaseConnection
class PlayerDAO:
    def __init__(self):
        self.conn = DatabaseConnection().connect()
        self.cur = self.conn.cursor()

    def save(self,p : Player):
        self.cur.execute(
            "INSERT INTO Player (Gamertag, Name, Forename, Password) VALUES (%s, %s, %s, crypt(%s, gen_salt('bf'))) "
            "RETURNING Player_ID",
            (p.gamertag, p.name, p.forename, p.password))
        player_id = self.cur.fetchone()[0]
        self.conn.commit()
        return player_id

    def delete(self,gamertag):
        self.cur.execute("SELECT player_id FROM Player WHERE gamertag = %s", gamertag)
        playerID = self.cur.fetchone()
        self.cur.execute("DELETE FROM PLAYER WHERE player_id = %s", playerID)
        self.cur.execute("DELETE FROM bet WHERE player_id = %s", playerID)

    def getAllTips(self,player_ID):
        self.cur.execute("Select d.forename, d.name,r.name, t.result from player inner join bet b on "
                         "player.player_id = b.player_id inner join tip t on t.tip_id = b.tip_id inner join driver d "
                         "on t.driver_id = d.driver_id inner join race r on t.race_id = r.race_id where b.player_id = "
                         "%s", (player_ID,))
        print(self.cur.fetchall())

    def getTipsRace(self, race_ID):
        self.cur.execute("Select d.forename, d.name,r.name, t.result from player inner join bet b on "
                         "player.player_id = b.player_id inner join tip t on t.tip_id = b.tip_id inner join driver d "
                         "on t.driver_id = d.driver_id inner join race r on t.race_id = r.race_id where t.race_id= "
                         "%s", (race_ID,))
        print(self.cur.fetchall())



