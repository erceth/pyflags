from gameObject import GameObject
from tank import Tank

class Flag(GameObject):
  def __init__(self, color, position, size):
    image = f'img/{color}_flag.png'
    size = (size, size)

    self.color = color
    self.pickedUpBy = None
    self.pickedUp = False

    super().__init__(image, position, size)

  def setPickedUp(self, tank):
    if (isinstance(tank, Tank) and not self.pickedUpBy):
      self.pickedUpBy = tank
      self.pickedUp = True

  def dropped(self):
    self.pickedUpBy = None
    self.pickedUp = False

  def update(self):
    if self.pickedUp:
      self.position = self.pickedUpBy.position
    super().update()
    