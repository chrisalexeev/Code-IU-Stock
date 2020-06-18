from SimpleStock import Stock
from Study import MovingAverage


if __name__ == "__main__":
    baba = Stock("BABA", "BABA.csv")

    # add two moving average studies study
    baba.add_study(MovingAverage(20, type='simple'))
    baba.add_study(MovingAverage(20, type='exponential'))

    baba.plot()
