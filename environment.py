import heapq
import itertools
from itertools import combinations

from graph import Graph
from packages import Package
from agents import Agent, Greedy, A_star, Real_time


def get_neighbors(node):
    x, y = node
    neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return neighbors


class Environment:
    def __init__(self):
        self.max_x = 0
        self.max_y = 0
        self.packages = []
        self.blocked_edges = set()
        self.fragile_edges = set()
        self.agents = []
        self.curr_time = 0  # time increment after every action.

    def read_input(self, input_file):  # read the input file as it required in the assignment.
        with open(input_file, 'r') as file:
            for line in file:
                parts = line.strip().split()

                if not parts:
                    continue

                elif parts[0] == "#X":
                    self.max_x = int(parts[1])
                elif parts[0] == "#Y":
                    self.max_y = int(parts[1])
                elif parts[0] == "#P":
                    package = Package(int(parts[1]), int(parts[2]), int(parts[3]), int(parts[5]), int(parts[6]),
                                      int(parts[7]))
                    self.packages.append(package)
                elif parts[0] == "#B":
                    self.add_blocked_edges(int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]))
                elif parts[0] == "#F":
                    self.add_fragile_edges(int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]))
                elif parts[0] == "#G":
                    agent = Greedy(int(parts[1]), int(parts[2]))
                    self.agents.append(agent)
                elif parts[0] == "#A":
                    agent = A_star(int(parts[1]), int(parts[2]))
                    self.agents.append(agent)
                elif parts[0] == "#R":
                    agent = Real_time(int(parts[1]), int(parts[2]))
                    self.agents.append(agent)

    def display(self):
        print("".join(['-'] * (8 * self.max_y + 1)), end='')
        curr_env_time = self.curr_time
        agent_time = 0
        agent_expansions = 0
        agent_score = 0
        agent_movement = 0
        for col in range(self.max_x + 1):
            edges = [' '] * (2 * self.max_y + 1)
            for row in (range(self.max_y + 1)):
                cell = '    '
                edges[row * 2] = '*'

                for i, package in enumerate(self.packages):
                    if package.s_time <= self.curr_time and (
                            package.status != 1 and package.status != 2 and (package.x, package.y) == (col, row)) or (
                            package.check_if_delivered() and (package.d_x, package.d_y) == (col, row)):
                        edges[row * 2] = str(i)
                for agent in self.agents:
                    if agent.x == col and agent.y == row:
                        edges[row * 2] = agent.symbol
                        agent_expansions = agent.expansions
                        agent_time = agent.curr_time
                        agent_score = agent.score
                        agent_movement = agent.movements

                if ((col, row), (col + 1, row)) in self.blocked_edges:
                    cell = 'B'
                elif ((col, row), (col + 1, row)) in self.fragile_edges:
                    cell = 'F'

                if ((col, row), (col, row + 1)) in self.blocked_edges:
                    edges[row * 2 + 1] = 'B'
                elif ((col, row), (col, row + 1)) in self.fragile_edges:
                    edges[row * 2 + 1] = 'F'
                print(cell, end='')
            print()
            print(" ".join(edges))
        print()
        print(f'environment time: {curr_env_time}')
        print(f'agent time: {agent_time}')
        print(f'agent expansions: {agent_expansions}')
        print(f'agent movements: {agent_movement}')
        print(f'agent score: {agent_score}')
        print("".join(['-'] * (8 * self.max_y + 1)))

    def display2(self):
        print("".join(['-'] * (8 * self.max_x + 1)), end='')
        curr_env_time = self.curr_time
        agent_time = 0
        agent_expansions = 0
        agent_score = 0
        agent_movement = 0
        for row in reversed(range(self.max_y + 1)):
            edges = [' '] * (2 * self.max_x + 1)
            for col in range(self.max_x + 1):
                cell = '    '
                edges[col * 2] = '*'

                for i, package in enumerate(self.packages):
                    if package.s_time <= self.curr_time and (
                            package.status != 1 and package.status != 2 and (package.x, package.y) == (col, row)) or (
                            package.check_if_delivered() and (package.d_x, package.d_y) == (col, row)):
                        edges[col * 2] = str(i)
                for agent in self.agents:
                    if agent.x == col and agent.y == row:
                        edges[col * 2] = agent.symbol
                        agent_expansions = agent.expansions
                        agent_time = agent.curr_time
                        agent_score = agent.score
                        agent_movement = agent.movements

                if ((col, row), (col + 1, row)) in self.blocked_edges:
                    edges[col * 2 + 1] = 'B'
                elif ((col, row), (col + 1, row)) in self.fragile_edges:
                    edges[col * 2 + 1] = 'F'

                if ((col, row), (col, row + 1)) in self.blocked_edges:
                    cell = 'B'
                elif ((col, row), (col, row + 1)) in self.fragile_edges:
                    cell = 'F'
                print(cell, end='')
            print()
            print(" ".join(edges))
        print()
        print(f'environment time: {curr_env_time}')
        print(f'agent time: {agent_time}')
        print(f'agent expansions: {agent_expansions}')
        print(f'agent movements: {agent_movement}')
        print(f'agent score: {agent_score}')
        print("".join(['-'] * (8 * self.max_x + 1)))

        def display2(self, filename='output.txt'):
            with open(filename, 'w') as file:
                file.write("".join(['-'] * (8 * self.max_x + 1)) + '\n')
                curr_env_time = self.curr_time
                agent_time = 0
                agent_expansions = 0
                agent_score = 0
                agent_movement = 0
                for row in reversed(range(self.max_y + 1)):
                    edges = [' '] * (2 * self.max_x + 1)
                    for col in range(self.max_x + 1):
                        cell = '    '
                        edges[col * 2] = '*'

                        for i, package in enumerate(self.packages):
                            if package.s_time <= self.curr_time and (
                                    package.status != 1 and package.status != 2 and (package.x, package.y) == (
                            col, row)) or (
                                    package.check_if_delivered() and (package.d_x, package.d_y) == (col, row)):
                                edges[col * 2] = str(i)
                        for agent in self.agents:
                            if agent.x == col and agent.y == row:
                                edges[col * 2] = agent.symbol
                                agent_expansions = agent.expansions
                                agent_time = agent.curr_time
                                agent_score = agent.score
                                agent_movement = agent.movements

                        if ((col, row), (col + 1, row)) in self.blocked_edges:
                            edges[col * 2 + 1] = 'B'
                        elif ((col, row), (col + 1, row)) in self.fragile_edges:
                            edges[col * 2 + 1] = 'F'

                        if ((col, row), (col, row + 1)) in self.blocked_edges:
                            cell = 'B'
                        elif ((col, row), (col, row + 1)) in self.fragile_edges:
                            cell = 'F'
                        file.write(cell)
                    file.write('\n')
                    file.write(" ".join(edges) + '\n')

                file.write('\n')
                file.write(f'environment time: {curr_env_time}\n')
                file.write(f'agent time: {agent_time}\n')
                file.write(f'agent expansions: {agent_expansions}\n')
                file.write(f'agent movements: {agent_movement}\n')
                file.write(f'agent score: {agent_score}\n')
                file.write("".join(['-'] * (8 * self.max_x + 1)) + '\n')

    def display3(self, filename='output.txt'):
        with open(filename, 'a') as file:
            file.write("".join(['-'] * (8 * self.max_x + 1)) + '\n')
            curr_env_time = self.curr_time
            agent_time = 0
            agent_expansions = 0
            agent_score = 0
            agent_movement = 0
            for row in reversed(range(self.max_y + 1)):
                edges = [' '] * (2 * self.max_x + 1)
                for col in range(self.max_x + 1):
                    cell = '    '
                    edges[col * 2] = '*'

                    for i, package in enumerate(self.packages):
                        if package.s_time <= self.curr_time and (
                                package.status != 1 and package.status != 2 and (package.x, package.y) == (
                        col, row)) or (
                                package.check_if_delivered() and (package.d_x, package.d_y) == (col, row)):
                            edges[col * 2] = str(i)
                    for agent in self.agents:
                        if agent.x == col and agent.y == row:
                            edges[col * 2] = agent.symbol
                            agent_expansions = agent.expansions
                            agent_time = agent.curr_time
                            agent_score = agent.score
                            agent_movement = agent.movements

                    if ((col, row), (col + 1, row)) in self.blocked_edges:
                        edges[col * 2 + 1] = 'B'
                    elif ((col, row), (col + 1, row)) in self.fragile_edges:
                        edges[col * 2 + 1] = 'F'

                    if ((col, row), (col, row + 1)) in self.blocked_edges:
                        cell = 'B'
                    elif ((col, row), (col, row + 1)) in self.fragile_edges:
                        cell = 'F'
                    file.write(cell)
                file.write('\n')
                file.write(" ".join(edges) + '\n')

            file.write('\n')
            file.write(f'environment time: {curr_env_time}\n')
            file.write(f'agent time: {agent_time}\n')
            file.write(f'agent expansions: {agent_expansions}\n')
            file.write(f'agent movements: {agent_movement}\n')
            file.write(f'agent score: {agent_score}\n')
            file.write("".join(['-'] * (8 * self.max_x + 1)) + '\n')

    def add_blocked_edges(self, x1, y1, x2, y2):
        # add blocked edges to the set of edges from both sides so agent can keep tracking it.
        self.blocked_edges.add(((x1, y1), (x2, y2)))
        self.blocked_edges.add(((x2, y2), (x1, y1)))

    def add_fragile_edges(self, x1, y1, x2, y2):
        # add fragile edges to the set of edges from both sides so agent can keep tracking it.
        self.fragile_edges.add(((x1, y1), (x2, y2)))
        self.fragile_edges.add(((x2, y2), (x1, y1)))

    def remove_fragile_edges(self, x1, y1, x2, y2):
        # we use this function when agent traverse throw it.
        self.fragile_edges.remove(((x1, y1), (x2, y2)))
        self.fragile_edges.remove(((x2, y2), (x1, y1)))

    def add_agent(self, agent):
        self.agents.append(agent)

    def get_curr_packages(self):
        # return package that are available.
        curr_packages_start = []
        curr_packages_deliver = []
        for package in self.packages:
            if package.is_available(self.curr_time):
                curr_packages_start.append((package.x, package.y))
                curr_packages_deliver.append((package.d_x, package.d_y))
        return curr_packages_start, curr_packages_deliver

    def curr_packages_location(self):
        pick_to_deliver = {}
        for package in self.packages:
            if package.is_available():
                pick_to_deliver[(package.x, package.y)] = (package.d_x, package.d_y)
        return pick_to_deliver

    def check_availability(self, location):
        # check availability in the grid.
        return 0 <= location[0] <= self.max_x and 0 <= location[1] <= self.max_y

    def can_enter(self, p1, p2):
        # check if between the positions in the grid there is no block edge, so the agent can traverse throw it.
        return (p1, p2) not in self.blocked_edges

    def shortest_path(self, start, target):
        # return shortest path between two things in the grid.
        priority_queue = [(0, start)]
        cost_so_far = {start: 0}
        while priority_queue:
            current_cost, current_node = heapq.heappop(priority_queue)
            if current_node == target:
                return current_cost
            neighbors = get_neighbors(current_node)
            for neighbor in neighbors:
                if self.check_availability(neighbor) and self.can_enter(current_node, neighbor):
                    next_cost = current_cost + 1
                    if (neighbor not in cost_so_far) or (next_cost < cost_so_far[neighbor]):
                        cost_so_far[neighbor] = next_cost
                        new_node = (next_cost, neighbor)
                        heapq.heappush(priority_queue, new_node)
        return -1

    def is_edge_blocked(self, node1, node2):
        # check if the edge is blocked.
        edge1 = (node1, node2)
        edge2 = (node2, node1)
        return (edge1 in self.blocked_edges) or (edge2 in self.blocked_edges)

    def no_interaction(self, neighbor):
        # check there is no interaction between agents.
        for agent in self.agents:
            location = (agent.x, agent.y)
            if neighbor == location:
                return False
        return True

    def expand_env(self, position):
        # get the neighbors of the position in the env so, we can expand agent move.
        # try to check if there is an agent in that position!!!!!!!!!!!!!!!!!!!!!!
        move = []
        neighbors = get_neighbors(position)
        for neighbor in neighbors:
            if self.check_availability(neighbor) and self.can_enter(position, neighbor) and self.no_interaction(
                    neighbor):
                move.append(neighbor)

        return move

    def to_graph(self, vertices_list):
        # make a graph from the environment that will calculate the shortest paths between all locations, so it will
        # be easy to detect mst.
        new_graph = Graph({})

        # Add vertices to the new graph
        for vertex in vertices_list:
            new_graph.add_vertex(vertex)

        # Use itertools.combinations to generate unique pairs of vertices
        visited_pairs = set()
        for vertex1, vertex2 in combinations(new_graph.get_vertices(), 2):
            # Check if the pair has been visited before
            if (vertex1, vertex2) in visited_pairs or (vertex2, vertex1) in visited_pairs:
                continue

            weight = self.shortest_path(vertex1, vertex2)
            if weight >= 0:
                new_graph.add_edge(vertex1, vertex2, weight)

            # Mark the pair as visited
            visited_pairs.add((vertex1, vertex2))

        return new_graph
