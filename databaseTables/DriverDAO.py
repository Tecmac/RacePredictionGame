from DatabaseConnection import DatabaseConnection


class DriverDAO:
    def __init__(self):
        self.conn = DatabaseConnection().connect()
        self.cur = self.conn.cursor()

    def read(self, familyName, givenName, nationality, permanentNumber, dateOfBirth):
        self.cur.execute(
            "SELECT driver_id,name, forename from driver where name = %s and forename = %s and nationality =%s and racenumber=%s and birthday =%s",
            (familyName, givenName, nationality,
             permanentNumber, dateOfBirth))
        print(self.cur.fetchall())
        self.conn.commit()

