import random
from shared.load import load_weapon_data, load_armor_data

class Weapon(object):
   def __init__(self, name, lowdmg, highdmg, elem):
      self.name = name
      self.lowdmg = lowdmg
      self.highdmg = highdmg
      self.elem = elem if elem is not None else "none"

   @staticmethod
   def load(name):
      jsonData = load_weapon_data(name)
      return Weapon(jsonData['name'], jsonData['lowdmg'],
                    jsonData['highdmg'], jsonData['elem'])

   def getDamage(self):
      damage = random.randint(self.lowdmg, self.highdmg)
      print "DEBUG: %s damages for %d" % (self.name, damage)
      return damage

   def __repr__(self):
      out = (self.name, self.lowdmg, self.highdmg, self.elem)
      return "%s, Damage Range %d-%d, Element %s" % out
   def __str__(self):
      return self.name

class Armor(object):
   def __init__(self, name, lowred, highred, elem):
      self.name = name
      self.lowred = lowred
      self.highred = highred
      self.elem = elem if elem is not None else "none"

   @staticmethod
   def load(name):
      jsonData = load_armor_data(name)
      return Armor(jsonData['name'], jsonData['lowred'],
                   jsonData['highred'], jsonData['elem'])

   def getDamageReduction(self):
      reduction = random.randint(self.lowred, self.highred)
      print "DEBUG: %s damages for %d" % (self.name, reduction)
      return reduction

   def __repr__(self):
      out = (self.name, self.lowred, self.highred, self.elem)
      return "%s, Damage Reduction %d-%d, Element %s" % out
   def __str__(self):
      return self.name
