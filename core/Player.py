import numpy as np
from Environnement import *
import threading
import time
import logging

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


class RMPlayer(Player):

    def __init__(self, environnement, id):
        super().__init__( environnement, id)
        self.cumulated_reget = np.zeros(self.env.tasks.shape)
        self.step = 0
        pass

    def observe(self):
        pred_ac = self.env.getPrecedentActionsMatrix().T
        for i in range(self.step, pred_ac.shape[0]):
            act = pred_ac[i]
            self.cumulated_reget[act[self.id]] = self.cumulated_reget[act[self.id]] + self.getRegret(act)
        self.step = pred_ac.shape[0]

    def getRegret(self, actions):
        moves_v = list(actions[:self.id]) + [slice(None, None, None)] + list(actions[self.id+1:])+ [self.id]
        u = self.env.utility[moves_v]
        return np.max(u) - u[actions[self.id]]
    
    
    def select_action(self):
        return np.argmin(self.cumulated_reget)