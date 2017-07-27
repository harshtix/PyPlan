from agents import switching_bandit_framework
from bandits import e_bandit_alg


class EPolicySwitchingAgentClass(switching_bandit_framework.SwitchingBanditAgentClass):
    my_name = "0.5-Greedy Policy Switching Agent"

    def __init__(self, depth, num_pulls, policies):
        switching_bandit_framework.SwitchingBanditAgentClass.__init__(self, depth=depth,
                                                                      pulls_per_node=num_pulls,
                                                                      policies=policies,
                                                                      bandit_class=e_bandit_alg.EBanditAlgClass,
                                                                      bandit_parameters=0.5)

        self.agent_name = self.my_name + " (d={}, n={}, e=0.5, policies={})".format(depth, num_pulls,
                                                                                    [p.agent_name for p in policies])