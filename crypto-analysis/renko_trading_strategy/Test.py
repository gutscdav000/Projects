#  author: David Gutsch
#  date: 09/28/2018

import unittest, os, quandl, pickle, math
from Renko import Renko
import numpy as np


class TestRenko(unittest.TestCase):

    
    # assertion test functions:
    # self.assertEqual(), self.assertTrue(), self.assertFalse(), self.assertRaises(Error), assertNotEqual, assertIs(a, b)
    #assertIsNot(a,b) assertIsNone(), assertIsNotNone(), asertIn(a,b), assertNotInt(), assertIsInstance(), assertNotIsInstance()
    #
    # assert something.name is not None or assert func(10) == 42



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

    

    
    ########################
    # constructor / datastream tests
    ########################


    # small dow test
    def test_constructor_small_dow(self):


        dow_df = self.get_quandl_data("FRED/M1109BUSM293NNBR")

        # organize dataset
        dow_ds = dow_df['VALUE'].tail(5).values.tolist()
        price_difference = [dow_ds[i] - dow_ds[i - 1] for i in range(len(dow_ds)) if i > 0]
        

        BLOCK_SIZE = 2

        r1 = Renko(BLOCK_SIZE, dow_df['VALUE'].tail(5).values)
        
        # find RAW_DATA
        # fill list of [price, price difference, renko blocks]
        raw_data = [[dow_ds[0], 0, 0]]
        for i in range(1, len(dow_ds)):
            raw_data.append([dow_ds[i], price_difference[i - 1], price_difference[i - 1] / BLOCK_SIZE]) 
        

        # tests
        self.assertEqual( len(r1.getRawData()) , len(raw_data))
        self.assertTrue( r1.getRawData() == raw_data)

        renko_blocks = []
        for item in raw_data:
            if item[2] > 0:
                renko_blocks.extend([1] * int(math.floor(item[2])))
            else:
                renko_blocks.extend([-1] * abs(int(math.ceil(item[2]))))

                    
        renko_data = []
        rolling_window = []        
        # find up renko_data
        # [block direction, buy/sell/none]
        for i in range(len(renko_blocks)):
            if i < 5:
                rolling_window.append(renko_blocks[i])
                renko_data.append([renko_blocks[i], None])
                    

            else:
                match = False

                # buy
                if rolling_window == [-1, -1, -1, 1, 1]:
                    renko_data.append([renko_blocks[i], "buy"])
                    match = True

                # remove update rolling window
                if i + 1 < len(renko_blocks):
                    rolling_window.pop(0)
                    rolling_window.append(renko_blocks[i + 1])
                    
                # sell
                if rolling_window == [1, 1, -1, -1, -1]:
                    renko_data.append([renko_blocks[i], "sell"])
                    match = True
                    
                # no pattern
                if not match:
                    renko_data.append([renko_blocks[i], None])

                    
        self.assertEqual(len(renko_data), len(r1.getRenkoData()))
        self.assertEqual(renko_data, r1.getRenkoData())
        
        

    # small nyse test
    def test_constructor_small_nyse(self):
        
        nyse_df = self.get_quandl_data("URC/NYSE_ADV")

        
         # organize dataset
        nyse_ds = nyse_df['Numbers of Stocks'].tail(5).values.tolist()
        price_difference = [nyse_ds[i] - nyse_ds[i - 1] for i in range(len(nyse_ds)) if i > 0]
        

        BLOCK_SIZE = 50

        r1 = Renko(BLOCK_SIZE, nyse_df['Numbers of Stocks'].tail(5).values)
        
        # find RAW_DATA
        # fill list of [price, price difference, renko blocks]
        raw_data = [[nyse_ds[0], 0, 0]]
        for i in range(1, len(nyse_ds)):
            raw_data.append([nyse_ds[i], price_difference[i - 1], price_difference[i - 1] / BLOCK_SIZE]) 
        

        # tests

        self.assertEqual( len(r1.getRawData()) , len(raw_data))
        self.assertTrue( r1.getRawData() == raw_data)

        renko_blocks = []
        for item in raw_data:
            if item[2] > 0:
                renko_blocks.extend([1] * int(math.floor(item[2])))
            else:
                renko_blocks.extend([-1] * abs(int(math.ceil(item[2]))))

                    
        renko_data = []
        rolling_window = []        
        # find up renko_data
        # [block direction, buy/sell/none]
        for i in range(len(renko_blocks)):
            if i < 5:
                rolling_window.append(renko_blocks[i])
                renko_data.append([renko_blocks[i], None])
                    

            else:
                match = False

                # buy
                if rolling_window == [-1, -1, -1, 1, 1]:
                    renko_data.append([renko_blocks[i], "buy"])
                    match = True

                # remove update rolling window
                if i + 1 < len(renko_blocks):
                    rolling_window.pop(0)
                    rolling_window.append(renko_blocks[i + 1])
                    
                # sell
                if rolling_window == [1, 1, -1, -1, -1]:
                    renko_data.append([renko_blocks[i], "sell"])
                    match = True
                    
                # no pattern
                if not match:
                    renko_data.append([renko_blocks[i], None])


        self.assertEqual(len(renko_data), len(r1.getRenkoData()))
        self.assertEqual(renko_data, r1.getRenkoData())
    




    # medium dow test
    def test_constructor_medium_dow(self):


        dow_df = self.get_quandl_data("FRED/M1109BUSM293NNBR")

        # organize dataset
        dow_ds = dow_df['VALUE'].tail(75).values.tolist()
        price_difference = [dow_ds[i] - dow_ds[i - 1] for i in range(len(dow_ds)) if i > 0]
        

        BLOCK_SIZE = 2

        r1 = Renko(BLOCK_SIZE, dow_df['VALUE'].tail(75).values)
        
        # find RAW_DATA
        # fill list of [price, price difference, renko blocks]
        raw_data = [[dow_ds[0], 0, 0]]
        for i in range(1, len(dow_ds)):
            raw_data.append([dow_ds[i], price_difference[i - 1], price_difference[i - 1] / BLOCK_SIZE]) 
        

        # tests
        self.assertEqual( len(r1.getRawData()) , len(raw_data))
        self.assertTrue( r1.getRawData() == raw_data)

        renko_blocks = []
        for item in raw_data:
            if item[2] > 0:
                renko_blocks.extend([1] * int(math.floor(item[2])))
            else:
                renko_blocks.extend([-1] * abs(int(math.ceil(item[2]))))

                    
        renko_data = []
        rolling_window = []        
        # find up renko_data
        # [block direction, buy/sell/none]
        for i in range(len(renko_blocks)):
            if i < 5:
                rolling_window.append(renko_blocks[i])
                renko_data.append([renko_blocks[i], None])
                    

            else:
                match = False

                # buy
                if rolling_window == [-1, -1, -1, 1, 1]:
                    renko_data.append([renko_blocks[i], "buy"])
                    match = True

                # remove update rolling window
                if i + 1 < len(renko_blocks):
                    rolling_window.pop(0)
                    rolling_window.append(renko_blocks[i + 1])
                    
                # sell
                if rolling_window == [1, 1, -1, -1, -1]:
                    renko_data.append([renko_blocks[i], "sell"])
                    match = True
                    
                # no pattern
                if not match:
                    renko_data.append([renko_blocks[i], None])

                    
        self.assertEqual(len(renko_data), len(r1.getRenkoData()))
        self.assertEqual(renko_data, r1.getRenkoData())
    
        



    # medium nyse test
    def test_constructor_medium_nyse(self):
        
        nyse_df = self.get_quandl_data("URC/NYSE_ADV")

        
         # organize dataset
        nyse_ds = nyse_df['Numbers of Stocks'].tail(50).values.tolist()
        price_difference = [nyse_ds[i] - nyse_ds[i - 1] for i in range(len(nyse_ds)) if i > 0]
        

        BLOCK_SIZE = 50

        r1 = Renko(BLOCK_SIZE, nyse_df['Numbers of Stocks'].tail(50).values)
        
        # find RAW_DATA
        # fill list of [price, price difference, renko blocks]
        raw_data = [[nyse_ds[0], 0, 0]]
        for i in range(1, len(nyse_ds)):
            raw_data.append([nyse_ds[i], price_difference[i - 1], price_difference[i - 1] / BLOCK_SIZE]) 
        

        # tests

        self.assertEqual( len(r1.getRawData()) , len(raw_data))
        self.assertTrue( r1.getRawData() == raw_data)

        renko_blocks = []
        for item in raw_data:
            if item[2] > 0:
                renko_blocks.extend([1] * int(math.floor(item[2])))
            else:
                renko_blocks.extend([-1] * abs(int(math.ceil(item[2]))))

                    
        renko_data = []
        rolling_window = []        
        # find up renko_data
        # [block direction, buy/sell/none]
        for i in range(len(renko_blocks)):
            if i < 5:
                rolling_window.append(renko_blocks[i])
                renko_data.append([renko_blocks[i], None])
                    

            else:
                match = False

                # buy
                if rolling_window == [-1, -1, -1, 1, 1]:
                    renko_data.append([renko_blocks[i], "buy"])
                    match = True

                # remove update rolling window
                if i + 1 < len(renko_blocks):
                    rolling_window.pop(0)
                    rolling_window.append(renko_blocks[i + 1])
                    
                # sell
                if rolling_window == [1, 1, -1, -1, -1]:
                    renko_data.append([renko_blocks[i], "sell"])
                    match = True
                    
                # no pattern
                if not match:
                    renko_data.append([renko_blocks[i], None])


        self.assertEqual(len(renko_data), len(r1.getRenkoData()))
        self.assertEqual(renko_data, r1.getRenkoData())
        
        

    # large dow test
    def test_constructor_large_dow(self):


        dow_df = self.get_quandl_data("FRED/M1109BUSM293NNBR")

        # organize dataset
        dow_ds = dow_df['VALUE'].values.tolist()
        price_difference = [dow_ds[i] - dow_ds[i - 1] for i in range(len(dow_ds)) if i > 0]
        

        BLOCK_SIZE = 2

        r1 = Renko(BLOCK_SIZE, dow_df['VALUE'].values)
        
        # find RAW_DATA
        # fill list of [price, price difference, renko blocks]
        raw_data = [[dow_ds[0], 0, 0]]
        for i in range(1, len(dow_ds)):
            raw_data.append([dow_ds[i], price_difference[i - 1], price_difference[i - 1] / BLOCK_SIZE]) 
        

        # tests
        self.assertEqual( len(r1.getRawData()) , len(raw_data))
        self.assertTrue( r1.getRawData() == raw_data)

        renko_blocks = []
        for item in raw_data:
            if item[2] > 0:
                renko_blocks.extend([1] * int(math.floor(item[2])))
            else:
                renko_blocks.extend([-1] * abs(int(math.ceil(item[2]))))

                    
        renko_data = []
        rolling_window = []        
        # find up renko_data
        # [block direction, buy/sell/none]
        for i in range(len(renko_blocks)):
            if i < 5:
                rolling_window.append(renko_blocks[i])
                renko_data.append([renko_blocks[i], None])
                    

            else:
                match = False

                # buy
                if rolling_window == [-1, -1, -1, 1, 1]:
                    renko_data.append([renko_blocks[i], "buy"])
                    match = True

                # remove update rolling window
                if i + 1 < len(renko_blocks):
                    rolling_window.pop(0)
                    rolling_window.append(renko_blocks[i + 1])
                    
                # sell
                if rolling_window == [1, 1, -1, -1, -1]:
                    renko_data.append([renko_blocks[i], "sell"])
                    match = True
                    
                # no pattern
                if not match:
                    renko_data.append([renko_blocks[i], None])

                    
        self.assertEqual(len(renko_data), len(r1.getRenkoData()))
        self.assertEqual(renko_data, r1.getRenkoData())
    
    

    
    # large nyse test
    def test_constructor_large_nyse(self):
        
        nyse_df = self.get_quandl_data("URC/NYSE_ADV")

        
         # organize dataset
        nyse_ds = nyse_df['Numbers of Stocks'].tail(750).values.tolist()
        price_difference = [nyse_ds[i] - nyse_ds[i - 1] for i in range(len(nyse_ds)) if i > 0]
        

        BLOCK_SIZE = 50

        r1 = Renko(BLOCK_SIZE, nyse_df['Numbers of Stocks'].tail(750).values)
        
        # find RAW_DATA
        # fill list of [price, price difference, renko blocks]
        raw_data = [[nyse_ds[0], 0, 0]]
        for i in range(1, len(nyse_ds)):
            raw_data.append([nyse_ds[i], price_difference[i - 1], price_difference[i - 1] / BLOCK_SIZE]) 
        

        # tests

        self.assertEqual( len(r1.getRawData()) , len(raw_data))
        self.assertTrue( r1.getRawData() == raw_data)

        renko_blocks = []
        for item in raw_data:
            if item[2] > 0:
                renko_blocks.extend([1] * int(math.floor(item[2])))
            else:
                renko_blocks.extend([-1] * abs(int(math.ceil(item[2]))))

                    
        renko_data = []
        rolling_window = []        
        # find up renko_data
        # [block direction, buy/sell/none]
        for i in range(len(renko_blocks)):
            if i < 5:
                rolling_window.append(renko_blocks[i])
                renko_data.append([renko_blocks[i], None])
                    

            else:
                match = False

                # buy
                if rolling_window == [-1, -1, -1, 1, 1]:
                    renko_data.append([renko_blocks[i], "buy"])
                    match = True

                # remove update rolling window
                if i + 1 < len(renko_blocks):
                    rolling_window.pop(0)
                    rolling_window.append(renko_blocks[i + 1])
                    
                # sell
                if rolling_window == [1, 1, -1, -1, -1]:
                    renko_data.append([renko_blocks[i], "sell"])
                    match = True
                    
                # no pattern
                if not match:
                    renko_data.append([renko_blocks[i], None])


        self.assertEqual(len(renko_data), len(r1.getRenkoData()))
        self.assertEqual(renko_data, r1.getRenkoData())



    # immense nyse test with entire data set
    def test_constructor_immense_nyse(self):
        
        nyse_df = self.get_quandl_data("URC/NYSE_ADV")

        
         # organize dataset
        nyse_ds = nyse_df['Numbers of Stocks'].values.tolist()
        price_difference = [nyse_ds[i] - nyse_ds[i - 1] for i in range(len(nyse_ds)) if i > 0]
        

        BLOCK_SIZE = 50

        r1 = Renko(BLOCK_SIZE, nyse_df['Numbers of Stocks'].values)
        
        # find RAW_DATA
        # fill list of [price, price difference, renko blocks]
        raw_data = [[nyse_ds[0], 0, 0]]
        for i in range(1, len(nyse_ds)):
            raw_data.append([nyse_ds[i], price_difference[i - 1], price_difference[i - 1] / BLOCK_SIZE]) 
        

        # tests

        self.assertEqual( len(r1.getRawData()) , len(raw_data))
        self.assertTrue( r1.getRawData() == raw_data)

        renko_blocks = []
        for item in raw_data:
            if item[2] > 0:
                renko_blocks.extend([1] * int(math.floor(item[2])))
            else:
                renko_blocks.extend([-1] * abs(int(math.ceil(item[2]))))

                    
        renko_data = []
        rolling_window = []        
        # find up renko_data
        # [block direction, buy/sell/none]
        for i in range(len(renko_blocks)):
            if i < 5:
                rolling_window.append(renko_blocks[i])
                renko_data.append([renko_blocks[i], None])
                    

            else:
                match = False

                # buy
                if rolling_window == [-1, -1, -1, 1, 1]:
                    renko_data.append([renko_blocks[i], "buy"])
                    match = True

                # remove update rolling window
                if i + 1 < len(renko_blocks):
                    rolling_window.pop(0)
                    rolling_window.append(renko_blocks[i + 1])
                    
                # sell
                if rolling_window == [1, 1, -1, -1, -1]:
                    renko_data.append([renko_blocks[i], "sell"])
                    match = True
                    
                # no pattern
                if not match:
                    renko_data.append([renko_blocks[i], None])


        self.assertEqual(len(renko_data), len(r1.getRenkoData()))
        self.assertEqual(renko_data, r1.getRenkoData())





    def test_process_price_event(self):
        
        nse_df = self.get_quandl_data("NSE/IBULISL")
        clean_data = []
        # [high, low close]
        for index, row in nse_df.iterrows():
            clean_data.append([row['High'], row['Low'], row['Close']])


        #just price
        price = [item[2] for item in clean_data]
        price_ar = np.array(price)    
            
        r = Renko(10)
        r_t = Renko(10, price_ar)
        
        for event in clean_data:
            r.process_price_event(event[2])
            
        
            
        self.assertEqual(r.getRawData(), r_t.getRawData())
        self.assertEqual(r.getRenkoData(), r_t.getRenkoData())



        
    
if __name__ == '__main__':
    unittest.main()
    
