import settings
import json

import sys, pygame, time, os, math
from pygame.locals import *

from character.playerbattlecharacter import PlayerBattleCharacter

from character.dumbbattlenpc import DumbBattleNPC

from environment.overworld import Overworld
from environment.battlescreen import Battlefield
from environment.wall import Wall

from battle import battleAnimation

import shared.colors
from shared.direction import Direction
from shared.load import load_sprite, load_tile

pygame.init()

screen = pygame.display.set_mode(settings.totalsize)

background = load_tile('green_grey.gif')

man = PlayerBattleCharacter.load("humantorch", center=(32 * 10 + 16, 32 * 10 + 16))

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

npc = DumbBattleNPC.load("mrfreeze", center=(32 * 8 + 16, 32 * 14 + 16), walkDelay=settings.fps/2)

overworld.addNPC(npc)

npc = DumbBattleNPC.load("mrfreeze", center=(32 * 13 + 16, 32 * 14 + 16), walkDelay=settings.fps/2)

overworld.addNPC(npc)

#overworld.fill_background()

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
         battleScreen = Battlefield("red_silver.gif", rpgevent.player, rpgevent.opponents)

   elif isBattle:
      battleScreen.update()
      battleScreen.draw(screen)

   else:
      processEvents()
      rpgevent = overworld.update()
      if rpgevent is not None:
         # currently can only be BattleEvent
         battleAnim = battleAnimation.slideRight(screen)
         continue

      overworld.draw(screen)

   pygame.display.flip()

