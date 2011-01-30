from character import NonPlayerCharacter, BattleableCharacter, BattleGroup

from shared.load import load_monster_data, load_monstergroup_data

def load_monster(name, center=None):
   try:
      jsonData = load_monstergroup_data(name)
   except IOError:
      jsonData = load_monster_data(name)

   return globals()[jsonData['monstertype']](jsonData, center)

class BattleableNonPlayerCharacter(NonPlayerCharacter, BattleableCharacter):
   def __init__(self, jsonData, center=None):
      displayname = jsonData['charactername']
      spritename = jsonData['spritename']

      NonPlayerCharacter.__init__(self, spritename, displayname, center)
      BattleableCharacter.__init__(self, jsonData)


class BattleableNonPlayerCharacterGroup(NonPlayerCharacter, BattleGroup):
   def __init__(self, jsonData, center=None):
      displayname = jsonData['displayname']
      spritename = jsonData['spritename']

      NonPlayerCharacter.__init__(self, spritename, displayname, center)
      
      BattleGroup.__init__(self, [load_monster(name) for name in jsonData['members']])
