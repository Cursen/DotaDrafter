from PlayerC import Player


class Match:
    def __init__(self, matchKey, jmatch):
        # jmatch = json.load(jmatch)
        self.matchId = jmatch['matchId']
        self.radiant_players = []
        self.dire_players = []
        for player in jmatch['direHeroes'].values():
            self.dire_players.append(Player(player['Hero_id'], player['steam_id']))

        for player in jmatch['radiantHeroes'].values():
            self.radiant_players.append(Player(player['Hero_id'], player['steam_id']))

        self.radiantWin = jmatch["radiantWin"]
        self.regionId = jmatch["regionId"]
        self.startDateTime = jmatch["startDateTime"]

    def __repr__(self):
        return repr('Match:: id: {0}, direplayers: {1}, radiantPlayers: {2}'.format(self.matchId, self.dire_players, self.radiant_players))