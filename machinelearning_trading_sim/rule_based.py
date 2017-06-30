import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import strpdate2num

import indicators as ind
import marketsim as ms
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

def setShort_Long_Sell(indicator, shortlongcondition, sellcondition):
    rules = indicator.copy()
    rules[rules >= 1 + shortlongcondition] = "BUY"
    rules[rules <= 1 - shortlongcondition] = "SHORT"
    return rules

def createOrders(rules, filename, showtradelines=False):

    Buy = ",IBM,BUY,500"
    Sell = ",IBM,SELL,500"
    Lastorder = "NOTHING"
    # print ("Lastorder date: {}".format(rules.index[0]))
    Lastordercounter = 100

    ofile = open(filename, 'w')
    dayscounter = 0
    ofile.write("Date,Symbol,Order,Shares\n")
    for index, row in rules.iterrows():
        # print row[0]
        if ((row[0] == "BUY") & (Lastordercounter > 10)):
            # print index.strftime('%Y-%m-%d')+Buy
            ofile.write(index.strftime('%Y-%m-%d') + Buy + '\n')
            Lastorder = "BUY"
            Lastordercounter = 0
            if showtradelines: plt.axvline(x=dayscounter, color='g', linestyle='-')
        elif ((row[0] == "SHORT") & (Lastordercounter > 10)):
            # print index.strftime('%Y-%m-%d')+Sell
            ofile.write(index.strftime('%Y-%m-%d') + Sell + '\n')
            Lastorder = "SHORT"
            Lastordercounter = 0
            if showtradelines: plt.axvline(x=dayscounter, color='r', linestyle='-')
        elif ((Lastordercounter == 10) & (Lastorder == "BUY")):
            # print index.strftime('%Y-%m-%d') + Sell
            # print "exit"+Lastorder
            ofile.write(index.strftime('%Y-%m-%d') + Sell + '\n')
            Lastorder = "NOTHING"
            Lastordercounter = 100
            if showtradelines: plt.axvline(x=dayscounter, color='black', linestyle='-')  # exit
        elif ((Lastordercounter == 10) & (Lastorder == "SHORT")):
            # print index.strftime('%Y-%m-%d') + Buy
            # print "exit"+Lastorder
            ofile.write(index.strftime('%Y-%m-%d') + Buy + '\n')
            Lastorder = "NOTHING"
            Lastordercounter = 100
            if showtradelines: plt.axvline(x=dayscounter, color='black', linestyle='-')  # exit
        else:
            Lastordercounter += 1
        dayscounter += 1
    ofile.close()


def getrulebased_returns(prices_insample, showtradelines=False):
    testindicator = ind.indicators(verbose=True)

    # global portvals_returns
    lookback = 10
    filename = 'neworders.csv'
    sma = testindicator.convertSMA(prices_insample, lookback)
    smaratio = testindicator.convertSMAratio(prices_insample, lookback)
    bb = testindicator.convertBB(prices_insample, lookback)
    momentum = testindicator.convertMomentum(prices_insample, lookback)
    ema = testindicator.convertEMA(prices_insample, lookback)
    emaratio = testindicator.convertEMAratio(prices_insample, lookback)
    # rules = setShort_Long_Sell(emaratio, .035, .0009) #139490
    # rules = setShort_Long_Sell(emaratio, .035, .0009) #139490
    rules = setShort_Long_Sell(emaratio, .023, .0009)  # 126765.0
    # rules = setShort_Long_Sell(emaratio, .04, .0009) #122555
    # rules = setShort_Long_Sell(emaratio, .04, .001) #117880
    # rules = setShort_Long_Sell(smaratio, .05, .001) # 78350.0
    createOrders(rules, filename, showtradelines)

    # comment out to turn off ploting
    # makelines(rules)

    portvals = ms.process_analyze_orders(filename, verbose=True)
    # print "**Portfolio values**"
    portvals_returns = portvals / portvals.ix[0]
    return portvals_returns


def makelines(rules, showtradelines=True):
    Lastorder = "NOTHING"
    Lastordercounter = 100

    dayscounter = 0
    fig = plt.figure()
    conv = np.vectorize(strpdate2num('%Y-%m-%d'))
    for index, row in rules.iterrows():
        dayscounter = conv(index.strftime('%Y-%m-%d'))
        if ((row[0] == "BUY") & (Lastordercounter > 10)):
            Lastorder = "BUY"
            Lastordercounter = 0
            if showtradelines: plt.axvline(x=dayscounter, color='g', linestyle='-')
        elif ((row[0] == "SHORT") & (Lastordercounter > 10)):
            Lastorder = "SHORT"
            Lastordercounter = 0
            if showtradelines: plt.axvline(x=dayscounter, color='r', linestyle='-')
        elif ((Lastordercounter == 10) & (Lastorder == "BUY")):
            Lastorder = "NOTHING"
            Lastordercounter = 100
            if showtradelines: plt.axvline(x=dayscounter, color='black', linestyle='-')  # exit
        elif ((Lastordercounter == 10) & (Lastorder == "SHORT")):
            Lastorder = "NOTHING"
            Lastordercounter = 100
            if showtradelines: plt.axvline(x=dayscounter, color='black', linestyle='-')  # exit
        else:
            Lastordercounter += 1
        dayscounter += 1

if __name__ == "__main__":
    testindicator = ind.indicators(verbose=True)
    prices_insample, prices_outsample = testindicator.get_samples()
    portvals_returns = getrulebased_returns(prices_insample, showtradelines=False)
    # print portvals_returns

    # print "**Benchmark**"
    benchmark = ms.process_analyze_orders('IBM500in.csv', verbose=False)
    benchmark_returns = benchmark / benchmark.ix[0]
    # print benchmark_returns[dt(2009, 12, 31)]
    # print benchmark_returns



    # ax = portvals_returns.plot(title="Manual vs Benchmark", fontsize=12, color='blue')
    # ax = benchmark_returns.plot(color='black')
    # ax.set_xlabel("Date")
    # ax.set_ylabel("Prices")
    # plt.savefig('./images/Manualrule.png')
