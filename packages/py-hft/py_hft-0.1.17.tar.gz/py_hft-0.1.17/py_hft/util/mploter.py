from .util import *
import matplotlib
import matplotlib.pyplot as plt
import math
import datetime
import matplotlib.dates as mdate
from collections import defaultdict
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

class Plotor:
  def __init__(self, one_width=5, area=80):
    pass

  @staticmethod
  def plot_one(ax, data, label, mode='plot'):
    if mode == 'twin' or mode == 'twinx':
      if '@' in label: mode = label.split('@')[-1]; label = '@'.join(label.split('@')[:-1])
      else: mode = 'plot';
      this_ax=ax.twinx(); this_ax._get_lines.get_next_color();# Handle TWIN
    elif mode=='twiny': #mode = 'plot';this_ax=ax.twiny(); next(this_ax._get_lines.prop_cycler);# Handle TWIN
      if '@' in label: mode = label.split('@')[-1]; label = '@'.join(label.split('@')[:-1])
      else: mode = 'plot';
      this_ax=ax.twiny(); this_ax._get_lines.get_next_color();# Handle TWIN
    elif mode=='twinxy':# mode = 'plot';this_ax=ax.twinx().twiny(); next(this_ax._get_lines.prop_cycler);# Handle TWIN
      if '@' in label: mode = label.split('@')[-1]; label = '@'.join(label.split('@')[:-1])
      else: mode = 'plot';
      this_ax=ax.twinx().twiny(); this_ax._get_lines.get_next_color();# Handle TWIN
    else: this_ax = ax
    if label == 'vline' or label == 'hline':
      for line in data: exec("this_ax.ax%s(line, ls='--', c='black')"%(label));
      return;
    elif label == 'annotate':  # annotate, format should be [{'title':, 'pos':}]
      for ana in data:
        title, pos, dist = ana['title'], ana['pos'], ana['dist'] if 'dist' in ana else (+15, -15)
        this_ax.annotate(title, xy=pos, xycoords='data', xytext=dist, textcoords='offset points', fontsize=12, arrowprops=dict(arrowstyle='-'), color='black')
      return
    if isinstance(data, pd.Series): x, y = data.index, data.values
    elif isinstance(data, dict) or isinstance(data, defaultdict): temp = sorted(data.items(), key=lambda x:x[0]);x, y = [x for x, y in temp], [y for x, y in temp]
    elif isinstance(data, list) or isinstance(data, np.ndarray): x, y = range(len(data)), data
    elif isinstance(data, tuple): x, y = data
    elif isinstance(data, pd.DataFrame): this_ax.table(cellText=data.round(3).values, colLabels=data.columns, rowLabels=data.index, loc='center', colWidths = [0.9/len(data.columns)]*len(data), label=label);this_ax.axis('off');return
    else: p('unknown data type', type(data)); sys.exit(1)
    if mode == 'plot':  this_ax.plot(x, y, label=label)
    elif mode == 'bar': this_ax.bar(range(len(x)), y, alpha=0.8, label=label); this_ax.set_xticklabels([x[int(i)] if i >= 0 and i < len(x) else 'NAN' for i in this_ax.get_xticks()]);
    #print([x[int(i)] if i >= 0 and i < len(x) else 'NAN' for i in this_ax.get_xticks()]); 
    elif mode == 'barh': this_ax.barh(range(len(x)), y, alpha=0.8, label=label); this_ax.set_yticklabels([x[int(i)] if i >= 0 and i < len(x) else 'NAN' for i in this_ax.get_yticks()]);
    elif mode == 'hist': this_ax.hist(data, bins=200, alpha=0.5, label=label)
    elif mode == 'scatter': this_ax.scatter(x, y, label=label, s=1)
    elif mode == 'pie': this_ax.pie(y, labels=x)
    elif mode == 'acf': plot_acf(pd.Series(y), this_ax, label=label);
    else: p('unknown mode', mode); sys.exit(1)

  @staticmethod
  def MultiPlot3(m, fig_name='default', show=False, prefix='', save_dir=os.environ['HOME']+'/MultiPlot', png_width=3, zoom=1.0, width_zoom=1., with_number = False, sc=1, full=False):
    # m = {subfig_title : {subfig_label: data -> list or dict}}
    s = time.time()
    #if not save_dir.startswith(os.environ['HOME']): save_dir = os.environ['HOME'] + '/' + save_dir
    os.system('install -d %s' % (save_dir))
    ksize = len(m.keys())
    fig_size = ((15 * zoom, 6 * zoom * width_zoom) if not full else (18 * zoom, 9 * zoom * width_zoom)) if png_width > 1 else (8 * zoom, 15 * zoom * width_zoom)
    ncol = min(math.ceil(math.sqrt(ksize)), png_width)
    nrow = min(math.ceil(ksize*1.0 / ncol), png_width) if png_width != 1 else ksize
    fig,ax = plt.subplots(nrows=nrow,ncols=ncol,figsize=fig_size);# fig.tight_layout()
    mitem = sorted(m.items(), key=lambda x: x[0])
    for count, (subfig_title, subfig_data) in enumerate(mitem):
      if count % (ncol*nrow) == 0 and count > 0: fig.tight_layout(); fig.savefig(save_dir+'/'+fig_name.replace('.', '_') + str(count) if with_number else fig_name.replace('.', '_')); fig,ax = plt.subplots(nrows=nrow,ncols=ncol,figsize=fig_size); print('finished @%d' %(count))  # open another fig
      this_ax = ax if nrow == 1 else ax[int(count/ncol)%nrow] if ncol == 1 else ax[int(count/ncol)%nrow, count%ncol];# this_ax.set_title(prefix+'@'+subfig_title); this_ax.grid()
      if isinstance(subfig_data, dict): # get into plot data
        #if isinstance(list(subfig_data.values())[0], int) or isinstance(list(subfig_data.values())[0], float):  # compatile for previous version
          #plt.plot(list(subfig_data.keys()), list(subfig_data.values()), label='empty');plt.grid();plt.legend()
          #continue
        for label, data in subfig_data.items():  # one label, one curve
          label = str(label)
          label, this_mode = ('@'.join(label.split('@')[:-1]), label.split('@')[-1]) if '@' in label else (label, 'plot')
          Plotor.plot_one(ax=this_ax, data=data, label=label, mode=this_mode)
          if this_mode != 'pie': this_ax.legend()
      else: Plotor.plot_one(ax=this_ax, data=subfig_data, label='empty', mode='plot'); this_ax.legend()
      this_ax.set_title(prefix+'@'+subfig_title); this_ax.grid()
      #if len(''.join(map(str, plt.xticks()[0]))) > 40:
      this_ax.xaxis.set_tick_params(rotation=30)
      #this_ax.tight_layout()
    fig.tight_layout();
    png_file = '%s/%s%s' % (save_dir, fig_name, '@%d'%(count) if with_number else '')
    fig.savefig(png_file.replace('.', '_'))
    if show: plt.show()
    else: RedPrint('Saving png to ', png_file, color='blue')
    #RedPrint('multiplot3 cost', time.time() - s)

