import settings

from pygame import Rect
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
   
   # improve this to only blit the area that the sprite just occupied
   def clear_callback(self, surface, rect):
      rect.inflate_ip(64, 64)
      (left, top) = rect.topleft
      rect.topleft = ((left // 32) * 32, (top // 32) * 32)
      for x in range(rect.left, rect.right, 32):
         for y in range(rect.top, rect.bottom, 32):
            surface.blit(self.background, Rect(x, y, 32, 32))

   def update(self):
      self.player.update()
   
   def draw(self):
      self.playergroup.clear(self.surface, self.clear_callback)
      self.playergroup.draw(self.surface)
