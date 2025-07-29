import pandas as pd
import numpy as np
import psutil
from tqdm import tqdm
import glob
from numpy import random
import os
import sys
import datetime as dt
from functools import reduce
import multiprocessing
import traceback
from queue import Queue
from collections.abc import Iterable
from collections import defaultdict
import time
import warnings
from tabulate import tabulate
from termcolor import colored
warnings.filterwarnings('ignore')

def timer(func):
  def wrapper(*args, **kwargs):
    s = time.time()
    r = func(*args, **kwargs)
    RedPrint('['+func.__name__+']', 'cost', time.time()-s, color='green')
    return r
  return wrapper

def header(func):
  def wrapper(*args, **kwargs):
    h(func.__name__)
    r = func(*args, **kwargs)
    t(func.__name__)
    return r
  return wrapper

def GetCon(ticker):
  for i, c in enumerate(ticker):
    if c.isdigit(): return ticker[:i]
  return ticker

def loop(func, params):
  pbar = tqdm(total=len(params), desc='Looping', colour="cyan")
  for param in params:
    pbar.set_description('Processing %s'%(str(param)))
    if isinstance(param, list): func(*param)
    else: func(param)
    pbar.update(1)

def current_time():
  sec = tme.mktime(dt.datetime.now().timetuple())
  usec = dt.datetime.now().microsecond
  return sec + usec / 1e7

def get_date(delta = 0):
  return (dt.date.today() + dt.timedelta(days=delta)).strftime('%Y%m%d')

def dateRange(beginDate, endDate, split_c='-'):
  split_c='-' if '-' in beginDate else ''
  dates = []
  d = dt.datetime.strptime(beginDate, '%Y' + split_c + '%m' + split_c + '%d')
  date = beginDate[:]
  while date <= endDate:
    dates.append(date)
    d = d + dt.timedelta(1)
    date = d.strftime('%Y' + split_c + '%m' + split_c + '%d')
  return dates

def Throw(func, args=(), dicts={}):
  multiprocessing.Process(target=func, args=args, kwargs=dicts).start()

@timer
def MPRun(func, args, dicts={}, n_pool= max(multiprocessing.cpu_count()-2, 1)):
  RedPrint('submit a multiprocess task with cpu', n_pool, color='purple')
  n_pool = multiprocessing.cpu_count()-n_pool-1 if n_pool < 0 else n_pool
  q = Queue()
  if not isinstance(args, list) or not isinstance(dicts, dict): RedPrint('args should be list, dicts should be dict', type(args), type(dicts)); sys.exit(1)
  pool = multiprocessing.Pool(processes=n_pool)
  res = []
  pbar = tqdm(total=len(args), desc=ColorString('MPRun %s'%(func.__name__), color='blue'), colour="cyan")
  for i, arg in enumerate(args):
    if not isinstance(args[0], list): q.put(pool.apply_async(func, tuple([arg]), dicts))
    else: q.put(pool.apply_async(func, tuple(arg), dicts))
  count = 0
  r = []
  while count < len(args):
    r.append(q.get().get())
    count += 1
    pbar.update(1)
  pbar.close()
  pool.close()
  pool.join()
  return r

def home_path():
  return os.environ['HOME']+'/'

color_list = ['black', 'red', 'green', 'yellow', 'blue', 'purple', 'cran', 'white']
fore_color = {c: i + 30 for i, c in enumerate(color_list)}
back_color = {c: i + 40 for i, c in enumerate(color_list)}
#show_list = ['default', 'highlight', 'underline', 'shinning', 'reverse', 'invisiable']
#show_way = {sl : i for i, sl in enumerate(show_list)}

def pretty_show(d, rd=-1):
  print(tabulate(d.round(rd) if rd > 0 else d, tablefmt='pretty', numalign='left', headers=d.columns))
  #RedPrint(tabulate(d.round(round_digit), tablefmt='pretty', numalign='left', headers=d.columns), color='blue')

def show_with_color(df, thr = 0., rd = -1):
  for col in df.columns: df[col] = [colored(str(x), None, 'on_red') if x < thr else str(x) for x in df[col]]
  pretty_show(df, rd)

def ColorString(*s, color='red'):
  fore, back = 30, 40
  if color in fore_color: fore = fore_color[color]
  if color in back_color: back = back_color[color]
  return '\033[%dm%s\033[0m'%(fore, ' '.join(map(lambda x: str(x), s)))

def RedPrint(*s, color = 'red', show='highlight'):
  print(ColorString(*s, color=color))

def h(*s, color='red', num = 13, chr ='#'):
  s = map(lambda x: str(x), s)
  RedPrint(chr*num, 'HEAD['+' '.join(s)+']', chr*num, color=color)

def t(*s, color='red', num = 13, chr ='#'):
  s = map(lambda x: str(x), s)
  RedPrint(chr*num, 'TAIL['+' '.join(s)+']', chr*num, color=color)

def p(*s, color='green'):
  te = traceback.extract_stack()
  c = [i[2] for i in traceback.extract_stack()]
  call_seq = c[-c[::-1].index('<module>'):]
  prefix = '[' + '->'.join(call_seq) + ']'
  s = map(lambda x: str(x), s)
  RedPrint(prefix, ' '.join(s), color=color)

def Assert(cond, *s, color='purple'):
  te = traceback.extract_stack()
  c = [i[2] for i in traceback.extract_stack()]
  call_seq = c[-c[::-1].index('<module>'):]
  prefix = '[' + '->'.join(call_seq) + ']'
  cs = ColorString(prefix+ 'Assert failed ' + ' '.join(s), color=color)
  assert cond, cs

def checkargtypes(args, func):
  for argname, annotation in func.__annotations__.items():
    if argname == "return": continue
    if type(args[argname]) is not type(annotation):
      print("the type of arg '{}' may be inappropriate.".format(argname))
      return False
  return True

def get_all_function(cls):
  funcs = []
  for i in cls.__dir__():
    if i.startswith('__'): continue
    if hasattr(eval('cls.%s'%(i)), '__call__'): funcs.append(eval('cls.%s'%(i)))
  return funcs

def file_dur(path):
  return (pd.to_datetime(os.path.getatime(path), unit='s').date()-dt.datetime.today().date()) / dt.timedelta(1)

def file_date(path):
  return str(pd.to_datetime(os.path.getatime(path), unit='s').date())

def get_process_memory():
  RedPrint(u'当前进程的内存使用：%.4f GB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024), color='purple')

def GetExpire(df):
  year = (df['date'] / 10000).apply(int)
  y_tag = year % 10
  ticker_y_tag = df['ticker'].str.slice(-3, -2).apply(int)
  ticker_m_tag = df['ticker'].str.slice(-2,).apply(int)
  y_dif = (ticker_y_tag - y_tag + 10) % 10
  a = y_dif[(y_dif > 2) & (y_dif < 0)]
  Assert(len(a) == 0, 'expire date illegal')
  rdate = (year * 10000 + ticker_m_tag * 100 + 28) + (y_dif * 10000)
  #Assert((rdate > df['date']).mean()==1)
  return rdate
 
def reload(lib):
  s = 'import importlib; import %s; importlib.reload(%s); from %s import *;'%(lib, lib, lib)
  return s

def get_default(m, key, default):
  if key in m:
    value = m[key]
    Assert(type(value) == type(default), '%s in params, but type is wrong %s, should be %s' %(key, type(m[key]), type(default)))
    return value
  return default

if __name__ == '__main__':
  #MPRun(A.print, [[a,1],[a,2],[a,3]])
  #Assert(1 == 2)
  print(GetExpire(20191111, 'M102'))
