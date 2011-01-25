''' Handles Displaying and storing status info for the battlefield '''
import settings

from pygame import font, Rect
from shared import colors

class BattlefieldStatus(object):
   def __init__(self, player, enemy):
      self.player = player
      self.enemy = enemy

      self.font = font.SysFont(font.get_default_font(), 32)

      # player names won't change
      self.playernamesize = self.font.size(self.player.charactername)
      self.playername = self.font.render(self.player.charactername, False, colors.white)

      # player names won't change
      self.enemynamesize = self.font.size(self.enemy.charactername)
      self.enemyname = self.font.render(self.enemy.charactername, False, colors.white)

      # might be more appropriate to calculate this somewhere else
      self._statusMiddle = settings.statusheight / 2 + settings.mapheight

   # this function is a goddamn mess.  I need to organize this data far better
   def draw(self, surface):
      # eh

      surface.fill(colors.black, rect=Rect((0, settings.mapheight), (settings.statussize)))

      # draw player's hp
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

      # draw enemy's hp
      hptext = "HP: " + str(self.enemy.curhp)
      mptext = "MP: " + str(self.enemy.curmp)

      hptextsize = self.font.size(hptext)
      mptextsize = self.font.size(mptext)

      hptext = self.font.render(hptext, False, colors.white)
      mptext = self.font.render(mptext, False, colors.white)

      surface.blit(self.enemyname, (6, self._statusMiddle - self.enemynamesize[1]))
      surface.blit(hptext, (6, self._statusMiddle))
      surface.blit(mptext, (6, self._statusMiddle + mptextsize[1]))
