import Firebase
import DotaBuff


class Main:

    def __init__(self):
        self.scraper = DotaBuff.DotaBuffScraper()
        self.fdb = Firebase.Main()

    def main(self):
        self.getMatches()

    def getMatches(self):
        matches = []
        self.scraper.getpagespec("all_pick", "ranked_matchmaking", "europe_west", "very_high_skill")
        matches = self.scraper.matchscrape()
        self.scraper.getpagespec("all_pick", "ranked_matchmaking", "europe_east", "very_high_skill")
        matches += self.scraper.matchscrape()
        for match in matches:
            self.fdb.firebase_tools.addScrapedMatch(match)


if __name__ == '__main__':
    m = Main()
    m.main()
