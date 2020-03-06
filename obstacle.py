from gameObject import GameObject

class Obstacle(GameObject):
  def __init__(self, position):
    image = f'img/wall.png'
    size = (50, 50) # TODO read from game constant

    super().__init__(image, position, size)