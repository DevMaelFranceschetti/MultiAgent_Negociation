import numpy as np

def replaceAlloc(allocation, v, t):
    """ Compute the new allocation with task t asigned to vehicle v
    
    Parameters :
        allocation : List(int) the list of tasks allocades to each vehicle (in order)
        v : int, the vehicle id
        t : int, the task id
    
    Returns :
        List(int), the new allocation
    
    """
    return list(allocation[:v])+[t]+list(allocation[v+1:])

def getUtilityShape(nb_vehicles, nb_tasks):
    """ Compute the shape for this settings
    
    Parameters :
        nb_vehicles : int, the number of vehicles
        nb_tasks : int, the number of tasks
        
    Returns :
        a tuple containing the shape (tasks^vehicles * vehicles),
        that is the shape for the utility matrix.
        
    """
    list_dim = [nb_tasks]*nb_vehicles +[nb_vehicles]# matrix of shape tasks^vehicles * vehicles
    return tuple(list_dim)


def computeFrequency(proposals, tasks):
    """ Compute the empirical frequency of each proposal
    
    Parameters :
        proposals : List(int), the allocation proposed
        tasks : List(int) the list of task ids
        
    Returns : 
        List(float), the empirical frequency of each proposal
    
    """
    return [np.count_nonzero(np.array(proposals) == t)/len(proposals) for t in range(len(tasks))]



def computePartialFrequencyMatrix(utilities, frequencies, vehicles, tasks, v):
    """
        Compute the expected utility for vehicle v foreach task, considering for each 
        other vehicle a random allocation choice with probability equal to empirical frequency observed 
        
    """
    temp_vehicles = vehicles[:v] + vehicles[v+1:] # create a list of index without vehicle v
    temp_alloc = np.zeros([len(tasks)]*(len(vehicles)-1)) # create a 0 array of shape (vehicles-1)^task
    allAlloc = [x for x,_ in np.ndenumerate(temp_alloc)] # enumerate all possible allocations for these vehicles
    expectations = []
    for t in range(len(tasks)):
        expected = 0
        for alloc in allAlloc : # for each possible allocation for vehicles without v
            # compute proba for these vehicles to do this allocation : 
            proba = np.prod([frequencies[temp_vehicles[v]][alloc[v]] for v in range(len(temp_vehicles))])
            # recreating full allocation with v :
            index = [0]*len(vehicles)
            for i in range(len(temp_vehicles)) :
                index[temp_vehicles[i]] = alloc[i]
            index[v] = t
            # get the utility for v if it do task t with this allocation for the other vehicles
            utility = utilities[tuple(index)][v]
            expected+= utility * proba # add proba time the utility of v to the expectation
        expectations.append(expected)
    return expectations