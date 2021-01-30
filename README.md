# MultiAgent_Negociation
Python code for basic negociation algorithms in task allocation case.

What we can currently do with the code :
 - defining a random utility matrix for a wanted number of vehicles (agents) and tasks 
 - checking if an allocation is a Nash Equilibrium, if not finding one agent that can increase its utility unilaterally
 - finding the Best Response of an agent (the task that increases unilaterally its utility the most) for a fixed allocation of other agents
 - **running the Best Response Dynamics algorithm to find a Nash Equilibrium (if it exists)**
 - computing a partial frequency matrix from the passed proposals of other agents
 - **running the Fictitious Play algorithm**
 - computing the average regret vector of an agent at each negociation step
 - **running the Regret Matching algorithm**
 - **running the Spatial Adaptative Play algorithm**

Requirements : numpy, time (for execution time comparison)
