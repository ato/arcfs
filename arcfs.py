#!/usr/bin/env python

#  Copyright (C) 2006  Andrew Straw  <strawman@astraw.com>
#
#  This program can be distributed under the terms of the GNU LGPL.
#  See the file COPYING.
#

import os, stat, errno
# pull in some spaghetti to make this stuff work without fuse-py being installed
try:
  import _find_fuse_parts
except ImportError:
  pass
import fuse
from fuse import Fuse
from trie import Trie


if not hasattr(fuse, '__version__'):
  raise RuntimeError, \
    "your fuse-py doesn't know of fuse.__version__, probably it's too old."

fuse.fuse_python_api = (0, 2)

hello_path = '/hello'
hello_str = 'Hello World!\n'

class MyStat(fuse.Stat):
  def __init__(self):
    self.st_mode = 0
    self.st_ino = 0
    self.st_dev = 0
    self.st_nlink = 0
    self.st_uid = 0
    self.st_gid = 0
    self.st_size = 0
    self.st_atime = 0
    self.st_mtime = 0
    self.st_ctime = 0

def breakpath(path):
  bits = path.split('/')[1:]
  if bits == ['']:
    return []
  return bits

class HelloFS(Fuse):
  trie = Trie(file('index.trie'))
  def getattr(self, path):
    t = self.trie.search(breakpath(path))
    st = MyStat()
    if t and t.pos is not None:
      st.st_mode = stat.S_IFDIR | 0755
      st.st_nlink = 2
    elif t:
      st.st_mode = stat.S_IFREG | 0444
      st.st_nlink = 1
      st.st_size = len(t.data)
    else:
      return -errno.ENOENT
    return st

  def readdir(self, path, offset):
    yield fuse.Direntry('.')
    yield fuse.Direntry('..')
    for t in self.trie.search(breakpath(path)):
      yield fuse.Direntry(t.key)

  def open(self, path, flags):
    #if path != hello_path:
    #  return -errno.ENOENT
    accmode = os.O_RDONLY | os.O_WRONLY | os.O_RDWR
    if (flags & accmode) != os.O_RDONLY:
      return -errno.EACCES

  def read(self, path, size, offset):
    t= self.trie.search(breakpath(path))
    if not t:
      return -errno.ENOENT

    hello_str = t.data
    slen = len(hello_str)
    if offset < slen:
      if offset + size > slen:
        size = slen - offset
      buf = hello_str[offset:offset+size]
    else:
      buf = ''
    return buf

def main():
  usage="""
Userspace hello example

""" + Fuse.fusage
  server = HelloFS(version="%prog " + fuse.__version__,
           usage=usage,
           dash_s_do='setsingle')


  server.parse(errex=1)
  server.main()

if __name__ == '__main__':
  main()
