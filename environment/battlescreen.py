import settings

from pygame import Rect
from pygame import sprite
from pygame.locals import *

from environment import Environment

from operator import itemgetter

from shared.direction import Direction

from status.battlestatus import BattlefieldStatus

from character.character import BattleGroup

class Battlefield(Environment):
   def __init__(self, background, player, enemy):
      Environment.__init__(self, background)
      self.player = player
      self.enemy = enemy
      if isinstance(player, BattleGroup):
         self.players = sprite.Group(player.groupmembers)
      else:
         self.players = sprite.Group(player)
      if isinstance(enemy, BattleGroup):
         self.enemies = sprite.Group(enemy.groupmembers)
      else:
         self.enemies = sprite.Group(enemy)

      self.sprites = sprite.RenderUpdates(self.players, self.enemies)
      self.combatants = sprite.Group(self.players, self.enemies)

      self.alignCombatants(self.players, 608 - 16, Direction.LEFT)
      self.alignCombatants(self.enemies, 32 + 16, Direction.RIGHT)
      
      # TODO: Battlefield status needs to be updated
      self.statusBar = BattlefieldStatus(self.players.sprites()[0], self.enemies.sprites()[0])

      self.frameCount = settings.fps / 2

      self.battleQueue = [ (c.speed, c) for c in self.combatants ]
      self.battleQueue.sort(key=itemgetter(0))

   @staticmethod
   def alignCombatants(combatants, xPos, direction):
      yPos = settings.mapheight / 2 - 32 * len(combatants)
      for combatant in combatants:
          combatant.stopWalking(combatant.curDirection)
          combatant._setwalkingdirection(direction)
          combatant.stopWalking(combatant.curDirection)
          combatant.rect.center = (xPos + 16, yPos + 16)
          yPos += 64

   def update(self):
      if self.frameCount > 0:
         self.frameCount -= 1
         return

      (curTime, character) = self.battleQueue.pop(0)
      while character not in self.players and character not in self.enemies:
         (curTime, character) = self.battleQueue.pop(0)

      # temporary hack
      if character in self.players:
         targets = self.enemies.sprites()
      else:
         targets = self.players.sprites()
      # this should eventually become a part of the players
      for strategem in character.strategy:
         target = strategem.condition.checkCondition(character, targets)
         if target:
            strategem.action.doAction(character, target)
            break

      if target.curhp <= 0:
         # target died
         target.kill()
         if not self.enemies:
            # player wins, return True
            self.enemy.kill()
            return True
         if not self.players:
            return False

         self.statusBar = BattlefieldStatus(self.players.sprites()[0], self.enemies.sprites()[0])

      self.battleQueue.append((curTime + character.speed, character))
      self.battleQueue.sort(key=itemgetter(0))
      self.frameCount = settings.fps / 2
   
   def draw(self, surface):
      # TODO: shouldn't be reblitting when nothing has changed...probably
      if self._shouldFillBackground:
         self.fill_background(surface)
         #self.walls.draw(surface)
      self.sprites.clear(surface, self.clear_callback)
      self.sprites.draw(surface)
      self.statusBar.draw(surface)
