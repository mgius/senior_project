import shared.element as element

class Condition(object):
   def __init__(self, extradata):
      pass

   def checkCondition(self, attacker, defenders):
      raise NotImplementedError, "Must be implemented by subclass"

class Always(Condition):
   def checkCondition(self, attacker, defenders):
      return defenders[0]

class WeakAgainst(Condition):
   def __init__(self, extradata):
      self.targetElement = extradata['targetElement']

   def checkCondition(self, attacker, defenders):
      for defender in defenders:
         if element.isWeak(self.targetElement, defender.armor.elem):
            return defender

      return None

class HealthBelow(Condition):
   def __init__(self, extradata):
      self.threshold = extradata['hpThreshold']

   def checkCondition(self, attacker, defenders):
      for defender in defenders:
         if defender.hp < self.threshold:
            return defender

      return None

