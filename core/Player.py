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
        



class FPPlayer(Player):
    
    def select_action(self):
        return np.argmax(self.env.getExpectationPlayer(self.id))