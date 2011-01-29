''' Handles Displaying and storing status info for the overworld '''
import settings

from pygame import font, Rect
from shared import colors

class OverWorldStatus(object):
   def __init__(self, player, location):
      self.player = player
      self.location = location

      self.font = font.SysFont(font.get_default_font(), 32)

      # player name won't change
      self.playernamesize = self.font.size(self.player.charactername)
      self.playername = self.font.render(self.player.charactername, False, colors.white)

      # might be more appropriate to calculate this somewhere else
      self._statusMiddle = settings.statusheight / 2 + settings.mapheight

   def draw(self, surface):
      surface.fill(colors.black, rect=Rect((0, settings.mapheight), (settings.statussize)))

      locationtext = self.font.render(self.location, False, colors.white)
      surface.blit(locationtext, (32, self._statusMiddle))

      hptext = "HP: " + str(self.player.curhp)
      mptext = "MP: " + str(self.player.curmp)

      hptextsize = self.font.size(hptext)
      mptextsize = self.font.size(mptext)

      hptext = self.font.render(hptext, False, colors.white)
      mptext = self.font.render(mptext, False, colors.white)

      width = max((hptextsize[0], mptextsize[0])) + 6

      surface.blit(self.playername, (settings.statuswidth - self.playernamesize[0] - 6, self._statusMiddle - self.playernamesize[1]))
      surface.blit(hptext, (settings.statuswidth - width, self._statusMiddle))
      surface.blit(mptext, (settings.statuswidth - width, self._statusMiddle + mptextsize[1]))
