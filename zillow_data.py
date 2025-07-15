import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#receives a dataframe and returns dataframe with year, mean, and median for each year
def get_mean_median_per_year(df):
    df['year'] = df['date'].dt.year
    summary = df.groupby('year')['value'].agg(['mean', 'median']).reset_index()
    summary = summary.round({'mean': 2, 'median': 0})
    return summary

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

#separate by category
rentals = full_data[full_data['category'] == 'Rentals'].copy()
home_values = full_data[full_data['category'] == 'Home values'].copy()
inv_sales = full_data[full_data['category'] == 'Inventory and sales'].copy()
by_region_type_rentals = rentals[rentals['region_type'] == 'zip'].copy()
by_region_type_home_values = rentals[rentals['region_type'] == 'zip'].copy()
by_zip_rentals = by_region_type_rentals[by_region_type_rentals['region'] in 80227].copy()
by_zip_home_values = by_region_type_home_values[by_region_type_home_values['region'] in 80227].copy()
print(by_zip_rentals)
print(by_zip_home_values)
#get mean, median by year for each category
'''rentals_mean_median = get_mean_median_per_year(rentals)
print(rentals_mean_median)
home_values_mean_median = get_mean_median_per_year(home_values)
print(home_values_mean_median)
inv_sales_mean_median = get_mean_median_per_year(inv_sales)
print(inv_sales_mean_median)


#plot above data
rentals_mean_median.plot(x='year',y=['mean','median'])
plt.title('Rental Prices Over Time')
plt.show()
home_values_mean_median.plot(x='year',y=['mean','median'])
plt.title('Home Values Over Time')
plt.show()
inv_sales_mean_median.plot(x='year',y=['mean','median'])
plt.title('Inventory & Sale Values Over Time')
plt.show()
'''