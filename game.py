import settings
import json

import sys, pygame, time, os, math
from pygame.locals import *

from character.playercharactertypes import load_player
from character.nonplayercharactertypes import load_monster

from environment.overworld import Overworld
from environment.battlescreen import Battlefield
from environment.wall import Wall

from battle import battleAnimation

import shared.colors
from shared.direction import Direction
from shared.load import load_sprite, load_tile

pygame.init()

screen = pygame.display.set_mode(settings.totalsize)

man = load_player("humantorch", center=(32 * 10 + 16, 32 * 10 + 16))

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
      overworld.processEvent(event)

testOverworldFile = open("media/maps/printArena.json")
jsonData = json.load(testOverworldFile)

overworld = Overworld.fromJson(jsonData, man)

if not pygame.font.get_init():
   print "Font rendering subsystem missing."

isBattleAnimation = False
isBattle = False
battleAnim = None
rgpevent = None
while 1:
   clock.tick(settings.fps)

   if battleAnim is not None:
      try:
         battleAnim.next()
      except StopIteration:
         battleAnim = None
         isBattle = True
         battleScreen = Battlefield("white.gif", rpgevent.player, rpgevent.opponents)

   elif isBattle:
      status = battleScreen.update()
      if status is not None:
         if status:
            print "Players Win!"
            isBattle = False
            overworld.returnFromBattle()
            overworld.fulldraw(screen)
         else:
            print "Players Lose!"
            sys.exit(0)

      battleScreen.draw(screen)

   else:
      processEvents()
      rpgevent = overworld.update()
      if rpgevent is not None:
         # currently can only be BattleEvent
         battleAnim = battleAnimation.randomAnimation()(screen)
         continue

      overworld.draw(screen)

   pygame.display.flip()

