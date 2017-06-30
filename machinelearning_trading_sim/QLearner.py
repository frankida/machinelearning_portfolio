"""
Template for implementing QLearner  (c) 2015 Tucker Balch
"""

import numpy as np
import random as rand

class QLearner(object):

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):

        self.verbose = verbose
        self.num_actions = num_actions
        self.s = 0  # current state
        self.a = 0  # currect action
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna
        # self.q = np.ndarray(shape= (num_states, num_actions), dtype= float)  #all important qtable
        self.q = np.random.uniform(-1.0, 1.0, [num_states, num_actions])
        # self.q[0,1]=3
        # self.q[0,2]=4
        # self.q[0,3]=2
        # self.q[4,0]=1
        # self.q[4,1]=10
        # self.q[4,2]=4
        # self.q[4,3]=2


    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """

        self.s = s
        action = rand.randint(0, self.num_actions - 1)
        self.a = action

        if self.verbose: print "s =", s,"a =",action
        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        """

        self.q[self.s, self.a] = (1 - self.alpha) * self.q[self.s, self.a] + self.alpha * (r + self.gamma *
                                                                                           self.q[s_prime, np.argmax(
                                                                                               self.q[s_prime, :])])

        # create a random action or use the qtable
        if rand.uniform(0.0, 1.0) <= self.rar:  # going rogue
            action = rand.randint(0, self.num_actions - 1)  # choose the random direction
            self.rar = self.rar * self.radr  # decrease randomness
        else:
            action = np.argmax(self.q[s_prime, :])

        # Update state and action
        self.s = s_prime
        self.a = action

        if self.verbose: print "s =", s_prime, "a =", self.a, "r =",r
        return action

if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"
    # newlearner = QLearner()
    # print newlearner.q
    # print
    # print np.argmax(newlearner.q[0, :])
    # print newlearner.q[0, :]
    # print np.argmax(newlearner.q[4, :])

    # print rand.uniform(0.0, 1.0)
    # if rand.uniform(0.0, 1.0) <= newlearner.rar:  # going rogue
    #     a = rand.randint(0, 3)  # choose the random direction
