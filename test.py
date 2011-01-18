import settings
import json

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

screen = pygame.display.set_mode(settings.totalsize)

background = load_tile('green_grey.gif')

man = PlayerCharacter(center=(32 * 10 + 16, 32 * 10 + 16))

clock = pygame.time.Clock()

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

testOverworldFile = open("media/maps/testArena.json")
jsonData = json.load(testOverworldFile)

overworld = Overworld.fromJson(jsonData, man)

npc = DumbNPC(center=(32 * 8 + 16, 32 * 14 + 16), walkDelay=settings.fps/2)

overworld.addNPC(npc)

npc = DumbNPC(center=(32 * 13 + 16, 32 * 14 + 16), walkDelay=settings.fps/2)

overworld.addNPC(npc)

#overworld.fill_background()

if not pygame.font.get_init():
   print "Font rendering subsystem missing."

isBattleAnimation = False
isBattle = False
battleAnim = None
while 1:
   clock.tick(settings.fps)

   if battleAnim is not None:
      print "BattleAnim"
      try:
         battleAnim.next()
      except StopIteration:
         battleAnim = None
         isBattle = True

   elif isBattle:
      print "Oh Hai! Battle here!"
      isBattle = False
      overworld.fulldraw(screen)

      # battle finished

   else:
      processEvents()
      event = overworld.update()
      if event is not None:
         print "Boo"
         # currently can only be BattleEvent
         battleAnim = battleAnimation.slideRight(screen)
         print "battleAnim:", battleAnim
         continue

      overworld.draw(screen)

   pygame.display.flip()

