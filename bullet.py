from gameObject import GameObject

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