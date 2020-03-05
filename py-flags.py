# https://stackoverflow.com/questions/45889954/rotating-and-moving-a-sprite-in-pygame
import math
import pygame as pg
from pygame.math import Vector2

screen = pg.display.set_mode((800, 800))

class GameObject(pg.sprite.Sprite):
    def __init__(self, image, position, size, direction = (0, 0), speed = 0, angle = 0):
        self.image = image
        self.position = Vector2(position)
        self.size = size
        self.halfHeight = (self.size[1] / 2)
        self.halfWidth = (self.size[0] / 2)
        self.direction = Vector2(direction)
        self.speed = speed
        self.angle = angle
        self.sprite = None
        self.image = pg.image.load(self.image)
        self.image = pg.transform.scale(self.image, self.size)
        self.original_image = self.image
        self.rect = self.image.get_rect(center=position)
        self.angleSpeed = 0
        super(GameObject, self).__init__() # TODO: move to bottom of init?
        self.sprite = pg.sprite.RenderPlain((self))
        self.top = None
        self.right = None
        self.bottom = None
        self.left = None
        self.preventDirection = {'up': False, 'right': False, 'down': False, 'left': False} # TODO: make sure I consistently do North East South West
        self.radius = self.halfWidth/.7071 # cosine(45)
        self.updateSides()
        self.markedForTermination = False

    def update(self):
        if self.angleSpeed != 0:
            # Rotate the direction vector and then the image.
            self.direction.rotate_ip(self.angleSpeed)
            self.angle = (self.angle + self.angleSpeed) % 360
            self.image = pg.transform.rotate(self.original_image, -self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
        # Update the position vector and the rect.
        newDirection = self._getPreventedDirection(self.direction)
        self.position += newDirection * self.speed
        self.preventDirection = {'up': False, 'right': False, 'down': False, 'left': False} # reset
        self.updateSides()
        self.rect.center = self.position

    def getSprite(self):
      return self.sprite
    
    def updateSides(self):
      self.top = self.position[1] - self.halfHeight
      self.bottom = self.position[1] + self.halfHeight
      self.left = self.position[0] - self.halfWidth
      self.right = self.position[0] + self.halfWidth

    def terminate(self):
      self.markedForTermination = True

    def _getPreventedDirection(self, direction): # TODO: comb through code and be consistent in not getters, setters, and private variables
      x,y = direction
      if(self.preventDirection['up']):
        y = max(y,0)
      if(self.preventDirection['right']):
        x = min(x,0)
      if(self.preventDirection['down']):
        y = min(y,0)
      if(self.preventDirection['left']):
        x = max(x,0)
      return Vector2((x,y))
      

    def preventMovement(self, direction):
      self.preventDirection[direction] = True

class Tank(GameObject):
  def __init__(self, color, position, number):
      # general attributes
      image = f'img/{color}_tank.png'
      size = (50, 50) # TODO read from game constant
      direction = (1,0) # TODO randomize
      speed = 4 # TODO read from game constant
      angle = 0 # TODO randomize

      # specific to tank
      self.color = color
      self.max_rotation = 10 # TODO read from game constant
      self.destination = position
      self.selected = False
      self.number = number
      self.font = pg.font.SysFont('Times New Roman', 32)
      self.text = self.font.render(str(self.number), False, (0,234,0))

      super().__init__(image, position, size, direction, speed, angle)
  
  def update(self):
    destVector = Vector2(self.destination[0] - self.position[0], self.destination[1] - self.position[1])
    angle = self.direction.angle_to(destVector)
    if (angle > 180): # compensate for angle_to picking the wrong direction in these cases
      angle = -360 + angle
    if (angle < -180):
      angle = 360 + angle
    self.angleSpeed = self.getMaxRotation(angle)
    super().update()
    if self.selected:
      pg.draw.circle(screen, (0,234,0), self.position, self.radius, 1) # TODO: put select color as a CONST
    screen.blit(self.text, (self.position[0], self.position[1] + self.radius))
  
  def getMaxRotation(self, desiredAngle):
    if (desiredAngle > self.max_rotation): # TODO create constant max turn variable
      return self.max_rotation
    elif (desiredAngle < -self.max_rotation):
      return -self.max_rotation
    else:
      return desiredAngle

  def setDestination(self, pos):
    self.destination = pos
  
  def fire(self):
    frontOfTank = self.position + self.direction * self.radius
    bullet = Bullet(self.color, frontOfTank, self.direction, self.angle)
    return bullet
  
  def select(self):
    self.selected = True

  def unselect(self):
    self.selected = False

class Bullet(GameObject):
  def __init__(self, color, position, direction, angle):
    image = f'img/{color}_tank.png' # TODO make bullet pictures
    size = (6, 6) # TODO read from game constant
    speed = 10 # TODO read from game conts

    super().__init__(image, position, size, direction, speed, angle)

  def update(self):
    x, y = self.position
    if(x < 0 or x > 800 or y < 0 or y > 800): # TODO: replace number with map height and width constant
      self.markedForTermination = True
    super().update()


class Obstacle(GameObject):
  def __init__(self, position):
    image = f'img/wall.png'
    size = (50, 50) # TODO read from game constant

    super().__init__(image, position, size)

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
    
    
    t1 = Tank(color = 'blue', position = (50, 50), number = 1)
    t2 = Tank(color = 'blue', position = (0, 50), number = 2)
    t3 = Tank(color = 'blue', position = (100, 50), number = 3)
    

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