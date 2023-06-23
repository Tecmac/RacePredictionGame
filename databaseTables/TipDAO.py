from DatabaseConnection import DatabaseConnection


class TipDAO:
    def __init__(self):
        self.conn = DatabaseConnection().connect()
        self.cur = self.conn.cursor()

    def create(self, driver, race, placement):
        self.cur.execute("INSERT INTO Tip (driver_id, race_id, result) VALUES (%s,%s,%s) RETURNING tip_id",
                         (driver, race, placement))
        self.conn.commit()
        return self.cur.fetchone()
    def unevaluatedTips(self):
        self.cur.execute("Select driver_id, race_id, result from tip where points = -1")
        return self.cur.fetchall()



