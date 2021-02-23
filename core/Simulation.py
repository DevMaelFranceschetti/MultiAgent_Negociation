import threading
import time
import logging
from Environnement import *
from Simulation import *
from Player import *
from utils import *
from Functions import *

logging.basicConfig(level=logging.ERROR,
                    format='[%(levelname)s] (%(threadName)) : %(message)s',
                    )









if(__name__ == "__main__"):
    env = Environnement(n_tasks = 3,n_players = 3)
    env.utility[0][1][2][0] = 1500
    env.utility[0][1][2][1] = 1500
    env.utility[0][1][2][2] = 1500

    #env.utility[0][1][0] = 20
    #env.utility[0][1][1] = 20
#
    P1 = GeneralizedRegretMatchingPlayer(env, 0, inertia_factor = 0.1, fadding_factor = 0.2)
    P2 = GeneralizedRegretMatchingPlayer(env, 1, inertia_factor = 0.1, fadding_factor = 0.2)
    P3 = GeneralizedRegretMatchingPlayer(env, 2, inertia_factor = 0.1, fadding_factor = 0.2)

    for i in range(0,10):
        print("===")
        t = threading.Thread(name="Player "+str(P1.id), target=P1.getWorkerFunction(10,verbose=False))
        w = threading.Thread(name="Player "+str(P2.id), target=P2.getWorkerFunction(10,verbose=False))
        s = threading.Thread(name="Player "+str(P3.id), target=P3.getWorkerFunction(10,verbose=False))
        w.start()
        t.start()
        s.start()
        w.join()
        t.join()
        s.join()
        print("===")

    print(env.is_EN())