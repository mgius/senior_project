import shared.element as element

class Action(object):
   def __init__(self, extradata):
      pass

   def doAction(self, attacker, defender):
      raise NotImplementedError, "Must be Impleented by Subclass"
   pass

class Attack(Action):
   def doAction(self, attacker, defender):
      damage = attacker.weapon.getDamage()
      reduction = defender.armor.getDamageReduction()
      if element.isWeak(attacker.weapon.elem, defender.armor.elem):
         damage *= 2
      damage -= reduction
      damage = max(1, damage)
      defender.curhp -= damage
      print "DEBUG: %s damages %s for %d damage" % (attacker.charactername, defender.charactername, damage)
