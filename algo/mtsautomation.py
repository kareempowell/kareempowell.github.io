
#automating the trading operation
import pandas as pd
class MomentumTrader(tpqoa.tpqoa):
    def __init__(self, config_file, momentum):
        super(MomentumTrader, self).__init__(config_file)
        self.momentum = momentum
        self.min_length = momentum + 1
        self.position = 0
        self.units = 10000
        self.tick_data = pd.DataFrame()
    def on_success(self, time, bid, ask):
        trade = False
        # print(self.ticks, end=' ')
        self.tick_data = self.tick_data.append(
            pd.DataFrame({'b': bid, 'a': ask, 'm': (ask + bid) / 2},
               index=[pd.Timestamp(time).tz_localize(tz=None)])
        )
        self.data = self.tick_data.resample('5s', label='right').last().ffill()
        self.data['r'] = np.log(self.data['m'] / self.data['m'].shift(1))
        self.data['m'] = self.data['returns'].rolling(self.momentum).mean()
        self.data.dropna(inplace=True)
        if len(self.data) > self.min_length:
            self.min_length += 1
            if self.data['m'].iloc[-2] > 0 and self.position in [0, -1]:
              o = api.create_order(self.stream_instrument,
                             units=(1 - self.position) * self.units,
                             suppress=True, ret=True)
              print('\n*** GOING LONG ***')
              api.print_transactions(tid=int(o['id']) - 1)
              self.position = 1
        if self.data['m'].iloc[-2] < 0 and self.position in [0, 1]:
              o = api.create_order(self.stream_instrument,
                            units=-(1 + self.position) * self.units,
                            suppress=True, ret=True)
              print('\n*** GOING SHORT ***')
              self.print_transactions(tid=int(o['id']) - 1)
              self.position = -1
#may need to leave this for jupityer
  mt = MomentumTrader('/content/drive/MyDrive/Paueru/Projects/Models/2. AlgoTrading Models/oanda.cfg', momentum=5)
  mt.stream_data('EUR_USD', stop=100)



      
