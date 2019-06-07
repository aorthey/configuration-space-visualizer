
class World(object):
  def plotObstacles(self, ax):
      raise NotImplementedError
  def plotRobotAtConfig(self, ax, q):
      raise NotImplementedError
  def isFeasible(self, q):
      raise NotImplementedError
  def getName(self):
      raise NotImplementedError

