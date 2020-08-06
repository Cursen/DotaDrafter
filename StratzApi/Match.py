import json
from Player import Player


class Match:
    def __init__(self, jmatch):
        jmatch = json.loads(jmatch)
        self.matchId = str(jmatch["id"])
        self.radiant_players = []
        self.dire_players = []
        for player in jmatch["players"]:
            if player["isRadiant"]:
                self.radiant_players.append(Player(player["heroId"], player["playerSlot"], steamid=player["steamAccountId"]))
            else:
                self.dire_players.append(Player(player["heroId"], player["playerSlot"], steamid=player["steamAccountId"]))
        self.radiantWin = jmatch["didRadiantWin"]
        self.regionId = jmatch["regionId"]
        self.startDateTime = jmatch["startDateTime"]

