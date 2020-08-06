class Player:
    def __init__(self, hero, steamid):
        self.hero_id = hero
        self.steam_id = steamid

    def __repr__(self):
        return repr("Players:: heroId: {0}, steamId: {1}".format(self.hero_id, self.steam_id))
