from DatabaseConnection import DatabaseConnection
from datetime import date


class RaceDAO:
    def __init__(self):
        self.conn = DatabaseConnection().connect()
        self.cur = self.conn.cursor()

    def upcomingRaces(self):
        self.cur.execute(
            "SELECT race_id,race.name, circuit.name from race inner join circuit on race.circuit_id = circuit.circuit_id where "
            "date > %s order by date",
            (date.today(),))
        self.conn.commit()
