# MultiAgent_Negociation
Python code for basic negociation algorithms in task allocation case.

What we can currently do with the basic code (basic_algorithms.ipynb):
 - defining a random utility matrix for a given number of vehicles (agents) and tasks 
 - checking if an allocation is a Nash Equilibrium, if not finding one agent that can increase its utility unilaterally
 - finding the Best Response of an agent (the task that increases unilaterally its utility the most) for a fixed allocation of other agents
 - **running the Best Response Dynamics algorithm to find a Nash Equilibrium (if it exists) with homogeneous agents**
 - computing a partial frequency matrix from the passed proposals of other agents
 - **running the Fictitious Play algorithm with homogeneous agents**
 - computing the average regret vector of an agent at each negociation step
 - **running the Regret Matching algorithm with homogeneous agents**
 - **running the Spatial Adaptative Play algorithm with homogeneous agents**

What we can currently do with the advanced code (core and COCOMA_nego.ipynb) :
 - **running a negociation with heterogenous agents** (example : negociation with 1 Random, 1 Best Response and 1 Regret Matching agent)
 - other agent (Players) types have been added : Random, SpatialFictiousPlay, GeneralizedRegretMatchingPlayer.
 - defining a Utility Shared matrix for a given number of vehicles (agents) and tasks 
 - generate yaml experiment files to setup a lot of negociation combinations
 - run an experiment file and plot the total utility during the negociation

Requirements : **numpy**, **time** (for execution time comparison), **matplotlib** (for graphics), **threading** (for advanced simulation with multi-threading), **logging** (for debugging and prints)
