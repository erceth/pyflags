from gameObject import GameObject

class Base(GameObject):
  def __init__(self, color, position, size):
    image = f'img/{color}_basetop.png'
    size = (size, size)

    super().__init__(image, position, size)