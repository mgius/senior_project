import shared.element as element
import random
from shared.load import load_spell_data

class Action(object):
   def __init__(self, extradata):
      pass

   def __repr__(self):
      return "Generic Action"
   def __str__(self):
      return __repr__(self)

   def canDoAction(self, attacker, defender):
      return True

   def doAction(self, attacker, defender):
      raise NotImplementedError, "Must be Implemented by Subclass"
   pass

class CastSpell(Action):
   def __init__(self, extradata):
      self.spellname = extradata['spellname']
      self.spell = None
      self.lastAttacker = None

   def __repr__(self):
      return "Cast Spell %s" % self.spellname

   def canDoAction(self, attacker, defender):
      if self.lastAttacker is not attacker or self.spell is None:
         self.spell = None
         for spell in attacker.spellbook:
            if spell.name == self.spellname:
               self.spell = spell
               break
         if self.spell is None:
            return False

      print "About to do Spell"
      return attacker.curmp >= self.spell.mpcost
   
   def doAction(self, attacker, defender):
      damage = self.spell.getDamage()
      if element.isWeak(self.spell.elem, defender.armor.elem):
         damage *= 2
      defender.curhp -= damage
      attacker.curmp -= self.spell.mpcost
      print "DEBUG: %s damages %s with %s for %d damage" % (attacker.charactername, defender.charactername, self.spellname, damage)

class Attack(Action):
   def __repr__(self):
      return "Attack Action"

   def doAction(self, attacker, defender):
      damage = attacker.weapon.getDamage()
      reduction = defender.armor.getDamageReduction()
      if element.isWeak(attacker.weapon.elem, defender.armor.elem):
         damage *= 2
      damage -= reduction
      damage = max(1, damage)
      defender.curhp -= damage
      print "DEBUG: %s damages %s for %d damage" % (attacker.charactername, defender.charactername, damage)
