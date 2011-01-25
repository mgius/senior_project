import settings

from pygame import Rect
from pygame import sprite
from pygame.locals import *

from environment import Environment

from shared.direction import Direction
from shared.colors import black

from status.battlestatus import BattlefieldStatus

class Battlefield(Environment):
   def __init__(self, background, player, enemy):
      Environment.__init__(self, background)
      self.player = player
      self.enemy = enemy
      self.sprites = sprite.RenderUpdates((player,enemy))

      # stop the player and make him turn left
      self.player.stopWalking(self.player.curDirection)
      self.player._setwalkingdirection(Direction.LEFT)
      self.player.stopWalking(self.player.curDirection)

      # stop the npc and make him turn right
      self.enemy.stopWalking(self.enemy.curDirection)
      self.enemy._setwalkingdirection(Direction.RIGHT)
      self.enemy.stopWalking(self.enemy.curDirection)

      # put them on opposite ends of the field
      self.enemy.rect.center = (32 + 16, 320 + 16)
      self.player.rect = (608 - 16, 320 + 16)

      self.statusBar = BattlefieldStatus(self.player, self.enemy)

      self.frameCount = settings.fps / 2

   def update(self):
      if self.frameCount > 0:
         self.frameCount -= 1
         return
      # this should eventually become a part of the players
      for strategem in self.player.strategy:
         if strategem.condition.checkCondition(self.player, self.enemy):
            strategem.action.doAction(self.player, self.enemy)
            break
      for strategem in self.enemy.strategy:
         if strategem.condition.checkCondition(self.enemy, self.player):
            strategem.action.doAction(self.enemy, self.player)
            break
      self.frameCount = settings.fps / 2
   
   def draw(self, surface):
      # TODO: shouldn't be reblitting when nothing has changed...probably
      if self._shouldFillBackground:
         self.fill_background(surface)
         #self.walls.draw(surface)
      self.sprites.draw(surface)
      self.statusBar.draw(surface)
