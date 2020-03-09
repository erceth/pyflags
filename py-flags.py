import math
import pygame as pg
from tank import Tank
from bullet import Bullet
from obstacle import Obstacle
from base import Base
from flag import Flag
from scoreboard import Scoreboard
import gameConsts

screen = gameConsts.screen

selectLast = -gameConsts.SELECT_ADD_TIME # negative to allow immediate select
selectedTanks = set()

bg = pg.image.load(gameConsts.MAP_BACKGROUND)
bg = pg.transform.scale(bg, (gameConsts.BACKGROUND_SIZE, gameConsts.BACKGROUND_SIZE))


def selectTank(tank):
  global selectLast
  global selectedTanks
  gameTime = pg.time.get_ticks()
  if gameTime - selectLast > gameConsts.SELECT_ADD_TIME:
    selectLast = gameTime
    for t in selectedTanks:
      t.unselect()
    selectedTanks.clear()
  selectedTanks.add(tank)
  tank.select()
              

def main():
    pg.init()
    gameObjects = []

    scoreboard = Scoreboard(gameConsts.players)

    for o in gameConsts.obstacles:
      gameObjects.append(Obstacle((o['x'], o['y']), o['size']))

    
    
    t1 = Tank(color = 'blue', position = (50, 50), number = 1)
    t2 = Tank(color = 'blue', position = (0, 50), number = 2)
    t3 = Tank(color = 'blue', position = (100, 50), number = 3)



    # after tanks puts them on top
    for p in gameConsts.players:
      gameObjects.append(Base(p['color'], (p['base']['x'], p['base']['y']), p['base']['size']))
      gameObjects.append(Flag(p['color'], (p['base']['x'], p['base']['y']), gameConsts.FLAG_SIZE))
    
    gameObjects.append(t1)
    gameObjects.append(t2)
    gameObjects.append(t3)



    clock = pg.time.Clock()
    done = False
    while not done:
      clock.tick(gameConsts.FPS)
      for event in pg.event.get():
          if event.type == pg.QUIT:
              done = True
          if event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            for t in selectedTanks:
              t.setDestination(pos)
          elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
              for t in selectedTanks:
                bullet = t.fire()
                gameObjects.append(bullet)
            if event.key == pg.K_1:
              selectTank(t1)
            if event.key == pg.K_2:
              selectTank(t2)
            if event.key == pg.K_3:
              selectTank(t3)
      # screen.fill(gameConsts.BACKGROUND_COLOR) # TODO: replace with grass
      for x in range(0, gameConsts.MAP_WIDTH, gameConsts.BACKGROUND_SIZE):
        for y in range(0, gameConsts.MAP_WIDTH, gameConsts.BACKGROUND_SIZE):
          screen.blit(bg, (x,y))

      
      scoreboard.update()
      for obj1 in gameObjects:
        for obj2 in gameObjects:
          if obj1 is obj2: continue
          if not(obj1.top > obj2.bottom or obj1.right < obj2.left or obj1.bottom < obj2.top or obj1.left > obj2.right):
            handleHit(obj1, obj2, gameObjects)
        if(obj1.markedForTermination):
          gameObjects.remove(obj1)
          del obj1
          continue
        if (isinstance(obj1, Tank)):
          checkWalls(obj1)
        obj1.update()
        obj1.getSprite().draw(screen)
        
      pg.display.flip()

def handleHit(o1, o2, gameObjects):
  if(isinstance(o1, Bullet) and isinstance(o2, Obstacle)): o1.terminate()
  if(isinstance(o1, Tank) and isinstance(o2, Obstacle) or isinstance(o1, Tank) and isinstance(o2, Tank)):
    xDiff = o2.position[0] - o1.position[0]
    yDiff = o2.position[1] - o1.position[1]
    if abs(abs(xDiff) - abs(yDiff)) < 3: # ignore exact corner collision. work around
      return
    angle = (math.atan2(-(xDiff), (yDiff)) * 180 / math.pi) % 360
    # print(angle)
    if(angle <= 225 and angle > 135):
      o1.preventMovement('up')
    elif(angle > 225 and angle <= 315):
      o1.preventMovement('right')
    elif (angle <= 45 or angle > 315):
      o1.preventMovement('down')
    else: #(angle > 45 and angle <= 135):
      o1.preventMovement('left')
  if(isinstance(o1, Bullet) and isinstance(o2, Tank) and (o1.color != o2.color or gameConsts.FRIENDLY_FIRE)):
    o1.terminate()
    o2.terminate()

def checkWalls(obj):
  if(obj.top <= 0):
    obj.preventMovement('up')
  elif(obj.bottom >= gameConsts.MAP_HEIGHT):
    obj.preventMovement('down')
  if(obj.right >= gameConsts.MAP_WIDTH):
    obj.preventMovement('right')
  elif(obj.left <= 0):
    obj.preventMovement('left')

if __name__ == '__main__':
    main()
    pg.quit()

# LEFT OFF