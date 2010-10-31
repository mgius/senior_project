class Battle(object):
   def __init__(self, combatants):
      self.combatants = combatants
      compatants.sort(lambda a,b : a.speed < b.speed)
