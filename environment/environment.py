import settings

from pygame import Rect
from pygame.locals import *

class Environment(object):
   def __init__(self, background, surface):
      self.background = background
      self.surface = surface

      self.fill_background()

   def processEvent(self, event):
      raise NotImplementedError, "Must be implemented by subclass"

   # may want to optimize this
   def fill_background(self):
      for x in range(0, settings.mapwidth, 32):
         for y in range(0, settings.mapheight, 32):
            self.surface.blit(self.background, Rect(x, y, 32, 32))
   
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

   def update(self):
      raise NotImplementedError, "This must be implemented by subclass"
   
   def draw(self):
      raise NotImplementedError, "This must be implemented by subclass"
