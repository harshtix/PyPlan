from agents import recursive_bandit_framework
from bandits import uniform_bandit


class SparseSamplingAgent(recursive_bandit_framework.RecursiveBanditFramework):
    base_name = "Sparse Sampling Agent"

    def __init__(self, depth, pulls_per_node, evaluation=None):
        recursive_bandit_framework.RecursiveBanditFramework.__init__(self, depth=depth, pulls_per_node=pulls_per_node,
                                                                     evaluation=evaluation,
                                                                     bandit_class=uniform_bandit.UniformBandit)
        self.name = self.base_name + " (d={}, pulls per node={})".format(depth, pulls_per_node)
