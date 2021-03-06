import settings

from shared.load import load_character_data

from character import Character
from dumbnpc import DumbNPC
from battlecharacter import BattleCharacter

class DumbBattleNPC(DumbNPC, BattleCharacter):
   @staticmethod
   def load(name, center=None, walkDelay=settings.fps):
      jsonData = load_character_data(name)

      self = DumbBattleNPC()

      Character.__init__(self, center, jsonData['spritename'])
      DumbNPC.__init__(self, walkDelay)
      BattleCharacter.__init__(self, jsonData)

      return self
