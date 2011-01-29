''' Player Character class and some supporting functions for them. '''
import settings
import pygame

from collections import deque

from character import Character

from shared.direction import Direction

class PlayerCharacter(Character):
   ''' Sets up movement rules for a player controlled character '''
   def __init__(self):
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
