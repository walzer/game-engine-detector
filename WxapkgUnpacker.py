#!/usr/bin/env python2

# lrdcq
# usage python2 unwxapkg.py filename

import sys, os
import struct

def run(name):

  root = os.path.dirname(os.path.realpath(name))

  f = open(name, 'rb')

  #read header

  firstMark = struct.unpack('B', f.read(1))[0]
  print 'first header mark = ' + str(firstMark)

  info1 = struct.unpack('>L', f.read(4))[0]
  print 'info1 = ' + str(info1)

  indexInfoLength = struct.unpack('>L', f.read(4))[0]
  print 'indexInfoLength = ' + str(indexInfoLength)

  bodyInfoLength = struct.unpack('>L', f.read(4))[0]
  print 'bodyInfoLength = ' + str(bodyInfoLength)

  lastMark = struct.unpack('B', f.read(1))[0]
  print 'last header mark = ' + str(lastMark)

  if firstMark != 0xBE or lastMark != 0xED:
    print name + 'is not a wxapkg file!!!!!'
    return

  fileCount = struct.unpack('>L', f.read(4))[0]
  print 'fileCount = ' + str(fileCount)

  # read index

  fileList = []
  

  class WxapkgFile(object):
    nameLen = 0
    name = ""
    offset = 0
    size = 0

  for i in range(fileCount):
    data = WxapkgFile()
    data.nameLen = struct.unpack('>L', f.read(4))[0]
    data.name = f.read(data.nameLen)
    data.offset = struct.unpack('>L', f.read(4))[0]
    data.size = struct.unpack('>L', f.read(4))[0]

    print 'readFile = ' + data.name + ' at Offset = ' + str(data.offset)

    fileList.append(data)

  # save files

  name = os.path.basename(f.name)
  taget_root = root + '/../wxapkgs_unpacked/' + os.path.basename(name)

  for d in fileList:
    # target_path = root + '/../wxapkgs_unpacked/' + os.path.basename(name) + '_dir'
    target_name = os.path.basename(d.name)
    target_path = taget_root + os.path.dirname(d.name)

    if not os.path.exists(target_path):
      os.makedirs(target_path)

    w = open(target_path + '/' + target_name, 'w')
    f.seek(d.offset)
    w.write(f.read(d.size))
    w.close()

    print 'writeFile = ' + target_path + target_name

  f.close()
