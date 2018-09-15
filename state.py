class State:
  '''
  this class would hold the game snapshot, used by the
  q learner to index it's table, as well as reward function
  to determine the reward of that particular state.

  :var rectPosition
  :var circlePosition
  '''

  def __init__(self, sensor_measurings, gran=50):
    self.measurings = sensor_measurings
    self.granularity = gran

  def hash(self):
    result = 0
    for measure in self.measurings:
      result *= 100
      if measure is None:
        result += 50
      else:
        result += int(measure / self.granularity)

    return result