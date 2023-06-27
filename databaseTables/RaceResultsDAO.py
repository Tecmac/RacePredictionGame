from DatabaseConnection import DatabaseConnection


class RaceResultsDAO:
    def __init__(self):
        self.conn = DatabaseConnection().connect()
        self.cur = self.conn.cursor()

    def readResultRaceDriver(self,race, driver):
        self.cur.execute("Select result from raceresults  where driver_id = %s and race_id = %s", (driver, race))
        data = self.cur.fetchone()
        return data