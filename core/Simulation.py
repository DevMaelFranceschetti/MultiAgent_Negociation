import threading
import time
import logging
from Environnement import *
from Simulation import *
from Player import *
from utils import *


logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)) : %(message)s',
                    )









if(__name__ == "__main__"):
    env = Environnement(n_tasks = 3,n_players = 3)
    env.utility[0][1][2][0] = -1500
    env.utility[0][1][2][1] = 1500
    env.utility[0][1][2][2] = -1500

    P1 = FPPlayer(env, 0)
    P2 = FPPlayer(env, 1)
    P3 = FPPlayer(env, 2)

    t = threading.Thread(name="Player "+str(P1.id), target=P1.getWorkerFunction(100,verbose=True))
    w = threading.Thread(name="Player "+str(P2.id), target=P2.getWorkerFunction(100,verbose=True))
    s = threading.Thread(name="Player "+str(P3.id), target=P3.getWorkerFunction(100,verbose=True))

    w.start()
    t.start()
    s.start()

    w.join()
    t.join()
    s.join()
    print("Historique des différents agents: ")

    for agent in env.hist:
        print("Agent : ",agent)
        #print(np.array(env.hist[agent]))

    #print(env.getFreqencyMatrix())
    print(env.is_EN())