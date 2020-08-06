from __future__ import division

import time
import math
import random


def randomPolicy(state):
    while not state.isTerminal():
        try:
            action = random.choice(state.getPossibleActions())
        except IndexError:
            raise Exception("Non-terminal state has no possible actions: " + str(state))
        state = state.takeAction(action)
    return state.getReward()


class treeNode():
    def __init__(self, state, parent):
        self.state = state
        self.isTerminal = state.isTerminal()
        self.isFullyExpanded = self.isTerminal
        self.parent = parent
        self.numVisits = 0
        self.totalReward = 0
        self.children = {}


class mcts():
    def __init__(self, timeLimit=None, iterationLimit=None, explorationConstant=2.5 / math.sqrt(2),
                 rolloutPolicy=randomPolicy):
        if timeLimit is not None:
            if iterationLimit is not None:
                raise ValueError("Cannot have both a time limit and an iteration limit")
            # time taken for each MCTS search in milliseconds
            self.timeLimit = timeLimit
            self.limitType = 'time'
        else:
            if iterationLimit is None:
                raise ValueError("Must have either a time limit or an iteration limit")
            # number of iterations of the search
            if iterationLimit < 1:
                raise ValueError("Iteration limit must be greater than one")
            self.searchLimit = iterationLimit
            self.limitType = 'iterations'
        self.explorationConstant = explorationConstant
        self.rollout = rolloutPolicy
        self.top5 = []

    def search(self, initialState):
        self.root = treeNode(initialState, None)

        if self.limitType == 'time':
            timeLimit = time.time() + self.timeLimit / 1000
            while time.time() < timeLimit:
                self.executeRound()
        else:
            for i in range(self.searchLimit):
                self.executeRound()
        top = []
        for node in self.top5:
            top.append(self.getAction(self.root, node))
        bestChild = self.getBestChild(self.root, 0)
        #for quick fix of development this part is commented out during botDraft
        return self.getAction(self.root, bestChild)#, top

    def executeRound(self):
        node = self.selectNode(self.root)
        reward = self.rollout(node.state)
        self.backpropogate(node, reward)

    def selectNode(self, node):
        while not node.isTerminal:
            if node.isFullyExpanded:
                node = self.getBestChild(node, self.explorationConstant)
            else:
                return self.expand(node)
        return node

    def expand(self, node):
        actions = node.state.getPossibleActions()
        for action in actions:
            if action not in node.children:
                newNode = treeNode(node.state.takeAction(action), node)
                node.children[action] = newNode
                if len(actions) == len(node.children):
                    node.isFullyExpanded = True
                return newNode

        raise Exception("Should never reach here")

    def backpropogate(self, node, reward):
        while node is not None:
            node.numVisits += 1
            node.totalReward += reward
            node = node.parent

    def getBestChild(self, node, explorationValue):
        bestValue = float("-inf")
        bestNodes = []
        for child in node.children.values():
            nodeValue = self.getNodeValue(child, explorationValue)
            if nodeValue > bestValue:
                bestValue = nodeValue
                bestNodes = [child]
                self.checktop5(child, explorationValue)
            elif nodeValue == bestValue:
                bestNodes.append(child)
                self.checktop5(child, explorationValue)
        return random.choice(bestNodes)

    def getAction(self, root, bestChild):
        for action, node in root.children.items():
            if node is bestChild:
                return action

    def checktop5(self, gnode, explorationValue):
        nodeValue = self.getNodeValue(gnode, explorationValue)
        if not self.top5 or len(self.top5) < 5:
            self.top5.append(gnode)
        else:
            lowestNode = self.top5[0]
            lowestNodeValue = self.getNodeValue(lowestNode, explorationValue)
            for node in self.top5:
                if lowestNodeValue > self.getNodeValue(node, explorationValue):
                    lowestNode = node
                    lowestNodeValue = self.getNodeValue(lowestNode, explorationValue)
            if nodeValue > lowestNodeValue:
                self.top5.append(gnode)
                self.top5.remove(lowestNode)

    def getNodeValue(self, node, explorationValue):
        return node.state.getCurrentPlayer() * node.totalReward / node.numVisits + explorationValue * math.sqrt(
            2 * math.log(node.numVisits) / node.numVisits)