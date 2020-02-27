# https://stackoverflow.com/questions/45889954/rotating-and-moving-a-sprite-in-pygame
import math
import pygame as pg
from pygame.math import Vector2

class GameObject(pg.sprite.Sprite):
    def __init__(self, image, position, size, direction = (0, 0), speed = 0, angle = 0):
        self.image = image
        self.position = Vector2(position)
        self.size = size
        self.direction = Vector2(direction)
        self.speed = speed
        self.angle = angle
        self.sprite = None
        self.image = pg.image.load(self.image)
        self.image = pg.transform.scale(self.image, self.size)
        self.original_image = self.image
        self.rect = self.image.get_rect(center=position)
        self.angle_speed = 0
        super(GameObject, self).__init__() # TODO: move to bottom of init?
        self.sprite = pg.sprite.RenderPlain((self))
        self.top = None
        self.bottom = None
        self.left = None
        self.right = None
        self.updateSides()

    def update(self):
        if self.angle_speed != 0:
            # Rotate the direction vector and then the image.
            self.direction.rotate_ip(self.angle_speed)
            self.angle += self.angle_speed
            self.image = pg.transform.rotate(self.original_image, -self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
        # Update the position vector and the rect.
        self.position += self.direction * self.speed
        self.updateSides()
        self.rect.center = self.position

    def getSprite(self):
      return self.sprite
    
    def updateSides(self):
      halfHeight = (self.size[1] / 2)
      halfWidth = (self.size[0] / 2)
      self.top = self.position[1] - halfHeight
      self.bottom = self.position[1] + halfHeight
      self.left = self.position[0] - halfWidth
      self.right = self.position[0] + halfWidth

class Tank(GameObject):
  def __init__(self, color, position):
      # general attributes
      image = f'img/{color}_tank.png'
      size = (50, 50) # TODO read from game constant
      direction = (1,0) # TODO randomize
      speed = 4 # TODO read from game constant
      angle = 0 # TODO randomize

      # specific to tank
      self.color = color
      self.max_rotation = 4 # TODO read from game constant
      self.destination = position

      super().__init__(image, position, size, direction, speed, angle)
  
  def update(self):
    destVector = Vector2(self.destination[0] - self.position[0], self.destination[1] - self.position[1])
    angle = self.direction.angle_to(destVector)
    if (angle > 180): # compensate for angle_to's inability to handle degrees > 360 or < -360
      angle = -360 + angle
    if (angle < -180):
      angle = 360 + angle
    self.angle_speed = self.getMaxRotation(angle)
    super().update()
  
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
    bullet = Bullet(self.color, self.position, self.direction, self.angle)
    return bullet

class Bullet(GameObject):
  def __init__(self, color, position, direction, angle):
    image = f'img/{color}_tank.png' # TODO make bullet pictures
    size = (6, 6) # TODO read from game constant
    speed = 10 # TODO read from game conts

    super().__init__(image, position, size, direction, speed, angle)

class Obstacle(GameObject):
  def __init__(self, position):
    image = f'img/wall.png'
    size = (50, 50) # TODO read from game constant

    super().__init__(image, position, size)


def main():
    pg.init()
    screen = pg.display.set_mode((800, 800))
    # One time paint
    o2 = Obstacle((400, 400))
    

    gameObjects = [o2]
    
    t1 = Tank(color = 'red', position = (50, 50))
    

    gameObjects.append(t1)

    clock = pg.time.Clock()
    done = False
    while not done:
        clock.tick(30)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN:
              pos = pg.mouse.get_pos()
              t1.setDestination(pos)
            elif event.type == pg.KEYDOWN:
              if event.key == pg.K_SPACE:
                  bullet = t1.fire()
                  gameObjects.append(bullet)
            #     elif event.key == pg.K_DOWN:
            #         player.speed -= 1
            #     elif event.key == pg.K_LEFT:
            #         player.angle_speed = -4
            #     elif event.key == pg.K_RIGHT:
            #         player.angle_speed = 4
            # elif event.type == pg.KEYUP:
            #     if event.key == pg.K_LEFT:
            #         player.angle_speed = 0
            #     elif event.key == pg.K_RIGHT:
            #         player.angle_speed = 0
        screen.fill((30, 30, 30))
          

        

        for obj1 in gameObjects:
          for obj2 in gameObjects:
            if obj1 is obj2: continue
            if not(obj1.right < obj2.left or obj1.left > obj2.right or obj1.top > obj2.bottom or obj1.bottom < obj2.top): # LEFT OFF
              print('hit')
          obj1.update()
          obj1.getSprite().draw(screen)

        pg.display.flip()

if __name__ == '__main__':
    main()
    pg.quit()

# create other classes