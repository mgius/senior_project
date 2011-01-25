''' I'm not entirely happy with the way this works.  Ideally I'd use
    something like a Java-style enum (assuming they support recursion...)
    but I'd rather not go into that level of overhead for something this
    simple.
'''

_elemMap = { "fire" : ["ice"],
             "ice" : ["fire"],
             "lighting" : [],
             "none" : [],
           }

def isWeak(attack, defend):
   if attack not in _elemMap:
      return False
   return defend in _elemMap[attack]
