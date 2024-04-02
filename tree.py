class Tree:
    def __init__(self, state, parent, g):
        self.state = state
        self.parent = parent
        self.g = g
        self.h = state.calculate_mst()

    def action_sequence(self):
        seq = []
        curr_node = self
        while curr_node.parent is not None:
            seq.append(curr_node.state.agent_position)
            curr_node = curr_node.parent
        return seq
        # seq = [self.state.agent_position]
        # curr_node = self
        # while curr_node.parent is not None:
        #     curr_node = curr_node.parent
        #     seq.append(curr_node.state.agent_position)
        #
        # return seq[::-1]

    def change_fragile(self):
        prev_position = self.parent.state.agent_position
        x1, y1 = prev_position
        curr_position = self.state.agent_position
        x2, y2 = curr_position
        if (prev_position, curr_position) in self.state.env.fragile_edges:
            self.state.env.add_blocked_edges(x1, y1, x2, y2)
            self.state.env.remove_fragile_edges(x1, y1, x2, y2)
            self.state.graph = self.state.env.to_graph(self.state.unvisited)
            self.h = self.state.calculate_mst()

    def g(self):
        return self.g

    def h(self):
        return self.h

    def __lt__(self, other):
        # Define the less-than comparison for the priority queue
        if (self.h + self.g) == (other.h + other.g):
            first_package = None
            first_package_other = None
            for package in self.state.packages_locations:
                if not self.state.packages_locations[package]:
                    first_package = package
            for package in other.state.packages_locations:
                if not other.state.packages_locations[package]:
                    first_package_other = package
            curr_weight = None
            other_weight = None
            if first_package and first_package_other is not None:
                curr_weight = self.state.graph.get_weight(self.state.agent_position, first_package)
                other_weight = other.state.graph.get_weight(other.state.agent_position, first_package_other)
            if curr_weight and other_weight is not None:
                return other_weight - curr_weight
        return (other.g + other.h) - (self.h + self.g)
