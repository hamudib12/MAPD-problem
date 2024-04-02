import copy


class State:
    def __init__(self, env, agent_position, packages_locations: dict):
        self.env = copy.deepcopy(env)
        self.agent_position = agent_position  # to know where the agent stand now.
        self.packages_locations = packages_locations  # {(x,y) -> bool}
        self.unvisited = self.unvisited_packages()
        if agent_position not in self.unvisited:  # add the agent to the packages to create the graph.
            self.unvisited.append(agent_position)
        self.graph = env.to_graph(self.unvisited)

    def visit(self):
        if self.agent_position in self.packages_locations.keys():
            self.packages_locations[self.agent_position] = True

    def unvisited_packages(self):
        packages = [pickup for pickup, value in self.packages_locations.items() if not value]
        return packages

    def num_of_unvisited(self):
        unvisited = self.unvisited_packages()
        return len(unvisited)

    def goal(self):
        return not self.packages_locations or all(self.packages_locations.values())
        # agent finish when all packages have been visited, or there is no packages to be visited.

    def calculate_mst(self):
        mst = self.graph.create_mst()
        return mst.mst_weight()
