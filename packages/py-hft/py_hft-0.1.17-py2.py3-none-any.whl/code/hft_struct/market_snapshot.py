import time
import pandas as pd
import struct

DEPTH = 5
class MarketSnapshot:
  def __init__(self):
    self.tk_= "none"
    self.ts_ = 1000000000
    self.uts_ = 1000
    for i in range(DEPTH): exec('self.bp%d_=0.'%(i))
    for i in range(DEPTH): exec('self.ap%d_=0.'%(i))
    for i in range(DEPTH): exec('self.bs%d_=0'%(i))
    for i in range(DEPTH): exec('self.as%d_=0'%(i))
    self.lp_ = 0.
    self.tvr_ = 0.
    self.ls_ = 0
    self.vol_ = 0
    self.oi_ = 0
  
  @property
  def fmt(self): return '8s16s2Q10d10idd3i4s'

  def pack(self):
    return struct.pack(self.fmt, bytes(self.tk_, 'utf-8'), bytes(self.tk_, 'utf-8'), self.ts_, self.uts_, self.bp0_, self.bp1_, self.bp2_, self.bp3_, self.bp4_, self.ap0_, self.ap1_, self.ap2_, self.ap3_, self.ap4_, self.bs0_, self.bs1_, self.bs2_, self.bs3_, self.bs4_, self.as0_, self.as1_, self.as2_, self.as3_, self.as4_, self.lp_, self.tvr_, self.ls_, self.vol_, self.oi_, b'')

  def Check(self, ts_check=False):
    if self.price_check:
      if self.bs0_ < 0.1 or self.as0_ < 0.1 or self.lp_ < 0.1 or self.bp0_ < 0.1 or self.ap0_ < 0.1 or len(self.tk_) > 20: return False
    if self.tk_ == 'tk': return False
    if self.tk_ == 'CODE': return False
    return True

  def __str__(self):
    split_char = ' '
    show_content = ""
    show_content += str(self.ts_) + '.' + str(self.uts_)
    show_content += split_char
    show_content += "SNAPSHOT"
    show_content += split_char
    show_content += self.tk_
    show_content += split_char
    show_content += '|'
    show_content += split_char
    for i in range(DEPTH): show_content += str(eval('self.bp%d_'%(i))) + split_char + str(eval('self.ap%d_'%(i))) + ' | ' + str(eval('self.bs%d_'%(i))) + ' x ' + str(eval('self.as%d_'%(i))) + ' |' + split_char
    show_content += str(self.lp_)
    show_content += split_char
    show_content += str(self.ls_)
    show_content += split_char
    show_content += str(self.vol_)
    show_content += split_char
    show_content += 'M'
    show_content += split_char
    show_content += str(self.tvr_)
    show_content += split_char
    show_content += str(self.oi_)
    show_content += split_char
    return show_content

if __name__ == '__main__':
  shot = MarketSnapshot()
  shot.tk = "HAHA"
  m = {}
  for i, j in zip(shot.cols, shot.to_csv().split(',')): m[i] = j
  print(pd.Series(m))
