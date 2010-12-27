import sys, pygame, time, os
from itertools import cycle
from pygame.locals import *
pygame.init()

size = width, height = 320, 240
speed = [2, 2]
black = 0, 0, 0
fps = 30

screen = pygame.display.set_mode(size)

mediadir = 'media'
spritedir = os.path.join(mediadir, 'sprites')

def readWalkingAnimation(name):
   walk = []
   walk.append(
         pygame.image.load(os.path.join(spritedir, name + '1.gif')).convert())
   walk.append(
         pygame.image.load(os.path.join(spritedir, name + '2.gif')).convert())
   walk = cycle(walk)
   return walk

def readWalkingAnimations(name):
   ''' Reads in a series of gifs as a walking animation 
       returns a 4-tuple of left, front, right, back, each
       implemented as a cycle of each walking animation

       TODO: Reimplement cycle so that I can restart the animation?
   '''

   lfWalk = readWalkingAnimation(name + '_lf')
   frWalk = readWalkingAnimation(name + '_fr')
   rtWalk = readWalkingAnimation(name + '_rt')
   bkWalk = readWalkingAnimation(name + '_bk')
   
   return (lfWalk, frWalk, rtWalk, bkWalk)

class Direction():
   ''' Python lacks a java-style enum, leading to this...'''
   LEFT = 0
   FRONT = 1
   RIGHT = 2
   BACK = 3

class Character(pygame.sprite.Sprite):
   def __init__(self):
      pygame.sprite.Sprite.__init__(self)
      (self.lfWalk, self.frWalk,
       self.rtWalk, self.bkWalk) = readWalkingAnimations('ftr1')

      self.walkingSpeed = fps / 4 # frames between steps
      self.walkingCount = self.walkingSpeed # frames until next step
      self.curDirection = Direction.LEFT

      self.curAnim = self.lfWalk
      self.image = self.curAnim.next()
      self.rect = self.image.get_rect()

   def changeDirection(self, newdirection):
      if (newdirection == self.curDirection):
         return

      self.curDirection = newdirection
      if newdirection == Direction.LEFT:
         self.curAnim = self.lfWalk
      elif newdirection == Direction.FRONT:
         self.curAnim = self.frWalk
      elif newdirection == Direction.RIGHT:
         self.curAnim = self.rtWalk
      elif newdirection == Direction.BACK:
         self.curAnim = self.bkWalk

      self.iamge = self.curAnim.next()
      self.rect = self.image.get_rect()
      # Force a frame update
      self.walkingCount = self.walkingSpeed


   def walk(self):
      if self.walkingCount >= self.walkingSpeed:
         self.walkingCount = 0
         self.image = self.curAnim.next()
      else:
         self.walkingCount += 1

   def update(self):
      self.walk()

man = Character()

clock = pygame.time.Clock()
allsprites = pygame.sprite.RenderPlain((man))

def processEvents():
   for event in pygame.event.get():
      if event.type == QUIT:
         sys.exit(0)
      elif event.type == KEYDOWN and event.key == K_ESCAPE:
         sys.exit(0)
      elif event.type == KEYDOWN and event.key == K_UP:
         man.changeDirection(Direction.BACK)
      elif event.type == KEYDOWN and event.key == K_LEFT:
         man.changeDirection(Direction.LEFT)
      elif event.type == KEYDOWN and event.key == K_RIGHT:
         man.changeDirection(Direction.RIGHT)
      elif event.type == KEYDOWN and event.key == K_DOWN:
         man.changeDirection(Direction.FRONT)

while 1:
   allsprites.draw(screen)
   pygame.display.flip()
   clock.tick(fps)
   processEvents()
   allsprites.update()
