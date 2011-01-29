''' Dumb NPC class and some supporting functions for them. '''
import settings
import pygame

import random

# TODO: Move readWalklingAnimations somewhere else
from character import Character
from shared.direction import Direction

class DumbNPC(Character):
   def __init__(self, walkDelay=settings.fps):
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
