from character import Character
class BattleCharacter(Character):

   @staticmethod
   def fromJson(jsonData, center=None):
      bc = BattleCharacter()

