
from statisticalrl_learners.MABs import Agent
from statisticalrl_learners.MABs.utils import *
class Oracle(Agent):
    """Oracle"""
    def __init__(self,env):
        self.env=env
        nA = env.action_space.n
        Agent.__init__(self,nA,name="Oracle")
        self.policy = [self.env.bestarm]

    def reset(self,initstate=0):
        ()

    def play(self,state=0):
        return self.env.bestarm

    def update(self, state, action, reward, observation):
       ()