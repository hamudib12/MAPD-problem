from state import State
from tree import Tree
from minheap import MinHeap

LIMIT = 10000
N_EXPANSIONS = 10
T = 0.00001


def g(vertex: Tree):
    return vertex.g


class Agent:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.curr_time = 0
        self.movements = 0
        self.expansions = 0
        self.score = 0
        self.env_packages = []
        self.to_deliver = []
        self.to_deliver1 = []
        self.act_seq = []

    def print_agent(self):
        print(f'agent time: {self.curr_time}')
        print(f'agent expansions: {self.expansions}')
        print(f'agent movements: {self.movements}')
        print(f'agent score: {self.score}')

    def formulate_problem(self, env):
        # check packages availability and packages that already delivered to their destination to update the state,
        # and formulate the problem.
        for i, package in enumerate(env.packages):
            if (package.x == self.x and package.y == self.y) and package.is_available(env.curr_time):
                package.mark_as_picked_up()
                # change the status to pick up, just if the agent is on it and it's status is available.
                self.to_deliver.append((package.d_x, package.d_y))
                self.env_packages.append(i)

        for i in self.env_packages:
            if env.packages[i].check_picked_up() and env.packages[i].arrive(self.x, self.y):
                if (self.x, self.y) in self.to_deliver:
                    self.to_deliver.remove((self.x, self.y))
                self.score += 1
                env.packages[i].mark_as_delivered()  # after marking p as delivered we won't use it again.
                # del env.packages[i] => delete the package, check if I need to make this process
                # del self.env_packages[i]

    def create_state(self, env):
        agent_position = (self.x, self.y)
        package_locations = dict()
        available_packages_start, available_packages_deliver = env.get_curr_packages()
        all_agent_packages = self.to_deliver + available_packages_start + available_packages_deliver
        for package in all_agent_packages:
            package_locations[package] = False
        state = State(env, agent_position, package_locations)
        return state

    def limited_search(self, env, fringe, limit):
        # fringe will insert the tree nodes, so it can detect the min f between all.
        expansion = 0
        init_state = self.create_state(env)
        start_node = Tree(init_state, None, 0)
        fringe.push(start_node)
        while not fringe.is_empty():
            curr_node = fringe.pop()
            node_state = curr_node.state
            node_state.visit()
            if expansion == limit or node_state.goal():
                # we have to delete the packages that has been delivered, otherwise it will be hard when more than
                # package in the same location!
                self.act_seq = curr_node.action_sequence()
                return expansion
            expansion += 1
            for move in node_state.env.expand_env(node_state.agent_position):
                neighbor_state = State(node_state.env, move,
                                       node_state.packages_locations)
                new_node = Tree(neighbor_state, curr_node, curr_node.g + 1)
                new_node.change_fragile()
                fringe.push(new_node)
        return expansion

    def limit_act(self, env, limit):
        self.formulate_problem(env)  # problem formulation
        if not self.act_seq:
            expansions = self.search(env, limit)
            self.expansions += expansions
            self.curr_time += T * expansions
            return
        prev_x, prev_y = self.x, self.y
        self.x, self.y = self.act_seq.pop()
        if ((prev_x, prev_y), (self.x, self.y)) in env.fragile_edges:
            env.add_blocked_edges(prev_x, prev_y, self.x, self.y)
            env.add_fragile_edges(prev_x, prev_y, self.x, self.y)
        self.movements += 1
        self.curr_time += 1

    def search(self, env, limit):
        pass

    def act(self, env):
        pass


class Greedy(Agent):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.symbol = 'G'

    def search(self, env, limit):
        init_queue = MinHeap(key_func=lambda tree: tree.h)
        return self.limited_search(env, init_queue, limit)

    def act(self, env):
        return self.limit_act(env, LIMIT)


class A_star(Agent):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.symbol = 'A'

    def search(self, env, limit):
        init_queue = MinHeap(key_func=lambda tree: tree.h + tree.g)
        return self.limited_search(env, init_queue, limit)

    def act(self, env):
        return self.limit_act(env, LIMIT)


class Real_time(Agent):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.symbol = 'R'

    def search(self, env, limit):
        init_queue = MinHeap(key_func=lambda tree: tree.h + tree.g)
        return self.limited_search(env, init_queue, limit)

    def act(self, env):
        return self.limit_act(env, N_EXPANSIONS)
