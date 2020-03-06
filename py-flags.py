# https://stackoverflow.com/questions/45889954/rotating-and-moving-a-sprite-in-pygame
import math
import pygame as pg
from tank import Tank
from bullet import Bullet
from obstacle import Obstacle
# import gameConsts


screen = pg.display.set_mode((800, 800))

selectLast = -500
selectedTanks = set()

def selectTank(tank):
  global selectLast
  global selectedTanks
  gameTime = pg.time.get_ticks()
  if gameTime - selectLast > 500:
    selectLast = gameTime
    for t in selectedTanks:
      t.unselect()
    selectedTanks.clear()
  selectedTanks.add(tank)
  tank.select()
              

def main():
    pg.init()
    #screen = pg.display.set_mode((800, 800)) # TODO: restore
    # One time paint
    

    gameObjects = [Obstacle((350, 400)), Obstacle((400, 400)), Obstacle((450, 400))]
    
    
    t1 = Tank(color = 'blue', position = (50, 50), number = 1, screen = screen)
    t2 = Tank(color = 'blue', position = (0, 50), number = 2, screen = screen)
    t3 = Tank(color = 'blue', position = (100, 50), number = 3, screen = screen)
    

    gameObjects.append(t1)
    gameObjects.append(t2)
    gameObjects.append(t3)

    clock = pg.time.Clock()
    done = False
    while not done:
        clock.tick(30)
        # print(len(gameObjects))
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
        screen.fill((30, 30, 30))
          

        

        for obj1 in gameObjects: # TODO: filter out sprites that can't move
          for obj2 in gameObjects:
            if obj1 is obj2: continue
            if not(obj1.top > obj2.bottom or obj1.right < obj2.left or obj1.bottom < obj2.top or obj1.left > obj2.right): # LEFT OFF
              handleHit(obj1, obj2, gameObjects)
          if(obj1.markedForTermination):
            gameObjects.remove(obj1)
            del obj1
            continue
          obj1.update()
          obj1.getSprite().draw(screen)
          

        pg.display.flip()

def handleHit(o1, o2, gameObjects):
  if(isinstance(o1, Bullet) and isinstance(o2, Obstacle)): o1.terminate()
  elif(isinstance(o1, Tank) and isinstance(o2, Obstacle) or isinstance(o1, Tank) and isinstance(o2, Tank)):
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

if __name__ == '__main__':
    main()
    pg.quit()

# LEFT OFF