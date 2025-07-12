import pandas as pd
import numpy as np

#read in data
df = pd.read_csv('ZILLOW_DATA.csv',dtype={'indicator_id':'category','region_id':'category'},parse_dates=['date'])
indicators = pd.read_csv('ZILLOW_INDICATORS.csv', dtype='category')
regions = pd.read_csv('ZILLOW_REGIONS.csv', dtype='category')

#set indexes
indicators.set_index('indicator_id', inplace=True)
regions.set_index('region_id', inplace=True)
df.set_index(['indicator_id','region_id'],inplace=True)

#merge datasets
full_data = df.join([indicators,regions])
print(full_data['category'].unique())