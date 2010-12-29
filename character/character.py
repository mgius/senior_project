''' Character class and some supporting functions for them. '''
import settings
import pygame

from collections import deque
from itertools import cycle
from glob import iglob

from shared.direction import Direction
from shared.load import load_sprites_glob, load_sprite

def readWalkingAnimation(name):
   ''' Reads in a two-piece walking animation from the sprite dir,
       and places the animation in a cyclical data structure so that
       it can be iterated over infinitely
       TODO: Support restarting the animation?  may have to reimplement cycle
   '''
   walk = []
   for sprite in load_sprites_glob(name + '*.gif'):
      walk.append(sprite)
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
      self.walkingRate = settings.fps / 10 # frames between steps
      self.walkingCount = self.walkingRate # frames until next step
      self.directionQueue = deque()
      self.directionBitSet = 0
      self.curDirection = None
      self.isWalking = False
      self.isDead = False
      self.isAttacking = False

      self.curAnim = None
      self.image = self.battleStance
      self.rect = self.image.get_rect()
      if center is not None:
         self.rect.center = center

   def startWalking(self, direction):
      if self.isDead:
         return
      # somebody spamming a direction key, the jerk
      if self.curDirection == direction:
         return
      # we best be walking now
      self.isWalking = True

      # OR in the new direction
      self.directionBitSet |= direction
      # and add it to the queue of directions
      self.directionQueue.append(direction)

   def stopWalking(self, direction):
      self.directionBitSet &= ~direction
      # should probably reset to a standing pose...hmm....
      # probably will be handled by block based moving, assuming I time the
      # animation correctly

   def _setwalkingdirection(self, direction):
      self.curDirection = direction
      print "DEBUG: direction: %d" % direction
      if direction == Direction.LEFT:
         self.curAnim = self.lfWalk
         self.speed = [-4, 0]
      elif direction == Direction.FRONT:
         self.curAnim = self.frWalk
         self.speed = [0, 4]
      elif direction == Direction.RIGHT:
         self.curAnim = self.rtWalk
         self.speed = [4, 0]
      elif direction == Direction.BACK:
         self.curAnim = self.bkWalk
         self.speed = [0, -4]

      self.image = self.curAnim.next()
      # Force a frame update
      self.walkingCount = self.walkingRate

   def _walkingAnimation(self):
      self.rect.move_ip(self.speed)
      print "Speed: %s" % self.speed
      print "Current Location: %d, %d\n" % self.rect.center

      if self.walkingCount >= self.walkingRate:
         self.walkingCount = 0
         self.image = self.curAnim.next()
      else:
         self.walkingCount += 1


   def _walk(self):
      print "DEBUG: Character center: %d, %d" % self.rect.center
      if self.isWalking and not (self.rect.centerx % 32) and not (self.rect.centery % 32):
         if self.directionBitSet == 0:
            # empty out the direction queue and stop walking
            self.isWalking = False
            self.directionQueue.clear()
            self.curDirection = None
            return
         elif self.curDirection == None or (self.directionBitSet & self.curDirection) == 0:
            # current direction has been lifted
            while len(self.directionQueue) != 0:
               direction = self.directionQueue.popleft()
               if (direction & self.directionBitSet) != 0:
                  self._setwalkingdirection(direction)
                  break;
      # finally, trigger the walking animation
      print "DEBUG: About to animate\n"
      self._walkingAnimation()


   def update(self):
      if self.isDead:
         return
      if self.isAttacking:
         self._attack()
      if self.isWalking:
         self._walk()

   def _die(self):
      self.isDead = True
      self.image = self.deadStance
      self.curDirection = None

   def _revive(self):
      self.isDead = False
      self.image = self.battleStance
      self.curDirection = None

   def startAttack(self):
      if not self.isAttacking and not self.isDead:
         self.attackFramesLeft = settings.fps / 3
         self.isAttacking = True
         self.image = self.battleStance

   def _attack(self):
      if self.attackFramesLeft > (settings.fps / 6):
         self.rect.move_ip((-1, 0))
      elif self.attackFramesLeft > 0:
         self.rect.move_ip((1, 0))
      elif self.attackFramesLeft <= 0:
         self.isAttacking = False
         print "Final location: %d, %d\n" % (self.rect.center)
      self.attackFramesLeft -= 1
