import pygame as pg
import gameConsts

screen = gameConsts.screen

class Scoreboard():
  def __init__(self, players):
    self.font = pg.font.SysFont(gameConsts.TANK_FONT, gameConsts.TANK_FONT_SIZE)
    self.score = {}
    self.x = gameConsts.scoreboard['x']
    self.y = gameConsts.scoreboard['y']
    for p in players:
      self.score[p['color']] = 0

    self.width = gameConsts.TANK_FONT_SIZE * 5
    self.height = (2 + len(self.score)) * gameConsts.TANK_FONT_SIZE

  def updateScore(self, playerColor, points):
    self.score[playerColor] = points

  def update(self):
    pg.draw.rect(screen, (10,10,10,25), (self.x, self.y, self.width, self.height))
    i = 0
    for key, s in self.score.items():
      self.text = self.font.render(f'{key}: {s}', False, (255,255,255))
      screen.blit(self.text, (self.x + gameConsts.TANK_FONT_SIZE, self.y + gameConsts.TANK_FONT_SIZE + (gameConsts.TANK_FONT_SIZE * i)))
      i = i + 1
    