import pandas as pd

zillow_indicators = pd.read_csv('ZILLOW_INDICATORS.csv', dtype= {'indicator_id': 'string', 'indicator': 'string', 'category': 'string'})
zillow_regions = pd.read_csv('ZILLOW_REGIONS.csv', dtype= {'region_id': 'int', 'region_type': 'string', 'region': 'string'})

zillow_indicators = zillow_indicators.replace({",":""}, regex=True)
zillow_regions = zillow_regions.replace({",":""}, regex=True)

zillow_indicators.to_csv('ZILLOW_INDICATORS_CLEANED.csv', index=False)
zillow_regions.to_csv('ZILLOW_REGIONS_CLEANED.csv', index=False)