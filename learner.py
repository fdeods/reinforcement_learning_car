import numpy as np

from policy import *
from state import State
from Car import NonStopCar
from Config import *

def create_learner(learner, policystr):
  policy = create_policy(policystr)
  if learner == "qlearning":
    return QLearner(policy)
  elif learner == "sarsa":
    return SarsaLearner(policy)
  else:
    return None

class QLearner:
  def __init__(self, policy):
    self.QIDic = {}
    self.qtable = np.zeros([27 ** 5, 3])  # number of states = sensor_length/10 + 2 (0 and MAX)
    self.policy = policy

  def get_policy_action(self, state):
    return self.policy.get_best_action(self.qtable[self.state_to_number(state), :])

  def get_best_action(self, state):
    return np.argmax(self.qtable[self.state_to_number(state), :])

  def calculate_score(self, collision_detected):
    if collision_detected:
      return -100
    else:
      return 1

  def state_to_number(self, state):
    n = state.hash()

    if n in self.QIDic:
        return self.QIDic[n]
    else:
        if len(self.QIDic):
            maximum = max(self.QIDic, key=self.QIDic.get)  # Just use 'min' instead of 'max' for minimum.
            self.QIDic[n] = self.QIDic[maximum] + 1
        else:
            self.QIDic[n] = 1
    return self.QIDic[n]

  def new_state_after_action(self, state, action, car, track):
    # actions: 2 - turn left, 0 - stay, 1 - turn right
    car_copy = NonStopCar((0,0))
    car_copy.position.x = car.position.x
    car_copy.position.y = car.position.y
    car_copy.velocity.x = car.velocity.x
    car_copy.velocity.y = car.velocity.y
    car_copy.angle = car.angle

    for i in range(states_granularity):
      car_copy.update(action)

    cente = (c1, c2) = car_copy.position * ppu
    distances = track.measure_intersections((c1,c2), car_copy.sensors)

    # print(distances)

    return State(distances)

  def learn(self, state, action, new_state, reward):
    self.qtable[self.state_to_number(state), action] += lr * (reward + y * np.max(self.qtable[self.state_to_number(new_state), :]) - self.qtable[self.state_to_number(state), action])

  def log_statistics(self, history, track_number):
    with open('logs/q_stats_'+str(track_number), "w") as outfile:
      outfile.write('\n'.join(history))


class SarsaLearner:
  def __init__(self, policy):
    self.QIDic = {}
    self.qtable = np.zeros([10 ** 5, 3])  # number of states = sensor_length/10 + 2 (0 and MAX)
    self.policy = policy

  def get_policy_action(self, state):
    return self.policy.get_best_action(self.qtable[self.state_to_number(state), :])

  def get_best_action(self, state):
    return np.argmax(self.qtable[self.state_to_number(state), :])

  def calculate_score(self, collision_detected):
    if collision_detected:
      return -100
    else:
      return 0

  def state_to_number(self, state):
    n = state.hash()

    if n in self.QIDic:
        return self.QIDic[n]
    else:
        if len(self.QIDic):
            maximum = max(self.QIDic, key=self.QIDic.get)  # Just use 'min' instead of 'max' for minimum.
            self.QIDic[n] = self.QIDic[maximum] + 1
        else:
            self.QIDic[n] = 1
    return self.QIDic[n]

  def new_state_after_action(self, state, action, car, track, gran):
    # actions: 2 - turn left, 0 - stay, 1 - turn right
    car_copy = NonStopCar((0,0))
    car_copy.position.x = car.position.x
    car_copy.position.y = car.position.y
    car_copy.velocity.x = car.velocity.x
    car_copy.velocity.y = car.velocity.y
    car_copy.angle = car.angle

    for i in range(states_granularity):
      car_copy.update(action)

    cente = (c1, c2) = car_copy.position * ppu
    distances = track.measure_intersections((c1,c2), car_copy.sensors)

    # print(distances)

    return State(distances, gran)

  def learn(self, state, action, new_state, reward):
    new_action = self.get_best_action(new_state)
    self.qtable[self.state_to_number(state), action] += lr * (reward + y * self.qtable[self.state_to_number(new_state), new_action] - self.qtable[self.state_to_number(state), action])
    return new_action

  def log_statistics(self, history, track_number, gran):
    with open('logs/sarsa_stats_'+str(track_number)+"_"+str(gran), "w") as outfile:
      outfile.write('\n'.join(history))