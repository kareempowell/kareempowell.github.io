class MomentumTimeSeries(bt.strategy)":

#choose a group of bitcoin, indices, and forex

#iterate through the instruments using the select function

  #for each instrument measure their relative performance and store in a list

  #combine this list in a matrix and provide the securities with the lowest correlation and highest sharpe ratio

#return this preferred list of securities

#then select the securities based on the above

#create a function to place orders for each of these securities. batch ordering?

def select_instrument(self):
    #selecting instruments N.B. 1st line previously data = oanda.get_history
    data = api.get_history(
        instrument='EUR_USD',
        start='2025-02-06',
        end='2025-02-07',
        granularity='M1',
        price='M'
    )
    data.info()

  def measure_performance(self):
    #Backtesting: Build out momentum strategy | NB. Why is this backtesting?
    import numpy as np
    data['returns'] = np.log(data['c'] / data['c'].shift(1))
    cols = []
    for momentum in [15, 30, 60, 120, 150]:
        col = f'p_{momentum}'
        data[col] = np.sign(data['returns'].rolling(momentum).mean())
        cols.append(col)
    
    #visualize strategy performance | N.B. line 2 previously 'seaborn'
    from pylab import plt
    plt.style.use('seaborn-v0_8-colorblind')
    strats = ['returns']
    for col in cols:
        strat = f's_{col[2:]}'
        data[strat] = data[col].shift(1) * data['returns']
        strats.append(strat)
    data[strats].dropna().cumsum().apply(np.exp).plot(cmap='coolwarm');

#initialize a sub-class
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

#Closing out orders

def closingactiveorders(self):
    #[3c]
    #closing out the final position. shows the complete, detailed order object
    from pprint import pprint
    o = mt.create_order('EUR_USD', units=-mt.position * mt.units,
                        suppress=True, ret = True)
    print('\n*** POSITION CLOSED ***')
    mt.print_transactions(tid=int(o['id']) - 1)
    print('\n')
    pprint(o)
    
          
