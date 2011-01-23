import settings

from os import path
from glob import iglob

import json
import pygame

def load_json_data(filename):
   jsonFile = open(filename + '.json')
   jsonData = json.load(jsonFile)
   jsonFile.close()
   return jsonData

def load_weapon_data(name):
   return load_json_data(path.join(settings.weaponsdir, name))

def load_armor_data(name):
   return load_json_data(path.join(settings.armordir, name))

def load_sprites_glob(fileglob, colorkey=None):
   for filename in iglob(path.join(settings.spritedir, fileglob)):
      yield load_sprite(path.basename(filename), -1)

def load_sprite(name, colorkey=None):
   try:
      image = pygame.image.load(path.join(settings.spritedir, name))
   except pygame.error, message: 
      print "cannot load image: %s" % name
      raise SystemExit, message
   image = image.convert()
   if colorkey is not None:
      if colorkey is -1:
         colorkey = (255,255,255)
         # RLEACCEL apparently makes things faster at the expense of modification
         # speed. Colorkey sets a color that represents the "background" of 
         # the sprite.  According to online documentation, this is actually
         # faster than a truly transparent image. 
         image.set_colorkey(colorkey, pygame.RLEACCEL)
   return image

def load_tile(name):
   try:
      image = pygame.image.load(path.join(settings.tilesdir, name))
   except pygame.error, message: 
      print "cannot load image: %s" % name
      raise SystemExit, message
   image = image.convert()
   return image

