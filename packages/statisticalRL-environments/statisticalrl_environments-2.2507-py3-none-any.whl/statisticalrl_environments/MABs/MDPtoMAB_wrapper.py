

import numpy as np

class MABofMDP:
    def __init__(self, mdp, policies,max_step=np.infty):
        self.mdp_env = mdp
        self.policies = policies
        self.max_step = max_step

    def step(self, policy):
        cumreward = 0.
        done = False
        observation, reward, info  = self.mdp_env.reset()
        policy.reset()
        t = 0
        while (not done) and (t<self.max_step):
            action = policy.action(observation)  # Get action
            newobservation, reward, done, truncated, info = self.mdp_env.step(action)
            policy.update(observation, action, reward, newobservation)  # Update policy
            observation = newobservation
            cumreward += reward
            t += 1
        return cumreward #(0,cumreward,False,False,{})


