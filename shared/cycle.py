import itertools
class cycle(object):
   def __init__(self, iterable):
      self.backup = [x for x in iterable]
      self.cycle = itertools.cycle(self.backup)

   def next(self):
      return self.cycle.next()
   
   def reset(self):
      self.cycle = cycle(self.backup)
