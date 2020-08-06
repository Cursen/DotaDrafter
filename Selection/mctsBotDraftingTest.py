import constant
from State import DraftState
from mcts import mcts

class botDraft:
    def __init__(self, radiantLimit, direLimit, timesToRun):
        self.mctsRadaint = mcts(timeLimi=radiantLimit)
        self.mctsDire = mcts(timeLimit=direLimit)
        self.timreToRun = timesToRun
        self.radiantWins = 0
        self.direWins = 0
        self.draws = 0

    def main(self):
        i = 0
        while(i < self.timesToRun):
            print(i)
            self.playADraft()
            i += 1
            print("radiantWins: {0}, direWins: {1}, draws: {2}".format(self.radiantWins, self.direWins, self.draws))
            print("Radiant Time: {0}, Dire Time: {1}".format(self.mctsRadiant.timeLimit, self.mctsDire.timeLimit))
    def playADraft(self):
        draft = constant.createDraft(None)
        radiantDraft = DraftState(draft, True)
        direDraft = DraftState(draft, False)
        succesfullPicks = 0
        while succesfullPicks < 5:
            radiantAction = self.mctsRadiant.search(initialState=radiantDraft)
            direAction = self.mctsDire.search(initialState=direDraft)
            if radiantAction is not direAction:
                # add togheter
                radiantDraft = radiantDraft.takeAction(radiantAction)
                direDraft = direDraft.takeAction(radiantAction)
                direDraft = direDraft.takeAction(direAction)
                radiantDraft = radiantDraft.takeAction(direAction)
                succesfullPicks += 1
            else:
                # run again, but remove this option, this is because the game bans options when both teams lock it.
                radiantDraft.removeAction(radiantAction)
                direDraft.removeAction(radiantAction)
        winner = constant.prediction(direDraft.draft, True)
        print(winner)
        if winner > 0.50:
            self.radiantWins += 1
        elif winner < 0.50:
            self.direWins += 1
        else:
            self.draws += 1

        #note this solution is extremely slow for many reasons including some bad decisions regarding neural network input,
        #it was originally intended to have more than one shaped nn to compare, using 10 ids, instead of one spot per hero.
        if __name__ == "main":
            botPlay = botDraft(radiantLimit=5000, direLimit = 5000, timesToRun=50)
            botPlay.main()
