''' Should contain a set of functions that can be applied to
    a surface that "transition" to a battle.'''

import settings
from pygame import time
from pygame import Rect

from shared.colors import black

def _horizSlide(surface, dx=None, slideTime=2, distance=settings.mapwidth):
   if dx is None:
      dx = settings.mapwidth / (slideTime * settings.fps)

   clock = time.Clock()
   for x in range(0, distance, dx):
      surface.scroll(dx=dx)
      surface.fill(black, rect=Rect(x, 0, dx, settings.mapheight,))
      yield True

def slideRight(surface):
   return _horizSlide(surface)



