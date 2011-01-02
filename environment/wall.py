from pygame import Rect
from pygame import sprite

from shared.load import load_tile

class Wall(sprite.Sprite):
   def __init__(self, tile, topleft=None, rect=None):
      sprite.Sprite.__init__(self)
      self.image = tile
      self.rect = None
      if rect is not None:
         self.rect = rect
      elif topleft is not None:
         self.rect = Rect(topleft, self.image.get_rect().size)
      else:
         print "Wall needs a location. Provide one"
         raise SystemExit
