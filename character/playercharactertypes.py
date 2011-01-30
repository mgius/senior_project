from character import PlayerCharacter, BattleableCharacter, BattleGroup

from shared.load import load_character_data

def load_player(name, center=None):
   jsonData = load_character_data(name)
   return globals()[jsonData['charactertype']](jsonData, center)

class BattleablePlayerCharacter(PlayerCharacter, BattleableCharacter):
   def __init__(self, jsonData, center=None):
      displayname = jsonData['charactername']
      spritename = jsonData['spritename']

      PlayerCharacter.__init__(self, spritename, displayname, center)
      BattleableCharacter.__init__(self, jsonData)


class BattleablePlayerCharacterGroup(PlayerCharacter, BattleGroup):
   def __init__(self, jsonData, center=None):
      displayname = jsonData['displayname']
      spritename = jsonData['spritename']

      PlayerCharacter.__init__(self, spritename, displayname, center)
      
      BattleGroup.__init__(self, [load_player(name) for name in jsonData['members']])
