import firebase_admin
from firebase_admin import credentials, db


class Main:

    def __init__(self):
        self.firebase_tools = FirebaseTools()

    def main(self):
        self.start()

    def start(self):
        pass


if __name__ == '__main__':
    m = Main()
    m.main()


class FirebaseTools:
    def __init__(self):
        # this needs to link to the .json file given by firebaseConsole.
        cred = credentials.Certificate("./FireKey.json")
        # this needs to be linked to the database URL in firebaseConsole.
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://dota-2-draft-db.firebaseio.com/'
        })
        self.scrapedMatches = db.reference("scrapedMatches")
        self.Matches = db.reference("matches")

    def addScrapedMatch(self, match):
        self.scrapedMatches.child(match.matchId).set({'downloaded': match.downloaded})

    def addMatch(self, dMatch):

            self.Matches.child(dMatch.matchId).set({"matchId": dMatch.matchId,
                                                    "radiantWin": dMatch.radiantWin,
                                                    "regionId": dMatch.regionId,
                                                    "startDateTime": dMatch.startDateTime})
            self.addPlayers(players=dMatch.radiant_players,matchId=dMatch.matchId,radiantTeam=True)
            self.addPlayers(players=dMatch.dire_players,matchId=dMatch.matchId,radiantTeam=False)
            print("sent add match")
            print("failed in addMatch")

            self.removeScrapedMatch(matchId=dMatch.matchId)

    def removeScrapedMatch(self, matchId):
        try:
            self.scrapedMatches.child(matchId).delete()
        except:
            print("Failed to remove scraped match")

    def getScrapedMatches(self):
        return db.reference("scrapedMatches").get()

    def addPlayers(self, players, matchId, radiantTeam):
        if (radiantTeam):
            teamString = "radiantHeroes"
        else:
            teamString = "direHeroes"

        for player in players:
            self.Matches.child(matchId).child(teamString).update({
                "Player{0}".format(player.player_slot): {
                    "Hero_id": player.hero_id,
                    "steam_id": player.steam_id}})

