import os, pickle, quandl
import numpy as np
import pandas as pd
from datetime import datetime
import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as ff

py.init_notebook_mode(connected = True)

#purpose: download and cache a Quandl dataseries
#signature: get_quandle_data(quandl_id: ) -> df: pandas dataframe
## *** quandl API key = WZpC82bNrwpdw59PaRK1
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


# purpose: merge common column of each dataframe into combined dataframe
# signature: merge_dfs_on_column(dataframes: list, labels: list, col: String) 
# -> pd.DataFrame(series_dict): dataframe
def merge_dfs_on_column(dataframes, labels, col):
    series_dict = {labels[i] : dataframes[i][col] for i in range(len(dataframes))}
    return pd.DataFrame(series_dict)

# purpose: 
# signature: df_scatter(df:dataframe, title, seperate_y_axis:Boolean, y_axis_label:String, scale:String, initial_hide:boolean) 
# -> ploty scatter plot
def df_scatter(df, title, seperate_y_axis = False, y_axis_label='', scale='linear', initial_hide=False): 
    label_arr = list(df)
    # lambda to be used for form trace
    series_arr = list(map(lambda col: df[col], label_arr))
    
    # plot layout config
    layout = go.Layout(
        title=title,
        legend=dict(orientation="h"),
        xaxis=dict(type='date'),
        yaxis=dict(
            title=y_axis_label,
            showticklabels= not seperate_y_axis,
            type=scale
        )
    )
    
    y_axis_config = dict(
        overlaying='y',
        showticklabels=False,
        type=scale )
    
    visibility = 'visible'
    if initial_hide:
        visibility = 'legendonly'
        
    # Form Trace for each series
    trace_arr = []
    for index, series in enumerate(series_arr):
        trace = go.Scatter(
            x=series.index, 
            y=series, 
            name=label_arr[index],
            visible=visibility
        )
        
        # add separate axis for series 
        if seperate_y_axis:
            trace['yaxis'] = 'y{}'.format(index + 1)
            layout['yaxis{}'.format(index + 1)] = y_axis_config  
        
        trace_arr.append(trace)
    
    fig = go.Figure(data = trace_arr, layout = layout)
    py.iplot(fig)
    
# purpose: Download and cache JSON data, return as a dataframe.
# signature: get_json_data(json_url:String, cache_path:String)
# -> df: dataframe
def get_json_data(json_url, cache_path): 
    try:        
        f = open(cache_path, 'rb')
        df = pickle.load(f)   
        print('Loaded {} from cache'.format(json_url))
    except (OSError, IOError) as e:
        print('Downloading {}'.format(json_url))
        df = pd.read_json(json_url)
        df.to_pickle(cache_path)
        print('Cached {} at {}'.format(json_url, cache_path))
    return df
    
    
#purpose: retrieve crypto data from poloniex 
#signiture: get_crypto_data(poloniex_pair:String) -> data_df: dataframe
def get_crypto_data(poloniex_pair):
    BASE_POLO_URL = 'https://poloniex.com/public?command=returnChartData&currencyPair={}&start={}&end={}&period={}'
    start_date = datetime.strptime('2015-01-01', '%Y-%m-%d') # get data from start of 2015
    print('START DATE:::', start_date)
    end_date = datetime.now()
    print('END DATE::: ', end_date)
    period = 86400 # pull daily data (86,400 seconds per day)
    
    json_url = BASE_POLO_URL.format(poloniex_pair, start_date.timestamp(), end_date.timestamp(), period)
    #json_url = BASE_POLO_URL.format(poloniex_pair, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), period)
    
    data_df = get_json_data(json_url, poloniex_pair)
    data_df = data_df.set_index('date')
    return data_df

    


#------------- MAIN --------------
# exchange info
exchanges = ['KRAKEN','COINBASE', 'BITSTAMP','ITBIT','OKCOIN', 'GETBTC','COINSBANK']
exch_data = {}

# retrieve exchange data and read into dictionary
for exchange in exchanges:
    exchange_df = get_quandl_data('BCHARTS/{}USD'.format(exchange))
    exch_data[exchange] = exchange_df
    
# Merge BTC price data series' into single dataframe
btc_usd_datasets = merge_dfs_on_column(list(exch_data.values()), list(exch_data.keys()), 'Weighted Price')
btc_usd_datasets.replace(0, np.nan, inplace = True) # remove 0 values

# Plot all of the BTC EXCHANGE prices
df_scatter(btc_usd_datasets, 'Bitcoin Price (USD) by Exchange')

# Calc avg in new column
btc_usd_datasets['avg_btc_price_usd'] = btc_usd_datasets.mean(axis = 1)

#plot the average price 
btc_trace = go.Scatter(x=btc_usd_datasets.index, y = btc_usd_datasets['avg_btc_price_usd'])
py.iplot([btc_trace])

# retreive alternate coin data
altcoins = ['ETH','LTC','XRP','ETC','STR','DASH','SC','XMR','XEM', 'GNT']
alt_data = {}

#change dir to poloniex_cache & create dir if it doesn't exist 
if not 'poloniex_cache' in os.listdir(os.getcwd()):
    os.mkdir('poloniex_cache')
    
path = os.path.join(os.getcwd(), 'poloniex_cache')
os.chdir(path)

for alt in altcoins:
    coinpair = 'BTC_{}'.format(alt)
    crypto_price_df = get_crypto_data(coinpair)
    alt_data[alt] = crypto_price_df

os.chdir('../')

# calculate USD Price as new col in each dataframe
for alt in alt_data.keys():
    alt_data[alt]['price_usd'] = alt_data[alt]['weightedAverage'] * btc_usd_datasets['avg_btc_price_usd']

# merge price into single dataframe
combined_df = merge_dfs_on_column(list(alt_data.values()), list(alt_data.keys()), 'price_usd')
# add BTC to the dataframe
combined_df['BTC'] = btc_usd_datasets['avg_btc_price_usd']
# chart alt coins (LOG)
df_scatter(combined_df, 'Alternate Currency Prices (USD)', seperate_y_axis = False, y_axis_label = 'Coin Value (USD)', scale = 'linear')

