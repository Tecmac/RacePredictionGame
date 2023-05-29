import psycopg2
import urllib.request, json
from DatabaseConnection import DatabaseConnection


class Player:

    def __init__(self, gamertag, name, forename, password):
        super().__init__(gamertag, name, forename, password)
        self.conn = DatabaseConnection().connect()
        self.cur = self.conn.cursor()



    def giveTip(self,DName, DForename, ):
        self.cur.execute("", )
