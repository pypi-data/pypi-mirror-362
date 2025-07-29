import time
import pandas as pd
import struct

DEPTH = 5
class BookTicker:
  def __init__(self):
    self.tk_= "none"
    self.ts_ = 1000000000
    self.uts_ = 1000
    self.bp0_ = self.ap0_ = self.bs0_ = self.as0_ = 0.
    self.ex_ = 'B'
    self.type_ = 'S'
  
  @property
  def fmt(self): return '8s16s2Q4dcc6s'

  def pack(self):
    return struct.pack(self.fmt, bytes(self.tk_, 'utf-8'), bytes(self.tk_, 'utf-8'), self.ts_, self.uts_, self.bp0_, self.ap0_, self.bs0_, self.as0_, self.ex_, self.type_,  b'')

  def __str__(self):
    split_char = ' '
    show_content = ""
    show_content += str(self.ts_) + '.' + str(self.uts_)
    show_content += split_char
    show_content += "BOOKTICKER"
    show_content += split_char
    show_content += self.tk_
    show_content += split_char
    show_content += '|'
    show_content += split_char
    show_content += str(self.bp0_) + split_char + str(self.ap0_) + ' | ' + str(self.bs0_) + ' x ' + str(self.as0_) + split_char
    show_content += str(self.ex_)
    show_content += split_char
    show_content += str(self.type_)
    return show_content

if __name__ == '__main__':
  shot = BookTicker()
  shot.tk = "HAHA"
  m = {}
  for i, j in zip(shot.cols, shot.to_csv().split(',')): m[i] = j
  print(pd.Series(m))
