import csv
import matplotlib.pyplot as plt

class Stock:
    def __init__(self,name,filename):
        self.name = name
        self.date = []
        self.close = []

        self.load_data(filename)
        self.current_price = close[-1]
        

    def load_data(self,filename):
        """
        Gets all close and date data from csv downloaded from Yahoo Finance
        """
        with open (filename) as csvfile:

            reader = csv.reader(csvfile)
            
            for r_index, row in enumerate(reader):
                for c_index, col in enumerate(row):
                    if c_index == 0:
                        self.date.append(col)
                    elif c_index == 4:
                        if r_index != 0: self.close.append(float(col))
                        else: self.close.append(col)

    def crude_graph(self,data=None,start=0,end=None):
        """
        Displays crude graph of stock close data. Start is the start index, end is the end index, data is lists of SMAs.
        """
        def _color_gen():
            i = 0
            while True:
                if i % 3 == 0:
                    yield 'r-'
                    i += 1
                if i % 3 == 1:
                    yield 'g-'
                    i += 1
                if i % 3 == 2:
                    yield 'p-'
                    i += 1

        color = _color_gen()
        if not end:
            plt.plot(baba.date[start:],baba.close[start:],'b-', alpha=0.4)
            for lst in data:
                plt.plot(baba.date[start:],lst[start:],next(color), alpha=0.4)
        else:
            plt.plot(baba.date[start:end],baba.close[start:end],'b-', alpha=0.4)
            for lst in data:
                plt.plot(baba.date[start:end],lst[start:end],next(color), alpha=0.4)
        
        plt.show()
        plt.close()

    def __str__(self):
        return f"{self.name}"

if __name__ == "__main__":

    filename = "BABA.csv"
    baba = Stock("BABA",filename)

    # sma21 = baba.simple_moving_avg(21)
    # sma50 = baba.simple_moving_avg(50)
    
    # baba.crude_graph(data=(sma21,sma50),start=1000)

    