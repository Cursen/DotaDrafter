from copy import deepcopy
from mcts import mcts
import constant


class DraftState:
    def __init__(self, draft, radiant):
        # it is expected that the radiant action, is accounted for first, even if the "player" is Dire.
        self.currentPlayer = 1
        self.radiant = radiant
        self.draft = draft
        self.banned = []

    def getCurrentPlayer(self):
        return self.currentPlayer

    def getPossibleActions(self):
        possibleActions = []
        for i in range(len(self.draft)):
            if self.draft[i] == 0 and not self.banned.__contains__(i):
                possibleActions.append(i)
            return possibleActions

    def takeAction(self, i):
        newState = deepcopy(self)
        newState.draft[i] = self.currentPlayer
        self.currentPlayer = self.currentPlayer * -1
        return newState

    # this is just used in main test
    def takeActualAction(self, i):
        print(i)
        self.draft[i] = self.currentPlayer
        self.currentPlayer = self.currentPlayer * -1

        # ban heroes from pool
        def removeAction(self, action):
            self.banned.append(action)

        def isTerminal(self):
            counter = 0
            for i in self.draft:
                if i != 0:
                    counter += 1
            if counter == 10:
                return True
            elif counter > 10:
                raise RuntimeError("counter was too big")
            else:
                return False

    def getReward(self):
        return constant.prediction(self.draft, self.radiant)


if __name__ == '__main__':
    heropicks = {2: 1, 5: -1, 75: 1, 76: -1}
    draft = constant.createDraft(heropicks)
    radiant = []
    dire = []
    initialState = DraftState(draft, True)
    initialState.banned.append(3)
    print(initialState.banned)
    mcts = mcts(timeLimit=10000)
    print(initialState.draft)
    # note top5 is most likely not accounted for atm
    action, top5 = mcts.search(initialState)
    print(action)
    print("recomended hero: {0}".format(constant.getDisplayName(action)))
    initialState.takeActualAction(action)
    if initialState.getPossibleActions().__contains__(3): print("ban contained in possible actions")
    constant.getDisplayName(initialState.draft)
    print("top5")
    for hero in top5:
        print(constant.getDisplayName(hero))
