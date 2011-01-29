from character import Character
import equipment

from strategy.strategem import Strategem

class BattleCharacter(Character):
   def __init__(self, jsonData):
      self.charactername = jsonData['charactername']

      self.maxhp = jsonData['maxhp']
      self.curhp = jsonData['curhp']
      self.maxmp = jsonData['maxmp']
      self.curmp = jsonData['curmp']
      
      self.weapon = equipment.Weapon.load(jsonData['weapon'])
      self.armor = equipment.Armor.load(jsonData['armor'])

      # could be expressed as a list comprehension, but I don't want to
      self.strategy = []
      for strategem in jsonData['strategems']:
         self.strategy.append(Strategem(strategem['action'], strategem['condition']))
