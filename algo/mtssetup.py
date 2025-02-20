

class MomentumTimeSeries(bt.strategy)":

    def connect_to_oanda(self):
      !pip install git+https://github.com/yhilpisch/tpqoa.git
      from google.colab import drive
      drive.mount('/content/drive')
      import tpqoa
      import configparser
      
      # Create a configparser object
      config = configparser.ConfigParser()
      # Read the configuration file
      config.read('/content/drive/MyDrive/Paueru/Projects/Models/2. AlgoTrading Models/oanda.cfg')
      # Check if the 'oanda' section exists
      if 'oanda' in config:
          # If the section exists, create the api object
          api = tpqoa.tpqoa('/content/drive/MyDrive/Paueru/Projects/Models/2. AlgoTrading Models/oanda.cfg')
      else:
          # If the section doesn't exist, print an error message
          print("Error: 'oanda' section not found in the configuration file.")
      # You can print the config to check the content
      # print(config)
      api = tpqoa.tpqoa('/content/drive/MyDrive/Paueru/Projects/Models/2. AlgoTrading Models/oanda.cfg')
  
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
