import numpy as np
import datetime as dt

class Order:
  def __init__(self):
    self.shot_time=1000000000.0;
    self.send_time=1000000000.0;
    self.ticker=''
    self.price=-1.0
    self.size=1
    self.traded_size=1
    self.side=-1
    self.order_ref=''
    self.action = -1
    self.status = -1
    self.offset=-1
    self.target_price = -1
    self.shot_latency = 0.0
    self.exchange = ''
    self.tbd=''
    action_list = ['Uninited', 'NewOrder', 'ModOrder', 'CancelOrder', 'QueryPos', 'PlainText']
    status_list = ['Uninited', 'SubmitNew', 'New', 'Rejected', 'Modifying', 'Cancelling', 'Cancelled', 'CancelRej', 'Pfilled', 'Filled', 'Sleep']
    self.action_map = {i:action_list[i] for i in range(len(action_list))}
    self.action_map[-1] = 'Unknown'
    self.status_map = {i:status_list[i] for i in range(len(status_list))}
    self.status_map[-1] = 'Unknown'

  @property
  def fmt(self): return "4Q32sd3i32s3i2d96s32s"

  def __str__(self):
    split_c = ' '
    show_str = ''
    show_str += repr(self.shot_time)
    show_str += split_c   
    show_str += repr(self.send_time)
    show_str += split_c + 'Order' + split_c
    show_str += str(self.ticker)
    show_str += split_c   
    show_str += str(self.price)
    show_str += '@'
    show_str += str(self.size)
    show_str += split_c   
    show_str += str(self.traded_size)
    show_str += split_c
    show_str += "BUY" if self.side == 1 else "SELL"
    show_str += split_c
    show_str += str(self.action_map[self.action])
    show_str += split_c   
    show_str += str(self.status_map[self.status])
    show_str += split_c
    show_str += str(self.shot_latency)
    show_str += split_c
    show_str += self.order_ref
    show_str += split_c   
    show_str += self.tbd
    show_str += split_c   
    show_str += self.exchange
    if self.shot_time < 1e10 and self.shot_time > 1e9:
      show_str += split_c   
      show_str += str(dt.datetime.fromtimestamp(int(self.shot_time)).time())
    return show_str

  def Check(self): return self.action != 4

if __name__=='__main__':
  o = Order()
  with open('/root/order.log') as f:
    for l in f:
      o.construct(l)
      o.Show()
