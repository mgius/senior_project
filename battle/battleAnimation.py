''' Should contain a set of functions that can be applied to
    a surface that "transition" to a battle.'''

import settings

import random

from pygame import time
from pygame import Rect

from shared.colors import black

def randomAnimation():
   return random.choice(animations)

def _horizSlide(surface, dx=None, slideTime=2, distance=settings.mapwidth):
   if dx is None:
      dx = settings.mapwidth / (slideTime * settings.fps)

   for x in range(0, distance, dx):
      surface.scroll(dx=dx)
      surface.fill(black, rect=Rect(x, 0, dx, settings.mapheight))
      yield True

def _horizSplit(surface, dx=None, slideTime=2, distance=settings.mapwidth):
   if dx is None:
      dx = settings.mapwidth / (slideTime * settings.fps)

   srect = surface.get_rect()

   left = surface.subsurface(Rect((srect.topleft),
                                  (srect.width / 2, srect.height)))
   right = surface.subsurface(Rect((srect.midtop),
                                   (srect.width / 2, srect.height)))

   for x in range(0, distance / 2, dx):
      left.scroll(dx=-dx)
      right.scroll(dx=dx)
      
      blackfill = Rect(srect.centerx - x, 0, x * 2, settings.mapheight)
      surface.fill(black, rect=blackfill)
      yield True

def horizBlinds(surface, dx=None, slideTime=2, distance=settings.mapwidth):
   if dx is None:
      dx = settings.mapwidth / (slideTime * settings.fps)

   srect = surface.get_rect()

   for x in range(0, distance / 2, dx):
      surface.scroll(dx=dx)
      
      blackfill = Rect(srect.centerx - x, 0, x * 2, settings.mapheight)
      surface.fill(black, rect=blackfill)
      yield True


def slideRight(surface):
   return _horizSlide(surface)

def splitMiddle(surface):
   return _horizSplit(surface)

animations = [horizBlinds, slideRight, splitMiddle]
