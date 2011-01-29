import settings

from pygame import Rect
from pygame import sprite
from pygame.locals import *

from collections import namedtuple
from environment import Environment

from operator import itemgetter

from shared.direction import Direction
from shared.colors import black

from status.battlestatus import BattlefieldStatus

class Battlefield(Environment):
   def __init__(self, background, player, enemy):
      Environment.__init__(self, background)
      self.players = sprite.Group(player)
      self.enemies = sprite.Group(enemy)
      self.sprites = sprite.RenderUpdates(self.players, self.enemies)
      self.combatants = sprite.Group(self.players, self.enemies)

      # stop the player and make him turn left
      for player in self.players:
          player.stopWalking(player.curDirection)
          player._setwalkingdirection(Direction.LEFT)
          player.stopWalking(player.curDirection)
          # TODO: Line them up
          player.rect.center = (608 - 16, 320 + 16)

      # stop the npc and make him turn right
      for player in self.enemies:
          enemy.stopWalking(enemy.curDirection)
          enemy._setwalkingdirection(Direction.RIGHT)
          enemy.stopWalking(enemy.curDirection)
          # TODO: Line them up
          enemy.rect.center = (32 + 16, 320 + 16)

      self.statusBar = BattlefieldStatus(self.players.sprites()[0], self.enemies.sprites()[0])

      self.frameCount = settings.fps / 2

      self.battleQueue = [ (c.speed, c) for c in self.combatants ]
      self.battleQueue.sort(key=itemgetter(0))

   def update(self):
      if self.frameCount > 0:
         self.frameCount -= 1
         return

      (curTime, character) = self.battleQueue.pop(0)
      # temporary hack
      if character in self.players:
         targets = self.enemies.sprites()
      else:
         targets = self.players.sprites()
      # this should eventually become a part of the players
      for strategem in character.strategy:
         target = strategem.condition.checkCondition(character, targets)
         if target:
            strategem.action.doAction(character, target)
            break

      if target.curhp <= 0:
         # target died
         target.kill()
         if not self.enemies:
            # player wins, return True
            return True
         if not self.players:
            return False

      self.battleQueue.append((curTime + character.speed, character))
      self.battleQueue.sort(key=itemgetter(0))
      self.frameCount = settings.fps / 2
   
   def draw(self, surface):
      # TODO: shouldn't be reblitting when nothing has changed...probably
      if self._shouldFillBackground:
         self.fill_background(surface)
         #self.walls.draw(surface)
      self.sprites.draw(surface)
      self.statusBar.draw(surface)
