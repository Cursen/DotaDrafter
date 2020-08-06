import time
import FireBaseAPIV as Firebase
import StratzDotaAPI as API
from Match import Match


class Main:

    def __init__(self):
        self.fdb = Firebase.Main()
        self.gMatches = []
        self.matches = []

    def main(self):
        self.getMatches()
        self.resetScrapedMatches()
        if len(self.gMatches) > 0:
            self.storeMatches()

    def getMatches(self):
        self.resetScrapedMatches()
        for key, value in self.matches.items():
            if not value['downloaded']:
                match = API.get_match(key, 0)
                if match:
                    self.gMatches.append(Match(match))
                if len(self.gMatches) > 50:
                    self.storeMatches()
                    self.resetScrapedMatches()
            time.sleep(1)

    def storeMatches(self):
        for match in self.gMatches:
            self.fdb.firebase_tools.addMatch(match)
            self.gMatches.remove(match)

    def resetScrapedMatches(self):
        self.matches = self.fdb.firebase_tools.getScrapedMatches()


if __name__ == '__main__':
    m = Main()
    m.main()
