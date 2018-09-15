class Logger:
  def __init__(self, algo, policy, gran):
    self.entries = []
    self.ifle = open("logs/" + algo + "_" + policy + "_" + str(gran), "a")

  def add_entry(self, entry):
    self.entries.append(entry+'\n')

  def flush(self):
    self.ifle.writelines(self.entries)
    self.entries = []

  def close(self):
    self.flush()
    self.ifle.close()