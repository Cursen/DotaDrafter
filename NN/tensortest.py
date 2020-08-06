import datetime
from tensorflow import keras
import numpy as np
import FirebaseMS as firebase
from random import shuffle
#only used for testing nn
from dateutil.relativedelta import relativedelta
from sklearn.metrics import roc_curve, auc, accuracy_score, precision_score, recall_score, f1_score, cohen_kappa_score, \
    confusion_matrix
import matplotlib.pyplot as plt

# take in a list, n for split so 2 = return two lists by splitting the given one based on given percentage.
# splitPerc is expected to be for example 0.7 for 70% first array 30% second
def split_list(alist, splitPerc: float):
    firstArrayL = len(alist) * splitPerc
    firstArray = []
    secondArray = []
    for i, val in enumerate(alist):
        if firstArrayL > i:
            firstArray.append(val)
        else:
            secondArray.append(val)
    return firstArray, secondArray


class Main:

    def __init__(self):
        self.fdb = firebase.Main()
        self.trainingMatches = []
        self.testingMatches = []
        self.heroes = []
        self.heroLength = 0
        self.save_path = 'F:\\Repos\\Uni\\dotadraftergit\\DotaDrafter\\NN\\savedNN.ckpt'
        self.model = None


    def main(self, train):
        self.heroes = self.fdb.firebase_tools.getHeroes()
        self.heroLength = len(self.heroes)
        if train:
            self.trainModel()

    def checkLength(self):
        self.fdb.firebase_tools.checkLengths()

    # Due to matches ids not being structured properly from 0 to LEN, it needs to be converted
    def convertToNeuralId(self, heroId):
        for hero in self.heroes:
            if hero.heroId == heroId:
                return hero.id

    def getEmptyHeroArray(self):
        counter = 0
        heroArray = []
        while counter < len(self.heroes):
            heroArray.append(0)
            counter += 1
        return heroArray

    def trainModel(self):
        # all sets are Numpy arrays
        matchDrafts_train, matchLabels_train, matchDrafts_test, matchLabels_test = self.matchSets()


        # the model needs 1 input neuron for each hero.
        # if hero is picked, set neuron to 1 for radiant -1 for dire. rest to 0
        # hidden layers is less specific, consider 300 or something and test.
        # output is 1 neuron. It should have a value between
        model = self.create_model()
        model.fit(matchDrafts_train, matchLabels_train, epochs=100,
                  validation_split=0.2, verbose=1)
        loss, acc = model.evaluate(matchDrafts_test, matchLabels_test)
        print("Restored model, accuracy: {:5.2f}%".format(100 * acc))
        model.save(self.save_path)

    def matchSets(self):
        totalMatches = self.fdb.firebase_tools.createMatches()
        shuffle(totalMatches)
        matchDrafts = []
        matchLabels = []
        # each value in total matches should be:
        # [1 if radiant, 0 if none -1 if dire], whoWonLabel?
        print(len(totalMatches))
        radiantWins = 0
        direWins = 0
        for match in totalMatches:
            try:
                heroArray = self.getEmptyHeroArray()
                radiantWin = match.radiantWin
                for player in match.radiant_players:
                    heroArray[self.convertToNeuralId(player.hero_id)] = 1

                for player in match.dire_players:
                    heroArray[self.convertToNeuralId(player.hero_id)] = -1
                matchDrafts.append(heroArray)
                if radiantWin:
                    radiantWins += 1
                    matchLabels.append(1)
                else:
                    direWins += 1
                    matchLabels.append(0)
            except TypeError:
                print("TypeError in {0}".format(match.matchId))
        print(direWins)
        print(radiantWins)
        matchDrafts_train, matchDrafts_test = split_list(matchDrafts, 0.8)
        matchLabels_train, matchLabels_test = split_list(matchLabels, 0.8)
        # Now that the "array" is sort off made, turn it into: train examples. train labels. Test examples. Test labels.
        matchDrafts_trainnp = np.asarray(matchDrafts_train)
        matchLabels_trainnp = np.asarray(matchLabels_train)
        matchDrafts_testnp = np.asarray(matchDrafts_test)
        matchLabels_testnp = np.asarray(matchLabels_test)
        return matchDrafts_trainnp, matchLabels_trainnp, matchDrafts_testnp, matchLabels_testnp

    def loadModel(self):
        model = keras.models.load_model(self.save_path)
        #matchDrafts_trainnp, matchLabels_trainnp, matchDrafts_testnp, matchLabels_testnp = self.matchSets()
        #loss, acc = model.evaluate(matchDrafts_testnp, matchLabels_testnp)
        #print("Restored model, accuracy: {:5.2f}%".format(100 * acc))
        model.summary()
        return model

    #quick attempt at getting for preventing "old" data usage, this is currently incomplete
    def matchSetsByDate(self):
        totalMatches = self.fdb.firebase_tools.createMatches()
        shuffle(totalMatches)
        matchDrafts = []
        matchLabels = []
        # how many days ago can the match have been played is set here
        cutOffDate = datetime.datetime.now()
        cutOffDate = cutOffDate - relativedelta(months=3)
        # each value in total matches should be:
        # [1 if radiant, 0 if none -1 if dire], whoWonLabel?
        radiantWins = 0
        direWins = 0
        for match in totalMatches:
            dateForm = datetime.datetime.fromtimestamp(match.startDateTime)
            if dateForm > cutOffDate:
                heroArray = self.getEmptyHeroArray()
                radiantWin = match.radiantWin
                for player in match.radiant_players:
                    heroArray[self.convertToNeuralId(player.hero_id)] = 1

                for player in match.dire_players:
                    heroArray[self.convertToNeuralId(player.hero_id)] = -1
                matchDrafts.append(heroArray)
                if radiantWin:
                    matchLabels.append(1)
                    radiantWins += 1
                else:
                    matchLabels.append(0)
                    direWins += 1
        print(len(totalMatches))
        print(len(matchDrafts))
        print(direWins)
        print(radiantWins)
        matchDrafts_train, matchDrafts_test = split_list(matchDrafts, 0.8)
        matchLabels_train, matchLabels_test = split_list(matchLabels, 0.8)
        # Now that the "array" is sort off made, turn it into numpy of: train examples. train labels. Test examples.
        # Test labels.
        matchDrafts_trainnp = np.asarray(matchDrafts_train)
        matchLabels_trainnp = np.asarray(matchLabels_train)
        matchDrafts_testnp = np.asarray(matchDrafts_test)
        matchLabels_testnp = np.asarray(matchLabels_test)
        return matchDrafts_trainnp, matchLabels_trainnp, matchDrafts_testnp, matchLabels_testnp
    # If any match is overlapped in x or y then return True
    def check_sets(self):
        result = False

        for x in self.trainingMatches:
            for y in self.testingMatches:
                if x == y:
                    result = True
                    return result
        return result


    # Built in way of using model.prediction, unused in overall implementation
    # radiant and dire are arrays of heroIds(NeuralIds)

    def checkDraft(self, radiant, dire):
        heroArray = self.getEmptyHeroArray()
        for pickedHero in radiant:
            heroArray[pickedHero] = 1

        for pickedHero in dire:
            heroArray[pickedHero] = -1
        prediction = self.model([heroArray])

        return prediction

    def create_model(self):
        model = keras.Sequential([
            # input layer, heroLength is currently 119
            keras.layers.Dense(self.heroLength, input_shape=(self.heroLength,)),
            # this is the hidden layer
            keras.layers.Dense(150, activation="relu"),
            #compare with and without dropout as a sollution to overfitting.
            keras.layers.Dropout(0.1),
            # Output layer which gives a predicted probability of Radiant win by 0-1.
            keras.layers.Dense(1, activation="sigmoid")
        ])
        optimizer = keras.optimizers.Adadelta(lr=0.01)
        model.compile(optimizer=optimizer, metrics=["accuracy"], loss="binary_crossentropy")
        return model
    # Plots the roc curve and prints its AUC. Based on a reference in the project
    def rocModel(self):
        model = self.loadModel()
        matchDrafts_train, matchLabels_train, matchDrafts_test, matchLabels_test = self.matchSets()
        y_pred = model.predict(matchDrafts_test).ravel()
        falsePositiveR, truePositiveR, tresholds = roc_curve(matchLabels_test, y_pred)
        aucCalc = auc(falsePositiveR, truePositiveR)
        plt.figure(1)
        plt.figure(1)
        plt.plot([0, 1], [0, 1], 'k--')
        plt.plot(falsePositiveR, truePositiveR, label='Keras (area = {:.3f})'.format(aucCalc))
        plt.xlabel('False positive rate')
        plt.ylabel('True positive rate')
        plt.title('ROC curve')
        plt.legend(loc='best')
        plt.show()
    # this test is heavily based on one of the references in the project
    def overAllTest(self):
        model = self.loadModel()
        matchDrafts_train, matchLabels_train, matchDrafts_test, matchLabels_test = self.matchSets()
        # predict probabilities for test set
        yhat_probs = model.predict(matchDrafts_test, verbose=0)
        # predict crisp classes for test set
        yhat_classes = model.predict_classes(matchDrafts_test, verbose=0)
        # reduce to 1d array
        yhat_probs = yhat_probs[:, 0]
        yhat_classes = yhat_classes[:, 0]
        # accuracy: (tp + tn) / (p + n)
        accuracy = accuracy_score(matchLabels_test, yhat_classes)
        print('Accuracy: %f' % accuracy)
        # precision tp / (tp + fp)
        precision = precision_score(matchLabels_test, yhat_classes)
        print('Precision: %f' % precision)
        # recall: tp / (tp + fn)
        recall = recall_score(matchLabels_test, yhat_classes)
        print('Recall: %f' % recall)
        # f1: 2 tp / (2 tp + fp + fn)
        f1 = f1_score(matchLabels_test, yhat_classes)
        print('F1 score: %f' % f1)
        # confusion matrix
        tn, fp, fn, tp = confusion_matrix(matchLabels_test, yhat_classes).ravel()
        print("true negative: {0}, false positive: {1}, false negative: {2}, true positive: {3}".format(tn,fp,fn,tp))
if __name__ == "__main__":
    m = Main()
    m.main(True)


