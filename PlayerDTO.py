import json
class PlayerDTO:
    def __init__(self, gamertag, name, forename, password):
        self.gamertag = gamertag
        self.name = name
        self.forename = forename
        self.password = password
        self.playerID = None
        self.points = 0

    def to_json(self):
        return json.dumps(self.__dict__)