
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

    # list of tuples containing input data (raw_price : float, raw_price / BLOCK_SIZE : float)
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
            self.renko_data = []
            #fill raw data field
            for price in np.nditer(dataStream, order='C'):
                self.renko_data.append((price, price / self.BLOCK_SIZE))


    
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
            
        except (OSError, IOError) as e:
            
            print('Downloading {} frpm Quandl'.format(quandl_id))
            df = quandl.get(quandl_id, returns = "pandas")
            df.to_pickle(cache_path)
            print('Cached {} at {}'.format(quandl_id, cache_path))
        
        os.chdir('../')
        return df



    # purpose: this function takes a dataframe and a block size and builds a matplotlib graph
    # signature: plot_renko(df: dataframe, brick_size: int) -> graph
    def plot_renko(self, data, brick_size):
        fig = plt.figure(1)
        fig.clf()
        axes = fig.gca()

    
 
        prev_num = 0
        bricks = []

        for delta in data:
        
            if delta > 0:
                #not a full block increment so round down
                delta = int(math.floor(delta))
                # add delta number of blocks to set
                bricks.extend([1]*delta)

            else:
                # not a full block so "round down", technically rounding up
                delta = int(math.ceil(delta))
                # add delta number of blocks to set
                bricks.extend([-1]*abs(delta))

        # vars to maintain plot size limits
        ind = 0
        minPrevNum = prev_num
        maxPrevNum = prev_num

        # build plot one block at a time and increment or update plot size vars
        for index, number in enumerate(bricks):
            if number == 1:
                facecolor='green'
            else:
                facecolor='red'

            prev_num += number
            
            renko = Rectangle(
                (index, prev_num * brick_size), 1, brick_size,
                facecolor=facecolor, alpha=0.5
            )

            ind = index

            if prev_num * brick_size < minPrevNum:
                minPrevNum = prev_num * brick_size
            if prev_num * brick_size > maxPrevNum:
                maxPrevNum = prev_num * brick_size
                        
            axes.add_patch(renko)

        # set plot size 
        axes.set_xlim(0, index + brick_size)
        axes.set_ylim(minPrevNum - 10, maxPrevNum + 10)
        
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
        

    dow_df['day_diff'] = dow_df['VALUE'] - dow_df['VALUE'].shift(1)
    dow_df.dropna(inplace=True)
    dow_df['bricks'] = dow_df.loc[:, ('day_diff',)] / BRICK_SIZE
        
    #        dow_df['bricks'] = dow_df['bricks']
    bricks = dow_df[dow_df['bricks'] != 0]['bricks'].tail(5).values

       

    print(bricks)

    default = Renko(2)
    renkoObject = Renko(2, bricks)
    
#        plot = plot_renko(bricks, BRICK_SIZE)
#        plot.savefig("dow_renko.png")
