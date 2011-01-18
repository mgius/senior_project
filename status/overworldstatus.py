''' Handles Displaying and storing status info for the overworld '''
import settings

from pygame import font
from shared import colors

class OverWorldStatus(object):
   def __init__(self, player, location):
      self.player = player
      # placeholders
      self.playername = "Player"
      self.hp = "HP: " + str(12)
      self.mp = "MP: " + str(10)
      self.location = location

      self.font = font.SysFont(font.get_default_font(), 32)

      # might be more appropriate to calculate this somewhere else
      self._statusMiddle = settings.statusheight / 2 + settings.mapheight

   def draw(self, surface):
      locationtext = self.font.render(self.location, False, colors.white)
      surface.blit(locationtext, (32, self._statusMiddle))

      hptext = self.font.render(self.hp, False, colors.white)
      mptext = self.font.render(self.mp, False, colors.white)

      hptextsize = self.font.size(self.hp)
      mptextsize = self.font.size(self.mp)

      width = max((hptextsize[0], mptextsize[0])) + 6

      surface.blit(hptext, (settings.statuswidth - width, self._statusMiddle))
      surface.blit(mptext, (settings.statuswidth - width, self._statusMiddle + mptextsize[1]))


