import numpy as np
import pandas as pd
import datetime as dt
import util as ut
import matplotlib.pyplot as plt
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

class indicators(object):
    def __init__(self, verbose=False):
        self.v = verbose

    def get_samples(self, syms=['IBM'], ):
        stdate = dt.datetime(2006, 1, 1)
        enddate = dt.datetime(2009, 12, 31)
        dates_insample = pd.date_range(stdate, enddate)
        prices_insample = ut.get_data(syms, dates_insample)
        prices_insample = prices_insample.drop("SPY", 1)
        # if self.v: print prices_insample
        # if self.v: print ms.daily_ret(prices_insample)


        stdate_out = dt.datetime(2010, 1, 1)
        enddate_out = dt.datetime(2010, 12, 31)
        dates_outsample = pd.date_range(stdate_out, enddate_out)
        prices_outsample = ut.get_data(syms, dates_outsample)
        prices_outsample = prices_outsample.drop('SPY', 1)
        # if self.v: print prices_outsample
        # if self.v:print ms.daily_ret(prices_outsample)

        return prices_insample, prices_outsample

    def convertSMA(self, prices, lookback):
        sma = pd.rolling_mean(prices, window=lookback, min_periods=lookback)
        # sma = prices.rolling(window=lookback, min_periods=lookback).mean()
        # print sma.columns.values[0]
        # sma = sma.rename(columns={sma.columns.values[0]:'SMA'})
        # print sma
        return sma

    def convertSMAratio(self, prices, lookback):
        sma = self.convertSMA(prices, lookback)
        ratio = sma / prices
        # print ratio
        # ratio = ratio.rename(columns={ratio.columns.values[0]: 'SMAratio'})
        # ratio.columns=['SMAratio']
        return ratio

    def convertBB(self, prices, lookback):
        sma = self.convertSMA(prices, lookback)
        rolling_std = pd.rolling_std(prices, window=lookback, min_periods=lookback)
        top_band = sma + (2 * rolling_std)
        bottom_band = sma - (2 * rolling_std)
        bbp = (prices - bottom_band) / (top_band - bottom_band)
        # bbp.columns=['BBP']
        return bbp

    def convertEMA(self, prices, lookback):
        # http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:moving_averages
        sma = self.convertSMA(prices, lookback)
        ema = pd.ewma(sma, span=lookback, adjust=True)
        # ema.columns = ['EMA']
        return ema

    def convertEMAratio(self, prices, lookback):
        sma = self.convertEMA(prices, lookback)
        ratio = sma / prices
        # ratio.columns = ['EMAratio']
        return ratio

    def convertBB_EMA(self, prices, lookback):
        ema = self.convertEMA(prices, lookback)
        rolling_std = pd.rolling_std(prices, window=lookback, min_periods=lookback)
        top_band = ema + (2 * rolling_std)
        bottom_band = ema - (2 * rolling_std)
        bbp = (prices - bottom_band) / (top_band - bottom_band)
        # bbp.columns = ['BBP_ema']
        return bbp

    def convertMomentum(self, prices, lookback):
        pricesshiftone = prices.copy().shift(lookback)
        # print prices
        # print pricesshiftone
        momentum = (prices / pricesshiftone) - 1
        # momentum.columns = ['momentum']
        return momentum


    def makeCharts(self, prices, indicator, indicatorname, startdate, enddate):
        mom = plt.title("IBM Price vs " + indicatorname)
        mom = plt.plot(prices[startdate:enddate])
        mom = plt.ylabel('Price', color='blue')
        mom = plt.xlabel('Date')
        mom = plt.twinx()
        mom.plot(indicator[startdate:enddate], label=indicatorname, color='g')
        mom.set_ylabel(indicatorname, color='green')
        for tl in mom.get_yticklabels():
            tl.set_color('g')
        plt.show()


def make_pricesinsampleChart():
    ax = prices_insample.plot(title="IBM", fontsize=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Prices")
    plt.savefig('./images/indicators.png')


if __name__ == "__main__":
    testindicator = indicators(verbose=True)

    prices_insample, prices_outsample = testindicator.get_samples()

    # ut.plot_data(prices_insample)
    lookback = 10
    startdate = 10
    enddate = 30

    sma = testindicator.convertSMA(prices_insample, lookback)
    smaratio = testindicator.convertSMAratio(prices_insample, lookback)
    bb = testindicator.convertBB(prices_insample, lookback)
    momentum = testindicator.convertMomentum(prices_insample, lookback)
    ema = testindicator.convertEMA(prices_insample, lookback)
    emaratio = ema / prices_insample

    print ("Hooah")

    # testindicator.makeCharts(prices_insample, momentum, "Momentum", startdate, enddate)
    # testindicator.makeCharts(prices_insample, bb, "Bollinger Band %", startdate, enddate)
    # testindicator.makeCharts(prices_insample, smaratio, "SMA/Price", startdate, enddate)
    # testindicator.makeCharts(prices_insample, ema/prices_insample, "EMA/Price", startdate, enddate)
    # testindicator.makeCharts(prices_insample, momentum, "Momentum", startdate, enddate)
    # testindicator.makeCharts(prices_insample, bb, "Bollinger Band %", startdate, enddate)

    # ax = plt.plot(prices_insample[startdate:enddate])
    # ax = plt.plot(sma[startdate:enddate], label='SMA', color='red')
    # ax = plt.ylabel('Price')
    # ax = plt.xlabel('Date')
    # ax = plt.title("Figure 1: IBM Analysis Price & Price")
    # plt.show()

    # smaratioplot = plt.plot(smaratio[startdate:enddate])
    # smaratioplot = plt.ylabel('SMA Ratio')
    # smaratioplot = plt.xlabel('Date')
    # smaratioplot = plt.title("SMA / Price & EMA / Price")
    # emaratioplot = plt.plot(emaratio[startdate:enddate])
    # emaratioplot = plt.ylabel('EMA Ratio')
    # emaratioplot = plt.xlabel('Date')
    # # emaratioplot = plt.title("EMA / Price")
    # plt.axhline(y=1, color='r', linestyle='-')
    # # plt.legend([smaratioplot, emaratioplot])
    # plt.show()

    # print prices_insample.ix[0]

    # print prices_insample.ix[0]
    # print prices_insample.ix[-1]
    # print prices_outsample.ix[0]
    # print prices_outsample.ix[-1]
    # print ("Return of stock in sample: {}".format(prices_insample.ix[-1] / prices_insample.ix[0]))
    # print ("Return of stock outsample: {}".format(prices_outsample.ix[-1] / prices_outsample.ix[0]))
    # ut.plot_data(prices_insample, "IBM", "Date", "Price")

    # make_pricesinsampleChart()
