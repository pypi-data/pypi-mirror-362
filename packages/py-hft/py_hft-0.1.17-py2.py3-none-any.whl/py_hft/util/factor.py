from .util import *
from .mploter import Plotor
import matplotlib.pyplot as plt
import time
import statsmodels.api as sm

def eval_factor(x, y, show=True, save_dir='%s/MultiPlot/'%(home_path()), fig_name = 'default', time=[], date=[]):
  Assert(len(x) == len(y), 'Evaling a length not align factor %d %d'%(len(x), len(y)))
  if len(date) != 0: Assert(len(date) == len(x), 'Passing Date, but len(date) != len(x) %d %d'%(len(date), len(x)))
  df = x.to_frame()
  df[y.name] = y
  if len(time) > 0: df = df.between_time(time[0], time[1], inclusive='left')
  df['group'] = pd.cut(df.index, 10, labels=False)
  gp = df.groupby('group')
  ts_ic  = gp.apply(lambda a: a[x.name].corr(a[y.name]))
  ts_psh = gp.apply(lambda a: (a[y.name]).sum() / a[x.name].abs().sum()) # ensure y is netual
  df['qcut'] = pd.qcut(df[x.name], 1000, duplicates='drop', labels=False)
  gp_qcut = df.groupby('qcut')
  sort_psh = gp_qcut.apply(lambda a: (a[y.name]).mean())# / a[x.name].abs().sum())
  sort_ic  = gp_qcut.apply(lambda a: a[x.name].corr(a[y.name]))
  #print(sort_psh)
  #print(sort_ic)
  #print(ts_psh)
  #print(ts_ic)
  #m = {'ic': {'ts@bar':ts_ic, 'sort@bar':sort_ic}, 'psh':{'ts@bar':ts_psh, 'sort@bar':sort_psh}, 'effsize':eff_plot, 'ts_x':x}
  m = {'sort': {'psh@bar':sort_psh}, 'time_series':{'ic=%.3f@bar'%(df[x.name].corr(df[y.name])):ts_ic, 'psh@twin':ts_psh}, 'effsize':{x.name : (x*y).cumsum()}, 'factor_hist':{'a@hist':x}}
  Plotor.MultiPlot3(m, show=show, save_dir=save_dir, fig_name = fig_name)

@timer
def see_predlength(x, ylist, date = None):
  #Assert(len(x) == len(y), 'Evaling a length not align factor %d %d'%(len(x), len(y)))
  #if date != None: Assert(len(date) == len(x), 'Passing Date, but len(date) != len(x) %d %d'%(len(date), len(x)))
  m, m2 = {}, {}
  for y in ylist: m[y] = x.corr(ylist[y])
  for y in ylist: m2[y] = x.corr(ylist[y], method='spearman')
  plt.plot(m.values(), label='pearson')
  plt.xticks(range(len(m)), list(m.keys()))
  plt.twinx()
  plt.plot(m2.values(), label='spearman')
  plt.xticks(range(len(m2)), list(m2.keys()))
  plt.legend()
  plt.show()

def ols_check(x, y): 
  Assert(len(x) == len(y), "OLS X Y length not equal")
  df = pd.DataFrame()
  df['x'] = list(x)
  df['y'] = list(y)
  df = df.dropna()
  if len(df) / (len(x)*1.) < 0.5: RedPrint('drop na more than 50%, length from %d -> %d'%(len(x), len(df)))
  x = df[['x']]
  y = df['y']
  x = sm.add_constant(x)
  print(sm.OLS(y, x).fit().summary())

def find_corr(df, greater=True, thr=0.6):
  m = []
  for i, (col, row) in enumerate(df.iterrows()):
    for j, (index, val) in enumerate(zip(row.index, row)):
      if i >= j: continue
      if greater and abs(val) > thr:m.append([col, index, val])
      if not greater and abs(val) < thr: m.append([col, index, col])
  return pd.DataFrame(m)

if __name__ == '__main__':
  from ..hft_struct.Reader import Reader
  r = Reader()
  df = r.load({'IC1@cffexl2'}, '20210101', '$TODAY')
  #eval_factor(df['vol_'], df['ap0_'])
  ols_check(df['vol_'], df['ap0_'])
