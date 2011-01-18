''' Events that can be triggered by an environment that need 
    to be handled by the driver class
'''

class Event(object):
   pass

class BattleEvent(Event):
   def __init__(self, player, opponents):
      self.player = player
      self.opponents = opponents
