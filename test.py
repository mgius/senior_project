import settings

import sys, pygame, time, os, math
from pygame.locals import *

from character.playercharacter import PlayerCharacter

from character.dumbnpc import DumbNPC

from environment.overworld import Overworld
from environment.wall import Wall

from battle import battleAnimation

import shared.colors
from shared.direction import Direction
from shared.load import load_sprite, load_tile

pygame.init()

screen = pygame.display.set_mode(settings.size)

background = load_tile('green_grey.gif')

man = PlayerCharacter(center=(32 * 10 + 16, 32 * 10 + 16))

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
         elif event.key == K_t:
            battleAnimation.slideRight(screen)
         elif event.key == K_n and event.key == K_LSHIFT or event.key == K_RSHIFT:
            npc.stopWalking()
         elif event.key == K_n:
            npc.startWalking()
      overworld.processEvent(event)

overworld = Overworld(background, character, screen, walls)

npc = DumbNPC(center=(32 * 13 + 16, 32 * 14 + 16), walkDelay=settings.fps/2)
overworld.addNPC(npc)
#overworld.fill_background()

while 1:
   processEvents()
   overworld.update()
   overworld.draw()
   pygame.display.flip()
   clock.tick(settings.fps)
