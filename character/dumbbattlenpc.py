from shared.load import load_character_data
from dumbnpc import DumbNPC
import equipment

from strategy.strategem import Strategem

class DumbBattleNPC(DumbNPC):
   @staticmethod
   def load(name, center=None, walkDelay=0):
      jsonData = load_character_data(name)

      bc = DumbBattleNPC()
      spritename = jsonData['spritename']
      DumbNPC.__init__(bc, center, spritename, walkDelay)

      bc.charactername = jsonData['charactername']

      bc.maxhp = jsonData['maxhp']
      bc.curhp = bc.maxhp
      bc.maxmp = jsonData['maxmp']
      bc.curmp = bc.maxmp
      
      bc.weapon = equipment.Weapon.load(jsonData['weapon'])
      bc.armor = equipment.Armor.load(jsonData['armor'])

      bc.strategy = []
      for strategem in jsonData['strategems']:
         bc.strategy.append(Strategem(strategem['action'], strategem['condition']))

      return bc

