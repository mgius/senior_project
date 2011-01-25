from playercharacter import PlayerCharacter
from shared.load import load_character_data
import equipment

from strategy.strategem import Strategem

class BattleCharacter(PlayerCharacter):
   @staticmethod
   def load(name, center=None):
      jsonData = load_character_data(name)
      bc = BattleCharacter()
      spritename = jsonData['spritename']
      PlayerCharacter.__init__(bc, center, spritename)

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
