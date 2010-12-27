import sys, pygame, time
import itertools
pygame.init()

size = width, height = 320, 240
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

mediadir = 'media'

class Character(pygame.sprite.Sprite):
   def __init__(self):
      pygame.sprite.Sprite.__init__(self)
      self.leftWalk = []
      self.leftWalk.append( pygame.image.load(mediadir +
         '/sprites/ftr3_lf1.gif').convert())
      self.leftWalk.append( pygame.image.load(mediadir +
         '/sprites/ftr3_lf2.gif').convert())
      self.leftWalk = itertools.cycle(self.leftWalk)
      self.image = self.leftWalk.next()
      self.rect = self.image.get_rect()

   def walk(self):


   def update(self):
      self.image = self.leftWalk.next()

man = Character()

allsprites = pygame.sprite.RenderPlain((man))
allsprites.draw(screen)

pygame.display.flip()
allsprites.update()
time.sleep(1)
allsprites.draw(screen)
pygame.display.flip()

time.sleep(3)

