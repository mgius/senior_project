import random

from shared.load import load_spell_data

class Spell(object):
   def __init__(self, name, mpcost, lowdmg, highdmg, elem):
      self.name = name
      self.mpcost = mpcost
      self.lowdmg = lowdmg
      self.highdmg = highdmg
      self.elem = elem

   @staticmethod
   def load(name):
      jsonData = load_spell_data(name)
      return Spell(jsonData['name'], jsonData['mpcost'],
                   jsonData['lowdmg'], jsonData['highdmg'],
                   jsonData['elem'])

   def getDamage(self):
      damage = random.randint(self.lowdmg, self.highdmg)
      return damage

   def __repr__(self):
      out = (self.name, self.lowdmg, self.highdmg, self.elem)
      return "%s spell, Damage Range %d-%d, Element %s" % out
   def __str__(self):
      return self.name
