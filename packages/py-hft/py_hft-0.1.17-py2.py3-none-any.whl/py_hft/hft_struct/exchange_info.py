type_list = ['Uninited','Acc','Rej','Cancelled','CancelRej',
'Filled','Pfilled','Position','Unknown']
side_int = {"BUY":1, 'SELL':2}
int_side = {-1:'UNKNOWN', 1:"BUY", 2:'SELL'}
type_int = {type_list[i]:i for i in range(len(type_list))}
int_type = {i:type_list[i] for i in range(len(type_list))}
int_type[-1] = 'uninit'

class ExchangeInfo:
  def __init__(self):
    self.show_time = 1000000000.0
    self.shot_time = 1000000000.0
    self.type = -1;
    self.ticker = 'none';
    self.order_ref = 'none';
    self.trade_size = -1;
    self.trade_price = -1.0;
    self.side = -1;
    self.reason = 'none';

  @property
  def fmt(): return "4Qi32s32sidi64s4s"

  def Check(self):
    return self.type == 5

  def __str__(self):
    show_str = ''
    split_c = ' '
    show_str += repr(self.show_time)
    show_str += split_c
    show_str += repr(self.shot_time)
    show_str += split_c
    show_str += 'exchangeinfo' + split_c
    show_str += self.order_ref + split_c
    show_str += '|' + split_c
    show_str += str(self.trade_price) + '@'+ str(self.trade_size) + split_c
    show_str += str(int_type[self.type]) + split_c
    show_str += self.ticker+split_c
    show_str += int_side[self.side]
    show_str += split_c
    show_str += self.reason
    return show_str

if __name__ == '__main__':
  with open('/today/filled') as f:
    for l in f:
      ei = ExchangeInfo()
      ei.construct(l)
      ei.Show()
