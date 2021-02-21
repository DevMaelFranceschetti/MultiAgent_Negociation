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
    env = Environnement(n_tasks = 2,n_players = 2)
    #env.utility[0][1][2][0] = 1500
    #env.utility[0][1][2][1] = 1500
    #env.utility[0][1][2][2] = 1500

    env.utility[0][1][0] = 1500
    env.utility[0][1][1] = 1500

    P1 = RMPlayer(env, 0)
    P2 = RMPlayer(env, 1)
    #P3 = FPPlayer(env, 2)

    t = threading.Thread(name="Player "+str(P1.id), target=P1.getWorkerFunction(10,verbose=True))
    w = threading.Thread(name="Player "+str(P2.id), target=P2.getWorkerFunction(5,verbose=True))
    #s = threading.Thread(name="Player "+str(P3.id), target=P3.getWorkerFunction(5,verbose=True))

    w.start()
    t.start()
    #s.start()

    w.join()
    t.join()
    #s.join()

    print(env.is_EN())