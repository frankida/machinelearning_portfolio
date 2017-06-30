R"""MC2-P1: Market simulator."""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data


def compute_portvals(orders_file="./orders/orders.csv", start_val=1000000):
    # this is the function the autograder will call to test your code
    # TODO: Your code here
    v = False
    overleveraged = True
    orders = pd.read_csv(orders_file, parse_dates=True, na_values=['nan'])
    if v: print ("Orders: \n{}".format(orders))
    prices, symbols = get_prices(orders)
    if v: print ("Prices: \n{}".format(prices))
    trades = process_trades(orders, prices)
    if v: print ("Trades: \n{}".format(trades))
    while overleveraged:
        holdings = process_holdings(start_val, trades)
        if v: print ("Holdings: \n{}".format(holdings))
        values = prices * holdings  # values = prices * holdings
        if v: print ("Values: \n{}".format(values))
        portvals = values.sum(axis=1)
        if v: print ("Portfolio values: \n{}".format(portvals))
        sum_abs_values = get_sum_abs_values(values)
        leverage = sum_abs_values / portvals
        # print ("how made trades are over levered: {}".format(leverage[leverage > 3].shape[0]))
        overleveraged = leverage[leverage > 3].shape[0] > 0
        if overleveraged:
            # print
            # print ("Over leveraged days:")
            # print leverage[leverage > 3]
            # print leverage[leverage>3].index[0]
            # print ("bad trade day: {}" .format(trades.loc[leverage[leverage>3].index[0]]))
            trades.loc[leverage[leverage > 3].index[0]] = 0
            # print trades.loc[leverage[leverage > 3].index[0]]

    return portvals


def get_sum_abs_values(values):
    # print(values.ix[:, 0:(values.shape[1] - 1)])
    abs_values = values.ix[:, 0:(values.shape[1] - 1)]
    abs_values = abs_values.abs()
    # print type(abs_values)
    # print abs_values
    sum_abs_values = abs_values.sum(axis=1)
    return sum_abs_values


def get_prices(orders):
    symbols = orders['Symbol'].unique().tolist()
    start_date, end_date = get_dates(orders)
    dates = pd.date_range(start_date, end_date)
    prices = get_data(symbols, dates)
    prices = prices[symbols]  # remove SPY
    prices['Cash'] = pd.Series(np.ones(len(prices)), prices.index)
    return prices, symbols


def get_dates(orders):
    start_date = orders['Date'].iloc[0]
    end_date = orders['Date'].iloc[-1]
    return start_date, end_date


def process_trades(orders, prices):
    # make the trades dataframe
    trades = zero_out_dataframe(prices)

    for order in orders.iterrows():
        leverage = 3.0
        tradedate = order[1][0]
        # print tradedate

        # if ((tradedate != '2011-06-15') and (leverage<=3)):

        # print ("Date: {}, Apple price: {}, IBM price: {}, GOOG price: {}, XOM Price {}, CASH: {}" \
        #        .format(tradedate, prices.loc[tradedate][0], prices.loc[tradedate][1], prices.loc[tradedate][2], \
        #                prices.loc[tradedate][3], prices.loc[tradedate][4]))

        tradesymbol = order[1][1]
        tradeorder = order[1][2]
        tradeshares = order[1][3]
        # print ("Date: {}, Symbol: {}, Order: {}, Shares: {}". \
        #        format(tradedate, tradesymbol, tradeorder, tradeshares))

        if tradeorder == "BUY":
            trades[tradesymbol].loc[tradedate] = trades[tradesymbol].loc[tradedate] + tradeshares
            trades['Cash'].loc[tradedate] = trades['Cash'].loc[tradedate] \
                                            - tradeshares * prices[tradesymbol].loc[tradedate]

        else:
            trades[tradesymbol].loc[tradedate] = trades[tradesymbol].loc[tradedate] - tradeshares
            trades['Cash'].loc[tradedate] = trades['Cash'].loc[tradedate] + \
                                            tradeshares * prices[tradesymbol].loc[tradedate]
    # print trades
    return trades


def process_holdings(start_val, trades):
    # holdingsing processing
    holdings = zero_out_dataframe(trades)
    # first row
    holdings.iloc[0, -1] = start_val
    holdings.iloc[0] = holdings.iloc[0] + trades.iloc[0]
    # print holdings.iloc[0]
    # middle of processing
    # print("Shape of holding: {}".format(holdings.shape[0]))
    for row in range(holdings.shape[0] - 1):
        # print row+1
        # print holdings.iloc[row+1]
        holdings.iloc[row + 1] = holdings.iloc[row] + trades.iloc[row + 1]
        # print (holdings.iloc[row+1])
    # print holdings
    return holdings


def zero_out_dataframe(dataframe):
    empty = dataframe.copy()
    empty.ix[:, :] = 0
    return empty


def compute_portfolio_stats(port_val,
                            rfr, sf):
    # rfr risk free rate

    daily_returns = daily_ret(port_val)
    daily_returns = daily_returns[1:]

    cr = calculate_return(port_val[0], port_val[-1])
    adr = daily_returns.mean()
    sddr = daily_returns.std()
    sr = calc_sharpe_daily(daily_returns, rfr, sddr, sf)
    return cr, adr, sddr, sr


def calc_sharpe_daily(df, rfr, sddr, sf):
    daily = sf ** (.5)
    return ((df - rfr).mean()) / sddr * daily


def calculate_return(startvalue, endvalue):
    return (endvalue - startvalue) / startvalue


def daily_ret(df):
    daily_returns = df.copy
    daily_returns = (df / df.shift(1)) - 1
    daily_returns.ix[0] = 0
    return daily_returns


def process_analyze_orders(orderfilename, verbose=True):
    of = orderfilename
    sv = 100000
    rfr = 0
    sf = 252.0
    # Process orders
    portvals = compute_portvals(orders_file=of, start_val=sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]]  # just get the first column
    else:
        "warning, code did not return a DataFrame"
    orders = pd.read_csv(of, parse_dates=True, na_values=['nan'])
    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date, end_date = get_dates(orders)
    dates = pd.date_range(start_date, end_date)
    portvals_SPY = get_data(['$SPX'], dates, False)
    portvals_SPY = portvals_SPY.dropna()
    portvals_SPY = portvals_SPY['$SPX']
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = compute_portfolio_stats(portvals, rfr, sf)
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = compute_portfolio_stats(portvals_SPY, rfr, sf)
    # Compare portfolio against $SPX
    if (verbose):
        print "Date Range: {} to {}".format(start_date, end_date)
        print
        print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
        print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
        print
        print "Cumulative Return of Fund: {}".format(cum_ret)
        print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
        print
        print "Standard Deviation of Fund: {}".format(std_daily_ret)
        print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
        print
        print "Average Daily Return of Fund: {}".format(avg_daily_ret)
        print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
        print
        print "Final Portfolio Value: {}".format(portvals[-1])

    return portvals


def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    process_analyze_orders("orders.csv")

if __name__ == "__main__":
    test_code()
