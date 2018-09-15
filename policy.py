import numpy as np
import random

from Config import *

def create_policy(policy):
  if policy == "greedy":
    return GreedyPolicy()
  elif policy == "softmax":
    return SoftMaxPolicy()
  elif policy == "random":
    return RandomPolicy()
  else:
    return None

class GreedyPolicy:
  def get_best_action(self, state_q):
    return np.argmax(state_q)

class RandomPolicy:
  def get_best_action(self, state_q):
    if random.random() > exploration_rate: # greedy action
      indices = np.where(state_q == state_q.max())
      return random.choice(indices[0])
    else:
      return random.choice([i for i in range(len(state_q))])

class SoftMaxPolicy:
  pass
