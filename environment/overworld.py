import settings

from pygame import Rect
from pygame import sprite
from pygame.locals import *

from shared.direction import Direction

class Overworld(object):
   def __init__(self, background, playergroup, surface, walls=()):
      self.background = background
      self.playergroup = playergroup
      # implicit assumption that playergroup is nonempty and the player
      # is the only member
      self.player = playergroup.sprites()[0]
      self.surface = surface
      self.walls = walls

   def processEvent(self, event):
      if event.type == KEYDOWN:
         if event.key == K_UP:
            self.player.startWalking(Direction.BACK)
         elif event.key == K_LEFT:
            self.player.startWalking(Direction.LEFT)
         elif event.key == K_RIGHT:
            self.player.startWalking(Direction.RIGHT)
         elif event.key == K_DOWN:
            self.player.startWalking(Direction.FRONT)
         # the following events are temporary for testing
         elif event.key == K_d:
            self.player._die()
         elif event.key == K_u:
            self.player._revive()
         elif event.key == K_a:
            self.player.startAttack()

      elif event.type == KEYUP:
         if event.key == K_UP:
            self.player.stopWalking(Direction.BACK)
         elif event.key == K_LEFT:
            self.player.stopWalking(Direction.LEFT)
         elif event.key == K_RIGHT:
            self.player.stopWalking(Direction.RIGHT)
         elif event.key == K_DOWN:
            self.player.stopWalking(Direction.FRONT)

   # may want to optimize this
   def fill_background(self):
      for x in range(0, settings.width, 32):
         for y in range(0, settings.height, 32):
            self.surface.blit(self.background, Rect(x, y, 32, 32))
      self.walls.draw(self.surface)
   
   # improve this to only blit the area that the sprite just occupied
   def clear_callback(self, surface, rect):
      (left, top) = rect.topleft
      newrect = Rect(((left // 32) * 32, (top // 32) * 32), rect.size)
      if (left % 32 != 0):
         newrect.width += 32
      if (top % 32 != 0):
         newrect.height += 32
      #print "DEBUG - x: %d, y: %d" % newrect.center
      #print "DEBUG - w: %d, h: %d\n" % newrect.size
      for x in range(newrect.left, newrect.right, 32):
         for y in range(newrect.top, newrect.bottom, 32):
            surface.blit(self.background, Rect(x, y, 32, 32))

   def update(self):
      self.player.update()
      if sprite.spritecollideany(self.player, self.walls):
         self.player._goback()
   
   def draw(self):
      # TODO: shouldn't be reblitting when nothing has changed...probably
      self.playergroup.clear(self.surface, self.clear_callback)
      self.playergroup.draw(self.surface)
