class Direction():
   ''' Python lacks a java-style enum, leading to this
       I also want to be able to do some C-style bit-ops'''
   LEFT = 1
   FRONT = 2
   RIGHT = 4
   BACK = 8

   DIRECTIONS = (LEFT, FRONT, RIGHT, BACK)
