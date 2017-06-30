from matplotlib.dates import strpdate2num

import RTLearner as rt
import marketsim as ms
import indicators as ind
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import BagLearner as bl
import rule_based as rb

warnings.simplefilter(action="ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)


def get_indicatorsmatrix(prices_insample):
    lookback = 10
    # sma = testindicator.convertSMA(prices_insample, lookback)
    smaratio = testindicator.convertSMAratio(prices_insample, lookback)
    bb = testindicator.convertBB(prices_insample, lookback)
    bbema = testindicator.convertBB_EMA(prices_insample, lookback)
    momentum = testindicator.convertMomentum(prices_insample, lookback)
    # ema = testindicator.convertEMA(prices_insample, lookback)
    emaratio = testindicator.convertEMAratio(prices_insample, lookback)

    allindicators = pd.merge(smaratio, bb, how='inner', left_index=True, right_index=True)
    # allindicators = pd.merge(allindicators, smaratio, how='inner', left_index=True, right_index=True)
    allindicators = pd.merge(allindicators, bbema, how='inner', left_index=True, right_index=True)
    allindicators = pd.merge(allindicators, momentum, how='inner', left_index=True, right_index=True)
    allindicators = pd.merge(allindicators, emaratio, how='inner', left_index=True, right_index=True)

    allindicators = allindicators.rename(columns={allindicators.columns.values[0]: 'smaratio',
                                                  allindicators.columns.values[1]: 'bbp',
                                                  allindicators.columns.values[2]: 'bbema',
                                                  allindicators.columns.values[2]: 'momentum',
                                                  allindicators.columns.values[3]: 'emaratio',
                                                  })
    allindicatior_matrix = allindicators.as_matrix()
    return allindicatior_matrix

def calc_futurereturns(prices_insample):
    prices_insample10day = prices_insample.copy().shift(-10)
    # print prices_insample
    # print prices_insample10day
    prices_10dayreturn = prices_insample10day / prices_insample
    return prices_10dayreturn

def generate_actions(prices_10dayreturn, deviation):
    prices_10dayreturn[(prices_10dayreturn >= (1 + deviation))] = 1.0
    prices_10dayreturn[(prices_10dayreturn <= (1 - deviation))] = -1.0
    # print prices_10dayreturn
    criteria = (prices_10dayreturn != 1.0) & (prices_10dayreturn != -1.0)  # weird exact syntax required
    prices_10dayreturn[criteria] = 0
    rules = prices_10dayreturn.as_matrix()
    return rules


def createMLOrders(query_actions, filename, showlines=False):
    Buy = ",IBM,BUY,500"
    Sell = ",IBM,SELL,500"
    Lastorder = 0
    # print ("Lastorder date: {}".format(rules.index[0]))
    Lastordercounter = 100.0

    ofile = open(filename, 'w')
    dayscounter = 0
    ofile.write("Date,Symbol,Order,Shares\n")
    for count, action in enumerate(query_actions):
        # print row[0]
        if ((action == 1.0) & (Lastordercounter > 10)):
            # print index.strftime('%Y-%m-%d')+Buy
            ofile.write(pd.to_datetime(pricesdates[count]).strftime('%Y-%m-%d') + Buy + '\n')
            Lastorder = 1.0
            Lastordercounter = 0
        elif ((action == -1) & (Lastordercounter > 10)):
            # print index.strftime('%Y-%m-%d')+Sell
            ofile.write(pd.to_datetime(pricesdates[count]).strftime('%Y-%m-%d') + Sell + '\n')
            Lastorder = -1.0
            Lastordercounter = 0
        elif ((Lastordercounter == 10) & (Lastorder == 1.0)):
            # print index.strftime('%Y-%m-%d') + Sell
            # print "exit"+Lastorder
            ofile.write(pd.to_datetime(pricesdates[count]).strftime('%Y-%m-%d') + Sell + '\n')
            Lastorder = 0.0
            Lastordercounter = 100
        elif ((Lastordercounter == 10) & (Lastorder == -1.0)):
            # print index.strftime('%Y-%m-%d') + Buy
            # print "exit"+Lastorder
            ofile.write(pd.to_datetime(pricesdates[count]).strftime('%Y-%m-%d') + Buy + '\n')
            Lastorder = 0.0
            Lastordercounter = 100
        else:
            Lastordercounter += 1
        dayscounter += 1
    ofile.close()


def use_baglearner(traindata, testdata, actions, leaf_size):
    learner = bl.BagLearner(learner=rt.RTLearner, kwargs={"leaf_size": leaf_size}, bags=10, boost=False, verbose=False)
    learner.addEvidence(traindata, actions)
    query_actions = learner.query(testdata)
    return query_actions


def use_RTlearner(traindata, testdata, actions, leaf_size):
    learner = rt.RTLearner(leaf_size=leaf_size)
    learner.verbose = False
    learner.addEvidence(traindata, actions)
    query_actions = learner.query(testdata)
    query_actions = query_actions.reshape(query_actions.shape[1])
    return query_actions


def makelines(query_actions):
    showlines = True
    Lastorder = 0
    Lastordercounter = 100.0

    fig = plt.figure()
    conv = np.vectorize(strpdate2num('%Y-%m-%d'))
    for count, action in enumerate(query_actions):
        dayscounter = conv(pd.to_datetime(pricesdates[count]).strftime('%Y-%m-%d'))
        if ((action == 1.0) & (Lastordercounter > 10)):
            Lastorder = 1.0
            Lastordercounter = 0
            if showlines: plt.axvline(x=dayscounter, color='g', linestyle='-')
        elif ((action == -1) & (Lastordercounter > 10)):
            Lastorder = -1.0
            Lastordercounter = 0
            if showlines: plt.axvline(x=dayscounter, color='r', linestyle='-')
        elif ((Lastordercounter == 10) & (Lastorder == 1.0)):
            Lastorder = 0.0
            Lastordercounter = 100
            if showlines: plt.axvline(x=dayscounter, color='black', linestyle='-')  # exit
        elif ((Lastordercounter == 10) & (Lastorder == -1.0)):
            Lastorder = 0.0
            Lastordercounter = 100
            if showlines: plt.axvline(x=dayscounter, color='black', linestyle='-')  # exit
        else:
            Lastordercounter += 1

if __name__ == "__main__":
    testindicator = ind.indicators(verbose=True)
    prices_insample, prices_outsample = testindicator.get_samples()

    sampletomodel = prices_insample

    allindicatior_matrix = get_indicatorsmatrix(sampletomodel)

    prices_10dayreturn = calc_futurereturns(sampletomodel)

    filename = 'MLorders.csv'
    range = .02
    actions = generate_actions(prices_10dayreturn, range)
    # for count, action in enumerate(actions):
    #     print "{} : {}".format(count, action)
    leaf_size = 5
    learner_type = "RT"  # change to "BL" for baglearner
    traindata = allindicatior_matrix
    testdata = get_indicatorsmatrix(sampletomodel)

    if learner_type == "RT":
        query_actions = use_RTlearner(traindata, testdata, actions, leaf_size)
        # for count, action in enumerate(query_actions):
        #     print "{} : {}".format(count, action)
    elif learner_type == "BL":
        query_actions = use_baglearner(traindata, testdata, actions, leaf_size)

    pricesdates = sampletomodel.index.values

    createMLOrders(query_actions, filename)

    print "ML_based Perfomance"
    portvals = ms.process_analyze_orders(filename, verbose=True)
    # print "**Portfolio values**"
    portvals_returns = portvals / portvals.ix[0]
    # print portvals_returns
    print

    print "Benchmark Perfomance"
    benchmark = ms.process_analyze_orders('IBM500in.csv', verbose=False)  # insample
    # benchmark = ms.process_analyze_orders('./orders/IBM500out.csv', verbose=False) #outsample

    benchmark_returns = benchmark / benchmark.ix[0]
    # print benchmark_returns

    rulebased = rb.getrulebased_returns(sampletomodel)
    # print rulebased


    # makelines(query_actions)
    # ax = portvals_returns.plot(title="ML vs Manual vs Benchmark", fontsize=12, color='green')
    # ax = benchmark_returns.plot(color='black')
    # ax = rulebased.plot(color='blue')
    # ax.set_xlabel("Date")
    # ax.set_ylabel("Prices")
    # plt.savefig('./images/MLbased.png')