if __name__ == '__main__':
  pt = Plotor()
  m = {"a":[i**2 for i in range(100)], "b":[i**3 for i in range(100)]}
  tm = {"a":{str(i):[(i+1)*j for j in range(100)] for i in range(2)}}
  tm['a']['test_twin'] = [i**2*10 for i in range(100)]
  m = {'IH': {"x":{1:398.26281569824187, 2:676.8502469238279}, 'vline':[1.5, 1.7], 'hxy_twin':[1,2,3], 'hline':[500], 'annotate':[{'title':'open', 'pos':(1.5, 400)}]}, 'IC': [543.9928998046876, 1008.4046122070322, 1472.891766406251, 1937.4634248046896], 'ni': [86.0, 142.0], 'IF': [430.87182810058596, 742.1164718994141]}
  #m = {str(i):[543.9928998046876, 1008.4046122070322, 1472.891766406251] for i in range(25)}
  #m = {'ni': {'raw': {datetime.date(2019, 3, 7): -50.0}, 'net': {datetime.date(2019, 3, 7): -74.0}}}
  a = {'20190912': {'netpnl': {'IC': [0, -0.8000000000001819, -0.6000000000003638, -3.600000000000364, -6.599999999999454]}, 'slip_twin': [292.1999999999998, 4.199999999999818, -10414.2, 3.4000000000005457, 10400.6, -15.0, -10447.2, 3.2000000000007276]}, 'huang':[1,2,3,4]}
  #a = {'20190912': {'netpnl': {start_ts +i*3600  :v for i, v in enumerate([0, -0.8000000000001819, -0.6000000000003638, -3.600000000000364, -6.599999999999454])}}}
  a = {'123':{'asd@scatter':{1:2, 2:3, 3:4}, 'vline':[1.2, 1.3]}, '2@bar':[1,2,3,4]}
  #pt.MultiPlot2(a, 'test', show=True)
  #pt.MultiPlot3({'123':([1,2,3], [1,2,3]), '1':{'1@scatter':(range(1000), range(100, 1100)),'2':(range(1000), range(1100, 2100)), 'annotate':[{'title':'asd', 'pos':(1,2), 'dist':(0,0)}]},'22':{'xhy':pd.Series({dt.datetime.strptime('20190101', '%Y%m%d'):2, dt.datetime.strptime('20200101', '%Y%m%d'):3})}, 'asd':{'asd@df':pd.DataFrame(np.reshape(range(100), (20,5)))}}, show=True)
  s = pd.Series({'a':3, 'b':2, 'c':4, 'd':8, 'ee': 10})
  #pt.MultiPlot3({'asd':{'a@bar':s, 'annotate':[{'pos':(i, ss/2),'dist':(0.05,0.05), 'title':'test'} for i, ss in enumerate(s)]}}, show=True)
  #pt.MultiPlot3({'asd':{'a@bar':s, 'b@bar@twin':[10, 20, 25]}}, show=True, full=True)
  pt.MultiPlot3({'asd':{'a@acf':list(range(100))}}, show=True, full=True)
  pt.MultiPlot3({'asd':{'a@pie':{'a':1, 'b':2, 'c':3}}}, show=True, full=True)
