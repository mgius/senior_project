import settings

import sys, pygame, time, os, math
from pygame.locals import *
from shared.load import load_sprite, load_tile

from character.character import Character

from shared.direction import Direction
pygame.init()

size = width, height = 640, 640
black = 0, 0, 0
white = 255, 255, 255
fps = 30

screen = pygame.display.set_mode(size)

background = load_tile('green_grey.gif')

def processEvents():
   for event in pygame.event.get():
      #print event
      if event.type == QUIT:
         sys.exit(0)
      elif event.type == KEYDOWN:
         if event.key == K_ESCAPE:
            sys.exit(0)
         elif event.key == K_q:
            sys.exit(0)
         elif event.key == K_UP:
            man.startWalking(Direction.BACK)
         #   processEvents.downCount += 1
         elif event.key == K_LEFT:
            man.startWalking(Direction.LEFT)
         #   processEvents.downCount += 1
         elif event.key == K_RIGHT:
            man.startWalking(Direction.RIGHT)
         #   processEvents.downCount += 1
         elif event.key == K_DOWN:
            man.startWalking(Direction.FRONT)
         #   processEvents.downCount += 1
         elif event.key == K_d:
            man._die()
         elif event.key == K_u:
            man._revive()
         elif event.key == K_a:
            man.startAttack()

      elif event.type == KEYUP:
         if event.key == K_UP:
            man.stopWalking(Direction.BACK)
         elif event.key == K_LEFT:
            man.stopWalking(Direction.LEFT)
         elif event.key == K_RIGHT:
            man.stopWalking(Direction.RIGHT)
         elif event.key == K_DOWN:
            man.stopWalking(Direction.FRONT)
         # Avoids issue where fast typist can strike down before releasing previous
         # key
         #if processEvents.downCount <= 0:
         #   man.stopWalking()

man = Character(center=screen.get_rect().center)
print man.rect.center

clock = pygame.time.Clock()
character = pygame.sprite.RenderUpdates((man))
walls = pygame.sprite.RenderPlain()

#processEvents.downCount = 0

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
