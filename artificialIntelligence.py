from tank import Tank
from bullet import Bullet
from obstacle import Obstacle
from base import Base
from flag import Flag
import random
import math

SIGHT_ENEMY_RANGE = 600
FIRE_ENEMY_RANGE = 300

class AI():
  def __init__(self, color, gameObjects):
    self.color = color
    self.myTanks = []
    self.enemyTanks = []
    self.myFlag = None
    self.enemyFlags = []
    self.myBase = None
    self.enemyBases = []
    for go in gameObjects:
      if (isinstance(go, Tank)):
        if go.color == self.color:
          self.myTanks.append(AITank(go))
        else:
          self.enemyTanks.append(go)
      elif (isinstance(go, Flag)):
        if go.color == self.color:
          self.myFlag = go
        else:
          self.enemyFlags.append(go)
      elif (isinstance(go, Base)):
        if go.color == self.color:
          self.myBase = go
        else:
          self.enemyBases.append(go)

  def control(self):
    for t in self.myTanks:
      if (isinstance(t.tank.flag, Flag)):
        t.target = None
        t.tank.setDestination(self.myBase.position)
        return
      tankTarget = {'dist': math.inf, 'enemyTank': None}
      for e in self.enemyTanks:
        dist = math.hypot(e.position[0] - t.tank.position[0], e.position[1] - t.tank.position[1])
        if (not e.respawn and dist < SIGHT_ENEMY_RANGE and dist < tankTarget['dist']):
          tankTarget['enemyTank'] = e
          tankTarget['dist'] = dist
        if(tankTarget['enemyTank'] is not None):
          t.tank.setDestination(tankTarget['enemyTank'].position)
          if(tankTarget['dist'] < FIRE_ENEMY_RANGE):
            t.tank.fire()
          return
          
          
        




      if (t.target == None):
        t.target = random.choice(self.enemyFlags)
      for f in self.enemyFlags:
        t.tank.setDestination(f.position)


class AITank():
  def __init__(self, tank):
    self.target = None
    self.tank = tank
  def setTarget(self, t):
    self.target = t
