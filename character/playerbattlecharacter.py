from character import Character
from playercharacter import PlayerCharacter
from battlecharacter import BattleCharacter

from shared.load import load_character_data

class PlayerBattleCharacter(PlayerCharacter, BattleCharacter):
   @staticmethod
   def load(name, center=None):
      jsonData = load_character_data(name)

      self = PlayerBattleCharacter()

      Character.__init__(self, center, jsonData['spritename'])
      PlayerCharacter.__init__(self)
      BattleCharacter.__init__(self, jsonData)

      return self
