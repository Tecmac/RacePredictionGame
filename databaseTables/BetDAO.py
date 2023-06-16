from DatabaseConnection import DatabaseConnection
import Player
class BetDAO:
    def __init__(self):
        self.conn = DatabaseConnection().connect()
        self.cur = self.conn.cursor()

    def create(self,player_id, tip_id):
        self.cur.execute("INSERT INTO bet(player_id, tip_id) VALUES (%s,%s)", (player_id, tip_id))


