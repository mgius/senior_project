''' Handles Displaying and storing status info for the battlefield '''
import settings

from pygame import font
from shared import colors

class BattlefieldStatus(object):
   def __init__(self, player, enemygroup):
      self.player = player
      self.enemygroup = enemygroup

      # temporary hack
      self.enemy = enemygroup.sprites()[0]

      self.font = font.SysFont(font.get_default_font(), 32)

      # might be more appropriate to calculate this somewhere else
      self._statusMiddle = settings.statusheight / 2 + settings.mapheight


   # TODO: Need to split out re-rendering of attributes vs blitting them,
   #       just like everything else.  Probably not worth it to flag 
   #       attributes as changed, but playername is unlikely to change.
   def update(self):
      pass

   # this function is a goddamn mess.  I need to organize this data far better
   def draw(self,surface):
      playernametext = self.font.render(self.player.name, False, colors.white)
      playerhptext = self.font.render("HP: " + str(self.player.hp), False, colors.white)
      playermptext = self.font.render("MP: " + str(self.player.mp), False, colors.white)

      playernamesize = self.font.size()
      (playerhptextsize, mptextsize) = (self.font.size(self.player.hp), self.font.size(self.player.mp))

      playertextwidth = max((playernamesize[0], playerhptextsize[0], playermptextsize[0])) + 6

      surface.blit(playernametext, (settings.statuswidth - width, self._statusMiddle - playernamesize[1]))
      surface.blit(playerhptext, (settings.statuswidth - width, self._statusMiddle))
      surface.blit(playermptext, (settings.statuswidth - width, self._statusMiddle + playermptextsize[1]))
