from DatabaseConnection import DatabaseConnection


class RaceResultsDAO:
    def __init__(self):
        self.conn = DatabaseConnection().connect()
        self.cur = self.conn.cursor()

    def readResultRaceDriver(self,race, driver):