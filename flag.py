from gameObject import GameObject

class Flag(GameObject):
  def __init__(self, color, position, size):
    image = f'img/{color}_flag.png'
    size = (size, size)

    super().__init__(image, position, size)