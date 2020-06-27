from SimpleStock import Stock
from Study import MovingAverage
from Study import MACD

if __name__ == "__main__":
    baba = Stock("BABA", "BABA.csv")

    # add two moving average studies study
    baba.add_study(MACD())

    baba.plot()
