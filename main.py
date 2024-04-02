from minQueue import MinPriorityQueue
from envSimulator import Simulator

if __name__ == '__main__':
    open('output.txt', 'w').close()
    envSimulator = Simulator("problem_instance.txt")
    envSimulator.simulate()
    envSimulator.env.display3()
    # for agent in envSimulator.env.agents:
    #   print(agent.print_agent())
