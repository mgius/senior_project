''' Handles Displaying and storing status info for the battlefield '''
import settings

from pygame import font
from shared import colors

class BattlefieldStatus(object):
   def __init__(self, surface, player, enemygroup):
      self.player = player
      self.surface = surface
      self.enemygroup = enemygroup
      # placeholders
      self.playername = "Player"
      self.hp = "HP: " + str(12)
      self.mp = "MP: " + str(10)
      self.locationname = "The Pit of Despair"

      self.font = font.SysFont(font.get_default_font(), 32)

      # might be more appropriate to calculate this somewhere else
      self._statusMiddle = settings.statusheight / 2 + settings.mapheight

   def draw(self):
      locationtext = self.font.render(self.locationname, False, colors.white)
      self.surface.blit(locationtext, (32, self._statusMiddle))

      hptext = self.font.render(self.hp, False, colors.white)
      mptext = self.font.render(self.mp, False, colors.white)

      hptextsize = self.font.size(self.hp)
      mptextsize = self.font.size(self.mp)

      width = max((hptextsize[0], mptextsize[0])) + 6

      self.surface.blit(hptext, (settings.statuswidth - width, self._statusMiddle))
      self.surface.blit(mptext, (settings.statuswidth - width, self._statusMiddle + mptextsize[1]))


