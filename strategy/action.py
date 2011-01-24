import shared.element as element

class Action(object):
   def __init__(self, extradata):
      pass

   def doAction(attacker, defender):
      raise NotImplementedError, "Must be Impleented by Subclass"
   pass

class Attack(Action):
   def doAction(attacker, defender):
      damage = attacker.weapon.getDamage() - defender.armor.getDamageReduction()
      damage = max(1, damage)
      if element.isWeak(attacker.weapon.elem, defender.armor.elem):
         damage *= 2
      defender.curhp -= damage
