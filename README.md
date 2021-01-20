# MultiAgent_Negociation
Python code for basic negociation algorithms for task allocation.

What we can currently do with the code :
 - defining a random utility matrix for a wanted number of vehicles (agents) and tasks 
 - checking if an allocation is a Nash Equilibrium, if not finding one agent that can increase its utility unilaterally
 - finding the Best Response of an agent (a new task that increase unilaterally its utility) for a fixed allocation of other agents
 - running the Best Response Dynamics algorithm to find a Nash Equilibrium (if it exists) using Best Response

Requirements : numpy only.
