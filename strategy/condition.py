class Condition(object):
   def __init__(self, extradata):
      pass

   def checkCondition(self, attacker, defenders):
      raise NotImplementedError, "Must be implemented by subclass"

class Always(Condition):
   def checkCondition(self, attacker, defenders):
      return defenders[0]
