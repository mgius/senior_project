import settings

import sys, pygame, time, os, math
from pygame.locals import *

from character.character import Character
from environment.overworld import Overworld
from environment.wall import Wall

import shared.colors
from shared.direction import Direction
from shared.load import load_sprite, load_tile

pygame.init()

screen = pygame.display.set_mode(settings.size)

background = load_tile('green_grey.gif')

man = Character(center=(32 * 10 + 16, 32 * 10 + 16))

clock = pygame.time.Clock()
character = pygame.sprite.RenderUpdates((man))
walls = pygame.sprite.RenderPlain()

for x in range(128, 256, 32):
   walls.add(Wall(load_tile("brown_wall_center.gif"), topleft=(x, 64)))

#processEvents.downCount = 0

def processEvents():
   for event in pygame.event.get():
      if event.type == QUIT:
         sys.exit(0)
      elif event.type == KEYDOWN:
         if event.key == K_ESCAPE:
            sys.exit(0)
         elif event.key == K_q:
            sys.exit(0)
      overworld.processEvent(event)

overworld = Overworld(background, character, screen, walls)
overworld.fill_background()

while 1:
   processEvents()
   overworld.update()
   overworld.draw()
   pygame.display.flip()
   clock.tick(settings.fps)
