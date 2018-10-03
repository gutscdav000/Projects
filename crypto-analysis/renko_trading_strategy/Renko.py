
#   author: David Gutsch
#   date:   09/26/2018

#class
# auxiliary funcions already written
# dataframe field
# historical buy / sell trading data
# real_time function for trading. uses function callback for specific api calls, also adds new data to existing dataframe



import pandas as pd
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import numpy as np
import os, quandl, pickle, math




class Renko:

    #----------------------------------
    #Fields
    #----------------------------------

    # integer value for size of renko blocks
    #BLOCK_SIZE 

    # nested list containing input data [raw_price : float, price_difference : float, block_magnitude : float]
    # raw_price = the actual price value
    # price_difference = this_price - last_price
    # block_magnitude = price_difference / BLOCK_SIZE
    #self.raw_data

    # list of tuples containing renko blocks (renko_block: 1 or -1, action None or "buy" or "sell")
    #self.renko_data

    ###################################
    #Constructor
    ###################################

    # purpose: this constructor takes a numpy array of Raw stock prices and test's and reports on them for testing,
    # IFF no dataStream variable is passed to the constructor then you are implicitly implying that you will be using
    #     the object for real time trading
    # signature: Renko(block_size: int, dataStream: numpyArray) 
    def __init__(self, blockSize, dataStream = None):
        self.BLOCK_SIZE = blockSize

        if dataStream is not None:

            # find price diff
            numpy_data = dataStream.tolist()
            price_diff = [ numpy_data[i] - numpy_data[i - 1] for i in range(len(numpy_data)) if i > 0]
            #print(price_diff)
            #print("len numpy_prices:", len(numpy_data), "len price_diff:", len(price_diff))
            
            self.raw_data = [[numpy_data[0], 0, 0]] # add the first elem since there is no price diff

            #fill raw data field
            for i in range(1, len(numpy_data)):
                self.raw_data.append([numpy_data[i], price_diff[i - 1] , price_diff[i - 1] / self.BLOCK_SIZE])

            #print("raw_data:\n",self.raw_data)

            # now organize renko data
            self.renko_data = []

            renko_bricks = []
            for lst in self.raw_data:
                renko_mag = lst[2]
                
                if renko_mag > 0:
                    #not a full block increment so round down
                    renko_mag = int(math.floor(renko_mag))
                    # add delta number of blocks to set
                    renko_bricks.extend([1]*renko_mag)
                    
                else:
                    # not a full block so "round down", technically rounding up
                    renko_mag = int(math.ceil(renko_mag))
                    # add delta number of blocks to set
                    renko_bricks.extend([-1]*abs(renko_mag)) 
                    



            rolling_window = []    
            # evaluate and build up renko_data
            for i in range(len(renko_bricks)):
                if i < 5:
                    rolling_window.append(renko_bricks[i])
                    self.renko_data.append([renko_bricks[i], None])
                    

                else:
                # pattern match
                # buy pop/append sell
                    match = False


                    # buy
                    if rolling_window == [-1, -1, -1, 1, 1]:
                        self.renko_data.append([renko_bricks[i], "buy"])
                        match = True

                    # remove first element & add next
                    if i + 1 < len(renko_bricks):
                        rolling_window.pop(0)
                        rolling_window.append(renko_bricks[i + 1])
                    
                    # sell
                    if rolling_window == [1, 1, -1, -1, -1]:
                        self.renko_data.append([renko_bricks[i], "sell"])
                        match = True
                        
                    # no pattern
                    if not match:
                        self.renko_data.append([renko_bricks[i], None])
        else:
            # initialize variables
            self.raw_data = [] 
            self.renko_data = []

                        
                




    #purpose: return the raw data list
    def getRawData(self):
        return self.raw_data

        
    #purpose: return the renko data list
    def getRenkoData(self):
        return self.renko_data

    
    # purpose: download and cache a Quandl dataseriews
    # signature: get_quandl_data(cuandl_id: ) -> df: panda dataframe
    def get_quandl_data(self, quandl_id):
        home = os.getcwd()
    
        # create directory if it doesn't already exist
        if 'quandl_cache' not in os.listdir(home):
            os.mkdir('quandl_cache')

        #change directory to quandl_cache
        path = os.path.join(home, 'quandl_cache/')
        os.chdir(path)

        # download & cache
        cache_path = 'quandl_cache/{}.pkl'.format(quandl_id).replace('/','-')
        try:
            #serialize python object structure
            file = open(cache_path, 'rb')
            df = pickle.load(file)
            print('Loaded {} from cache'.format(quandl_id))
            file.close()
            
        except (OSError, IOError) as e:
            
            print('Downloading {} frpm Quandl'.format(quandl_id))
            df = quandl.get(quandl_id, returns = "pandas")
            df.to_pickle(cache_path)
            print('Cached {} at {}'.format(quandl_id, cache_path))
        
        os.chdir('../')
        return df

    #purpose: this function finds the average true range for a period given a Current High, Current Low, Previous Close data set
    # signature: findATR(dataSet: nested list, widnowSize: int, setToBlockSize: bool) -> ATR block size value
    # dataset: list where each inex is a list of the following values for the day: [High, Low, CLose]
    # windowStart, windowEnd: the range of the dataset that you want to find the ATR of 
    # setToBlockSize when true resets self.BLOCK_SIZE to the return value of ATR
    def findATR(self, dataSet, windowStart, windowEnd, setToBlockSize = False):
        trueValueAccum = 0
        
        for i in range(windowStart, windowEnd):
            #                      ( high - low)                      abs(high - previous close)            abs(low - previous close)
            trueValueAccum += max(dataSet[i][0] - dataSet[i][1], abs(dataSet[i][0] - dataSet[i - 1][2]), abs(dataSet[i][1] - dataSet[i - 1][2]))

        
        ATR = trueValueAccum / (windowEnd - windowStart)
        
        if setToBlockSize == True:
            self.BLOCK_SIZE = int(ATR)

        return ATR

    #purpose: function that processes new data
    def process_price_event(self, price):
        i = len(self.raw_data)
        if i == 0:
            self.raw_data.append([price, 0, 0])
            return

        else:

            diff = price - self.raw_data[-1][0]
            renko_mag = (price - self.raw_data[-1][0]) / self.BLOCK_SIZE
        
            self.raw_data.append([price, diff , renko_mag])

            
            bricks = []
            if renko_mag > 0:
                bricks.extend([1] * int(math.floor(renko_mag)))
            else:
                bricks.extend([-1] * abs(int(math.ceil(renko_mag))))



            # if len > 0 add to renko_data otherwise don't
            if len(bricks) == 0:
                return


            prevLen = len(self.renko_data)
            self.renko_data = []

            renko_bricks = []
            for lst in self.raw_data:
                renko_mag = lst[2]
                
                if renko_mag > 0:
                    #not a full block increment so round down
                    renko_mag = int(math.floor(renko_mag))
                    # add delta number of blocks to set
                    renko_bricks.extend([1]*renko_mag)
                    
                else:
                    # not a full block so "round down", technically rounding up
                    renko_mag = int(math.ceil(renko_mag))
                    # add delta number of blocks to set
                    renko_bricks.extend([-1]*abs(renko_mag)) 
                    



            rolling_window = []    
            # evaluate and build up renko_data
            for i in range(len(renko_bricks)):
                if i < 5:
                    rolling_window.append(renko_bricks[i])
                    self.renko_data.append([renko_bricks[i], None])
                    

                else:
                # pattern match
                # buy pop/append sell
                    match = False


                    # buy
                    if rolling_window == [-1, -1, -1, 1, 1]:
                        self.renko_data.append([renko_bricks[i], "buy"])
                        match = True
                        ############
                        if len(self.renko_data) > prevLen:
                            ###### buy!!!
                            print("buy")

                    # remove first element & add next
                    if i + 1 < len(renko_bricks):
                        rolling_window.pop(0)
                        rolling_window.append(renko_bricks[i + 1])
                    
                    # sell
                    if rolling_window == [1, 1, -1, -1, -1]:
                        self.renko_data.append([renko_bricks[i], "sell"])
                        match = True
                        ############
                        if len(self.renko_data) > prevLen:
                               ####### sell!!!
                               print("sell")
                        
                    # no pattern
                    if not match:
                        self.renko_data.append([renko_bricks[i], None])
 

    # purpospe: this function may be implemented to purchase as it is called on a buy action
    def buyAction(self):
        print("*" * 100)
        print("BUY")
        print("*" * 100)


    # purpospe: this function may be implemented to sell as it is called on a sell action
    def sellAction(self):
        print("*" * 100)
        print("SELL")
        print("*" * 100)

        
        
                        

    # purpose: this function takes a dataframe and a block size and builds a matplotlib graph
    # signature: plot_renko(df: dataframe, brick_size: int) -> graph
    def plot_renko(self, fileName ):
        fig = plt.figure(1)
        fig.clf()
        axes = fig.gca()

    
 
        prev_num = 0
        bricks = []


        # vars to maintain plot size limits
        ind = 0
        minPrevNum = prev_num
        maxPrevNum = prev_num

        # build plot one block at a time and increment or update plot size vars
        actionIndicator = -1
        #for index, lst in enumerate(self.renko_data):
        for i in range(len(self.renko_data)):
            
            number = self.renko_data[i][0]
            action = self.renko_data[i][1]

            # set block color
            # color for buy and sell
            if action is not None:
                if action == "sell":
                    facecolor = "orange"
                else:
                    facecolor = "blue"
                
            # colors for no action
            elif number == 1:
                facecolor='green'
            else:
                facecolor='red'
            
            prev_num += number
            
            renko = Rectangle(
                (i, prev_num * self.BLOCK_SIZE), 1, self.BLOCK_SIZE,
                facecolor=facecolor, alpha=0.5
            )

            ind = i

            if prev_num * self.BLOCK_SIZE < minPrevNum:
                minPrevNum = prev_num * self.BLOCK_SIZE
            if prev_num * self.BLOCK_SIZE > maxPrevNum:
                maxPrevNum = prev_num * self.BLOCK_SIZE
                        
            axes.add_patch(renko)

        # set plot size 
        axes.set_xlim(0, ind + self.BLOCK_SIZE)
        axes.set_ylim(minPrevNum - int(minPrevNum * .5), maxPrevNum + int(maxPrevNum * .5))

        
        plt.savefig(fileName)
        return plt

    


    






