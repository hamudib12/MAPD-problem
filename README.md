# MAPD-problem

In the MAPD problem, a team of robots needs to pick up and deliver a set of packages. Each package has a pickup location, and a delivery location. The robots need to visit all pickup locations to pick up the packages, and then all the delivery locations to deliver the packages. This problem is repeatedly solved and implemented nowadays in automated warehouses, such as some operated by Amazon. A standard simplification is representing locations by graph nodes, and possible robot trajecteories between them by edges. In particular, in many implementations, as in this assignment, a 2D grid-shaped graph is assumed. Some of the grid edges may be blocked, either permenently or temporarily, known in advance in this assignment Initial robot locations are knowm. Packages to be delivered may appear at any time, with origin and delivery locations known in advance in this assignment. All the above is given in the input in a format specified below. The problem is to pick up and deliver all the packages as quickly as possible. This is equivalent to finding an appropriate shortest path in a graph. However, unlike standard shortest path problems in graphs, which have easy known efficient solution methods (e.g. the Dijkstra algorithm), here the problem is that there is more than 1 vertex to visit, and their order is not given. It utilizes various pathfinding algorithms to find optimal routes for agents, including Greedy Search, A* Search, and Real-time A* Search.

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [File Structure](#file-structure)
4. [Installation And Running Instructions](#installation-and-running-instructions)

## Introduction

The environment consists of an undirected graph with the general shape of a grid, i.e. vertice at integer locations (i,j) ranging from (0,0) to (X,Y) inclusive, with X and Y specified in the input. There are edges along the x and y axes between every pair of neighboring vertices in the x and y directions. However, some of these edges, as specified in the input, are initially blocked.

A robot agent (pickup and delivery robot) at a vertex automatically picks up a package at that vertex if there is one. A picked up package stays with the robot until the robot reaches the package's delivery location, upon which the packege is automatically delivered. Some unblocked edges, specified in the input, are known to be fragile, and become permanently blocked after an agent traverses them. Package initial locations and time of appearance are specified in the input, as well as target locations and delivery deadline. There is also another type of agent, that also travels the graph, but does not pick up or deliver any packages. Its only role is to block fragile edges by crossing them, and interfering. Both agents types can only do traverse and no-op actions. Each action takes 1 time unit. The action always succeeds if the edge to be traversed is unblocked and there is no other agent at the destination; otherwise the action behaves the same as no-op. The simulation ends when all packages have been delivered, or there is no path for any agent to pick up or deliver any more packages on time.

The simulator should keep track of time, the number of actions done by each agent, and the total number packages successfully delivered by each agent. For simplicity, we assume in this assignment that agents take turns, each move advancing the clock by 1, and do not move concurently.

## Features

- **Multiple Pathfinding Algorithms:** The system supports different pathfinding algorithms, including Greedy Search, A* Search, and Real-time A* Search, allowing users to choose the most suitable algorithm for their needs.
  
- **Dynamic Environment:** The environment may contain obstacles and fragile edges that can change over time. Agents must adapt to these changes to find optimal routes.

- **Real-time Simulation:** The system provides real-time simulation of package delivery, allowing users to visualize agent movements and monitor their performance.

## File Structure

The repository has the following file structure:

- **agents.py:** Defines different types of agents that navigate the environment.
- **environment.py:** Implements the environment in which agents operate, including obstacles, packages, and fragile edges.
- **graph.py:** Defines the graph data structure and provides methods for pathfinding algorithms.
- **packages.py:** Defines the Package class representing packages to be delivered.
- **simulator.py:** Contains the main simulation script that orchestrates the package delivery simulation.
- **minQueue.py:** Implements a minimum priority queue used in A* Search algorithm.
- **README.md:** This file, providing an overview of the project and instructions for usage.

## Installation And Running Instructions:

1. **Clone the Repository:**
```shell
git clone https://github.com/hamudib12/MAPD-problem
cd MAPD-problem
```

2. **Run the Application:**
```shell
python main.py
```
