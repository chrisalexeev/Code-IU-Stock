from Stock import Stock
from Study import *
from Strategy import BuyAndHold
from Strategy import MovingAverageCrossover
from Strategy import MACDCrossover

if __name__ == "__main__":
    # globals
    stocks = ["SPY", "DIA", "WTI", "GLD", "SLV", "SCCO", "DD", "GE",
              "CAT", "BAC", "DFS", "F", "UAL", "CCL", "COST", "TGT",
              "EBAY", "CL", "HD", "M", "KSS", "NKE", "HBI", "XOM", "OXY",
              "BP", "DUK", "AEP", "XLU", "MO", "JNJ", "PFE", "AMT", "AVB",
              "EWT", "MSFT", "GOOG", "T", "CSCO", "CMCSA"]

    # average return buying and holding 2016-2020
    pls = []
    for stock in stocks:
        stock = Stock(stock, "stocks/"+stock+"2016.csv")
        strat = BuyAndHold(stock)
        strat.run()
        pls.append(strat.getPL())
    print("avg P/L: "+str(sum(pls)/len(pls))+"%")

    # average return macdcrossover 2016-2020
    pls = []
    for stock in stocks:
        stock = Stock(stock, "stocks/"+stock+"2016.csv")
        strat = MACDCrossover(stock)
        strat.run()
        pls.append(strat.getPL())
    print("avg P/L: "+str(sum(pls)/len(pls))+"%")

    # spy = Stock("SPY", "stocks/SPY2008.csv")
    # spy.add_study(MACD())
    # macd_strat = MACDCrossover(spy)
    # macd_strat.run()
    # print("P/L: "+str(macd_strat.getPL())+"%")
    # for i in range(len(macd_strat.data['activity'])):
    #     activity = macd_strat.data['activity'][i].split(',')
    #     print(macd_strat.data['activity'][i])

    # spy.addplot(macd_strat.data['balance'], lower=True, plot_type='bar')
    # spy.addplot(macd_strat.data['buys'], lower=False, plot_type='scatter', color='green')
    # spy.addplot(macd_strat.data['sells'], lower=False, plot_type='scatter', color='red')
    # spy.plot()
