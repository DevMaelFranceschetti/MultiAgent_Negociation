from utils import *
import numpy as np
import threading
import time
import logging


class Environnement:

    def __init__(self, n_tasks, n_players, utilities = np.zeros(1)):
        """
        utilities : Matrix(int) the utility matrix of dimension nb_tasks^nb_vehicles * nb_vehicles
        n_players : Number of players
        tasks : Number of tasks
        """
        self.tasks = np.arange(n_tasks)
        self.players = np.arange(n_players)
        self.lock = threading.Lock()

        self.played_moves = 0

        if(utilities.all() == 0):
            shapes = getUtilityShape(n_players,n_tasks)
            self.utility = np.random.randint(0,10,shapes)
        else:
            self.utility = utilities

        # if(utilities != None):
        #     self.utility = utilities
        # else:
        #     shapes = getUtilityShape(n_players,n_tasks)
        #     self.utility = np.random.randint(0,10,shapes)

        self.hist = {}
        for player in self.players:
            self.hist[player] = list(self.tasks)
        self.allocation = np.zeros(n_players).astype(int)
        self.global_opt = self.utility.sum(axis = len(self.players)).max()



    def getUtilityShape(self):
        return getUtilityShape(self.players.shape[0], self.tasks.shape[0])

    def getCosts(self, allocation=None):
        if(allocation):
            return self.utility[tuple(allocation)]
        return self.utility[tuple(self.allocation)]

    def getUnilateralChanges(self, player):
        new_all = list(self.allocation)
        new_all[player] = slice(None)
        unilateral_changes = self.utility[tuple(new_all)]
        return unilateral_changes

    def getMultiLateralChanges(self, players):
        new_all = list(self.allocation)
        for player in players:
            new_all[player] = slice(None)
        multilateral_changes = self.utility[tuple(new_all)]
        return multilateral_changes

    def getBestAction(self,vehicle):
        ch = self.getUnilateralChanges(vehicle)[:,vehicle]
        return ch.max(), ch.argmax()

    def getBestActionPerPlayer(self):
        L = []
        better_action = []
        for vehicle in self.players:
            L.append(self.getUnilateralChanges(vehicle)[:,vehicle].max())
            better_action.append(self.getUnilateralChanges(vehicle)[:,vehicle].argmax())
        L = np.array(L)
        better_action = np.array(better_action)
        return L, better_action


    def getFrequenciesPlayer(self,player):
        return computeFrequency(self.hist[int(player)], self.tasks)

    def getFreqencyMatrix(self):
        v = []
        for player in self.players:
            v.append(np.array(self.getFrequenciesPlayer(player)))
        v = np.array(v)
        return v

    def getFrequencyMatrixL(self):
        L = []
        for agent in self.players:
            arr = self.hist[agent]
            tasks = self.tasks
            freq = np.zeros((len(tasks)))
            for t in tasks:
                k = len(np.where(arr == t)[0])
                freq[t] = k
            L.append(freq / freq.sum())
        L = np.array(L)
        return L

    def getPrecedentActionsMatrix(self):
        min_s = np.inf
        for agent in self.hist:
            min_s = min(min_s, len(self.hist[agent]))
        L = []
        for agent in self.hist:
            L.append(np.array(self.hist[agent][:min_s]))
        return np.array(L)




    def getFrequency(self):
        v = {}
        for player in self.players:
            v[player] = (np.array(self.getFrequenciesPlayer(player)))
        return v


    def getExpectationPlayer(self, player):
        return computePartialFrequencyMatrix(self.utility, self.getFreqencyMatrix(), list(self.players), list(self.tasks), player)


    def is_EN_v(self):
        return (self.getBestActionPerPlayer()[0] == self.utility[tuple(self.allocation)]).any()

    def is_EN(self):
        """ Check if the current allocation is a Nash Equilibrium or not
    Returns :
        Tuple(boolean, int)
        A tuple containing a boolean (True if this allocation is a Nash Equilibrium, else False)
        and an integer that is the id of a vehicle that can increase its utility
        by changing unilateraly its allocation (if not EN, -1)
    """
        for v in range(len(self.players)) : # for each vehicle
            current_task = self.allocation[v]
            current_utility = self.utility[tuple(self.allocation)][v]
            for t in range(len(self.tasks)) :
                if t != current_task : # check all other tasks
                    temp_ind = replaceAlloc(self.allocation, v, t) # allocating task t to vehicle v
                    utility = self.utility[tuple(temp_ind)][v]
                    if utility > current_utility : # changing to another task gives more utility -> Not NE
                        return (False, v)
        return (True, -1)


    def play(self, player, action, verbose=False):
        self.played_moves = self.played_moves + 1
        self.lock.acquire()
        self.allocation[player] = action
        if(verbose):
            logging.debug('Playing '+str(action))
            logging.debug('Current allocation '+ str(self.allocation))
        self.hist[player] = self.hist.get(player,[self.tasks])+ [action]
        self.lock.release()
