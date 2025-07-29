import sys
import libpyutil as pyutil
import libpytrade as pymmm
from ..util.util import *
from .struct_util import *
import os
import pandas as pd
import gzip
import time
import glob

class Reader:
  def __init__(self):
    pass

  # load 10G data cost 40s, gzip.read() cost 10s, open.read()(not zipped file) 1s
  @staticmethod
  def load_shot_file(s, file_path):
    shot_size = get_size(s)
    shot_content = gzip.open(file_path).read() if file_path.endswith('.gz') else open(file_path, 'rb').read()
    if len(shot_content) % shot_size != 0: print("%s filesize not shot's times" %(file_path))
    self.shot_size = int(len(shot_content) / shot_size)
    for i in range(shot_size): yield unpack(s, shot_content[i*shot_size:(i+1)*shot_size])

  @staticmethod
  def load_shot_files(files): return [Reader.load_shot_file(f) for f in files]

  @staticmethod
  def load_bt(tickers={'BTC_USDT'}, start_date='20200101', end_date='$TODAY', mp=False, cols= ['bp0_', 'ap0_', 'bs0_', 'as0_', 'ex_', 'type_']):
    start = time.time()
    fd = pymmm.Find(start_date, end_date, tickers)
    tfm = defaultdict(list)
    for date, f in fd.items():
      for topic, path in f.items(): tfm[topic].append(path)
    if mp: df = pd.concat(MPRun(Reader.bt_load,  [[f, topic, cols] for topic, fm in tfm.items() for f in fm]))
    else: df = pd.concat([Reader.bt_load(f, topic, cols) for topic, fm in tfm.items() for f in fm])
    df['sec'] = df['ts_'] % (24*3600)
    df = df[((df['sec'] >= 3600) & (df['sec'] <= 7*3600)) | ((df['sec'] >= 13*3600) & (df['sec'] <= 18.5 * 3600))]
    del df['ts_'], df['sec']
    RedPrint('load cost', time.time()-start,  color='green')
    return df.set_index('dt')

  @staticmethod
  def bt_load(file_path, topic, cols=['bp0_', 'ap0_', 'bs0_', 'as0_', 'ex_', 'type_']):
    shot = BookTicker()
    m = 'a8,a16,i8,i8,' + 'f8,' * 4 + 'a1,a1,a6'
    df = pd.DataFrame(np.frombuffer(open('%s'%(file_path), 'rb').read()[40:], dtype=m))
    df.columns = ['vptr'] + list(shot.__dict__.keys()) + ['left']
    del df['vptr'], df['left']
    tme = df['ts_'] + df['uts_'] / 1e6
    del df['uts_']
    df['tk_'] = df['tk_'].apply(lambda x: str(x)[2:].split('\\x0')[0].split("'")[0])
    df['topic'] = topic
    dtt = pd.to_datetime(tme, unit='s', utc=True).dt.tz_convert('Asia/Shanghai')
    df['dt'] = dtt
    if 'min' in topic or 'daily' in topic:
      rdf = df[set(['ts_', 'tk_', 'dt', 'topic'] + cols + ['bp1_', 'bp2_', 'ap1_', 'ap2_'])]
      rdf = rdf[~np.isnan(rdf['bp2_'])]
      del_cols = ['lp_', 'ls_']
      for col in del_cols: 
        if col in rdf.columns: del rdf[col]
      return rdf.rename(columns={'bp1_':'open', 'bp2_':'low', 'ap1_':'close', 'ap2_':'high'})
    cols = list(set(['ts_', 'tk_', 'dt', 'topic'] + cols))
    return df[cols]


  @staticmethod
  def load(tickers={'JM1'}, start_date='20200101', end_date='$TODAY', mp=False, cols= ['bp0_', 'ap0_', 'bs0_', 'as0_', 'lp_', 'tvr_', 'ls_', 'vol_', 'oi_']):
    start = time.time()
    fd = pymmm.Find(start_date, end_date, tickers)
    tfm = defaultdict(list)
    for date, f in fd.items():
      for topic, path in f.items(): tfm[topic].append(path)
    if mp: df = pd.concat(MPRun(Reader.load_shot,  [[f, topic, cols] for topic, fm in tfm.items() for f in fm]))
    else: df = pd.concat([Reader.load_shot(f, topic, cols) for topic, fm in tfm.items() for f in fm])
    df['sec'] = df['ts_'] % (24*3600)
    df = df[((df['sec'] >= 3600) & (df['sec'] <= 7*3600)) | ((df['sec'] >= 13*3600) & (df['sec'] <= 18.5 * 3600))]
    del df['ts_'], df['sec']
    RedPrint('load cost', time.time()-start,  color='green')
    return df.set_index('dt')

  @staticmethod
  def load_shot(file_path, topic, cols=['bp0_', 'ap0_', 'bs0_', 'as0_', 'lp_', 'tvr_', 'ls_', 'vol_', 'oi_']):
    shot = MarketSnapshot()
    m = 'a8,a16,i8,i8,' + 'f8,' * 10 + 'i4,' * 10 + 'f8,f8,' + 'i4,' * 3 + 'i4'
    df = pd.DataFrame(np.frombuffer(open('%s'%(file_path), 'rb').read()[40:], dtype=m))
    #del df['f24'], df['f29']
    del df['f28']
    df.columns = ['vptr'] + list(shot.__dict__.keys())
    del df['vptr']
    tme = df['ts_'] + df['uts_'] / 1e6
    del df['uts_']
    df['tk_'] = df['tk_'].apply(lambda x: str(x)[2:].split('\\x0')[0].split("'")[0])
    df['topic'] = topic
    dtt = pd.to_datetime(tme, unit='s', utc=True).dt.tz_convert('Asia/Shanghai')
    #df['date'] = dtt.dt.date#.apply(lambda x: int(x.strftime('%Y%M%d')))
    #df['time'] = dtt.dt.time
    df['dt'] = dtt
    if 'min' in topic or 'daily' in topic:
      rdf = df[set(['ts_', 'tk_', 'dt', 'topic'] + cols + ['bp1_', 'bp2_', 'ap1_', 'ap2_'])]
      rdf = rdf[~np.isnan(rdf['bp2_'])]
      del_cols = ['lp_', 'ls_']
      for col in del_cols: 
        if col in rdf.columns: del rdf[col]
      return rdf.rename(columns={'bp1_':'open', 'bp2_':'low', 'ap1_':'close', 'ap2_':'high'})
    #return df[['tk_', 'date', 'time', 'topic'] + cols]
    cols = list(set(['ts_', 'tk_', 'dt', 'topic'] + cols))
    return df[cols]

if __name__=='__main__':
  df = Reader.load_tick(['IC1', 'NI1'], start_date=20200928, end_date=20200928)
  print(df)
