# Ring-Star Metro Design Optimization
Exact and Heuristic Methods for the Ring-Star Problem (NP-Hard)

## Abstract

This project studies the **Ring-Star Problem (RSP)** applied to metro network design.  
The goal is to construct:

- a circular metro line (ring) connecting a subset of selected stations
- star-shaped assignments linking remaining stations to the nearest selected hub

We aim to minimize a weighted sum of:
- metro construction cost (ring edges)
- walking/assignment cost (star edges)

The problem is **NP-hard**, as it generalizes both the Traveling Salesman Problem (TSP) and the p-median problem.

We propose:
- An **exact MILP formulation (PLNE)** solved using PuLP + CPLEX
- A **constructive greedy heuristic**
- A **stochastic local search (SWAP metaheuristic)**

Experiments were conducted on TSPLIB benchmark instances.
