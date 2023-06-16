from DatabaseConnection import DatabaseConnection
class TipDAO:
    def __init__(self):
        self.conn = DatabaseConnection().connect()
        self.cur = self.conn.cursor()


    def create(self):






