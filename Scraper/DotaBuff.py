import time
import requests
from MatchScrape import MatchScrape
from bs4 import BeautifulSoup


# TODO add several queries based on different regions than just europe west.

class DotaBuffScraper:
    def __init__(self):
        self.soup = BeautifulSoup(self.getpage(), 'lxml')

    def main(self):
        self.refreshpage()
        self.matchscrape()

    def getpage(self):
        result = requests.get(
            "https://www.dotabuff.com/matches?game_mode=all_pick&lobby_type=ranked_matchmaking&region=europe_west&skill_bracket=very_high_skill",
            headers={'User-agent': 'your bot 0.1'})
        if result.status_code == 200:
            print("found page")
            return result.content
        else:
            print("did not find page, waiting 1 second")
            time.sleep(1000)
            self.getpage()

    def getpagespec(self, game_mode, lobby_type, region, skill_bracket):
        specurl = "https://www.dotabuff.com/matches?game_mode={0}&lobby_type={1}&region={2}&skill_braket={3}".format(game_mode,lobby_type,region,skill_bracket)
        result = requests.get(
            specurl,
            headers={'User-agent': 'your bot 0.1'})
        if result.status_code == 200:
            print("found page")
            self.soup = BeautifulSoup(result.content, 'lxml')
        else:
            print("did not find page")
            pass

    def refreshpage(self):
        self.soup = BeautifulSoup(self.getpage(), 'lxml')

    def matchscrape(self):
        matches = []
        # get all match IDs and "minutes ago" with beatifulsoup.
        # get the table entries
        matchTable = self.soup.find("table").find("tbody").find_all("tr")
        # get the id and time associated
        for tr in matchTable:
            cols = tr.find_all('td')
            # due to website layout, we only need the first col.
            matchColumn = cols[0]
            matchId = matchColumn.find('a').text
            # print(matchId)
            matchDate = matchColumn.find('time')['datetime']
            # print(matchDate)
            match = MatchScrape(matchId)
            # just in case, lets try to not add several of same matchId.
            # This does cause more work per match.
            if not any(matc.matchId == matchId for matc in matches):
                matches.append(match)

        return matches

    def getmatchtable(self):
        return self.matches


if __name__ == '__main__':
    m = Main()
    m.main()
