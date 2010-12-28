import sys, pygame, time, os
import math
from itertools import cycle
from pygame.locals import *
pygame.init()

size = width, height = 640, 480
black = 0, 0, 0
white = 255, 255, 255
fps = 30

screen = pygame.display.set_mode(size)

mediadir = 'media'
spritedir = os.path.join(mediadir, 'sprites')
tilesdir = os.path.join(mediadir, 'tiles')

background = pygame.image.load(os.path.join(tilesdir, 'green_grey.gif')).convert()

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
   def __init__(self, center = None):
      pygame.sprite.Sprite.__init__(self)
      (self.lfWalk, self.frWalk,
       self.rtWalk, self.bkWalk) = readWalkingAnimations('ftr1')
      self.battleStance = pygame.image.load(os.path.join(spritedir,
         'ftr1_battle.gif')).convert()
      self.deadStance = pygame.image.load(os.path.join(spritedir,
         'ftr1_dead.gif')).convert()

      self.speed = [-4,0]
      self.walkingRate = fps / 4 # frames between steps
      self.walkingCount = self.walkingRate # frames until next step
      self.curDirection = Direction.LEFT
      self.isWalking = False
      self.isDead = False
      self.isAttacking = False

      self.curAnim = self.lfWalk
      self.image = self.curAnim.next()
      self.rect = self.image.get_rect()
      self.rect.center = (self.rect.w/2, self.rect.h/2) if center is None else center

   def startWalking(self, newdirection):
      if self.isDead:
         return
      self.isWalking = True
      if self.curDirection == newdirection:
         return
      self.curDirection = newdirection
      if newdirection == Direction.LEFT:
         self.curAnim = self.lfWalk
         self.speed = [-4, 0]
      elif newdirection == Direction.FRONT:
         self.curAnim = self.frWalk
         self.speed = [0, 4]
      elif newdirection == Direction.RIGHT:
         self.curAnim = self.rtWalk
         self.speed = [4, 0]
      elif newdirection == Direction.BACK:
         self.curAnim = self.bkWalk
         self.speed = [0, -4]

      self.image = self.curAnim.next()
      # Force a frame update
      self.walkingCount = self.walkingRate

   def stopWalking(self):
      self.isWalking = False;
      # should probably reset to a standing pose...hmm....

   def walk(self):
      self.rect.move_ip(self.speed)
      if self.walkingCount >= self.walkingRate:
         self.walkingCount = 0
         self.image = self.curAnim.next()
      else:
         self.walkingCount += 1

   def update(self):
      if self.isDead:
         return
      if self.isAttacking:
         self.attack()
      if self.isWalking:
         self.walk()

   def die(self):
      self.isDead = True
      self.image = self.deadStance
      self.curDirection = None

   def revive(self):
      self.isDead = False
      self.image = self.battleStance
      self.curDirection = None

   def startAttack(self):
      if not self.isAttacking:
         self.attackFramesLeft = fps / 3
         self.isAttacking = True
         self.image = self.battleStance

   def attack(self):
      if self.attackFramesLeft > (fps / 6):
         self.rect.move_ip((-1, 0))
      elif self.attackFramesLeft > 0:
         self.rect.move_ip((1, 0))
      elif self.attackFramesLeft <= 0:
         self.isAttacking = False
         print "Final location: %d, %d\n" % (self.rect.center)
      self.attackFramesLeft -= 1




def processEvents():
   for event in pygame.event.get():
      #print event
      if event.type == QUIT:
         sys.exit(0)
      elif event.type == KEYDOWN and event.key == K_ESCAPE:
         sys.exit(0)
      elif event.type == KEYDOWN and event.key == K_q:
         sys.exit(0)
      elif event.type == KEYDOWN and event.key == K_UP:
         man.startWalking(Direction.BACK)
         processEvents.downCount += 1
      elif event.type == KEYDOWN and event.key == K_LEFT:
         man.startWalking(Direction.LEFT)
         processEvents.downCount += 1
      elif event.type == KEYDOWN and event.key == K_RIGHT:
         man.startWalking(Direction.RIGHT)
         processEvents.downCount += 1
      elif event.type == KEYDOWN and event.key == K_DOWN:
         man.startWalking(Direction.FRONT)
         processEvents.downCount += 1
      elif event.type == KEYDOWN and event.key == K_d:
         man.die()
      elif event.type == KEYDOWN and event.key == K_u:
         man.revive()
      elif event.type == KEYDOWN and event.key == K_a:
         man.startAttack()

      elif event.type == KEYUP and (event.key == K_UP or 
            event.key == K_LEFT or
            event.key == K_RIGHT or
            event.key == K_DOWN):
         processEvents.downCount -= 1
         # Avoids issue where fast typist can strike down before releasing previous
         # key
         if processEvents.downCount <= 0:
            man.stopWalking()

man = Character(center=screen.get_rect().center)

clock = pygame.time.Clock()
character = pygame.sprite.RenderUpdates((man))
walls = pygame.sprite.RenderPlain()


processEvents.downCount = 0

# may want to optimize this
def fill_background(surf, background):
   for x in range(0, width, 32):
      for y in range(0, height, 32):
         surf.blit(background, Rect(x, y, 32, 32))

# improve this to only blit the area that the sprite just occupied
def clear_callback(surf, rect):
   rect.inflate_ip(64, 64)
   (left, top) = rect.topleft
   rect.topleft = ((left // 32) * 32, (top // 32) * 32)
   for x in range(rect.left, rect.right, 32):
      for y in range(rect.top, rect.bottom, 32):
         surf.blit(background, Rect(x, y, 32, 32))

fill_background(screen, background)
while 1:
   character.clear(screen, clear_callback)
   character.draw(screen)
   pygame.display.flip()
   clock.tick(fps)
   processEvents()
   character.update()
