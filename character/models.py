class Character(object):
   __slot__ = ['name', 'sprite']

class Battleable(Character):
   __slot__ = ['hp', 'mp', 'level', 'exp', 'strategy', 'speed']

class PlayerCharacter(Battleable):
   __slot__ = ['weapon', 'armor', 'items', 'magic']

class Monster(Battleable):
   __slot__ = ['attacks', 'drops']

class NonPlayerCharacter(Character):
   # currently unimplemened
   pass
