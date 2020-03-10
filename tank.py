import pygame as pg
from gameObject import GameObject
from pygame.math import Vector2
from bullet import Bullet
import math
import gameConsts
import random

screen = gameConsts.screen

class Tank(GameObject):
  def __init__(self, color, position, number):
      # general attributes
      image = f'img/{color}_tank.png'
      size = gameConsts.TANK_SIZE
      direction = (1,0) # direction the image naturally faces
      speed = gameConsts.TANK_MAX_SPEED
      angle = 0

      # specific to tank
      self.color = color
      self.destination = position
      self.selected = False
      self.font = pg.font.SysFont(gameConsts.TANK_FONT, gameConsts.TANK_FONT_SIZE)
      self.text = self.font.render(str(number), False, gameConsts.SELECTED_COLOR)
      self.flag = None
      self.respawn = False
      self.timeOfDeath = 0

      super().__init__(image, position, size, direction, speed, angle)

      # start at random angle
      randomAngle = random.randint(0, 360)
      self.direction.rotate_ip(randomAngle)
      self.angle = round((self.angle + randomAngle) % 360, 2)
      self.image = pg.transform.rotate(self.original_image, -self.angle)
      self.rect = self.image.get_rect(center=self.rect.center)
  
  def update(self):
    xDiff = self.destination[0] - self.position[0]
    yDiff = self.destination[1] - self.position[1]
    if(abs(xDiff) > 1 and abs(yDiff) > 1): # if at destination, don't calc angleSpeed
      destVector = Vector2(xDiff, yDiff)
      destAngle = round(self.direction.angle_to(destVector), 2)
      if (destAngle > 180): # compensate for destAngle_to picking the wrong direction in these cases
        destAngle = -360 + destAngle
      if (destAngle < -180):
        destAngle = 360 + destAngle
      self.angleSpeed = round(self.getMaxRotation(destAngle), 2)

    distance = math.hypot(self.position[0] - self.destination[0], self.position[1] - self.destination[1])
    if distance < self.radius:
      self.speed = round(4 * distance / self.radius, 2)
    else:
      self.speed = gameConsts.TANK_MAX_SPEED
    super().update()
    if self.selected:
      pg.draw.circle(screen, gameConsts.SELECTED_COLOR, self.position, self.radius, 1)
    # self.text = self.font.render(f'{str(self.angle)}-{str(self.direction)}', False, gameConsts.SELECTED_COLOR) # DEBUG
    screen.blit(self.text, (self.position[0], self.position[1] + self.radius))
  
  def getMaxRotation(self, desiredAngle):
    if (desiredAngle > gameConsts.TANK_MAX_ROTATION):
      return gameConsts.TANK_MAX_ROTATION
    elif (desiredAngle < -gameConsts.TANK_MAX_ROTATION):
      return -gameConsts.TANK_MAX_ROTATION
    else:
      return desiredAngle

  def setDestination(self, pos):
    self.destination = pos
  
  def fire(self):
    bulletRadius = gameConsts.BULLET_SIZE / 2 / math.cos(45)
    frontOfTank = self.position + self.direction * (self.radius + bulletRadius + gameConsts.TANK_MAX_SPEED) # TANK_MAX_SPEED cases when tank postion is updated before bullet
    bullet = Bullet(self.color, frontOfTank, self.direction, self.angle)
    return bullet
  
  def select(self):
    self.selected = True

  def unselect(self):
    self.selected = False

  def setFlag(self, flag):
    self.flag = flag

  def setRespawn(self, timeOfDeath):
    self.respawn = True
    self.timeOfDeath = timeOfDeath
    self.position = Vector2((-gameConsts.TANK_SIZE[0], -gameConsts.TANK_SIZE[1])) # off screen
    self.setDestination(self.position)
