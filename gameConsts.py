import pygame as pg
import sys
import json
map = sys.argv[1] # map

with open (f'maps/{map}.json') as f:
  data = json.load(f)

MAP_WIDTH = data['width']
MAP_HEIGHT = data['height']
screen = pg.display.set_mode((MAP_WIDTH, MAP_HEIGHT))
MAP_BACKGROUND = data['background']
obstacles = data['obstacles']
players = data['players']

TANK_SIZE = (50, 50)
TANK_MAX_SPEED = 4
TANK_MAX_ROTATION = 7
TANK_FONT = 'Times New Roman'
TANK_FONT_SIZE = 32
SELECTED_COLOR = (0,234,0)
FPS = 30
SELECT_ADD_TIME = 500 # milliseconds
BACKGROUND_COLOR = (59, 113, 55)
BACKGROUND_SIZE = 120 # must be square