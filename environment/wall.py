from pygame import Rect
from pygame import sprite

from shared.load import load_tile

class Wall(sprite.Sprite):
   def __init__(self, tile, topleft=None, rect=None):
      sprite.Sprite.__init__(self)
      self.image = load_tile(tile)
      self.rect = None
      if rect is not None:
         self.rect = rect
      elif topleft is not None:
         self.rect = Rect(topleft, self.image.get_rect().size)
      else:
         print "Wall needs a location. Provide one"
         raise SystemExit

   @staticmethod
   def fromJson(jsonMapList):
      ''' Reads in a JsonMap representing a set of walls 
          Could benefit from some caching of the tile

          Expects a list of elements containing two elements.  
          
          "tile"  is a string that corresponds to a tile gif filename
          "locations" is a list of two-element (x,y) sequences
      '''
      retlist = []
      for tileset in jsonMapList:
         for location in tileset["locations"]:
            retlist.append(Wall(tileset["tile"], location))

      return retlist
