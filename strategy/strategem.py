from action import *
from condition import * 
class Strategem(object):
   def __init__(self, action, condition):
      self.action = globals()[action['name']](action)
      self.condition = globals()[condition['name']](condition)

   def __repr__(self):
      return "Strategem: %s when %s" % (self.action.__repr__(), self.condition.__repr__())
   def __str__(self):
      return "Strategem: %s when %s" % (self.action.__str__(), self.condition.__str__())
