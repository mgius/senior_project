import shared.element as element
import random
from shared.load import load_spell_data

class Action(object):
   def __init__(self, extradata):
      pass

   def canDoAction(self, attacker, defender):
      return True

   def doAction(self, attacker, defender):
      raise NotImplementedError, "Must be Implemented by Subclass"
   pass

class CastSpell(Action):
   def __init__(self, extradata)
      self.spellname = extradata['spellname']
      self.spell = load_spell_data(spellname)
      self.lowdmg = self.spell['lowdmg']
      self.highdmg = self.spell['highdmg']
      self.mpCost = self.spell['mpCost']
      self.elem = self.spell['elem']
   def canDoAction(self, attacker, defender):
      return self.attacker.curmp >= self.mpCost
   
   def doAction(self, attacker, defender):
      damage = random.randint(self.lowdmg, self.highdmg)
      if element.isWeak(self.elem, defender.armor.elem):
         damage *= 2
      defender.curhp -= damage
      attacker.curmp -= self.mpCost
      print "DEBUG: %s damages %s for %d damage" % (attacker.charactername, defender.charactername, damage)

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
