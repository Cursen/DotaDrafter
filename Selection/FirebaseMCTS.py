import firebase_admin
from firebase_admin import credentials, db
from Hero import Hero
from MatchC import Match

class FirebaseTools:
    def __init__(self):
        # this needs to link to the .json file given by firebaseConsole.
        cred = credentials.Certificate("./FireKey.json")
        # this needs to be linked to the database URL in firebaseConsole.
        firebase_admin.initialize_app(cred, {
             'databaseURL': 'https://dota-2-draft-db.firebaseio.com/'
        })
        self.Matches = db.reference("matches")
        self.Heroes = db.reference("heroes")

    def createMatches(self):
        dMatches = []
        for key, matchDetails in self.Matches.get().items():
            try:
                dMatches.append(Match(key, matchDetails))
            except KeyError:
                print("{0} was improperly formated for some reason".format(key))
                print(matchDetails)
            return dMatches
    # test function to see amount of games stored
    def checkLengths(self):
        SMatches = db.reference("ScrapedMatches")
        dMatches = []
        sMatches = []

        for key, matchDetails in self.Matches.get().items():
            dMatches.append(key)
        for key, value in SMatches.get().items():
            sMatches.append(key)
        print('The length of scraped: {0}'.format(len(sMatches)))
        print('The length of matches: {0}'.format(len(dMatches)))

    def getHeroes(self):
        heroList = []
        for value in self.Heroes.get():
            if value is not None:
                heroList.append(Hero(value))
        return heroList
