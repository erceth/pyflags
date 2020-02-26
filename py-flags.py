# https://stackoverflow.com/questions/45889954/rotating-and-moving-a-sprite-in-pygame
import math
import pygame as pg
from pygame.math import Vector2

class GameObject(pg.sprite.Sprite):

    def __init__(self, image, position, size, direction, speed, angle, max_rotation, destination):
        self.image = image
        self.position = Vector2(position)
        self.size = size
        self.direction = Vector2(direction)
        self.speed = speed
        self.angle = angle
        self.max_rotation = max_rotation

        self.destination = (800, 800) # TODO: assign destination to start as the same thing as self.pos
        self.image = pg.image.load(self.image)
        self.image = pg.transform.scale(self.image, self.size)
        self.original_image = self.image
        self.rect = self.image.get_rect(center=position)
        self.angle_speed = 0
        super(GameObject, self).__init__()

    def update(self):
        destVector = Vector2(self.destination[0] - self.position[0], self.destination[1] - self.position[1]) # TODO: might need to remove destination for objects like bullets
        angle = self.direction.angle_to(destVector)
        if (angle > 180): # compensate for angle_to's inability to handle degrees > 360 or < -360
          angle = -360 + angle
        if (angle < -180):
          angle = 360 + angle
        self.angle_speed = self.getMaxRotation(angle)
        if self.angle_speed != 0:
            # Rotate the direction vector and then the image.
            self.direction.rotate_ip(self.angle_speed)
            self.angle += self.angle_speed
            self.image = pg.transform.rotate(self.original_image, -self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
        # Update the position vector and the rect.
        self.position += self.direction * self.speed
        self.rect.center = self.position

    def getMaxRotation(self, desiredAngle):
        if (desiredAngle > self.max_rotation): # TODO create constant max turn variable
          return self.max_rotation
        elif (desiredAngle < -self.max_rotation):
          return -self.max_rotation
        else:
          return desiredAngle


class Tank(GameObject):
  def __init__(self, color, position):
      image = f'img/{color}_tank.png'
      size = (50, 50) # TODO read from game constant
      direction = (1,0) # TODO randomize
      speed = 4 # TODO read from game constant
      angle = 0 # TODO randomize
      max_rotation = 4 # TODO read from game constant
      destination = (800, 800) # TODO delete
      super().__init__(image, position, size, direction, speed, angle, max_rotation, destination)

  def setDestination(self, pos):
    self.destination = pos


def main():
    pg.init()
    screen = pg.display.set_mode((800, 800))
    player = Tank(color = 'red', position = (50, 50))
    playersprite = pg.sprite.RenderPlain((player))

    clock = pg.time.Clock()
    done = False
    while not done:
        clock.tick(30)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN:
              pos = pg.mouse.get_pos()
              player.setDestination(pos)
            # elif event.type == pg.KEYDOWN:
            #     if event.key == pg.K_UP:
            #         player.speed += 1
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

        playersprite.update()

        screen.fill((30, 30, 30))
        playersprite.draw(screen)
        pg.display.flip()

if __name__ == '__main__':
    main()
    pg.quit()

# accept click from mouse to move tank
# make tank shoot
# remove destination from GameObject
# put classes in different files and import them
# create other classes