import settings

from pygame import Rect
from pygame import sprite
from pygame.locals import *

from environment import Environment

from shared.direction import Direction
from shared.colors import black

from status.battlestatus import BattlefieldStatus

class Battlefield(Environment):
   def __init__(self, background, player, enemygroup):
      Environment.__init__(self, background)
      self.player = player
      self.playergroup = sprite.RenderUpdates((player))
      self.enemygroup = sprite.RenderUpdates((enemygroup))

      # stop the player and make him turn left
      self.player.stopWalking(self.player.curDirection)
      self.player._setwalkingdirection(Direction.LEFT)
      self.player.stopWalking(self.player.curDirection)

      # stop the npc and make him turn right
      self.enemy = self.enemygroup.sprites()[0]
      self.enemy._setwalkingdirection(Direction.RIGHT)
      self.enemy.stopWalking(self.enemy.curDirection)

      # put them on opposite ends of the field
      self.enemy.rect.center = (32 + 16, 320 + 16)
      self.player.rect = (608 - 16, 320 + 16)

      ##TODO:  This is a hack
      #self.player.name = "Player"
      #self.player.hp = 12
      #self.player.mp = 10

      #for enemy in self.enemygroup:
      #   enemy.name = "Tom"
      #   enemy.hp = 1000
      #   enemy.mp = 4000

      #self.statusBar = BattlefieldStatus(self.player, self.enemygroup)

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
      self.playergroup.clear(surface, self.clear_callback)
      self.playergroup.draw(surface)
      self.enemygroup.clear(surface, self.clear_callback)
      self.enemygroup.draw(surface)
      #self.statusBar.draw(surface)
