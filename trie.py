import sys, os

class Trie(object):
  def __init__(self, f, data=None):
    self.f = f
    self.data = data
    self.value = None
    self.key = None

    if data is None:
      f.seek(2, 2)
      while f.read(1) != '\n':
        f.seek(-2, 1)
      self.pos = int(f.readline())
    else:
      bits = data.split(' ')
      self.key = bits[0]

      if bits[1] == '-':
        self.pos = None
      else:
        self.pos = int(bits[1])
      if len(bits) > 2:
        self.value = ' '.join(bits[2:])
  
  def __iter__(self):
    if self.pos is None:
      return
    self.f.seek(self.pos)
    for line in self.f:
      line = line[:-1]
      if not line: break
      yield Trie(self.f, line)

  def __repr__(self):
    return '<Trie ' + repr(self.key) + '>'

  def search(self, path):
    "FIXME: use binsearch, this'll require changing the format so we know where the node ends."
    if not path:
      return self
    for trie in self:
      if trie.key == path[0]:
        return trie.search(path[1:])

if __name__ == '__main__':
  t = Trie(file('index.trie'))
  print t.search([])
  print t.search('155.144.24.81/_images/pics_utilities/aec_hy_red.gif'.split('/')).data