if __name__ == "__main__":


    #  just defining this down here to grab input data to feed to objects
    
    def get_quandl_data(quandl_id):
        home = os.getcwd()
    
        # create directory if it doesn't already exist
        if 'quandl_cache' not in os.listdir(home):
            os.mkdir('quandl_cache')

        #change directory to quandl_cache
        path = os.path.join(home, 'quandl_cache/')
        os.chdir(path)

        # download & cache
        cache_path = 'quandl_cache/{}.pkl'.format(quandl_id).replace('/','-')
        try:
            #serialize python object structure
            file = open(cache_path, 'rb')
            df = pickle.load(file)
            print('Loaded {} from cache'.format(quandl_id))
            
        except (OSError, IOError) as e:
            
            print('Downloading {} frpm Quandl'.format(quandl_id))
            df = quandl.get(quandl_id, returns = "pandas")
            df.to_pickle(cache_path)
            print('Cached {} at {}'.format(quandl_id, cache_path))
                
        os.chdir('../')
        return df




    # Chart building resources:
    # https://avilpage.com/2018/01/how-to-plot-renko-charts-with-python.html
    
    # notes on data streams:
    #   "URC/NYSE_ADV" : gets NYSE: number of stocks with prices advaancing data from Unicorn research corporation
    #   "FRED/M1109BUSM293NNBR" : gets DOW JOnes industrial
    

    BRICK_SIZE = 2
    

    nyse_df = get_quandl_data("URC/NYSE_ADV")
    dow_df = get_quandl_data("FRED/M1109BUSM293NNBR")
    nse_df = get_quandl_data("NSE/IBULISL")

    nse_df = get_quandl_data("NSE/IBULISL")
    clean_data = []
    # [high, low close]
    for index, row in nse_df.iterrows():
        clean_data.append([row['High'], row['Low'], row['Close']])
        
        r = Renko(10)
        
        for event in clean_data:
            r.process_price_event(event[2])
            

            print("*" * 100)
        print(r.getRenkoData())
        



