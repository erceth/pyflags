import pygame as pg
from gameObject import GameObject
from pygame.math import Vector2
from bullet import Bullet

class Tank(GameObject):
  def __init__(self, color, position, number, screen):
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
      self.screen = screen

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
      pg.draw.circle(self.screen, (0,234,0), self.position, self.radius, 1) # TODO: put select color as a CONST
    self.screen.blit(self.text, (self.position[0], self.position[1] + self.radius)) # TODO: don't pass screen to constructor, do this another way
  
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