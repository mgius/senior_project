import shared.element as element

class Condition(object):
   def __init__(self, extradata):
      pass

   def __repr__(self):
      return "Generic Condition"
   def __str__(self):
      return self.__repr__()

   def checkCondition(self, attacker, defenders):
      raise NotImplementedError, "Must be implemented by subclass"

class Always(Condition):
   def __repr__(self):
      return "Always"

   def checkCondition(self, attacker, defenders):
      return defenders[0]

class WeakAgainst(Condition):
   def __init__(self, extradata):
      self.targetElement = extradata['targetElement']

   def __repr__(self):
      return "Weak Against %s" % self.targetElement

   def checkCondition(self, attacker, defenders):
      for defender in defenders:
         if element.isWeak(self.targetElement, defender.armor.elem):
            print "DEBUG: About to return %s as target" % defender
            return defender

      print "DEBUG: No target found for weak against %s" % self.targetElement
      return None

class HealthBelow(Condition):
   def __init__(self, extradata):
      self.threshold = extradata['hpThreshold']

   def __repr__(self):
      return "Target Health Below %d" % self.threshold

   def checkCondition(self, attacker, defenders):
      for defender in defenders:
         if defender.hp < self.threshold:
            return defender

      return None

