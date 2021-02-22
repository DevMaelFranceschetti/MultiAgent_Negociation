import numpy as np
from Environnement import *
import threading
import time
import logging
from Functions import *
import random


logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )


class Player():
    """
    This class encapsulates the high level design of a player in a negociation game.
    To use it you just have to redefind the observation and the action methods.
    """

    def __init__(self, environnement, id):
        self.env = environnement
        self.id  = id
        pass
    
    def getWorkerFunction(self,steps, verbose = False):
        def worker():
            for i in range(steps):
                action = self.select_action()
                self.env.play(self.id, self.select_action(),verbose=verbose)
                self.observe()
        return worker

    def bestAnswer(self, other_moves):
        t = other_moves[:self.id] + [-1]+ other_moves[self.id+1:] + [self.id]
        t[self.id] = slice(None, None, None)
        print (self.env.utility[t])
        return np.argmax(self.env.utility[t]), np.max(self.env.utility[t])

    def computeBestMove(self):
        L = []
        for agent in self.env.hist:
            if(agent != self.id):
                L.append(self.env.hist[agent])
        a,v = self.bestAnswer(L)
        print(f"Best action {a} with a value of {v}")
        return a,v 
    
    def observe(self):
        pass

    def select_action(self):
        pass




class RandomPlayer(Player):

    def select_action(self):
        action = np.random.randint(0, self.env.tasks.shape[0])
        return action




class BRPlayer(Player):
    
    def select_action(self):
        return self.env.getBestAction(self.id)[1]
        



class FPPlayer1(Player):
    def select_action(self):
        return np.argmax(self.env.getExpectationPlayer(self.id))

class FPPlayer(Player):

    def getExpectedUtility(self):
        fmatrix = self.env.getFrequencyMatrixL()
        t = len(self.env.players)*[slice(None, None, None)]+[self.id]
        it = np.nditer(self.env.utility[t], flags=['multi_index'])
        act = np.zeros(self.env.tasks.shape)
        for x in it:
            p = 1
            for n,a in  enumerate(it.multi_index):
                p = p  * (fmatrix[n][a])
            mya = it.multi_index[self.id]
            act[mya] = act[mya] + p*x
        return act
        
    
    def select_action(self):
        a = self.getExpectedUtility()
        logging.debug('Expected utility  '+str(a))
        return np.argmax(a)


class RegretMatchingPlayer(Player):

    def __init__(self, environnement, id):
        super().__init__( environnement, id)
        self.cumulated_reget = np.zeros(self.env.tasks.shape)
        self.step = 0

    def observe(self):
        pred_ac = self.env.getPrecedentActionsMatrix().T
        for i in range(self.step, pred_ac.shape[0]):
            act = pred_ac[i]
            self.cumulated_reget[act[self.id]] = self.cumulated_reget[act[self.id]] + self.getRegret(act)
        self.step = pred_ac.shape[0]

    def getRegret(self, actions):
        moves_v = list(actions[:self.id]) + [slice(None, None, None)] + list(actions[self.id+1:])+ [self.id]
        u = self.env.utility[tuple(moves_v)]
        return np.max(u) - u[actions[self.id]]
    
    def select_action(self):
        norm_regret = (self.cumulated_reget / self.step) if (self.step != 0 ) else self.cumulated_reget
        return np.argmin(norm_regret)



class SAPlayer(Player):
    
    def select_action(self):
        ch = self.env.getUnilateralChanges(self.id)[:,self.id]
        ch = softmax(ch)
        act = np.random.choice(self.env.tasks, p=ch)
        return self.env.getBestAction(self.id)[1]
    





class SpatialFictiousPlayPlayer(Player):

    def __init__(self, environnement, id, func = softmax):
        super().__init__( environnement, id)
        self.func = func

    def getExpectedUtility(self):
        fmatrix = self.env.getFrequencyMatrixL()
        print(fmatrix.shape)
        t = len(self.env.players)*[slice(None, None, None)]+[self.id]
        it = np.nditer(self.env.utility[t], flags=['multi_index'])
        act = np.zeros(self.env.tasks.shape)
        for x in it:
            p = 1
            for n,a in  enumerate(it.multi_index):
                p = p  * (fmatrix[n][a])
            mya = it.multi_index[self.id]
            act[mya] = act[mya] + p*x
        return act
        
    
    def select_action(self):
        a = self.getExpectedUtility()
        ch = self.func(a)
        act = np.random.choice(self.env.tasks, p=ch)
        return act



class GeneralizedRegretMatchingPlayer(Player):
    
    def __init__(self, environnement, id, func = softmax, fadding_factor = 0, inertia_factor = 0):
        super().__init__( environnement, id)
        self.cumulated_reget = np.zeros(self.env.tasks.shape)
        self.precedent_action = random.randint(0, len(self.env.tasks))
        self.step = 0
        self.func = func
        self.fadding_factor = fadding_factor
        self.inertia_factor = inertia_factor

    def observe(self):
        pred_ac = self.env.getPrecedentActionsMatrix().T
        #self.cumulated_reget = self.cumulated_reget*(1-self.fadding_factor)
        for i in range(self.step, pred_ac.shape[0]):
            act = pred_ac[i]
            self.cumulated_reget[act[self.id]] = self.cumulated_reget[act[self.id]] + self.getRegret(act)
        self.step = pred_ac.shape[0]

    def getRegret(self, actions):
        moves_v = list(actions[:self.id]) + [slice(None, None, None)] + list(actions[self.id+1:])+ [self.id]
        u = self.env.utility[moves_v]
        return np.max(u) - u[actions[self.id]]
    
    def select_action(self):
        norm_regret = (self.cumulated_reget / self.step) if (self.step != 0 ) else self.cumulated_reget
        norm_regret = norm_regret.max()-norm_regret
        ch = self.func(norm_regret)
        act = np.random.choice(self.env.tasks, p=ch)
        #print("Regret : ", self.cumulated_reget)


        r = random.random()
        if(r < self.inertia_factor):
            logging.debug("INERTIA ! ")
            return self.precedent_action

        if(self.id == 2):
            logging.debug('Regret  '+str(self.cumulated_reget))
            logging.debug('norm_regret  '+str(norm_regret))
            logging.debug('Distribution  '+str(ch))
            logging.debug("Acting : "+ str(act))
        
        self.precedent_action = act
        return act
