''' Character class and some supporting functions for them. '''
import settings
import pygame
import random

import equipment

from collections import deque

from strategy.strategem import Strategem

from shared.cycle import cycle
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
   def __init__(self, spritename, displayname, center=None):
      pygame.sprite.Sprite.__init__(self)
      # animations and other sprite images
      (self.lfWalk, self.frWalk,
       self.rtWalk, self.bkWalk) = readWalkingAnimations(spritename)
      self.battleStance = load_sprite(spritename + '_battle.gif', -1)
      self.deadStance = load_sprite(spritename + '_dead.gif', -1)

      self.walkingSpeed = [0,0]
      self.walkingRate = settings.fps / 10 # frames between steps
      self.walkingCount = self.walkingRate # frames until next step
      self.curDirection = None
      self.isWalking = False
      self.isDead = False

      self.charactername = displayname

      self.curAnim = None
      self.image = self.battleStance
      self.rect = self.image.get_rect()
      if center is not None:
         self.rect.center = center

   def startWalking(self, direction):
      raise NotImplementedError, "This must be implemented by subclass"

   def stopWalking(self, direction):
      raise NotImplementedError, "This must be implemented by subclass"

   def _setwalkingdirection(self, direction):
      self.curDirection = direction
      #print "DEBUG: direction: %d" % direction
      if direction == Direction.LEFT:
         self.curAnim = self.lfWalk
         self.walkingSpeed = [-4, 0]
      elif direction == Direction.FRONT:
         self.curAnim = self.frWalk
         self.walkingSpeed = [0, 4]
      elif direction == Direction.RIGHT:
         self.curAnim = self.rtWalk
         self.walkingSpeed = [4, 0]
      elif direction == Direction.BACK:
         self.curAnim = self.bkWalk
         self.walkingSpeed = [0, -4]

      self.image = self.curAnim.next()
      # Force a frame update
      self.walkingCount = self.walkingRate

   def _walkingAnimation(self):
      self.rect.move_ip(self.walkingSpeed)

      if self.walkingCount >= self.walkingRate:
         self.walkingCount = 0
         self.image = self.curAnim.next()
      else:
         self.walkingCount += 1

   def _goback(self):
      self.rect.move_ip(-self.walkingSpeed[0], -self.walkingSpeed[1])

   def update(self):
      raise NotImplementedError, "This must be implemented by subclass"

   def _die(self):
      self.isDead = True
      self.image = self.deadStance
      self.curDirection = None

   def _revive(self):
      self.isDead = False
      self.image = self.battleStance
      self.curDirection = None

class PlayerCharacter(Character):
   ''' Sets up movement rules for a player controlled character '''
   def __init__(self, spritename, displayname, center=None):
      Character.__init__(self, spritename, displayname, center)
      self.directionQueue = deque()
      self.directionBitSet = 0

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

   def _walk(self):
      # when in the center of a block, determine if I should still be moving
      if self.isWalking and divmod(self.rect.centerx, 32)[1] == 16 and divmod(self.rect.centery, 32)[1] == 16:
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
      self._walkingAnimation()

   def update(self):
      if self.isDead:
         return
      if self.isWalking:
         self._walk()

class NonPlayerCharacter(Character):
   def __init__(self, spritename, displayname, center=None, walkDelay=settings.fps):
      Character.__init__(self, spritename, displayname, center)
      # frames to wait before choosing a new direction
      self.walkDelay = walkDelay
      self.toWait = walkDelay
      self.shouldBeWalking = False

   def startWalking(self, direction=None):
      if self.isDead:
         return
      # we best be walking now
      self.shouldBeWalking = True

   def stopWalking(self, direction=None):
      self.shouldBeWalking = False

   def _walk(self):
      # not walking, but I should be, or soonish
      if not self.isWalking:
         if self.toWait > 0:
            self.toWait -= 1
            return
         else:
            self._setwalkingdirection(random.choice(Direction.DIRECTIONS))
            self.isWalking = True

      # found a block center
      elif divmod(self.rect.centerx, 32)[1] == 16 and divmod(self.rect.centery, 32)[1] == 16:
         self.isWalking = False
         # shouldn't be walking, exit out
         if not self.shouldBeWalking:
            return
         else:
            self.toWait = self.walkDelay
            return

      self._walkingAnimation()

   def update(self):
      if self.isDead:
         return
      if self.shouldBeWalking or self.isWalking:
         self._walk()

class BattleableCharacter(Character):
   def __init__(self, jsonData):
      ''' Does not call Character.__init__ intentionally '''
      self.charactername = jsonData['charactername']

      self.maxhp = jsonData['maxhp']
      self.curhp = jsonData['curhp'] if 'curhp' in jsonData else self.maxhp

      self.maxmp = jsonData['maxmp']
      self.curmp = jsonData['curmp'] if 'curmp' in jsonData else self.maxmp

      self.speed = jsonData['speed']
      
      self.weapon = equipment.Weapon.load(jsonData['weapon'])
      self.armor = equipment.Armor.load(jsonData['armor'])

      # could be expressed as a list comprehension, but I don't want to
      self.strategy = []
      for strategem in jsonData['strategems']:
         self.strategy.append(Strategem(strategem['action'], strategem['condition']))

   def prepareForBattle(self):
      ''' Backs up certain attributes that are going to be changed 
          during the battle
      '''
      # TODO: Bug if npc runs into me
      self._goback()
      self.backuprect = self.rect.copy()
      self.backupdirection = self.curDirection
      self.backupanim = self.curAnim
      self.backupimage = self.image

   def returnFromBattle(self):
      self.rect = self.backuprect
      del self.backuprect
      self.curDirection = self.backupdirection
      del self.backupdirection
      self.curAnim = self.backupanim
      del self.backupanim
      self.image = self.backupimage
      del self.backupimage

class BattleGroup(Character):
   def __init__(self, groupmembers):
      self.groupmembers = groupmembers
