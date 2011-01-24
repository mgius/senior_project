from action import *
from condition import * 
class Strategem(object):
   def __init__(self, action, condition):
      self.action = globals()[action['name']](action)
      self.condition = globals()[condition['name']](condition)

