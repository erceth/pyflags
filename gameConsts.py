import pygame as pg
import sys
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("map", type=str,
                    help="Map to load, json file in map directory without extention Ex: blocks")
parser.add_argument("-ff", "--friendlyFire", action="store_true",
                    help="Turn on friendly fire")
args = parser.parse_args()


with open (f'maps/{args.map}.json') as f:
  data = json.load(f)


MAP_WIDTH = data['width']
MAP_HEIGHT = data['height']
screen = pg.display.set_mode((MAP_WIDTH, MAP_HEIGHT))
MAP_BACKGROUND = data['background']
obstacles = data['obstacles']
players = data['players']
scoreboard = data['scoreboard']

TANK_SIZE = (50, 50)
TANK_MAX_SPEED = 8
TANK_MAX_ROTATION = 7
TANK_FONT = 'Times New Roman'
TANK_FONT_SIZE = 32
SELECTED_COLOR = (0,234,0)
FPS = 30
SELECT_ADD_TIME = 500 # milliseconds
BACKGROUND_COLOR = (59, 113, 55)
BACKGROUND_SIZE = 120 # must be square
FLAG_SIZE = 25
FRIENDLY_FIRE = args.friendlyFire
BULLET_SIZE = 6
BULLET_SPEED = 10