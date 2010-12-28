''' Character class and some supporting functions for them. '''
import settings
import pygame

from itertools import cycle

from shared.direction import Direction
from shared.load import load_sprite

def readWalkingAnimation(name):
   ''' Reads in a two-piece walking animation from the sprite dir,
       and places the animation in a cyclical data structure so that
       it can be iterated over infinitely
       TODO: Modify to support animations of any length
       TODO: Support restarting the animation?  may have to reimplement cycle
   '''
   walk = []
   walk.append(load_sprite(name + '1.gif', -1))
   walk.append(load_sprite(name + '2.gif', -1))
   walk = cycle(walk)

   return walk

def readWalkingAnimations(name):
   ''' Reads in a series of gifs as a walking animation 
       returns a 4-tuple of left, front, right, back, each
       implemented as a cycle of each walking animation
   '''

   lfWalk = readWalkingAnimation(name + '_lf')
   frWalk = readWalkingAnimation(name + '_fr')
   rtWalk = readWalkingAnimation(name + '_rt')
   bkWalk = readWalkingAnimation(name + '_bk')
   
   return (lfWalk, frWalk, rtWalk, bkWalk)

class Character(pygame.sprite.Sprite):
   def __init__(self, center = None, spritename='ftr1'):
      pygame.sprite.Sprite.__init__(self)
      # animations and other sprite images
      (self.lfWalk, self.frWalk,
       self.rtWalk, self.bkWalk) = readWalkingAnimations(spritename)
      self.battleStance = load_sprite(spritename + '_battle.gif', -1)
      self.deadStance = load_sprite(spritename + '_dead.gif', -1)

      self.speed = [0,0]
      self.walkingRate = settings.fps / 4 # frames between steps
      self.walkingCount = self.walkingRate # frames until next step
      self.curDirection = None
      self.isWalking = False
      self.isDead = False
      self.isAttacking = False

      self.curAnim = self.lfWalk
      self.image = self.curAnim.next()
      self.rect = self.image.get_rect()
      if center is not None:
         self.rect.center = center

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
      if not self.isAttacking and not self.isDead:
         self.attackFramesLeft = settings.fps / 3
         self.isAttacking = True
         self.image = self.battleStance

   def attack(self):
      if self.attackFramesLeft > (settings.fps / 6):
         self.rect.move_ip((-1, 0))
      elif self.attackFramesLeft > 0:
         self.rect.move_ip((1, 0))
      elif self.attackFramesLeft <= 0:
         self.isAttacking = False
         print "Final location: %d, %d\n" % (self.rect.center)
      self.attackFramesLeft -= 1
