import numpy as np

from state import State
from Car import NonStopCar
from Config import *

class QLearner:
  def __init__(self):
    self.QIDic = {}
    self.qtable = np.zeros([27 ** 5, 3])  # number of states = sensor_length/10 + 2 (0 and MAX)


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
    print(cente)
    print(car_copy.angle)
    print(car_copy.sensors)
    distances = track.measure_intersections((c1,c2), car_copy.sensors)

    # print(distances)

    return State(distances)

  def learn(self, state, action, new_state, reward):
    # print("current=" + str(state.measurings))
    # print("new=" + str(new_state.measurings))
    # print(np.max(self.qtable[self.state_to_number(new_state), :]))
    # print (self.qtable[self.state_to_number(state), action])
    # print("==============")
    self.qtable[self.state_to_number(state), action] += lr * (reward + y * np.max(self.qtable[self.state_to_number(new_state), :]) - self.qtable[self.state_to_number(state), action])

  def log_statistics(self, history, track_number):
    with open("q_learning_stats_"+str(track_number), "w") as outfile:
      outfile.write('\n'.join(history))