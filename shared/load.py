from os import path
import pygame

mediadir = 'media'
spritedir = path.join(mediadir, 'sprites')
tilesdir = path.join(mediadir, 'tiles')

def load_sprite(name, colorkey=None):
   try:
      image = pygame.image.load(path.join(spritedir, name))
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
         image.set_colorkey(colorkey, pygame.locals.RLEACCEL)
   return image

def load_tile(name):
   try:
      image = pygame.image.load(path.join(tilesdir, name))
   except pygame.error, message: 
      print "cannot load image: %s" % name
      raise SystemExit, message
   image = image.convert()
   return image

