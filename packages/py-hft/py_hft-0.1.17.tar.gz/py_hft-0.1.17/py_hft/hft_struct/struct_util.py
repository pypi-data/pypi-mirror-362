from .market_snapshot import *
from .book_ticker import *
from .order import *
from .exchange_info import *
from collections.abc import Iterable
import sys

def Show(s, f=None):
  if f: f.write(s.__str__()+'\n')
  else: print(s)

def ShowCsv(s, f=None):
  if f: f.write(s.to_csv() + '\n')
  else: print(s.to_csv() + '\n')

def to_csv(s, split_c=','): return split_c.join([str(val) for val in s.__dict__.values()])

def to_series(s): return pd.Series({key:val for key, val in s.__dict__.items()})

def unpack(s, text):
  #print(len(struct.unpack(s.fmt, text)))
  #print(len(s.__dict__.keys()))
  for key, val in zip(s.__dict__.keys(), struct.unpack(s.fmt, text)):
    if isinstance(val, bytes): exec('s.%s=val.decode("utf-8")'%(key))
    else: exec('s.%s=val'%(key))
  return s

def get_size(s): return struct.calcsize(s.fmt)

if __name__ == '__main__':
  shot = MarketSnapshot()
  with open('/QData/market_data/futures/tick/ctp_zhaoshang/20210714/NI1.20210714.bin', 'rb') as f:
    s = f.read()
    unpack(shot, s[100*struct.calcsize(shot.fmt):101*struct.calcsize(shot.fmt)])
    sys.exit(1)
