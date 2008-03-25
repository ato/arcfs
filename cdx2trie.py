import sys

class Outer(object):
  def __init__(self, f):
    self.pos = 0
    self.f = f

  def write(self, data):
    self.f.write(data)
    self.pos += len(data)

  def tell(self):
    return self.pos

class PeakFile(object):
  def __init__(self, f):
    self.f = f
    self.pushed = []

  def readline(self):
    if self.pushed:
      return self.pushed.pop()
    line = self.f.readline()
    return line

  def pushline(self, line):
    self.pushed.append(line)

def getline(f):
  fields = f.readline()[:-1].split(' ')
  path = fields[0]
  pathbits = path.split('/')
  return pathbits

def getbits(line):
  return line[:-1].split(' ')[0].split('/')

def doindex(f, o, depth):
  line = f.readline()
  bits = getbits(line)

  node = bits[:depth]
  children = []
  #print '+', '/'.join(node)

  data = ''
  if node == bits:
    i = line.find(' ')
    if i != -1:
      data = line[i:-1]

  while line and len(bits) > depth and bits[:depth] == node:
    f.pushline(line)
    children.append(doindex(f, o, depth + 1))
    line = f.readline()
    bits = getbits(line)

  if bits[:depth] != node:
    f.pushline(line)

  if children:
    start = o.tell()
    for child in children:
      o.write(child + '\n')
    length = o.tell() - start
  else:
    start = length = '-'

  if node:
    return node[-1] + ' ' + str(start)  + ' ' + str(length) +  data
  return str(start) + ' ' + str(length)

print doindex(PeakFile(sys.stdin), Outer(sys.stdout), 0)
