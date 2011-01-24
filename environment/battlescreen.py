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

   def update(self):
      # this is awful, I hate myself
      #self.player.update()
      #self.enemygroup.update()
      #if sprite.spritecollideany(self.player, self.walls):
      #   self.player._goback()
      #for npc in sprite.groupcollide(self.enemygroup, self.walls, False, False):
      #   npc._goback()
      #if sprite.spritecollideany(self.player, self.enemygroup):
      #   self.startBattleTransition()
      pass
   
   def draw(self, surface):
      # TODO: shouldn't be reblitting when nothing has changed...probably
      if self._shouldFillBackground:
         self.fill_background(surface)
         #self.walls.draw(surface)
      self.sprites.draw()
      #self.statusBar.draw(surface)
