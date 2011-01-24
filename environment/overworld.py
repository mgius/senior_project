import settings

from pygame import Rect
from pygame import sprite
from pygame.locals import *

from environment import Environment

from event import BattleEvent

from wall import Wall

from shared.direction import Direction
from shared.colors import black

from status.overworldstatus import OverWorldStatus

class Overworld(Environment):
   def __init__(self, background, player, location, walls=()):
      Environment.__init__(self, background)
      self.player = player
      self.playergroup = sprite.GroupSingle(player)
      self.walls = sprite.RenderPlain(walls)
      self.__battleAnimShifted = 0
      self.npcgroup = sprite.Group()

      self.sprites = sprite.RenderUpdates()
      self.sprites.add(self.player)

      self.statusBar = OverWorldStatus(self.player, location)

   @staticmethod
   def fromJson(jsonData, player):
      backgroundTile = jsonData["backgroundTile"]
      walls = Wall.fromJson(jsonData["walls"])
      location = jsonData["locationName"]
      return Overworld(backgroundTile, player, location, walls)

   def addNPC(self, npc):
      self.npcgroup.add(npc)
      self.sprites.add(npc)

   def processEvent(self, event):
      if event.type == KEYDOWN:
         if event.key == K_UP:
            self.player.startWalking(Direction.BACK)
         elif event.key == K_LEFT:
            self.player.startWalking(Direction.LEFT)
         elif event.key == K_RIGHT:
            self.player.startWalking(Direction.RIGHT)
         elif event.key == K_DOWN:
            self.player.startWalking(Direction.FRONT)
         # the following events are temporary for testing
         elif event.key == K_d:
            self.player._die()
         elif event.key == K_u:
            self.player._revive()
         elif event.key == K_a:
            self.player.startAttack()

      elif event.type == KEYUP:
         if event.key == K_UP:
            self.player.stopWalking(Direction.BACK)
         elif event.key == K_LEFT:
            self.player.stopWalking(Direction.LEFT)
         elif event.key == K_RIGHT:
            self.player.stopWalking(Direction.RIGHT)
         elif event.key == K_DOWN:
            self.player.stopWalking(Direction.FRONT)

   def update(self):
      self.player.update()
      self.npcgroup.update()
      if sprite.spritecollideany(self.player, self.walls):
         self.player._goback()
      for npc in sprite.groupcollide(self.npcgroup, self.walls, False, False):
         npc._goback()
      npcCollisions = sprite.spritecollide(self.player, self.npcgroup, False)
      if len(npcCollisions) > 0:
         self.sprites.remove(npcCollisions[0])
         self.npcgroup.remove(npcCollisions[0])
         return BattleEvent(self.player, npcCollisions[0])
      return None
         
   
   def draw(self, surface):
      # TODO: shouldn't be reblitting when nothing has changed...probably
      if self._shouldFillBackground:
         self.fill_background(surface)
         self.walls.draw(surface)
      self.sprites.clear(surface, self.clear_callback)
      self.sprites.draw(surface)
      self.statusBar.draw(surface)

   def fulldraw(self, surface):
      self._shouldFillBackground = True
      self.draw(surface)
