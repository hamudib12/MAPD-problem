from environment import Environment


class Simulator:
    def __init__(self, input_file):
        self.env = Environment()
        self.env.read_input(input_file)

    def simulate(self):
        while self.env.packages and not all(package.check_if_delivered() for package in self.env.packages):
            self.env.display3()
            for agent in self.env.agents:
                agent.act(self.env)
            self.env.curr_time += 1
