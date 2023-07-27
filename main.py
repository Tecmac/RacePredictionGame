import threading
from Player import Player
from PlayerDAO import PlayerDAO
from databaseTables import TipDAO, RaceResultsDAO
from Admin import Admin
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()


class loginInfo(BaseModel):
    username: str
    password: str


@app.post("/login")
async def fLogin(l: loginInfo):
    p = PlayerDAO()

    result = p.login(username, password)
    if result:
        playerID = result[0]
        name = result[1]
        forename = result[2]
        player = Player(username, name, forename, password)
        player.playerID = playerID
        print("Login erfolgreich!")
        return {"test1"}
    else:

        return {"test2"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
