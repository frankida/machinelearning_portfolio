Readme.txt for using the files for ML for Trading by Frank Hahn fhahn3

indicators.py
-Creates all the necessary indicators
- def get_samples(self, syms=['IBM'], ) returns the insample and outsample
- def convertSMA(self, prices, lookback) returns a DF of SMA by date
-  other similar functions include SMAratio, BB (Bollinger band %), EMA (exponential moving average),
 EMA ratio, and momentum



rule_based.py
- Creates stock trade order based upon indicators by calculating the indicator over the defined period
then creates orders in the period by defined upper and lower limits
- def setShort_Long_Sell(indicator, shortlongcondition, sellcondition) returns list of "buy" or "short" based upon
the indicator and the shortlongcondition.  The shortlongcondition is a decimal number like .02 that is compared against
the indicator
-def createOrders(rules, filename, showtradelines=False) creates an order textfile that can be processed by the
marketsimulator to a csvfile (filename = 'neworders.csv')
- def getrulebased_returns(prices_insample, showtradelines=False) returns the portfolio returns from the trades

ML_based.py
- Uses the RTlearner (retooled to mode vs mean to be a classification learner) and is inputed the indicators to create
trades
- The ydata is the 10 day future returns defined into Buy, Short, Do Nothing based upon a defined range of returns.
- def get_indicatorsmatrix(prices_insample) returns the matrix to fed to the RTlearner
- def calc_futurereturns(prices_insample) calculates the future returns
- def generate_actions(prices_10dayreturn, deviation) returns the trade actions based upon deviation which is the range
- def use_RTlearner(traindata, testdata, actions, leaf_size) - loads the train data - xdata, actions - ydata into
the learner.  testdata queries the RTlearner to return the trade actions
- def createMLOrders(query_actions, filename, showlines=False) - processes the trade actions into a csvfile
(filename = 'MLorders.csv')
