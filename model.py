from pybrain.rl.learners.valuebased import ActionValueTable
from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners import Q
from pybrain.rl.experiments import Experiment
from pybrain.rl.explorers import EpsilonGreedyExplorer
from scipy import clip, asarray
from pybrain.rl.environments.task import Task
from pybrain.rl.environments.environment import Environment

av_table = ActionValueTable(5000000, 2)
# av_table = ActionValueTable(50000000, 3)
av_table.initialize(-1.0)

learner = Q(0.9, 0.99)
learner._setExplorer(EpsilonGreedyExplorer(0.1))
agent = LearningAgent(av_table, learner)


class ModelEnv(Environment):
    indim = 1
    outdim = 3

    discreteActions = True
    numActions = 1

    def __init__(self, world):
        self.world = world
        self.lastobs = 5.0

    def getSensors(self):
        # data = [self.world.closest_square(), self.world.player().y]
        # return data
        data = [self.world.closest_square()]
        print("Range: %s" % self.world.closest_square())
        return asarray(data)

    def performAction(self, action):
        print("Action: %s" % action[0])
        if action:
            self.world.player().jump()
        else:
            self.world.player().nojump()

    def reset(self):
        self.world.reset()

    def set_world(self, world):
        self.world = world


class ModelTask(Task):
    def __init__(self, env):
        self.env = env
        self.lastobs = 6.0
        self.sensor_limits = None
        self.actor_limits = None
        self.clipping = True
        self.lastreward = 6.0

    def getObservation(self):
        return self.env.getSensors()

    def getReward(self):
        if self.env.world.collided():
            score = -30
        else:
            score = self.env.world.player().jumped
        print("Score: %s" % score)
        return score
