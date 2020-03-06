import pygame as pg
from pygame.math import Vector2

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