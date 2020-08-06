import FirebaseMCTS as Firebase
import tensortest
import numpy as np

# change this to change number of turns played.
NUM_TURNS = 5

# NN model to be used for reward calculation
nn = tensortest.Main()
nn.main(False)
reward_model = nn.loadModel()

fdb = nn.fdb

# represents the range of heroes. This should align with what is used in the Reward function option wise.
HEROES = fdb.firebase_tools.getHeroes()
HEROES.sort(key=lambda x: x.id)
HEROES_Length = len(HEROES)


def getNeuralId(heroName):
    heroId = 0
    for hero in HEROES:
        if hero.displayName == heroName:
            heroId = hero.id
            return heroId
    return heroId


def getDisplayName(neuralId):
    for hero in HEROES:
        if hero.id == neuralId:
            return hero.displayName
    return "Not Found"


def prediction(pickedHeroes, radiant):
    heroes = np.array(pickedHeroes)
    # the reshape for the predict*( expecting batches, but we want only one at a time.
    reward = reward_model.predict(heroes.reshape(1, -1))
    if not radiant:
        reward = reward * -1
    return reward


def createDraft(pickedHeroIds):
    heroArray = nn.getEmptyHeroArray()
    if pickedHeroIds:
        for key, value in pickedHeroIds.items():
            if value == 1:
                heroArray[key] = 1
            elif value == -1:
                heroArray[key] = -1
    return heroArray
