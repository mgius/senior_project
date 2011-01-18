import settings

from pygame import Rect
from pygame import sprite
from pygame.locals import *

from shared.direction import Direction
from shared.colors import black

from status.overworldstatus import OverWorldStatus

class Battlefield(object):
   def __init__(self, background, playergroup, surface, enemygroup):
      self.background = background
      self.playergroup = playergroup
      # implicit assumption that playergroup is nonempty and the player
      # is the only member
      self.player = playergroup.sprites()[0]
      self.surface = surface
      self.enemygroup = enemygroup

      self.statusBar = BattlefieldStatus(self.surface, self.player, self.enemygroup)

      self.fill_background()

   # may want to optimize this
   def fill_background(self):
      for x in range(0, settings.mapwidth, 32):
         for y in range(0, settings.mapheight, 32):
            self.surface.blit(self.background, Rect(x, y, 32, 32))
      self.walls.draw(self.surface)
   
   def clear_callback(self, surface, rect):
      (left, top) = rect.topleft
      # lock blitting area to a 32x32 block
      newrect = Rect(((left // 32) * 32, (top // 32) * 32), rect.size)
      # stretch to also blit the square next to it if necessary
      if (left % 32 != 0):
         newrect.width += 32
      if (top % 32 != 0):
         newrect.height += 32
      for x in range(newrect.left, newrect.right, 32):
         for y in range(newrect.top, newrect.bottom, 32):
            surface.blit(self.background, Rect(x, y, 32, 32))

   def _battleTransition(self):
      self.surface.scroll(dx=settings.mapwidth/60)
      self.surface.fill(black, rect=Rect(self.__battleAnimShifted, 0, settings.width/60, settings.height))
      self.__battleAnimShifted += settings.mapwidth/60
      #self._battleTransition.scrolled += 5
      if self.__battleAnimShifted >= settings.mapwidth:
         self.enterBattle = False
         print "Stopped animating after %d pixels" % self.__battleAnimShifted

   def startBattleTransition(self):
      if not self.enterBattle:
         self.enterBattle = True
         self.__battleAnimShifted = 0
      #   self._battleTransition.scrolled = 0

   def endBattle(self):
      self.fill_background()
      self.draw()

   def update(self):
      if self.enterBattle:
         self._battleTransition()
      else:
         self.player.update()
         self.npcgroup.update()
         if sprite.spritecollideany(self.player, self.walls):
            self.player._goback()
         for npc in sprite.groupcollide(self.npcgroup, self.walls, False, False):
            npc._goback()
         if sprite.spritecollideany(self.player, self.npcgroup):
            self.startBattleTransition()
   
   def draw(self):
      # TODO: shouldn't be reblitting when nothing has changed...probably
      if not self.enterBattle:
         self.playergroup.clear(self.surface, self.clear_callback)
         self.playergroup.draw(self.surface)
         self.npcgroup.clear(self.surface, self.clear_callback)
         self.npcgroup.draw(self.surface)
      self.statusBar.draw()
