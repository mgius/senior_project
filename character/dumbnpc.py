''' Dumb NPC class and some supporting functions for them. '''
import settings
import pygame

from collections import deque
from itertools import cycle
from glob import iglob
import random

# TODO: Move readWalklingAnimations somewhere else
from character import Character, readWalkingAnimations
from shared.direction import Direction
from shared.load import load_sprites_glob, load_sprite

class DumbNPC(Character):
   def __init__(self, center=None, spritename='ftr1', walkDelay=0):
      Character.__init__(self, center, spritename)
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

   def _setwalkingdirection(self, direction):
      self.curDirection = direction
      #print "DEBUG: direction: %d" % direction
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

   #def _walkingAnimation(self):

   # TODO: this is an absolute mess, clean it up
   def _walk(self):
      print "In NPC _walk"
      if self.toWait > 0:
         self.toWait -= 1
         return
      elif self.isWalking and divmod(self.rect.centerx, 32)[1] == 16 and divmod(self.rect.centery, 32)[1] == 16:
         self.isWalking = False
         self.curDirection = None
         if self.shouldBeWalking:
            self.toWait = self.walkDelay
         return
      elif self.shouldBeWalking and self.toWait == 0:
         self.curDirection = random.choice(direction.DIRECTIONS)

      self._walkingAnimation()

   #def _goback(self):

   #def update(self):

   #def _die(self):

   #def _revive(self):

   #def startAttack(self):

   #def _attack(self):
