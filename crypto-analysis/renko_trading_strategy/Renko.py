
#   author: David Gutsch
#   date:   09/26/2018



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


    ###################################
    #Constructor
    ###################################

    # purpose: this constructor takes a numpy array of Raw stock prices and test's and reports on them for testing,
    # IFF no dataStream variable is passed to the constructor then you are implicitly implying that you will be using
    #     the object for real time trading
    # signature: Renko(block_size: int, dataStream: numpyArray) 
    def __init__(self, blockSize, dataStream = None):
        self.BLOCK_SIZE = blockSize
        self.ATR = 0
        
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
    #signiture: getRawData() -> self.raw_data
    def getRawData(self):
        return self.raw_data
    
    
    #purpose: return the renko data list
    #signiture: getRenkoData() -> self.renko_data
    def getRenkoData(self):
        return self.renko_data

    #purpose: reset BLOCK_SIZE field
    # signiture: setBlockSize(size:int) -> updates self.BLOCK_SIZE
    def setBlockSize(self, size):
        self.BLOCK_SIZE = size

    
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

    #purpose: this function finds the average true range for the first ATR 
    # signature: findFirstATR(dataSet: nested list, widnowSize: int) -> ATR : float (also updates self.ATR, and sets self.ATR_WINDOW_SIZE for future findATR calls)
    # dataset: list where each inex is a list of the following values for the day: [High, Low, CLose]
    # windowSize: the size of the interval over which ATR is being calculated
    def findFirstATR(self, dataSet, windowSize):
        trueValueAccum = 0

        
        for i in range(windowSize):
            #                      ( high - low)                      abs(high - previous close)            abs(low - previous close)
            trueValueAccum += max(dataSet[i][0] - dataSet[i][1], abs(dataSet[i][0] - dataSet[i - 1][2]), abs(dataSet[i][1] - dataSet[i - 1][2]))


        ATR = trueValueAccum / windowSize
        self.ATR = ATR
        self.ATR_WINDOW_SIZE = windowSize
        

        return ATR
    
    #purpose: this function finds the average true range for every value after the first window range
    #signature:  findATR( prevClose: float, high: float, low: float) -> ATR : float (also updates self.ATR)
    def findATR(self, prevClose, high, low,):

        self.ATR = (self.ATR * (self.ATR_WINDOW_SIZE - 1) + max(high - low, abs(high - prevClose), abs(low - prevClsoe))) / self.ATR_WINDOW_SIZE


        return self.ATR
        

    #purpose: function that processes new data 
    #signiture: process_price_event(price: float) -> adds values to self.raw_data and self.renko_data
    def process_price_event(self, price):
        # base, if there is not any data yet, there is no difference, etc.
        i = len(self.raw_data)
        if i == 0:
            self.raw_data.append([price, 0, 0])
            return

        else:
            # find difference and renko_magnitude
            diff = price - self.raw_data[-1][0]
            renko_mag = (price - self.raw_data[-1][0]) / self.BLOCK_SIZE
        
            self.raw_data.append([price, diff , renko_mag])

            # find how many renko bricks there will be
            bricks = []
            if renko_mag > 0:
                bricks.extend([1] * int(math.floor(renko_mag)))
            else:
                bricks.extend([-1] * abs(int(math.ceil(renko_mag))))



            # if len > 0 add to renko_data otherwise there is nothing to do
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
                    



            # determine if there is a buy or sell action
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
                            self.buyAction()

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
                            self.sellAction()
                        
                    # no pattern
                    if not match:
                        self.renko_data.append([renko_bricks[i], None])
 

    # purpospe: this function may be implemented to purchase as it is called on a buy action
    # NOTE: must be integrated with trading API
    # signiture: buyAction() -> ???
    def buyAction(self):
        print("BUY")



    # purpospe: this function may be implemented to sell as it is called on a sell action
    # NOTE: must be integrated with trading API
    # signiture: buyAction() -> ???
    def sellAction(self):
        print("SELL")


        
        
                        

    # purpose: this function takes renko_data and builds a matplotlib graph
    # signature: plot_renko(fileName: string) -> graph
    def plot_renko(self, fileName):
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
        axes.set_ylim(minPrevNum - int(abs(minPrevNum * .75)), maxPrevNum + int(maxPrevNum * .75))

        
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
    
   
    

   # nyse_df = get_quandl_data("URC/NYSE_ADV")
   # dow_df = get_quandl_data("FRED/M1109BUSM293NNBR")
   # nse_df = get_quandl_data("NSE/IBULISL")




   # pulling historical data
    nse_df = get_quandl_data("NSE/IBULISL")

    clean_data = []

    #organizing clean_data into nested list of the following structure:
    # [high, low close]
    for day, row in nse_df.iterrows():
        clean_data.append([row['High'], row['Low'], row['Close']])
<<<<<<< HEAD
=======


        
        
    #creating the renko object passing it original block size
    r = Renko(10)
    # the window size for ATR calculation
    ATR_WINDOW = 10
    i = 0
    first_call = True
    
    # this is the simulation of real time data collection
    # each iteration represents the collection of 1 real-time data point
    for event in clean_data:
        # don't calculate ATR until you can fill the ATR_window
        if i > 10:
            if first_call == True:
                r.findFirstATR(clean_data, ATR_WINDOW)
            # after the first time it has been filled calculate atr based off of the previous value
            else: 
                r.findATR(clean_data, clean_data[i][2], clean_data[i][0], clean_data[i][1])

        # this function processes the price and adds it to self.raw_data and self.renko_data
        r.process_price_event(event[2])
        i += 1
        

    #this method plots the graph of renko bricks (green & red indicate direction. blue and orange indicate trade action
    r.plot_renko("nse_with_atr.png")
        

>>>>>>> a1c7e713062dafd8abab1519d1486bcd59cf20b0


        #just price
    price = [item[2] for item in clean_data]
    price_ar = np.array(price)    
            
    r = Renko(10)
        
    for event in clean_data:
        r.process_price_event(event[2])
